# coding: latin1

"""
testing Datasource.apply_GET()

"""
import types

from lino.misc.tsttools import TestCase
from lino.schemas.sprl import demo

class Case(TestCase):

	def setUp(self):
		
		self.db = demo.getDemoDB()
		self.db.installto(globals()) 

	def tearDown(self):
		self.db.shutdown()


	def test01(self):
		be = NATIONS.peek('be')
		
		# method 1
		q = CITIES.query(nation=be)
		l = len(q)
		
		# method 2
		q = CITIES.query()
		q.apply_GET(nation=('be',))
		self.assertEqual(l,len(q))

		# method 3
		q = be.cities.query()
		self.assertEqual(l,len(q))
		
	def test02(self):
		jnl = JOURNALS.peek('OUT')
		inv = INVOICES.peek(jnl,1)
		self.assertEqual(str(inv.partner),"Anton Ausdemwald")
		self.assertEqual(len(inv.lines),2)

		q = INVOICELINES.query(invoice=inv)
		l = len(q)
		
		q = INVOICELINES.query()
		q.apply_GET(invoice=("OUT,1",))
		
		self.assertEqual(l,len(q))
		

if __name__ == '__main__':
	import unittest
	unittest.main()

