#coding: latin1
## Copyright Luc Saffre 2003-2004.

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

    
from lino.misc.tsttools import TestCase, main
#import unittest
from lino.apps.pinboard import demo
from lino.apps.pinboard.tables import *


class Case(TestCase):
    """
    Filters (not finished)
    """

    def setUp(self):
        TestCase.setUp(self)
        self.db = demo.startup()
        
        #self.db = demo.beginSession()

    def tearDown(self):
        self.db.shutdown()

    def test01(self):
        "Simple query with a filter"
        q = self.db.query(Author,
                          "firstName name",
                          orderBy='name')
        q.setSqlFilters('name LIKE "B%"')
        s = "\n".join([str(row) for row in q])
        self.assertEqual(s,"""\
Donald Bisset
Georges Brassens
Jacques Brel""")

    def test02(self):
        "Finding Georges Brassens"
        AUTHORS = self.db.query(Author)
        p = AUTHORS.findone(firstName="Georges",
                            name="Brassens")
        # self.assertNotEqual(p,None)
        self.assertEqual(p.name,"Brassens")
        self.assertEqual(p.firstName,"Georges")
        
        

if __name__ == '__main__':
    main()

