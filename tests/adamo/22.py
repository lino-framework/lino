# coding: latin1
#----------------------------------------------------------------------
# ID:        $Id: 22.py,v 1.1 2004/06/18 12:25:31 lsaffre Exp $
# Copyright: (c) 2003-2004 Luc Saffre
# License:	 GPL
#----------------------------------------------------------------------


import unittest

from lino.schemas.sprl import demo

class Case(unittest.TestCase):
	"Does the big demo database startup()"

	def setUp(self):
		self.db = demo.getDemoDB(langs="en fr",
										 populator=None)
		self.db.installto(globals())

	def tearDown(self):
		self.db.shutdown()


	def test01(self):
		demo.populate(self.db,big=True)
		self.assertEqual(NATIONS.peek('ee').area,45226)
		self.assertEqual(NATIONS.peek('be').area,30510)
		self.assertEqual(NATIONS.peek('ee').population,1408556)
		self.assertEqual(NATIONS.peek('be').population,10289088)

if __name__ == '__main__':
	unittest.main()

