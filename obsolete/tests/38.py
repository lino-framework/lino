## Copyright 2005-2007 Luc Saffre

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

from lino.adamo.ddl import Schema, DATE, TIME
from lino.misc.tsttools import TestCase, main
#from lino.adamo.datatypes import 

#from lino.apps.raceman.raceman_forms import Raceman
from lino.apps.raceman.raceman_tables import *
#Race, Participant, RacemanSchema

class Case(TestCase):

    def test01(self):
        schema=RacemanSchema()
        sess = schema.createContext()

        R = sess.query(Race)
        P = sess.query(Participant)

        heute = DATE.parse("2005-01-28")
        jetzt = TIME.parse("17:38:59")
        
        R.startDump()
        race = R.appendRow(name1="test a",
                           date=heute,
                           startTime=jetzt )
        sql = R.stopDump()
        #print sql
        self.assertEquivalent(sql,"""\
SELECT MAX(id) FROM Races; INSERT INTO Races (
id, name1, name2, xdate, status, tpl, type_id,
startTime, known, unknown, invalid, missing, event_id
) VALUES
( 1, 'test a', NULL, 731974, NULL, NULL, NULL,
'17:38:59', NULL, NULL, NULL, NULL, NULL );        
        """)

        R.startDump()
        race = R.peek(1)
        sql = R.stopDump()
        #print sql
        self.assertEquivalent(sql,"""\
SELECT id, name1, name2, xdate, status, tpl, type_id, startTime, known, unknown, invalid, missing, event_id
FROM Races WHERE id = 1;        
        """)
        self.assertEqual(race.startTime,jetzt)
        self.assertEqual(race.date,heute)

        sess.shutdown()
        

if __name__ == '__main__':
    main()

