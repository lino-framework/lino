# coding: latin1
import unittest
from lino.misc import tsttools
from lino.schemas.sprl import demo

class Case(tsttools.TestCase):
	def setUp(self):
		self.db = demo.getDemoDB(withJokes=True)
		self.db.installto(globals())
		
	def tearDown(self):
		self.db.shutdown()
		
	def test01(self):
		"new style to specify samples for a query using **kw"
		s = ""
		de = LANGS.peek('de')
		q = QUOTES.query("abstract author.name id",
							  orderBy="id",
							  lang=de)
		q.setSqlFilters("abstract LIKE '%Dummheit%'")
		self.assertEquivalent(q.getSqlSelect(),"""\
		SELECT lead.id,
		  lead.abstract,
		  lead.author_id,
		  author.id,
		  author.name, lead.lang_id
		FROM QUOTES AS lead
        LEFT JOIN AUTHORS AS author
          ON (lead.author_id = author.id)
        WHERE lang_id = 'de'
          AND abstract LIKE '%Dummheit%'
        ORDER BY lead.id
		""")
		
		for quote in q:
			s += quote.abstract + "\n"

		self.assertEqual(s,"""\
Alles hat Grenzen, nur die Dummheit ist unendlich.
Alter schützt nicht vor Torheit, aber Dummheit vor Intelligenz.
Dummheit, verlass ihn nicht, sonst steht er ganz allein.
Lieber natürliche Dummheit als künstliche Intelligenz.
""")

		s = ""
		q = QUOTES.query("abstract",
							  orderBy="abstract",
							  lang=de)
		q.setSqlFilters("abstract LIKE '%Klügere%'")
		for quote in q:
			s += quote.abstract + "\n"

		#print s
		self.assertEqual(s,"""\
Der Klügere gibt so lange nach, bis er der Dumme ist.
Der Klügere gibt vor, nachzugeben.
Der Klügere zählt nach.
So lange der Klügere nachgibt, wird die Welt von Dummen beherrscht.
""")
		
if __name__ == '__main__':
	unittest.main()

