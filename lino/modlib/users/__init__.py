# Copyright 2011-2018 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""
Implements functionality for managing users.  See
:doc:`/specs/users` and :doc:`/dev/users`

Submodules:

.. autosummary::
   :toctree:

    utils
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
        m.add_action('users.UserRoles')
        if site.social_auth_backends is not None:
            m.add_action('users.SocialAuths')


