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

from lino.adamo.exceptions import DataVeto

from lino.schemas.sprl import demo
from lino.schemas.sprl.tables import *
from lino.misc.tsttools import TestCase, main

class Case(TestCase):

    def setUp(self):
        TestCase.setUp(self)
        self.sess = demo.startup(self.ui)
        
    def tearDown(self):
        self.sess.shutdown()


    def test01(self):
        
        l = []
        for t in self.sess.schema.getTableList():
            s = t.getTableName() + ": "
            s += ", ".join(["%s(%s)"%a
                           for a in t.getPrimaryAtoms()])
            l.append(s)

        s = "\n".join(l)

        #print s

        self.assertEquivalent(s,"""\
Languages: id(StringType)
Users: id(StringType)
Currencies: id(StringType)
Nations: id(StringType)
Cities: nation_id(StringType), id(AutoIncType)
Organisations: id(AutoIncType)
Partners: id(AutoIncType)
PartnerTypes: id(StringType)
Events: id(AutoIncType)
EventTypes: id(StringType)
Journals: id(StringType)
Years: id(IntType)
Products: id(AutoIncType)
Invoices: jnl_id(StringType), seq(IntType)
InvoiceLines: invoice_jnl_id(StringType), invoice_seq(IntType), line(IntType)
Bookings: invoice_jnl_id(StringType), invoice_seq(IntType), seq(IntType)
Authors: id(AutoIncType)
AuthorEvents: author_id(AutoIncType), seq(AutoIncType)
AuthorEventTypes: id(AutoIncType)
Topics: id(AutoIncType)
Publications: id(AutoIncType)
Quotes: id(AutoIncType)
PubTypes: id(StringType)
PubByAuth: p_id(AutoIncType), c_id(AutoIncType)
Pages: id(AutoIncType)
Projects: id(AutoIncType)
ProjectStati: id(StringType)
News: id(AutoIncType)
Newsgroups: id(StringType)
""")

        
if __name__ == '__main__':
    main()
