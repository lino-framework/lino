# coding: latin1
"""
20040428

The first multi-language database

"""
import unittest
from lino.misc.tsttools import TestCase
from lino.schemas.sprl import demo
from lino.adamo.datatypes import DataVeto

class Case(TestCase):
	def setUp(self):
		self.db = demo.beginSession(langs="en de fr")
		self.db.installto(globals())
		
	def tearDown(self):
		self.db.shutdown()
		
	def test01(self):
		n = NEWS.appendRow(date=20040428,title="test")
		self.assertEqual(str(n.date),'20040428')

		q = LANGS.query(orderBy="name")
		
		setBabelLangs('en')
		self.assertEquivalent(q.getSqlSelect(),"""\
		SELECT
		  id, name_en, name_de, name_fr
		FROM LANGS
		  ORDER BY name_en
		""")
		s = ""
		for row in q:
			s += row.getLabel() + "\n"
		#print s
		self.assertEquivalent(s,"""\
Dutch
English
Estonian
French
German
""")

		setBabelLangs('fr')
		self.assertEquivalent(q.getSqlSelect(),"""\
		SELECT
		  id, name_en, name_de, name_fr
		FROM LANGS
		  ORDER BY name_fr
		""")
		s = ""
		for row in LANGS.query(orderBy="name"):
			s += row.getLabel() + "\n"
		#print s
		self.assertEquivalent(s,"""\
Allemand
Anglais
Estonien
Français
Neerlandais
""")
		
		

		
if __name__ == '__main__':
	unittest.main()

