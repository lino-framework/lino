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
#from tables import User, Partner
#from web import MemoMixin, MemoTreeMixin
import pinboard_tables as tables


class Project(MemoTreeRow):
    tableName="Projects"
    def initTable(self,table):
        MemoTreeRow.initTable(self,table)
        table.addField('id',ROWID)
        table.addField('startDate',DATE)
        table.addField('stopDate',DATE)

        table.addPointer('responsible',tables.User)#.setDetail("projects")
        table.addPointer('sponsor', tables.Contact) 
        table.addPointer('status', ProjectStatus)#.setDetail("projects")
        
        #from sdk import Version
        #self.version = Pointer(Version,"projects")

##         table.addView("std",
##                      columnNames="title abstract status",
##                      #label="Top-level projects",
##                      super=None)

class ProjectsReport(DataReport):
    leadTable=Project
    columnNames="title abstract status"
    orderBy="title"
    masters={'super': None}


class ProjectStatus(BabelRow):
    "list of codes used to formulate how far a project is"
    tableName="ProjectStati"
    def initTable(self,table):
        BabelRow.initTable(self,table)
        table.addField('id',STRING)
        #self.name = BabelField(STRING)


class ProjectStatiReport(DataReport):
    leadTable=ProjectStatus
    
