# Copyright 2011-2017 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""Utilities for authentication. Adapted from `django.contrib.auth`.

"""
from __future__ import unicode_literals
from builtins import object

from django.conf import settings
from django.utils.crypto import constant_time_compare
from django.utils.module_loading import import_string

from lino.utils import SimpleSingleton

class AnonymousUser(SimpleSingleton):
    """A singleton class whose instance will be assigned to the
    :attr:`user` attribute of anonymous incoming requests, similar to
    Django's approach.

    See also :attr:`lino.core.site.Site.anonymous_user_type`.

    """
    authenticated = False
    """This is always `False`.
    See also :attr:`lino.modlib.users.models.User.authenticated`.
    """
    is_active = False

    email = None
    username = 'anonymous'
    modified = None
    partner = None
    language = None
    readonly = True
    pk = None
    time_zone =  None
    notify_myself = False
    user_type = None
    
    def __init__(self):
        settings.SITE.startup()
        from lino.modlib.users.choicelists import UserTypes
        self.user_type = UserTypes.get_by_name(self.username, None)

    # @classmethod
    # def instance(cls):
    #     if cls._instance is None:
    #         # Call startup() to fill UserTypes also in a
    #         # multi-threaded environment:
    #         settings.SITE.startup()
    #         cls._instance = cls()
    #         from lino.modlib.users.choicelists import UserTypes
    #         cls._instance.user_type = UserTypes.get_by_name(
    #             'anonymous', None)
    #         # cls._instance.user_type = UserTypes.get_by_value(
    #         #     settings.SITE.anonymous_user_type, None)
    #         # if cls._instance.user_type is None:
    #         #     raise Exception(
    #         #         "Invalid value %r for `SITE.anonymous_user_type`. "
    #         #         "Must be one of %s" % (
    #         #             settings.SITE.anonymous_user_type,
    #         #             [i.value for i in list(UserTypes.items())]))
    #     return cls._instance

    def __str__(self):
        return self.username

    def get_typed_instance(self, model):
        # 20131022 AttributeError at /api/outbox/MyOutbox : 'AnonymousUser'
        # object has no attribute 'get_typed_instance'
        return self
    
    def get_username(self):
        return self.username
    
    def get_preferences(self):
        """Return the preferences of this user. The returned object is a
        :class:`lino.core.userprefs.UserPrefs` object.

        """
        from lino.core import userprefs
        return userprefs.reg.get(self)
    
    def is_authenticated(self):
        return False
    
    def has_perm(self, perm, obj=None):
        return False
    
    def has_perms(self, perm_list, obj=None):
        for perm in perm_list:
            if not self.has_perm(perm, obj):
                return False
        return True

    def get_choices_text(self, request, actor, field):
        return str(self)

# copied from django.contrib.auth:

# SESSION_KEY = '_auth_user_id'
# BACKEND_SESSION_KEY = '_auth_user_backend'
# HASH_SESSION_KEY = '_auth_user_hash'
# REDIRECT_FIELD_NAME = 'next'

# # copied from django.contrib.auth.models
# SESSION_KEY = '_auth_user_id'
# BACKEND_SESSION_KEY = '_auth_user_backend'
# HASH_SESSION_KEY = '_auth_user_hash'
# REDIRECT_FIELD_NAME = 'next'

# def load_backend(path):
#     return import_string(path)()


# def get_user_model():
#     # from lino.api import rt
#     # rt.models.users.User
#     return settings.SITE.user_model

# # copied from django.contrib.auth
# def _get_user_session_key(request):
#     # This value in the session is always serialized to a string, so we need
#     # to convert it back to Python whenever we access it.
#     return get_user_model()._meta.pk.to_python(request.session[SESSION_KEY])


# # adapted copy of django.contrib.auth.get_user
# def get_user(request):
#     """
#     Returns the user model instance associated with the given request session.
#     If no user is retrieved an instance of `AnonymousUser` is returned.
#     """
#     user = None
#     try:
#         user_id = _get_user_session_key(request)
#         backend_path = request.session[BACKEND_SESSION_KEY]
#     except KeyError:
#         pass
#     else:
#         if backend_path in settings.AUTHENTICATION_BACKENDS:
#             backend = load_backend(backend_path)
#             user = backend.get_user(user_id)
#             # Verify the session
#             if ('django.contrib.auth.middleware.SessionAuthenticationMiddleware'
#                 in settings.MIDDLEWARE_CLASSES and hasattr(user, 'get_session_auth_hash')):
#                 session_hash = request.session.get(HASH_SESSION_KEY)
#                 session_hash_verified = session_hash and constant_time_compare(
#                     session_hash,
#                     user.get_session_auth_hash()
#                 )
#                 if not session_hash_verified:
#                     request.session.flush()
#                     user = None

#     return user or AnonymousUser()

