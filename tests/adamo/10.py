# coding: latin1
"""

"Detail" RowAttributes reimplemented.  Details are used to "access a
Pointer from the other side".  If Table.addPointer() is called with
the "detailName" argument, then the other Table (the one where the
Pointer points to) will get a row method with that name.

For example, a NATIONS instance has a mathod cities() which returns a
pre-build query of CITIES from this nation.


"""
import unittest
from lino.schemas.sprl import demo

class Case(unittest.TestCase):
	def setUp(self):
		self.db = demo.beginSession(populator=None)
		demo.populate(self.db,big=True)
		self.db.installto(globals())
		
	def tearDown(self):
		self.db.shutdown()
		
	def test01(self):
		be = NATIONS.peek('be')
		s = ''
		for city in be.cities.query(orderBy="name",
											 search="eup"):
			s += city.zipCode + " "+ city.name + "\n"
		# print s
		self.assertEqual(s,"""\
4700 Eupen
9700 Leupegem
4120 Neupre
4280 Villers-le-Peuplier
""")
		
if __name__ == '__main__':
	unittest.main()

