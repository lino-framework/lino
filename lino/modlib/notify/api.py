# -*- coding: UTF-8 -*-
# Copyright 2020 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

import json

from lino.api import rt
import logging
from django.utils.timezone import now
logger = logging.getLogger(__name__)

NOTIFICATION = "NOTIFICATION"
CHAT = "CHAT"

NOTIFICATION_TYPES = [
    NOTIFICATION, CHAT
]


def send_notification(user, id, subject, body, created):
    """
    :param user:
    :param id:
    :param subject:
    :param body:
    :param created:
    :return:
    """
    # importing channels at module level would cause certain things to fail
    # when channels isn't installed, e.g. `manage.py prep` in `lino_book.projects.workflows`.
    from channels.layers import get_channel_layer
    from asgiref.sync import async_to_sync

    msg = dict(
        type=NOTIFICATION,
        subject=subject,
        id=id,
        body=body,
        created=created,
    )

    try:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(str(user.pk),
                                                {"type": "send_notification",  # method name in consumer
                                                 "text": json.dumps(msg)})  # data

    except Exception as E:
        logger.exception(E)


def send_global_chat(message):
    """
    Sends a WS message to each user using ChatProps"""
    from channels.layers import get_channel_layer
    from asgiref.sync import async_to_sync

    for chat in message.chatProps.all():
        msg = dict(
            type=CHAT,
            chat=chat.serialize())

        try:
            assert bool(chat.user)
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(str(chat.user.pk),
                                                    {"type": "send_notification",
                                                     # just pointer to method name in consumer
                                                     "text": json.dumps(msg)})  # data
            chat.sent = now()
            chat.save()
        except Exception as E:
            logger.exception(E)
