#coding: latin1
   
from lino.adamo import quickdb
from lino.misc.tsttools import TestCase
from lino.examples import pizzeria2


class Case(TestCase):
	"""
	(this failed on 20040322)
	"""

	def setUp(self):
		self.db = quickdb(schema=pizzeria2.Pizzeria2(),
								isTemporary=True,
								label="Lucs Pizza Restaurant")
		self.db.createTables()
		self.db.installto(globals())

	def tearDown(self):
		self.db.shutdown()

	def test01(self):
		c = CUST.appendRow(name="Henri")
		self.assertEqual(c.id,1) # ok
		
		#self.db.flush()
		
		c = CUST.peek(1)
		self.assertEqual(c.id,1) # failed
		
if __name__ == '__main__':
	from unittest import main
	main()

