# coding: latin1

## Copyright 2003-2007 Luc Saffre

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
    verbosity=2

    def test03(self):
        "logical primary key versus atomic primary key"

        db=ledger_demo.startup()

        INVOICES = db.query(Invoice)
        INVOICELINES = db.query(ProductInvoiceLine)
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
        db.shutdown()
        


        
if __name__ == '__main__':
    main()
