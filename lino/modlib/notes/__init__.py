# Copyright 2013-2014 Luc Saffre
# This file is part of the Lino Welfare project.
# Lino Welfare is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
# Lino Welfare is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
# You should have received a copy of the GNU Lesser General Public License
# along with Lino Welfare; if not, see <http://www.gnu.org/licenses/>.


"""
Adds a multipurpose model "Note"

.. autosummary::
   :toctree:

   models
   fixtures.demo
   fixtures.std

"""

from lino import ad
from django.utils.translation import ugettext_lazy as _


class Plugin(ad.Plugin):

    verbose_name = _("Notes")

    def setup_main_menu(config, site, profile, m):
        system = site.plugins.system
        m = m.add_menu("office", system.OFFICE_MODULE_LABEL)
        m.add_action('notes.MyNotes')

    def setup_config_menu(config, site, profile, m):
        system = site.plugins.system
        m = m.add_menu("office", system.OFFICE_MODULE_LABEL)
        m.add_action('notes.NoteTypes')
        m.add_action('notes.EventTypes')

    def setup_explorer_menu(config, site, profile, m):
        system = site.plugins.system
        m = m.add_menu("office", system.OFFICE_MODULE_LABEL)
        m.add_action('notes.AllNotes')

