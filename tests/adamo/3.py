# coding: latin1

"""
Logical columns (row attributes) versus physical columns (atoms)

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

	def test02(self):
		""
		q = PRODUCTS.query("name price", orderBy="name")
		l = []
		for prod in q:
			l.append("a %s costs %s." % (prod.name,str(prod.price)))
		s = " ".join(l)
		self.assertEqual(s,"a Chair costs 12. a Table costs 56.")
			

		
		
	def test03(self):
		"2 successive appendRow() without specifying id"
		pot = AUTHORS.appendRow(firstName="Harry",name="Potter")
		bel = AUTHORS.appendRow(firstName="Harry",name="Bellafonte")
		self.assertEqual(pot.id, bel.id-1)
		

	
## if __name__ == "__main__":
##		print __file__
##		from lino.misc import tsttools
##		tsttools.run(__file__[:-3]) 
	

if __name__ == '__main__':
	import unittest
	unittest.main()

