# coding: latin1

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

"""
Some tests on getDemoDB()
"""

#import types
#import unittest

from lino.adamo.exceptions import DataVeto

from lino.apps.ledger import demo
from lino.apps.ledger.tables import *
from lino.misc.tsttools import TestCase, main

class Case(TestCase):

    def setUp(self):
        TestCase.setUp(self)
        self.sess = demo.startup()
        
    def tearDown(self):
        self.sess.shutdown()


    def test01(self):
        
        s = " ".join([str(t.getTableName())
              for t in self.sess.db.app.getTableList()])

        #print s
        self.assertEquivalent(s, """\
Users Currencies Nations Cities Organisations Partners PartnerTypes
Journals Years Products Invoices InvoiceLines BalanceItems
CashFlowItems ProfitAndLossItems Accounts Bookings
""")
        


    def test03(self):
        "logical primary key versus atomic primary key"

        INVOICES = self.sess.query(Invoices)
        INVOICELINES = self.sess.query(InvoiceLines)
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
