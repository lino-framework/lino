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

"""
Lino CMS is yet another simple Content Management System.

"""

from django.utils.translation import ugettext_lazy as _

from lino.projects.std.settings import *


class Site(Site):

    #~ title = __name__
    verbose_name = "Lino CMS"
    #~ description = _("yet another Content Management System.")
    version = "0.1"
    author = 'Luc Saffre'
    author_email = 'luc.saffre@gmail.com'

    default_ui = 'plain'

    languages = 'en de fr'

    project_model = 'tickets.Project'
    user_model = 'users.User'

    sidebar_width = 3

    def get_installed_apps(self):
        yield super(Site, self).get_installed_apps()
        yield 'django.contrib.contenttypes'
        yield 'lino.modlib.system'
        yield 'lino.modlib.users'
        yield 'lino.modlib.countries'
        yield 'lino.modlib.contacts'
        #~ yield 'lino.modlib.outbox'
        yield 'lino.modlib.blogs'
        yield 'lino.modlib.tickets'
        yield 'lino.modlib.pages'
        yield 'lino.projects.cms'


    # def get_apps_modifiers(self, **kk):
    #     kw = super(Site, self).get_apps_modifiers(**kk)
    #     kw.update(extjs=None)
    #     return kw


SITE = Site(globals())
