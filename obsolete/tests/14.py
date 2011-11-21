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

import datetime
from lino.misc.tsttools import TestCase, main

from lino.adamo.datatypes import itod

from lino.apps.pinboard.pinboard_demo import startup
from lino.apps.pinboard.pinboard_tables import Event

class Case(TestCase):
    def setUp(self):
        TestCase.setUp(self)
        self.db = startup(populate=False)
        
    def tearDown(self):
        self.db.shutdown()
        
    def test01(self):
        EVENTS = self.db.query(Event)
        d = itod(20040413)
        for i in range(100):
            EVENTS.appendRow(date=d,
                             title="Event # %d" % i)
            d += datetime.timedelta(days=1)

        e = EVENTS.findone(date=itod(20040501))
        self.assertEqual(e.id,19)
        self.assertEqual(e.title,'Event # 18')
        #print e

        
if __name__ == '__main__':
    main()

