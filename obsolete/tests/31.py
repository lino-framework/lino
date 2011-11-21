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

tests new races module
tests wrapped header labels and "d" or "*" as item in columnWidths

"""
import os

from lino.adamo import *
from lino.adamo.datatypes import itod, DURATION
#from lino.tools.normalDate import ND
#from lino.ui import console
from lino.misc.tsttools import TestCase, main

from lino.apps.raceman.raceman import Raceman
from lino.apps.raceman import raceman_tables as tables

#from lino.reports import DataReport

#from lino.apps.raceman.races import Races, Participants, RaceTypes,\
#     Categories, Clubs, Persons

        
class Case(TestCase):
    
    def test01(self):
        app = Raceman() # label="Raceman Report Tester")
        #races.setupSchema(schema)
        sess = app.createContext() # quickStartup()

        PERSONS = sess.query(tables.Person)
        norbert = PERSONS.appendRow(name="Ausdemwald",
                                    firstName="Norbert",
                                    sex="M",
                                    birthDate="19800506")
        edgar = PERSONS.appendRow( name="Ausdemwald",
                                   firstName="Edgar",
                                   sex="M",
                                   birthDate="19800505")

        RACES = sess.query(tables.Race)
        race = RACES.appendRow(date=itod(20040112),name1="test race")
        qry=race.participants()
        qry.appendRow(
            person=norbert,
            dossard="0012",
            duration=DURATION.parse("00.55.10"))
        qry.appendRow(
            person=edgar,
            dossard="0013",
            duration=DURATION.parse("01.10.50"))

        #sess.startDump()
        q = qry.query(
            "duration dossard person.name person.firstName",
            orderBy="duration dossard",
            pageLen=10)
        
        q.show(columnWidths="d d 20 15")
        #rpt=sess.createDataReport(q,columnWidths="d d 20 15")
        #sess.showReport(rpt)
        #q.report(columnWidths="d d 20 15")
        #self.ui.report(rpt)
        #q.executeReport(columnWidths="d d 20 15")
        s = self.getConsoleOutput()
        #print s
        self.assertEquals(s,"""\
Participants (race=test race)
=============================
duration|doss|person.name         |person.firstNam
        |ard |                    |e              
--------+----+--------------------+---------------
00.55.10|0012|Ausdemwald          |Norbert        
01.10.50|0013|Ausdemwald          |Edgar          
""")

        sess.shutdown()



        
        
if __name__ == "__main__":
    main()
