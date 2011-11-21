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

from lino.adamo.ddl import *

#from lino.apps.addrbook.tables import Partner
#from web import Node
import pinboard_tables as tables


class Event(tables.Node):
    tableName="Events"
    def initTable(self,table):
        #MemoMixin.init(self,table)
        tables.Node.initTable(self,table)
        table.getRowAttr('id').setType(ROWID)
        table.addField('date', DATE)
        table.addField('time', STRING)
        table.addPointer('type', EventType)#.setDetail("eventsByType")
        
        table.addPointer('responsible',tables.Contact)
        table.addPointer('place',tables.Contact)
        

        #table.setColumnList('date time place title abstract')
        table.setOrderBy("date time")

    def __str__(self):
        s = ''
        if self.title is None:
            s = self.type.title
        else:
            s = self.title
        s += " (" + str(self.date)
        if self.time is not None:
            s += ' ' + self.time + ' Uhr'
        s += ')'
        return s
    
class EventType(MemoRow):
    tableName="EventTypes"
    def initTable(self,table):
        MemoRow.initTable(self,table)
        table.addField('id',STRING)
        table.addBabelField('name',STRING)
        #table.addDetail('eventsByType',Event)
        
    def __str__(self):
        return self.title
        
