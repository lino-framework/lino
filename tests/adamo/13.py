# coding: latin1
import types
import unittest

from lino.adamo.datatypes import DataVeto

from lino.schemas.sprl import demo

class Introduction(unittest.TestCase):

	def setUp(self):
		
		self.db = demo.beginSession()
		self.db.installto(globals()) #.update(demo.db.tables)

	def tearDown(self):
		self.db.shutdown()


	def test01(self):
		#print [a.name for a in PAGES._table.peekQuery._atoms]
		PAGES.appendRow(match="index",
							 title="Main page",
							 abstract="Welcome",
							 body="bla bla "*50)
		PAGES.appendRow(match="copyright",
							 title="Copyright",
							 abstract="Legal notes for this site.",
							 body="BLA BLA "*50)
		#PAGES.commit()
		row = PAGES.findone(match="index")

		self.assertEqual(row.title,'Main page')
		

if __name__ == '__main__':
	unittest.main()

