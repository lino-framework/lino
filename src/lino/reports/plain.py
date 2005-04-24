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








raise "no longer used"

import sys
from textwrap import TextWrapper

from lino.reports.base import BaseReport, ConfigError

class Report(BaseReport):
    
    """a report that renders in plain text, destination just needs a
    write method """
    def __init__(self,
                 writer=sys.stdout.write,
                 columnSep='|',
                 columnHeaderSep='-',
                 **kw):
        self.writer = writer
        self.columnSep = columnSep
        self.columnHeaderSep = columnHeaderSep
        BaseReport.__init__(self,**kw)
                 
    def setdefaults(self,kw):
        kw.setdefault('columnSep',self.columnSep)
        kw.setdefault('columnHeaderSep',self.columnHeaderSep)
        BaseReport.setdefaults(self,kw)

    def write(self,txt):
        self.writer(txt)

    def onBeginReport(self):
        #self.wrappers = []
        for col in self.columns:
            col.wrapper = TextWrapper(col.width)
            #self.wrappers.append(TextWrapper(col.width))
        self.width += len(self.columnSep)*(len(self.columns)-1)
        BaseReport.onBeginReport(self)


    def renderHeader(self):
        if self.label is not None:
            self.write(self.label+"\n")
            self.write("="*len(self.label)+"\n")
            
        # wrap header labels:
        headerCells = []
        headerHeight=1
        for col in self.columns:
            cell = col.wrapper.wrap(col.getLabel())
            headerCells.append(cell)
            headerHeight = max(headerHeight,len(cell))
        for cell in headerCells:
            self.vfill(cell,self.TOP,headerHeight)
        for i in range(headerHeight):
            self._writeLine(headerCells,i)
                               
##         l = [ self.hfill(col.getLabel(),
##                          col.halign,
##                          col.width )
##               for col in self.columns]
##         self.write(self.columnSep.join(l) + "\n")
        
        l = [ self.columnHeaderSep * col.width
              for col in self.columns]
        self.write("+".join(l) + "\n")
            

    def formatCell(self,col,value):
        s = BaseReport.formatCell(self,col,value)
        l = col.wrapper.wrap(s)
        if len(l) == 0:
            return ['']
        return l
    
    def onEndRow(self):
        
##         # wrap long text contents
##         for i in range(len(self.columns)):
##             self.cellValues[i] = self.wrappers[i].wrap(
##                 self.cellValues[i])
            
        # find out rowHeight for this row
        if self.rowHeight is None:
            rowHeight = 1
            for linelist in self.cellValues:
                rowHeight = max(rowHeight,len(linelist))
        else:
            rowHeight = self.rowHeight

        if rowHeight == 1:
            self._writeLine(self.cellValues,0)
        else:
            # vfill each cell:
            for j in range(len(self.columns)):
                self.vfill(self.cellValues[j],
                           self.columns[j].valign,
                           rowHeight)
             
            for i in range(rowHeight):
                self._writeLine(self.cellValues,i)

    def _writeLine(self,cellValues,i):
        l = []
        for j in range(len(self.columns)):
            l.append(self.hfill(cellValues[j][i],
                                self.columns[j].halign,
                                self.columns[j].width
                                ))
        self.write(self.columnSep.join(l) + "\n")

        
    def hfill(self,s,align,width):
        if align == self.LEFT:
            return s.ljust(width)
        if align == self.RIGHT:
            return s.rjust(width)
        if align == self.CENTER:
            return s.center(width)
        raise ConfigError("hfill() : %s" % repr(align))

    def vfill(self,lines,valign,height):
        n = height - len(lines) # negative if too many
        if n == 0: return
        if valign == self.TOP:
            if n > 0:
                for i in range(n):
                    lines.append("")
            else:
                del lines[n:] # ?
        elif valign == self.BOTTOM:
            if n > 0:
                for i in range(-n):
                    lines.insert(0,"")
            else:
                del lines[0:n] # ?
        elif valign == self.CENTER:
            raise NotImplementedError
        else:
            raise ConfigError("vfill() : %s" % repr(valign))
                
