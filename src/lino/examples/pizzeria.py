#coding: latin1
#----------------------------------------------------------------------
# $Id: pizzeria.py,v 1.10 2004/06/12 03:06:51 lsaffre Exp $
# Copyright: (c) 2003-2004 Luc Saffre
# License:	 GPL
#----------------------------------------------------------------------

"""
This is a short example to illustrate Adamo's basic idea.

"""

from lino.adamo import *

from forum.normalDate import ND

# 1. Define the database schema


#from lino.adamo.schema import DatabaseSchema, quickdb

class Products(Table):
	def init(self):
		self.name = Field(STRING)
		self.price = Field(PRICE)

class Customers(Table):
	def init(self):
		self.name = Field(STRING)
		self.street = Field(STRING)
		self.city = Field(STRING)

	 
class Orders(Table):
	def init(self):
		self.date = Field(DATE)
		self.customer = Pointer(Customers)
		self.totalPrice = Field(PRICE)
		self.isRegistered = Field(BOOL)
		
	class Row(Table.Row):
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
		self.ordr = Pointer(Orders)
		self.product = Pointer(Products)
		self.qty = Field(INT)
		self.ordr.setDetail('lines')
		
	class Row(Table.Row):
		def validate(self):
			if self.ordr is None:
				return "order is mandatory"
			if self.product is None:
				return "product is mandatory"


class BasePlugin(SchemaPlugin):
	def defineTables(self,schema,ui):
		schema.addTable( Products("PROD"))
		schema.addTable(Customers("CUST"))
		schema.addTable(Orders("ORDERS"))
		schema.addTable(OrderLines("LINES"))
		
def Pizzeria():
	schema = Schema()
	schema.addPlugin(BasePlugin())
	return schema

		
		
def populate(sess):
	"""
	Create some data and play with it
	"""
	sess.installto(globals())
	
	c1 = CUST.appendRow(name="Henri")
	c2 = CUST.appendRow(name="James")

	p1 = PROD.appendRow(name="Pizza Margerita",price=6)
	p2 = PROD.appendRow(name="Pizza Marinara",price=7)

	o1 = ORDERS.appendRow(customer=c1,
								 date=ND(20030816))
	LINES.appendRow(ordr=o1,product=p1,qty=2)


	o2 = ORDERS.appendRow(customer=c2,date=ND(20030816))
	LINES.appendRow(ordr=o2,product=p1,qty=3)
	LINES.appendRow(ordr=o2,product=p2,qty=5)

	sess.commit()

	o1.register()
	o2.register()

	sess.commit()
	

def query(sess):
	"""
	Create some data and play with it
	"""
	sess.installto(globals())
	
## 	q = ORDERS.query("customer totalPrice")
## 	for (customer,totalPrice) in q:
## 		print "%s must pay %d EUR" % (customer.name,totalPrice)
	for o in ORDERS.query("customer totalPrice"):
		print "%s must pay %d EUR" % (o.customer.name,
												o.totalPrice)

def main():

	db = quickdb(schema=Pizzeria(),
					 isTemporary=True,
					 label="Lucs Pizza Restaurant")

	# create empty tables
	db.createTables()
	
	sess = ConsoleSession(db=db)
	#sess.beginContext(db.beginContext())

	# play around
	populate(sess)
	sess.commit()
	
	query(sess)

	# commit changes and release the database file
	sess.shutdown()
	
if __name__ == "__main__":
	main()
