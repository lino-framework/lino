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

from pizzeria import Customers, Orders, OrderLines, Products, \
     populate, Pizzeria
from lino.adamo import *
from lino.adamo.datatypes import itod
from lino import adamo

class Services(Products):
    
    def init(self):
        Products.init(self)
        self.addField('responsible',STRING)
        

def populate2(sess):
    
    populate(sess)
    
    SERV = sess.query(Services)
    CUST = sess.query(Customers)
    ORDERS = sess.query(Orders)
    PROD = sess.query(Products)
    
    s1 = SERV.appendRow(name="bring home",price=1)
    s2 = SERV.appendRow(name="organize party",price=100)
    c3 = CUST.appendRow(name="Bernard")

    o1 = ORDERS.appendRow(customer=c3,date=itod(20040318))
    q = o1.lines 
    q.appendRow(product=PROD.peek(1),qty=1)
    q.appendRow(product=s1,qty=1)
    
    o2 = ORDERS.appendRow(customer=CUST.peek(1),date=itod(20040319))
    q = o2.lines 
    q.appendRow(product=PROD.peek(1),qty=2)
    q.appendRow(product=PROD.peek(2),qty=3)

    o1.register()
    o2.register()



def do_report(sess):
    ORDERS = sess.query(Orders)
    o = ORDERS.peek(3)
    print "Order #:", o.id
    print "Date:", o.date
    print "Customer:", o.customer.name
    print "-" * 40
    for line in o.lines:
        print "%-20s %3d %5d" % (line.product.name,
                                 line.qty,
                                 line.product.price*line.qty)
    print "-" * 40
    print "Total: ", o.totalPrice


def beginSession():

    schema = Pizzeria(label="Lucs second Pizza Restaurant")
    schema.addTable(Services)
    
    sess = schema.quickStartup()
    
    populate2(sess)
    
    return sess
    
def main():
    sess = beginSession()
    do_report(sess)
    sess.shutdown()
    
if __name__ == "__main__":
    main()
