# Copyright 2011-2016 Luc Saffre
# License: BSD (see file COPYING for details)

"""Utilities for :mod:`lino.modlib.users`.

.. autosummary::

"""
from __future__ import unicode_literals
from builtins import object

from django.conf import settings
from lino.core import userprefs


class AnonymousUser(object):
    """A singleton class whose instance will be assigned to the
    :attr:`user` attribute of anonymous incoming requests, similar to
    Django's approach.

    See also :attr:`lino.core.site.Site.anonymous_user_type`.

    """
    authenticated = False
    """This is always `False`.
    See also :attr:`lino.modlib.users.models.User.authenticated`.
    """

    email = None
    username = 'anonymous'
    modified = None
    partner = None
    language = None
    readonly = True
    pk = None
    timezone = None

    _instance = None

    @classmethod
    def instance(cls):
        if cls._instance is None:
            # Call startup() to fill UserTypes also in a
            # multi-threaded environment:
            settings.SITE.startup()
            cls._instance = AnonymousUser()
            from lino.modlib.users.choicelists import UserTypes
            cls._instance.profile = UserTypes.get_by_value(
                settings.SITE.anonymous_user_type, None)
            if cls._instance.profile is None:
                raise Exception(
                    "Invalid value %r for `SITE.anonymous_user_type`. "
                    "Must be one of %s" % (
                        settings.SITE.anonymous_user_type,
                        [i.value for i in list(UserTypes.items())]))
        return cls._instance

    def __str__(self):
        return self.username

    def get_typed_instance(self, model):
        # 20131022 AttributeError at /api/outbox/MyOutbox : 'AnonymousUser'
        # object has no attribute 'get_typed_instance'
        return self
    
    def get_preferences(self):
        """Return the preferences of this user. The returned object is a
        :class:`lino.core.userprefs.UserPrefs` object.

        """
        return userprefs.reg.get(self)
    
