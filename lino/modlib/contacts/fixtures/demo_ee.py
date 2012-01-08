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

from django.conf import settings
from lino.tools import resolve_model
from lino.utils.instantiator import Instantiator
#from lino import reports
#contacts = reports.get_app('contacts')


def objects():
    #~ city = Instantiator('countries.City','name country').build
    #~ yield city('Vigala','EE')
    if 'et' in settings.LINO.languages:
        lang = 'et'
    else:
        # if language 'et' is not available, use the default language
        lang = settings.LINO.languages[0]
        
    company = Instantiator(settings.LINO.company_model,country='EE',language=lang).build
    yield company(name=u'Minu Firma OÜ')
    yield company(name=u'Mets ja Puu OÜ')
    yield company(name=u'Kenavälja OÜ')
    
    person = Instantiator(settings.LINO.person_model,"first_name last_name",country='EE').build
    yield person(u'Aare',u'Aaresild')
    yield person(u'Ahti',u'Aaspere')
    yield person(u'Peeter',u'Bach')
    yield person(u'Tiina',u'Engelbert')
    yield person(u'Inge',u'Hallik')
    yield person(u'Harri',u'Hunt')
    yield person(u'Ingmar',u'Iliste')
    yield person(u'Jaan',u'Janno')
    yield person(u'Jaan',u'Jõgi')
    yield person(u'Karl',u'Kask')
    yield person(u'Leo',u'Lepamets')
    yield person(u'Madis',u'Mäeorg')
    yield person(u'Natalja',u'Nagel')
    yield person(u'Ott',u'Ojavee')
    yield person(u'Piret',u'Paas')
    yield person(u'Rannes',u'Rannala')
    yield person(u'Silja',u'Sääsk')
    yield person(u'Tõnu',u'Tamm')
    yield person(u'Tiina',u'Türnpuu')
    yield person(u'Urmas',u'Uukivi')
    
