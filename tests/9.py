# coding: latin1
## Copyright Luc Saffre 2003-2005

## This file is part of the Lino project.

## Lino is free software; you can redistribute it and/or modify it
## under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.

## Lino is distributed in the hope that it will be useful, but WITHOUT
## ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
## or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public
## License for more details.

## You should have received a copy of the GNU General Public License
## along with Lino; if not, write to the Free Software Foundation,
## Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

from lino.misc.tsttools import TestCase, main
from lino.apps.pinboard import demo
from lino.apps.pinboard.tables import Partner,\
     Quote, Author, Language

from lino.apps.pinboard import quotes_de

class Case(TestCase):
    def setUp(self):
        TestCase.setUp(self)
        self.db = demo.startup(withJokes=True)
        #quotes_de.populate(self.db)
        #self.db.commit()
        
    def tearDown(self):
        self.db.shutdown()
        
    def test01(self):
        "new style to specify samples for a query using **kw"
        LANGS = self.db.query(Language)
        QUOTES = self.db.query(Quote)
        s = ""
        de = LANGS.peek('de')
        q = QUOTES.query("quote author.name id",
                         orderBy="id",
                         lang=de)
        q.setSqlFilters("quote LIKE '%Dummheit%'")
        self.assertEquivalent(q.getSqlSelect(),"""\
        SELECT lead.id,
          lead.quote,
          lead.author_id,
          author.id,
          author.name, lead.lang_id
        FROM Quotes AS lead
        LEFT JOIN Authors AS author
          ON (lead.author_id = author.id)
        WHERE lang_id = 'de'
          AND quote LIKE '%Dummheit%'
        ORDER BY lead.id
        """)
        
        for quote in q:
            s += quote.quote + "\n"

        self.assertEqual(s,"""\
Alles hat Grenzen, nur die Dummheit ist unendlich.
Alter schützt nicht vor Torheit, aber Dummheit vor Intelligenz.
Dummheit, verlass ihn nicht, sonst steht er ganz allein.
Lieber natürliche Dummheit als künstliche Intelligenz.
""")

        s = ""
        q = QUOTES.query("quote",
                         orderBy="quote",
                         lang=de)
        q.setSqlFilters("quote LIKE '%Klügere%'")
        for quote in q:
            s += quote.quote + "\n"

        #print s
        self.assertEqual(s,"""\
Der Klügere gibt so lange nach, bis er der Dumme ist.
Der Klügere gibt vor, nachzugeben.
Der Klügere zählt nach.
So lange der Klügere nachgibt, wird die Welt von Dummen beherrscht.
""")
        
if __name__ == '__main__':
    main()

