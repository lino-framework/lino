# -*- coding: UTF-8 -*-
# Copyright 2011-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""
The :xfile:`models.py` module for `lino.modlib.outbox`.
"""
from builtins import str
from builtins import object

import logging
logger = logging.getLogger(__name__)

import os

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.core.exceptions import ValidationError


from lino import mixins
from lino.api import dd
from lino.core import actions

from lino.utils.html2text import html2text
from django.core.mail import EmailMultiAlternatives
from lino.modlib.gfks.mixins import Controllable
from lino.modlib.users.mixins import UserAuthored
from lino.modlib.office.roles import OfficeUser, OfficeStaff

from .choicelists import RecipientTypes


@dd.python_2_unicode_compatible
class Recipient(dd.Model):

    """
    Abstract base for :class:`inbox.Recipient` and :class:`outbox.Recipient`.
    """
    allow_cascaded_delete = ['mail']

    class Meta(object):
        verbose_name = _("Recipient")
        verbose_name_plural = _("Recipients")
    mail = models.ForeignKey('outbox.Mail')
    partner = models.ForeignKey('contacts.Partner',
                                #~ verbose_name=_("Recipient"),
                                blank=True, null=True)
    type = RecipientTypes.field(
        default=RecipientTypes.to.as_callable)
    address = models.EmailField(_("Address"), blank=True)
    name = models.CharField(_("Name"), max_length=200)

    def name_address(self):
        return '%s <%s>' % (self.name, self.address)

    def __str__(self):
        #~ return "[%s]" % unicode(self.name or self.address)
        return str(self.name or self.address)
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
    required_roles = dd.required(OfficeStaff)
    model = Recipient
    #~ column_names = 'mail  type *'
    #~ order_by = ["address"]


class RecipientsByMail(Recipients):
    required_roles = dd.required(OfficeUser)
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
                     actions.ShowDetailAction)  # but not from InsertRow

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
            msg += ', '.join([str(r) for r in missing_addresses])
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

        elem.sent = timezone.now()
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


@dd.python_2_unicode_compatible
class Mail(UserAuthored, mixins.Printable,
           mixins.ProjectRelated, Controllable):

    class Meta(object):
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

    def __str__(self):
        return u'%s #%s' % (self._meta.verbose_name, self.pk)

    def get_recipients(self, rr):
        #~ recs = []
        recs = [str(r) for r in
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
    required_roles = dd.required(OfficeStaff)
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
    required_roles = dd.required(OfficeUser)

    label = _("My Outbox")
    master_key = 'user'

    @classmethod
    def setup_request(self, ar):
        if ar.master_instance is None:
            ar.master_instance = ar.get_user()
        #~ print "20120519 MyOutbox.setup_request()", ar.master_instance
        super(MyOutbox, self).setup_request(ar)


class MailsByController(Mails):
    required_roles = dd.required()
    master_key = 'owner'
    auto_fit_column_widths = True
    #~ label = _("Postings")
    #~ slave_grid_format = 'summary'


class MailsByUser(Mails):
    required_roles = dd.required()
    label = _("Outbox")
    column_names = 'sent subject recipients'
    #~ order_by = ['sent']
    order_by = ['-date']
    master_key = 'user'

if settings.SITE.project_model is not None:

    class MailsByProject(Mails):
        required_roles = dd.required()
        label = _("Outbox")
        column_names = 'date subject recipients user *'
        #~ order_by = ['sent']
        order_by = ['-date']
        master_key = 'project'


class SentByPartner(Mails):
    """Shows the Mails that have been sent to a given Partner.
    """
    required_roles = dd.required()
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


@dd.python_2_unicode_compatible
class Attachment(Controllable):

    allow_cascaded_delete = ['mail']

    class Meta(object):
        verbose_name = _("Attachment")
        verbose_name_plural = _("Attachments")

    mail = models.ForeignKey('outbox.Mail')

    def __str__(self):
        if self.owner_id:
            return str(self.owner)
        return str(self.id)

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
    required_roles = dd.required(OfficeStaff)
    model = Attachment
    #~ window_size = (400,500)
    #~ detail_layout = """
    #~ mail owner
    #~ """


class AttachmentsByMail(Attachments):
    required_roles = dd.required(OfficeUser)
    master_key = 'mail'
    slave_grid_format = 'summary'


class AttachmentsByController(Attachments):
    master_key = 'owner'


dd.update_field(Mail, 'user', verbose_name=_("Sender"))
