# -*- coding: UTF-8 -*-
# Copyright 2011-2018 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

from __future__ import unicode_literals

import json
from builtins import object
from builtins import str
from io import StringIO

from lxml import etree

from lino import DJANGO2

html_parser = etree.HTMLParser()

from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils import translation

from lino.api import dd, rt, _

# from lino.core.roles import SiteStaff
from lino.core.gfks import gfk2lookup
# from lino.core.requests import BaseRequest
from lino.core.site import html2text

from lino.mixins import Created, ObservedDateRange
from lino.modlib.gfks.mixins import Controllable
# from lino.modlib.notify.consumers import PUBLIC_GROUP
from .mixins import PUBLIC_GROUP
from lino.modlib.users.mixins import UserAuthored, My
from lino.modlib.office.roles import OfficeUser

from lino.utils.format_date import fds
from etgen.html import E, tostring

from datetime import timedelta

from .choicelists import MessageTypes, MailModes

import logging

logger = logging.getLogger(__name__)


def groupname(s):
    # Remove any invalid characters from the given string so that it can
    # be used as a Redis group name.
    # "Group name must be a valid unicode string containing only
    # alphanumerics, hyphens, or periods."

    s = s.replace('@', '-')
    return s.encode('ascii', 'ignore')


class MarkAllSeen(dd.Action):
    select_rows = False
    http_method = 'POST'
    show_in_plain = True

    label = _("Mark all as seen")
    button_text = "✓"  # u"\u2713"

    def run_from_ui(self, ar, **kwargs):
        qs = rt.models.notify.Message.objects.filter(
            user=ar.get_user(), seen__isnull=True)
        for obj in qs:
            obj.seen = timezone.now()
            obj.save()
        ar.success(eval_js='window.top.document.querySelectorAll(".' + ar.actor.actor_id.replace(".","-") + '")[0].classList.add("dashboard-item-closed"); console.log("lel")')



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
    class Meta(object):
        app_label = 'notify'
        verbose_name = _("Notification message")
        verbose_name_plural = _("Notification messages")
        ordering = ['created', 'id']

    message_type = MessageTypes.field(default="change")
    seen = models.DateTimeField(_("seen"), null=True, editable=False)
    sent = models.DateTimeField(_("sent"), null=True, editable=False)
    body = dd.RichTextField(_("Body"), editable=False, format='html')
    mail_mode = MailModes.field(default=MailModes.as_callable('often'))
    subject = models.CharField(
        _("Subject"), max_length=250, editable=False)

    def __str__(self):
        return "{} #{}".format(self.message_type, self.id)

        # return _("About {0}").format(self.owner)

    # return self.message
    # return _("Notify {0} about change on {1}").format(
    #     self.user, self.owner)

    @classmethod
    def emit_notification(
            cls, ar, owner, message_type, msg_func, recipients):
        # recipients = list(recipients)
        # dd.logger.info(
        #     "20180612 %s emit_notification() for %d recipients",
        #     owner, len(recipients))

        # remove recipients without user:
        if ar is None:
            me = None
        else:
            me = ar.get_user()
        others = set()
        for user, mm in recipients:
            if user is not None and mm != MailModes.silent:
                if user.user_type is None:
                    continue
                if me is None or me.notify_myself or user != me:
                    others.add((user, mm))

        if len(others):
            # rr = message_type.required_roles
            # subject = "{} by {}".format(message_type, me)
            # dd.logger.info(
            #     "20180612 Notify %s users", len(others))
            for user, mm in sorted(others, key=lambda x: x[0].username):
                # if not user.user_type.has_required_roles(rr):
                if message_type in user.user_type.mask_message_types:
                    continue
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

    mark_all_seen = MarkAllSeen()
    mark_seen = MarkSeen()
    clear_seen = ClearSeen()

    @classmethod
    def send_summary_emails(cls, mm):
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

        message = {
            "id": self.id,
            "subject": self.subject,
            "body": html2text(self.body),
            "created": self.created.strftime("%a %d %b %Y %H:%M"),
        }

        # Encode and send that message to the whole channels Group for our
        # liveblog. Note how you can send to a channel or Group from any part
        # of Django, not just inside a consumer.
        if not DJANGO2:
            from channels import Group
            Group(PUBLIC_GROUP).send({
                # WebSocket text frame, with JSON content
                "text": json.dumps(message),
            })
        else:
            from channels.layers import get_channel_layer
            channel_layer = get_channel_layer()
            from asgiref.sync import async_to_sync
            async_to_sync(channel_layer.group_send)(PUBLIC_GROUP, {"text": json.dumps(message)})

        return

    def send_browser_message(self, user):

        message = {
            "id": self.id,
            "subject": str(self.subject),
            "body": html2text(self.body),
            "created": self.created.strftime("%a %d %b %Y %H:%M"),
        }

        # Encode and send that message to the whole channels Group for our
        # Websocket. Note how you can send to a channel or Group from any part
        # of Django, not just inside a consumer.
        logger.info("Sending browser notification to %s", user.username)
        if not DJANGO2:
            from channels import Group
            Group(groupname(user.username)).send({
                # WebSocket text frame, with JSON content
                "text": json.dumps(message),
            })
        else:
            from channels.layers import get_channel_layer
            channel_layer = get_channel_layer()
            from asgiref.sync import async_to_sync
            async_to_sync(channel_layer.group_send)(user.username, {"type": "send.notification",
                                                                    "text": message['body']})

        return


dd.update_field(Message, 'user',
                verbose_name=_("Recipient"), editable=False)
# Message.update_controller_field(
#     null=True, blank=True, verbose_name=_("About"))

dd.inject_field(
    'users.User', 'notify_myself',
    models.BooleanField(_('Notify myself'), default=False))

dd.inject_field(
    'users.User', 'mail_mode',
    MailModes.field(default=MailModes.as_callable('often')))


class Messages(dd.Table):
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
            yield str(pv.show_seen)

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
    required_roles = dd.login_required(dd.SiteAdmin)


class MyMessages(My, Messages):
    # label = _("My messages")
    required_roles = dd.login_required(OfficeUser)
    # column_names = "created subject owner sent workflow_buttons *"
    column_names = "created subject message_type workflow_buttons *"
    created_order = "-created"
    order_by = [created_order]
    # hide_headers = True
    display_mode = 'summary'

    # display_mode = 'list'
    # display_mode = 'grid'

    @classmethod
    def get_table_summary(cls, mi, ar):
        qs = rt.models.notify.Message.objects.filter(
            user=ar.get_user()).order_by(cls.created_order)
        qs = qs.filter(seen__isnull=True)
        # mark_all = rt.models.notify.MyMessages.get_action_by_name(
        #     'mark_all_seen')
        # html = tostring(ar.action_button(mark_all, None))
        # TODO: make action_button() work with list actions
        # html = ''
        ba = rt.models.notify.MyMessages.get_action_by_name('mark_seen')

        def fmt(obj):
            s = tostring(ar.action_button(ba, obj))
            s += fds(obj.created) + " " + obj.created.strftime(
                settings.SITE.time_format_strftime) + " "
            if obj.body:
                s += ar.parse_memo(obj.body)
            else:
                s += ar.parse_memo(obj.subject)
            e = etree.parse(StringIO(s), html_parser)
            return E.li(E.div(*e.iter()))
            # s += obj.body
            # return "<li>{}</li>".format(s)

        items = []
        for obj in qs:
            items.append(fmt(obj))
        return E.ul(*items)
        # return html + "<ul>{}</ul>".format(''.join(items))

    # filter = models.Q(seen__isnull=True)

    @classmethod
    def param_defaults(self, ar, **kw):
        kw = super(MyMessages, self).param_defaults(ar, **kw)
        kw.update(show_seen=dd.YesNo.no)
        return kw


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
    "ignore",
    "You do not have a working installation of the service_identity module: .* Many valid certificate/hostname mappings may be rejected.",
    UserWarning)
