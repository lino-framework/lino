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

"""
"""
from lino.misc.tsttools import TestCase, main

from lino.schemas.sprl import demo
from lino.schemas.sprl.tables import Languages

class Case(TestCase):
    def setUp(self):
        TestCase.setUp(self)
        self.db = demo.startup(self.ui)
        
    def tearDown(self):
        self.db.shutdown()
        
    def test01(self):
        LANGS = self.db.query(Languages)
        #LANGS.setBabelLangs('en')
        de = LANGS.peek('de')
        #print LANGS._table.getAttrList()
        for p in de.pages_by_lang:
            self.assertEqual(p.title,'Bullshit Bingo')
            
        #print len(de.listof_PAGES)
        #print de.listof_PAGES[0]

        msg = de.vetoDelete()
        self.assertEqual(msg,"German : quotes_by_lang not empty")
        
        et = LANGS.peek('et')
        self.assertEqual(et.vetoDelete(),None)
        
    def test02(self):
        LANGS = self.db.query(Languages)
        #LANGS.setBabelLangs('en')
        xx = LANGS.peek('xx')
        self.assertEqual(xx,None)
        
        self.assertEqual(len(LANGS),5)
        xx = LANGS.appendRow(id='xx')
        self.assertEqual(xx.id,'xx')
        xx.lock()
        xx.name='Xytoxolian'
        xx.unlock()
        self.assertEqual(len(LANGS),6)

        
if __name__ == '__main__':
    main()

