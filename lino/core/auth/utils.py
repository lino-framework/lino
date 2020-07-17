# Copyright 2011-2020 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""Utilities for authentication. Adapted from `django.contrib.auth`.

"""

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
    # authenticated = False

    is_authenticated = False
    """This is always `False`.
    See also :attr:`lino.modlib.users.User.is_authenticated`.
    """

    is_active = False

    email = None
    username = 'anonymous'
    modified = None
    partner = None
    language = None
    readonly = True
    pk = None
    id = None
    time_zone =  None
    notify_myself = False
    user_type = None
    is_anonymous = True

    def __init__(self):
        settings.SITE.startup()
        from lino.modlib.users.choicelists import UserTypes
        self.user_type = UserTypes.get_by_name(self.username, None)

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

    def has_perm(self, perm, obj=None):
        return False

    def has_perms(self, perm_list, obj=None):
        for perm in perm_list:
            if not self.has_perm(perm, obj):
                return False
        return True

    def get_choices_text(self, request, actor, field):
        return str(self)
