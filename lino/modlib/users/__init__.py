# Copyright 2011-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""Lino's :mod:`lino.modlib.users` is Lino's replacement for Django's
:mod:`django.contrib.auth` module.  This module does not require
:mod:`django.contrib.sessions` to be installed.  See also
:doc:`/dev/users`. Note that parts of this module are being used by
Lino's core even if it is not among the installed apps.

.. autosummary::
   :toctree:

    utils
    mixins
    roles
    models
    choicelists
    fixtures.demo
    fixtures.demo_users
    fixtures.demo2

"""

from lino.api import ad, _


class Plugin(ad.Plugin):
    "See :doc:`/dev/plugins`."
    verbose_name = _("Users")

    def on_init(self):
        super(Plugin, self).on_init()
        self.site.set_user_model('users.User')

    def setup_config_menu(self, site, profile, m):
        g = site.plugins.system
        m = m.add_menu(g.app_label, g.verbose_name)
        m.add_action('users.Users')

    def setup_explorer_menu(self, site, profile, m):
        g = site.plugins.system
        m = m.add_menu(g.app_label, g.verbose_name)
        m.add_action('users.Authorities')
        m.add_action('users.UserProfiles')


