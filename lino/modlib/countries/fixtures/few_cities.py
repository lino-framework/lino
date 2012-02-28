# -*- coding: UTF-8 -*-
## Copyright 2009-2012 Luc Saffre
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

from lino.utils import dblogger
from lino.tools import resolve_model
from lino.utils.instantiator import Instantiator
#~ from lino.utils.babel import default_language
#from lino import reports
#contacts = reports.get_app('contacts')


def objects():
    #~ dblogger.info("Installing countries few_cities fixture")
    City = resolve_model('countries.City')
    city = Instantiator(City,'name country').build
    def make_city(name,country_id,**kw):
        try:
            return City.objects.get(country__isocode=country_id,name=name)
        except City.DoesNotExist:
            return city(name,country_id,**kw)
        
    yield make_city(u'Eupen','BE',zip_code='4700')
    yield make_city(u'Kelmis','BE',zip_code='4720')
    yield make_city(u'Kettenis','BE',zip_code='4701')
    yield make_city(u'Raeren','BE',zip_code='4730')
    yield make_city(u'Angleur','BE',zip_code='4031')
    yield make_city(u'Liège','BE',zip_code='4000')
    yield make_city(u'Bruxelles','BE',zip_code='1000')
    #~ yield city('Brussel','BE',zip_code='1000')
    #~ yield city(u'Brüssel','BE',zip_code='1000')
    yield make_city(u'Oostende','BE',zip_code='8400')
    
    yield make_city('Vigala','EE')
    yield make_city('Tallinn','EE')
    yield make_city(u'Pärnu','EE')
    yield make_city(u'Tartu','EE')
    yield make_city(u'Narva','EE')
    yield make_city(u'Ääsmäe','EE')

    yield make_city(u'Aachen','DE')
    yield make_city(u'Köln','DE')
    yield make_city(u'Berlin','DE')
    yield make_city(u'Hamburg','DE')
    yield make_city(u'München','DE')
    
    yield make_city(u'Maastricht','NL')
    yield make_city(u'Amsterdam','NL')
    yield make_city(u'Den Haag','NL')
    yield make_city(u'Rotterdam','NL')
    yield make_city(u'Utrecht','NL')
    yield make_city(u'Breda','NL')
    
    yield make_city(u'Paris','FR')
    yield make_city(u'Nice','FR')
    yield make_city(u'Metz','FR')
    yield make_city(u'Strasbourg','FR')
    yield make_city(u'Nancy','FR')
    yield make_city(u'Marseille','FR')
