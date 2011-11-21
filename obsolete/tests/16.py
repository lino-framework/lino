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
"""
from lino.misc.tsttools import TestCase, main

from lino.apps.pinboard.pinboard_demo import startup
from lino.apps.pinboard.pinboard_tables import Language, Node

class Case(TestCase):
    def setUp(self):
        TestCase.setUp(self)
        self.db = startup()
        
    def tearDown(self):
        self.db.shutdown()
        
    def test01(self):
        LANGS = self.db.query(Language)
        #LANGS.setBabelLangs('en')
        de = LANGS.peek('de')
        #print LANGS._table.getAttrList()
        for p in self.db.query(Node,lang=de):
        #for p in de.nodes_by_lang:
            self.assertEqual(p.title,'Bullshit Bingo')
            
        #print len(de.listof_PAGES)
        #print de.listof_PAGES[0]

        msg = de.vetoDelete()
        self.assertEqual(msg,"German is used by 1 rows in Quotes")
        #("German : quotes_by_lang not empty")
        
        et = LANGS.peek('et')
        self.assertEqual(et.vetoDelete(),None)
        
    def test02(self):
        LANGS = self.db.query(Language)
        #LANGS.setBabelLangs('en')
        xx = LANGS.peek('xx')
        self.assertEqual(xx,None)
        
        self.assertEqual(len(LANGS),5)
        xx = LANGS.appendRow(id='xx',name="Xyphoxolian")
        self.assertEqual(xx.id,'xx')
        xx.lock()
        xx.name='Xyphhoxolian'
        xx.unlock()
        self.assertEqual(len(LANGS),6)

        
if __name__ == '__main__':
    main()

