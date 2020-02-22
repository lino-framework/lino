# -*- coding: UTF-8 -*-
# Copyright 2011-2020 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

from lino.modlib.notify.api import send_notification, send_global_chat
from lino.utils.format_date import fds
from lino.modlib.office.roles import OfficeUser
from lino.modlib.users.mixins import UserAuthored, My
from lino.modlib.gfks.mixins import Controllable
from lino.modlib.memo.mixins import Previewable
from lino.mixins import Created, ObservedDateRange,BabelNamed, Referrable
#from lino_noi.lib.groups.models import Group
from lino.core.site import html2text
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
logger = logging.getLogger(__name__)


html_parser = etree.HTMLParser()


def groupname(s):
    # Remove any invalid characters from the given string so that it can
    # be used as a Redis group name.
    # "Group name must be a valid unicode string containing only
    # alphanumerics, hyphens, or periods."

    s = s.replace('@', '-')
    return s.encode('ascii', 'ignore')

class ChatGroup(UserAuthored, Created, Referrable, BabelNamed):

    class Meta(object):
        app_label = 'chat'
        verbose_name = _("Chat group")
        verbose_name_plural = _("Chat groups")
        ordering = ['created', 'id']
    title = dd.CharField(max_length=20)
    description = dd.RichTextField(max_length=200)

    @dd.action(_("ChatsGroupChats"))
    def getGroupChats(self, ar):
        if self.id:
             obj = [self]
        else:
            obj = ChatGroup.objects.prefetch_related('messages').all()[:10]
        rows = []
        for c in obj:
            messages = []
            all_messages = c.messages.all()[:10]
            last_ten = reversed(all_messages)
            for m in last_ten:
                messages.append((m.user.username, ar.parse_memo(m.body), m.created, m.seen, m.pk, m.user.id))
            rows.append({
                'name': c.name,
                'id':c.id,
                'messages':messages
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
        'chat.ChatGroup', blank=True, null=True,  verbose_name=_(u'Group'), related_name="messages")
    #body = dd.RichTextField(_("Body"), editable=False, format='html')

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
        logger.info("Sending Message %s:#%s" % (self.user, self.pk))
        send_global_chat(**message)
        self.sent = timezone.now()
        self.save()

    @classmethod
    def markAsSeen(Cls, data):
        msg_ids = data['body']
        oldMsg = Cls.objects.filter(pk__in=msg_ids,seen__isnull=True)
        oldMsg.update(seen=timezone.now())

    @classmethod
    def onRecive(Cls, data):
        args = dict(
            user=data['user'],
            body=data['body']['body'],
            group_id=data['body']['group_id'],
        )
        newMsg = Cls(**args)
        newMsg.full_clean()
        newMsg.save()
        newMsg.after_ui_create()
        newMsg.send_global_message()

    def after_ui_create(self, *args):
        # print(self)

        #Place holder
        self.group=dd.resolve_model("chat.ChatGroup").objects.all()[0]
        self.save()

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
        unseen = ChatProps.objects.filter(user=ar.get_user(), chat=self, seen__isnull=True).order_by('-created').select_related("chat")

        last_ten_in_ascending_order = reversed(last_ten_seen)
        unseen_in_ascending_order = reversed(unseen)
        rows = [
            [(c.chat.user.username, ar.parse_memo(c.chat.body), c.chat.created, c.seen, c.chat.pk, c.chat.user.id) for c in last_ten_in_ascending_order],
            [(c.chat.user.username, ar.parse_memo(c.chat.body), c.chat.created, c.seen, c.chat.pk, c.chat.user.id)for c in unseen_in_ascending_order]
        ]
        return ar.success(rows=rows)


class ChatProps(UserAuthored, Created):
    class Meta(object):
        app_label = 'chat'
        # verbose_name = _("Chat message")
        # verbose_name_plural = _("Chat messages")
        ordering = ['user', 'chat']
    chat = dd.ForeignKey(ChatMessage)
    seen = models.DateTimeField(_("seen"), null=True, editable=False, default=None)




