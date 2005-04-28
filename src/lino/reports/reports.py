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


#import copy

from lino.misc.descr import Describable
from lino.adamo.datatypes import STRING

class ConfigError(Exception):
    pass

LEFT = 1
RIGHT = 2
CENTER = 3
TOP = 4
BOTTOM = 5
    
class Report(Describable):


    DEFAULT_TYPE = STRING
    
    def __init__(self, iterator,
                 columnWidths=None,
                 width=None,
                 rowHeight=None,
                 name=None,
                 label=None,
                 doc=None):

        self.columns = []
        self.groups = []
        self.totals = []
        self._onRowEvents=[]
        
        self.iterator = iterator

        self.rowHeight = rowHeight
        self.columnWidths = columnWidths
        self.width = width
        
        Describable.__init__(self,name,label,doc)

##     def setdefaults(self,kw):
##         kw.setdefault('columnNames',self.columnNames)
##         kw.setdefault('columnWidths',self.columnWidths)
##         kw.setdefault('rowHeight',self.rowHeight)
##         #self.ds.setdefaults(self,kw)

    def child(self,
              iterator=None,
              columnWidths=None,
              width=None,
              rowHeight=None,
              name=None,
              label=None,
              doc=None,
              **kw):
        
        if iterator is None:
            if len(kw):
                iterator=self.iterator.child(**kw)
            else:
                iterator=self.iterator
        else:
            assert len(kw) == 0
            
        if columnWidths is None: columnWidths=self.columnWidths
        if width is None: width=self.width
        if rowHeight is None: rowHeight=self.rowHeight
        if name is None: name=self.name
        if label is None: label=self.label
        if doc is None: doc=self.doc
        
        return self.__class__(iterator,
                              columnWidths,width,rowHeight,
                              name,label,doc)

    def getTitle(self):
        return self.getLabel()
    

##     def __getattr__(self,name):
##         # forwards "everything else" to the iterator...
##         return getattr(self.iterator,name)

    def computeWidths(self):
        
        """set total width or distribute available width to columns
        without width. Note that these widths are to be interpreted as
        logical widths.

        """
        
        if self.columnWidths is not None:
            i = 0
            for item in self.columnWidths.split():
                col = self.columns[i]
                if item.lower() == "d":
                    col.width = col.getPreferredWidth()
                elif item == "*":
                    col.width = None
                else:
                    col.width = int(item)
                i += 1

        autoWidthColumns = []
        totalWidth = 0
        for col in self.columns:
            if col.width is None:
                autoWidthColumns.append(col)
            else:
                totalWidth += col.width
        if len(autoWidthColumns) > 0:
            if self.width is None:
                raise ConfigError("not all columns have a width")
            autoWidth = int( (self.width - totalWidth) / 2)
            for col in autoWidthColumns:
                col.width = autoWidth
        elif self.width is None:
            self.width = totalWidth


    def beginReport(self,doc):
        self.computeWidths()
        #self.rowno = 0
        #self.onBeginReport()
        
    def endReport(self,doc):
        pass
        #self.onEndReport()

        
        
    def processItem(self,doc,item):
        row = Row(item)

        for e in self._onRowEvents:
            e(row)
        # note: a report is not thread-safe
        #assert self.cellValues is None
        #self.rowno += 1
        #self.cellValues = []
        #self.crow = row
        #cells = []
        
        #self.onBeginRow()

        # first compute all values
        for col in self.columns:
            if col.when and not col.when(row):
                v = None
            else:
                v = col.getValue(row)
            row.cells.append(Cell(row,col,v))
            
##         # now only stringify all values
##         i = 0
##         for col in self.columns:
##             cellValues[i] = doc.formatReportCell(
##                 col, cellValues[i])
##             i += 1
            
        #self.onEndRow()
        
        #forget cellValues and crow 
        #self.cellValues = None
        #self.crow = None

        return row

##     def formatCell(self,doc,col,value):
##         if value is None:
##             return ""
##         return col.format(value)

    ##
    ## methods to be overridden by implementor subclasses
    ##
        
##     def onBeginReport(self):
##         self.renderHeader()
        
##     def onEndReport(self):
##         self.renderFooter()
        
##     def renderHeader(self):
##         pass
    
##     def renderFooter(self):
##         pass

##     def onBeginRow(self):
##         pass
    
##     def onEndRow(self):
##         pass
    
    ##
    ## public methods for user code
    ##

    def addColumn(self,meth,**kw):
        col = VurtReportColumn(self,meth,**kw)
        self.columns.append(col)
        return col

    def onEach(self,meth):
        self._onRowEvents.append(meth)

##     def execute(self,iter):
##         self.beginReport()
##         for row in iter:
##             self.processRow(row)
##         self.endReport()

class DataReport(Report):
    def __init__(self,ds,
                 columnWidths=None,width=None,rowHeight=None,
                 name=None,label=None,doc=None):

        if name is None:
            name=ds._table.getName()
        if label is None: label=ds._table.getLabel()
        if doc is None: doc=ds._table.getDoc()
        
        Report.__init__(self,ds,
                        columnWidths,width,rowHeight,
                        name=name,label=label,doc=doc)
    
    def beginReport(self,doc):
        if len(self.columns) == 0:
            for dc in self.iterator.getVisibleColumns():
                self.addDataColumn(dc,
                                   width=dc.getMaxWidth(),
                                   label=dc.getLabel())
        Report.beginReport(self,doc)
            
    def addDataColumn(self,dc,**kw):
        col = DataReportColumn(self,dc,**kw)
        self.columns.append(col)
        return col

    #def execute(self,ds):
    #    rpt.configure(**kw)

##     def child(self,**kw):
##         fwd={}
##         c = copy.copy(self)
##         for k,v in kw.items():
##             if hasattr(self,k):
##                 setattr(self,k,v)
##             else:
##                 fwd[k]=v
##         if len(fwd):
##             assert c.iterator is self.iterator
##             #print "fwd %s to %s" % (fwd,c.iterator)
##             c.iterator = c.iterator.child(**fwd)
##         return c


class DictReport(Report):
    def __init__(self,d,*args,**kw):
        Report.__init__(self,d.items(),*args,**kw)
                            
    def beginReport(self,doc):
        if len(self.columns) == 0:
            self.addColumn(meth=lambda row: str(row[0]),
                           label="key",
                           width=12)
            self.addColumn(meth=lambda row: repr(row[1]),
                           label="value",
                           width=40)
        Report.beginReport(self,doc)
        
    

class ReportColumn(Describable):
    
    def __init__(self,owner,
                 name=None,label=None,doc=None,
                 when=None,
                 halign=LEFT,
                 valign=TOP,
                 width=None,
                 ):
        self._owner = owner
        if label is None:
            label = name
        Describable.__init__(self, name,label,doc)

        self.width = width
        self.valign = valign
        self.halign = halign
        self.when = when
        
        
    def getValue(self,row):
        raise NotImplementedError

    def getPreferredWidth(self):
        return None

    def format(self,v):
        raise NotImplementedError
        #return str(v)
    

class DataReportColumn(ReportColumn):
    def __init__(self,owner,datacol,
                 name=None,label=None,doc=None,
                 **kw):
        if name is None: name=datacol.name
        #assert name != "DataReportColumn"
        if label is None: label=datacol.rowAttr.label
        if doc is None: label=datacol.rowAttr.doc
        ReportColumn.__init__(self,owner,name,label,doc,
                              **kw)
        #assert self.name != "DataReportColumn"
        self.datacol = datacol

    def getValue(self,row):
        #return self.datacol.getCellValue(self._owner.crow)
        return self.datacol.getCellValue(row.item)

    def getPreferredWidth(self):
        return self.datacol.getMaxWidth()
        
    def format(self,v):
        return self.datacol.format(v)
    
class VurtReportColumn(ReportColumn):
    def __init__(self,owner,meth,type=None,**kw):
        ReportColumn.__init__(self,owner,**kw)
        self.meth = meth
        if type is None:
            type = owner.DEFAULT_TYPE
        self.type=type

    def getValue(self,row):
        #return self.meth(self._owner.crow)
        return self.meth(row)
    
    def getPreferredWidth(self):
        return self.type.maxWidth
        
    def format(self,v):
        return self.type.format(v)


class Cell:
    def __init__(self,row,col,value):
        self.row = row
        self.col = col
        self.value = value

class Row:
    def __init__(self,item):
        self.item = item
        self.cells = []

        
