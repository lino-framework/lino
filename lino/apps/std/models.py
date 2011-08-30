#coding: UTF-8
## Copyright 2010 Luc Saffre
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
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

#~ import lino
#~ logger.debug(__file__+' : started')

from lino import reports
from lino import mixins
from lino.utils import perms
from lino import fields
from lino.modlib.contacts import models as contacts
#from lino.modlib.projects import models as projects
#from lino.modlib.properties import models as properties
from lino.modlib.projects import models as projects
from lino.modlib.notes import models as notes
#~ from lino.models import get_site_config
from lino.tools import get_field


#~ class Person(contacts.Person):
    #~ class Meta:
        #~ app_label = 'contacts'
    
#~ class Company(contacts.Company):
    #~ class Meta:
        #~ app_label = 'contacts'
    
    