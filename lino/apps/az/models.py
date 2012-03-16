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
     
     
