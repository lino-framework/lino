## Copyright 2008 Luc Saffre.
## This file is part of the Lino project. 

## Lino is free software; you can redistribute it and/or modify it
## under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.

## Lino is distributed in the hope that it will be useful, but WITHOUT
## ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
## or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public
## License for more details.

## You should have received a copy of the GNU General Public License
## along with Lino; if not, write to the Free Software Foundation,
## Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

import unittest
from lino.django.contacts.models import Person

class TestCase(unittest.TestCase):
    
    def setUp(self):
        be=Country(name="Belgium",iso2="be")
        de=Country(name="Germany",iso2="de")
        ee=Country(name="Estonia",iso2="ee")
        vv=City(name="Vana-Vigala",country=ee)
        v=City(name="Vigala",country=ee)
        
        self.john=Person(firstname="John",name="Lennon")
        self.luc=Person(firstname="Luc",name="Saffre")
        self.luc.home.create(
          addr1="Rummajaani talu",
          country=ee,city=vv,zipcode="78003")
        
        
    def test01(self):
        self.assertEquals(unicode(self.luc), u'''Luc Saffre
        Rummajaani talu
        ''')
 
if __name__ == '__main__':
    unittest.main()