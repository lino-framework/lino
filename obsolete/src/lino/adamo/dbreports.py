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

from lino.reports import Report, BaseReport, ReportColumn, RIGHT
from lino.reports.reports import ReportRow
from lino.adamo.datatypes import INT
from lino.adamo.rowattrs import Field, Pointer, Detail

class DataReportColumn(ReportColumn):
    def __init__(self,datacol,
                 name=None,label=None,doc=None,
                 formatter=None,
                 selector=None,
                 **kw):
        if name is None: name=datacol.name
        if formatter is None: formatter=datacol.format
        #if selector is None: selector=datacol.showSelector
        #assert name != "DataReportColumn"
        if label is None: label=datacol.rowAttr.label
        if doc is None: label=datacol.rowAttr.doc
        ReportColumn.__init__(self,
                              formatter,selector,
                              name,label,doc,
                              **kw)
        #assert self.name != "DataReportColumn"
        self.datacol = datacol

    def getCellValue(self,row):
        return self.datacol.getCellValue(row.item)
    
    def setCellValue(self,row,value):
        #print "dbreports:setCellValue()",row.item,value
        self.datacol.setCellValue(row.item,value)
        row.values[self.index]=value
        #print row.item

    def getMinWidth(self):
        return self.datacol.getMinWidth()
    def getMaxWidth(self):
        return self.datacol.getMaxWidth()

##     def addFilter(self,*args):
##         self.datacol.addFilter(*args)
        
    def isMandatory(self):
        return self.datacol.isMandatory()
    
    def canWrite(self,row):
        if row is None:
            return self.datacol.canWrite(None)
        return self.datacol.canWrite(row.item)
    
    def validate(self,value):
        return self.datacol.rowAttr.validate(value)
    
    def parse(self,s):
        return self.datacol.parse(s)

    def getType(self):
        #return self.datacol.rowAttr.getType()
        return self.datacol.rowAttr.type
    
    #def format(self,v):
    #    return self.formatter(v)
        #return self.datacol.format(v)
    


class DataReportRow(ReportRow):
    def lock(self):
        ReportRow.lock(self)
        self.item.lock()
        
    def unlock(self):
        self.item.unlock()
        ReportRow.unlock(self)

    def printRow(self,doc):
        doc.body.h1(self.item.getLabel())
        t=doc.body.table()
        for col,s in self.cells():
            t.addrow( col.getLabel(), s )
            
        
        #doc.report(RowFormReport(self))
            
        

class QueryReport(BaseReport):
    rowClass=DataReportRow
    def __init__(self,qry,
                 columnSpec=None,
                 columnWidths=None,
                 width=None,rowHeight=None,
                 title=None,
                 #name=None,label=None,doc=None,
                 **kw):
        
        if len(kw):
            """forward unknown keyword arguments to the query"""
            qry=qry.child(**kw)

        self.query=qry
            
        BaseReport.__init__(self,None,
                            columnWidths,width,rowHeight,
                            title=title)
                            #name=name,label=label,doc=doc)
            
        if columnSpec is not None:
            self.setColumnSpec(columnSpec)
            
    def getIterator(self):
        return self.query
    
    def __xml__(self,wr):
        return self.query.__xml__(wr)
    
##     def onClose(self):
##         BaseReport.onClose(self)
##         self.query.unlock()
        
    def getTitle(self):
        "may override"
        if self.title is not None: return self.title
        return self.query.buildTitle()
    
    def setupMenu(self,frm):
        "may override"
        self.query.setupMenu(frm)

    def setupReport(self):
        "may override"
        if len(self.columns) == 0:
            for dc in self.query.getVisibleColumns():
                col = DataReportColumn(dc,label=dc.getLabel())
                self.add_column(col)
            self.formColumnGroups=None
        
    def addDataColumn(self,colName,**kw):
        dc=self.query.findColumn(colName)
        return self.add_column(DataReportColumn(dc,**kw))

##     def doesShow(self,qry):
##         #used in lino.gendoc.html
##         raise "is this necessary?"
##         myqry=self.query
##         if myqry.getLeadTable().name != qry.getLeadTable().name:
##             return False
##         #if myqry._masters != qry._masters:
##         #    return False
##         return True

    def canSort(self):
        return True

    def createRow(self,index):
        row=self.query.appendRowForEditing()
        #print "dbreports createRow()",row
        return self.rowClass(self,row,index)

    def setOrderBy(self,*args,**kw):
        return self.query.setOrderBy(*args,**kw)

    def setColumnSpec(self,columnSpec):
        assert type(columnSpec) in (str,unicode) 
        #l = []
        groups = []
        for ln in columnSpec.splitlines():
            grp=[]
            for colName in ln.split():
                x = colName.split(':')
                if len(x) == 1:
                    w=None
                elif len(x) == 2:
                    colName=x[0]
                    w=int(x[1])
                if colName == "*":
                    for datacol in self.query.getColumns():
                    #for fld in self.ds.getLeadTable().getFields():
                    #    datacol = self.ds.findColumn(fld.getName())
                    #    if datacol is None:
                    #        datacol = self.ds._addColumn(
                    #            fld.getName(),fld)
                        col=DataReportColumn(datacol,width=w)
                        self.add_column(col)
                        grp.append(col)
                else:
                    dc=self.query.provideColumn(colName)
                    col=DataReportColumn(dc,width=w)
                    self.add_column(col)
                    grp.append(col)
            #l += grp
            groups.append(tuple(grp))
        #self.visibleColumns = tuple(l)
        if len(groups) <= 1:
            self.formColumnGroups = None
        else:
            self.formColumnGroups = tuple(groups)



class DatabaseOverview(Report):
    # originally copied from sprl1.py
    def __init__(self,dbsess):
        self.dbsess=dbsess
        Report.__init__(self)
        
    def setupRow(self,row):
        row.qry=self.dbsess.query(row.item._instanceClass)
        
    def getIterator(self):
        return self.dbsess.db.schema.getTableList()
        
    def setupReport(self):
        self.addVurtColumn(
            label="TableName",
            meth=lambda row: row.item.getTableName(),
            width=20)
        self.addVurtColumn(
            label="Count",
            meth=lambda row: len(row.qry),
            datatype=INT,
            width=5, halign=RIGHT
            )
        self.addVurtColumn(
            label="First",
            meth=lambda row: unicode(row.qry[0]),
            when=lambda row: len(row.qry)>0,
            width=20)
        self.addVurtColumn(
            label="Last",
            meth=lambda row: unicode(row.qry[-1]),
            when=lambda row: len(row.qry)>0,
            width=20)


class SchemaOverview(Report):
    def __init__(self,schema):
        self.schema=schema
        Report.__init__(self)
        
    def getIterator(self):
        return self.schema.getTableList()
        
    def setupReport(self):

        self.addVurtColumn(
            label="TableName",
            meth=lambda row: row.item.getTableName(),
            width=15)
        self.addVurtColumn(
            label="Fields",
            meth=lambda row:\
            ", ".join([fld.name for fld in row.item.getFields()
                       if isinstance(fld,Field) \
                       and not isinstance(fld,Pointer)]),
            width=20)
        self.addVurtColumn(
            label="Pointers",
            meth=lambda row:\
            ", ".join([fld.name for fld in row.item.getFields()
                       if isinstance(fld,Pointer)]),
            width=13)
        self.addVurtColumn(
            label="Details",
            meth=lambda row:\
            ", ".join([fld.name for fld in row.item.getFields()
                       if isinstance(fld,Detail)]),
            width=20)


            
            
            
from lino.adamo.query import Query

class DataReport(QueryReport):
    
    leadTable=None
    columnNames=None
    columnSpec=None
    columnWidths=None
    orderBy=None
    pageLen=None
    masters={}
    masterColumns=None
    
    def __init__(self,dataProvider):
        if isinstance(dataProvider,Query):
            q=dataProvider.child(
                orderBy=self.orderBy,
                columnNames=self.columnNames,
                masterColumns=self.masterColumns,
                pageLen=self.pageLen
                **self.masters)
            assert q.getLeadTable().__class__ is self.leadTable
        else:
            q=dataProvider.query(
                self.leadTable,
                orderBy=self.orderBy,
                columnNames=self.columnNames,
                pageLen=self.pageLen,
                **self.masters)
        QueryReport.__init__(self,q,columnSpec=self.columnSpec)
        
            


## class RowFormReport(Report):
##     """Print the content of a ReportRow as a table.
##     """
##     def __init__(self,row,**kw):
##         self.row=row
##         Report.__init__(self,**kw)
        
##     def setupReport(self):
##         for col in self.row.rpt.columns:
##             self.addVurtColumn(lambda cell: cell.col.getLabel(),
##                                width=20,
##                                label="fieldName")
##             self.addVurtColumn(lambda cell: str(cell),
##                                width=50,
##                                label="value")
            
##         for c in self.row:
##             self.addColumn(lambda cell: cell.col.getLabel(),
##                            width=20,
##                            label="fieldName")
##             self.addColumn(lambda cell: str(cell),
##                            width=50,
##                            label="value")
