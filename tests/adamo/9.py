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

from lino.misc import tsttools
from lino.schemas.sprl import demo
from lino.schemas.sprl.tables import Partners
from lino.schemas.sprl.tables import Quotes, Authors, Languages

class Case(tsttools.TestCase):
    def setUp(self):
        self.db = demo.beginSession(withJokes=True)
        
    def tearDown(self):
        self.db.shutdown()
        
    def test01(self):
        "new style to specify samples for a query using **kw"
        LANGS = self.db.query(Languages)
        QUOTES = self.db.query(Quotes)
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
        FROM Quotes AS lead
        LEFT JOIN Authors AS author
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
    tsttools.main()

