# coding: latin1
"""

- new trigger accept_xx()
- "row is not locked"

"""

import unittest

from lino.schemas.sprl import demo
from lino.adamo import DataVeto, InvalidRequestError

class Case(unittest.TestCase):

	def setUp(self):
		
		self.sess = demo.beginSession()

	def tearDown(self):
		self.sess.shutdown()


	def test01(self):
		NATIONS = self.sess.tables.NATIONS
		try:
			NATIONS.appendRow(id="foo",name="Fooland")
			self.fail("expected DataVeto")
		except DataVeto,e:
			self.assertEqual(str(e),"Nation.id must be 2 chars")


		be = NATIONS.peek('be')
		try:
			be.name = "België"
			self.fail("expected DataVeto")
		except InvalidRequestError,e:
			self.assertEqual(str(e),"row is not locked")
		
			

if __name__ == '__main__':
	unittest.main()
