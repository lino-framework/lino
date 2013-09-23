# -*- coding: UTF-8 -*-
## Copyright 2012-2013 Luc Saffre
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

from lino.projects.std.settings import *

from lino.modlib import cal
from lino.modlib import vat

#~ class Site(Site):
#~ class Site(Site,cal.SiteMixin):
class Site(Site,vat.SiteMixin):
    #~ title = __name__
    version = "0.0.1"
    verbose_name = "Lino-HWS"
    url = "http://www.lino-framework.org/autodoc/lino.projects.homeworkschool"
    #~ author = "Luc Saffre"
    #~ author_email = "luc.saffre@gmx.net"
    
    #~ help_url = "http://lino.saffre-rumma.net/az/index.html"
    #~ migration_module = 'lino.projects.az.migrate'
    
    demo_fixtures = 'std few_countries few_cities few_languages demo demo2'.split()
    
    #~ project_model = 'contacts.Person'
    #~ project_model = 'courses.Pupil'
    project_model = 'courses.Course'
    #~ project_model = None
    user_model = 'users.User'
    
    languages = ('en', 'de', 'fr')
    
    use_eid_jslib = False
    
    #~ index_view_action = "dsbe.Home"
    
    override_modlib_models = [
        #~ 'contacts.Partner', 
        'contacts.Person', 
        #~ 'contacts.Company',
        #~ 'households.Household',
        'sales.Invoice', 
        'sales.InvoiceItem', 
        ]
    
    #~ remote_user_header = "REMOTE_USER"
    
       
    #~ def get_main_action(self,user):
        #~ return self.modules.ui.Home.default_action
        
    #~ def get_application_info(self):
        #~ return (__name__,__version__,__url__)
        
        
    #~ def setup_quicklinks(self,ui,user,tb):
        #~ tb.add_action(self.modules.contacts.Persons.detail_action)
        #~ if self.use_extensible:
            #~ tb.add_action(self.modules.cal.Panel)
        #~ tb.add_action(self.modules.dsbe.MyPersons)
        #~ tb.add_action(self.modules.isip.MyContracts)
        #~ tb.add_action(self.modules.jobs.MyContracts)
        
    def get_installed_apps(self):
        for a in super(Site,self).get_installed_apps():
            yield a
        yield 'django.contrib.contenttypes'
        yield 'lino.modlib.system'
        yield 'lino.modlib.users'
        yield 'lino.modlib.countries'
        yield 'lino.modlib.contacts'
        yield 'lino.modlib.households'
        yield 'lino.modlib.notes'
        yield 'lino.modlib.uploads'
        yield 'lino.modlib.cal'
        yield 'lino.modlib.outbox'
        yield 'lino.modlib.pages'
        
        yield 'lino.modlib.accounts'
        yield 'lino.modlib.ledger'
        yield 'lino.modlib.vat'
        yield 'lino.modlib.products'
        yield 'lino.modlib.auto.sales'
        
        yield 'lino.modlib.courses'
        yield 'lino.projects.homeworkschool'
      
    def setup_choicelists(self):
        """
        This defines default user profiles for :mod:`lino_welfare`.
        """
        #~ raise Exception(123)
        from lino import dd
        from django.utils.translation import ugettext_lazy as _
        dd.UserProfiles.reset('* office')
        add = dd.UserProfiles.add_item
        
        add('000', _("Anonymous"),     '_ _', name='anonymous',
            readonly=True,authenticated=False)
        add('100', _("User"),          'U U', name='user')
        add('900', _("Administrator"), 'A A', name='admin')
        
      
