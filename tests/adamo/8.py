# coding: latin1

"""

the first test after Karneval 2004

Queries and Reports are no longer "connected". They don't know on
which Database they are going to be used.  So I cannot do "for row in
q", I must somehow specify the database too.

An AreaIterator is an iterator over the data rows of a query (or
report) which has been executed in a database.
An Area is a "connected table". 

>>> for i in db.fetchtuples(rpt)
>>> for i in db.fetchinstances(rpt)

>>> for t in q.tuples(**queryParams):
>>> for i in q.instances(**queryParams):

Alternatively (later):
		
>>> for t in q.tuples(db):
>>> for i in q.instances(db):

This is less elegant because one needs to specify the db handle again.

		
Perhaps even Areas are not needed?

But how to call it?
area.query(**keywords) or area.report(**keywords)


Notes:

- QueryIterator.appendRow() is different than Area.appendRow()

- "Table.peekQuery becomes Area.query. Code using peekQuery should now
  expect an area instead of a Table." No, because the peekQuery is a
  part of the Schema. If an application has many databases with the
  same Schema, there is still only one peekQuery for each Table.

- Should Area get an additional member "query" (assert query.leadTable
  is self._table)?  No, because an Area is primarily a cache for a
  table/connection pair.
  
- Should QueryIterator become a subclass of Area? No, because...

- QueryIterator becomes AreaIterator?

- Moved from Table to Area: values2id(), createTable()

"""
	


import unittest

class Case(unittest.TestCase):

		
	def test02(self):
		from lino.schemas.sprl import demo
		db = demo.getDemoDB()
		db.installto(globals())
		s1 = ''
		q = PARTNERS.query("name street city.name", orderBy="name")
		for row in q:
			#print row[0]
			s1 += str(row[0]) + " "
			s1 += str(row[1]) + " "
			s1 += str(row[2]) + "\n"
			
		s2 = ''
		for i in q:
			s2 += str(i.name) + " "
			s2 += str(i.street) + " "
			s2 += str(i.city.name) + "\n"

		#print s1
		self.assertEqual(s1,s2)

		
		self.assertEqual(s1,"""\
Arens None Eupen
Ausdemwald None Aachen
Bodard None Verviers
Eesti Telefon Sõpruse pst. Tallinn
Eierschal None Eupen
Eierschal None Eupen
Freitag None Eupen
Girf OÜ Laki Tallinn
Großmann None Eupen
PAC Systems PGmbH Hütte Eupen
Rumma & Ko OÜ Tartu mnt. Tallinn
Saffre None Tallinn
""")

		db.shutdown()

if __name__ == '__main__':
	unittest.main()

