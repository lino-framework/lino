import functools
import json

from channels import Channel
from channels import Group
from channels.sessions import channel_session, http_session
# from channels.auth import channel_session_user, channel_session_user_from_http
from django.conf import settings
from django.utils import timezone
from django.utils.module_loading import import_string
from django.utils.crypto import constant_time_compare

from lino.modlib.notify.models import Message
from lino.modlib.users.utils import AnonymousUser

# copied from django.contrib.auth.models
SESSION_KEY = '_auth_user_id'
BACKEND_SESSION_KEY = '_auth_user_backend'
HASH_SESSION_KEY = '_auth_user_hash'
REDIRECT_FIELD_NAME = 'next'


def load_backend(path):
    return import_string(path)()


def get_user_model():
    # from lino.api import rt
    # rt.models.users.User
    return settings.SITE.user_model


# adapted copy of django.contrib.auth.models
def _get_user_session_key(request):
    # This value in the session is always serialized to a string, so we need
    # to convert it back to Python whenever we access it.
    return get_user_model()._meta.pk.to_python(request.session[SESSION_KEY])


# adapted copy of django.contrib.auth.models
def get_user(request):
    """
    Returns the user model instance associated with the given request session.
    If no user is retrieved an instance of `AnonymousUser` is returned.
    """
    user = None
    try:
        user_id = _get_user_session_key(request)
        backend_path = request.session[BACKEND_SESSION_KEY]
    except KeyError:
        pass
    else:
        if backend_path in settings.AUTHENTICATION_BACKENDS:
            backend = load_backend(backend_path)
            user = backend.get_user(user_id)
            # Verify the session
            if ('django.contrib.auth.middleware.SessionAuthenticationMiddleware'
                in settings.MIDDLEWARE_CLASSES and hasattr(user, 'get_session_auth_hash')):
                session_hash = request.session.get(HASH_SESSION_KEY)
                session_hash_verified = session_hash and constant_time_compare(
                    session_hash,
                    user.get_session_auth_hash()
                )
                if not session_hash_verified:
                    request.session.flush()
                    user = None

    return user or AnonymousUser()


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
    message_id = message['message_id']
    message = Message.objects.get(pk=message_id )
    message.seen = timezone.now()
    message.save()


@channel_session_user
def user_connected(message):
    username = message['username']
    Group(username).add(message.reply_channel)
    # Not need any more
    # message.reply_channel.send({
    #     "text": username,
    # })
