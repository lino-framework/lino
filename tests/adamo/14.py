# coding: latin1
import unittest
from lino.schemas.sprl import demo
#from lino.adamo.schema import quickdb
#from mx.DateTime import Date
from lino.tools.normalDate import ND

class Case(unittest.TestCase):
	def setUp(self):
		#self.db = quickdb()
		self.db = demo.getDemoDB(populator=None)
		self.db.installto(globals())
		
	def tearDown(self):
		self.db.shutdown()
		
	def test01(self):
		d = ND(20040413)
		for i in range(100):
			EVENTS.appendRow(date=d,
								  title="Event # %d" % i)
			d += 1
		#self.db.commit()

		e = EVENTS.findone(date=ND(20040501))
		self.assertEqual(e.id,19)
		self.assertEqual(e.title,'Event # 18')
		#print e

		
if __name__ == '__main__':
	unittest.main()

