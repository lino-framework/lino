# -*- coding: UTF-8 -*-
# Copyright 2020 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

import json

from lino.api import rt

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
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(user.username,
                                            {"type": "send_notification",  # method name in consumer
                                             "text": json.dumps(msg)})  # data

def send_global_chat(id, user, body, created):

    from channels.layers import get_channel_layer
    from asgiref.sync import async_to_sync

    msg = dict(
        type=CHAT,
        id=id,
        body=body,
        created=created,
        user=user.username,
    )

    channel_layer = get_channel_layer()
    for user in rt.models.resolve("users.User").objects.exclude(user_type=None):
            async_to_sync(channel_layer.group_send)(user.username,
                                            {"type": "send_notification",  # method name in consumer
                                             "text": json.dumps(msg)})  # data

