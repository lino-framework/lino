# coding: latin1
#----------------------------------------------------------------------
# ID:        $Id: 4.py,v 1.9 2004/07/24 04:52:37 lsaffre Exp $
# Copyright: (c) 2003-2004 Luc Saffre
# License:	 GPL
#----------------------------------------------------------------------

"""
a very short test for when I am working in adamo...
"""
import unittest

from lino.schemas.sprl import demo

class Case(unittest.TestCase):
	"Does the default demo database startup()"

	def setUp(self):
		self.db = demo.getDemoDB()
		self.db.installto(globals())

	def tearDown(self):
		self.db.shutdown()


	def test01(self):
		self.assertEqual(NATIONS.peek('ee').name, 'Estonia')
		
		try:
			NATIONS.peek(['ee'])
		except TypeError,e:
			pass
		else:
			self.fail('Failed to raise TypeError')
			
		try:
			NATIONS.peek(1)
		except TypeError,e:
			pass
		else:
			self.fail('Failed to raise TypeError')
			

if __name__ == '__main__':
	unittest.main()

