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
#from lino.adamo.query import Query

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


    def __init__(self, parent,
                 ds,
                 columnWidths=None,
                 width=None,
                 rowHeight=None,
                 **kw
                 ):

        self.columns = []
        self.groups = []
        self.totals = []
        self._onRowEvents=[]


        Describable.__init__(self,parent,**kw)
        if parent is not None:
            #if iterator is None: iterator=parent._iterator
            if ds is None: ds=parent.ds
            if columnWidths is None: columnWidths=parent.columnWidths
            if width is None: width=parent.width
            if rowHeight is None: rowHeight=parent.rowHeight
        #self._iterator = iterator.__iter__()
        self.ds = ds
        self.rowHeight = rowHeight
        self.columnWidths = columnWidths
        self.width = width
        
        
    def getTitle(self):
        return self.getLabel()

    def setupMenu(self,navigator):
        pass
    
    def __xml__(self,wr):
        return self.ds.__xml__(wr)

    def __len__(self):
        return len(self.ds)

    def __getitem__(self,i):
        #return self.ds.__getitem__(i)
        return ReportRow(self,self.ds.__getitem__(i))

    def canWrite(self):
        return self.ds.canWrite()

    def getVisibleColumns(self):
        return self.columns



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
                if col.getMaxWidth() is not None \
                      and col.getMaxWidth() < autoWidth:
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

    def rows(self,doc):
        return ReportIterator(self,doc)
        
    #def processItem(self,doc,item):
    def processItem(self,item):
        return ReportRow(self,item)
        #return ReportRow(self,doc,item)
        #row = Row(item)

        #return row

    
    ##
    ## public methods for user code
    ##

    def addColumn(self,col):
        self.columns.append(col)
        return col
    
    def addVurtColumn(self,meth,**kw):
        return self.addColumn(VurtReportColumn(meth,**kw))

    def onEach(self,meth):
        self._onRowEvents.append(meth)

    def show(self,**kw):
        syscon.showReport(self,**kw)

    def setupForm(self,frm,row=None,**kw):
        
        if row is None:
            row = self[0]
            
        kw.setdefault('data',row)
        kw.setdefault('name',self.getName())
        kw.setdefault('label',self.getLabel())
        kw.setdefault('doc',self.getDoc())
        frm.configure(**kw)
        
        for col in self.getVisibleColumns():
            frm.addDataEntry(col,label=col.getLabel())
##         for cell in row:
##             dc = cell.col
##             frm.addDataEntry(dcname=dc.name,
##                          label=dc.getLabel(),
##                          enabled=cell.canWrite(),
##                          getter=cell.__str__,
##                          setter=cell.setValueFromString)

        def afterSkip(nav):
            row = self[nav.currentPos]
            frm.data = row
            #frm.refresh()
##             for cell in row:
##                 setattr(frm.entries,cell.col.name,cell.format())
        frm.addNavigator(self,afterSkip=afterSkip)
        

    


class ReportColumn(Describable):
    
    type=STRING
    
    def __init__(self,
                 formatter=str,
                 selector=None,
                 name=None,label=None,doc=None,
                 when=None,
                 halign=LEFT,
                 valign=TOP,
                 width=None,
                 ):
        #self._owner = owner
        if label is None:
            label = name
        Describable.__init__(self, None, name,label,doc)

        self.width = width
        self.valign = valign
        self.halign = halign
        self.when = when
        self._formatter=formatter
        if selector is None:
            selector=self.showSelector
        self._selector=selector
        
        
    def getMinWidth(self):
        return self.width
    def getMaxWidth(self):
        return self.width

    def getCellValue(self,row):
        raise NotImplementedError,str(self.__class__)

    def format(self,v):
        return self._formatter(v)

    def validate(self,value):
        pass
    
    def showSelector(self,frm,row):
        return self._selector(frm,row)

    def canWrite(self,row):
        return False
    
##     def getType(self):
##         return self.type


class DataReportColumn(ReportColumn):
    def __init__(self,datacol,
                 name=None,label=None,doc=None,
                 formatter=None,
                 selector=None,
                 **kw):
        if name is None: name=datacol.name
        if formatter is None: formatter=datacol.format
        if selector is None: selector=datacol.showSelector
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

    def getMinWidth(self):
        return self.datacol.getMinWidth()
    def getMaxWidth(self):
        return self.datacol.getMaxWidth()

    def addFilter(self,*args):
        self.datacol.addFilter(*args)
        
    def canWrite(self,row):
        if row is None:
            return self.datacol.canWrite(None)
        return self.datacol.canWrite(row.item)
    
    def validate(self,value):
        return self.datacol.rowAttr.validate(value)
        
##     def getType(self):
##         return self.datacol.rowAttr.getType()
    
##     def format(self,v):
##         return self.datacol.format(v)
    
class VurtReportColumn(ReportColumn):
    
    def __init__(self,meth,type=None,formatter=None,**kw):
        if type is not None:
            self.type=type
        if formatter is None: formatter=self.type.format
        ReportColumn.__init__(self,formatter,**kw)
        self.meth = meth

    def getCellValue(self,row):
        return self.meth(row)
    
    def getMinWidth(self):
        return self.type.minWidth
    def getMaxWidth(self):
        return self.type.maxWidth
        
##     def format(self,v):
##         return self.type.format(v)


## class Cell:
##     def __init__(self,row,col,value):
##         self.row = row
##         self.col = col
##         self.value = value


class ReportRow:
    def __init__(self,rpt,item):
        self.item = item
        #self.cells = []
        self.values = []
        
        for e in rpt._onRowEvents:
            e(self)
            
            # onEach event may do some lookup or computing and store
            # the result in the ReportRow instance.
            

        # compute all cell values
        for col in rpt.columns:
            if col.when and not col.when(self):
                v = None
            else:
                v = col.getCellValue(self)
                if v is not None:
                    #col.getType().validate(v)
                    col.validate(v)
            #self.cells.append(Cell(self,col,v))
            self.values.append(v) 
            



class ReportIterator:
    def __init__(self,rpt,doc):
        self.iterator=rpt.ds.__iter__()
        self.rpt=rpt
        self.doc=doc
        
    def __iter__(self):
        return self

    def next(self):
        return self.rpt.processItem(self.iterator.next())
        #return self.rpt.processItem(self.doc,self.iterator.next())

class DataReport(BaseReport):
    
    def __init__(self,qry,
                 columnWidths=None,width=None,rowHeight=None,
                 name=None,label=None,doc=None,**kw):

        if name is None:
            name=qry.getLeadTable().getName()+"Report"
        if label is None: label=qry.getLabel()
        #if doc is None: doc=ds.getDoc()
        
        if len(kw):
            # forward keywords to the Query
            qry=qry.child(**kw)
            
        BaseReport.__init__(self,None,qry,
                            columnWidths,width,rowHeight,
                            name=name,label=label,doc=doc)
    
    def setupMenu(self,navigator):
        self.ds.setupMenu(navigator)
        
    def beginReport(self,doc):
        if len(self.columns) == 0:
            for dc in self.ds.getVisibleColumns():
                col = DataReportColumn(dc,label=dc.getLabel())
                self.columns.append(col)
                                   
        BaseReport.beginReport(self,doc)
            
    def addDataColumn(self,colName,**kw):
        dc=self.ds.findColumn(colName)
        return self.addColumn(DataReportColumn(dc,**kw))

    def doesShow(self,qry):
        #used in lino.gendoc.html
        myqry=self.ds
        if myqry.getLeadTable().name != qry.getLeadTable().name:
            return False
        #if myqry._masters != qry._masters:
        #    return False
        return True

    def canSort(self):
        return True
        
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
            self.addVurtColumn(meth=lambda row: str(row.item[0]),
                               label="key",
                               width=12)
            self.addVurtColumn(meth=lambda row: str(row.item[1]),
                               label="value",
                               width=40)
        BaseReport.beginReport(self,doc)

    def canSort(self):
        return False
        
    
        
class Report(BaseReport):
    def __init__(self,ds,**kw):
        BaseReport.__init__(self,None, ds, **kw)

        
## def createReport(iterator,**kw):
##     if isinstance(iterator,Query):
##         return DataReport(None,iterator,**kw)
##     if isinstance(iterator,dict):
##         return DictReport(iterator,**kw)
##     return Report(None,iterator,**kw)
