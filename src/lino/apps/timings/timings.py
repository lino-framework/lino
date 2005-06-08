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
from lino.adamo.filters import DateEquals
from lino.adamo.datatypes import itod

from lino.gendoc.html import HtmlDocument
from lino.reports.reports import DataReport, ReportColumn

import datetime

DAY = datetime.timedelta(1)

## def everyday(d1,d2):
##     l=[]
##     d=d1
##     while d <= d2:
##         l.append(d)
##         d += DAY
##     return l

def everyday(d1,d2):
    #return xrange(itod(d1),itod(d2),DAY)
    return urange(itod(d1),itod(d2),DAY)

class urange:

    def __init__(self, start, stop, step=DAY):
        self.start = start
        self.stop = stop
        self.step = step
        
    def __contains__(self, obj):
        return self.start <= obj <= self.stop

    def __iter__(self):
        return uiter(self)

class uiter:
    def __init__(self,rng):
        self.rng=rng
        self.current=None # rng.start

    def __iter__(self):
        return self
    
    def next(self):
        if self.current is None:
            self.current = self.rng.start
        else:
            self.current += self.rng.step
        if self.current > self.rng.stop:
            raise StopIteration
        return self.current

def iif(test,x,y):
    if test: return x
    return y
        
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

        root.addResolver(
            Resources,
            lambda row: "resources/"+row.id.strip()
            )
        root.addResolver(
            UsageTypes, lambda x: "types/"+x.id.strip()
            )
        root.addResolver(
            Usages, lambda x: "days/"+str(x.date)
            )
        root.addResolver(
            Days, lambda x: "days/"+str(x.date)
            )

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
        doc=root.addReportChild(rpt)
        mnu.addLink(doc)
        
            
        
        ds = sess.query(UsageTypes,
                        pageLen=50,
                        orderBy="id")
        rpt = DataReport(ds)
        doc=root.addReportChild(rpt)
        mnu.addLink(doc)
        
        ds = sess.query(Days,
                        pageLen=50,
                        orderBy="date")
        rpt = DataReport(ds)
        doc=root.addReportChild(rpt)
        mnu.addLink(doc)

        for r in sess.query(Resources):
            root.addReportChild(DataReport(
                r.usages_by_resource,orderBy="date start"))

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

    def writeMonthCalendar(self,sess,year=2005,month=6):
        ds=sess.query(Days, orderBy="date")
        def fmt(d):
            return "["+str(d)+"]" # "%d-%d-%d"
        rpt = DataReport(ds)
        rpt.addDataColumn("date",formatter=fmt).addFilter(
            DateEquals,year,month)
        
        rpt.addVurtColumn(lambda row:str(row.item.date),
                      label="ISO")

        class ResourceColumn(ReportColumn):
            def __init__(self,owner,res):
                self.res=res
                ReportColumn.__init__(self,owner,
                                      width=10,
                                      label=res.getLabel())
            def getValue(self,row):
                return self.res.usages_by_resource.child(
                    date=row.item)
            def format(self,qry):
                return ", ".join([u.short() for u in qry])
        
        for res in sess.query(Resources,orderBy="id"):
##             def val(row):
##                 #qry=sess.query(Usages,
##                 #               date=row.cells[0].value,
##                 #               resource=res)
##                 return res.usages_by_resource.child(
##                     date=row.cells[0].value)
##                 #print qry.getSqlSelect()
##                 #return qry.lister
##             def fmt(qry):
##                 return ", ".join([u.short() for u in qry])
##             rpt.addColumn(val,
##                           label=res.getLabel(),
##                           formatter=fmt)
##             rpt.addColumn(val,
            rpt.addColumn(ResourceColumn(rpt,res))

        sess.report(rpt)
        

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
