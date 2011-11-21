## Copyright 2003-2007 Luc Saffre

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
from lino.apps.pinboard.pinboard_tables import Node


class Introduction(TestCase):

    def setUp(self):
        TestCase.setUp(self)
        self.db = startup()

    def tearDown(self):
        self.db.shutdown()


    def test01(self):
        PAGES = self.db.query(Node)
        #print [a.name for a in PAGES._table.peekQuery._atoms]
        PAGES.appendRow(match="index",
                        title="Main page",
                        abstract="Welcome",
                        body="bla bla"*50)
        PAGES.appendRow(match="copyright",
                        title="Copyright",
                        abstract="Legal notes for this site.",
                        body="BLA BLA"*50)
        # PAGES.commit()
        # PAGES.query("id match title",match="index").report()
        row = PAGES.findone(match="index")

        self.assertEqual(row.title,'Main page')
        

if __name__ == '__main__':
    main()

