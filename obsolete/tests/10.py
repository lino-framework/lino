## Copyright 2003-2006 Luc Saffre

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

"Detail" RowAttributes reimplemented.  Details are used to "access a
Pointer from the other side".  If Table.addPointer() is called with
the "detailName" argument, then the other Table (the one where the
Pointer points to) will get a row method with that name.

For example, a NATIONS instance has a mathod cities() which returns a
pre-build query of CITIES from this nation.


"""

from lino.misc.tsttools import TestCase, main
from lino.apps.contacts.contacts_demo import startup
from lino.apps.contacts.contacts_tables import Nation

class Case(TestCase):
    
    #todo="Crash in big contacts demo"
    def setUp(self):
        TestCase.setUp(self)
        self.db = startup(big=True)
        #self.db = demo.beginSession(populator=None,big=True)
        #demo.populate(self.db,big=True)
        
    def tearDown(self):
        self.db.shutdown()
        
    def test01(self):
        be = self.db.query(Nation).peek('be')
        s = ''
        
        #cities=be.cities
        #print cities._masters
        #cities=be.cities.query(orderBy="name",
        #                       search="eup")
        #print cities.getSqlSelect()
        for city in be.cities(orderBy="name",search="eup"):
            s += city.zipCode + " "+ city.name + "\n"
        # print s
        self.assertEqual(s,"""\
4700 Eupen
9700 Leupegem
4120 Neupre
4280 Villers-le-Peuplier
""")
        
if __name__ == '__main__':
    main()

