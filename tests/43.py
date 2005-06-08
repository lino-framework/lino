## Copyright 2003-2005 Luc Saffre

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

"validators"

from lino.misc.tsttools import TestCase, main

from lino.apps.timings.timings import Timings
from lino.apps.timings.tables import *

from lino.adamo.ddl import DataVeto, itod


class Case(TestCase):

    def setUp(self):
        TestCase.setUp(self)
        self.sess = Timings().quickStartup() 

    def tearDown(self):
        self.sess.shutdown()


    def test01(self):
        
        days = self.sess.query(Days)
        
        try:
            days.appendRow()
        except DataVeto,e:
            self.assertEqual(
                str(e), "Column 'Days.date' may not be empty")
        else:
            self.fail('Failed to raise DataVeto')

        today=days.appendRow(date=itod(20050607))
            
        resources = self.sess.query(Resources)

        try:
            luc=resources.appendRow(name="Luc Saffre")
        except DataVeto,e:
            self.assertEqual(
                str(e), "Column 'Resources.id' may not be empty")
        else:
            self.fail('Failed to raise DataVeto')
            
        luc=resources.appendRow(id="LS",name="Luc Saffre")
        
        usages = self.sess.query(Usages)
        
        try:
            usages.appendRow(date=today)
        except DataVeto,e:
            self.assertEqual(
                str(e), "Column 'Usages.resource' may not be empty")
        else:
            self.fail('Failed to raise DataVeto')
            

if __name__ == '__main__':
    main()

