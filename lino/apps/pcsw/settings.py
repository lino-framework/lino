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
    
    languages = ('de', 'fr', 'nl', 'en')
    
    #~ index_view_action = "pcsw.Home"
    
    remote_user_header = "REMOTE_USER"
    
    def get_app_source_file(self):
        return __file__
        
    def setup_quicklinks(self,ui,user,tb):
        #~ tb.add_action(self.modules.contacts.Persons().detail)
        #~ tb.add_action(self.modules.contacts.Persons,'detail')
        #~ tb.add_action(self.modules.contacts.Persons,'detail')
        tb.add_action(self.modules.contacts.Persons.detail_action)
        if self.use_extensible:
            tb.add_action(self.modules.cal.Panel)
        tb.add_action(self.modules.pcsw.MyPersons)
        tb.add_action(self.modules.isip.MyContracts)
        tb.add_action(self.modules.jobs.MyContracts)
        #~ tb.add_action(self.modules.pcsw.Home)
        
        
    def setup_menu(self,ui,user,main):
        from django.utils.translation import ugettext_lazy as _
        from django.db import models
        
        #~ LISTINGS = [
          #~ self.modules.jobs.ContractsSituation,
          #~ self.modules.lino.DataControlListing,
        #~ ]
        
        m = main.add_menu("contacts",_("Contacts"))
        if user.is_spis:
            m.add_action(self.modules.contacts.Companies)
            m.add_action(self.modules.contacts.Persons)
            #~ m.add_action('contacts.Persons.detail')
            #~ m.add_action('contacts.Persons',label="Alle Personen",params={})
            m.add_action(self.modules.pcsw.MyPersonSearches)
            m.add_action(self.modules.contacts.AllPartners)
            #~ m.add_action(self.modules.pcsw.Newcomers)
        self.modules.isip.setup_main_menu(self,ui,user,m)
        self.modules.newcomers.setup_main_menu(self,ui,user,m)
        #~ jobs.setup_main_menu(self,ui,user,m)
        #~ m.add_action('jobs.JobProviders')


        #~ if user is None:
            #~ return main
            
        m = main.add_menu("my",_("My menu"))
        #~ m.add_action('projects.Projects')
        m.add_action(self.modules.notes.MyNotes)
        
        if user.is_spis:
            mypersons = m.add_menu("mypersons",self.modules.pcsw.MyPersons.label)
            mypersons.add_action(self.modules.pcsw.MyPersons)
            for pg in self.modules.pcsw.PersonGroup.objects.order_by('ref_name'):
                mypersons.add_action(
                  self.modules.pcsw.MyPersonsByGroup,
                  label=pg.name,
                  params=dict(master_instance=pg))
                #~ m.add_action('contacts.MyPersonsByGroup',label=pg.name,
                #~ params=dict(master_id=pg.pk))
            
        self.modules.isip.setup_my_menu(self,ui,user,m)
        self.modules.jobs.setup_my_menu(self,ui,user,m)
        self.modules.newcomers.setup_my_menu(self,ui,user,m)
        
        self.modules.cal.setup_my_menu(self,ui,user,m)
        self.modules.mails.setup_my_menu(self,ui,user,m)
        m.add_action(self.modules.uploads.MyUploads)
        m.add_action(self.modules.lino.MyTextFieldTemplates)

        #~ m.add_instance_action(user,label="My user preferences")

        if user.is_spis:
            m = main.add_menu("courses",_("Courses"))
            m.add_action(self.modules.courses.CourseProviders)
            m.add_action(self.modules.courses.CourseOffers)
            
        if user.is_newcomers:
            m  = main.add_menu("newcomers",_("Newcomers"))
            m.add_action(self.modules.newcomers.Newcomers)
            m.add_action(self.modules.newcomers.UsersByNewcomer)
            m.add_action(self.modules.newcomers.NewClients)
            
        
        self.modules.jobs.setup_main_menu(self,ui,user,main)
        
        #~ sitemenu = system.add_site_menu(self)
        #~ if False:
        m = main.add_menu("lst",_("Listings"))
        #~ for listing in LISTINGS:
            #~ m.add_action(listing,'listing')
        if user.is_spis:
            m.add_action(self.modules.jobs.JobsOverview)
            #~ m.add_action(self.modules.jobs.ContractsSearch)
            #~ m.add_action(self.modules.pcsw.OverviewClientsByUser)
            m.add_action(self.modules.pcsw.UsersWithClients)
            m.add_action(self.modules.pcsw.ClientsTest)
            #~ listings.add_instance_action(lst)
            #~ for lst in pcsw.FooListing.objects.all():
                #~ listings.add_instance_action(lst)
        
        if user.is_staff:
            cfg = main.add_menu("config",_("Configure"))
            
            self.modules.contacts.setup_config_menu(self,ui,user,cfg)
            
            #~ config_notes    = cfg.add_menu("notes",_("~Notes"))
            config_pcsw     = cfg.add_menu("pcsw",_("SIS"))
            
            #~ config_cv       = cfg.add_menu("cv",_("CV"))
            
            
            m = cfg.add_menu("courses",_("Courses"))
            m.add_action(self.modules.courses.CourseContents)
            m.add_action(self.modules.courses.CourseEndings)
            
            self.modules.notes.setup_config_menu(self,ui,user,cfg)
            self.modules.isip.setup_config_menu(self,ui,user,cfg)
            self.modules.jobs.setup_config_menu(self,ui,user,cfg)
            self.modules.newcomers.setup_config_menu(self,ui,user,cfg)
            
            config_pcsw.add_action(self.modules.pcsw.PersonGroups)
        
            if True: # user.is_expert:
                self.modules.properties.setup_config_menu(self,ui,user,cfg)
        
            config_pcsw.add_action(self.modules.pcsw.Activities)
            config_pcsw.add_action(self.modules.pcsw.ExclusionTypes)
            config_pcsw.add_action(self.modules.pcsw.AidTypes)
            #~ config_jobs.add_action('jobs.Jobs')
            #~ m.add_action('pcsw.JobTypes')
            #~ m.add_action('pcsw.CoachingTypes')
            
            #~ links.setup_config_menu(self,ui,user,cfg)
            
            
            config_pcsw.add_action(self.modules.uploads.UploadTypes)
            
            self.modules.cal.setup_config_menu(self,ui,user,cfg)
            self.modules.mails.setup_config_menu(self,ui,user,cfg)
            self.modules.lino.setup_config_menu(self,ui,user,cfg)
            
            m = main.add_menu("explorer",_("Explorer"))
            
            m.add_action(self.modules.contacts.AllPersons)
            self.modules.contacts.setup_explorer_menu(self,ui,user,m)
            self.modules.notes.setup_explorer_menu(self,ui,user,m)
            self.modules.isip.setup_explorer_menu(self,ui,user,m)
            self.modules.jobs.setup_explorer_menu(self,ui,user,m)
            self.modules.newcomers.setup_explorer_menu(self,ui,user,m)
            m.add_action(self.modules.uploads.Uploads)
            m.add_action(self.modules.pcsw.Exclusions)
            m.add_action(self.modules.pcsw.PersonSearches)
            #~ m.add_action(self.modules.lino.ContentTypes)
            m.add_action(self.modules.properties.Properties)
            m.add_action(self.modules.thirds.Thirds)
            
            courses = m.add_menu("courses",_("Courses"))
            courses.add_action(self.modules.courses.Courses)
            courses.add_action(self.modules.courses.CourseRequests)
            
            
            self.modules.cal.setup_explorer_menu(self,ui,user,m)
            
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
        from lino.tools import models_by_abc
        from django.db.models import Q
        from lino.modlib.isip import models as isip
        #~ from lino.apps.pcsw.models import only_my_persons
        
        for obj in self.modules.contacts.Person.objects.filter(
          Q(coach2=user)|Q(coach2__isnull=True,coach1=user)):
        #~ for obj in only_my_persons(
            #~ self.modules.contacts.Person.objects.all(),user):
            yield obj
        for obj in self.modules.uploads.Upload.objects.filter(user=user):
            yield obj
        for model in models_by_abc(isip.ContractBase):
            for obj in model.objects.filter(user=user):
                yield obj
                
                
    def migrate_from_1_4_3(self,globals_dict): 
        """
        - :mod:`lino.modlib.contacts` : renamed "Contact" to "Partner".
        - :mod:`lino.modlib.mails` : renamed "Mail.contact" to "Mail.partner".
        - renamed "bcss" to "cbss"
        - renamed "lino.apps.dsbe" to "lino.apps.pcsw"
        - cal.Event.rset
        """
        from lino.tools import resolve_model
        #~ from lino.utils import mti
        #~ from lino.utils import dblogger
        
        globals_dict.update(bcss_IdentifyPersonRequest = resolve_model("cbss.IdentifyPersonRequest"))
        globals_dict.update(contacts_Contact=resolve_model("contacts.Partner"))
        globals_dict.update(dsbe_Activity = resolve_model("pcsw.Activity"))
        globals_dict.update(dsbe_AidType = resolve_model("pcsw.AidType"))
        globals_dict.update(dsbe_Course = resolve_model("courses.Course"))
        globals_dict.update(dsbe_CourseContent = resolve_model("courses.CourseContent"))
        globals_dict.update(dsbe_CourseEnding = resolve_model("courses.CourseEnding"))
        globals_dict.update(dsbe_CourseOffer = resolve_model("courses.CourseOffer"))
        globals_dict.update(dsbe_CourseProvider = resolve_model("courses.CourseProvider"))
        globals_dict.update(dsbe_CourseRequest = resolve_model("courses.CourseRequest"))
        globals_dict.update(dsbe_Exclusion = resolve_model("pcsw.Exclusion"))
        globals_dict.update(dsbe_ExclusionType = resolve_model("pcsw.ExclusionType"))
        globals_dict.update(dsbe_LanguageKnowledge = resolve_model("cv.LanguageKnowledge"))
        globals_dict.update(dsbe_PersonGroup = resolve_model("pcsw.PersonGroup"))
        globals_dict.update(dsbe_PersonSearch = resolve_model("pcsw.PersonSearch"))
        globals_dict.update(dsbe_WantedLanguageKnowledge = resolve_model("pcsw.WantedLanguageKnowledge"))
        
        mails_Recipient = resolve_model("mails.Recipient")
        def create_mails_recipient(id, mail_id, contact_id, type, address, name):
            return mails_Recipient(id=id,mail_id=mail_id,partner_id=contact_id,type=type,address=address,name=name)
        globals_dict.update(create_mails_recipient=create_mails_recipient)
        
        cal_Event = resolve_model("cal.Event")
        new_content_type_id = globals_dict['new_content_type_id']
        def create_cal_event(id, user_id, created, modified, owner_type_id, owner_id, project_id, build_time, calendar_id, uid, start_date, start_time, summary, description, access_class_id, sequence, auto_type, user_modified, rset_id, end_date, end_time, transparent, type_id, place_id, priority_id, status_id):
            owner_type_id = new_content_type_id(owner_type_id)
            return cal_Event(id=id,user_id=user_id,created=created,modified=modified,owner_type_id=owner_type_id,owner_id=owner_id,project_id=project_id,build_time=build_time,calendar_id=calendar_id,uid=uid,start_date=start_date,start_time=start_time,summary=summary,description=description,access_class_id=access_class_id,sequence=sequence,auto_type=auto_type,user_modified=user_modified,
                #~ rset_id=rset_id,
                end_date=end_date,end_time=end_time,transparent=transparent,type_id=type_id,place_id=place_id,priority_id=priority_id,status_id=status_id)
        globals_dict.update(create_cal_event=create_cal_event)
        
    
        return '1.4.4'
                

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
  'lino.modlib.properties',
  'lino.modlib.contacts',
  #~ 'lino.modlib.projects',
  'lino.modlib.notes',
  #~ 'lino.modlib.links',
  'lino.modlib.uploads',
  'lino.modlib.thirds',
  'lino.modlib.cal',
  'lino.modlib.mails',
  'lino.modlib.cv',
  'lino.modlib.jobs',
  'lino.modlib.isip',
  'lino.modlib.cbss',
  'lino.modlib.newcomers',
  'lino.apps.pcsw',
  'lino.apps.pcsw.courses',
  #~ 'south', # http://south.aeracode.org
)

#~ LANGUAGES = language_choices('de','fr','nl','en')
#~ LANGUAGES = language_choices('de','fr','en')

