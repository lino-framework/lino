# -*- coding: UTF-8 -*-
## Copyright 2009-2012 Luc Saffre
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
Default settings for :doc:`/pcsw/index`.

"""

import os
import lino

from lino.apps.std.settings import *

#~ LISTINGS = """
#~ jobs.ContractsSituation
#~ lino.DataControlListing
#~ """.split()


class Lino(Lino):
    """
    Lino/PCSW is
    the first of the real-world demo applications that are part 
    of the Lino project.
    It is a tool for social assistants that help receivers 
    of public aid to find a suitable job or education, 
    adapted to Belgian *Public Centres for Social Welfare* 
    (Centres Publics d'Action Sociale).
    
    """
    source_dir = os.path.dirname(__file__)
    title = "Lino/PCSW"
    #~ domain = "pcsw.saffre-rumma.net"
    help_url = "http://lino.saffre-rumma.net/pcsw/index.html"
    migration_module = 'lino.apps.pcsw.migrate'
    
    #~ project_model = 'contacts.Person'
    project_model = 'contacts.Person'
    user_model = 'users.User'
    
    languages = ('de', 'fr', 'nl', 'en')
    
    #~ index_view_action = "pcsw.Home"
    
    remote_user_header = "REMOTE_USER"
    
    def get_app_source_file(self):
        return __file__
        
    override_modlib_models = ['contacts.Person','contacts.Company']
        
        
        
    anonymous_user_profile = '400'
    
    #~ def setup_user_profiles(self):
    def setup_choicelists(self):
        """
        This defines default user profiles for :mod:`lino.apps.pcsw`.
        """
        from lino import dd
        from django.utils.translation import ugettext_lazy as _
        dd.UserProfiles.reset('* office integ cbss newcomers debts')
        add = dd.UserProfiles.add_item
        add('100', _("Integration Agent"),          'U U U U _ _')
        add('110', _("Integration Agent (Senior)"), 'U M M U _ _')
        add('200', _("Newcomers consultant"),       'U U _ U U _')
        add('300', _("Debts consultant"),           'U U _ _ _ U')
        #~ add('400', _("Readonly Manager"),           'M M M M M M', readonly=True)
        add('400', _("Readonly User"),              'U U U U U U', readonly=True)
        add('500', _("CBSS only"),                  'U _ _ U _ _')
        add('900', _("Administrator"),              'A A A A A A',name='admin')
        
        #~ for p in dd.UserProfiles.items():
            #~ print 20120715, repr(p)
            

    def setup_quicklinks(self,ui,user,tb):
        #~ tb.add_action(self.modules.contacts.Persons().detail)
        #~ tb.add_action(self.modules.contacts.Persons,'detail')
        #~ tb.add_action(self.modules.contacts.Persons,'detail')
        tb.add_action(self.modules.contacts.Persons.detail_action)
        self.on_each_app('setup_quicklinks',ui,user,tb)
        
        tb.add_action(self.modules.pcsw.MyPersons)
        tb.add_action(self.modules.isip.MyContracts)
        tb.add_action(self.modules.jobs.MyContracts)
        #~ tb.add_action(self.modules.pcsw.Home)
        
        
    def setup_menu(self,ui,user,main):
        from django.utils.translation import ugettext_lazy as _
        from django.db import models
        from lino.modlib.users.models import UserLevels
        
        m = main.add_menu("master",_("Master"))
        
        m = main.add_menu("contacts",_("Contacts"))
        #~ if user.is_spis:
        if user.profile.level:
            m.add_action(self.modules.contacts.Companies)
            m.add_action(self.modules.contacts.Persons)
            #~ m.add_action('contacts.Persons.detail')
            #~ m.add_action('contacts.Persons',label="Alle Personen",params={})
            m.add_action(self.modules.contacts.AllPartners)
            #~ m.add_action(self.modules.pcsw.Newcomers)
        if user.profile.integ_level:
            m.add_action(self.modules.pcsw.MyPersonSearches)
            
        self.modules.isip.setup_master_menu(self,ui,user,m)
        self.modules.households.setup_master_menu(self,ui,user,m)
        

        #~ if user is None:
            #~ return main
        if user.profile.level and not user.profile.readonly:
          
            m = main.add_menu("my",_("My menu"))
            #~ m.add_action('projects.Projects')
            m.add_action(self.modules.notes.MyNotes)
            
            #~ if user.is_spis:
            if user.profile.integ_level:
                mypersons = m.add_menu("mypersons",self.modules.pcsw.MyPersons.label)
                mypersons.add_action(self.modules.pcsw.MyPersons)
                for pg in self.modules.pcsw.PersonGroup.objects.order_by('ref_name'):
                    mypersons.add_action(
                      self.modules.pcsw.MyPersonsByGroup,
                      label=pg.name,
                      params=dict(master_instance=pg))
                    #~ m.add_action('contacts.MyPersonsByGroup',label=pg.name,
                    #~ params=dict(master_id=pg.pk))
            self.on_each_app('setup_my_menu',ui,user,m)
            #~ self.modules.isip.setup_my_menu(self,ui,user,m)
            #~ self.modules.jobs.setup_my_menu(self,ui,user,m)
            #~ self.modules.households.setup_my_menu(self,ui,user,m)
            #~ self.modules.newcomers.setup_my_menu(self,ui,user,m)
            #~ self.modules.debts.setup_my_menu(self,ui,user,m)
            
            #~ self.modules.cal.setup_my_menu(self,ui,user,m)
            #~ self.modules.outbox.setup_my_menu(self,ui,user,m)
            #~ m.add_action(self.modules.uploads.MyUploads)
            m.add_action(self.modules.lino.MyTextFieldTemplates)

            #~ m.add_instance_action(user,label="My user preferences")
        

        #~ self.modules.newcomers.setup_main_menu(self,ui,user,m)
        
        self.on_each_app('setup_main_menu',ui,user,main)
        #~ self.modules.newcomers.setup_main_menu(self,ui,user,main)
        #~ self.modules.debts.setup_main_menu(self,ui,user,main)
        #~ self.modules.courses.setup_main_menu(self,ui,user,main)
        #~ self.modules.jobs.setup_main_menu(self,ui,user,main)
        
        #~ sitemenu = system.add_site_menu(self)
        #~ if False:
        m = main.add_menu("lst",_("Listings"))
        m.add_action(self.modules.jobs.JobsOverview)
        m.add_action(self.modules.pcsw.UsersWithClients)
        m.add_action(self.modules.pcsw.ClientsTest)
        
        if user.profile.level >= UserLevels.manager: # is_staff:
            cfg = main.add_menu("config",_("Configure"))
            
            self.on_each_app('setup_config_menu',ui,user,cfg)
            
            config_pcsw     = cfg.add_menu("pcsw",_("SIS"))
            config_pcsw.add_action(self.modules.pcsw.PersonGroups)
            config_pcsw.add_action(self.modules.pcsw.Activities)
            config_pcsw.add_action(self.modules.pcsw.ExclusionTypes)
            config_pcsw.add_action(self.modules.pcsw.AidTypes)
            
            
        if user.profile.level >= UserLevels.manager: # is_staff:
          
            m = main.add_menu("explorer",_("Explorer"))
            
            m.add_action(self.modules.contacts.AllPersons)
            
            self.on_each_app('setup_explorer_menu',ui,user,m)
            
            #~ m.add_action(self.modules.uploads.Uploads)
            m.add_action(self.modules.pcsw.Exclusions)
            m.add_action(self.modules.pcsw.PersonSearches)
            #~ m.add_action(self.modules.lino.ContentTypes)
            m.add_action(self.modules.properties.Properties)
            #~ m.add_action(self.modules.thirds.Thirds)
            
            
            #~ self.modules.cal.setup_explorer_menu(self,ui,user,m)
            
            #~ lst = m.add_menu("lst",_("Listings"))
            #~ for listing in LISTINGS:
                #~ lst.add_action(listing)
            

        
        m = main.add_menu("site",_("Site"))
        self.modules.lino.setup_site_menu(self,ui,user,m)
        
        #~ m = main.add_menu("help",_("Help"))
        #~ m.add_item('userman',_("~User Manual"),
            #~ href='http://lino.saffre-rumma.net/pcsw/index.html')
            
        return main
      
    def get_reminder_generators_by_user(self,user):
        """
        Yield a list of objects susceptible to generate 
        automatic reminders for the specified user.
        Used by :func:`lino.modlib.cal.update_reminders`.
        """
        from lino.core.modeltools import models_by_abc
        from django.db.models import Q
        from lino.modlib.isip import models as isip
        #~ from lino.apps.pcsw.models import only_my_persons
        
        for obj in self.modules.contacts.Person.objects.filter(
          Q(coach2=user)|Q(coach2__isnull=True,coach1=user)):
            yield obj
        for obj in self.modules.uploads.Upload.objects.filter(user=user):
            yield obj
        for model in models_by_abc(isip.ContractBase):
            for obj in model.objects.filter(user=user):
                yield obj
                
                

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
  #~ 'lino.modlib.workflows',
  'lino.modlib.countries',
  #~ 'lino.modlib.documents',
  'lino.modlib.properties',
  'lino.modlib.contacts',
  #~ 'lino.modlib.projects',
  'lino.modlib.notes',
  #~ 'lino.modlib.links',
  'lino.modlib.uploads',
  #~ 'lino.modlib.thirds',
  'lino.modlib.cal',
  'lino.modlib.outbox',
  'lino.modlib.postings',
  'lino.modlib.cv',
  'lino.modlib.jobs',
  'lino.modlib.isip',
  'lino.modlib.cbss',
  'lino.modlib.newcomers',
  'lino.modlib.households',
  'lino.modlib.debts',
  'lino.modlib.courses',
  'lino.apps.pcsw',
  #~ 'south', # http://south.aeracode.org
)

#~ LANGUAGES = language_choices('de','fr','nl','en')
#~ LANGUAGES = language_choices('de','fr','en')

