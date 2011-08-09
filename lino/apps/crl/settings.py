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
Default settings for :mod:`lino.apps.crl`.

"""

import os
import lino

from lino.apps.std.settings import *

from lino.utils.jsgen import js_code

class Lino(Lino):
    source_dir = os.path.dirname(__file__)
    title = "Lino/CRL"
    #~ domain = "dsbe.saffre-rumma.net"
    help_url = "http://lino.saffre-rumma.net/crl/index.html"
    #~ migration_module = 'lino.apps.polo.migrate'
    
    def get_site_menu(self,ui,user):
        from django.utils.translation import ugettext_lazy as _
        from lino.utils import perms
        from lino.utils import menus
        from lino.apps.dsbe import models as dsbe
        from lino.modlib.properties import models as properties
        from lino.modlib.cal import models as cal

        main = menus.Toolbar('main')
        m = main.add_menu("contacts",_("~Contacts"))
        m.add_action('contacts.Companies')
        m.add_action('contacts.Persons')

        if user is None:
            return main
            
        m = main.add_menu("cal",_("~Calendar"))
        m.add_action('cal.MyEvents')
        m.add_action('cal.MyTasks')
        
        if False:
            listings = main.add_menu("lst",_("~Listings"))
            LISTINGS = """
            lino.DataControlListing
            """.split()
            for listing in LISTINGS:
                listings.add_action(listing + '.listing')
            
        if True or user.is_staff:
            cfg = main.add_menu("config",_("~Configure"))
            
            config_contacts = cfg.add_menu("contacts",_("~Contacts"))
            #~ config_notes    = cfg.add_menu("notes",_("~Notes"))
            #~ config_jobs     = cfg.add_menu("jobs",_("~Jobs"))
            #~ config_cv       = cfg.add_menu("cv",_("C~V"))
            config_etc      = cfg.add_menu("etc",_("~System"))
            
            config_contacts.add_action('countries.Countries')
            config_contacts.add_action('countries.Cities')
        
            config_contacts.add_action('contacts.CompanyTypes')
            config_contacts.add_action('contacts.ContactTypes')
            config_contacts.add_action('countries.Languages')
            
            #~ config_notes.add_action('notes.NoteTypes')
            #~ config_notes.add_action('notes.EventTypes')
        
            #~ config_jobs.add_action('jobs.ContractTypes')
            #~ config_jobs.add_action('jobs.JobTypes')
        
            if False and user.is_expert:
                config_props = cfg.add_menu("props",_("~Properties"))
                config_props.add_action('properties.PropGroups')
                config_props.add_action('properties.PropTypes')
                for pg in properties.PropGroup.objects.all():
                    config_props.add_action('properties.PropsByGroup',params=dict(master_instance=pg),label=pg.name)
        
            config_etc.add_action('links.LinkTypes')
            config_etc.add_action('uploads.UploadTypes')
            
            cal.setup_config_menu(self,ui,user,cfg)
            
            config_etc.add_action('users.Users')
            #~ if self.use_tinymce:
            config_etc.add_action('lino.TextFieldTemplates')
            config_etc.add_instance_action(self.config)
        
            m = cfg.add_menu("explorer",_("E~xplorer"))
            #m.add_action('properties.PropChoices')
            #~ m.add_action('properties.PropValues')
            #~ m.add_action('contacts.AllPersons')
            #~ m.add_action('notes.Notes')
            #~ m.add_action('lino.TextFieldTemplates')
            m.add_action('links.Links')
            #~ m.add_action('jobs.Contracts')
            m.add_action('uploads.Uploads')
            m.add_action('contenttypes.ContentTypes')
            #~ m.add_action('properties.Properties')
            cal.setup_explorer_menu(self,ui,user,m)
            #~ m = m.add_menu('listings',_('~Listings'))
            #~ for listing in LISTINGS:
                #~ m.add_action(listing)

        
        m = main.add_menu("help",_("~Help"))
        m.add_item('userman',_("~User Manual"),
            href='http://lino.saffre-rumma.net/crl/index.html')

        #~ self.main_menu.add_item('home',_("~Home"),href='/')
        main.add_url_button(self.root_url,_("Home"))
          
        return main
      

LINO = Lino(__file__,globals())


#~ PROJECT_DIR = abspath(dirname(__file__))
#~ DATA_DIR = join(PROJECT_DIR,"data")
#~ LINO_SETTINGS = join(PROJECT_DIR,"lino_settings.py")

#~ MEDIA_ROOT = join(LINO.project_dir,'media')
#~ MEDIA_ROOT = join(PROJECT_DIR,'media')

TIME_ZONE = 'Europe/Brussels'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en'
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
  #~ 'lino.modlib.thirds',
  'lino.modlib.cal',
  #~ 'lino.modlib.jobs',
  'lino.apps.crl',
  #~ 'south', # http://south.aeracode.org
)

LANGUAGES = language_choices('en','fr', 'de')
