# coding: latin1

"""
forms
"""
import types

from lino.misc.tsttools import TestCase
from lino.schemas.sprl import demo

class Case(TestCase):
	"""

	"""

	def setUp(self):
		self.sess = demo.beginSession()

	def tearDown(self):
		self.sess.shutdown()


	def test01(self):
		self.sess.startDump(verbose=True)
		frm = self.sess.forms.login
		self.assertEqual(frm.getFormName(),"login")
		self.assertEqual(frm.password,None)
		self.assertEqual(frm.uid,None)
		frm.uid = "luc"
		frm.ok()
		usr = self.sess.getUser()
		self.assertEqual(usr.getLabel(),"Luc Saffre")
		self.assertEqual(usr.password,None)
		s = self.sess.stopDump()
		self.assertEquivalent(s,"Hello, Luc Saffre")
		
if __name__ == '__main__':
	from unittest import main
	main()

