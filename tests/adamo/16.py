# coding: latin1
"""
"""
import unittest
from lino.schemas.sprl import demo
from lino.adamo.datatypes import DataVeto

class Case(unittest.TestCase):
	def setUp(self):
		self.db = demo.getDemoDB()
		self.db.installto(globals())
		
	def tearDown(self):
		self.db.shutdown()
		
	def test01(self):
		de = LANGS.peek('de')
		#print LANGS._table.getAttrList()
		for p in de.pages_by_lang:
			self.assertEqual(p.title,'Bullshit Bingo')
			
		#print len(de.listof_PAGES)
		#print de.listof_PAGES[0]

		msg = de.vetoDelete()
		self.assertEqual(msg,"German : quotes_by_lang not empty")
		
		et = LANGS.peek('et')
		self.assertEqual(et.vetoDelete(),None)
		
	def test02(self):
		xx = LANGS.peek('xx')
		self.assertEqual(xx,None)
		
## 		try:
## 			xx = LANGS.peek('xx')
##  			self.fail('failed to raise exception')
##  		except DataVeto,e:
##  			pass

		
		self.assertEqual(len(LANGS),5)
		xx = LANGS.appendRow(id='xx')
		self.assertEqual(xx.id,'xx')
		xx.lock()
		xx.name='Xytoxolian'
		xx.unlock()
		self.assertEqual(len(LANGS),6)

		
if __name__ == '__main__':
	unittest.main()

