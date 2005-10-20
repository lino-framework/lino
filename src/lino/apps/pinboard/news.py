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

from lino.adamo import ddl # import *

from babel import Language
from web import Node
from lino.apps.addrbook.tables import User
from projects import Project

class NewsItem(ddl.MemoRow):
    tableName="News"
    def initTable(self,table):
        ddl.MemoRow.initTable(self,table)
        table.addField('id',ddl.ROWID)
        table.addField('date',ddl.DATE)
        table.addField('time',ddl.TIME)
        table.addPointer('newsgroup',Newsgroup).setDetail(
            'newsByGroup', orderBy='date')
        table.addPointer('author',User).setDetail('newsByAuthor')
        table.addPointer('lang',Language)
        #table.addField('lang',LANG)
        table.addPointer('project',Project)
        table.addPointer('node',Node)

        #self.writeParagraph = Vurt(self.Instance.writeParagraph,MEMO)

        #table.setColumnList('date title newsgroup abstract id lang')
        #table.setOrderBy("date")
        table.addView("std","date title abstract",
                     orderBy="date")
        table.addView("list","date writeParagraph",
                         orderBy="date")
        
    def __str__(self):
        s = str(self.date)
        if self.newsgroup is not None:
            s += ' (%s)' % self.newsgroup
        if self.title:
            s += " " + self.title
        return s
    
class Newsgroup(ddl.StoredDataRow):
    tableName="Newsgroups"
    def initTable(self,table):
        table.addField('id',ddl.STRING)
        table.addField('name',ddl.STRING).setMandatory()
        
        table.addView("std","id name")
        
    def __str__(self):
        return self.name
        
##  def asPage(self,renderer):
##      body = ''
##      newsByGroup = NEWS
