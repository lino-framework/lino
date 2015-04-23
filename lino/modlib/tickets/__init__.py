# Copyright 2008-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""
Adds functionality for managing tickets.

.. autosummary::
   :toctree:

    models

"""

from lino.api import ad, _


class Plugin(ad.Plugin):
    "See :doc:`/dev/plugins`."

    verbose_name = _("Tickets")

    # needs_plugins = ['lino.modlib.clocking']

    def setup_main_menu(self, site, profile, m):
        p = self.get_menu_group()
        m = m.add_menu(p.app_label, p.verbose_name)
        m.add_action('tickets.Projects')
        # m.add_action('tickets.MyOwnedTickets')
        m.add_action('tickets.ActiveTickets')

    def setup_config_menu(self, site, profile, m):
        p = self.get_menu_group()
        m = m.add_menu(p.app_label, p.verbose_name)
        m.add_action('tickets.ProjectTypes')

    def setup_explorer_menu(self, site, profile, m):
        p = self.get_menu_group()
        m = m.add_menu(p.app_label, p.verbose_name)
        # m.add_action('tickets.Projects')
        m.add_action('tickets.Tickets')
        m.add_action('tickets.Milestones')
        m.add_action('tickets.Dependencies')
        m.add_action('tickets.Sponsorship')
