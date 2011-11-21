#coding: latin1
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

20041004 : pizzeria2.beginSession() now also populates.  That's okay I
           think. Adapted this test.

"""
   
from lino import adamo #import quickdb, beginQuickSession
from lino.adamo.datatypes import itod
from lino.misc.tsttools import TestCase, main
from lino.apps.pizzeria import pizzeria, services
from lino.apps.pizzeria.services import Service
from lino.apps.pizzeria.pizzeria import Customer,\
     Product, Order, OrderLine


class Case(TestCase):
    """
    Tests switching pointers
    """

    def setUp(self):
        TestCase.setUp(self)
        app=services.MyPizzeria()
        self.sess = app.createContext()
        services.populate(self.sess)
        #services.beginSession()

    def tearDown(self):
        self.sess.shutdown()

    def test01b(self):
        # testing whether INSERT INTO is correctly done
        SERV = self.sess.query(Service)
        SERV.startDump()
        s1 = SERV.appendRow(name="bring home",price=99)
        sql = SERV.stopDump()
        self.assertEquivalent(sql,"""\
INSERT INTO Services (
  id, name, price, responsible
)
  VALUES  ( 3,  'bring home', 99, NULL );
""")
        
    def test02(self):
        #pizzeria2.populate(self.db)
        SERV = self.sess.query(Service)
        CUST = self.sess.query(Customer)
        PROD = self.sess.query(Product)
        ORDERS = self.sess.query(Order)
        LINES = self.sess.query(OrderLine)
        c = CUST.appendRow(name="Henri")
        p = PROD.appendRow(name="Pizza Margerita",price=599)
        self.assertEqual(c.id,4)
        self.assertEqual(p.id,3)
        #self.db.flush()
        c = CUST.peek(4)
        self.assertEqual(c.id,4)
        p = PROD.peek(3)
        self.assertEqual(p.id,3)
        ORDERS.startDump()
        o = ORDERS.appendRow(date=itod(20040322),customer = c)
        #SELECT MAX(id) FROM ORDERS;
        self.assertEquivalent(ORDERS.stopDump(),"""\
INSERT INTO Orders ( id, xdate, customer_id, totalPrice, isRegistered )
            VALUES ( 5, 731662, 4, NULL, NULL );
""")
        
        LINES.startDump()
        q = o.lines()
        q.appendRow(product=p,qty=2)
        s=LINES.stopDump()
        #print s
        # SELECT MAX(id) FROM LINES;
        #SELECT id, date, customer_id, totalPrice, isRegistered
        #FROM Orders
        #WHERE id = 5;
        
        self.assertEquivalent(s,"""\
INSERT INTO OrderLines (
id, order_id, productProducts_id, productServices_id, qty )
VALUES ( 8, 5, 3, NULL, 2 );
""")
        q = LINES.query(order=ORDERS.peek(1))
        self.assertEqual(len(q),1)
        for line in q:
            self.assertEqual(line.order.id,1)
        #self.db.flush()

        
        PROD.startDump()
        prod = PROD.peek(1)
        #self.assertEqual(len(PROD._cachedRows.keys()),1)
        #self.assertEqual(PROD._cachedRows.keys()[0],(1,))
        self.assertEqual(prod.name,"Pizza Margerita")
        self.assertEquivalent(PROD.stopDump(),"""\
SELECT id, name, price FROM Products WHERE id = 1;
""")
        #self.db.flush()
        #self.assertEqual(len(PROD._cachedRows.keys()),0)

        
        
        LINES.startDump()
        line = LINES.peek(1)
        #self.assertEquivalent(self.db.conn.stopDump(),"")
        self.assertEquivalent(LINES.stopDump(),"""\
SELECT id, order_id, productProducts_id, productServices_id, qty FROM OrderLines WHERE id = 1;        
""")

        PROD.startDump()
        self.assertEqual(line.product.name,"Pizza Margerita")
        #print self.db.conn.stopDump()
        self.assertEquivalent(PROD.stopDump(),"""\
SELECT id, name, price FROM Products WHERE id = 1;
""")
        #self.db.flush()

        
        

    def test03(self):
        SERV = self.sess.query(Service)
        CUST = self.sess.query(Customer)
        PROD = self.sess.query(Product)
        ORDERS = self.sess.query(Order)
        LINES = self.sess.query(OrderLine)
        q = LINES.query("product.name")
        self.assertEquivalent(q.getSqlSelect(), """
        SELECT
            lead.id,
            lead.productProducts_id,
            productProducts.id,
            lead.productServices_id,
            productServices.id,
            productProducts.name,
            productServices.name
        FROM OrderLines AS lead
            LEFT JOIN Products AS productProducts
                  ON (lead.productProducts_id = productProducts.id)
            LEFT JOIN Services AS productServices
                  ON (lead.productServices_id = productServices.id)
        """)

    def test04(self):
        SERV = self.sess.query(Service)
        CUST = self.sess.query(Customer)
        PROD = self.sess.query(Product)
        ORDERS = self.sess.query(Order)
        LINES = self.sess.query(OrderLine)
        #db = self.db
        pizzeria.populate(self.sess)
        
        s1 = SERV.appendRow(name="bring home",price=1)
        s2 = SERV.appendRow(name="organize party",price=100)
        c3 = CUST.appendRow(name="Bernard")

        p1 = PROD.peek(1)
        p2 = PROD.peek(2)

        o1 = ORDERS.appendRow(customer=c3,date=itod(20040318))
        q = o1.lines()
        q.appendRow(product=s1,qty=1)
        q.appendRow(product=p1,qty=1)

        o2 = ORDERS.appendRow(customer=CUST[1],
                              date=itod(20040319))
        q = o2.lines()
        q.appendRow(product=p1,qty=2)
        q.appendRow(product=p2,qty=3)
        #LINES.appendRow(order=o1,product=s2,qty=1)

        #db.commit()

        q = o1.lines("product qty")
        
        totalPrice = 0
        for line in q:
            #print line.product.name, line.qty
            totalPrice += (line.qty * line.product.price)
            
        o1.register()
        o2.register()

        self.sess.commit()

        
        
    def test05(self):
        return
        SERV = self.sess.query(Service)
        CUST = self.sess.query(Customer)
        PROD = self.sess.query(Product)
        ORDERS = self.sess.query(Order)
        LINES = self.sess.query(OrderLine)
        services.populate(self.sess)
        q = LINES.query("order.date order.customer.name",
                             product=PROD[1])
        self.assertEquivalent(q.getSqlSelect(), """
        SELECT
          lead.id, lead.order_id, xorder.id, xorder.customer_id,
          xorder_customer.id,
          lead.productProducts_id,
          lead.productServices_id,
          xorder.xdate,
          xorder_customer.name
        FROM OrderLines AS lead
          LEFT JOIN Orders AS xorder
            ON (lead.order_id = xorder.id)
          LEFT JOIN Customers AS xorder_customer
            ON (xorder.customer_id = xorder_customer.id)
        WHERE AND product_id ISNULL
                AND productProducts_id = 1""")

        

if __name__ == '__main__':
    main()

