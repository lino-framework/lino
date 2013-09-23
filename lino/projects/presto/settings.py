## Copyright 2011-2013 Luc Saffre
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


from lino.projects.std.settings import *
#~ from lino.projects.presto import __version__, __url__, __name__

from lino.modlib import vat

class Site(Site,vat.SiteMixin):

    #~ title = __name__
    verbose_name = "Lino Presto"
    version = "0.1"
    url = "http://www.lino-framework.org/autodoc/lino.projects.presto"
    #~ description = "a Lino application for Belgian Public Welfare Centres"
    #~ author = 'Luc Saffre'
    #~ author_email = 'luc.saffre@gmail.com'
    
    #~ demo_fixtures = 'std few_countries few_cities few_languages props demo demo2 history'.split()
    #~ demo_fixtures = 'std all_countries be few_cities few_languages props democfg demo demo2'.split()
    demo_fixtures = 'std few_countries few_cities few_languages props democfg demo demo2'.split()
    
    #~ languages = ['en']
    languages = 'de fr et en'
    
    project_model = 'tickets.Project'
    user_model = 'users.User'
    
    #~ remote_user_header = "REMOTE_USER"
    
    override_modlib_models = [
      'contacts.Person','contacts.Company',
      'households.Household',
      'sales.Invoice', 'sales.InvoiceItem']
    
      
    #~ def get_main_action(self,user):
        #~ return self.modules.lino.Home.default_action
        
    #~ def setup_quicklinks(self,ui,user,tb):
        #~ tb.add_action(self.modules.contacts.Persons.detail_action)
        
    #~ def get_partner_account(self,voucher):
        #~ tt = voucher.get_trade_type()
        #~ if tt.name == 'sales':
            #~ return '400000'
        #~ elif tt.name == 'purchases':
            #~ return '440000'
            
    #~ def get_product_base_account(self,tt,product):
        #~ if tt.name == 'sales':
            #~ return '704000'
        #~ elif tt.name == 'purchases':
            #~ return '604000'
            
    #~ def get_vat_account(self,tt,vc,vr):
        #~ return '472100'
        
        
    def setup_choicelists(self):
        """
        Defines application-specific default user profiles.
        Local site administrators can override this in their :xfile:.
        """
        from lino import dd
        from django.utils.translation import ugettext_lazy as _
        dd.UserProfiles.reset('* office')
        add = dd.UserProfiles.add_item
        add('000', _("Anonymous"),       '_ _', 'anonymous',
            readonly=True,authenticated=False)
        add('100', _("User"),            'U U', 'user')
        add('900', _("Administrator"),   'A A', 'admin')
        
            
    def get_installed_apps(self):
        for a in super(Site,self).get_installed_apps(): yield a
        yield 'django.contrib.contenttypes'
        yield 'lino.modlib.system'
        yield 'lino.modlib.users'
        yield 'lino.modlib.countries'
        yield 'lino.modlib.properties'
        yield 'lino.modlib.contacts'
        yield 'lino.modlib.households'
        yield 'lino.modlib.products'
        yield 'lino.modlib.accounts'
        yield 'lino.modlib.ledger'
        yield 'lino.modlib.vat'
        #~ yield 'lino.modlib.sales'
        yield 'lino.modlib.auto.sales'
        #~ 'lino.modlib.projects',
        yield 'lino.modlib.blogs'
        yield 'lino.modlib.tickets'
        #~ 'lino.modlib.links',
        yield 'lino.modlib.uploads'
        #~ 'lino.modlib.thirds',
        yield 'lino.modlib.cal'
        yield 'lino.modlib.outbox'
        #~ yield 'lino.modlib.postings'
        #~ yield 'lino.modlib.pages'
        yield 'lino.projects.presto'
      



SITE = Site(globals()) 


