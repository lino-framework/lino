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
first oogen testcase
"""

import os
import unittest
#from lino.ui import console
from lino.console import syscon
from lino.misc import tsttools
from lino.oogen import SpreadsheetDocument, TextDocument


class Case(tsttools.TestCase):
    def test01(self):

        fn = self.addTempFile("1.sxw", showOutput=True)
        doc = TextDocument(fn)
        doc.h(1,"Generating OpenOffice documents")
        doc.p("Here is a table:")
        t = doc.table()
        t.column()
        t.column()
        t.row("Kunde","Datum")
        t.row("Hinz","2004-11-16")
        t.row("Kunz","2004-11-17")
    
        doc.p("Here is another paragraph.")
        doc.save(syscon)
        
    def test02(self):

        fn = self.addTempFile("1.sxc", showOutput=True)
        doc = SpreadsheetDocument(fn)
        
        t = doc.table(name="Kunden")
        t.column()
        t.column()
        t.row("Kunde","Datum")
        t.row("Hinz","2004-11-16")
        t.row("Kunz","2004-11-17")
        
        t = doc.table(name="Freunde")
        t.column()
        t.column()
        t.row("Freund","Datum")
        t.row("Hinz","2004-11-16")
        t.row("Kunz","2004-11-17")
    
        doc.save(syscon)
        

##         for ext in (".sxw", ".sxc"):
##             fn = self.addTempFile(doc.name+ext,
##                                   showOutput=True)
##             doc.save(fn)

            

if __name__ == "__main__":
    unittest.main()
