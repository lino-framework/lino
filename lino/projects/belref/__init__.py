# -*- coding: UTF-8 -*-
## Copyright 2013 Luc Saffre
## This file is part of the Lino project.
## Lino is free software; you can redistribute it and/or modify 
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 3 of the License, or
## (at your option) any later version.
## Lino is distributed in the hope that it will be useful, 
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
## GNU General Public License for more details.
## You should have received a copy of the GNU General Public License
## along with Lino; if not, see <http://www.gnu.org/licenses/>.

"""
Lino Belref is how I would implement a Belgian Reference website 
with various information in English + the three national languages.

"""

from __future__ import unicode_literals


from os.path import join, abspath, dirname

from lino.projects.std.settings import *

from django.utils.translation import ugettext_lazy as _

class Site(Site):
  
    #~ title = __name__
    verbose_name = "Lino Belref"
    description = _("Belgian Reference System.")
    version = "0.1"
    url = "http://www.lino-framework.org/autodoc/lino.projects.belref"
    author = 'Luc Saffre'
    author_email = 'luc.saffre@gmail.com'
    
    demo_fixtures = 'demo all_countries be few_cities inscodes'
    #~ demo_fixtures = 'demo'
    
    #~ admin_prefix = '/admin'
    use_extjs = False
    plain_prefix = ''
    
    #~ anonymous_user_profile = 
    
    #~ languages = ['en','fr','nl','de']
    languages = ['fr','nl','de']
    #~ languages = 'de fr et en'.split()
    
    #~ project_model = 'tickets.Project'
    #~ user_model = 'users.User'
    
    #~ sidebar_width  = 3
    
    #~ def get_main_action(self,user):
        #~ return self.modules.lino.Home.default_action
            
    def get_installed_apps(self):
        for a in super(Site,self).get_installed_apps():
            yield a
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
        yield 'lino.projects.belref'

    def setup_menu(self,ui,profile,main):
        """
        We create a new menu from scratch because the default menu structure
        wouldn't fit.
        """
        from django.utils.translation import ugettext_lazy as _
        from lino import dd
        concepts = dd.resolve_app('concepts')
        m = main.add_menu("concepts",concepts.MODULE_LABEL)
        m.add_action(self.modules.concepts.Concepts)
        m.add_action(self.modules.countries.Countries)
        m.add_action(self.modules.countries.Cities)
        

    def get_main_action(self,user):
        return self.modules.belref.Main.default_action
