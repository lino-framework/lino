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
This is a short example to illustrate Adamo's basic idea.

"""

from lino.adamo.ddl import *
from lino.adamo.datatypes import itod


# 1. Define the database schema

class Product(StoredDataRow):
    tableName="Products"
    def initTable(self,table):
        table.addField('name',STRING)
        table.addField('price',PRICE)

class Customer(StoredDataRow):
    tableName="Customers"
    def initTable(self,table):
        table.addField('name',STRING)
        table.addField('street',STRING)
        table.addField('city',STRING)
        
    def getLabel(self):
        return self.name

     
class Order(StoredDataRow):
    tableName="Orders"
    def initTable(self,table):
        table.addField('date',DATE)
        table.addPointer('customer',Customer)
        table.addField('totalPrice',PRICE)
        table.addField('isRegistered',BOOL)
        table.addDetail('lines',OrderLine,'order')

##     def lines(self,*args,**kw):
##         kw['order']=self
##         return self.detail(OrderLine,*args,**kw)
        
    def register(self):
        """
        compute totalPrice and set isRegistered to True to prevent
        further editing."""
        self.lock()
        totalPrice = 0
        for line in self.lines():
            #print line
            assert line.order.id == self.id
            assert line.product.price is not None, \
                   "%r : price is None!" % (line.product)
            totalPrice += (line.qty * line.product.price)
        self.totalPrice = totalPrice
        self.isRegistered = True
        self.unlock()
      
     
class OrderLine(StoredDataRow):
    tableName="OrderLines"
    def initTable(self,table):
        table.addPointer('order',Order,detailName='lines')
        #table.order.setDetail('lines')
        table.addPointer('product',Product)
        table.addField('qty',INT)
        
    def validate(self):
        if self.order is None:
            return "order is mandatory"
        if self.product is None:
            return "product is mandatory"



class ProductsReport(DataReport):
    leadTable=Product


class CustomersReport(DataReport):
    leadTable=Customer

class OrdersReport(DataReport):
    leadTable=Order


class PizzeriaSchema(Schema):
    
    tableClasses = (Product, Customer, Order, OrderLine)


class PizzeriaMain(DbMainForm):
    
    schemaClass=PizzeriaSchema
    
    """
    
Welcome to Pizzeria, the most simple Lino demo application.
Note that this application is not meant to be used for anything
else than learning.

"""

    def setupMenu(self):
        m = self.addMenu("pizzeria","&Pizzeria")
        self.addReportItem(
            m,"products",ProductsReport,label="&Products")
        self.addReportItem(
            m,"customers",CustomersReport,label="&Customers")
        self.addReportItem(
            m,"orders",OrdersReport,label="&Orders")
        self.addProgramMenu()


class Pizzeria(DbApplication):
    name="Lino Pizzeria"
    mainFormClass=PizzeriaMain

##     def setupSchema(self):
##         for cl in Product, Customer, Order, OrderLine:
##             self.addTable(cl)


        
def populate(dbc):
    """
    Create some data and play with it
    """

    CUST = dbc.query(Customer)
    PROD = dbc.query(Product)
    ORDERS = dbc.query(Order)
    LINES = dbc.query(OrderLine)
    
    c1 = CUST.appendRow(name="Henri")
    c2 = CUST.appendRow(name="James")

    p1 = PROD.appendRow(name="Pizza Margerita",price=6)
    assert p1.price == 6
    p2 = PROD.appendRow(name="Pizza Marinara",price=7)

    o1 = ORDERS.appendRow(customer=c1,
                          date=itod(20030816))
    l1=LINES.appendRow(order=o1,product=p1,qty=2)
    assert l1.product.price == 6


    o2 = ORDERS.appendRow(customer=c2,date=itod(20030816))
    LINES.appendRow(order=o2,product=p1,qty=3)
    LINES.appendRow(order=o2,product=p2,qty=5)

    p=PROD.peek(1)
    assert p.price == 6
    
    o1.register()
    o2.register()
    

def query(sess):
    """
    Create some data and play with it
    """
    
    ORDERS = sess.query(Order)
##  q = ORDERS.query("customer totalPrice")
##  for (customer,totalPrice) in q:
##      print "%s must pay %d EUR" % (customer.name,totalPrice)
    for o in ORDERS.query("customer totalPrice"):
        print "%s must pay %d EUR" % (o.customer.name, o.totalPrice)

def main():

    app = Pizzeria() #label="Luc's Pizza Restaurant")

    sess = schema.quickStartup()
    
    populate(sess)

    query(sess)

    sess.shutdown()
    
if __name__ == "__main__":
    main()
