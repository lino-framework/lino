#coding: latin1
#----------------------------------------------------------------------
# $Id: pizzeria2.py,v 1.6 2004/06/18 12:23:57 lsaffre Exp $
# Copyright: (c) 2003-2004 Luc Saffre
# License:	 GPL
#----------------------------------------------------------------------

from pizzeria import Products, populate, Pizzeria
from lino.adamo import *
#from lino.adamo.schema import quickdb

class ServicesPlugin(SchemaPlugin):
	def defineTables(self,schema,ui):
		schema.addTable(Services("SERV"))

		

class Services(Products):
	
	def init(self):
		Products.init(self)
		self.responsible = Field(STRING)



def Pizzeria2():
	schema = Pizzeria()
	schema.addPlugin(ServicesPlugin())
	return schema
		
def populate2(sess):
	populate(sess)
	sess.installto(globals())
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

	sess.commit()

	o1.register()
	o2.register()

	sess.commit()


def query(sess):	
	# make table names global variables
	sess.installto(globals())
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

def query2(sess):
	sess.installto(globals())
	from lino.adamo.plain import PlainRenderer
	r = PlainRenderer(None,sess)
	rpt = LINES.report("ordr.date ordr.customer.name",
							 product=PROD.peek(1))
	print r.renderReport(None,rpt)
	#print q.report()


	

def main():

	db = quickdb(schema=Pizzeria2(),
					 isTemporary=True,
					 label="Lucs Pizza Restaurant")
	db.createTables()
	sess = db.beginSession()
	populate2(sess)
	query(sess)
	sess.shutdown()
	
if __name__ == "__main__":
	main()
