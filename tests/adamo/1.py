# coding: latin1
"""
Some tests on getDemoDB()
"""

import types
import unittest

from lino.adamo.datatypes import DataVeto

from lino.schemas.sprl import demo

class Case(unittest.TestCase):

	def setUp(self):
		
		self.db = demo.beginSession()
		self.db.installto(globals())

	def tearDown(self):
		self.db.shutdown()


	def test01(self):
		
		ae = self.assertEqual
		
		l1 = [str(t.getTableName())
				for t in self.db.schema.getTableList()]
		l1.sort()
		
		l2 = """AUTHORS BOOKINGS CITIES Currencies EVENTS EVENTTYPES
		INVOICELINES INVOICES JOURNALS LANGS NATIONS NEWS NEWSGROUPS
		ORGS PAGES PARTNERS PARTYPES PEREVENTS PEVTYPES PRJSTAT PRODUCTS
		PROJECTS PUB2AUTH PUBLICATIONS PUBTYPES QUOTES TOPICS USERS
		YEARS""".split()

		self.assertEqual(l1,l2)
		
		setBabelLangs("en")
		l = []
		for ds in self.db.tables.values():
			line = [ds.getTableName()]
			line.append(len(ds))
			if len(ds) != 0:
				line.append(ds[0])
				line.append(ds[-1])
				
			l.append(tuple(line))
## 			else:
## 				if len(a._table.getPrimaryKey()) == 1:
## 					r = q.appendRow()

		l.sort()
		
		lines = []
		for line in l:
			lines.append("\t".join([str(x) for x in line]))
		s = "\n".join(lines)
		#print s
		ae(s,"""\
AUTHORS	13	Bill Gates	Henry Louis Mencken
BOOKINGS	0
CITIES	27	Bruxelles (be)	Alfter-Oedekoven (de)
Currencies	3	EUR	BEF
EVENTS	0
EVENTTYPES	0
INVOICELINES	2	('OUT', 1, 1)	('OUT', 1, 2)
INVOICES	1	OUT-1	OUT-1
JOURNALS	1	outgoing invoices	outgoing invoices
LANGS	5	English	Dutch
NATIONS	5	Estonia	United States of America
NEWS	0
NEWSGROUPS	0
ORGS	1	(1,)	(1,)
PAGES	2	Lino Demo Data	Bullshit Bingo
PARTNERS	12	Luc Saffre	Eesti Telefon
PARTYPES	5	Customer	Sponsor
PEREVENTS	0
PEVTYPES	5	born	other
PRJSTAT	5	to do	sleeping
PRODUCTS	2	(3,)	(16,)
PROJECTS	10	Project 1	Project 1.3.2.2
PUB2AUTH	0
PUBLICATIONS	0
PUBTYPES	6	Book	Software
QUOTES	8	[q1]	[q8]
TOPICS	0
USERS	2	Luc Saffre	James Bond
YEARS	0""")
				

		row = PARTNERS.peek(1)

		# print "foobar " + repr(row.getValues())

		""" The row returned by peek() is an object whose properties can
		be accessed (or not) according to the specific rules.	 """

		# simple fields :
		
		ae(row.id,1)
		ae(row.name,"Saffre")
		ae(row.getLabel(),"Luc Saffre")

		tallinn = CITIES.findone(name="Tallinn")
		
		ae(row.city,tallinn)
		
		ae(row.city.name,"Tallinn")
		ae(row.nation.name,"Estonia")
		




	def test05(self):
		
		""" If you are going to create several rows and don't want to
		specify the field names each time, then you can create a Query:
		"""

		q = PARTNERS.query('id firstName name')
		
		row = q.appendRow(1000,"Jean","Dupont")
		self.assertEqual(row.id,1000)
		self.assertEqual(row.firstName,"Jean")
		self.assertEqual(row.name,"Dupont")
		
		q.appendRow(1001,"Joseph","Dupont")
		q.appendRow(1002,"Juliette","Dupont")
		
	def test06(self):
		"Samples"
		
		""" If you tell a Query of Cities that you want only cities in
		Belgium, then use this query to create a city row, then this row
		will automatically know that it's nation is Belgium.	"""

		be = NATIONS.peek("be")
		q = CITIES.query(nation=be)
		q = be.cities #.query('id name')
		stv = q.appendRow(name='Sankt-Vith')
		# print row.getValues()
		self.assertEqual(stv.nation,be)
		self.assertEqual(stv.name,"Sankt-Vith")
		# q.appendRow(21,'Eynatten')


	def test03(self):
		"logical primary key versus atomic primary key"

		#INVOICES = self.db.schema.INVOICES
		#INVOICELINES = self.db.schema.INVOICELINES
		self.assertEqual(INVOICES._table.getPrimaryKey(),
							  ("jnl","seq"))
		self.assertEqual(
			tuple(map(lambda (n,t) : n,
						 INVOICES._table.getPrimaryAtoms())),
			("jnl_id","seq")
			)
		
		self.assertEqual(INVOICELINES._table.getPrimaryKey(),
							  ("invoice","line"))
		self.assertEqual(
			tuple(map(lambda (n,t) : n,
						 INVOICELINES._table.getPrimaryAtoms())),
			("invoice_jnl_id","invoice_seq","line")
			)
		


		
## if __name__ == "__main__":
##		from lino.misc import tsttools
##		tsttools.run("1")

if __name__ == '__main__':
	unittest.main()
