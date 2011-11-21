## Copyright 2004-2006 Luc Saffre 

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



import os
import sys


from lino import adamo

from raceman_tables import *
#Races, RaceTypes, Categories, \
#     Participants, Persons, Clubs

from lino.adamo.table import DbfMirrorLoader


class PersonsMirrorLoader(DbfMirrorLoader):
    tableClass = Person
    tableName = "PAR"
    def appendFromDBF(self,q,row):
        q.appendRow(
            id=int(row['IDPAR']),
            name=row['FIRME'],
            firstName=row['VORNAME'],
            sex=row['SEX'],
            birthDate=row['BIRTH'])


class ClubsMirrorLoader(DbfMirrorLoader):
    tableClass = Club
    tableName = "CLB"
    def appendFromDBF(self,q,row):
        q.appendRow(
            id=row['IDCLB'],
            name=row['NAME'],
            )

class RaceTypesMirrorLoader(DbfMirrorLoader):
    tableClass = RaceType
    tableName = "CTY"
    def appendFromDBF(self,q,row):
        q.appendRow(
            id=row['IDCTY'],
            name=row['NAME'],
            )


class CategoriesMirrorLoader(DbfMirrorLoader):
    tableClass = Category
    tableName = "CAT"
    def appendFromDBF(self,q,row):
        q.appendRow(
            id=row['IDCAT'],
            seq=row['SEQ'],
            sex=row['SEX'],
            type=q.getSession().peek(RaceTypes,row['IDCTY']),
            name=row['NAME'],
            ageLimit=row['MAXAGE'],
            )
        

class RacesMirrorLoader(DbfMirrorLoader):
    tableClass = Race
    tableName = "RAL"
    #def init(self):
    #    Races.init(self)
    #    self.getRowAttr('id').setType(adamo.STRING(width=6))
    def appendFromDBF(self,q,row):
        sess = q.getSession()
        raceType = sess.peek(RaceTypes,row['CATTYPE'])
        q.appendRow(
            id=int(row['IDRAL']),
            name1=row['NAME1'],
            name2=row['NAME2'],
            date=self.dbfdate(row['DATE']),
            type=raceType,
            startTime=self.dbftime(row['STARTTIME']),
            )
        

class ParticipantsMirrorLoader(DbfMirrorLoader):
    tableClass = Participant
    tableName = "POS"
    def appendFromDBF(self,q,row):
        sess = q.getSession()
        race = sess.peek(Races,int(row['IDRAL']))
        person = sess.peek(Persons,int(row['IDPAR']))
        if race.type is None:
            cat = None
        else:
            cat = sess.peek(Categories,race.type,row['IDCAT'])
        club = sess.peek(Clubs,row['IDCLB'])
        q.appendRow(
            race=race,
            person=person,
            cat=cat,
            club=club,
            dossard=row['IDPOS'],
            duration=self.dbfduration(row['TIME']),
            place=int(row['PLACE']),
            catPlace=int(row['CATPLACE']),
            payment=row['PAYE'],
            )
    

LOADERS = (
    PersonsMirrorLoader,
    ClubsMirrorLoader,
    RacesMirrorLoader,
    RaceTypesMirrorLoader,
    CategoriesMirrorLoader,
    ParticipantsMirrorLoader,
    )

## def makeSchema(dbfpath):
    
##     schema = adamo.Schema()
##     schema.addTable(Clubs).setMirrorLoader(
##         ClubsMirrorLoader(dbfpath))
##     schema.addTable(Persons).setMirrorLoader(
##         PersonsMirrorLoader(dbfpath))
##     schema.addTable(RaceTypes).setMirrorLoader(
##         RaceTypesMirrorLoader(dbfpath))
##     schema.addTable(Categories).setMirrorLoader(
##         CategoriesMirrorLoader(dbfpath))
##     schema.addTable(Races).setMirrorLoader(
##         RacesMirrorLoader(dbfpath))
##     schema.addTable(Participants).setMirrorLoader(
##         ParticipantsMirrorLoader(dbfpath))
##     schema.addTable(Arrivals)
##     return schema
    





