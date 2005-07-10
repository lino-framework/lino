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
# from babel import Languages

from tables import Persons, Cities, Languages

class Quotes(Table):
    def init(self):
        #MemoTable.init(self)
        self.addField('id',ROWID)
        self.addField('quote',MEMO)
        self.addPointer('author',Authors).setDetail('quotesByAuthor')
        self.addPointer('lang',Languages)
        #self.addField('lang',LANG)
        
        #self.pubRef = Field(STRING)
        #self.pub = Pointer("PUBLICATIONS")
        
    class Instance(MemoTable.Instance):
        def __str__(self):
            return "[q"+str(self.id)+"]"

class Publications(MemoTreeTable):
    def init(self):
        MemoTreeTable.init(self)
        self.addField('id',ROWID)
        self.addField('year',INT)
        self.addField('subtitle',STRING)
        self.addField('typeRef',STRING)
        self.addPointer('type', PubTypes)
        self.addPointer('author',Authors)
        self.addPointer('lang',Languages)
        #self.addField('lang',LANG)
        self.addField('url',URL)

class PubTypes(BabelTable):
    def init(self):
        self.addField('id',STRING)
        BabelTable.init(self)
        self.addField('typeRefPrefix',STRING)
        self.addBabelField('pubRefLabel',STRING)
        

class Topics(TreeTable):
    def init(self):
        TreeTable.init(self)
        self.addField('id',ROWID)
        self.addBabelField('name',STRING)
        #self.addPointer('lang',Languages)
        self.addField('dewey',STRING)
        self.addField('cdu',STRING)
        self.addField('dmoz',URL)
        self.addField('wikipedia',URL)
        self.addBabelField('url',URL)
        
        self.addView('simple',"name url super children")
        
    class Instance(TreeTable.Instance):
        def __str__(self):
            return self.name
    

class Authors(Persons):
    def init(self):
        self.addField('id',STRING)
        Persons.init(self)
        #self.birthDate = Field(DATE)
        #self.birthPlace = Pointer(City)
        #self.deathDate = Field(DATE)
        #self.deathPlace = Pointer(City)
    class Instance(Persons.Instance):
        pass

class PubByAuth(LinkTable):
    def __init__(self,parent,**kw):
        LinkTable.__init__(self,parent,Publications,Authors,**kw)


class AuthorEvents(BabelTable):
    "Birth, diplom, marriage, death..."
    def init(self):
        BabelTable.init(self)
        self.addField('seq',ROWID)
        self.addPointer('type',AuthorEventTypes)
        self.addPointer('author',Authors)
        self.addField('date',DATE)
        self.addPointer('place',Cities)
        #self.remark = Field(STRING)
        self.setPrimaryKey('author seq')
        
    class Instance(BabelTable.Instance):
        def __str__(self):
            s = str(self.type)
            if self.date is not None:
                s += " " + str(self.date)
            return s
        
class AuthorEventTypes(BabelTable):
    "Birth, diplom, marriage, death..."
    def init(self):
        BabelTable.init(self)
        self.addField('id',ROWID,\
                      doc="the internal id" )
        #self.name = BabelField(STRING)
        

    class Instance(BabelTable.Instance):
        pass

