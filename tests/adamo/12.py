#coding: latin1
   
from lino.adamo import quickdb
from lino.misc.tsttools import TestCase
from lino.examples import pizzeria2


class Case(TestCase):
	"""
	(this failed on 20040322)
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
		c = CUST.appendRow(name="Henri")
		self.assertEqual(c.id,1) # ok
		
		#self.db.flush()
		
		c = CUST.peek(1)
		self.assertEqual(c.id,1) # failed
		
if __name__ == '__main__':
	from unittest import main
	main()

