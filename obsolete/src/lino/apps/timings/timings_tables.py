## Copyright 2005-2006 Luc Saffre 

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

import os
import datetime

from lino.tools.anyrange import anyrange
from lino.adamo.datatypes import itod, iif

from lino.reports.reports import ReportColumn
#from lino.adamo.dbreports import DataReport

from lino.adamo.ddl import *
from lino.adamo.filters import DateEquals

from lino.gendoc.html_site import HtmlDocument
from lino.gendoc.html_site import DataRowElement



DAY = datetime.timedelta(1)

def everyday(d1,d2):
    return anyrange(itod(d1),itod(d2),DAY)


class Resource(StoredDataRow):
    tableName="Resources"
    def initTable(self,table):
        table.addField('id',STRING) 
        table.addField('name',STRING)
        #table.addView("std", "id name")
        table.addDetail('usages_by_resource',Usage,'resource')
        

    def setupMenu(self,nav):
        frm = nav.getForm()
        m = frm.addMenu("&Resource")
        def f():
            res = nav.getCurrentRow()
            frm.session.showTableGrid(res.usages)
            
        m.addItem("detail",
                  label="&Usages",
                  action=f,
                  accel="ENTER")

    def __str__(self):
        if self.name is not None: return self.name
        return self.id

    def delete(self):
        self.usages.deleteAll()

##     def usages_by_resource(self,*args,**kw):
##         kw['resource']=self
##         return self.detail(Usage,*args,**kw)

class ResourcesReport(DataReport):
    leadTable=Resource
    columnNames="id name"

            
        
class Usage(StoredDataRow):
    tableName="Usages"
    def initTable(self,table):
        table.addField('id',ROWID) 
        table.addPointer('date',Day).setMandatory()
        table.addField('start',TIME)
        table.addField('stop',TIME)
        table.addPointer('type',UsageType)
        table.addField('remark',STRING)
        #table.addField('mtime',TIMESTAMP)
        table.addPointer('resource',Resource).setMandatory()
        #table.addView("std", "id date start stop type remark")

    def __str__(self):
        s=""
        if self.remark is not None:
            s+=self.remark+" "
        if self.type is not None:
            s+= self.type.id + " "
        if self.start is None and self.stop is None:
            return s
        s += " %s-%s" % (self.start,self.stop)
        return s

        
class UsagesReport(DataReport):
    leadTable=Usage
    columnNames="id date start stop type remark"


class UsageType(StoredDataRow):
    tableName="UsageTypes"
    def initTable(self,table):
        table.addField('id',STRING(width=2))
        table.addField('name',STRING)
        #table.addView("std", "id name")

    def __str__(self):
        return self.name
        
class UsageTypesReport(DataReport):
    leadTable=UsageType
    columnNames="id name"

class Day(StoredDataRow):
    tableName="Days"
    def initTable(self,table):
        table.addField('date',DATE)
        table.addField('remark',STRING)
        table.setPrimaryKey("date")
        #table.addView("std", "date remark")
        
    def __str__(self):
        return str(self.date)

class DaysReport(DataReport):
    leadTable=Day
    columnNames="date remark"



class MonthlyCalendar(DataReport):
    
    leadTable=Day
    orderBy="date"
    
    def __init__(self,dbsess,year=2005, month=6):
        DataReport.__init__(self,dbsess)
        self.year=year
        self.month=month

    def setupReport(self,*args,**kw):
        sess=self.query.getContext()

        self.query.addFilter(
            DateEquals(self.query.findColumn('date'),
                       self.year,self.month))
        def fmt(d):
            return "["+str(d)+"]" # "%d-%d-%d"
        self.addDataColumn("date",width=12,formatter=fmt)
        
        self.addVurtColumn(lambda row:str(row.item.date),
                           label="ISO",width=10)

        class ResourceColumn(ReportColumn):
            def __init__(self,res):
                self.res=res
                ReportColumn.__init__(self,label=str(res))
            def getCellValue(self,row):
                return self.res.usages_by_resource(date=row.item)
            def format(self,qry):
                return ", ".join([str(u) for u in qry])
        
        for res in sess.query(Resource,orderBy="id"):
            self.addColumn(ResourceColumn(res))


    

class TimingsSchema(Schema):
    tableClasses=(
        Day,
        UsageType,
        Resource,
        Usage,
        )

class TimingsMainForm(DbMainForm):

    schemaClass=TimingsSchema
    
    def layout(self,panel):
        panel.label("""
    
Welcome to Timings, a Lino application to to manage your resources and
their usage.

Warning: This application is not stable and there are no known users.

        """)


    def setupMenu(self):
        m = frm.addMenu("db","&Datenbank")

        m.addReportItem("resources",ResourcesReport,
                        label="&Resources")
        
        m.addReportItem("usages",UsagesReport,
                        label="&Usages")
        
        m.addReportItem("usageTypes",UsageTypesReport,
                        label="Usage &Types")
        
        m = frm.addMenu("reports","&Reports")
        m.addItem("s",label="&Static HTML").setHandler(
            self.writeStaticSite,sess)
        m.addReportItem("monthly",MonthlyCalendar,
                        label="&Monthly Calendar")
        
        self.addProgramMenu()


class Timings(DbApplication):
    #name="Lino/Timings"
    years='2005-2006'
    author="Luc Saffre"
    htmlRoot="gendoc_html"
    mainFormClass=TimingsMainForm
    
    def writeStaticSite(self,sess):
        if not sess.confirm("Generate HTML in %s" % self.htmlRoot):
            return
        files = self._writeStaticSite(sess,self.htmlRoot)
        sess.notice("%d files have been generated",len(files))
        
        
    def _writeStaticSite(self,sess,targetRoot):
        root = HtmlDocument(title="Timings",
                            stylesheet="wp-admin.css")

        root.site.addResolver(
            tables.Resource,
            lambda x: "resources/"+x.id.strip()
            )
        root.site.addResolver(
            tables.UsageType, lambda x: "types/"+x.id.strip()
            )
        root.site.addResolver(
            tables.Usage, lambda x: "usages/"+str(x.date)
            )
        root.site.addResolver(
            tables.Day, lambda x: "days/"+str(x.date)
            )


        mnu = root.addMenu()

        class ResourcesReport(tables.ResourcesReport):
            pageLen=50
        ds = sess.query(tables.Resource,
                        pageLen=50,
                        orderBy="name")
        rpt = DataReport(ds)
        doc=root.addReportChild(rpt)
        mnu.addLink(doc)
        
            
        
        ds = sess.query(tables.UsageType,
                        pageLen=50,
                        orderBy="id")
        rpt = DataReport(ds)
        doc=root.addReportChild(rpt)
        mnu.addLink(doc)
        
        
        ds = sess.query(tables.Day,
                        pageLen=50,
                        orderBy="date")
        rpt = DataReport(ds)
        doc=root.addReportChild(rpt)
        mnu.addLink(doc)

        for r in sess.query(tables.Resource):
            rpt=DataReport(r.usages_by_resource(orderBy="date start"))
            root.addReportChild(rpt)

        filenames=root.save(sess,targetRoot)

        
        for cl in (tables.Resource, UsageType, Usage, Day):
            rs=root.site.findResolver(cl)
            for x in sess.query(cl):
                ch=root.__class__(parent=root,
                                  name=rs.i2name(x),
                                  title=str(x),
                                  content=DataRowElement(x))
                filenames += ch.save(sess,targetRoot)

        return filenames
    

##     def showMonthlyCalendar(self,sess,year=2005,month=6):
##         ds=sess.query(Day, orderBy="date")
##         ds.addFilter(DateEquals(ds.findColumn('date'),year,month))
##         rpt = DataReport(ds)
        
##         def fmt(d):
##             return "["+str(d)+"]" # "%d-%d-%d"
##         rpt.addDataColumn("date",width=12,formatter=fmt)
        
##         rpt.addVurtColumn(lambda row:str(row.item.date),
##                           label="ISO",width=10)

##         class ResourceColumn(ReportColumn):
##             def __init__(self,res):
##                 self.res=res
##                 ReportColumn.__init__(self,label=str(res))
##             def getCellValue(self,row):
##                 return self.res.usages_by_resource.child(
##                     date=row.item)
##             def format(self,qry):
##                 return ", ".join([str(u) for u in qry])
        
##         for res in sess.query(Resource,orderBy="id"):
##             rpt.addColumn(ResourceColumn(res))

##         sess.showReport(rpt)
##         #sess.report(rpt)
        


    

__all__ = [t.__name__ for t in TimingsSchema.tableClasses]
__all__.append('TimingsSchema')
__all__.append('Timings')

