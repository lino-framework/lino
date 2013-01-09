# -*- coding: UTF-8 -*-
## Copyright 2009-2013 Luc Saffre
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
Adds an arbitrary selection of a few demo cities.
"""

from __future__ import unicode_literals

import logging
logger = logging.getLogger(__name__)

from django.core.exceptions import MultipleObjectsReturned
from lino.utils import dblogger
from lino.core.modeltools import resolve_model
from lino.utils.instantiator import Instantiator
from lino.utils.babel import babel_values


from lino import dd

def objects():
    #~ dblogger.info("Installing countries few_cities fixture")
    countries = dd.resolve_app('countries')
    #~ City = resolve_model('countries.City')
    City = countries.City
    Country = countries.Country
    CityTypes = countries.CityTypes
    city = Instantiator(City,'name country').build
    def make_city(name,country_id,**kw):
        try:
            return City.objects.exclude(type=CityTypes.county).get(
                country__isocode=country_id,name=name)
        except MultipleObjectsReturned:
            qs = City.objects.exclude(type=CityTypes.county).filter(country__isocode=country_id,name=name)
            logger.info("Oops, there are multiple cities in %s", qs)
            return qs[0]
        except City.DoesNotExist:
            return city(name,country_id,**kw)
        
    BE = Country.objects.get(pk='BE')
    DE = Country.objects.get(pk='DE')
    FR = Country.objects.get(pk='FR')
    yield make_city('Eupen','BE',zip_code='4700',type=CityTypes.city)
    yield City(country=BE,zip_code='4720',type=CityTypes.city,
      **babel_values('name',de='Kelmis',fr='La Calamine',en="Kelmis"))
    yield make_city('Kettenis','BE',zip_code='4701',type=CityTypes.village)
    yield make_city('Raeren','BE',zip_code='4730',type=CityTypes.village)
    yield make_city('Angleur','BE',zip_code='4031',type=CityTypes.city)
    yield City(country=BE,zip_code='4000',type=CityTypes.city,
      **babel_values('name',de='Lüttich',fr='Liège',en='Liège',nl="Luik"))
    yield City(country=BE,zip_code='1000',type=CityTypes.city,
      **babel_values('name',de='Brüssel',fr='Bruxelles',nl="Brussel",en="Brussels"))
    #~ yield city('Brussel','BE',zip_code='1000')
    #~ yield city(u'Brüssel','BE',zip_code='1000')
    yield City(country=BE,zip_code='8400',type=CityTypes.city,
      **babel_values('name',de='Ostende',fr='Ostende',nl="Oostende",en="Ostende"))
    
    harjumaa = make_city(u'Harjumaa','EE',type=CityTypes.county)
    yield harjumaa
    parnumaa = make_city(u'Pärnumaa','EE',type=CityTypes.county)
    yield parnumaa
    raplamaa = make_city(u'Raplamaa','EE',type=CityTypes.county)
    yield raplamaa
    
    yield make_city(u'Vigala','EE',type=CityTypes.municipality,parent=raplamaa)
    yield make_city(u'Rapla','EE',type=CityTypes.town,parent=raplamaa)
    
    yield make_city(u'Tallinn','EE',type=CityTypes.city,parent=harjumaa)
    yield make_city(u'Pärnu','EE',type=CityTypes.town,parent=parnumaa)
    yield make_city(u'Tartu','EE',type=CityTypes.town)
    yield make_city(u'Narva','EE',type=CityTypes.town)
    yield make_city(u'Ääsmäe','EE',type=CityTypes.town,parent=harjumaa)

    #~ yield make_city(u'Aachen','DE')
    yield City(country=DE,type=CityTypes.city,
      **babel_values('name',de='Aachen',fr='Aix-la-Chapelle',nl="Aken",en="Aachen"))
    yield City(country=DE,type=CityTypes.city,
      **babel_values('name',de='Köln',fr='Cologne',nl="Keulen",en="Cologne"))
    yield make_city(u'Berlin','DE')
    yield make_city(u'Hamburg','DE')
    yield City(country=DE,type=CityTypes.city,
      **babel_values('name',de='München',fr='Munich',en="Munich"))
    
    yield make_city(u'Maastricht','NL')
    yield make_city(u'Amsterdam','NL')
    yield make_city(u'Den Haag','NL')
    yield make_city(u'Rotterdam','NL')
    yield make_city(u'Utrecht','NL')
    yield make_city(u'Breda','NL')
    
    yield City(country=FR,type=CityTypes.city,
      **babel_values('name',de='Paris',fr='Paris',en="Paris",et="Pariis",nl="Parijs"))
    yield City(country=FR,type=CityTypes.city,
      **babel_values('name',de='Nizza',fr='Nice',en="Nice"))
    yield make_city(u'Metz','FR')
    yield make_city(u'Strasbourg','FR')
    yield make_city(u'Nancy','FR')
    yield make_city(u'Marseille','FR')
