# coding: latin1

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
Some tests on getDemoDB()
"""

#import types
#import unittest

from lino.misc.tsttools import TestCase, main

from lino.adamo.exceptions import DataVeto

from lino.apps.ledger import ledger_demo
from lino.apps.ledger.ledger_tables import *

class Case(TestCase):

    def setUp(self):
        TestCase.setUp(self)
        self.sess = ledger_demo.startup()
        
    def tearDown(self):
        self.sess.shutdown()


##     def test01(self):
        
##         s = " ".join([str(t.getTableName())
##               for t in self.sess.db.schema.getTableList()])

##         #print s
##         self.assertEquivalent(s, """\
## Currencies Languages Nations Cities Organisations Persons Partners PartnerTypes Products Journals BankStatements MiscOperations Invoices InvoiceLines BalanceItems CashFlowItems ProfitAndLossItems Accounts Bookings
## """)
        


    def test03(self):
        "logical primary key versus atomic primary key"

        INVOICES = self.sess.query(Invoice)
        INVOICELINES = self.sess.query(ProductInvoiceLine)
        self.assertEqual(INVOICES.getLeadTable().getPrimaryKey(),
                              ("jnl","seq"))
        self.assertEqual(
            tuple(map(lambda (n,t) : n,
                         INVOICES.getLeadTable().getPrimaryAtoms())),
            ("jnl_id","seq")
            )
        
        self.assertEqual(INVOICELINES.getLeadTable().getPrimaryKey(),
                              ("invoice","line"))
        self.assertEqual(
            tuple(map(lambda (n,t) : n,
                         INVOICELINES.getLeadTable().getPrimaryAtoms())),
            ("invoice_jnl_id","invoice_seq","line")
            )
        


        
## if __name__ == "__main__":
##      from lino.misc import tsttools
##      tsttools.run("1")

if __name__ == '__main__':
    main()
