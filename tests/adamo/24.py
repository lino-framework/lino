# coding: latin1

"""
bug 20040724 : setting a sample on a query modifies the 

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
		q = CITIES.query()
		l = len(q)
		
		be = NATIONS.peek('be')
		q = CITIES.query(nation=be)
		
		q = CITIES.query()
		self.assertEqual(l,len(q))
		

if __name__ == '__main__':
	import unittest
	unittest.main()

