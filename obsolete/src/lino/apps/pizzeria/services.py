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

from lino.adamo.ddl import *
from lino.adamo.datatypes import itod
from lino.apps.pizzeria import pizzeria
#from lino.apps.pizzeria.pizzeria import Orders, Products, OrderLines, Customers

class Service(pizzeria.Product):
    tableName="Services"
    def initTable(self,table):
        pizzeria.Product.initTable(self,table)
        table.addField('responsible',STRING)

class ServicesReport(DataReport):
    leadTable=Service



        
class MyPizzeriaSchema(pizzeria.PizzeriaSchema):
    
    tableClasses = (pizzeria.Product,
                    Service,
                    pizzeria.Customer,
                    pizzeria.Order, pizzeria.OrderLine)


class MyPizzeriaMain(pizzeria.PizzeriaMain):
    
    schemaClass=MyPizzeriaSchema
    
    """
    
Welcome to MyPizzeria, a customization of the most simple Lino demo
application.  Note that this application is for demonstration purposes
only.

"""

    def setupMenu(self):
        m = self.addMenu("my","&My Pizzeria")
        self.addReportItem(
            m,"services",ServicesReport,label="&Services")
        pizzeria.PizzeriaMain.setupMenu(self)

class MyPizzeria(pizzeria.Pizzeria):
    name="My Pizzeria"
    mainFormClass=MyPizzeriaMain
    



def populate(dbc):
    
    pizzeria.populate(dbc)
    
    SERV = dbc.query(Service)
    CUST = dbc.query(pizzeria.Customer)
    ORDERS = dbc.query(pizzeria.Order)
    PROD = dbc.query(pizzeria.Product)
    
    s1 = SERV.appendRow(name="bring home",price=1)
    s2 = SERV.appendRow(name="organize party",price=100)
    c3 = CUST.appendRow(name="Bernard")

    o1 = ORDERS.appendRow(customer=c3,date=itod(20040318))
    q = o1.lines()
    q.appendRow(product=PROD.peek(1),qty=1)
    q.appendRow(product=s1,qty=1)
    
    o2 = ORDERS.appendRow(customer=CUST.peek(1),date=itod(20040319))
    q = o2.lines()
    q.appendRow(product=PROD.peek(1),qty=2)
    q.appendRow(product=PROD.peek(2),qty=3)

    o1.register()
    o2.register()


