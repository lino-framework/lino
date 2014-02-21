# -*- coding: UTF-8 -*-
# Copyright 2012-2014 Luc Saffre
# This file is part of the Lino project.
# Lino is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
# Lino is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
# You should have received a copy of the GNU Lesser General Public License
# along with Lino; if not, see <http://www.gnu.org/licenses/>.

from lino.projects.std.settings import *


class Site(Site):
    title = "Lino Mini 1"

    user_model = 'users.User'

    default_user = 'root'

    demo_fixtures = 'std demo'

    def setup_quicklinks(self, ar, tb):
        tb.add_action(self.modules.contacts.Persons.detail_action)
        tb.add_action(self.modules.contacts.Companies.detail_action)

    def get_installed_apps(self):
        yield super(Site, self).get_installed_apps()

        yield 'django.contrib.contenttypes'
        yield 'lino.modlib.system'
        yield 'lino.modlib.users'
        yield 'lino.modlib.countries'
        yield 'lino.modlib.contacts'

SITE = Site(globals())
