# -*- coding: UTF-8 -*-
# Copyright 2011-2020 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

import logging ; logger = logging.getLogger(__name__)
import json
from io import StringIO
from lxml import etree
from datetime import timedelta

from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils import translation
from etgen.html import E, tostring

from lino import DJANGO2
from lino.api import dd, rt, _

# from lino.core.roles import SiteStaff
from lino.core.gfks import gfk2lookup
# from lino.core.requests import BaseRequest
from lino.core.site import html2text

from lino.mixins import Created, ObservedDateRange
from lino.modlib.gfks.mixins import Controllable
# from lino.modlib.notify.consumers import PUBLIC_GROUP
from lino.modlib.users.mixins import UserAuthored, My
from lino.modlib.office.roles import OfficeUser

from lino.utils.format_date import fds

from lino.modlib.notify.api import send_notification, send_global_chat

html_parser = etree.HTMLParser()

def groupname(s):
    # Remove any invalid characters from the given string so that it can
    # be used as a Redis group name.
    # "Group name must be a valid unicode string containing only
    # alphanumerics, hyphens, or periods."

    s = s.replace('@', '-')
    return s.encode('ascii', 'ignore')

class ChatMessage(UserAuthored, Created):
    class Meta(object):
        app_label = 'chat'
        verbose_name = _("Chat message")
        verbose_name_plural = _("Chat messages")
        ordering = ['created', 'id']

    # message_type = MessageTypes.field(default="change")

    # seen = models.DateTimeField(_("seen"), null=True, editable=False)
    # sent = models.DateTimeField(_("sent"), null=True, editable=False)
    body = dd.RichTextField(_("Body"), editable=False, format='html')

    def __str__(self):
        return "{}: {}".format(self.user, self.body)

        # return _("About {0}").format(self.owner)

    # return self.message
    # return _("Notify {0} about change on {1}").format(
    #     self.user, self.owner)

    def send_global_message(self):

        message = {
            "id": self.pk,
            # "subject": str(self.subject),
            "user": self.user,
            "body": html2text(self.body),
            "created": self.created.strftime("%a %d %b %Y %H:%M"),
        }
        logger.info("Sending Message %s:#%s"%(self.user, self.pk))
        send_global_chat(**message)

    @classmethod
    def onRecive(Cls, data):
        args = dict(
            user= data['user'],
            body=data['body']
        )
        newMsg = Cls(**args)
        print(newMsg)
        newMsg.full_clean()
        newMsg.save()
        newMsg.send_global_message()


# TODO Status table
# Each row should be a 1 to many relation with Chatmessage
# One row for each user x message that they should get.
# If row doesn't exist, we assume SEEN READ and DELIVERED
# If after a certain age, it's none, then we forward a notification to notify contianing all missed chats




# dd.update_field(Message, 'user',
#                 verbose_name=_("Recipient"), editable=False)
# Message.update_controller_field(
#     null=True, blank=True, verbose_name=_("About"))
#
# dd.inject_field(
#     'users.User', 'notify_myself',
#     models.BooleanField(_('Notify myself'), default=False))
#
# dd.inject_field(
#     'users.User', 'mail_mode',
#     MailModes.field(default=MailModes.as_callable('often')))


class ChatMessages(dd.Table):
    model = 'chat.ChatMessage'
    column_names = "created user body *"
    # cell_edit = False

    detail_layout = dd.DetailLayout("""
     user 
     body
    """, window_size=(50, 15))

    parameters = ObservedDateRange(
        # user=dd.ForeignKey(
        #     settings.SITE.user_model,
        #     blank=True, null=True),
        # show_seen=dd.YesNo.field(_("Seen"), blank=True),
    )

    params_layout = "user start_date end_date"

    # @classmethod
    # def get_simple_parameters(cls):
    #     for p in super(Messages, cls).get_simple_parameters():
    #         yield p
    #     yield 'user'

    @classmethod
    def get_request_queryset(self, ar, **filter):
        qs = super(ChatMessages, self).get_request_queryset(ar, **filter)
        # pv = ar.param_values
        #
        # if pv.show_seen == dd.YesNo.yes:
        #     qs = qs.filter(seen__isnull=False)
        # elif pv.show_seen == dd.YesNo.no:
        #     qs = qs.filter(seen__isnull=True)
        return qs

    @dd.action("getChats")
    def getChats(self, ar):
        # doto, have work.
        return ar.success(rows=[(c.user, c.body) for c in ChatMessage.objects.order_by("created")[:10]])

# class AllMessages(Messages):
#     required_roles = dd.login_required(dd.SiteAdmin)


# class MyMessages(My, ChatMessages):
#     # label = _("My messages")
#     required_roles = dd.login_required(OfficeUser)
#     # column_names = "created subject owner sent workflow_buttons *"
#     column_names = "created subject message_type workflow_buttons *"
#     created_order = "-created"
#     order_by = [created_order]
#     # hide_headers = True
#     display_mode = 'summary'
#
#     # display_mode = 'list'
#     # display_mode = 'grid'
#
#     @classmethod
#     def get_table_summary(cls, mi, ar):
#         qs = rt.models.notify.Message.objects.filter(
#             user=ar.get_user()).order_by(cls.created_order)
#         qs = qs.filter(seen__isnull=True)
#         # mark_all = rt.models.notify.MyMessages.get_action_by_name(
#         #     'mark_all_seen')
#         # html = tostring(ar.action_button(mark_all, None))
#         # TODO: make action_button() work with list actions
#         # html = ''
#         ba = rt.models.notify.MyMessages.get_action_by_name('mark_seen')
#
#         def fmt(obj):
#             s = tostring(ar.action_button(ba, obj))
#             s += fds(obj.created) + " " + obj.created.strftime(
#                 settings.SITE.time_format_strftime) + " "
#             if obj.body:
#                 s += ar.parse_memo(obj.body)
#             else:
#                 s += ar.parse_memo(obj.subject)
#             e = etree.parse(StringIO(s), html_parser)
#             return E.li(E.div(*e.iter()))
#             # s += obj.body
#             # return "<li>{}</li>".format(s)
#
#         items = []
#         for obj in qs:
#             items.append(fmt(obj))
#         return E.ul(*items)
#         # return html + "<ul>{}</ul>".format(''.join(items))
#
#     # filter = models.Q(seen__isnull=True)
#
#     @classmethod
#     def param_defaults(self, ar, **kw):
#         kw = super(MyMessages, self).param_defaults(ar, **kw)
#         kw.update(show_seen=dd.YesNo.no)
#         return kw
#

# h = settings.EMAIL_HOST
# if not h or h.endswith('example.com'):
#     dd.logger.debug(
#         "Won't send pending messages because EMAIL_HOST is %r",
#         h)

# @dd.schedule_often(every=10)
# def send_pending_emails_often():
#     rt.models.notify.Message.send_summary_emails(MailModes.often)
#
#
# @dd.schedule_daily()
# def send_pending_emails_daily():
#     rt.models.notify.Message.send_summary_emails(MailModes.daily)


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


# remove_after = dd.plugins.notify.remove_after
#
# if remove_after:
#
#     @dd.schedule_daily()
#     def clear_seen_messages():
#
#         Message = rt.models.notify.Message
#         qs = Message.objects.filter(
#             created__lt=timezone.now() - timedelta(hours=remove_after))
#         if dd.plugins.notify.keep_unseen:
#             qs = qs.filter(seen__isnull=False)
#         if qs.count() > 0:
#             dd.logger.info(
#                 "Removing %d messages older than %d hours.",
#                 qs.count(), remove_after)
#             qs.delete()
