# -*- coding: UTF-8 -*-
# Copyright 2011-2020 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

from lino.modlib.notify.api import send_notification, send_global_chat
from lino.utils.format_date import fds
from lino.modlib.office.roles import OfficeUser
from lino.modlib.users.mixins import UserAuthored, My
from lino.modlib.gfks.mixins import Controllable
from lino.modlib.memo.mixins import Previewable
from lino.mixins import Created, ObservedDateRange, BabelNamed, Referrable
# from lino_noi.lib.groups.models import Group
from lino.core.site import html2text
from lino.core.requests import BaseRequest
from lino.core.gfks import gfk2lookup
from lino.api import dd, rt, _
from lino import DJANGO2
from etgen.html import E, tostring
from django.utils import translation
from django.utils import timezone
from django.conf import settings
from django.db import models
from datetime import timedelta
from datetime import datetime
from lxml import etree
from io import StringIO
import json
import logging

from django.core.serializers.json import DjangoJSONEncoder

logger = logging.getLogger(__name__)

html_parser = etree.HTMLParser()


def groupname(s):
    # Remove any invalid characters from the given string so that it can
    # be used as a Redis group name.
    # "Group name must be a valid unicode string containing only
    # alphanumerics, hyphens, or periods."

    s = s.replace('@', '-')
    return s.encode('ascii', 'ignore')


class ChatGroup(UserAuthored, Created, Referrable):
    class Meta(object):
        app_label = 'chat'
        verbose_name = _("Chat group")
        verbose_name_plural = _("Chat groups")
        ordering = ['created', 'id']

    title = dd.CharField(max_length=20)
    description = dd.RichTextField(max_length=200, blank=True, null=True);
    ticket = dd.ForeignKey("tickets.Ticket", blank=True, null=True);

    @dd.action(_("getChatGroups"))
    def getChatGroups(self, ar):
        """
        Returns info on all GroupChats for this user.
        """
        qs = ChatGroupMember.objects.filter(user=ar.get_user()).select_related("group")

        rows = [{"id": cp.group.pk,
                 "title": cp.group.title,
                 "unseen": cp.group.get_unseen_count(ar)} for cp in qs]

        return ar.success(rows=rows)

    def get_unseen_count(self, ar):
        """
        Returns count of messages that haven't been seen yet."""
        return ChatProps.objects.filter(chat__group=self, user=ar.get_user(), seen__isnull=True).count()

    @dd.action(_("Load GroupChat"))
    def loadGroupChat(self, ar):
        """Returns chat messages for a given chat"""
        rows = []
        if 'mk' in ar.rqdata:
            # master = rt.models.resolve("contenttypes.ContentType").get(pk=ar.rqdata['mt']).get(pk=ar.rqdata["mk"])
            ar.selected_rows = [ChatGroup.objects.get(ticket__pk=ar.rqdata['mk'])]
        for group in ar.selected_rows:
             last_ten = ChatProps.objects.filter(user=ar.get_user(),
                                                chat__group=group
                                                ).order_by(
                '-created').select_related("chat")
             rows.append({
                'title': group.title,
                'id': group.id,
                'messages': [cp.serialize(ar) for cp in last_ten]
            })
        return ar.success(rows=rows)


class ChatGroupMember(Created):
    class Meta(object):
        app_label = 'chat'

    user = dd.ForeignKey(
        'users.User',
        verbose_name=_("Author"),
        related_name="ChatGroups",
        blank=True, null=True)

    group = dd.ForeignKey(ChatGroup,

                          related_name="ChatGroupsMembers",
                          )


class ChatMessage(UserAuthored, Created, Previewable):
    class Meta(object):
        app_label = 'chat'
        verbose_name = _("Chat message")
        verbose_name_plural = _("Chat messages")
        ordering = ['created', 'id']

    # message_type = MessageTypes.field(default="change")

    seen = models.DateTimeField(_("seen"), null=True, editable=False)
    sent = models.DateTimeField(_("sent"), null=True, editable=False)
    group = dd.ForeignKey(
        'chat.ChatGroup', blank=True, null=True, verbose_name=_(u'Group'), related_name="messages")
    hash = dd.CharField(_("Hash"), max_length=25, null=True, blank=True)

    # body = dd.RichTextField(_("Body"), editable=False, format='html')

    def __str__(self):
        return "{}: {}".format(self.user, self.body)

        # return _("About {0}").format(self.owner)

    # return self.message
    # return _("Notify {0} about change on {1}").format(
    #     self.user, self.owner)

    def send_global_message(self):
        # message = {
        #     "id": self.pk,
        #     # "subject": str(self.subject),
        #     "user": self.user,
        #     "body": html2text(self.body),
        #     "created": self.created.strftime("%a %d %b %Y %H:%M"),
        # }
        logger.info("Sending Message %s:#%s" % (self.user, self.pk))
        send_global_chat(self)
        # self.sent = timezone.now()
        # self.save()

    @classmethod
    def markAsSeen(Cls, data):
        group_id = data['body'][0]
        # msg_ids = [chat[3] for chat in data['body'][1]]
        ChatProps.objects.filter(chat__group__pk=group_id, user=data['user'], seen__isnull=True).update(seen=timezone.now())


    @classmethod
    def onRecive(Cls, data):
        print(data)
        args = dict(
            user=data['user'],
            body=data['body']['body'],
            group_id=data['body']['group_id'],
            hash=data['body']['hash']
        )
        newMsg = Cls(**args)
        newMsg.full_clean()
        newMsg.save()
        newMsg.after_ui_create()
        newMsg.send_global_message()

    def after_ui_create(self, *args):
        for sub in self.group.ChatGroupsMembers.all().select_related("user"):
            props = ChatProps(chat=self, user=sub.user)
            props.full_clean()
            props.save()

        # super(ChatMessage, self).after_ui_save()

    @dd.action(_("ChatsMsg"))
    def getChats(self, ar):
        # return ar.success(rows=[])

        # doto, have work.
        last_ten_seen = ChatProps.objects.filter(seen__isnull=False).order_by('-created').select_related("chat")[:10]
        unseen = ChatProps.objects.filter(user=ar.get_user(), chat=self, seen__isnull=True).order_by(
            '-created').select_related("chat")

        last_ten_in_ascending_order = reversed(last_ten_seen)
        unseen_in_ascending_order = reversed(unseen)
        rows = [
            [(c.chat.user.username, ar.parse_memo(c.chat.body), c.chat.created, c.seen, c.chat.pk, c.chat.user.id) for c
             in last_ten_in_ascending_order],
            [(c.chat.user.username, ar.parse_memo(c.chat.body), c.chat.created, c.seen, c.chat.pk, c.chat.user.id) for c
             in unseen_in_ascending_order]
        ]
        return ar.success(rows=rows)


class ChatProps(UserAuthored, Created):
    class Meta(object):
        app_label = 'chat'
        # verbose_name = _("Chat message")
        # verbose_name_plural = _("Chat messages")
        ordering = ['user', 'chat']

    def serialize(self, ar=None):
        if ar is None:
            ar = BaseRequest()
        return (
        self.chat.user.username,
        ar.parse_memo(self.chat.body),
        json.loads(json.dumps(self.created, cls=DjangoJSONEncoder)),
        json.loads(json.dumps(self.seen, cls=DjangoJSONEncoder)),
        self.chat.pk,
        self.chat.user.id,
        self.chat.group.id,
        self.chat.hash,
        self.chat.ticket.id if self.chat.ticket else None,
        )

    chat = dd.ForeignKey(ChatMessage, related_name="chatProps")
    seen = models.DateTimeField(_("seen"), null=True, editable=False, default=None)
    sent = models.DateTimeField(_("sent"), null=True, editable=False, default=None)
