#coding: iso-8859-1

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

from lino.adamo.ddl import *
from tables import User
#from web import MemoMixin, MemoTreeMixin

from lino.apps import addrbook


class PRB(StoredDataRow):
    tableName="Themen"
    def initTable(self,table):
        StoredDataRow.initTable(self,table)
        table.addField('id',ROWID)
        table.addField('ref',STRING)
        table.addField('name',STRING)
        
class DLA(StoredDataRow):
    tableName="Dienstleistungsarten"
    def initTable(self,table):
        StoredDataRow.initTable(self,table)
        table.addField('id',ROWID)
        table.addField('ref',STRING)
        table.addField('name',STRING)
        
class Partner(addrbook.tables.Partner):
    tableName="Akten"
    def initTable(self,table):
        addrbook.tables.Partner.initTable(self,table)
        #table.addField('id',STRING)
        #table.addField('firstName',STRING)
        #table.addField('name',STRING)
        table.addField('birthDate',DATE)
        table.addField('dbcode',STRING(1))
        
class DLS(StoredDataRow):
    tableName="Dienstleistungen"
    def initTable(self,table):
        StoredDataRow.initTable(self,table)
        table.addField('id',ROWID)
        table.addField('date',DATE)
        table.addField('nb',STRING)

        table.addPointer('dla',DLA)
        table.addPointer('partner',Partner)
        
