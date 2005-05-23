# coding: latin1
## Copyright Luc Saffre 2003-2005

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
Logical columns (row attributes) versus physical columns (atoms)

"""
import types

from lino.misc.tsttools import TestCase
from lino.schemas.sprl import demo
from lino.schemas.sprl.tables import *

class Case(TestCase):

    def setUp(self):
        TestCase.setUp(self)
        self.db = demo.startup()
        self.db.setBabelLangs('en')

    def tearDown(self):
        self.db.shutdown()

    def test02(self):
        ""
        q = self.db.query(Products,"name price", orderBy="name")
        l = []
        for prod in q:
            l.append("a %s costs %s." % (prod.name,str(prod.price)))
        s = " ".join(l)
        self.assertEqual(s,"a Chair costs 12. a Table costs 56.")
            

        
        
    def test03(self):
        "2 successive appendRow() without specifying id"
        AUTHORS = self.db.query(Authors)
        pot = AUTHORS.appendRow(firstName="Harry",name="Potter")
        bel = AUTHORS.appendRow(firstName="Harry",name="Bellafonte")
        self.assertEqual(pot.id, bel.id-1)
        

    
## if __name__ == "__main__":
##      print __file__
##      from lino.misc import tsttools
##      tsttools.run(__file__[:-3]) 
    

if __name__ == '__main__':
    import unittest
    unittest.main()

