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
from tempfile import gettempdir
from lino.apps.std.settings import *

class Lino(Lino):
  
    source_dir = os.path.dirname(__file__)
  
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

    def configure(self,sc):
        super(Lino,self).configure(sc)
        
    def setup_main_menu(self):
  
        from django.utils.translation import ugettext_lazy as _
        from lino.utils import perms

        from lino import models as system

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

        from lino.utils import perms
        from lino import models as system

        #~ ledger.set_accounts(
          #~ #providers='4400',
          #~ #customers='4000',
          #~ sales_base='7000',
          #~ sales_vat='4510',
        #~ )
          
        m = self.add_menu("contacts","~Contacts")
        m.add_action('contacts.Companies')
        m.add_action('contacts.Persons')
        #~ m.add_action('sales.Customers')

        m = self.add_menu("prods","~Products")
        m.add_action('products.Products')
        m.add_action('products.ProductCats')

        m = self.add_menu("journals","~Journals",can_view=perms.is_staff)
        
        #~ for jnl in journals.Journal.objects.all().order_by('pos'):
            #~ m.add_action('contacts.MyPersonsByGroup',label=jnl.name,
                #~ params=dict(master_instance=jnl))
        
        for jnl in journals.Journal.objects.all().order_by('pos'):
            m.add_action(str(jnl.get_doc_report()),
                params=dict(master_instance=jnl))
            # m.add_action(jnl.get_doc_report(),args=[jnl.pk])
            #~ m.add_action(str(jnl.get_doc_report()))
            
        m = self.add_menu("sales","~Sales",
          can_view=perms.is_authenticated)
        #m.add_action(Orders())
        #m.add_action(Invoices())
        m.add_action('sales.DocumentsToSign')
        m.add_action('sales.PendingOrders')

        #~ m = self.add_menu("admin","~Administration",
          #~ can_view=perms.is_staff)
        #~ m.add_action(MakeInvoicesDialog())

        m = self.add_menu("config","~Configuration",
          can_view=perms.is_staff)
        m.add_action('sales.InvoicingModes')
        m.add_action('sales.ShippingModes')
        m.add_action('sales.PaymentTerms')
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

        system.add_site_menu(self)

LINO = Lino(__file__,globals())

#~ PROJECT_DIR = abspath(dirname(__file__))
#~ DATA_DIR = join(PROJECT_DIR,"data")
#~ LINO_SETTINGS = join(PROJECT_DIR,"lino_settings.py")
#~ MEDIA_ROOT = join(LINO.project_dir,'media')
TIME_ZONE = 'Europe/Tallinn'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-US'
#~ LANGUAGE_CODE = 'fr-BE'

#~ ROOT_URLCONF = 'lino.demos.dsbe.urls'

#~ SITE_ID = 1 # see also fill.py


INSTALLED_APPS = (
    #~ 'django.contrib.auth',
    'lino.modlib.users',
    'django.contrib.contenttypes',
    #~ 'django.contrib.sessions',
    #~ 'django.contrib.sites',
    #~ 'django.contrib.markup',
    #'django.contrib.admin',
    #'django.contrib.databrowse',
    
    'lino',
    'lino.modlib.countries',
    'lino.modlib.contacts',
    'lino.modlib.notes',
    'lino.modlib.products',
    'lino.modlib.journals',
    #~ 'lino.modlib.documents',
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
