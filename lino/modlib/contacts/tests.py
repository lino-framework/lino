# -*- coding: utf-8 -*-
## Copyright 2008-2011 Luc Saffre
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


from lino.utils.test import TestCase
#from lino.igen import models
#from lino.modlib.contacts.models import Contact, Companies
#from lino.modlib.countries.models import Country
from lino.modlib.contacts.models import Companies

from lino.tools import resolve_model,resolve_app
Person = resolve_model('contacts.Person')
contacts = resolve_app('contacts')
#Companies = resolve_model('contacts.Companies')
from lino.utils.instantiator import Instantiator

class StdTest(TestCase):
    #~ fixtures = [ 'std', 'few_countries', 'ee', 'be', 'demo', 'demo_ee']
    #~ fixtures = 'few_countries few_languages demo_cities std demo demo_ee'.split()
    fixtures = 'std few_countries few_cities few_languages props demo'.split()
    
    
person = Instantiator('contacts.Person').build
company = Instantiator('contacts.Company').build
        
def test01(self):
    """
    Tests some basic funtionality.
    """
    luc = Person.objects.get(first_name__exact='Luc',last_name__exact='Saffre')
    self.assertEquals(luc.address(), u'''\
Herrn Luc SAFFRE
Uus 1
Vana-Vigala küla
78003 Vigala
Estonia''')
    self.assertEquals(luc.address_location(), u'''\
Uus 1
Vana-Vigala küla
78003 Vigala
Estonia''')
    
    
        
        
