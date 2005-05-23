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



from lino.misc.tsttools import TestCase, main
from lino.schemas.sprl import demo
from lino.schemas.sprl.tables \
     import Cities, Nations, Invoices, InvoiceLines, Journals

class Case(TestCase):
    
    "testing Datasource.apply_GET()"
    
    skip=1

    def setUp(self):
        TestCase.setUp(self)
        
        self.db = demo.startup()

    def tearDown(self):
        self.db.shutdown()


    def test01(self):
        CITIES = self.db.query(Cities)
        NATIONS = self.db.query(Nations)
        be = NATIONS.peek('be')
        
        # method 1
        q = CITIES.query(nation=be)
        l = len(q)
        
        # method 2
        q = CITIES.query()
        q.apply_GET(nation=('be',))
        self.assertEqual(l,len(q))

        # method 3
        q = be.cities.query()
        self.assertEqual(l,len(q))
        
    def test02(self):
        JOURNALS = self.db.query(Journals)
        INVOICES = self.db.query(Invoices)
        INVOICELINES = self.db.query(InvoiceLines)
        
        jnl = JOURNALS.peek('OUT')
        inv = INVOICES.peek(jnl,1)
        self.assertEqual(str(inv.partner),"Anton Ausdemwald")
        self.assertEqual(len(inv.lines),2)

        q = INVOICELINES.query(invoice=inv)
        l = len(q)
        
        q = INVOICELINES.query()
        q.apply_GET(invoice=("OUT,1",))
        
        self.assertEqual(l,len(q))
        

if __name__ == '__main__':
    main()

