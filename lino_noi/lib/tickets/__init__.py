# Copyright 2008-2016 Luc Saffre
#
# This file is part of Lino Noi.
#
# Lino Noi is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# Lino Noi is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with Lino Noi.  If not, see
# <http://www.gnu.org/licenses/>.

"""
Adds functionality for managing tickets.

.. autosummary::
   :toctree:

    roles
    models
    ui
    choicelists


"""

from lino.api import ad, _


class Plugin(ad.Plugin):
    "See :class:`lino.core.plugin.Plugin`."

    verbose_name = _("Tickets")

    needs_plugins = [
        'lino_xl.lib.stars', 'lino_xl.lib.excerpts',
        'lino_xl.lib.topics',
        'lino.modlib.comments', 'lino.modlib.changes',
        'lino_noi.lib.noi']

    def setup_main_menu(self, site, profile, m):
        p = self.get_menu_group()
        m = m.add_menu(p.app_label, p.verbose_name)
        m.add_action('tickets.MyTickets')
        m.add_action('tickets.SuggestedTickets')
        m.add_action('tickets.TicketsToDo')
        # m.add_action('tickets.MyOwnedTickets')
        m.add_action('tickets.ActiveTickets')
        m.add_action('tickets.AllTickets')
        # m.add_action('tickets.MyKnownProblems')
        m.add_action('tickets.UnassignedTickets')
        m.add_action('tickets.ActiveProjects')

    def setup_config_menu(self, site, profile, m):
        p = self.get_menu_group()
        m = m.add_menu(p.app_label, p.verbose_name)
        m.add_action('tickets.AllProjects')
        m.add_action('tickets.TopLevelProjects')
        m.add_action('tickets.ProjectTypes')
        m.add_action('tickets.TicketTypes')
        m.add_action('tickets.AllSites')

    def setup_explorer_menu(self, site, profile, m):
        p = self.get_menu_group()
        m = m.add_menu(p.app_label, p.verbose_name)
        # m.add_action('tickets.Projects')
        m.add_action('tickets.Links')
        m.add_action('tickets.TicketStates')
