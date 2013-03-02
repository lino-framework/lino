# -*- coding: UTF-8 -*-
## Copyright 2012 Luc Saffre
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


import os
import lino

from lino.projects.std.settings import *

class Site(Site):
    #~ source_dir = os.path.dirname(__file__)
    title = "Lino/MinimalApp 1"
    #~ help_url = "http://lino.saffre-rumma.net/az/index.html"
    #~ migration_module = 'lino.projects.az.migrate'
    
    use_extensible = False
    #~ project_model = 'contacts.Person'
    #~ project_model = 'contacts.Person'
    #~ project_model = None
    user_model = 'users.User'
    #~ user_model = None
    
    default_user = 'root'
    
    #~ languages = ('de', 'fr')
    languages = ['en']
    
    #~ index_view_action = "dsbe.Home"
    
    #~ remote_user_header = "REMOTE_USER"
    
    #~ def get_app_source_file(self):  return __file__
        
    def setup_quicklinks(self,ar,tb):
        tb.add_action(self.modules.contacts.Persons.detail_action)
        tb.add_action(self.modules.contacts.Companies.detail_action)
        
    def get_installed_apps(self):
        for a in super(Site,self).get_installed_apps():
            yield a

        yield 'django.contrib.contenttypes'
        yield 'lino.modlib.users'
        yield 'lino.modlib.countries'
        yield 'lino.modlib.contacts'
        #~ yield 'lino.projects.min1'
      
SITE = Site(__file__,globals())


