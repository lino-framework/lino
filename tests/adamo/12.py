#coding: latin1
   
from lino.misc.tsttools import TestCase
from lino.examples import pizzeria2


class Case(TestCase):
	"""
	(this failed on 20040322)
	"""

	def setUp(self):
		self.sess = pizzeria2.beginSession()
		self.sess.installto(globals())

	def tearDown(self):
		self.sess.shutdown()

	def test01(self):
		c = CUST.appendRow(name="Mark")
		newID = c.id
		c = CUST.peek(newID)
		self.assertEqual(c.id,newID) # failed
		
if __name__ == '__main__':
	from unittest import main
	main()

