# -*- coding: UTF-8 -*-
# Copyright 2011-2015 Luc Saffre
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

"""The :mod:`lino_noi.lib.faculties` package add "Competences" and "Faculties" to tickets.

.. autosummary::
   :toctree:

   models

"""

from lino.api import ad, _


class Plugin(ad.Plugin):
    "See :class:`lino.core.plugin.Plugin`."

    verbose_name = _("Faculties")

    needs_plugins = ['lino_noi.lib.tickets']


    def setup_main_menu(self, site, profile, m):
        mgt = site.plugins.tickets
        m = m.add_menu(mgt.app_label, mgt.verbose_name)
        m.add_action('faculties.UnassignedTickets')
        # m = m.add_menu(self.app_label, self.verbose_name)
        # m.add_action('faculties.Faculties')
        # m.add_action('faculties.Competences')

    def setup_config_menu(self, site, profile, m):
        mgt = site.plugins.tickets
        m = m.add_menu(mgt.app_label, mgt.verbose_name)
        m.add_action('faculties.Faculties')
        m.add_action('faculties.Competences')

    def setup_explorer_menu(self, site, profile, m):
        p = self.get_menu_group()
        m = m.add_menu(p.app_label, p.verbose_name)
        m.add_action('faculties.Faculties')
        m.add_action('faculties.Competences')
