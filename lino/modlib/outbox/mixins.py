# -*- coding: UTF-8 -*-
# Copyright 2011-2015 Luc Saffre
# License: BSD (see file COPYING for details)
"Model mixins for :mod:`lino.modlib.outbox`."
from builtins import str
from builtins import object


import logging
logger = logging.getLogger(__name__)


from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from lino.api import dd, rt
from lino.core import actions


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

    class Meta(object):
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
        return dd.plugins.jinja.list_templates('.eml.html', *tplgroups)


class CreateMail(dd.Action):

    """
    Creates an outbox mail and displays it.
    """
    url_action_name = 'email'
    icon_name = 'email_add'
    help_text = _('Create an email from this')
    label = _('Create email')

    callable_from = (actions.GridEdit,
                     actions.ShowDetailAction)  # but not from InsertRow

    def get_action_permission(self, ar, obj, state):
        """This action is not available:
        
        - when the user has not email address

        - on an obj whose MailableType is empty or has no
          :attr:`MailableType.email_template` configured

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

        m = rt.modules.outbox.Mail(
            user=ar.get_user(),
            date=dd.today(),
            subject=elem.get_mailable_subject(),
            owner=elem)
        #~ if as_attachment:
        m.body = elem.get_mailable_intro(ar)
        m.full_clean()
        m.save()
        Recipient = rt.modules.outbox.Recipient
        for t, p in elem.get_mailable_recipients():
            r = Recipient(mail=m, type=t, partner=p)
            r.full_clean()
            r.save()
        if as_attachment:
            a = rt.modules.outbox.Attachment(mail=m, owner=elem)
            a.save()
        js = ar.renderer.instance_handler(ar, m)
        kw.update(eval_js=js)
        ar.success(**kw)


class Mailable(dd.Model):

    """Mixin for models that provide a "Post" button.  A Mailable model
    must also inherit from :class:`mixins.Printable` or some subclass
    thereof.

    """

    class Meta(object):
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
                env = settings.SITE.plugins.jinja.renderer.jinja_env
                tpl = env.get_template(group+"/"+name)
                context = self.get_printable_context(ar)
                return ar.render_jinja(tpl, **context)

    def get_mailable_subject(self):
        """Return the content of the `subject` field for the email to be
        created.

        """
        return str(self)


