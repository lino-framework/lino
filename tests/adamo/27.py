# coding: latin1

"""
forms
"""
import types

from lino.misc.tsttools import TestCase
from lino.schemas.sprl import demo
from lino.adamo import DataVeto

class Case(TestCase):
	"""

	"""

	def setUp(self):
		self.sess = demo.beginSession()

	def tearDown(self):
		self.sess.shutdown()


	def test01(self):
		self.sess.startDump(verbosity=1)
		frm = self.sess.openForm('login')
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
		
		frm.password = "random password"
		try:
			frm.ok()
			self.fail("failed to complain about wrong password for luc")
		except DataVeto,e:
			self.assertEqual(str(e),"invalid password for Luc Saffre")

		try:
			frm.uid = "!luc"
			self.fail("failed to complain about invalid username")
		except DataVeto,e:
			self.assertEqual(str(e),"!luc : invalid username")
			
		frm.uid = "foo"
		try:
			frm.ok()
			self.fail("failed to complain about non-existing user")
		except DataVeto,e:
			self.assertEqual(str(e),"foo : no such user")

		
if __name__ == '__main__':
	from unittest import main
	main()

