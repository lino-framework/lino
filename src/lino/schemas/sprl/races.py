## Copyright Luc Saffre 2004-2005.

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

from lino.adamo import *
from babel import Languages
from addrbook import Persons, SEX

NAME = STRING.child(width=30)

class Races(Table):
    def init(self):
        self.addField('name1',NAME)
        self.addField('name2',NAME)
        self.addField('date',DATE)
        self.addField('status',STRING.child(width=1))
        self.addField('tpl',STRING.child(width=6))
        self.addPointer('type',RaceTypes)
        self.addField('startTime',TIME)

    class Instance(Table.Instance):
        def getLabel(self):
            return self.name1
        
class RaceTypes(Table):
    def init(self):
        self.addField('id',STRING.child(width=5))
        self.addField('name',NAME)

    class Instance(Table.Instance):
        def getLabel(self):
            return self.name
        
class Categories(Table):
    def init(self):
        self.addPointer('type',RaceTypes)
        self.addField('id',STRING.child(width=3))
        self.addField('seq',ROWID)
        self.addField('name',STRING.child(width=30))
        self.addField('sex',SEX)
        self.addField('ageLimit',INT)
        
        self.setPrimaryKey('type id')

    class Instance(Table.Instance):
        def getLabel(self):
            return self.id + " ("+self.name+")"
        
class Participants(Table):
    def init(self):
        self.setPrimaryKey("race dossard")
        
        self.addPointer('race',Races)
        self.addField('dossard',STRING)
        self.addPointer('person',Persons)
        self.addField('time',TIME)
        self.addPointer('cat',Categories)
        self.addField('payment',STRING.child(width=1))
        

