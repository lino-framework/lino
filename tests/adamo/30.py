# coding: latin1
"""

- testing ConsoleSession.report()

"""

from lino.misc.tsttools import main, TestCase
#import unittest

from lino.schemas.sprl import demo
from lino.adamo import DataVeto, InvalidRequestError

class Case(TestCase):

	def setUp(self):
		self.sess = demo.beginSession()

	def tearDown(self):
		self.sess.shutdown()


	def test01(self):
		"report with a Pointer"
		rpt = self.sess.tables.CITIES.report("id name nation",
														 orderBy="name",
														 pageLen=10)
		# print [col.name for col in rpt._clist.visibleColumns]
		self.sess.startDump()
		self.sess.showReport(rpt)
		s = self.sess.stopDump()
		# print s
		self.assertEquivalent(s,"""\
Cities
======
id    name                                               nation
----- -------------------------------------------------- ----------
1 Aachen Germany
7 Alfter-Oedekoven Germany
3 Berlin Germany
4 Bonn Germany
2 Brugge Belgium
1 Bruxelles Belgium
9 Charleroi Belgium
6 Eschweiler Germany
3 Eupen Belgium
5 Kelmis Belgium
""")		
		
	def test02(self):
		"report with a BabelField"
		rpt = self.sess.tables.NATIONS.report("id name",
														  columnWidths="2 25")
		self.sess.startDump()
		self.sess.showReport(rpt)
		s = self.sess.stopDump()
		#print s
		self.assertEquivalent(s,"""\
Nations
=======
id name
-- -------------------------
ee Estonia
be Belgium
de Germany
fr France
us United States of America
""")

if __name__ == '__main__':
	main()
