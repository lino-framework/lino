from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

import json

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
