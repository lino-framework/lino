#coding: latin1
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

from lino.forms import gui

from lino.apps.timings.tables import *
from lino.apps.timings.tables import TABLES
from lino.adamo.ddl import Schema

from lino.gendoc.html import HtmlDocument
from lino.reports.reports import DataReport


class Timings(Schema):
    #name="Lino/Timings"
    years='2005'
    author="Luc Saffre"
    htmlRoot="gendoc_html"
    
    tables = TABLES

    def writeStaticSite(self,sess):
        if not sess.confirm("Generate HTML in %s" % self.htmlRoot):
            return
        files = self._writeStaticSite(sess,self.htmlRoot)
        sess.notice("%d files have been generated",len(files))
        
        
    def _writeStaticSite(self,sess,targetRoot):
        root = HtmlDocument(title="Timings",
                            stylesheet="wp-admin.css")

        root.addResolver(Resources, lambda x: x.id.strip())
        root.addResolver(UsageTypes, lambda x: x.id.strip())
        root.addResolver(Usages, lambda x: str(x.date))
        root.addResolver(Days, lambda x: str(x.date))

##         def query2name(q):
##             if q.getLeadTable().__class__ == Resources:
##                 return "resources"
##         root.addResolver(Query, query2name)
##         root.addResolver(
##             Days,
##             lambda x: str(x.date.year)+str(x.date.month)
        
        

        mnu = root.addMenu()

        
        ds = sess.query(Resources,
                        pageLen=50,
                        orderBy="name")
        rpt = DataReport(ds)
        doc=root.addChild(location="resources",
                          name=rpt.name,
                          title=rpt.getLabel())
        doc.report(rpt)
        mnu.addLink(doc)
        
            
        
        ds = sess.query(UsageTypes,
                        pageLen=50,
                        orderBy="id")
        rpt = DataReport(ds)
        doc=root.addChild(location="usagetypes",
                          name=rpt.name,
                          title=rpt.getLabel())
        doc.report(rpt)
        mnu.addLink(doc)
        
        ds = sess.query(Days,
                        pageLen=50,
                        orderBy="date")
        rpt = DataReport(ds)
        doc=root.addChild(location="days",
                          name=rpt.name,
                          title=rpt.getLabel())
        doc.report(rpt)
        mnu.addLink(doc)

        filenames=root.save(sess,targetRoot)

        from lino.gendoc.html import DataRowElement
        
        for cl in (Resources, UsageTypes, Days):
            rs=root.findResolver(cl)
            for x in sess.query(cl):
                ch=root.__class__(parent=root,
                                  name=rs.i2name(x),
                                  title=x.getLabel(),
                                  content=DataRowElement(x))
                filenames += ch.save(sess,targetRoot)
        
        

        return filenames
        

    def showMainForm(self,sess):
        frm = sess.form(
            label="Main menu",
            doc="""\
This is the Timings main menu.                                     
"""+("\n"*10))

        m = frm.addMenu("db","&Datenbank")
        m.addItem("resources",label="&Resources").setHandler(
            sess.showTableGrid, Resources)
        m.addItem("usages",label="&Usages").setHandler(
            sess.showTableGrid, Usages)
        m.addItem("usageTypes",label="Usage &Types").setHandler(
            sess.showTableGrid, UsageTypes)
        
        m = frm.addMenu("reports","&Reports")
        m.addItem("s",label="&Static HTML").setHandler(
            self.writeStaticSite,sess)
        
        self.addProgramMenu(sess,frm)

        frm.addOnClose(sess.close)

        frm.show()


if __name__ == '__main__':
    app=Timings()
    app.quickStartup()
    #app.main()
    gui.run(app)
