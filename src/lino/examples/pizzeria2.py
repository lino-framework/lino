#coding: latin1
#----------------------------------------------------------------------
# $Id: pizzeria2.py,v 1.6 2004/06/18 12:23:57 lsaffre Exp $
# Copyright: (c) 2003-2004 Luc Saffre
# License:	 GPL
#----------------------------------------------------------------------

from  pizzeria import Pizzeria, Products, populate
from lino.adamo import *
#from lino.adamo.schema import quickdb

class Pizzeria2(Pizzeria):
	def defineTables(self,ui):
		Pizzeria.defineTables(self,ui)
		self.addTable(Services("SERV"))

		

class Services(Products):
	
	def init(self):
		Products.init(self)
		self.responsible = Field(STRING)

	 
		
def populate2(db):
	populate(db)
	db.installto(globals())
	s1 = SERV.appendRow(name="bring home",price=1)
	s2 = SERV.appendRow(name="organize party",price=100)
	c3 = CUST.appendRow(name="Bernard")

	o1 = ORDERS.appendRow(customer=c3,date="20040318")
	q = o1.lines #.query()
	q.appendRow(product=PROD.peek(1),qty=1)
	q.appendRow(product=s1,qty=1)
	
	o2 = ORDERS.appendRow(customer=CUST.peek(1),date="20040319")
	q = o2.lines #.query()
	q.appendRow(product=PROD.peek(1),qty=2)
	q.appendRow(product=PROD.peek(2),qty=3)
	#LINES.appendRow(order=o1,product=s2,qty=1)

	db.commit()

	o1.register()
	o2.register()

	db.commit()


def query(db):	
	# make table names global variables
	db.installto(globals())
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

def query2(db):	
	db.installto(globals())
	from lino.adamo.plain import PlainRenderer
	r = PlainRenderer(None,db)
	rpt = LINES.report("ordr.date ordr.customer.name",
							 product=PROD.peek(1))
	print r.renderReport(None,rpt)
	#print q.report()


	

def main():

	db = quickdb(schema=Pizzeria2(),
					 isTemporary=True,
					 label="Lucs Pizza Restaurant")
	db.createTables()
	populate2(db)
	query(db)
	db.shutdown()
	
if __name__ == "__main__":
	main()
