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



"""
Logical columns (row attributes) versus physical columns (atoms)

"""

from lino.misc.tsttools import TestCase, main
from lino.adamo.datatypes import itod
from lino.schemas.sprl import demo

from lino.schemas.sprl.tables import \
     Partners, Journals, Invoices, Products



class Case(TestCase):

    def setUp(self):
        
        self.db = demo.startup()

    def tearDown(self):
        self.db.shutdown()


    def test01(self):
        "create an invoice"

        PARTNERS = self.db.query(Partners)
        JOURNALS = self.db.query(Journals)
        INVOICES = self.db.query(Invoices)
        PRODUCTS = self.db.query(Products)
        
        """get the partner # 1 and Journal."""
        p = PARTNERS.peek(1)
        self.assertEqual(p.getLabel(),"Luc Saffre")

        jnl = JOURNALS.peek("OUT")
        self.assertEqual(jnl.id,"OUT")

        "create a query"
        
        invoices = INVOICES.query("jnl date remark",
                                          partner=p)
        #invoices.setSamples(partner=p)
        #csr = invoices.executeSelect()
        #count = csr.rowcount
        count = len(invoices)
        

        self.assertEqual(count,0)

        # create a new invoice :
        i = invoices.appendRow(jnl,itod(20030816),"test")
        
        """
        The `seq` field of INVOICES is an auto-incrementing integer.
        """
        self.assertEqual(i.seq,2)

        
        #i.commit()

        # self.db.commit()

        """the following should be equivalent :
        i = p.invoices.appendRow()
        """


        """ len(p.invoices) is increased because an invoice for this
        partner has been created:"""

        """create two rows in this invoice :"""

        #lines = INVOICELINES.query("line product qty",invoice=i)
        #lines.setSamples(invoice=i)

        lines = i.lines.query("line product qty")

        lines.appendRow(1,PRODUCTS.peek(3), 2) # price is 12
        lines.appendRow(2,PRODUCTS.peek(16), 3) # price is 56

        # INVOICELINES.commit()

        l = []
        for line in lines:
            l.append(str(line.product.name))
        s = " ".join(l)
        self.assertEqual(s,"Chair Table")
            
        # register() the invoice :
        i.close()
        
        self.assertEqual(i.amount, 2*12 + 3*56 )

##          # get a cursor on BOOKINGS :
##          q = BOOKINGS.query("invoice")

##          # we want only the bookings for one invoice
##          q.setSlice(q.invoice,i)

##          """first invocation of len() will silently execute a query to
##          find out the number of rows. There must be 2 rows"""

##          # bc.executeCount()

##          self.assertEqual(len(q),2)



if __name__ == '__main__':
    main()

