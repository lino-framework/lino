#coding: latin1
	
import unittest
from lino.schemas.sprl import demo


class Case(unittest.TestCase):
	"""
	Filters (not finished)
	"""

	def setUp(self):
		
		self.db = demo.getDemoDB()
		self.db.installto(globals()) 

	def tearDown(self):
		self.db.shutdown()

	def test01(self):
		"Simple query with a filter"
		q = AUTHORS.query("firstName name",
								 orderBy='name')
		q.setSqlFilters('name LIKE "B%"')
		s = "\n".join([row.getLabel() for row in q])
		self.assertEqual(s,"""\
Donald Bisset
Georges Brassens
Jacques Brel""")

	def test02(self):
		"Finding Georges Brassens"
		p = AUTHORS.findone(firstName="Georges",
								  name="Brassens")
		# self.assertNotEqual(p,None)
		self.assertEqual(p.name,"Brassens")
		self.assertEqual(p.firstName,"Georges")
		
		

if __name__ == '__main__':
	unittest.main()

