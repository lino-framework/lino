## Copyright Luc Saffre 2003-2005

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
"""
"""

from lino.adamo.ddl import *

from babel import Languages
from web import Pages
from lino.schemas.sprl.addrbook import Users
from projects import Projects

class News(MemoTable):
    
    def init(self):
        MemoTable.init(self)
        self.addField('id',ROWID)
        self.addField('date',DATE)
        self.addPointer('newsgroup',Newsgroups).setDetail(
            'newsByGroup', orderBy='date')
        self.addPointer('author',Users).setDetail('newsByAuthor')
        self.addPointer('lang',Languages)
        self.addPointer('project',Projects)
        self.addPointer('page',Pages)

        #self.writeParagraph = Vurt(self.Instance.writeParagraph,MEMO)

        #table.setColumnList('date title newsgroup abstract id lang')
        self.setOrderBy("date")
        self.addView("simple","date title abstract",
                         orderBy="date")
        self.addView("list","date writeParagraph",
                         orderBy="date")
        
    class Instance(MemoTable.Instance):
        def __str__(self):
            s = str(self.date)
            if self.newsgroup is not None:
                s += ' (%s)' % self.newsgroup
            if self.title:
                s += " " + self.title
            return s
    
class Newsgroups(Table):
    def init(self):
        self.addField('id',STRING)
        self.addField('name',STRING).setMandatory()
        
    class Instance(Table.Instance):
        def __str__(self):
            return self.name
        
##  def asPage(self,renderer):
##      body = ''
##      newsByGroup = NEWS
