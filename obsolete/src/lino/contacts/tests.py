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
from lino.django.contacts.models import Person, Country, City, Contact

class TestCase(unittest.TestCase):
    
    def setUp(self):
        be=Country(name="Belgium",iso2="be")
        de=Country(name="Germany",iso2="de")
        ee=Country(name="Estonia",iso2="ee")
        vv=City(name="Vana-Vigala",country=ee)
        v=City(name="Vigala",country=ee)
        
        self.john=Person(firstname="John",name="Lennon")
        self.luc=Person(firstname="Luc",name="Saffre")
        self.luc.save()
        self.luc.home=Contact(
          addr1="Rummajaani talu",
          country=ee,city=vv,zipcode="78003")
        self.luc.home.save()
        
        
    def test01(self):
        self.assertEquals(unicode(self.luc.home), '''
Rummajaani talu
78003 Vana-Vigala
Estonia''')

## to run these tests, see
## http://docs.djangoproject.com/en/dev/topics/testing/#topics-testing
## the following wouldn't work because there's no database
## if __name__ == '__main__':
##    unittest.main()