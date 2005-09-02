# coding: latin1

## Copyright 2003-2005 Luc Saffre

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
from lino.adamo.datatypes import itod
from lino.apps.ledger import demo

from lino.apps.ledger.tables import \
     Partner, Journal, Invoice, Product



class Case(TestCase):
    
    "Create an invoice for a table and 4 chairs"
    
    todo="updateRow() must first store all values, then validate"

    def setUp(self):
        TestCase.setUp(self)
        self.db = demo.startup()

    def tearDown(self):
        self.db.shutdown()


    def test01(self):
        "create an invoice"

        PARTNERS = self.db.query(Partner)
        JOURNALS = self.db.query(Journal)
        INVOICES = self.db.query(Invoice)
        PRODUCTS = self.db.query(Product)
        
        """get the partner # 1 and Journal."""
        p = PARTNERS.peek(1)
        self.assertEqual(str(p),"Luc Saffre")

        jnl = JOURNALS.peek("OUT")
        self.assertEqual(jnl.id,"OUT")

        "create a query"
        
        invoices = INVOICES.query("jnl date remark lines",
                                  partner=p)
        #invoices.setSamples(partner=p)
        #csr = invoices.executeSelect()
        #count = csr.rowcount
        count = len(invoices)
        

        self.assertEqual(count,0)

        # create a new invoice :
        i = invoices.appendRow(jnl,itod(20030816),"test")
        
        """
        The `seq` field of Invoices is an auto-incrementing integer.
        """
        self.assertEqual(i.seq,2)

        
        """ len(p.invoices) is increased because an invoice for this
        partner has been created:"""

        """create two rows in this invoice :"""

        lines = i.lines.query("line product qty")

        lines.appendRow(1,PRODUCTS.peek(3), 4) # price is 12
        lines.appendRow(2,PRODUCTS.peek(16), 1) # price is 56

        i.lines.query(
            "line product.name qty unitPrice amount").showReport()

        s=self.getConsoleOutput()
        print s
        self.assertEquivalent(s,"""\
        """)

        # register() the invoice :
        i.close()
        
        self.assertEqual(i.amount, 2*12 + 3*56 )



if __name__ == '__main__':
    main()

