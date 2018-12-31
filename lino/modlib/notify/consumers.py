import functools
import json

from channels import Channel
from channels import Group
from channels.sessions import channel_session, http_session
# from channels.auth import channel_session_user, channel_session_user_from_http
from django.utils import timezone

from lino.core.auth import BACKEND_SESSION_KEY, SESSION_KEY, HASH_SESSION_KEY
from lino.core.auth import get_user
from lino.core.auth.utils import AnonymousUser
from .mixins import PUBLIC_GROUP


# adapted copy from channels.auth
def transfer_user(from_session, to_session):
    """
    Transfers user from HTTP session to channel session.
    """
    if BACKEND_SESSION_KEY in from_session and \
                    SESSION_KEY in from_session and \
                    HASH_SESSION_KEY in from_session:
        to_session[BACKEND_SESSION_KEY] = from_session[BACKEND_SESSION_KEY]
        to_session[SESSION_KEY] = from_session[SESSION_KEY]
        to_session[HASH_SESSION_KEY] = from_session[HASH_SESSION_KEY]


# adapted copy from channels.auth
def channel_session_user(func):
    """
    Presents a message.user attribute obtained from a user ID in the channel
    session, rather than in the http_session. Turns on channel session implicitly.
    """

    @channel_session
    @functools.wraps(func)
    def inner(message, *args, **kwargs):
        # If we didn't get a session, then we don't get a user
        if not hasattr(message, "channel_session"):
            raise ValueError("Did not see a channel session to get auth from")
        if message.channel_session is None:
            # Inner import to avoid reaching into models before load complete
            message.user = AnonymousUser()
        # Otherwise, be a bit naughty and make a fake Request with just
        # a "session" attribute (later on, perhaps refactor contrib.auth to
        # pass around session rather than request)
        else:
            fake_request = type("FakeRequest", (object,), {"session": message.channel_session})
            message.user = get_user(fake_request)
        # Run the consumer
        return func(message, *args, **kwargs)

    return inner


# adapted copy from channels.auth
def http_session_user(func):
    """
    Wraps a HTTP or WebSocket consumer (or any consumer of messages
    that provides a "COOKIES" attribute) to provide both a "session"
    attribute and a "user" attibute, like AuthMiddleware does.

    This runs http_session() to get a session to hook auth off of.
    If the user does not have a session cookie set, both "session"
    and "user" will be None.
    """

    @http_session
    @functools.wraps(func)
    def inner(message, *args, **kwargs):
        # If we didn't get a session, then we don't get a user
        if not hasattr(message, "http_session"):
            raise ValueError("Did not see a http session to get auth from")
        if message.http_session is None:
            # Inner import to avoid reaching into models before load complete
            message.user = AnonymousUser()
        # Otherwise, be a bit naughty and make a fake Request with just
        # a "session" attribute (later on, perhaps refactor contrib.auth to
        # pass around session rather than request)
        else:
            fake_request = type("FakeRequest", (object,), {"session": message.http_session})
            message.user = get_user(fake_request)
        # Run the consumer
        return func(message, *args, **kwargs)

    return inner


# adapted copy from channels.auth
def channel_session_user_from_http(func):
    """
    Decorator that automatically transfers the user from HTTP sessions to
    channel-based sessions, and returns the user as message.user as well.
    Useful for things that consume e.g. websocket.connect
    """

    @http_session_user
    @channel_session
    @functools.wraps(func)
    def inner(message, *args, **kwargs):
        if message.http_session is not None:
            transfer_user(message.http_session, message.channel_session)
        return func(message, *args, **kwargs)

    return inner


# This decorator copies the user from the HTTP session (only available in
# websocket.connect or http.request messages) to the channel session (available
# in all consumers with the same reply_channel, so all three here)
@channel_session_user_from_http
def ws_connect(message):
    Group(PUBLIC_GROUP).add(message.reply_channel)


@channel_session_user_from_http
def ws_disconnect(message):
    Group(PUBLIC_GROUP).discard(message.reply_channel)


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
    message_id = message['message_id']
    from lino.modlib.notify.models import Message
    message = Message.objects.get(pk=message_id)
    message.seen = timezone.now()
    message.save()


@channel_session_user
def user_connected(message):
    if message.get('text', False):
        payload = json.loads(message['text'])
        Group(payload['username']).add(message.reply_channel)
        print (payload['username'], "is connected")
    # Not need any more
    # message.reply_channel.send({
    #     "text": username,
    # })
