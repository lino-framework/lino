#coding: latin1

## Copyright 2003-2006 Luc Saffre

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


"""
20040428

The first multi-language database

"""
from lino.misc.tsttools import TestCase, main

from lino.adamo.datatypes import itod
from lino.apps.pinboard.pinboard_demo import startup
from lino.apps.pinboard.pinboard_tables import Language,NewsItem

class Case(TestCase):
    def setUp(self):
        TestCase.setUp(self)
        self.db = startup(langs="en de fr")
        
    def tearDown(self):
        self.db.shutdown()
        
    def test01(self):
        
        NEWS = self.db.query(NewsItem)
        LANGS = self.db.query(Language)
        
        n = NEWS.appendRow(date=itod(20040428),title="test")
        self.assertEqual(str(n.date),'2004-04-28')

        q = LANGS.query(orderBy="name")
        
        LANGS.setBabelLangs('en')
        self.assertEquivalent(q.getSqlSelect(),"""\
        SELECT
          id, name_en, name_de, name_fr
        FROM Languages
          ORDER BY name_en
        """)
        s = ""
        for row in q:
            s += row.name + "\n"
        #print s
        self.assertEquivalent(s,"""\
Dutch
English
Estonian
French
German
""")

        LANGS.setBabelLangs('fr')
        self.assertEquivalent(q.getSqlSelect(),"""\
        SELECT
          id, name_en, name_de, name_fr
        FROM Languages
          ORDER BY name_fr
        """)
        s = ""
        for row in LANGS.query(orderBy="name"):
            s += row.name + "\n"
        #print s
        self.assertEquivalent(s,u"""\
Allemand
Anglais
Estonien
Français
Neerlandais
""")
        
        

        
if __name__ == '__main__':
    main()

