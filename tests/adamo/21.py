# coding: latin1
#----------------------------------------------------------------------
# $Id: 21.py,v 1.3 2004/07/31 07:13:47 lsaffre Exp $
# Copyright: (c) 2004 Luc Saffre
# License:	 GPL
#----------------------------------------------------------------------

"""
- loop through partners in Belgium, setting currency to EUR 
- test for equality of DataRow instances


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

		be = NATIONS.peek("be")
		BEF = Currencies.peek('BEF')
		EUR = Currencies.peek('EUR')
		s = ""
		for p in PARTNERS.query("currency",
										orderBy="name firstName",
										nation=be):
			#if p.currency is None:
			#	s += p.getLabel() + " : currency remains None\n"
			if p.currency != EUR:
				# print p, p.currency.id
				s += p.getLabel() + " : currency %s updated to EUR\n" % str(p.currency)
				p.lock()
				p.currency = EUR
				p.unlock()
			else:
				s += p.getLabel() + " : currency was already EUR\n"

		#print s
		self.assertEqual(s,"""\
Andreas Arens : currency BEF updated to EUR
Henri Bodard : currency BEF updated to EUR
Emil Eierschal : currency was already EUR
Erna Eierschal : currency was already EUR
Frédéric Freitag : currency None updated to EUR
Gerd Großmann : currency was already EUR
PAC Systems PGmbH : currency None updated to EUR
""")
		
		


if __name__ == '__main__':
	unittest.main()

