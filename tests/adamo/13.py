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

import unittest

from lino.schemas.sprl import demo
from lino.schemas.sprl.tables import Pages

class Introduction(unittest.TestCase):

    def setUp(self):
        
        self.db = demo.beginSession()

    def tearDown(self):
        self.db.shutdown()


    def test01(self):
        PAGES = self.db.query(Pages)
        #print [a.name for a in PAGES._table.peekQuery._atoms]
        PAGES.appendRow(match="index",
                        title="Main page",
                        abstract="Welcome",
                        body="bla bla "*50)
        PAGES.appendRow(match="copyright",
                        title="Copyright",
                        abstract="Legal notes for this site.",
                        body="BLA BLA "*50)
        # PAGES.commit()
        # PAGES.query("id match title",match="index").report()
        row = PAGES.findone(match="index")

        self.assertEqual(row.title,'Main page')
        

if __name__ == '__main__':
    unittest.main()

