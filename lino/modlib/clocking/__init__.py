# Copyright 2008-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""
Adds functionality for managing worktime clocking.

.. autosummary::
   :toctree:

    models
    ui

"""

from lino.api import ad, _


class Plugin(ad.Plugin):
    "See :doc:`/dev/plugins`."

    verbose_name = _("Clocking")

    needs_plugins = ['lino.modlib.tickets', 'lino.modlib.excerpts']

    def setup_main_menu(self, site, profile, m):
        p = self.get_menu_group()
        m = m.add_menu(p.app_label, p.verbose_name)
        m.add_action('clocking.MySessions')
        m.add_action('clocking.MySessionsByDate')
        m.add_action('clocking.InvestedTimes')

    def setup_reports_menu(self, site, profile, m):
        p = self.get_menu_group()
        m = m.add_menu(p.app_label, p.verbose_name)
        m.add_action('clocking.ServiceReports')

    def setup_config_menu(self, site, profile, m):
        p = self.get_menu_group()
        m = m.add_menu(p.app_label, p.verbose_name)
        m.add_action('clocking.SessionTypes')

    def setup_explorer_menu(self, site, profile, m):
        p = self.get_menu_group()
        m = m.add_menu(p.app_label, p.verbose_name)
        m.add_action('clocking.Sessions')
