#coding: latin1
## Copyright 2005 Luc Saffre 

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

from lino.adamo.ddl import *

class Resource(StoredDataRow):
    tableName="Resources"
    def initTable(self,table):
        table.addField('id',STRING) 
        table.addField('name',STRING)
        table.addView("std", "id name")
        

    def setupMenu(self,nav):
        frm = nav.getForm()
        m = frm.addMenu("&Resource")
        def f():
            res = nav.getCurrentRow()
            frm.session.showTableGrid(res.usages)
            
        m.addItem("detail",
                  label="&Usages",
                  action=f,
                  accel="ENTER")

    def __str__(self):
        if self.name is not None: return self.name
        return self.id

    def delete(self):
        self.usages.deleteAll()

class ResourcesReport        

            
        
class Usage(StoredDataRow):
    tableName="Usages"
    def initTable(self,table):
        table.addField('id',ROWID) 
        table.addPointer('date',Day).setMandatory()
        table.addField('start',TIME)
        table.addField('stop',TIME)
        table.addPointer('type',UsageType)
        table.addField('remark',STRING)
        #table.addField('mtime',TIMESTAMP)
        table.addPointer('resource',Resource).setMandatory()
        table.addView("std", "id date start stop type remark")

    def __str__(self):
        s=""
        if self.remark is not None:
            s+=self.remark+" "
        if self.type is not None:
            s+= self.type.id + " "
        if self.start is None and self.stop is None:
            return s
        s += " %s-%s" % (self.start,self.stop)
        return s

        

class UsageType(StoredDataRow):
    tableName="UsageTypes"
    def initTable(self,table):
        table.addField('id',STRING(width=2))
        table.addField('name',STRING)
        table.addView("std", "id name")

    def __str__(self):
        return self.name
        
class Day(StoredDataRow):
    tableName="Days"
    def initTable(self,table):
        table.addField('date',DATE)
        table.addField('remark',STRING)
        table.setPrimaryKey("date")
        table.addView("std", "date remark")
        
    def __str__(self):
        return str(self.date)


TABLES = (
    Day,
    UsageType,
    Resource,
    Usage,
    )

__all__ = [t.__name__ for t in TABLES]

