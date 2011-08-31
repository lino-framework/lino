# -*- coding: UTF-8 -*-
## Copyright 2009-2011 Luc Saffre
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
    city = Instantiator('countries.City','name country').build
    City = resolve_model('countries.City')
    #~ Country = resolve_model('countries.Country')
    #~ BE = Country.objects.get(pk="BE")
    try:
        City.objects.get(country__isocode='BE',name="Eupen")
    except City.DoesNotExist:
        yield city('Eupen','BE',zip_code='4700')
        yield city('Kelmis','BE',zip_code='4720')
        yield city('Kettenis','BE',zip_code='4701')
        yield city('Raeren','BE',zip_code='4730')
        yield city('Angleur','BE',zip_code='4031')
        yield city('Bruxelles','BE',zip_code='1000')
        #~ yield city('Brussel','BE',zip_code='1000')
        #~ yield city('Brüssel','BE',zip_code='1000')
        yield city('Oostende','BE',zip_code='8400')
    
    yield city('Vigala','EE')
    yield city('Tallinn','EE')
    yield city(u'Pärnu','EE')
    yield city(u'Tartu','EE')
    yield city(u'Narva','EE')
    yield city(u'Ääsmäe','EE')

    yield city(u'Aachen','DE')
    yield city(u'Köln','DE')
    yield city(u'Berlin','DE')
    yield city(u'Hamburg','DE')
    yield city(u'München','DE')
    
    yield city(u'Maastricht','NL')
    yield city(u'Amsterdam','NL')
    yield city(u'Den Haag','NL')
    yield city(u'Rotterdam','NL')
    yield city(u'Utrecht','NL')
    yield city(u'Breda','NL')
    
    yield city(u'Paris','FR')
    yield city(u'Nice','FR')
    yield city(u'Metz','FR')
    yield city(u'Strasbourg','FR')
    yield city(u'Nancy','FR')
    yield city(u'Marseille','FR')
