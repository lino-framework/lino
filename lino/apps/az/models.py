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

from django.db import models
from django.utils.translation import ugettext_lazy as _


from lino import dd
from lino import mixins
#~ from lino.models import SiteConfig

from lino.modlib.contacts import models as contacts
from lino.modlib.cal import models as cal

class Person(contacts.PersonMixin,contacts.Partner,contacts.Born):
    class Meta(contacts.PersonMixin.Meta):
        app_label = 'contacts'
        #~ # see :doc:`/tickets/14`
        #~ verbose_name = _("Person")
        #~ verbose_name_plural = _("Persons")


class PersonDetail(contacts.PersonDetail):
#~ class PersonDetail(dd.DetailLayout):
   
    
    #~ contact = contacts.PersonDetail.main
    
    mails = """
    mails.InboxByPartner
    mails.OutboxByPartner
    """
    
    main = "contact mails"

    contact = """
    box1 box2
    remarks contacts.RolesByPerson
    """
    
    box1 = """
    last_name first_name:15 #title:10
    country city zip_code:10
    #street_prefix street:25 street_no street_box
    addr2:40
    """
    
    box2 = """
    id:12 language
    email
    phone fax
    gsm
    gender birth_date age:10 
    """
    
    
    def setup_handle(self,lh):
      
        lh.contact.label = _("Contact")
        lh.mails.label = _("Mails")




class Company(contacts.Partner,contacts.CompanyMixin):
    class Meta(contacts.CompanyMixin.Meta):
        app_label = 'contacts'
        #~ # see :doc:`/tickets/14`
        #~ verbose_name = _("Company")
        #~ verbose_name_plural = _("Companies")
        
class Event(cal.Event):
    class Meta(cal.Event.Meta):
        app_label = 'cal'

class Task(cal.Task):
    class Meta(cal.Task.Meta):
        app_label = 'cal'
     
     
def site_setup(site):
    site.modules.contacts.Persons.set_detail(PersonDetail())

