## Copyright Luc Saffre 2003-2004.

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

from addrbook import Persons, Cities
#from babel import Language
#from web import MemoMixin, MemoTreeMixin, TreeMixin

class Quotes(MemoTable):
    def init(self):
        MemoTable.init(self)
        self.id = Field(ROWID)
        self.author = Pointer(Authors)
        self.author.setDetail('quotesByAuthor')
        self.lang = Pointer(Languages)
        
        #self.pubRef = Field(STRING)
        #self.pub = Pointer("PUBLICATIONS")
        
    class Instance(MemoTable.Instance):
        def getLabel(self):
            return "[q"+str(self.id)+"]"

class Publications(MemoTreeTable):
    def init(self):
        MemoTreeTable.init(self)
        self.id = Field(ROWID)
        self.year = Field(INT)
        self.subtitle = Field(STRING)
        self.typeRef = Field(STRING)
        self.type = Pointer( PubTypes)
        self.author = Pointer(Authors)
        self.lang = Pointer(Languages)

class PubTypes(BabelTable):
    def init(self):
        self.id = Field(STRING)
        BabelTable.init(self)
        self.typeRefPrefix = Field(STRING)
        self.pubRefLabel = BabelField(STRING)
        

##  def populate(self,area):
##      q = area.query('id name typeRefPrefix pubRefLabel')
##      q.appendRow("book",'Book','ISBN: ','page')
##      q.appendRow("url",'Web Page','http:',None)
##      q.appendRow("cd",'CompactDisc','cddb: ','track')
##      q.appendRow("art",'Article','','page')
##      q.appendRow("mag",'Magazine','','page')
##      q.appendRow("sw",'Software','',None)


class Topics(TreeTable):
    def init(self):
        TreeTable.init(self)
        self.id = Field(ROWID)
        self.name = BabelField(STRING)
        #self.lang = Pointer(Languages)
        self.dewey = Field(STRING)
        self.cdu = Field(STRING)
        self.dmoz = Field(URL)
        self.wikipedia = Field(URL)
        self.url = BabelField(URL)
        self.addView('simple',"name url super children")
        
    class Instance(TreeTable.Instance):
        def getLabel(self):
            return self.name
    

class Authors(Persons):
    def init(self):
        self.id = Field(STRING)
        Persons.init(self)
        #self.birthDate = Field(DATE)
        #self.birthPlace = Pointer(City)
        #self.deathDate = Field(DATE)
        #self.deathPlace = Pointer(City)
    class Instance(Persons.Instance):
        pass

class PubByAuth(LinkTable):
    def __init__(self,**kw):
        LinkTable.__init__(self,Publications,Authors,**kw)


class AuthorEvents(BabelTable):
    "Birth, diplom, marriage, death..."
    def init(self):
        BabelTable.init(self)
        self.seq = Field(ROWID)
        self.type = Pointer(AuthorEventTypes)
        self.author = Pointer(Authors)
        self.date = Field(DATE)
        self.place = Pointer(Cities)
        #self.remark = Field(STRING)
        self.setPrimaryKey('author seq')
        
    class Instance(BabelTable.Instance):
        def getLabel(self):
            s = self.type.getLabel()
            if self.date is not None:
                s += " " + str(self.date)
            return s
        
class AuthorEventTypes(BabelTable):
    "Birth, diplom, marriage, death..."
    def init(self):
        BabelTable.init(self)
        self.id = Field(ROWID,\
                          doc="the internal" )
        #self.name = BabelField(STRING)
        

    class Instance(BabelTable.Instance):
        pass
