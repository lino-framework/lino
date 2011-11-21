#coding: latin1

## Copyright Luc Saffre 2004-2005.

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

import os
#from lino.console import syscon
from lino.misc.tsttools  import TestCase, main
from lino.oogen import TextDocument

class Case(TestCase):
    #todo="Migrate oogen to gendoc.openoffice"
    
    def test01(self):
        "First styles"

        fn = self.addTempFile("66.sxw", showOutput=True)
        doc = TextDocument(fn)
        
        s = doc.addStyle(name="Rechts",
                         family="paragraph",
                         parentStyleName="Standard",
                         className="text")
        s.addProperties(textAlign="end",
                        justifySingleWord=False)
        
        doc.body.heading(1,"Rechnung Nr. 040235")
        doc.body.par("Datum: 10. Dezember 2004",styleName="Rechts")
        
        t = doc.body.table()
        t.column()
        t.column()
        t.column()
        t.column()
        t.row("Bezeichnung", "Menge", u"Stückpreis", "Preis")
        t.row("Tisch","1","15","15")
        t.row("Stuhl","4","10","40")
        
        doc.body.par(u"Alle Preise in €.")
        doc.body.par("Zahlungsbedingungen: ...")

        doc.save()
        
if __name__ == "__main__":
    main()
