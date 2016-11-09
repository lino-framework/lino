import json

from channels import Channel
from channels import Group
from channels.auth import channel_session_user, channel_session_user_from_http
from django.utils import timezone
from lino.modlib.notify.models import Notification


# This decorator copies the user from the HTTP session (only available in
# websocket.connect or http.request messages) to the channel session (available
# in all consumers with the same reply_channel, so all three here)
@channel_session_user_from_http
def ws_connect(message):
    pass


def ws_receive(message):
    # All WebSocket frames have either a text or binary payload; we decode the
    # text part here assuming it's JSON.
    # You could easily build up a basic framework that did this encoding/decoding
    # for you as well as handling common errors.
    payload = json.loads(message['text'])
    payload['reply_channel'] = message.content['reply_channel']
    Channel("notify.receive").send(payload)


@channel_session_user
def set_notification_as_seen(message):
    notification_id = message['notification_id']
    notif = Notification.objects.get(pk=notification_id)
    notif.seen = timezone.now()
    notif.save()


@channel_session_user
def user_connected(message):
    username = message['username']
    Group(username).add(message.reply_channel)
    message.reply_channel.send({
        "text": username,
    })
