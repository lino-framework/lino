#coding: latin1

## Copyright Luc Saffre 2003-2004.

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

testing new races module, wrapped header labels and "d" or "*" as item
in columnWidths

"""
import os

from lino.adamo import *
from lino.tools.normalDate import ND
from lino.ui import console
from lino.misc.tsttools import TestCase, main

from lino.schemas.sprl.addrbook import Persons

from lino.schemas.sprl.races import Races, Participants, RaceTypes,\
     Categories, Clubs


class BasePlugin(SchemaPlugin):
    def defineTables(self,schema):
        schema.addTable(Clubs)
        schema.addTable(Persons)
        schema.addTable(Categories)
        schema.addTable(RaceTypes)
        schema.addTable(Races)
        schema.addTable(Participants)
        
        
        
class Case(TestCase):
    
    def test01(self):
        schema = Schema(label="Raceman Report Tester")
        schema.addPlugin(BasePlugin())

        sess = schema.quickStartup()



        PERSONS = sess.query(Persons)
        norbert = PERSONS.appendRow( name="Ausdemwald",
                                     firstName="Norbert",
                                     sex="M",
                                     birthDate="19800506")
        edgar = PERSONS.appendRow( name="Ausdemwald",
                                   firstName="Edgar",
                                   sex="M",
                                   birthDate="19800505")

        RACES = sess.query(Races)
        race = RACES.appendRow(date=ND(20040112),name1="test race")
        race.participants_by_race.appendRow(person=norbert,
                                            dossard="0012",
                                            time="13:30:10")
        race.participants_by_race.appendRow(person=edgar,
                                            dossard="0013",
                                            time="12:10:80")

        sess.startDump()
        q = sess.query(Participants,
                       "time dossard person.name person.firstName",
                       race=race,
                       orderBy="time dossard",
                       pageLen=10)
        q.executeReport(columnWidths="d d 20 15")
        s = sess.stopDump()
        #print s
        self.assertEquals(s,"""\
Participants
============
time    |doss|name                |firstName      
        |ard |                    |               
--------+----+--------------------+---------------
12:10:80|0013|Ausdemwald          |Edgar          
13:30:10|0012|Ausdemwald          |Norbert        
""")

        sess.shutdown()



        
        
if __name__ == "__main__":
    main()
