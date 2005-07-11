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


raise "lino.reports.base replaced by lino.reports.reports"

from lino.misc.descr import Describable
from lino.adamo.datatypes import STRING


class BaseReport(Describable):

    LEFT = 1
    RIGHT = 2
    CENTER = 3
    TOP = 4
    BOTTOM = 5

    DEFAULT_TYPE = STRING
    
    def __init__(self,
                 iterator=None,
                 columnWidths=None,
                 width=None,
                 rowHeight=None,
                 *args, **kw):

        self.iterator = iterator
        self.cellValues = None
        self.columns = []
        self.groups = []
        self.totals = []

        self.rowHeight = rowHeight
        self.columnWidths = columnWidths
        self.width = width
        
        Describable.__init__(self,*args,**kw)

##     def setdefaults(self,kw):
##         kw.setdefault('columnNames',self.columnNames)
##         kw.setdefault('columnWidths',self.columnWidths)
##         kw.setdefault('rowHeight',self.rowHeight)
##         #self.ds.setdefaults(self,kw)

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
        self.rowno = 0
        #self.onBeginReport()
        
    def endReport(self,doc):
        pass
        #self.onEndReport()
        
    def processRow(self,doc,row):
        # note: a report is not thread-safe
        assert self.cellValues is None
        #self.rowno += 1
        #self.cellValues = []
        #self.crow = row
        cellValues = []
        
        #self.onBeginRow()

        # first compute all values
        for col in self.columns:
            if col.when and not col.when(self):
                v = None
            else:
                v = col.getValue(row)
            cellValues.append(v)
            
        # now only stringify all values
        i = 0
        for col in self.columns:
            cellValues[i] = doc.formatReportCell(
                col, cellValues[i])
            i += 1
            
        #self.onEndRow()
        
        #forget cellValues and crow 
        #self.cellValues = None
        #self.crow = None

        return cellValues

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

##     def execute(self,iter):
##         self.beginReport()
##         for row in iter:
##             self.processRow(row)
##         self.endReport()





class DataReport(BaseReport):
    def __init__(self,ds,name=None,label=None,doc=None):

        if name is None: name=ds._table.getName()
        if label is None: label=ds._table.getLabel()
        if doc is None: doc=ds._table.getDoc()
        
        BaseReport.__init__(self,ds,name=name,label=label,doc=doc)
    
    def beginReport(self,doc):
        if len(self.columns) == 0:
            for dc in ds.getVisibleColumns():
                self.addDataColumn(dc,
                                   width=dc.getMaxWidth(),
                                   label=dc.getLabel())
        BaseReport.beginReport(self,doc)
            
    def addDataColumn(self,dc,**kw):
        col = DataReportColumn(self,dc,**kw)
        self.columns.append(col)
        return col

    def execute(self,ds):
        rpt.configure(**kw)


class DictReport(BaseReport):
    def __init__(self,d):
        BaseReport.__init__(self,iterator=d.items())
                            
    def beginReport(self,doc):
        if len(self.columns) == 0:
            self.addColumn(meth=lambda row: str(row[0]),
                           label="key",
                           width=12)
            self.addColumn(meth=lambda row: repr(row[1]),
                           label="value",
                           width=40)
        BaseReport.beginReport(self,doc)
        
    

class ReportColumn(Describable):
    
    def __init__(self,owner,
                 name=None,label=None,doc=None,
                 when=None,
                 halign=BaseReport.LEFT,
                 valign=BaseReport.TOP,
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
    def __init__(self,owner,datacol,**kw):
        ReportColumn.__init__(self,owner,**kw)
        self.datacol = datacol

    def getValue(self,row):
        return self.datacol.getCellValue(self._owner.crow)

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
        return self.meth(self._owner.crow)
    
    def getPreferredWidth(self):
        return self.type.maxWidth
        
    def format(self,v):
        return self.type.format(v)
        
class ConfigError(Exception):
    pass
