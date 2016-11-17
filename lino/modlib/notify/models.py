# -*- coding: UTF-8 -*-
# Copyright 2011-2016 Luc Saffre
# License: BSD (see file COPYING for details)

"""Database models for this plugin.

"""
from __future__ import unicode_literals
# from builtins import str
from builtins import object
import json

from django.db import models
from django.conf import settings
from django.utils import timezone

from lino.api import dd, rt, _

from lino.core.roles import SiteStaff
from lino.core.gfks import gfk2lookup
from lino.core.requests import BaseRequest
from lino.core.site import html2text

from lino.mixins import Created, ObservedPeriod
from lino.modlib.gfks.mixins import Controllable
from lino.modlib.users.mixins import UserAuthored, My
from lino.modlib.office.roles import OfficeStaff, OfficeUser
from lino.mixins.bleached import body_subject_to_elems

from lino.utils.xmlgen.html import E
from lino.utils import join_elems

from datetime import timedelta


class MarkSeen(dd.Action):
    label = _("Mark as seen")
    show_in_bbar = False
    show_in_workflow = True
    button_text = "✓"  # u"\u2713"

    # button_text = u"\u2611"  # BALLOT BOX WITH CHECK

    def get_action_permission(self, ar, obj, state):
        if obj.seen:
            return False
        return super(MarkSeen, self).get_action_permission(ar, obj, state)

    def run_from_ui(self, ar):
        for obj in ar.selected_rows:
            obj.seen = timezone.now()
            obj.save()
        ar.success(refresh_all=True)


class ClearSeen(dd.Action):
    """Mark this message as not yet seen."""
    label = _("Clear seen")
    show_in_bbar = False
    show_in_workflow = True

    # button_text = u"\u2610"  # BALLOT BOX

    def get_action_permission(self, ar, obj, state):
        if not obj.seen:
            return False
        return super(ClearSeen, self).get_action_permission(ar, obj, state)

    def run_from_ui(self, ar):
        for obj in ar.selected_rows:
            obj.seen = None
            obj.save()
        ar.success(refresh_all=True)


# @dd.python_2_unicode_compatible
class Message(UserAuthored, Controllable, Created):
    """A **Message** is a message to a given user about a given
    database object.
    
    Use the class method :meth:`create_message` to create a new
    message (and to skip creation in case that user has already
    been notified about that owner)

    .. attribute:: subject
    .. attribute:: body
    .. attribute:: user

        The recipient.

    .. attribute:: owner
 
       The database object this message is about.
       This field is labelled `About`.

    .. attribute:: created
    .. attribute:: sent
    .. attribute:: seen

    """

    class Meta(object):
        app_label = 'notify'
        verbose_name = _("Message")
        verbose_name_plural = _("Messages")

    seen = models.DateTimeField(_("seen"), null=True, editable=False)
    sent = models.DateTimeField(_("sent"), null=True, editable=False)
    # message = models.TextField(_("Message"), editable=False)
    subject = models.CharField(_("Subject"), max_length=250, editable=False)
    body = models.TextField(_("Body"), editable=False)

    # def __str__(self):
    #     return _("About {0}").format(self.owner)
    # return self.message
    # return _("Notify {0} about change on {1}").format(
    #     self.user, self.owner)

    @classmethod
    def emit_message(cls, ar, owner, subject, body, recipients):
        """Create one message for every recipient.

        Note that the changing user does not get notified about their
        own changes, except when working as another user.

        """
        # dd.logger.info("20160717 %s emit_messages()", self)
        others = set()
        me = ar.get_user()
        for user in recipients:
            if user and user != me:
                others.add(user)

        if len(others):
            dd.logger.info(
                "Notify %s users that %s", len(others), subject)
            for user in others:
                cls.create_message(
                    ar, user, owner, subject=subject, body=body)

    @classmethod
    def create_message(cls, ar, user, owner=None, **kwargs):
        """Create a message unless that user has already been notified
        about that object.

        Does not send an email because that might skiw down response
        time.

        """
        fltkw = gfk2lookup(cls.owner, owner)
        qs = cls.objects.filter(
            user=user, seen__isnull=True, **fltkw)
        if not qs.exists():
            obj = cls(user=user, owner=owner, **kwargs)
            obj.full_clean()
            obj.save()
            if dd.plugins.notify.use_websockets:
                obj.send_browser_message(user)

    @dd.displayfield(_("Subject"))
    def subject_more(self, ar):
        if ar is None:
            return ''
        elems = [self.subject]
        if self.body:
            elems.append(' ')
            # elems.append(ar.obj2html(self, _("(more)")))
            elems.append(E.raw(self.body))
        # print 20160908, elems
        return E.p(*elems)

    @dd.displayfield(_("Overview"))
    def overview(self, ar):
        if ar is None:
            return ''
        return self.get_overview(ar)

    def get_overview(self, ar):
        """Return the content to be displayed in the :attr:`overview` field.
        On interactive rendererers (extjs, bootstrap3) the `obj` and
        `user` are clickable.

        This is also used from the :xfile:`notify/body.eml` template
        where they should just be surrounded by **double asterisks**
        so that Thunderbird displays them bold.

        """
        elems = body_subject_to_elems(ar, self.subject, self.body)
        return E.div(*elems)
        # context = dict(
        #     obj=ar.obj2str(self.owner),
        #     user=ar.obj2str(self.user))
        # return _(self.message).format(**context)
        # return E.p(
        #     ar.obj2html(self.owner), " ",
        #     _("was modified by {0}").format(self.user))

    def send_email(self):
        """"""
        if not self.user.email:
            # debug level because we don't want to see this message
            # every 10 seconds:
            dd.logger.debug("User %s has no email address", self.user)
            return
        # dd.logger.info("20151116 %s %s", ar.bound_action, ar.actor)
        # ar = ar.spawn_request(renderer=dd.plugins.bootstrap3.renderer)
        # sar = BaseRequest(
        #     # user=self.user, renderer=dd.plugins.bootstrap3.renderer)
        #     user=self.user, renderer=settings.SITE.kernel.text_renderer)
        # tpl = dd.plugins.notify.email_subject_template
        # subject = tpl.format(obj=self)
        subject = settings.EMAIL_SUBJECT_PREFIX + self.subject
        # template = rt.get_template('notify/body.eml')
        # context = dict(obj=self, E=E, rt=rt, ar=sar)
        # body = template.render(**context)

        template = rt.get_template('notify/body.eml')
        context = dict(obj=self, E=E, rt=rt)
        body = template.render(**context)

        sender = settings.SERVER_EMAIL
        rt.send_email(subject, sender, body, [self.user.email])
        self.sent = timezone.now()
        self.save()

    @dd.action(label=_("Send e-mail"),
               show_in_bbar=False, show_in_workflow=True,
               button_text="✉")  # u"\u2709"
    def do_send_email(self, ar):
        self.send_email()

    # @dd.action(label=_("Seen"),
    #            show_in_bbar=False, show_in_workflow=True,
    #            button_text="✓")  # u"\u2713"
    # def mark_seen(self, ar):
    #     self.seen = timezone.now()
    #     self.save()
    #     ar.success(refresh_all=True)

    mark_seen = MarkSeen()
    clear_seen = ClearSeen()

    def send_browser_message(self, user):
        """
        Send_message to the user's browser
        """

        message = {
            "id": self.id,
            "subject": self.subject,
            "body": html2text(self.body),
            "created": self.created.strftime("%a %d %b %Y %H:%M"),
        }

        # Encode and send that message to the whole channels Group for our
        # liveblog. Note how you can send to a channel or Group from any part
        # of Django, not just inside a consumer.
        from channels import Group
        Group(user.username).send({
            # WebSocket text frame, with JSON content
            "text": json.dumps(message),
        })

        return


dd.update_field(Message, 'user',
                verbose_name=_("Recipient"), editable=False)
Message.update_controller_field(
    null=True, blank=True, verbose_name=_("About"))

dd.inject_field(
    'users.User', 'notifyme_mode',
    models.BooleanField(
        _('Send messages via e-mail'), default=True))


class Messages(dd.Table):
    "Base for all tables of messages."
    model = 'notify.Message'
    column_names = "created subject user seen sent *"

    # detail_layout = dd.DetailLayout("""
    # created user seen sent owner
    # overview
    # """, window_size=(50, 15))

    parameters = ObservedPeriod(
        user=dd.ForeignKey(
            settings.SITE.user_model,
            blank=True, null=True),
        show_seen=dd.YesNo.field(_("Seen"), blank=True),
    )

    params_layout = "user show_seen start_date end_date"

    @classmethod
    def get_simple_parameters(cls):
        s = super(Messages, cls).get_simple_parameters()
        s.add('user')
        return s

    @classmethod
    def get_request_queryset(self, ar):
        qs = super(Messages, self).get_request_queryset(ar)
        pv = ar.param_values

        if pv.show_seen == dd.YesNo.yes:
            qs = qs.filter(seen__isnull=False)
        elif pv.show_seen == dd.YesNo.no:
            qs = qs.filter(seen__isnull=True)
        return qs

    @classmethod
    def get_title_tags(self, ar):
        for t in super(Messages, self).get_title_tags(ar):
            yield t
        pv = ar.param_values
        if pv.show_seen:
            yield unicode(pv.show_seen)

    @classmethod
    def unused_get_detail_title(self, ar, obj):
        """This was used to set `seen` automatically when a detail was
        shown.

        """
        if obj.seen is None and obj.user == ar.get_user():
            obj.seen = timezone.now()
            obj.save()
            # dd.logger.info("20151115 Marked %s as seen", obj)
        return super(Messages, self).get_detail_title(ar, obj)


class AllMessages(Messages):
    """The gobal list of all messages.

    """
    required_roles = dd.required(dd.SiteAdmin)


class MyMessages(My, Messages):
    """Shows messages emitted to you."""
    # label = _("My messages")
    required_roles = dd.required(OfficeUser)
    # column_names = "created subject owner sent workflow_buttons *"
    column_names = "subject_more workflow_buttons *"
    order_by = ['created']

    # filter = models.Q(seen__isnull=True)

    @classmethod
    def param_defaults(self, ar, **kw):
        kw = super(MyMessages, self).param_defaults(ar, **kw)
        kw.update(show_seen=dd.YesNo.no)
        return kw

    @classmethod
    def unused_get_welcome_messages(cls, ar, **kw):
        """Emits the :message:`You have %d unseen messages.` message.

        This is no longer used, applications should rather yield this
        table at the beginning of :meth:`get_admin_main_items`.

        """
        sar = ar.spawn(cls)
        if not sar.get_permission():
            return
        count = sar.get_total_count()
        if count > 0:
            msg = _("You have %d unseen messages.") % count
            yield ar.href_to_request(sar, msg)


# def welcome_messages(ar):
#     """Yield messages for the welcome page."""

#     Message = rt.models.notify.Message
#     qs = Message.objects.filter(user=ar.get_user(), seen__isnull=True)
#     if qs.count() > 0:
#         chunks = [
#             str(_("You have %d unseen messages: ")) % qs.count()]
#         chunks += join_elems([
#             ar.obj2html(obj, obj.subject) for obj in qs])
#         yield E.span(*chunks)

# dd.add_welcome_handler(welcome_messages)

if dd.plugins.notify.use_websockets:
    @dd.schedule_daily()
    def send_pending_emails_daily():
        send_pending_emails()
else:
    @dd.schedule_often(every=10)
    def send_pending_emails_often():
        send_pending_emails()


def send_pending_emails():
    h = settings.EMAIL_HOST
    if not h or h.endswith('example.com'):
        dd.logger.debug(
            "Won't send pending messages because EMAIL_HOST is %r",
            h)
        return
    Message = rt.models.notify.Message
    qs = Message.objects.filter(sent__isnull=True)
    qs = qs.filter(user__notifyme_mode=True)
    if qs.count() > 0:
        dd.logger.debug(
            "Send out emails for %d messages.", qs.count())
        for obj in qs:
            obj.send_email()
    else:
        dd.logger.debug("No messages to send.")


@dd.schedule_daily()
def clear_seen_messages():
    """Daily task which deletes messages older than 24 hours.

    Currently it deletes *all* messages, regardless of whether
    they have been seen or not.  TODO: make this configurable.

    """
    remove_after = 24
    Message = rt.models.notify.Message
    qs = Message.objects.filter(
        seen__lt=timezone.now() - timedelta(hours=remove_after))
    if False:  # TODO: make this configurable
        qs = qs.filter(seen__isnull=False)
    if qs.count() > 0:
        dd.logger.info(
            "Removing %d messages older than %d hours.",
            qs.count(), remove_after)
        qs.delete()
