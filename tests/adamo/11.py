#coding: latin1
   
from lino.adamo import quickdb
from lino.misc.tsttools import TestCase
from lino.examples import pizzeria, pizzeria2


class Case(TestCase):
	"""
	Tests about switching pointers, using the pizzeria2 example
	"""

	def setUp(self):
		db = quickdb(schema=pizzeria2.Pizzeria2(),
								isTemporary=True,
								label="Lucs Pizza Restaurant")
		db.createTables()
		self.sess = db.beginSession()
		self.sess.installto(globals())

	def tearDown(self):
		self.sess.shutdown()

	def test01(self):
		# testing whether INSERT INTO is correctly done
		self.sess.startDump()
		s1 = SERV.appendRow(name="bring home",price=99)
		sql = self.sess.stopDump()
		self.assertEquivalent(sql,"""\
SELECT MAX(id) FROM SERV;
INSERT INTO SERV ( id, responsible, name, price )
         VALUES  ( 1,  NULL, 'bring home', 99 );
""")
		
	def test02(self):
		#pizzeria2.populate(self.db)
		c = CUST.appendRow(name="Henri")
		p = PROD.appendRow(name="Pizza Margerita",price=599)
		self.assertEqual(c.id,1)
		self.assertEqual(p.id,1)
		#self.db.flush()
		c = CUST.peek(1)
		self.assertEqual(c.id,1)
		p = PROD.peek(1)
		self.assertEqual(p.id,1)
		self.sess.startDump()
		o = ORDERS.appendRow(date="20040322",customer = c)
		self.assertEquivalent(self.sess.stopDump(),"""\
SELECT MAX(id) FROM ORDERS;
INSERT INTO ORDERS (
id,
customer_id,
date,
totalPrice,
isRegistered
) VALUES ( 1, 1,
20040322,
NULL,
NULL );
""")
		
		self.sess.startDump()
		q = o.lines.query()
		q.appendRow(product=p,qty=2)
		#print self.db.conn.stopDump()
		self.assertEquivalent(self.sess.stopDump(),"""\
SELECT MAX(id) FROM LINES;
INSERT INTO LINES (
id, productPROD_id, productSERV_id,
qty,
ordr_id
) VALUES ( 1, 1, NULL, 2, 1 );
""")
		q = LINES.query(ordr=ORDERS.peek(1))
		self.assertEqual(len(q),1)
		for line in q:
			self.assertEqual(line.ordr.id,1)
		#self.db.flush()

		
		self.sess.startDump()
		prod = PROD.peek(1)
		#self.assertEqual(len(PROD._cachedRows.keys()),1)
		#self.assertEqual(PROD._cachedRows.keys()[0],(1,))
		self.assertEqual(prod.name,"Pizza Margerita")
		self.assertEquivalent(self.sess.stopDump(),"""\
SELECT id, name, price FROM PROD WHERE id = 1;
""")
		#self.db.flush()
		#self.assertEqual(len(PROD._cachedRows.keys()),0)

		
		
		self.sess.startDump()
		line = LINES.peek(1)
		#self.assertEquivalent(self.db.conn.stopDump(),"")
		self.assertEquivalent(self.sess.stopDump(),"""\
SELECT id, productPROD_id, productSERV_id, qty, ordr_id  FROM LINES WHERE id = 1;""")

		self.sess.startDump()
		self.assertEqual(line.product.name,"Pizza Margerita")
		#print self.db.conn.stopDump()
		self.assertEquivalent(self.sess.stopDump(),"""\
SELECT id, name, price FROM PROD WHERE id = 1;
""")
		#self.db.flush()

		
		

	def test03(self):
		q = LINES.query("product.name")
		self.assertEquivalent(q.getSqlSelect(), """
		SELECT
			lead.id,
			lead.productPROD_id,
			productPROD.id,
			lead.productSERV_id,
			productSERV.id,
			productPROD.name,
			productSERV.name
		FROM LINES AS lead
			LEFT JOIN PROD AS productPROD
				  ON (lead.productPROD_id = productPROD.id)
			LEFT JOIN SERV AS productSERV
				  ON (lead.productSERV_id = productSERV.id)
		""")

	def test04(self):
		#db = self.db
		pizzeria.populate(self.sess)
		self.sess.installto(globals())
		
		s1 = SERV.appendRow(name="bring home",price=1)
		s2 = SERV.appendRow(name="organize party",price=100)
		c3 = CUST.appendRow(name="Bernard")

		p1 = PROD.peek(1)
		p2 = PROD.peek(2)

		o1 = ORDERS.appendRow(customer=c3,date="20040318")
		q = o1.lines.query()
		q.appendRow(product=s1,qty=1)
		q.appendRow(product=p1,qty=1)

		o2 = ORDERS.appendRow(customer=CUST[1],date="20040319")
		q = o2.lines.query()
		q.appendRow(product=p1,qty=2)
		q.appendRow(product=p2,qty=3)
		#LINES.appendRow(order=o1,product=s2,qty=1)

		#db.commit()

		q = o1.lines.query("product qty")
		
		totalPrice = 0
		for line in q:
			#print line.product.name, line.qty
			totalPrice += (line.qty * line.product.price)
			
		o1.register()
		o2.register()

		self.sess.commit()

		
		
	def test05(self):
		return
		pizzeria2.populate(self.db)
		q = LINES.query("ordr.date ordr.customer.name",
							 product=PROD[1])
		self.assertEquivalent(q.getSqlSelect(), """
		SELECT
		  lead.id, lead.ordr_id, ordr.id, ordr.customer_id,
		  ordr_customer.id,
		  lead.productPROD_id,
		  lead.productSERV_id,
		  ordr.date,
		  ordr_customer.name
		FROM LINES AS lead
		  LEFT JOIN ORDERS AS ordr
		    ON (lead.ordr_id = ordr.id)
		  LEFT JOIN CUST AS ordr_customer
		    ON (ordr.customer_id = ordr_customer.id)
		WHERE AND product_id ISNULL
				AND productPROD_id = 1""")

		

if __name__ == '__main__':
	from unittest import main
	main()

