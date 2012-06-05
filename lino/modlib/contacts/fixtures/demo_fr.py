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
"""

from django.conf import settings
from lino.utils.choicelists import Gender
from lino.utils import Cycler
from lino import dd
from lino.utils import demonames as demo
            
  
def objects():
                
    last_names = demo.LAST_NAMES_BELGIUM
    male_first_names = demo.MALE_FIRST_NAMES_FRANCE
    female_first_names = demo.FEMALE_FIRST_NAMES_FRANCE

    Person = dd.resolve_model(settings.LINO.person_model)
    City = dd.resolve_model('countries.City')
    
    CITIES = Cycler(City.objects.filter(country_id='BE',zip_code__startswith='40'))
    STREETS = streets_of_liege()
    
    common = dict(language='fr',country_id='BE')
    for i in range(100):
        yield Person(
          first_name=male_first_names.pop(),
          last_name=last_names.pop(),
          gender=Gender.male,
          city=CITIES.pop(),
          street=STREETS.pop(),
          **common
        )
        yield Person(
          first_name=female_first_names.pop(),
          last_name=last_names.pop(),
          gender=Gender.female,
          city=CITIES.pop(),
          street=STREETS.pop(),
          **common
        )
