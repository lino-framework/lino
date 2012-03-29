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

from lino.apps.std.settings import *


class Lino(Lino):
    source_dir = os.path.dirname(__file__)
    title = "Lino/AZ"
    help_url = "http://lino.saffre-rumma.net/az/index.html"
    #~ migration_module = 'lino.apps.dsbe.migrate'
    
    #~ project_model = 'contacts.Person'
    #~ project_model = 'contacts.Person'
    project_model = None
    
    languages = ('de', 'fr')
    
    #~ index_view_action = "dsbe.Home"
    
    remote_user_header = "REMOTE_USER"
    
    def get_app_source_file(self):  return __file__
        
    def setup_quicklinks(self,ui,user,tb):
        tb.add_action(self.modules.contacts.Persons.detail_action)
        if self.use_extensible:
            tb.add_action(self.modules.cal.Panel)
        #~ tb.add_action(self.modules.dsbe.MyPersons)
        #~ tb.add_action(self.modules.isip.MyContracts)
        #~ tb.add_action(self.modules.jobs.MyContracts)
        
        
    def setup_menu(self,ui,user,main):
        from django.utils.translation import ugettext_lazy as _
        from django.db import models
        
        #~ LISTINGS = [
          #~ self.modules.jobs.ContractsSituation,
          #~ self.modules.lino.DataControlListing,
        #~ ]
        
        m = main.add_menu("master",_("Master"))
        m.add_action(self.modules.contacts.Persons)
        m.add_action(self.modules.contacts.Companies)
        #~ m.add_action(self.modules.dsbe.MyPersonSearches)
        #~ m.add_action(self.modules.contacts.AllContacts)
        #~ m.add_action(self.modules.dsbe.Newcomers)

        self.modules.families.setup_main_menu(self,ui,user,m)
        self.modules.school.setup_main_menu(self,ui,user,m)

        #~ if user is None:
            #~ return main
            
        m = main.add_menu("my",_("My menu"))
        
        self.modules.cal.setup_my_menu(self,ui,user,m)
        self.modules.mails.setup_my_menu(self,ui,user,m)
        self.modules.school.setup_my_menu(self,ui,user,m)
        self.modules.families.setup_my_menu(self,ui,user,m)
        m.add_action(self.modules.lino.MyTextFieldTemplates)

        #~ m.add_instance_action(user,label="My user preferences")

        
        if user.is_staff:
            cfg = main.add_menu("config",_("Configure"))
            
            self.modules.contacts.setup_config_menu(self,ui,user,cfg)
            self.modules.families.setup_config_menu(self,ui,user,cfg)
            self.modules.school.setup_config_menu(self,ui,user,cfg)
            
            #~ self.modules.notes.setup_config_menu(self,ui,user,cfg)
            
            self.modules.cal.setup_config_menu(self,ui,user,cfg)
            self.modules.mails.setup_config_menu(self,ui,user,cfg)
            self.modules.lino.setup_config_menu(self,ui,user,cfg)
            
            m = main.add_menu("explorer",_("Explorer"))
            
            self.modules.contacts.setup_explorer_menu(self,ui,user,m)
            self.modules.families.setup_explorer_menu(self,ui,user,m)
            self.modules.school.setup_explorer_menu(self,ui,user,m)
            self.modules.cal.setup_explorer_menu(self,ui,user,m)
            
        
        m = main.add_menu("site",_("Site"))
        self.modules.lino.setup_site_menu(self,ui,user,m)
        
        return main
      
LINO = Lino(__file__,globals())


#~ PROJECT_DIR = abspath(dirname(__file__))
#~ DATA_DIR = join(PROJECT_DIR,"data")
#~ LINO_SETTINGS = join(PROJECT_DIR,"lino_settings.py")

#~ MEDIA_ROOT = join(LINO.project_dir,'media')
#~ MEDIA_ROOT = join(PROJECT_DIR,'media')

#~ TIME_ZONE = 'Europe/Brussels'
TIME_ZONE = None

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
#~ LANGUAGE_CODE = 'de'
#~ LANGUAGE_CODE = 'de-BE'
#~ LANGUAGE_CODE = 'fr-BE'

#~ SITE_ID = 1 # see also fill.py

INSTALLED_APPS = (
  #~ 'django.contrib.auth',
  'django.contrib.contenttypes',
  #~ 'django.contrib.sessions',
  #~ 'django.contrib.sites',
  #~ 'django.contrib.markup',
  #~ 'lino.modlib.system',
  'lino',
  'lino.modlib.users',
  'lino.modlib.countries',
  #~ 'lino.modlib.documents',
  #~ 'lino.modlib.properties',
  'lino.modlib.contacts',
  #~ 'lino.modlib.projects',
  'lino.apps.az.families',
  #~ 'lino.az.notes',
  'lino.apps.az.school',
  #~ 'lino.modlib.links',
  'lino.modlib.uploads',
  #~ 'lino.modlib.thirds',
  'lino.modlib.cal',
  'lino.modlib.mails',
  #~ 'lino.modlib.jobs',
  #~ 'lino.modlib.isip',
  #~ 'lino.modlib.bcss',
  #~ 'lino.modlib.newcomers',
  'lino.apps.az',
  #'dsbe.modlib.contacts',
  #'dsbe.modlib.projects',
  #~ 'south', # http://south.aeracode.org
)


