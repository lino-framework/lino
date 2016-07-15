# -*- coding: UTF-8 -*-
# Copyright 2014-2016 Luc Saffre
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

.. autosummary::
   :toctree:

   demo
   doctests
   www
   memory
   fixtures



"""

from __future__ import print_function
from __future__ import unicode_literals

from lino_noi.projects.team.settings import *


class Site(Site):

    verbose_name = "Lino Care"

    demo_fixtures = ['std', 'demo', 'demo2']
    user_profiles_module = 'lino_noi.projects.care.roles'

    def setup_plugins(self):
        super(Site, self).setup_plugins()
        self.plugins.topics.partner_model = 'users.User'
        self.plugins.topics.menu_group = 'users'
        # self.plugins.lists.partner_model = 'users.User'
        self.plugins.countries.configure(hide_region=True)

    def get_apps_modifiers(self, **kw):
        kw = super(Site, self).get_apps_modifiers(**kw)

        # remove whole plugin:
        # kw.update(products=None)
        # kw.update(clocking=None)
        kw.update(contacts=None)
        kw.update(lists=None)
        kw.update(outbox=None)
        # kw.update(excerpts=None)

        # alternative implementations:
        kw.update(tickets='lino_noi.projects.care.lib.tickets')
        kw.update(users='lino_noi.lib.users')
        return kw


# the following line should not be active in a checked-in version
# DATABASES['default']['NAME'] = ':memory:'
