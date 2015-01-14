# Copyright 2008-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""
Adds functionality for managing foos.

.. autosummary::
   :toctree:

    models

"""

from lino import ad, _


class Plugin(ad.Plugin):

    verbose_name = _("Tickets")

    def setup_main_menu(config, site, profile, m):
        m = m.add_menu("tickets", _("Tickets"))
        m.add_action('tickets.MyProjects')
        m.add_action('tickets.MyTickets')
        m.add_action('tickets.MySessions')
        m.add_action('tickets.MySessionsByDate')

    def setup_config_menu(config, site, profile, m):
        m = m.add_menu("tickets", _("Tickets"))
        m.add_action('tickets.ProjectTypes')
        m.add_action('tickets.SessionTypes')

    def setup_explorer_menu(config, site, profile, m):
        m = m.add_menu("tickets", _("Tickets"))
        m.add_action('tickets.Projects')
        m.add_action('tickets.Tickets')
        m.add_action('tickets.Sessions')
        m.add_action('tickets.Milestones')
        m.add_action('tickets.Dependencies')
        m.add_action('tickets.Votes')
