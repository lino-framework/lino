# -*- coding: UTF-8 -*-
# Copyright 2013 Luc Saffre
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

from __future__ import unicode_literals

from lino.projects.std.settings import *

from django.utils.translation import ugettext_lazy as _


class Site(Site):

    #~ title = __name__
    verbose_name = "Lino Belref"
    description = _("Belgian Reference")
    version = "0.1"
    url = "http://www.lino-framework.org/belref.html"
    author = 'Luc Saffre'
    author_email = 'luc.saffre@gmail.com'

    demo_fixtures = 'demo all_countries be inscodes'
    #~ demo_fixtures = 'demo'

    #~ admin_prefix = 'admin'
    # default_ui = 'plain'
    default_ui = 'bootstrap3'

    #~ anonymous_user_profile =

    languages = 'fr nl de'

    #~ project_model = 'tickets.Project'
    #~ user_model = 'users.User'

    #~ sidebar_width  = 3

    # hidden_apps = 'extjs'

    def get_apps_modifiers(self, **kk):
        kw = super(Site, self).get_apps_modifiers(**kk)
        kw.update(extjs=None)
        kw.update(plain=None)
        return kw

    def get_installed_apps(self):
        yield super(Site, self).get_installed_apps()
            # if a != 'lino.extjs':
            #     yield a
        #~ yield 'django.contrib.contenttypes'
        #~ yield 'lino.modlib.users'
        yield 'lino.modlib.system'
        yield 'lino.modlib.statbel'
        yield 'lino.modlib.countries'
        #~ yield 'lino.modlib.contacts'
        #~ yield 'lino.modlib.outbox'
        #~ yield 'lino.modlib.blogs'
        #~ yield 'lino.modlib.tickets'
        #~ yield 'lino.modlib.pages'
        yield 'lino.modlib.concepts'
        # yield 'lino.modlib.bootstrap3'
        yield 'lino.projects.belref'

    def setup_menu(self, ui, profile, main):
        """
        We create a new menu from scratch because the default menu structure
        wouldn't fit.
        """
        from django.utils.translation import ugettext_lazy as _
        from lino import dd
        concepts = dd.resolve_app('concepts')
        m = main.add_menu("concepts", concepts.MODULE_LABEL)
        m.add_action(self.modules.concepts.Concepts)
        m.add_action(self.modules.countries.Countries)
        m.add_action(self.modules.countries.Places)

    def get_main_action(self, user):
        return self.modules.belref.Main.default_action
