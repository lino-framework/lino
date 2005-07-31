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

from lino.schemas.sprl.addrbook import Partners
from web import Pages


class Events(Pages):
    def init(self):
        #MemoMixin.init(self,table)
        Pages.init(self)
        self.getRowAttr('id').setType(ROWID)
        self.addField('date', DATE)
        self.addField('time', STRING)
        self.addPointer('type', EventTypes).setDetail("eventsByType")
        
        self.addPointer('responsible',Partners).setDetail(
            'eventsByResponsible')
        self.addPointer('place',Partners).setDetail('eventsByPlace')
        

        #self.setColumnList('date time place title abstract')
        self.setOrderBy("date time")

    class Instance(Pages.Instance):
        
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
    
class EventTypes(MemoTable):
    def init(self):
        MemoTable.init(self)
        self.addField('id',STRING)
        self.addBabelField('name',STRING)
        #table.addDetail('eventsByType',Event)
        
    class Instance(Table.Instance):
        def __str__(self):
            return self.title
        
