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

#from babel import Language
import pinboard_tables as tables

        
#   def getChildren(self):
#       return self._area.instances( orderBy='seq',
#                                             samples={'super':self})

class Node(MemoTreeRow):
    #tableName="WebPages"
    tableName="Nodes"
    def initTable(self,table):
        MemoTreeRow.initTable(self,table)
        table.addField('id',ROWID)
        table.addField('created',DATE)
        table.addField('modified',DATE)
        table.addPointer('author',tables.User)
        table.addPointer('lang',tables.Language)
        #table.addField('lang',LANG)
        table.addField('match',STRING)
        table.addField('subtitle',STRING)
        
        #self.addField('pubRef',STRING)
        #table.addPointer("pub","PUBLICATIONS")

        #rpt = table.provideReport()
        #table.setColumnList('title abstract id created lang')
        #rpt.setLabel('Pages')

##         table.addView(
##             'std',
##             "title subtitle match created id modified author lang")

class NodesReport(DataReport):
    leadTable=Node
    columnNames="title subtitle match created id modified author lang"

    
##  def validate(self):
##      if self.match is not None:
##          pass


##  def __html__(self,renderer,request,fmt):
##      if fmt == renderer.FMT_PAGE:
            
##          #body += "<p>"
##          #body += memo2html(row.body)

##          body += "<ul>"
##          for child in self.children(orderBy="seq").instances():
                
##              body += '<li>' + renderer.renderLink(
##                  url=renderer.rowUrl(child),
##                  label=child.getLabel())
##              body += renderer.memo2html(child.abstract)
##              body += "</li>"
##          body += "</ul>"
##          return body
        
##      return renderer.renderLink(url=renderer.rowUrl(self),
##                                          label=self.getLabel())
        
            
## class Page2Page(StoredDataRow):
##     def initTable(self,table):
##         table.addField('seq',ROWID)
        
##         table.setPrimaryKey(tuple())
