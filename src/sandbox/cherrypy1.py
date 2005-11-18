# coding: latin1

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

from cStringIO import StringIO
import cherrypy

from cherrypy.lib.cptools import PositionalParametersAware 



from lino.apps.pinboard import demo
#from lino.gendoc.gendoc import WriterDocument
from lino.gendoc.html import HtmlDocument
from lino.forms.base import MenuContainer

from HTMLgen import HTMLgen as html

from lino.console.htmlgen_toolkit import HtmlServer
from lino.console import syscon

def showReport(doc,rpt):
    rpt.setupReport()
    table=html.Table(
        tabletitle=rpt.getTitle(),
        heading=[col.getLabel() for col in rpt.columns])
    print rpt.columns
    for row in rpt:
        l= []
        for col in rpt.columns:
            v=col.getCellValue(row)
            if v is None:
                l.append("&nbsp;")
            else:
                l.append(html.Text(col.format(v)))
        table.body.append(l)
    doc.append(table)


class MyRoot(MenuContainer,PositionalParametersAware):
    def __init__(self,dbsess):
        self.dbsess=dbsess
        self.beginResponse = dbsess.toolkit.beginResponse
        self.endResponse = dbsess.toolkit.endResponse
        
    def index(self):
        doc=self.beginResponse(title="index()")
        doc.append(html.Para("This is the top-level page"))
        return self.endResponse()
    index.exposed=True
    
    def report(self, *args,**kw):
        doc=self.beginResponse(title="report()")
        if len(args) > 0:
            tcl=self.dbsess.getTableClass(args[0])
            if tcl is not None:
                rpt=self.dbsess.getViewReport(tcl,*args[1:],**kw)
                
                showReport(doc,rpt)
                #self.dbsess.showViewGrid(table._instanceClass,
                #                         *args[1:],**kw)
            else:
                doc.append(html.Para(args[0]+" : no such table"))
                
            return self.endResponse()

        list=html.UL()
        for table in self.dbsess.db.app.getTableList():
            p=html.Para()
            p.append(html.Href("report/"+table.getTableName(),
                               table.getTableName()))
            p.append("")
            p.append(str(len(self.dbsess.query(table._instanceClass))))
            list.append(p)
        doc.append(list)
                    
        doc.append(html.Para("This is the report page"))
        doc.append(html.Para("args : " + repr(args)))
        doc.append(html.Para("kw : " + repr(kw)))
        doc.append(html.Para("dbsess : " + repr(self.dbsess)))

        return self.endResponse()

    report.exposed=True
    

    
syscon.setToolkit(HtmlServer())
sess = demo.startup()
cherrypy.root = MyRoot(sess)

cherrypy.server.start()
sess.shutdown()

