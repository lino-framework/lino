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

from lino.apps.ledger import demo
from lino.misc.tsttools import TestCase, main

class Case(TestCase):

    def setUp(self):
        TestCase.setUp(self)
        self.sess = demo.startup()
        
    def tearDown(self):
        self.sess.shutdown()


    def test01(self):
        
        l = []
        for t in self.sess.db.app.getTableList():
            s = t.getTableName() + ": "
            s += ", ".join(["%s(%s)"%a
                           for a in t.getPrimaryAtoms()])
            l.append(s)

        s = "\n".join(l)

        #print s

        self.assertEquivalent(s,"""\
Currencies: id(StringType)
Languages: id(StringType)
Nations: id(StringType)
Cities: nation_id(StringType), id(AutoIncType)
Organisations: id(AutoIncType)
Persons: id(AutoIncType)
Partners: id(AutoIncType)
PartnerTypes: id(StringType)
Products: id(AutoIncType)
Journals: id(StringType)
BankStatements: jnl_id(StringType), seq(AutoIncType)
MiscOperations: jnl_id(StringType), seq(AutoIncType)
Invoices: jnl_id(StringType), seq(AutoIncType)
InvoiceLines: invoice_jnl_id(StringType), invoice_seq(AutoIncType), line(AutoIncType)
BalanceItems: id(StringType)
CashFlowItems: id(StringType)
ProfitAndLossItems: id(StringType)
Accounts: id(AutoIncType)
Bookings: id(AutoIncType)
""")

        
if __name__ == '__main__':
    main()
