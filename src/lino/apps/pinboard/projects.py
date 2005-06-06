#coding: latin1

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
from tables import Users, Partners
#from web import MemoMixin, MemoTreeMixin


class Projects(MemoTreeTable):
    
    def init(self):
        MemoTreeTable.init(self)
        self.addField('id',ROWID)
        self.addField('date',DATE)
        self.addField('stopDate',DATE)

        self.addPointer('responsible',Users).setDetail("projects")
        self.addPointer('sponsor', Partners) 
        self.addPointer('status', ProjectStati).setDetail("projects")
        
        #from sdk import Version
        #self.version = Pointer(Version,"projects")

        self.addView("std",
                     columnNames="title abstract status",
                     label="Top-level projects",
                     super=None)

    class Instance(MemoTreeTable.Instance):
        pass


class ProjectStati(BabelTable):
    "list of codes used to formulate how far a project is"
    def init(self):
        BabelTable.init(self)
        self.addField('id',STRING)
        #self.name = BabelField(STRING)


