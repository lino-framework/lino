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


import cherrypy
from cherrypy.lib.cptools import PositionalParametersAware 
from HyperText import HTML as html
from lino.apps.pinboard import pinboard_demo 
from lino.console.htmlgen_toolkit import HtmlServer
from lino.console import syscon
from lino.reports.reports import Report

def text2html(s):
    s2=""
    for c in s:
        o=ord(c)
        if o <= 127:
            s2 += c
        else:
            s2 += '&#%d;' % o
    return s2
    

def showReport(doc,rpt):
    rpt.setupReport()
    table=html.TABLE(title=rpt.getTitle()); doc.append(table)
    
    tr=html.TR(); table.append(tr)
    for col in rpt.columns:
        tr.append(html.TH(col.getLabel()))
    
    for row in rpt:
        tr=html.TR() ; table.append(tr)
        for col in rpt.columns:
            v=col.getCellValue(row)
            if v is None:
                tr.append(html.TD("&nbsp;"))
            else:
                s=text2html(col.format(v).decode())
                tr.append(html.TD(s))
    





class MyRoot(PositionalParametersAware):
    def __init__(self,dbsess):
        self.dbsess=dbsess
        self.beginResponse = dbsess.toolkit.beginResponse
        self.endResponse = dbsess.toolkit.endResponse
        
    def index(self):
        doc=self.beginResponse(title="index()")
        doc.append(html.P("This is the top-level page"))
        return self.endResponse()
    index.exposed=True
    
    def report(self, *args,**kw):
        doc=self.beginResponse(title="report()")
        if len(args) > 0:
            tcl=self.dbsess.getTableClass(args[0])
            if tcl is not None:
                rpt=self.dbsess.getViewReport(tcl,*args[1:],**kw)
                showReport(doc,rpt)
            else:
                doc.append(html.P(args[0]+" : no such table"))
                
            return self.endResponse()
        list=html.UL(); doc.append(list)
        for table in self.dbsess.db.app.getTableList():
            li=html.LI() ; list.append(li)
            li.append(html.A(table.getLabel(),
                             href="report/"+table.getTableName()))
            li.append(" (%d rows)" %
                len(self.dbsess.query(table._instanceClass)))

        return self.endResponse()

    report.exposed=True
    

    
syscon.setToolkit(HtmlServer())
sess = pinboard_demo.startup()
cherrypy.root = MyRoot(sess)

cherrypy.server.start()
sess.shutdown()

