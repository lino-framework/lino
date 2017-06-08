# -*- coding: UTF-8 -*-
# Copyright 2016-2017 Luc Saffre.
# License: BSD, see LICENSE for more details.
"""The user preferences registry.

Application code should get the preferences for a user by calling
:meth:`lino.core.site.Site.get_user_prefs` which returns an object
of this class.

There is one instance per user which will be created upon first
request. 

After instantiating a preferences object, Lino calls the
:meth:`setup_user_prefs
<lino.core.plugin.Plugin.setup_user_prefs>` of every installed
plugin once on it. This feature is used by
:mod:`lino.modlib.dashboard`).



"""

from django.conf import settings

from .actors import Actor
from .dashboard import ActorItem, DashboardItem

def get_available_items(user):
    """Return a list of all available dasboard items for this user.

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
        for p in settings.SITE.installed_plugins:
            p.setup_user_prefs(self)
        settings.SITE.logger.debug(
            "User preferences for %s have been initialized.", self.user)
        
    def invalidate(self):
        k = self.user.username
        reg._user_prefs.pop(k, None)
        # like del, but no problem if it didn't exist.
        
        
class Registry(object):
    """"""
    def __init__(self):
        self._user_prefs = {}
        
    def get(self, user):
        k = user.username
        prefs = self._user_prefs.get(k, None)
        if prefs is None:
            prefs = UserPrefs(self, user)
            self._user_prefs[k] = prefs
        return prefs
    
    def clear(self, user):
        k = user.username
        del self._user_prefs[k]
        
    
reg = Registry()
