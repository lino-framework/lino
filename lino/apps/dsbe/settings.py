## Copyright 2009-2011 Luc Saffre
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
Default settings for :doc:`/dsbe/index`.

"""

import os
import lino

from lino.apps.std.settings import *

from lino.utils.jsgen import js_code

class Lino(Lino):
    source_dir = os.path.dirname(__file__)
    title = "Lino/DSBE"
    #~ domain = "dsbe.saffre-rumma.net"
    help_url = "http://lino.saffre-rumma.net/dsbe/index.html"
    
    #~ residence_permit_upload_type = None
    #~ work_permit_upload_type = None
    #~ driving_licence_upload_type = None 
    
    #~ def init_site_config(self,sc):
        #~ super(LinoSite,self).init_site_config(sc)
        #~ sc.next_partner_id = 200000
        #~ print 20110305, self.__class__

    def configure(self,sc):
        super(Lino,self).configure(sc)
        
    def setup_main_menu(self):
      try:
  
        from django.utils.translation import ugettext_lazy as _
        from lino.utils import perms

        #~ from lino import models as system
        from lino.apps.dsbe import models as dsbe

        m = self.add_menu("contacts",_("~Contacts"))
        m.add_action('contacts.Companies')
        m.add_action('contacts.Persons')
        m.add_action('dsbe.MySearches')

        m = self.add_menu("my",_("~My menu"),can_view=perms.is_authenticated)
        #~ m.add_action('projects.Projects')
        m.add_action('notes.MyNotes')
        m.add_action('uploads.MyUploads')
        m.add_action('dsbe.MyContracts')
        m.add_action('contacts.MyPersons')
        for pg in dsbe.PersonGroup.objects.all():
            m.add_action('contacts.MyPersonsByGroup',label=pg.name,
                params=dict(master_instance=pg))
            #~ m.add_action('contacts.MyPersonsByGroup',label=pg.name,
            #~ params=dict(master_id=pg.pk))
            #~ m.add_request_action(contacts.MyPersonsByGroup().request(master_instance=pg),label=pg.name)


        m = self.add_menu("courses",_("~Courses"),can_view=perms.is_authenticated)
        m.add_action('dsbe.Courses')
        m.add_action('contacts.CourseProviders')
        m.add_action('dsbe.CourseContents')
        m.add_action('dsbe.CourseEndings')
        
        #~ sitemenu = system.add_site_menu(self)
        
        cfg = self.add_menu("config",_("~Configure"),can_view=perms.is_authenticated)
        
        
        config_contacts = cfg.add_menu("contacts",_("~Contacts"),can_view=perms.is_authenticated)
        config_notes    = cfg.add_menu("notes",_("~Notes"),can_view=perms.is_authenticated)
        config_props    = cfg.add_menu("props",_("~Properties"),can_view=perms.is_authenticated)
        config_dsbe     = cfg.add_menu("dsbe",_("~DSBE"),can_view=perms.is_authenticated)
        config_cv       = cfg.add_menu("cv",_("C~V"),can_view=perms.is_authenticated)
        config_etc      = cfg.add_menu("etc",_("~System"),can_view=perms.is_authenticated)
        
        config_contacts.add_action('contacts.CompanyTypes',can_view=perms.is_staff)
        config_contacts.add_action('contacts.ContactTypes',can_view=perms.is_staff)
        config_contacts.add_action('countries.Languages',can_view=perms.is_staff)
        config_contacts.add_action('countries.Countries')
        config_contacts.add_action('countries.Cities')
        
        config_notes.add_action('notes.NoteTypes',can_view=perms.is_staff)
        config_notes.add_action('notes.EventTypes',can_view=perms.is_staff)
        
        #~ mm = m.add_menu("manager",_("~Manager"),can_view=perms.is_authenticated)
        #~ ma = m.add_menu("admin",_("Local Site ~Administrator"),can_view=perms.is_staff)
        #~ me = m.add_menu("expert",_("~Expert"),can_view=perms.is_expert)
        
        #~ m.add_action('projects.ProjectTypes')
        config_dsbe.add_action('dsbe.ContractTypes',can_view=perms.is_staff)
        config_dsbe.add_action('dsbe.PersonGroups')
        
        from lino.modlib.properties import models as properties
        
        config_props.add_action('properties.PropGroups',can_view=perms.is_expert)
        config_props.add_action('properties.PropTypes',can_view=perms.is_expert)
        for pg in properties.PropGroup.objects.all():
            #~ mm.add_request_action(properties.PropsByGroup().request(master_instance=pg),label=pg.name)
            config_props.add_action('properties.PropsByGroup',params=dict(master_instance=pg),label=pg.name)
        
        #~ config_props.add_action('properties.PropsByGroup',can_view=perms.is_staff)
        #~ ma.add_action('dsbe.Skills1')
        #~ ma.add_action('dsbe.Skills2')
        #~ ma.add_action('dsbe.Skills3')
        #~ me.add_action('auth.Permissions')
        #~ ma.add_action('auth.Users')
        #~ me.add_action('auth.Groups')
        #~ m.add_action('dsbe.DrivingLicenses')
        config_cv.add_action('dsbe.StudyTypes')
        config_cv.add_action('dsbe.Activities')
        
        config_dsbe.add_action('dsbe.ExclusionTypes')
        config_dsbe.add_action('dsbe.AidTypes')
        config_dsbe.add_action('dsbe.ContractEndings')
        #~ m.add_action('dsbe.JobTypes')
        config_dsbe.add_action('dsbe.ExamPolicies')
        #~ m.add_action('dsbe.CoachingTypes')
        
        config_etc.add_action('links.LinkTypes')
        config_etc.add_action('uploads.UploadTypes')
        config_etc.add_action('users.Users',can_view=perms.is_staff)
        
        #~ config_etc.add_instance_action(self.config,label=_('Site Configuration'),can_view=perms.is_staff)
        config_etc.add_instance_action(self.config,can_view=perms.is_staff)
        

        m = cfg.add_menu("explorer",_("E~xplorer"),
          can_view=perms.is_staff)
        #m.add_action('properties.PropChoices')
        #~ m.add_action('properties.PropValues')
        m.add_action('notes.Notes')
        m.add_action('links.Links')
        m.add_action('dsbe.Exclusions')
        m.add_action('dsbe.Contracts')
        m.add_action('uploads.Uploads')
        m.add_action('dsbe.CourseRequests')
        m.add_action('contenttypes.ContentTypes')
        m.add_action('dsbe.PersonSearches')
        m.add_action('properties.Properties')

        
        m = self.add_menu("help",_("~Help"))
        m.add_item('userman',_("~User Manual"),
            href='http://lino.saffre-rumma.net/dsbe/index.html')

        #~ self.main_menu.add_item('home',_("~Home"),href='/')
        self.main_menu.items.append(dict(
          xtype='button',text=_("Home"),
          handler=js_code("function() {window.location='%s';}" % self.root_url)))
      except Exception,e:
        import traceback
        traceback.print_exc(e)


LINO = Lino(__file__)


#~ PROJECT_DIR = abspath(dirname(__file__))
#~ DATA_DIR = join(PROJECT_DIR,"data")
#~ LINO_SETTINGS = join(PROJECT_DIR,"lino_settings.py")

MEDIA_ROOT = join(LINO.project_dir,'media')
#~ MEDIA_ROOT = join(PROJECT_DIR,'media')

TIME_ZONE = 'Europe/Brussels'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'de'
#~ LANGUAGE_CODE = 'de-BE'
#~ LANGUAGE_CODE = 'fr-BE'

#~ SITE_ID = 1 # see also fill.py

INSTALLED_APPS = (
  #~ 'django.contrib.auth',
  'lino.modlib.users',
  'django.contrib.contenttypes',
  #~ 'django.contrib.sessions',
  #~ 'django.contrib.sites',
  #~ 'django.contrib.markup',
  #~ 'lino.modlib.system',
  'lino',
  'lino.modlib.countries',
  #~ 'lino.modlib.documents',
  'lino.modlib.properties',
  'lino.modlib.contacts',
  #~ 'lino.modlib.projects',
  'lino.modlib.notes',
  'lino.modlib.links',
  'lino.modlib.uploads',
  'lino.modlib.thirds',
  'lino.apps.dsbe',
  #'dsbe.modlib.contacts',
  #'dsbe.modlib.projects',
  #~ 'south', # http://south.aeracode.org
)

LANGUAGES = language_choices('de','fr','nl','en')
#~ LANGUAGES = language_choices('de','fr','en')

# Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
# Always use forward slashes, even on Windows.
# Don't forget to use absolute paths, not relative paths.
TEMPLATE_DIRS = (
      #~ join(abspath(DATA_DIR),'templates'),
      join(abspath(LINO.project_dir),'templates'),
      join(abspath(dirname(lino.__file__)),'templates'),
)

