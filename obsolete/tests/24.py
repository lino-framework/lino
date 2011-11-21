# coding: latin1
## Copyright Luc Saffre 2003-2006

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


"""
bug 20040724 : setting a sample on a query modifies the 

"""
from lino.misc.tsttools import TestCase, main
from lino.apps.contacts.contacts_demo import startup
from lino.apps.contacts.contacts_tables import City, Nation


class Case(TestCase):

    def setUp(self):
        TestCase.setUp(self)
        self.db = startup()

    def tearDown(self):
        self.db.shutdown()


    def test01(self):
        CITIES = self.db.query(City)
        NATIONS = self.db.query(Nation)
        
        q = CITIES.query()
        l = len(q)
        
        be = NATIONS.peek('be')
        q = CITIES.query(nation=be)
        
        q = CITIES.query()
        self.assertEqual(l,len(q))
        

if __name__ == '__main__':
    main()

