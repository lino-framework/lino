# coding: latin1
"""

bug 20040914: tables LANGS and NATIONS of demo db seemed empty (theyr
len() was 0) because Datasource.rowcount (which is a cached value) was
not re-read from database when some other Datasource on same store did
an appendRow().

"""

import unittest

from lino.schemas.sprl import demo

class Case(unittest.TestCase):

	def setUp(self):
		
		self.sess = demo.beginSession()

	def tearDown(self):
		self.sess.shutdown()


	def test01(self):
		#for lang in self.sess.tables.LANGS:
		#	print lang
		self.assertEqual(len(self.sess.tables.LANGS),5)
		

if __name__ == '__main__':
	unittest.main()
