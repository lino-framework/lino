# -*- coding: UTF-8 -*-
# Copyright 2016-2018 Rumma & Ko Ltd
# License: BSD, see LICENSE for more details.
"""
The user preferences registry.

Application code should get the preferences for a user by calling
:meth:`lino.modlib.users.User.get_preferences` which returns an object
of this class.

There is one instance per user which will be created upon first
request.

After instantiating a preferences object, Lino calls the
:meth:`setup_user_prefs <lino.core.plugin.Plugin.setup_user_prefs>` of
every installed plugin once on it. This feature is used by
:mod:`lino.modlib.dashboard`).
"""

import threading

from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from .actors import Actor
from .dashboard import ActorItem, DashboardItem
from .utils import obj2unicode

prefs_rlock = threading.RLock()  # Lock() or RLock()?

def get_available_items(user):
    """
    Return a list of all available dasboard items for this user.

    This does not call :meth:`setup_user_prefs` of installed plugins.
    """
    lst = []
    for i in settings.SITE.get_dashboard_items(user):
        if isinstance(i, type) and issubclass(i, Actor):
            i = ActorItem(i)
        elif not isinstance(i, DashboardItem):
            raise Exception("Unsupported dashboard item %r" % i)
        if i.get_view_permission(user.user_type):
            lst.append(i)
    return lst

    
class UserPrefs(object):
    """A volatile object which holds the preferences of a user.

    .. attribute:: dashboard_items

        A list of the items to be displayed in the dashboard (see
        :xfile:`admin_main.html`). Every item is an instance of
        :class:`DashboardItem` or subclass thereof.

    """
    def __init__(self, site, user):
        self.user = user
        self.dashboard_items = get_available_items(self.user)
        # a set of (model, pk) of very locked row
        self.locked_rows = set()
        for p in settings.SITE.installed_plugins:
            p.setup_user_prefs(self)
        settings.SITE.logger.debug(
            "User preferences for %s have been initialized.", self.user)

    def has_row_lock(self, obj):
        k = (obj.__class__, obj.pk)
        return k in self.locked_rows
        
    def lock_row(self, obj):
        k = (obj.__class__, obj.pk)
        if k in reg.locked_rows:
            msg = _("{} is being edited by another user. "
                    "Please try again later.")
            raise Warning(msg.format(obj))
        with prefs_rlock:
            settings.SITE.logger.debug("%s locks %s.%s", self.user, *k)
            reg.locked_rows.add(k)
            self.locked_rows.add(k)
        
    def unlock_row(self, obj):
        k = (obj.__class__, obj.pk)
        if not k in self.locked_rows:
            # silently ignore a request to unlock a row if it wasn't
            # locked.  This can happen e.g. when user click Save on a
            # row that wasn't locked.
            return
        with prefs_rlock:
            settings.SITE.logger.debug(
                "%s releases lock on %s.%s", self.user, *k)
            reg.locked_rows.remove(k)
            self.locked_rows.remove(k)
            obj._disabled_fields = None  # clear cache
        
    def invalidate(self):
        k = self.user.username
        reg.user_prefs.pop(k, None)
        # like del, but no problem if it didn't exist.
        
        
class Registry(object):
    """
    A volatile singleton which holds

    .. attribute:: user_prefs
    .. attribute:: locked_rows

    A set of (model, pk) of very locked row

    """
    def __init__(self):
        self.user_prefs = {}
        self.locked_rows = set()
        
    def get(self, user):
        k = user.username
        prefs = self.user_prefs.get(k, None)
        if prefs is None:
            prefs = UserPrefs(self, user)
            self.user_prefs[k] = prefs
        return prefs
    
    def clear(self, user):
        k = user.username
        del self.user_prefs[k]
        
    
reg = Registry()
