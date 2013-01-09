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

"""
Lino CMS is yet another simple Content Management System.

"""

from os.path import join, abspath, dirname

from lino.apps.std.settings import *

from django.utils.translation import ugettext_lazy as _

class Lino(Lino):
  
    #~ title = __name__
    short_name = u"Lino CMS"
    description = _("yet another Content Management System.")
    version = "0.1"
    url = "http://www.lino-framework.org/autodoc/lino.apps.cms"
    author = 'Luc Saffre'
    author_email = 'luc.saffre@gmail.com'
    
    admin_prefix = '/admin'
    
    languages = ['en','de','fr']
    #~ languages = 'de fr et en'.split()
    
    project_model = 'tickets.Project'
    user_model = 'users.User'
    
    #~ remote_user_header = "REMOTE_USER"
    
    def get_app_source_file(self): return __file__
      
    #~ def get_main_action(self,user):
        #~ return self.modules.lino.Home.default_action
            
    def get_installed_apps(self):
        for a in super(Lino,self).get_installed_apps():
            yield a
        yield 'django.contrib.contenttypes'
        yield 'lino.modlib.users'
        yield 'lino.modlib.countries'
        yield 'lino.modlib.contacts'
        #~ yield 'lino.modlib.outbox'
        yield 'lino.modlib.blogs'
        yield 'lino.modlib.tickets'
        yield 'lino.modlib.pages'
        yield 'lino.apps.cms'
