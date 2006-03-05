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
#from lino.apps.pinboard.babel import Language

from lino.apps.pinboard.tables import Person, City, Language

class Quote(StoredDataRow):
    tableName="Quotes"
    def initTable(self,table):
        #MemoTable.init(self)
        table.addField('id',ROWID)
        table.addField('quote',MEMO)
        table.addPointer('author',Author).setDetail('quotesByAuthor')
        table.addPointer('lang',Language)
        #table.addField('lang',LANG)
        
        #self.pubRef = Field(STRING)
        #self.pub = Pointer("PUBLICATIONS")
        
    def __str__(self):
        return "[q"+str(self.id)+"]"

class QuotesReport(DataReport):
    leadTable=Quote


class Publication(MemoTreeRow):
    tableName="Publications"
    def initTable(self,table):
        MemoTreeRow.initTable(self,table)
        table.addField('id',ROWID)
        table.addField('pubYear',INT)
        table.addField('subtitle',STRING)
        table.addField('typeRef',STRING)
        table.addPointer('pubType', PubType)
        table.addPointer('author',Author)
        table.addPointer('lang',Language)
        #table.addField('lang',LANG)
        table.addField('url',URL)

class PublicationsReport(DataReport):
    leadTable=Publication

class PubType(BabelRow):
    tableName="PubTypes"
    def initTable(self,table):
        table.addField('id',STRING)
        BabelRow.initTable(self,table)
        table.addField('typeRefPrefix',STRING)
        table.addBabelField('pubRefLabel',STRING)
        
class PubTypesReport(DataReport):
    leadTable=PubType

class Topic(TreeRow):
    tableName="Topics"
    def initTable(self,table):
        TreeRow.initTable(self,table)
        table.addField('id',ROWID)
        table.addBabelField('name',STRING)
        #table.addPointer('lang',Language)
        table.addField('dewey',STRING)
        table.addField('cdu',STRING)
        table.addField('dmoz',URL)
        table.addField('wikipedia',URL)
        table.addBabelField('url',URL)
        
        #table.addView('simple',"name url super children")
        
    def __str__(self):
        return self.name
    
class TopicsReport(DataReport):
    leadTable=Topic
    columnNames="name url super children"


class Author(Person):
    tableName="Authors"
    
    def initTable(self,table):
        Person.initTable(self,table)
        table.addDetail('quotesByAuthor',Quote,'author')
    
##     def quotesByAuthor(self,*args,**kw):
##         kw['author']=self
##         return self.detail(Quote,*args,**kw)

class AuthorsReport(DataReport):
    leadTable=Author
    


class PubAuthor(LinkingRow):
    tableName="PubAuthors"
    fromClass=Publication
    toClass=Author
    
##     def __init__(self,parent,**kw):
##         LinkingRow.__init__(self,parent,Publication,Author,**kw)
    
class PubAuthorsReport(DataReport):
    leadTable=PubAuthor
    


class AuthorEvent(BabelRow):
    "Birth, diplom, marriage, death..."
    tableName="AuthorEvents"
    def initTable(self,table):
        BabelRow.initTable(self,table)
        table.addField('seq',ROWID)
        table.addPointer('aetype',AuthorEventType)
        table.addPointer('author',Author)
        table.addField('aedate',DATE)
        table.addPointer('place',City)
        table.setPrimaryKey('author seq')
        
    def __str__(self):
        s = str(self.type)
        if self.date is not None:
            s += " " + str(self.date)
        return s
        
class AuthorEventsReport(DataReport):
    leadTable=AuthorEvent
    
class AuthorEventType(BabelRow):
    "Birth, diplom, marriage, death..."
    tableName="AuthorEventTypes"
    def initTable(self,table):
        BabelRow.initTable(self,table)
        table.addField('id',ROWID,\
                      doc="the internal id" )
        #self.name = BabelField(STRING)
        

class AuthorEventTypesReport(DataReport):
    leadTable=AuthorEventType
    
