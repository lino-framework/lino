# -*- coding: UTF-8 -*-
# Copyright 2011-2017 Luc Saffre
# License: BSD (see file COPYING for details)

"""Database models for this plugin.

"""
from __future__ import unicode_literals
from builtins import str
from builtins import object
import json

from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils import translation

from lino.api import dd, rt, _
from lino.api import pgettext

#from lino.core.roles import SiteStaff
from lino.core.gfks import gfk2lookup
#from lino.core.requests import BaseRequest
from lino.core.site import html2text

from lino.mixins import Created, ObservedDateRange
from lino.modlib.gfks.mixins import Controllable
from lino.modlib.notify.consumers import PUBLIC_GROUP
from lino.modlib.users.mixins import UserAuthored, My
from lino.modlib.office.roles import OfficeStaff, OfficeUser
from lino.mixins.bleached import body_subject_to_elems

from lino.utils.format_date import fds
from lino.utils.xmlgen.html import E
from lino.utils import join_elems

from datetime import timedelta

from .choicelists import MessageTypes, MailModes

import logging
logger = logging.getLogger(__name__)

def groupname(s):
    """Remove any invalid characters from the given string so that it can
    be used as a Redis group name.

    "Group name must be a valid unicode string containing only
    alphanumerics, hyphens, or periods."

    """
    s = s.replace('@', '-')
    return s.encode('ascii', 'ignore')

class MarkAllSeen(dd.Action):
    select_rows = False
    http_method = 'POST'

    label = _("Mark all as seen")

    def run_from_ui(self, ar):
        qs = rt.models.notify.Message.objects.filter(
            user=ar.get_user(), seen__isnull=True)

        def ok(ar):
            for obj in qs:
                obj.seen = timezone.now()
                obj.save()
            ar.success(refresh_all=True)

        ar.confirm(
            ok,
            _("Mark {} notifications as seen.").format(qs.count()),
            _("Are you sure?"))


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


@dd.python_2_unicode_compatible
class Message(UserAuthored, Controllable, Created):
    """A **Notification message** is a instant message sent by the
    application to a given user.

    Applications can either use it indirectly by sublassing
    :class:`ChangeObservable
    <lino.modlib.notify.mixins.ChangeObservable>` or by directly
    calling the class method :meth:`create_message` to create a new
    message.


    .. attribute:: subject
    .. attribute:: body
    .. attribute:: user

        The recipient.

    .. attribute:: owner
 
       The database object which controls this message. 

       This may be `None`, which means that the message has no
       controller. When a notification is controlled, then the
       recipient will receive only the first message for that object.
       Any following message is ignored until the recipient has
       "confirmed" the first message. Typical use case are the
       messages emitted by :class:`ChangeObservable`: you don't want
       to get 10 mails just because a colleague makes 10 small
       modifications when authoring the text field of a
       ChangeObservable object.

    .. attribute:: created
    .. attribute:: sent
    .. attribute:: seen

    """

    class Meta(object):
        app_label = 'notify'
        verbose_name = _("Notification message")
        verbose_name_plural = _("Notification messages")

    message_type = MessageTypes.field()
    seen = models.DateTimeField(_("seen"), null=True, editable=False)
    sent = models.DateTimeField(_("sent"), null=True, editable=False)
    body = dd.RichTextField(_("Body"), editable=False, format='html')
    mail_mode = MailModes.field(default=MailModes.often.as_callable)
    subject = models.CharField(
        _("Subject"), max_length=250, editable=False)

    def __str__(self):
        return "{} #{}".format(self.message_type, self.id)

        # return _("About {0}").format(self.owner)

    # return self.message
    # return _("Notify {0} about change on {1}").format(
    #     self.user, self.owner)

    @classmethod
    def emit_message(
            cls, ar, owner, message_type, msg_func, recipients):
        """Create one database object for every recipient.

        `recipients` is a list of `(user, mail_mode)` tuples. Items
        with duplicate or empty user are removed.

        `msg_func` is a callable expected to return a tuple (subject,
        body). It is called for each recipient (in the recipient's
        language).

        The changing user does not get notified about their own
        changes, except when working as another user.

        """
        # dd.logger.info("20160717 %s emit_messages()", self)
        # remove recipients without user:
        if ar is None:
            me = None
        else:
            me = ar.get_user()
        others = set()
        for user, mm in recipients:
            if user:
                if me is None or me.notify_myself or user != me:
                    others.add((user, mm))

        if len(others):
            # subject = "{} by {}".format(message_type, me)
            # dd.logger.info(
            #     "Notify %s users about %s", len(others), subject)
            for user, mm in others:
                if mm is None:
                    mm = MailModes.often
                with dd.translation.override(user.language):
                    subject_body = msg_func(user, mm)
                    if subject_body is not None:
                        subject, body = subject_body
                        cls.create_message(
                            user, owner, body=body,
                            subject=subject,
                            mail_mode=mm, message_type=message_type)

    @classmethod
    def create_message(cls, user, owner=None, **kwargs):
        """Create a message unless that user has already been notified
        about that object.

        """
        if owner is not None:
            fltkw = gfk2lookup(cls.owner, owner)
            qs = cls.objects.filter(
                user=user, seen__isnull=True, **fltkw)
            if qs.exists():
                return
        obj = cls(user=user, owner=owner, **kwargs)
        obj.full_clean()
        obj.save()
        if settings.SITE.use_websockets:
            obj.send_browser_message(user)

    # @dd.displayfield(_("Subject"))
    # def subject_more(self, ar):
    #     if ar is None:
    #         return ''
    #     elems = [self.subject]
    #     if self.body:
    #         elems.append(' ')
    #         # elems.append(ar.obj2html(self, _("(more)")))
    #         elems.append(E.raw(self.body))
    #     # print 20160908, elems
    #     return E.p(*elems)

    # @dd.displayfield(_("Overview"))
    # def overview(self, ar):
    #     if ar is None:
    #         return ''
    #     return self.get_overview(ar)

    # def get_overview(self, ar):
    #     """Return the content to be displayed in the :attr:`overview` field.
    #     On interactive rendererers (extjs, bootstrap3) the `obj` and
    #     `user` are clickable.

    #     This is also used from the :xfile:`notify/body.eml` template
    #     where they should just be surrounded by **double asterisks**
    #     so that Thunderbird displays them bold.

    #     """
    #     elems = body_subject_to_elems(ar, self.subject, self.body)
    #     return E.div(*elems)
    #     # context = dict(
    #     #     obj=ar.obj2str(self.owner),
    #     #     user=ar.obj2str(self.user))
    #     # return _(self.message).format(**context)
    #     # return E.p(
    #     #     ar.obj2html(self.owner), " ",
    #     #     _("was modified by {0}").format(self.user))

    def unused_send_individual_email(self):
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
        if self.owner is None:
            subject = str(self)
        else:
            subject = pgettext("notification", "{} in {}").format(
                self.message_type, self.owner)
        subject = settings.EMAIL_SUBJECT_PREFIX + subject
        # template = rt.get_template('notify/body.eml')
        # context = dict(obj=self, E=E, rt=rt, ar=sar)
        # body = template.render(**context)

        template = rt.get_template('notify/individual.eml')
        context = dict(obj=self, E=E, rt=rt)
        body = template.render(**context)

        sender = settings.SERVER_EMAIL
        rt.send_email(subject, sender, body, [self.user.email])
        self.sent = timezone.now()
        self.save()

    # for testing, set show_in_workflow to True:
    # @dd.action(label=_("Send e-mail"),
    #            show_in_bbar=False, show_in_workflow=False,
    #            button_text="✉")  # u"\u2709"
    # def do_send_email(self, ar):
    #     self.send_individual_email()

    # @dd.action(label=_("Seen"),
    #            show_in_bbar=False, show_in_workflow=True,
    #            button_text="✓")  # u"\u2713"
    # def mark_seen(self, ar):
    #     self.seen = timezone.now()
    #     self.save()
    #     ar.success(refresh_all=True)

    mark_all_seen = MarkAllSeen()
    mark_seen = MarkSeen()
    clear_seen = ClearSeen()

    @classmethod
    def send_summary_emails(cls, mm):
        """Send summary emails for all pending notifications with the given
        mail_mode `mm`.

        """
        qs = cls.objects.filter(sent__isnull=True)
        qs = qs.exclude(user__email='')
        qs = qs.filter(mail_mode=mm).order_by('user')
        if qs.count() == 0:
            return
        from lino.core.renderer import MailRenderer
        ar = rt.login(renderer=MailRenderer())
        context = ar.get_printable_context()
        sender = settings.SERVER_EMAIL
        template = rt.get_template('notify/summary.eml')
        users = dict()
        for obj in qs:
            lst = users.setdefault(obj.user, [])
            lst.append(obj)
        dd.logger.debug(
            "Send out %s summaries for %d users.", mm, len(users))
        for user, messages in users.items():
            with translation.override(user.language):
                if len(messages) == 1:
                    subject = messages[0].subject
                else:
                    subject = _("{} notifications").format(len(messages))
                subject = settings.EMAIL_SUBJECT_PREFIX + subject
                context.update(user=user, messages=messages)
                body = template.render(**context)
                # dd.logger.debug("20170112 %s", body)
                rt.send_email(subject, sender, body, [user.email])
                for msg in messages:
                    msg.sent = timezone.now()
                    msg.save()


    def send_browser_message_for_all_users(self, user):
        """
        Send_message to all connected users
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
        Group(PUBLIC_GROUP).send({
            # WebSocket text frame, with JSON content
            "text": json.dumps(message),
        })

        return

    def send_browser_message(self, user):
        """
        Send_message to the user's browser
        """

        message = {
            "id": self.id,
            "subject": str(self.subject),
            "body": html2text(self.body),
            "created": self.created.strftime("%a %d %b %Y %H:%M"),
        }

        # Encode and send that message to the whole channels Group for our
        # Websocket. Note how you can send to a channel or Group from any part
        # of Django, not just inside a consumer.
        from channels import Group
        logger.info("Sending browser notification to %s", user.username)
        Group(groupname(user.username)).send({
            # WebSocket text frame, with JSON content
            "text": json.dumps(message),
        })

        return


dd.update_field(Message, 'user',
                verbose_name=_("Recipient"), editable=False)
# Message.update_controller_field(
#     null=True, blank=True, verbose_name=_("About"))

dd.inject_field(
    'users.User', 'notify_myself',
    models.BooleanField(
        _('Notify myself'), default=False))

dd.inject_field(
    'users.User', 'mail_mode',
    MailModes.field(
        _('Email notification mode'),
        default=MailModes.often.as_callable))


class Messages(dd.Table):
    "Base for all tables of messages."
    model = 'notify.Message'
    column_names = "created subject user seen sent *"
    # cell_edit = False

    # detail_layout = dd.DetailLayout("""
    # created user seen sent owner
    # overview
    # """, window_size=(50, 15))

    parameters = ObservedDateRange(
        # user=dd.ForeignKey(
        #     settings.SITE.user_model,
        #     blank=True, null=True),
        show_seen=dd.YesNo.field(_("Seen"), blank=True),
    )

    params_layout = "user show_seen start_date end_date"

    # @classmethod
    # def get_simple_parameters(cls):
    #     for p in super(Messages, cls).get_simple_parameters():
    #         yield p
    #     yield 'user'

    @classmethod
    def get_request_queryset(self, ar, **filter):
        qs = super(Messages, self).get_request_queryset(ar, **filter)
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
    required_roles = dd.login_required(dd.SiteAdmin)


class MyMessages(My, Messages):
    """Shows messages emitted to you."""
    # label = _("My messages")
    required_roles = dd.login_required(OfficeUser)
    # column_names = "created subject owner sent workflow_buttons *"
    column_names = "created subject message_type workflow_buttons *"
    order_by = ['-created']
    # hide_headers = True
    slave_grid_format = 'summary'
    # slave_grid_format = 'list'
    # slave_grid_format = 'grid'

    @classmethod
    def get_slave_summary(cls, mi, ar):
        qs = rt.models.notify.Message.objects.filter(
            user=ar.get_user()).order_by('created')
        qs = qs.filter(seen__isnull=True)
        # mark_all = rt.models.notify.MyMessages.get_action_by_name(
        #     'mark_all_seen')
        # html = E.tostring(ar.action_button(mark_all, None))
        # TODO: make action_button() work with list actions
        html = ''
        ba = rt.models.notify.MyMessages.get_action_by_name('mark_seen')

        def fmt(obj):
            s = E.tostring(ar.action_button(ba, obj))
            s += fds(obj.created) + " " + obj.created.strftime(
                settings.SITE.time_format_strftime) + " "
            if obj.body:
                s += ar.parse_memo(obj.body)
            else:
                s += ar.parse_memo(obj.subject)
            # s += obj.body
            return "<li>{}</li>".format(s)

        items = []
        for obj in qs:
            items.append(fmt(obj))
        return html + "<ul>{}</ul>".format(''.join(items))

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
        table at the beginning of :meth:`get_dashboard_items`.

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


# h = settings.EMAIL_HOST
# if not h or h.endswith('example.com'):
#     dd.logger.debug(
#         "Won't send pending messages because EMAIL_HOST is %r",
#         h)

@dd.schedule_often(every=10)
def send_pending_emails_often():
    rt.models.notify.Message.send_summary_emails(MailModes.often)

@dd.schedule_daily()
def send_pending_emails_daily():
    rt.models.notify.Message.send_summary_emails(MailModes.daily)
    
# @dd.schedule_often(every=10)
# def send_pending_emails_often():
#     Message = rt.models.notify.Message
#     qs = Message.objects.filter(sent__isnull=True)
#     qs = qs.filter(user__mail_mode=MailModes.immediately)
#     if qs.count() > 0:
#         dd.logger.debug(
#             "Send out emails for %d messages.", qs.count())
#         for obj in qs:
#             obj.send_individual_email()
#     else:
#         dd.logger.debug("No messages to send.")


remove_after = dd.plugins.notify.remove_after

if remove_after:
    
    @dd.schedule_daily()
    def clear_seen_messages():
        # Daily task which deletes messages older than X hours.

        Message = rt.models.notify.Message
        qs = Message.objects.filter(
            created__lt=timezone.now() - timedelta(hours=remove_after))
        if dd.plugins.notify.keep_unseen: 
            qs = qs.filter(seen__isnull=False)
        if qs.count() > 0:
            dd.logger.info(
                "Removing %d messages older than %d hours.",
                qs.count(), remove_after)
            qs.delete()


import warnings
warnings.filterwarnings(
    "ignore", "You do not have a working installation of the service_identity module: .* Many valid certificate/hostname mappings may be rejected.",
    UserWarning)
        
