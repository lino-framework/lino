## Copyright 2008-2011 Luc Saffre
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
Default settings for :doc:`/igen/index`.

"""
import os
import sys
from os.path import join,dirname, normpath, abspath
from lino.apps.std.settings import *

class Lino(Lino):
  
    languages = ['en']
    
    #~ source_dir = os.path.dirname(__file__)
  
    title = "Lino/iGen"
    domain = "igen-demo.saffre-rumma.net"
    help_url = "http://lino.saffre-rumma.net/igen/index.html"
    
    person_model = "contacts.Person"
    company_model = "contacts.Company"
    
    #~ residence_permit_upload_type = None
    #~ work_permit_upload_type = None
    #~ driving_licence_upload_type = None 
    #ledger_providers='4400',
    #ledger_customers='4000',
    #~ sales_base_account = None # '7000',
    #~ sales_vat_account = None # '4510',
    
    #~ def init_site_config(self,sc):
        #~ super(IgenSite,self).init_site_config(sc)
        #~ sc.next_partner_id = 200000

    def get_app_source_file(self):
        return __file__
        

LINO = Lino(__file__,globals())

#~ TIME_ZONE = 'Europe/Tallinn'
TIME_ZONE = None

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
#~ LANGUAGE_CODE = 'en'
#~ LANGUAGE_CODE = 'en-US'
#~ LANGUAGE_CODE = 'fr-BE'


INSTALLED_APPS = (
    #~ 'django.contrib.auth',
    'lino.modlib.users',
    'django.contrib.contenttypes',
    'lino',
    'lino.modlib.countries',
    'lino.modlib.contacts',
    #~ 'lino.modlib.notes',
    'lino.modlib.cal',
    'lino.modlib.mails',
    'lino.modlib.products',
    'lino.modlib.journals',
    'lino.modlib.ledger',
    'lino.modlib.sales',
    'lino.modlib.finan',
    'lino.modlib.uploads',
    'lino.apps.igen',
    #~ 'lino.modlib.properties',
)

# Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
# Always use forward slashes, even on Windows.
# Don't forget to use absolute paths, not relative paths.
#~ TEMPLATE_DIRS = (
      #~ # join(abspath(DATA_DIR),'templates'),
      #~ join(abspath(LINO.project_dir),'templates'),
      #~ join(abspath(dirname(lino.__file__)),'templates'),
#~ )

# Make this unique, and don't share it with anybody.
#~ SECRET_KEY = 'cqt^18t(Fb#14a@s%mbtdif+ih8fscpf8l9aw+0ivo2!3c(c%&'
