# coding: latin1
#----------------------------------------------------------------------
# $Id: 20.py,v 1.3 2004/07/31 07:13:47 lsaffre Exp $
# Copyright: (c) 2004 Luc Saffre
# License:	 GPL
#----------------------------------------------------------------------

"""

Deciding whether to store values of a DataRow in a tuple of atomic
values or in a dict of complex values...

1. I iterate over a PARTNERS query with only the "currency" column
   (because this is the only one I am going to use. Plus the implicit
   "nation" column.

	The "print p" statement will do a call to Partners.getRowLabel()
	which will access row.name --- a field that was not included in my
	query!

	Or if I modify the row, then the validateRow() action will be
	triggered and it will ask for the partner's name.

	If a field was not part of the initial query, it will silently be
	looked up.

2. Accessing p.nation.name means that an attribute "p.nation" exists
   and has a Nations row as value.

3. (new:) Iterating over a row returns the cell value for each visible
   column of its query.



"""
import unittest
import types

#from lino.adamo import *
from lino.schemas.sprl import demo

class Case(unittest.TestCase):
	
	def setUp(self):
		
		self.db = demo.getDemoDB()
		self.db.installto(globals()) 

	def tearDown(self):
		self.db.shutdown()

	def test01(self):
		s = ""
		be = NATIONS.peek("be")
		q = PARTNERS.query("title firstName name",nation=be)
		for row in q:
			s += "\t".join([str(cell.getValue()) for cell in row]) + "\n"
		#print s
		self.assertEqual(s,"""\
Herrn	Andreas	Arens
Dr.	Henri	Bodard
Herrn	Emil	Eierschal
Frau	Erna	Eierschal
Herrn	Gerd	Großmann
Herrn	Frédéric	Freitag
None	None	PAC Systems PGmbH
""")
			
				

if __name__ == '__main__':
	unittest.main()

