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
This is a short example to illustrate Adamo's basic idea.

"""

from lino.adamo.ddl import *
from lino.adamo.datatypes import itod


# 1. Define the database schema

class Products(Table):
    def init(self):
        self.addField('name',STRING)
        self.addField('price',PRICE)

class Customers(Table):
    def init(self):
        self.addField('name',STRING)
        self.addField('street',STRING)
        self.addField('city',STRING)
        
    class Instance(Table.Instance):
        def __str__(self):
            return self.name

     
class Orders(Table):
    def init(self):
        self.addField('date',DATE)
        self.addPointer('customer',Customers)
        self.addField('totalPrice',PRICE)
        self.addField('isRegistered',BOOL)
        
    class Instance(Table.Instance):
        def register(self):
            self.lock()
            totalPrice = 0
            for line in self.lines:
                #print line
                assert line.ordr.id == self.id
                totalPrice += (line.qty * line.product.price)
            self.totalPrice = totalPrice
            self.isRegistered = True
            self.unlock()
      
     
class OrderLines(Table):
    def init(self):
        self.addPointer('ordr',Orders,detailName='lines')
        #self.ordr.setDetail('lines')
        self.addPointer('product',Products)
        self.addField('qty',INT)
        
    class Instance(Table.Instance):
        def validate(self):
            if self.ordr is None:
                return "order is mandatory"
            if self.product is None:
                return "product is mandatory"


class Pizzeria(Schema):
    tables=Products, Customers, Orders, OrderLines


        
def populate(sess):
    """
    Create some data and play with it
    """

    CUST = sess.query(Customers)
    PROD = sess.query(Products)
    ORDERS = sess.query(Orders)
    LINES = sess.query(OrderLines)
    
    c1 = CUST.appendRow(name="Henri")
    c2 = CUST.appendRow(name="James")

    p1 = PROD.appendRow(name="Pizza Margerita",price=6)
    p2 = PROD.appendRow(name="Pizza Marinara",price=7)

    o1 = ORDERS.appendRow(customer=c1,
                          date=itod(20030816))
    LINES.appendRow(ordr=o1,product=p1,qty=2)


    o2 = ORDERS.appendRow(customer=c2,date=itod(20030816))
    LINES.appendRow(ordr=o2,product=p1,qty=3)
    LINES.appendRow(ordr=o2,product=p2,qty=5)

    o1.register()
    o2.register()
    

def query(sess):
    """
    Create some data and play with it
    """
    
    ORDERS = sess.query(Orders)
##  q = ORDERS.query("customer totalPrice")
##  for (customer,totalPrice) in q:
##      print "%s must pay %d EUR" % (customer.name,totalPrice)
    for o in ORDERS.query("customer totalPrice"):
        print "%s must pay %d EUR" % (o.customer.name, o.totalPrice)

def main():

    app = Pizzeria() #label="Luc's Pizza Restaurant")

    sess = schema.quickStartup()
    #print sess.ui
    #raw_input("ok")
    
    populate(sess)

    query(sess)

    sess.shutdown()
    
if __name__ == "__main__":
##     from lino.ui import console
##     console.parse_args()
    main()
