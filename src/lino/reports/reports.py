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
from lino.console import syscon
from lino.adamo.datatypes import STRING
from lino.adamo.query import Query

class ConfigError(Exception):
    pass

class NotEnoughSpace(Exception):
    pass

LEFT = 1
RIGHT = 2
CENTER = 3
TOP = 4
BOTTOM = 5
    
class BaseReport(Describable):


    DEFAULT_TYPE = STRING
    
    def __init__(self, parent,
                 iterator,
                 columnWidths=None,
                 width=None,
                 rowHeight=None,
                 **kw
                 ):

        self.columns = []
        self.groups = []
        self.totals = []
        self._onRowEvents=[]

        self.iterator = iterator

        Describable.__init__(self,parent,**kw)
        if parent is not None:
            if iterator is None: iterator=parent.iterator
            if columnWidths is None: columnWidths=parent.columnWidths
            if width is None: width=parent.width
            if rowHeight is None: rowHeight=parent.rowHeight
        self.rowHeight = rowHeight
        self.columnWidths = columnWidths
        self.width = width
        
        

##     def setdefaults(self,kw):
##         kw.setdefault('columnNames',self.columnNames)
##         kw.setdefault('columnWidths',self.columnWidths)
##         kw.setdefault('rowHeight',self.rowHeight)
##         #self.ds.setdefaults(self,kw)

##     def child(self,
##               iterator=None,
##               columnWidths=None,
##               width=None,
##               rowHeight=None,
##               name=None,
##               label=None,
##               doc=None,
##               **kw):
        
##         if iterator is None: iterator=self.iterator
## ##         if iterator is None:
## ##             if len(kw):
## ##                 iterator=self.iterator.child(**kw)
## ##             else:
## ##                 iterator=self.iterator
## ##         else:
## ##             assert len(kw) == 0
            
##         if columnWidths is None: columnWidths=self.columnWidths
##         if width is None: width=self.width
##         if rowHeight is None: rowHeight=self.rowHeight
##         if name is None: name=self.name
##         if label is None: label=self.label
##         if doc is None: doc=self.doc
        
##         return self.__class__(iterator,
##                               columnWidths,width,rowHeight,
##                               name,label,doc,**kw)

    def getTitle(self):
        return self.getLabel()
    

##     def __getattr__(self,name):
##         # forwards "everything else" to the iterator...
##         return getattr(self.iterator,name)

    def computeWidths(self,doc):
        
        """set total width or distribute available width to columns
        without width. Note that these widths are to be interpreted as
        logical widths.

        """
        
        if self.columnWidths is not None:
            i = 0
            for item in self.columnWidths.split():
                col = self.columns[i]
                if item.lower() == "d":
                    col.width = col.getMinWidth()
                elif item == "*":
                    col.width = None
                else:
                    col.width = int(item)
                i += 1

        waiting = [] # columns waiting for automatic width
        used = 0 # how much width used up by columns with a width
        for col in self.columns:
            if col.width is None:
                waiting.append(col)
            else:
                used += col.width
                
        available=self.width - \
                   doc.getColumnSepWidth()*(len(self.columns)-1)

        if available <= 0:
            raise NotEnoughSpace()
        
        l=[]
        if len(waiting) > 0:
            
            # first loop: distribute width to those columns who need
            # less than available
            
            autoWidth = int((available - used) / len(waiting))
            for col in waiting:
                if col.getMaxWidth() < autoWidth:
                    col.width = col.getMaxWidth()
                    used += col.width
                else:
                    l.append(col)
                    
        if len(l) > 0:
            # second loop: 
            w = int((available - used) / len(l))
            for col in l:
                col.width = w
                used += w
         
        #elif self.width is None:
        #    self.width = totalWidth


    def beginReport(self,doc):
        if self.width is None:
            self.width=doc.getLineWidth()
        self.computeWidths(doc)
        
    def endReport(self,doc):
        pass

        
        
    def processItem(self,doc,item):
        row = Row(item)

        for e in self._onRowEvents:
            e(row)
            

        # compute all cell values
        for col in self.columns:
            if col.when and not col.when(row):
                v = None
            else:
                v = col.getValue(row)
            row.cells.append(Cell(row,col,v))
            

        return row

    
    ##
    ## public methods for user code
    ##

    def addColumn(self,meth,**kw):
        col = VurtReportColumn(self,meth,**kw)
        self.columns.append(col)
        return col

    def onEach(self,meth):
        self._onRowEvents.append(meth)

    def show(self,**kw):
        syscon.report(self,**kw)



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
        Describable.__init__(self, None, name,label,doc)

        self.width = width
        self.valign = valign
        self.halign = halign
        self.when = when
        
        
    def getValue(self,row):
        raise NotImplementedError

    def getMinWidth(self):
        raise NotImplementedError
    def getMaxnWidth(self):
        raise NotImplementedError

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

    def getMinWidth(self):
        return self.datacol.getMinWidth()
    def getMaxWidth(self):
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
    
    def getMinWidth(self):
        return self.type.minWidth
    def getMaxWidth(self):
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



class DataReport(BaseReport):
    
    def __init__(self,ds,
                 columnWidths=None,width=None,rowHeight=None,
                 name=None,label=None,doc=None,**kw):

        if name is None:
            name=ds.getLeadTable().getName()+"Report"
        if label is None: label=ds.getLabel()
        #if doc is None: doc=ds.getDoc()
        
        if len(kw):
            # forward keywords to the query
            ds=ds.child(**kw)
            
        BaseReport.__init__(self,None,ds,
                            columnWidths,width,rowHeight,
                            name=name,label=label,doc=doc)
    
    def beginReport(self,doc):
        if len(self.columns) == 0:
            for dc in self.iterator.getVisibleColumns():
                self.addDataColumn(dc,
                                   #width=dc.getMaxWidth(),
                                   label=dc.getLabel())
        BaseReport.beginReport(self,doc)
            
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


class DictReport(BaseReport):
    
    def __init__(self,d,**kw):
        BaseReport.__init__(self,None, d.items(), **kw)
        
    def beginReport(self,doc):
        if len(self.columns) == 0:
            self.addColumn(meth=lambda row: str(row[0]),
                           label="key",
                           width=12)
            self.addColumn(meth=lambda row: repr(row[1]),
                           label="value",
                           width=40)
        Report.beginReport(self,doc)
        
    
        
class Report(BaseReport):
    def __init__(self,iterator,**kw):
        BaseReport.__init__(self,None, iterator, **kw)

        
def createReport(iterator,**kw):
    if isinstance(iterator,Query):
        return DataReport(None,iterator,**kw)
    if isinstance(iterator,dict):
        return DictReport(iterator,**kw)
    return Report(None,iterator,**kw)
