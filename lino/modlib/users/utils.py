# Copyright 2011-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""Utilities for :mod:`lino.modlib.users`.

.. autosummary::

"""
from __future__ import unicode_literals

import logging
logger = logging.getLogger(__name__)

from django.conf import settings

from .choicelists import UserProfiles


class AnonymousUser(object):
    """
    Similar to Django's approach to represent anonymous visitors
    as a special kind of user.
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
    #~ id = None
    pk = None

    _instance = None

    @classmethod
    def instance(cls):
        if cls._instance is None:
            # Call startup() to fill UserProfiles also in a
            # multi-threaded environment:
            settings.SITE.startup()
            cls._instance = AnonymousUser()
            cls._instance.profile = UserProfiles.get_by_value(
                settings.SITE.anonymous_user_profile, None)
            if cls._instance.profile is None:
                raise Exception(
                    "Invalid value %r for `SITE.anonymous_user_profile`. "
                    "Must be one of %s" % (
                        settings.SITE.anonymous_user_profile,
                        [i.value for i in UserProfiles.items()]))
        return cls._instance

    def __str__(self):
        return self.username

    def get_typed_instance(self, model):
        # 20131022 AttributeError at /api/outbox/MyOutbox : 'AnonymousUser'
        # object has no attribute 'get_typed_instance'
        return self
