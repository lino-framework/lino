# coding: latin1

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

from lino.misc.tsttools import TestCase, main

from lino.apps.pinboard.pinboard_demo import startup
from lino.apps.pinboard.pinboard_tables import Author


class Case(TestCase):
    
    def setUp(self):
        TestCase.setUp(self)
        self.sess = startup(populate=False)

    def tearDown(self):
        self.sess.shutdown()


    def test01(self):
        
        ae = self.assertEqual
        
        l1 = [str(t.getTableName())
              for t in self.sess.getTableList()]
        #l1.sort()

        s=" ".join(l1)
        
        #print s

        self.assertEquivalent(s, """
Users Contacts Nations Cities Languages ProjectStati Projects
EventTypes Events Nodes Newsgroups News AuthorEventTypes AuthorEvents
Authors Topics Publications Quotes PubTypes PubAuthors
""")
        
        
    def test02(self):
        "2 successive appendRow() without specifying id"
        AUTHORS = self.sess.query(Author)
        pot = AUTHORS.appendRow(firstName="Harry",name="Potter")
        bel = AUTHORS.appendRow(firstName="Harry",name="Bellafonte")
        self.assertEqual(pot.id, bel.id-1)
        

if __name__ == '__main__':
    main()

