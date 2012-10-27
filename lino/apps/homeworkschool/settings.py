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
    title = "Lino Homework School Manager"
    #~ help_url = "http://lino.saffre-rumma.net/az/index.html"
    #~ migration_module = 'lino.apps.az.migrate'
    
    #~ project_model = 'contacts.Person'
    #~ project_model = 'school.Pupil'
    project_model = 'school.Course'
    #~ project_model = None
    user_model = 'users.User'
    
    languages = ('de', 'fr')
    
    use_eid_jslib = False
    
    #~ index_view_action = "dsbe.Home"
    
    override_modlib_models = [
        #~ 'contacts.Partner', 
        'contacts.Person', 
        #~ 'contacts.Company',
        #~ 'households.Household',
        ]
    
    
    remote_user_header = "REMOTE_USER"
    
    def get_app_source_file(self):  return __file__
        
    def get_main_action(self,user):
        return self.modules.lino.Home.default_action
        
    #~ def setup_quicklinks(self,ui,user,tb):
        #~ tb.add_action(self.modules.contacts.Persons.detail_action)
        #~ if self.use_extensible:
            #~ tb.add_action(self.modules.cal.Panel)
        #~ tb.add_action(self.modules.dsbe.MyPersons)
        #~ tb.add_action(self.modules.isip.MyContracts)
        #~ tb.add_action(self.modules.jobs.MyContracts)
        
    def setup_choicelists(self):
        """
        This defines default user profiles for :mod:`lino_welfare`.
        """
        from lino import dd
        from django.utils.translation import ugettext_lazy as _
        dd.UserProfiles.reset('* office')
        add = dd.UserProfiles.add_item
        #~ add('100', _("Integration Agent"),          'U U')
        #~ add('900', _("System admin"),          'U U')
        
        add('100', _("User"),          'U U', name='user')
        add('900', _("Administrator"), 'A A', name='admin')
        
      
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
  'lino.modlib.households',
  'lino.modlib.notes',
  'lino.apps.homeworkschool.school',
  #~ 'lino.modlib.links',
  'lino.modlib.uploads',
  #~ 'lino.modlib.thirds',
  'lino.modlib.cal',
  'lino.modlib.outbox',
  #~ 'lino.modlib.jobs',
  #~ 'lino.modlib.isip',
  #~ 'lino.modlib.bcss',
  #~ 'lino.modlib.newcomers',
  'lino.apps.homeworkschool',
  #'dsbe.modlib.contacts',
  #'dsbe.modlib.projects',
  #~ 'south', # http://south.aeracode.org
)


