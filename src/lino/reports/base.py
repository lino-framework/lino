## Copyright Luc Saffre 2003-2005.

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



from lino.misc.descr import Describable

class BaseReport(Describable):

    LEFT = 1
    RIGHT = 2
    CENTER = 3
    TOP = 4
    BOTTOM = 5
    
    def __init__(self,
                 columnWidths=None,
                 width=None,
                 rowHeight=None,
                 *args, **kw):
        
        self.cellValues = None
        self.columns = []
        self.groups = []
        self.totals = []

        self.rowHeight = rowHeight
        self.columnWidths = columnWidths
        self.width = width
        
        Describable.__init__(self,*args,**kw)

    def setdefaults(self,kw):
        kw.setdefault('columnNames',self.columnNames)
        kw.setdefault('columnWidths',self.columnWidths)
        kw.setdefault('rowHeight',self.rowHeight)
        #self.ds.setdefaults(self,kw)

    def computeWidths(self):
        
        """set total width or distribute available width to columns
        without width. Note that these widths are to be interpreted as
        logical widths.

        """
        
        if self.columnWidths is not None:
            i = 0
            for item in self.columnWidths.split():
                if item.lower() == "d":
                    pass
                elif item == "*":
                    self.columns[i].width = None
                else:
                    self.columns[i].width = int(item)
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


    def addDataColumn(self,dc,**kw):
        col = DataReportColumn(self,dc,**kw)
        self.columns.append(col)
        return col

    ## public methods 

    def addColumn(self,meth,**kw):
        col = VurtReportColumn(self,meth,**kw)
        self.columns.append(col)
        return col


    def execute(self,datasource):
        self.beginReport()
        for row in datasource:
            self.processRow(row)
        self.endReport()

    def beginReport(self):
        self.computeWidths()
        self.onBeginReport()
        
    def endReport(self):
        self.onEndReport()
        
    def processRow(self,row):
        # TODO: what if the report running in a thread...?
        assert self.cellValues is None
        self.cellValues = []
        self.crow = row
        
        self.onBeginRow()

        # first compute all values
        for col in self.columns:
            if col.when and not col.when(self):
                v = None
            else:
                v = col.getValue(row)
            self.cellValues.append(v)
            
        # now only stringify all values
        i = 0
        for col in self.columns:
            self.cellValues[i] = self.formatCell(col,
                                                 self.cellValues[i])
            i += 1
            
        self.onEndRow()
        
        #forget cellValues and crow 
        self.cellValues = None
        self.crow = None

    def formatCell(self,col,value):
        if value is None:
            return ""
        return str(value)

    ##
    ## methods to be overridden by subclasses
    ##
        
    def onBeginReport(self):
        self.renderHeader()
        
    def onEndReport(self):
        self.renderFooter()
        
    def renderHeader(self):
        pass
    
    def renderFooter(self):
        pass

    def onBeginRow(self):
        pass
    
    def onEndRow(self):
        pass
    

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

    

class DataReportColumn(ReportColumn):
    def __init__(self,owner,datacol,width=None,**kw):
        if width is None:
            width = datacol.getPreferredWidth()
        ReportColumn.__init__(self,owner,width=width,**kw)
        self.datacol = datacol

    def getValue(self,row):
        return self.datacol.getCellValue(self._owner.crow)
        
class VurtReportColumn(ReportColumn):
    def __init__(self,owner,meth,**kw):
        ReportColumn.__init__(self,owner,**kw)
        self.meth = meth

    def getValue(self,row):
        return self.meth(self._owner.crow)
        
class ConfigError(Exception):
    pass
