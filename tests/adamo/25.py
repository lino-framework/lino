# coding: latin1

"""
new function Datasource.setCsvSamples()

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
		q = CITIES.query(nation=be)
		l = len(q)
		
		q = CITIES.query()
		q.setCsvSamples(nation='be')
		
		self.assertEqual(l,len(q))
		
	def test02(self):
		jnl = JOURNALS.peek('OUT')
		inv = INVOICES.peek(jnl,1)
		self.assertEqual(str(inv.partner),"Anton Ausdemwald")
		self.assertEqual(len(inv.lines),2)

		q = INVOICELINES.query(invoice=inv)
		l = len(q)
		
		q = INVOICELINES.query()
		q.setCsvSamples(invoice="OUT,1")
		
		self.assertEqual(l,len(q))
		

if __name__ == '__main__':
	import unittest
	unittest.main()

