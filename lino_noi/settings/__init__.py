# -*- coding: UTF-8 -*-
# Copyright 2014 Luc Saffre
# This file is part of the Lino project.
# Lino is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
# Lino is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with Lino; if not, see <http://www.gnu.org/licenses/>.


from __future__ import print_function
from __future__ import unicode_literals

from lino.projects.std.settings import *


class Site(Site):

    verbose_name = "Lino Noi"

    version = '0.0.1'

    user_model = 'users.User'

    def get_installed_apps(self):
        yield super(Site, self).get_installed_apps()
        yield 'django.contrib.contenttypes'
        yield 'lino.modlib.system'
        yield 'lino.modlib.users'
        yield 'lino.modlib.countries'
        yield 'lino.modlib.contacts'
        yield 'lino.modlib.products'

        yield 'lino.modlib.excerpts'
        yield 'lino.modlib.appypod'
        yield 'lino.modlib.export_excel'
        yield 'lino.modlib.smtpd'

        yield 'lino_noi'



# the following line should not be active in a checked-in version
#~ DATABASES['default']['NAME'] = ':memory:'
