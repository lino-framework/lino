# Copyright 2011-2014 Luc Saffre
# License: BSD (see file COPYING for details)

"""Lino's :mod:`lino.modlib.users` is an alternative to Django's
:mod:`django.contrib.auth` module.

This module is much more simple and does not require
:mod:`django.contrib.sessions` to be installed.
See :doc:`/tickets/31` for discussion.

To use it, you must override :setting:`user_model` and
:setting:`get_installed_apps` in your
:class:`lino.lino_site.Site`. Example::

    user_model = 'users.User'
    
    def get_installed_apps(self):
        yield super(Lino,self).get_installed_apps()
        yield 'lino.modlib.system'
        yield 'lino.modlib.users'
        # continue with your own modules

"""

from lino import ad

from django.utils.translation import ugettext_lazy as _


class Plugin(ad.Plugin):
    "Ceci n'est pas une documentation."
    verbose_name = _("Users")

