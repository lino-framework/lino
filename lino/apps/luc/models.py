# -*- coding: UTF-8 -*-
## Copyright 2011-2012 Luc Saffre
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
import cgi
import datetime

from django.db import models
#~ from django.db.models import Q
from django.conf import settings
from django.utils.translation import ugettext_lazy as _


from lino import mixins

from lino.modlib.contacts import models as contacts
from lino.modlib.notes import models as notes

class Person(contacts.PersonMixin,contacts.Partner,contacts.Born,mixins.Printable):
    class Meta(contacts.PersonMixin.Meta):
        app_label = 'contacts'
        


class Company(contacts.Partner,contacts.CompanyMixin):
    
    class Meta(contacts.CompanyMixin.Meta):
        app_label = 'contacts'

#~ class Companies(contacts.Partners):
    #~ model = Company
    #~ app_label = 'contacts'
    #~ order_by = ["name"]

class Note(notes.Note,contacts.PartnerDocument):
    class Meta:
        app_label = 'notes'
        #~ verbose_name = _("Event/Note") # application-specific override
        #~ verbose_name_plural = _("Events/Notes")

