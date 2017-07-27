# Copyright 2011-2017 Luc Saffre
# License: BSD (see file COPYING for details)

"""Implements functionality for managing users.  See
:doc:`/specs/users`.

Submodules:

.. autosummary::
   :toctree:

    utils
    fixtures.demo
    fixtures.demo_users
    fixtures.demo2

"""


from lino.api import ad, _


class Plugin(ad.Plugin):
    verbose_name = _("Users")

    needs_plugins = ['lino.modlib.system']

    online_registration = False

    def on_init(self):
        super(Plugin, self).on_init()
        self.site.set_user_model('users.User')

    def setup_config_menu(self, site, user_type, m):
        g = site.plugins.system
        m = m.add_menu(g.app_label, g.verbose_name)
        m.add_action('users.AllUsers')

    def setup_explorer_menu(self, site, user_type, m):
        g = site.plugins.system
        m = m.add_menu(g.app_label, g.verbose_name)
        m.add_action('users.Authorities')
        m.add_action('users.UserTypes')


