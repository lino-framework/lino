#coding: latin1
## Copyright Luc Saffre 2004.

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

this was my first oogen testcase.  Principle: first you fill document
with content (adding elements to its story).  Tables are also
collected in a separate list.

A same document tree can be reused by several generators.  Currently I
am interested in spreadsheets and documents. graphics come later.
Spreadsheets use only the tables, not the story of a document.


"""

import os
import unittest
from lino.ui import console
from lino.misc import tsttools
from lino.oogen import Document


class Case(tsttools.TestCase):
    
    def test01(self):

        doc = Document("1")
        doc.h(1,"Generating OpenOffice documents")
        doc.p("Here is a table:")
        t = doc.table()
        t.addColumn()
        t.addColumn()
        t.addRow("Kunde","Datum")
        t.addRow("Hinz","2004-11-16")
        t.addRow("Kunz","2004-11-17")
    
        doc.p("Here is another paragraph.")

        for ext in (".sxw", ".sxc"):
            fn = self.addTempFile(doc.name+ext,
                                  showOutput=True)
            doc.save(fn)

if __name__ == "__main__":
    unittest.main()
