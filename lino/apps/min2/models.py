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

"""
A :term:`minimal application` used for 
tests, demonstrations and didactical purposes.
"""


from django.db import models
from django.utils.translation import ugettext_lazy as _

from lino import dd

from lino.modlib.contacts import models as contacts

class Person(contacts.PersonMixin,contacts.Partner,contacts.Born):
    class Meta(contacts.PersonMixin.Meta):
        app_label = 'contacts'

class PersonDetail(contacts.PersonDetail):
    general = contacts.PersonDetail.main
    main = "general outbox.SentByPartner"
    def setup_handle(self,dh):
        dh.general.label = _("General")
    
class Company(contacts.Partner,contacts.CompanyMixin):
    class Meta(contacts.CompanyMixin.Meta):
        app_label = 'contacts'
        
class CompanyDetail(contacts.CompanyDetail):
    general = contacts.CompanyDetail.main
    main = "general outbox.SentByPartner"
    def setup_handle(self,dh):
        dh.general.label = _("General")

def site_setup(site):
    contacts.Persons.set_detail(PersonDetail())
    contacts.Companies.set_detail(CompanyDetail())

#~ def setup_master_menu(site,ui,user,m):
    #~ m.add_action(site.modules.contacts.Persons)
    #~ m.add_action(site.modules.contacts.Companies)

