# coding: latin1

"""
Logical columns (row attributes) versus physical columns (atoms)

"""
import types

from lino.misc.tsttools import TestCase
from lino.schemas.sprl import demo

class Case(TestCase):
	"""

	"""

	def setUp(self):
		self.sess = demo.getDemoDB()

	def tearDown(self):
		self.sess.shutdown()


	def test01(self):
		frm = self.sess.openForm("login")
		self.assertEqual(frm.password,None)
		self.assertEqual(frm.uid,None)
		frm.uid = "luc"
		frm.onSubmit()
		#self.assertEqual(sess.getUser(),)
		usr = self.sess.getUser()
		self.assertEqual(usr.getLabel(),"Luc Saffre")
		self.assertEqual(usr.password,None)
		
if __name__ == '__main__':
	from unittest import main
	main()

