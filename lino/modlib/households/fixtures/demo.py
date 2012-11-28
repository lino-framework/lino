# -*- coding: UTF-8 -*-
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
The `demo` fixture for `households`
===================================

Creates some households by marrying a few Persons.

"""

#~ from django.contrib.contenttypes.models import ContentType
#~ from lino.utils.instantiator import Instantiator, i2d
from lino.core.modeltools import resolve_model
from django.utils.translation import ugettext_lazy as _


from django.db import models
from django.conf import settings
from lino.utils.babel import babel_values
from lino.utils import Cycler
#~ from lino.utils.choicelists import Gender
#~ from lino.modlib.contacts.utils import Gender
from lino import mixins


def objects():
  
    Role = resolve_model('households.Role')
    Member = resolve_model('households.Member')
    Household = resolve_model('households.Household')
    Person = resolve_model('contacts.Person')
    
    MEN = Cycler(Person.objects.filter(gender=mixins.Genders.male).order_by('birth_date'))
    WOMEN = Cycler(Person.objects.filter(gender=mixins.Genders.female).order_by('birth_date'))
    
    for i in range(3):
        he = MEN.pop()
        she = WOMEN.pop()
        #~ fam = Household(father=MEN.pop(),mother=WOMEN.pop())
        fam = Household(name=he.last_name+"-"+she.last_name,type_id=3)
        yield fam
        yield Member(household=fam,person=he,role=Role.objects.get(pk=1))
        yield Member(household=fam,person=she,role=Role.objects.get(pk=2))
    
