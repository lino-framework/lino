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
        
    def setup_menu(self,ui,user,main):
  
        from django.utils.translation import ugettext_lazy as _
        from lino.utils import perms

        #~ from lino.modlib.cal import models as cal
        #~ from lino.modlib.notes import models as notes

        from django.db import models

        #~ system = models.get_app('system')
        countries = models.get_app('countries')
        contacts = models.get_app('contacts')
        products = models.get_app('products')
        #~ documents = models.get_app('documents')
        ledger = models.get_app('ledger')
        sales = models.get_app('sales')
        finan = models.get_app('finan')
        journals = models.get_app('journals')
        notes = models.get_app('notes')
        cal = models.get_app('cal')
        mails = models.get_app('mails')

        m = main.add_menu("contacts","~Contacts")
        m.add_action('contacts.Companies')
        m.add_action('contacts.Persons')
        #~ m.add_action('sales.Customers')

        m = main.add_menu("prods","~Products")
        m.add_action('products.Products')
        m.add_action('products.ProductCats')
        
        if user and user.is_active:
            m = main.add_menu("my",_("~My menu"))
            cal.setup_my_menu(self,ui,user,m)
            mails.setup_my_menu(self,ui,user,m)
        
        
        
        if user and user.is_staff:
            m = main.add_menu("journals","~Journals")
            
            #~ for jnl in journals.Journal.objects.all().order_by('pos'):
                #~ m.add_action('contacts.MyPersonsByGroup',label=jnl.name,
                    #~ params=dict(master_instance=jnl))
            
            for jnl in journals.Journal.objects.all().order_by('pos'):
                m.add_action(str(jnl.get_doc_report()),
                    params=dict(master_instance=jnl))
                # m.add_action(jnl.get_doc_report(),args=[jnl.pk])
                #~ m.add_action(str(jnl.get_doc_report()))
            
        #~ if user and user.is_active:
            #~ m = main.add_menu("sales","~Sales")
            #~ #m.add_action(Orders())
            #~ #m.add_action(Invoices())
            #~ m.add_action('sales.DocumentsToSign')
            #~ m.add_action('sales.PendingOrders')

        #~ m = self.add_menu("admin","~Administration",
          #~ can_view=perms.is_staff)
        #~ m.add_action(MakeInvoicesDialog())

        if user and user.is_staff:
            m = main.add_menu("config","~Configuration")
            sales.setup_config_menu(self,ui,user,m)
            notes.setup_config_menu(self,ui,user,m)
            cal.setup_config_menu(self,ui,user,m)
            m.add_action('journals.Journals')
            #~ m = self.add_menu("ledger","~Ledger",
              #~ can_view=perms.is_authenticated)
            m.add_action('ledger.Accounts')
            

            m.add_action('countries.Countries')
            #m.add_action(contacts.Countries())
            m.add_action('contenttypes.ContentTypes')
            #m = self.add_menu("system","~System")
            #~ m.add_action('auth.Permissions')
            #~ m.add_action('auth.Users')
            m.add_action('users.Users')
            #~ m.add_action('auth.Groups')
            #m.can_view = perms.is_staff
            
        if user and user.is_expert:
            m = main.add_menu("explorer",_("E~xplorer"))
            sales.setup_explorer_menu(self,ui,user,m)
            notes.setup_explorer_menu(self,ui,user,m)
            cal.setup_explorer_menu(self,ui,user,m)
            mails.setup_explorer_menu(self,ui,user,m)
            
            

        #~ system.add_site_menu(self)
        
        m = main.add_menu("help",_("~Help"))
        m.add_item('userman',_("~User Manual"),
            href='http://lino.saffre-rumma.net/igen/index.html')

        return main
        

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
    'lino.modlib.notes',
    'lino.modlib.cal',
    'lino.modlib.mails',
    'lino.modlib.products',
    'lino.modlib.journals',
    'lino.modlib.ledger',
    'lino.modlib.sales',
    'lino.modlib.finan',
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
