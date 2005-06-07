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

import os, types

from lino.misc.tsttools import TestCase
from lino.schemas.sprl import demo
from lino.schemas.sprl.tables import *

"""
Here we test how a query translates to SQL.
"""

class Case(TestCase):

    def setUp(self):
        TestCase.setUp(self)
        self.db = demo.startup()
        self.db.setBabelLangs('en')

    def tearDown(self):
        self.db.shutdown()


    def test01(self):

        #conn = self.db.conn
        

        """ Pointers to a table with simple primary key will produce a
        single column whose name is the pointer's name with the pointed
        table's primary key suffixed, usually "_id". """
        
        q = self.db.query(Organisations,"id name city nation")
        assert q.getJoinList() == ""
        #self.assertEquivalent(q.getSqlSelect(), """
        self.assertEquivalent(q.getSqlSelect(), """\
SELECT id, name, city_nation_id, city_id, nation_id FROM Organisations
        """)

        q = self.db.query(Invoices,"seq date jnl remark partner")
        assert q.getJoinList() == ""
        #self.assertEquivalent(q.getSqlSelect(), """
        self.assertEquivalent(q.getSqlSelect(), """
        SELECT
            jnl_id, 
            seq,
            date, 
            remark,
            partner_id
        FROM Invoices 
        """)


        

        """ If a non-primary-key column from a foreign table is
        requested, then this table will automatically be joined to the
        query.

        A join in a query will automatically make sure that the
        necessary atoms are included in the column list.
        
        """
        
        q = self.db.query(Organisations,
                          "id name city.name nation.id nation.name")
        self.assertEquivalent(q.getSqlSelect(), """
        SELECT
            lead.id,
            lead.name,
            lead.city_nation_id, 
            city.nation_id,
            lead.city_id,
            city.id,
            city.name,
            lead.nation_id,
            nation.id,
            nation.name_en
        FROM Organisations AS lead
            LEFT JOIN Cities AS city
                  ON (lead.city_nation_id = city.nation_id
                  AND lead.city_id = city.id)
            LEFT JOIN Nations AS nation
                  ON (lead.nation_id = nation.id)
        """)
        # atom city_id has automatically been added because necessary
        # for the join        
        assert q.getJoinList() == "city nation"


        q = self.db.query(Invoices,"seq date jnl remark partner.name")
        self.assertEquivalent(q.getSqlSelect(), """
        SELECT
            lead.jnl_id,
            lead.seq,
            lead.date,
            lead.remark,
            lead.partner_id,
            partner.id,
            partner.name
        FROM Invoices AS lead
            LEFT JOIN Partners AS partner
                ON (lead.partner_id = partner.id)
        """)


        # atom city_id has automatically been added because necessary
        # for the join
        self.assertEqual(q.getJoinList(),"partner")

        

        """ Invoices has a complex primary key, so the 'invoice' pointer
        in a InvoiceLines query will be expanded to the 3 columns that
        make up the primary key.  """
        
        q = self.db.query(InvoiceLines,
                          "invoice product unitPrice")
        self.assertEquivalent(q.getSqlSelect(), """
        SELECT
            invoice_jnl_id,
            invoice_seq,
            line,
            product_id,
            unitPrice
        FROM InvoiceLines 
        """)

        self.assertEqual(q.getJoinList(),"")
        
        q = self.db.query(InvoiceLines,
                          "invoice.date product.name unitPrice")
        self.assertEqual(q.getJoinList(),"invoice product")
        self.assertEquivalent(q.getSqlSelect(), """
        SELECT
          lead.invoice_jnl_id,
          lead.invoice_seq,
          lead.line,
          invoice.jnl_id,
          invoice.seq,
          invoice.date,
          lead.product_id,
          product.id,
          product.name,
          lead.unitPrice
        FROM InvoiceLines AS lead
          LEFT JOIN Invoices AS invoice
             ON (lead.invoice_jnl_id = invoice.jnl_id
                AND lead.invoice_seq = invoice.seq)
          LEFT JOIN Products AS product
             ON (lead.product_id = product.id)
        """)


        """
        
        until now we had only level-1 joins: the query's leadTable
        points to another table and the query wants some column from
        this foreign table.

        a level-2 join is when the leadTable points to another table who
        then points on her part to a third table who contains the
        requested column.
        
        Example: if I am on an InvoiceLines row and want to know the
        name of the customer who bought this item, then the SQL query
        must look up the invoice header who knows the partner_id, then
        look up for this id in the Partners table to get his name
        
        """
        
        q = self.db.query(InvoiceLines,
            "invoice.partner.name product.name")
        self.assertEquivalent(q.getSqlSelect(), """
        SELECT
          lead.invoice_jnl_id,
          lead.invoice_seq,
          lead.line,
          invoice.jnl_id,
          invoice.seq,
          invoice.partner_id,
          invoice_partner.id,
          invoice_partner.name,
          lead.product_id,
          product.id,
          product.name
        FROM InvoiceLines AS lead
          LEFT JOIN Invoices AS invoice
             ON (lead.invoice_jnl_id = invoice.jnl_id
                AND lead.invoice_seq = invoice.seq)
          LEFT JOIN Partners AS invoice_partner
             ON (invoice.partner_id = invoice_partner.id)
          LEFT JOIN Products AS product
             ON (lead.product_id = product.id)
        """)
        assert q.getJoinList() == "invoice invoice_partner product"
        
        """
        - invoice is a pointer from InvoiceLines to Invoices 
        - invoice_partner is a pointer from Invoices to Partners
        - product is a pointer from InvoiceLines to Products
        """

        
        """ Note : `invoice.partner_id` and not
        `invoice.invoice_partner_id`
        """

        CITIES = self.db.query(Cities)
        eupen = CITIES.findone(name="Eupen")
        q = self.db.query(Partners,
                          "name", city=eupen)
        assert q.getJoinList() == ""
        #self.assertEquivalent(q.getSqlSelect(), """
        self.assertEquivalent(q.getSqlSelect(), """
        SELECT id, name, city_nation_id, city_id        
        FROM Partners
        WHERE city_nation_id = 'be'
        AND city_id = %d
        """ % eupen.id)



if __name__ == "__main__":
    from unittest import main
    main()
    #from lino.misc import tsttools
    #tsttools.run("2")
    

