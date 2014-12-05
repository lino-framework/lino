# -*- coding: UTF-8 -*-
# Copyright 2011-2014 Luc Saffre
# License: BSD (see file COPYING for details)

"""
The :xfile:`models.py` module for :mod:`lino.modlib.outbox`.
"""

import logging
logger = logging.getLogger(__name__)

import os
import datetime

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError


from lino import mixins
from lino import dd, rt
from lino.core import actions

from lino.utils.html2text import html2text
from django.core.mail import EmailMultiAlternatives
from lino.modlib.contenttypes.mixins import Controllable

from .mixins import RecipientTypes


#~ class MailType(mixins.PrintableType,babel.BabelNamed):
    #~ "Deserves more documentation."

    #~ templates_group = 'mails/Mail'

    #~ class Meta:
        #~ verbose_name = _("Mail Type")
        #~ verbose_name_plural = _('Mail Types')

#~ class MailTypes(dd.Table):
    #~ model = MailType
    #~ column_names = 'name build_method template *'


class MailableType(dd.Model):

    """Mixin for Models that serve as `type` of a :class:`Mailable`.
    Concrete examples are cal.EventType, cal.GuestRole,
    notes.NoteType.

    """
    templates_group = None
    """
    Should contain a string "<app_label>/<Model>" of the Mailable
    being typed by this MailableType. Example::
    
      class NoteType(..., MailableType):
          templates_group = 'notes/Note'
          
      class Note(..., Mailable):
          type = models.ForeignKey(NoteType)

    """

    class Meta:
        abstract = True

    attach_to_email = models.BooleanField(
        _("Attach to email"),
        default=False,
        help_text="""\
Whether the printable file should be attached to the email
when creating an email from a mailable of this type.
""")
    #~ email_as_attachment = models.BooleanField(_("Email as attachment"))

    email_template = models.CharField(
        max_length=200,
        verbose_name=_("Email template"),
        blank=True,
        help_text=_(
            "The name of the file to be used as "
            "template when creating an email from a mailable of this type."))

    @dd.chooser(simple_values=True)
    def email_template_choices(cls):
        tplgroups = cls.get_template_groups()
        return settings.SITE.list_templates('.eml.html', *tplgroups)


class CreateMail(dd.Action):

    """
    Creates an outbox mail and displays it.
    """
    url_action_name = 'email'
    icon_name = 'email_add'
    help_text = _('Create an email from this')
    label = _('Create email')

    callable_from = (actions.GridEdit,
                     actions.ShowDetailAction,
                     actions.ShowEmptyTable)  # but not from InsertRow

    def get_action_permission(self, ar, obj, state):
        """
        This action is not available:
        
        - when the user has not email address
        - on an obj whose MailableType is empty or has no :attr:`MailableType.email_template` configured
        """
        if not ar.get_user().email:
            return False
        if obj is not None:
            mt = obj.get_mailable_type()
            if not mt or not mt.email_template:
                return False
            #~ if obj.attach_to_email(ar) and obj.get_target_name() is None:
            if mt.attach_to_email and not obj.get_target_name():
                return False
        return super(CreateMail, self).get_action_permission(ar, obj, state)

    def run_from_ui(self, ar, **kw):
        elem = ar.selected_rows[0]

        as_attachment = elem.attach_to_email(ar)

        m = Mail(user=ar.get_user(),
                 date=settings.SITE.today(),
                 subject=elem.get_mailable_subject(),
                 owner=elem)
        #~ if as_attachment:
        m.body = elem.get_mailable_intro(ar)
        m.full_clean()
        m.save()
        for t, p in elem.get_mailable_recipients():
            r = Recipient(mail=m, type=t, partner=p)
            r.full_clean()
            r.save()
        if as_attachment:
            a = Attachment(mail=m, owner=elem)
            a.save()
        js = ar.renderer.instance_handler(ar, m)
        kw.update(eval_js=js)
        ar.success(**kw)


class Mailable(dd.Model):

    """Mixin for models that provide a "Post" button.  A Mailable model
    must also inherit from :class:`mixins.Printable` or some subclass
    thereof.

    """

    class Meta:
        abstract = True

    create_mail = CreateMail()

    def get_mailable_type(self):
        raise NotImplementedError()
        #~ return self.type

    def attach_to_email(self, ar):
        return self.get_mailable_type().attach_to_email
        #~ return isinstance(self,mixins.CachedPrintable)

    def get_mailable_intro(self, ar):
        mt = self.get_mailable_type()
        #~ print 20130101, mt.email_template
        name = mt.email_template
        if not name:
            return ''
        for group in self.get_template_groups():
            filename = rt.find_config_file(name, group)
            if filename:
                tpl = settings.SITE.jinja_env.get_template(group+"/"+name)
                context = self.get_printable_context(ar=ar)
                # context = dict(
                #     instance=self,
                # )
                return ar.render_jinja(tpl, **context)

    def get_mailable_subject(self):
        """
        Return the content of the `subject` 
        field for the email to be created.
        """
        return unicode(self)


class Recipient(dd.Model):

    """
    Abstract base for :class:`inbox.Recipient` and :class:`outbox.Recipient`.
    """
    allow_cascaded_delete = ['mail']

    class Meta:
        verbose_name = _("Recipient")
        verbose_name_plural = _("Recipients")
    mail = models.ForeignKey('outbox.Mail')
    partner = models.ForeignKey('contacts.Partner',
                                #~ verbose_name=_("Recipient"),
                                blank=True, null=True)
    type = RecipientTypes.field(default=RecipientTypes.to)
    address = models.EmailField(_("Address"), blank=True)
    name = models.CharField(_("Name"), max_length=200)

    def name_address(self):
        return '%s <%s>' % (self.name, self.address)

    def __unicode__(self):
        #~ return "[%s]" % unicode(self.name or self.address)
        return unicode(self.name or self.address)
        #~ return "[%s]" % unicode(self.address)

    def full_clean(self):
        if self.partner:
            if not self.address:
                self.address = self.partner.email
            if not self.name:
                self.name = self.partner.get_full_name(salutation=False)
        super(Recipient, self).full_clean()

    def get_row_permission(self, ar, state, ba):
        """
        Recipients of a Mail may not be edited if the Mail is read-only.
        """
        if self.mail_id and not self.mail.get_row_permission(ar, state, ba):
            #~ logger.info("20120920 Recipient.get_row_permission()")
            return False
        return super(Recipient, self).get_row_permission(ar, state, ba)


class Recipients(dd.Table):
    required = dd.required(user_level='manager', user_groups='office')
    #~ required_user_level = UserLevels.manager
    model = Recipient
    #~ column_names = 'mail  type *'
    #~ order_by = ["address"]


class RecipientsByMail(Recipients):
    required = dd.required()
    #~ required_user_level = None
    master_key = 'mail'
    column_names = 'partner:20 address:20 name:20 type:10 *'
    #~ column_names = 'type owner_type owner_id'
    #~ column_names = 'type owner'


class SendMail(dd.Action):

    """
    Sends an `outbox.Mail` as an email.
    """

    icon_name = 'email_go'
    url_action_name = 'send'
    label = _('Send email')
    callable_from = (actions.GridEdit,
                     actions.ShowDetailAction,
                     actions.ShowEmptyTable)  # but not from InsertRow

    #~ callable_from = None

    def get_action_permission(self, ar, obj, state):
        if obj is not None and obj.sent:
            return False
        return super(SendMail, self).get_action_permission(ar, obj, state)

    def run_from_ui(self, ar, **kw):
        elem = ar.selected_rows[0]
        #~ if elem.sent:
            #~ return rr.ui.error(message='Mail has already been sent.')
        #~ subject = elem.subject
        #~ sender = "%s <%s>" % (rr.get_user().get_full_name(),rr.get_user().email)
        sender = "%s <%s>" % (elem.user.get_full_name(), elem.user.email)
        #~ recipients = list(elem.get_recipients_to())
        to = []
        cc = []
        bcc = []
        found = False
        missing_addresses = []
        for r in elem.recipient_set.all():
            recipients = None
            if r.type == RecipientTypes.to:
                recipients = to
            elif r.type == RecipientTypes.cc:
                recipients = cc
            elif r.type == RecipientTypes.bcc:
                recipients = bcc
            if recipients is not None:
                if not r.address:
                    missing_addresses.append(r)
                if r.address.endswith('@example.com'):
                    logger.info("20120712 ignored recipient %s",
                                r.name_address())
                else:
                    recipients.append(r.name_address())
                found = True
            #~ else:
                #~ logger.info("Ignoring recipient %s (type %s)",r,r.type)
        if not found:
            return ar.error(_("No recipients found."))
        if len(missing_addresses):
            msg = _("There are recipients without address: ")
            msg += ', '.join([unicode(r) for r in missing_addresses])
            return ar.error(msg, alert=True)
        #~ as_attachment = elem.owner.attach_to_email(rr)
        #~ body = elem.body
        #~ if as_attachment:
            #~ body = elem.body
        #~ else:
            #~ body = elem.owner.get_mailable_body(rr)
        text_content = html2text(elem.body)
        msg = EmailMultiAlternatives(subject=elem.subject,
                                     from_email=sender,
                                     body=text_content,
                                     to=to, bcc=bcc, cc=cc)
        msg.attach_alternative(elem.body, "text/html")
        for att in elem.attachment_set.all():
            #~ if as_attachment or att.owner != elem.owner:
            fn = att.owner.get_target_name()
            if fn is None:
                raise Warning(_("Couldn't find target file of %s") % att.owner)
            msg.attach_file(fn)

        uploads = dd.resolve_app("uploads")
        for up in uploads.UploadsByController.request(elem):
        #~ for up in uploads.Upload.objects.filter(owner=elem):
            fn = os.path.join(settings.MEDIA_ROOT, up.file.name)
            msg.attach_file(fn)

        num_sent = msg.send()

        elem.sent = datetime.datetime.now()
        kw.update(refresh=True)
        #~ msg = "Email %s from %s has been sent to %s." % (
            #~ elem.id,elem.sender,', '.join([
                #~ r.address for r in elem.recipient_set.all()]))
        msg = _("Email %(id)s from %(sender)s has been sent to %(num)d recipients.") % dict(
            id=elem.id, sender=sender, num=num_sent)
        kw.update(message=msg, alert=True)
        #~ for n in """EMAIL_HOST SERVER_EMAIL EMAIL_USE_TLS EMAIL_BACKEND""".split():
            #~ msg += "\n" + n + " = " + unicode(getattr(settings,n))
        logger.info(msg)
        if elem.owner:
            elem.owner.after_send_mail(elem, ar, kw)
        elem.save()
        ar.success(**kw)


class Mail(mixins.AutoUser, mixins.Printable,
           mixins.ProjectRelated, Controllable):

    class Meta:
        verbose_name = _("Outgoing Mail")
        verbose_name_plural = _("Outgoing Mails")

    send_mail = SendMail()

    date = models.DateField(
        verbose_name=_("Date"),
        help_text="""
        The official date to be printed on the document.
        """)

    subject = models.CharField(_("Subject"),
                               max_length=200, blank=True,
                               # null=True
                               )
    body = dd.RichTextField(_("Body"), blank=True, format='html')

    #~ type = models.ForeignKey(MailType,null=True,blank=True)

    #~ sender = models.ForeignKey(settings.SITE.user_model,
        #~ verbose_name=_("Sender"))
        #~ related_name='outmails_by_sender',
        #~ blank=True,null=True)
    sent = models.DateTimeField(null=True, editable=False)

    def on_create(self, ar):
        self.date = settings.SITE.today()
        super(Mail, self).on_create(ar)

    #~ def disabled_fields(self,ar):
        #~ if not self.owner.post_as_attachment:
            #~ return ['body']
        #~ return []
    #~ @classmethod
    #~ def get_model_actions(self,table):
        #~ for x in super(Mail,self).get_model_actions(table): yield x
        #~ yield 'send_mail',SendMail()
    def get_print_language(self):
        if self.user is not None:
            return self.user.language
        return super(Mail, self).get_print_language()

    def __unicode__(self):
        return u'%s #%s' % (self._meta.verbose_name, self.pk)

    def get_recipients(self, rr):
        #~ recs = []
        recs = [unicode(r) for r in
                Recipient.objects.filter(mail=self, type=RecipientTypes.to)]
        return ', '.join(recs)
    recipients = dd.VirtualField(dd.HtmlBox(_("Recipients")), get_recipients)

    def get_row_permission(self, ar, state, ba):
        """
        Mails may not be edited after they have been sent.
        """
        if self.sent and not ba.action.readonly:
            #~ logger.info("20120920 Mail.get_row_permission()")
            return False
        return super(Mail, self).get_row_permission(ar, state, ba)


#~ class MailDetail(dd.FormLayout):
    #~ main = """
    #~ """

class Mails(dd.Table):
    #~ read_access = dd.required(user_level='manager')
    required = dd.required(user_level='manager', user_groups='office')
    model = Mail
    column_names = "sent recipients subject * body"
    hidden_columns = 'body'
    order_by = ["sent"]
    detail_layout = dd.FormLayout("""
    subject project date
    user sent #build_time id owner
    RecipientsByMail:50x5 AttachmentsByMail:20x5 uploads.UploadsByController:20x5
    body:90x10
    """)
    insert_layout = dd.FormLayout("""
    project
    subject
    body
    """, window_size=(60, 20))

if not settings.SITE.project_model:
    Mails.detail_layout.remove_element('project')


class MyOutbox(Mails):
    required = dd.required(user_groups='office')

    label = _("My Outbox")
    master_key = 'user'

    @classmethod
    def setup_request(self, ar):
        if ar.master_instance is None:
            ar.master_instance = ar.get_user()
        #~ print "20120519 MyOutbox.setup_request()", ar.master_instance
        super(MyOutbox, self).setup_request(ar)


class MailsByController(Mails):
    required = dd.required()
    master_key = 'owner'
    #~ label = _("Postings")
    #~ slave_grid_format = 'summary'


class MailsByUser(Mails):
    required = dd.required()
    label = _("Outbox")
    column_names = 'sent subject recipients'
    #~ order_by = ['sent']
    order_by = ['-date']
    master_key = 'user'

if settings.SITE.project_model is not None:

    class MailsByProject(Mails):
        required = dd.required()
        label = _("Outbox")
        column_names = 'date subject recipients user *'
        #~ order_by = ['sent']
        order_by = ['-date']
        master_key = 'project'


class SentByPartner(Mails):
    """Shows the Mails that have been sent to a given Partner. 
    """
    required = dd.required()
    master = 'contacts.Partner'
    label = _("Outbox")
    column_names = 'sent subject user'
    order_by = ['sent']

    @classmethod
    def get_request_queryset(self, ar):
        q1 = Recipient.objects.filter(
            partner=ar.master_instance).values('mail').query
        qs = Mail.objects.filter(id__in=q1)
        qs = qs.order_by('sent')
        return qs


class Attachment(Controllable):

    allow_cascaded_delete = ['mail']

    class Meta:
        verbose_name = _("Attachment")
        verbose_name_plural = _("Attachments")

    mail = models.ForeignKey('outbox.Mail')

    def __unicode__(self):
        if self.owner_id:
            return unicode(self.owner)
        return unicode(self.id)

    def unused_save(self, *args, **kw):
        # see blog/2012/0929
        if not hasattr(self.owner, 'get_target_url'):
            raise ValidationError(
                "Controller %r has no method `get_target_url`." % self.owner)
        super(Attachment, self).save(*args, **kw)

    def summary_row(self, ar, **kw):
        url = self.owner.get_target_url()
        #~ url = ui.build_url(*parts)
        text = url.split('/')[-1]
        return [ar.renderer.href(url, text)]


class Attachments(dd.Table):
    required = dd.required(user_level='manager', user_groups='office')
    model = Attachment
    #~ window_size = (400,500)
    #~ detail_layout = """
    #~ mail owner
    #~ """


class AttachmentsByMail(Attachments):
    required = dd.required(user_groups='office')
    master_key = 'mail'
    slave_grid_format = 'summary'


class AttachmentsByController(Attachments):
    master_key = 'owner'


MODULE_LABEL = _("Outbox")

system = dd.resolve_app('system')


def setup_main_menu(site, ui, profile, m):
    m = m.add_menu("office", system.OFFICE_MODULE_LABEL)
    m.add_action(MyOutbox)


#~ def setup_config_menu(site,ui,user,m):
    #~ if user.level >= UserLevels.manager:
    #~ m  = m.add_menu("outbox",MODULE_LABEL)
    #~ m.add_action(MailTypes)


def setup_explorer_menu(site, ui, profile, m):
    #~ if user.level >= UserLevels.manager:
    m = m.add_menu("office", system.OFFICE_MODULE_LABEL)
    #~ m  = m.add_menu("outbox",MODULE_LABEL)
    m.add_action(Mails)
    m.add_action(Attachments)


dd.update_field(Mail, 'user', verbose_name=_("Sender"))
