# Copyright 2011-2017 Luc Saffre
# License: BSD (see file COPYING for details)

"""

Documentation is in :doc:`/specs/users` and :doc:`/dev/users`

.. autosummary::
   :toctree:

    utils
    roles
    choicelists
    actions
    forms
    views
    fixtures.demo
    fixtures.demo_users
    fixtures.demo2

"""

from lino.api import ad, _


class Plugin(ad.Plugin):
    """See :doc:`/dev/plugins`.

    .. attribute:: online_registration

        Whether this site offers :ref:`online registration
        <online_registration>` of new users.

    """
    verbose_name = _("Users")

    needs_plugins = ['lino.modlib.system']

    online_registration = False

    def on_init(self):
        super(Plugin, self).on_init()
        self.site.set_user_model('users.User')

    def setup_config_menu(self, site, profile, m):
        g = site.plugins.system
        m = m.add_menu(g.app_label, g.verbose_name)
        m.add_action('users.AllUsers')

    def setup_explorer_menu(self, site, profile, m):
        g = site.plugins.system
        m = m.add_menu(g.app_label, g.verbose_name)
        m.add_action('users.Authorities')
        m.add_action('users.UserTypes')


