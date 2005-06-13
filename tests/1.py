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

from lino.schemas.sprl import demo
from lino.schemas.sprl.tables import *
from lino.misc.tsttools import TestCase, main

class Case(TestCase):

    def setUp(self):
        TestCase.setUp(self)
        self.sess = demo.startup() # self.ui)
        
        #self.db = demo.beginSession()
        #self.db.installto(globals())

    def tearDown(self):
        self.sess.shutdown()


    def test01(self):
        
        ae = self.assertEqual
        
        l1 = [str(t.getTableName())
              for t in self.sess.db.app.getTableList()]

        s=" ".join(l1)
        
        #print s

        self.assertEquivalent(s, """\
Users Currencies Nations Cities Organisations Partners PartnerTypes
Journals Years Products Invoices InvoiceLines BalanceItems
CashFlowItems ProfitAndLossItems Accounts Bookings
""")
        
        self.sess.setBabelLangs("en")
        PARTNERS = self.sess.query(Partners)
        CITIES = self.sess.query(Cities)
        row = PARTNERS.peek(1)

        # print "foobar " + repr(row.getValues())

        """ The row returned by peek() is an object whose properties can
        be accessed (or not) according to the specific rules.    """

        # simple fields :
        
        ae(row.id,1)
        ae(row.name,"Saffre")
        ae(str(row),"Luc Saffre")

        tallinn = CITIES.findone(name="Tallinn")
        
        ae(row.city,tallinn)
        
        ae(row.city.name,"Tallinn")
        ae(row.nation.name,"Estonia")
        




    def test05(self):
        
        """ If you are going to create several rows and don't want to
        specify the field names each time, then you can create a Query:
        """

        PARTNERS = self.sess.query(Partners)
        CITIES = self.sess.query(Cities)
        
        q = PARTNERS.query('id firstName name')
        
        row = q.appendRow(1000,"Jean","Dupont")
        self.assertEqual(row.id,1000)
        self.assertEqual(row.firstName,"Jean")
        self.assertEqual(row.name,"Dupont")
        
        q.appendRow(1001,"Joseph","Dupont")
        q.appendRow(1002,"Juliette","Dupont")
        
    def test06(self):
        "Samples"
        
        """ If you tell a Query of Cities that you want only cities in
        Belgium, then use this query to create a city row, then this row
        will automatically know that it's nation is Belgium.    """

        NATIONS = self.sess.query(Nations)
        PARTNERS = self.sess.query(Partners)
        CITIES = self.sess.query(Cities)
        
        be = NATIONS.peek("be")
        q = CITIES.query(nation=be)
        q = be.cities #.query('id name')
        stv = q.appendRow(name='Sankt-Vith')
        # print row.getValues()
        self.assertEqual(stv.nation,be)
        self.assertEqual(stv.name,"Sankt-Vith")
        # q.appendRow(21,'Eynatten')


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
