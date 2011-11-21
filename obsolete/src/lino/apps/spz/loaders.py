## Copyright 2004-2005 Luc Saffre 

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


from lino.apps.spz import tables

from lino.adamo.table import DbfMirrorLoader


class ProblemsMirrorLoader(DbfMirrorLoader):
    tableClass = tables.PRB
    tableName = "PRB"
    def appendFromDBF(self,q,row):
        q.appendRow(
            id=int(row['IDPRB']),
            name=row['NAME'],
            ref=row['REF'],
            )

## class NodesMirrorLoader(DbfMirrorLoader):
##     tableClass = tables.Node
##     tableName = "MSX"
##     def appendFromDBF(self,q,row):
##         q.appendRow(
##             id=int(row['IDMSX']),
##             title=row['TITLE'],
##             subtitle=row['SUBTITLE'],
##             abstract=row['ABSTRACT'],
##             body=row['BODY'],
##             modified=self.dbfdate(row['LASTMOD']),
##             match=row['MATCH'],
##             lang=tim2lang(q,row['IDLNG'])
##             )

## class NewsMirrorLoader(DbfMirrorLoader):
##     tableClass = tables.NewsItem
##     tableName = "NEW"
##     def appendFromDBF(self,q,row):
##         sess = q.getSession()
##         #if len(row['IDMSX'].strip()) == 0:
##         if row['IDMSX'] is None:
##             node=None
##         else:
##             node = sess.peek(tables.Node,int(row['IDMSX']))
##         q.appendRow(
##             id=int(row['IDNEW']),
##             title=row['TITLE'],
##             node=node,
##             abstract=row['ABSTRACT'],
##             body=row['BODY'],
##             date=self.dbfdate(row['DATE']),
##             time=self.dbftime(row['TIME']),
##             lang=tim2lang(q,row['IDLNG'])
##             )

## class PublicationsMirrorLoader(DbfMirrorLoader):
##     tableClass = tables.Publication
##     tableName = "PUB"
##     def appendFromDBF(self,q,row):
##         sess = q.getSession()
##         #if len(row['IDAUT'].strip()) == 0:
##         if row['IDAUT'] is None:
##             author=None
##         else:
##             author = sess.peek(tables.Author,int(row['IDAUT']))
##         q.appendRow(
##             id=int(row['IDPUB']),
##             title=row['TITLE'],
##             subtitle=row['SUBTITLE'],
##             author=author,
##             url=row['URL'],
##             lang=tim2lang(q,row['IDLNG'])
##             #lang=row['IDLNG'],
##             )


## class RaceTypesMirrorLoader(DbfMirrorLoader):
##     tableClass = RaceTypes
##     tableName = "CTY"
##     def appendFromDBF(self,q,row):
##         q.appendRow(
##             id=row['IDCTY'],
##             name=row['NAME'],
##             )


## class CategoriesMirrorLoader(DbfMirrorLoader):
##     tableClass = Categories
##     tableName = "CAT"
##     def appendFromDBF(self,q,row):
##         q.appendRow(
##             id=row['IDCAT'],
##             seq=row['SEQ'],
##             sex=row['SEX'],
##             type=q.getSession().peek(RaceTypes,row['IDCTY']),
##             name=row['NAME'],
##             ageLimit=row['MAXAGE'],
##             )
        

## class RacesMirrorLoader(DbfMirrorLoader):
##     tableClass = Races
##     tableName = "RAL"
##     #def init(self):
##     #    Races.init(self)
##     #    self.getRowAttr('id').setType(adamo.STRING(width=6))
##     def appendFromDBF(self,q,row):
##         sess = q.getSession()
##         raceType = sess.peek(RaceTypes,row['CATTYPE'])
##         q.appendRow(
##             id=int(row['IDRAL']),
##             name1=row['NAME1'],
##             name2=row['NAME2'],
##             date=self.dbfdate(row['DATE']),
##             type=raceType,
##             startTime=self.dbftime(row['STARTTIME']),
##             )
        

## class ParticipantsMirrorLoader(DbfMirrorLoader):
##     tableClass = Participants
##     tableName = "POS"
##     def appendFromDBF(self,q,row):
##         sess = q.getSession()
##         race = sess.peek(Races,int(row['IDRAL']))
##         person = sess.peek(Persons,int(row['IDPAR']))
##         if race.type is None:
##             cat = None
##         else:
##             cat = sess.peek(Categories,race.type,row['IDCAT'])
##         club = sess.peek(Clubs,row['IDCLB'])
##         q.appendRow(
##             race=race,
##             person=person,
##             cat=cat,
##             club=club,
##             dossard=row['IDPOS'],
##             duration=self.dbfduration(row['TIME']),
##             place=int(row['PLACE']),
##             catPlace=int(row['CATPLACE']),
##             payment=row['PAYE'],
##             )
    

LOADERS = (
    ProblemsMirrorLoader
    )






