#coding: latin1

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

import sys
from textwrap import TextWrapper

from lino.gendoc.gendoc import GenericDocument
from lino.reports import reports

class PlainDocument(GenericDocument):
    def __init__(self,
                 writer=sys.stdout.write,
                 columnSep='|',
                 columnHeaderSep='-',
                 **kw):
        self.writer = writer
        self.columnSep = columnSep
        self.columnHeaderSep = columnHeaderSep
    
    def getLineWidth(self):
        return 79

    def getColumnSepWidth(self):
        return len(self.columnSep)
    
    def write(self,txt):
        self.writer(txt)
        
    def report(self,rpt):
        #print __file__, rpt.iterator._filters
        # initialize...
        rpt.beginReport(self)
        wrappers = []
        for col in rpt.columns:
            wrappers.append(TextWrapper(col.width))
        width = rpt.width + len(self.columnSep)*(len(rpt.columns)-1)

        # renderHeader

        title=rpt.getTitle()
        if title is not None:
            self.write(title+"\n")
            self.write("="*len(title)+"\n")
            
        # wrap header labels:
        headerCells = []
        headerHeight=1
        i=0
        for col in rpt.columns:
            cell = wrappers[i].wrap(col.getLabel())
            headerCells.append(cell)
            headerHeight = max(headerHeight,len(cell))
            i+=1
            
        for cell in headerCells:
            self.vfill(cell,reports.TOP,headerHeight)
            
        for i in range(headerHeight):
            self._writeLine(rpt,headerCells,i)
                               
        l = [ self.columnHeaderSep * col.width
              for col in rpt.columns]
        self.write("+".join(l) + "\n")
        
        #print __file__,rpt.iterator._filters
        # iterate...

        for row in rpt.rows(self):
        #for item in rpt._iterator:
        #    row=rpt.processItem(self,item)

            wrappedCells = []
            for col,s in row.cells():
                l = wrappers[col.index].wrap(s)
                if len(l) == 0:
                    wrappedCells.append([''])
                else:
                    wrappedCells.append(l)
            
##             i = 0
##             for value in row.values:
##                 col=rpt.columns[i]
##                 #if cell.value is None:
##                 if value is None:
##                     s = ""
##                 else:
##                     s = col.format(value)
                    
##                 l = wrappers[i].wrap(s)
##                 if len(l) == 0:
##                     wrappedCells.append([''])
##                 else:
##                     wrappedCells.append(l)
##                 i += 1
            
            # find out rowHeight for this row
            if rpt.rowHeight is None:
                rowHeight = 1
                for linelist in wrappedCells:
                    rowHeight = max(rowHeight,len(linelist))
            else:
                rowHeight = rpt.rowHeight

            if rowHeight == 1:
                self._writeLine(rpt,wrappedCells,0)
            else:
                # vfill each cell:
                for j in range(len(rpt.columns)):
                    self.vfill(wrappedCells[j],
                               rpt.columns[j].valign,
                               rowHeight)

                for i in range(rowHeight):
                    self._writeLine(rpt,wrappedCells,i)
            
        # renderFooter
        
        rpt.endReport(self)

    
##     def formatReportCell(self,col,value):
##         s = Document.formatReportCell(self,col,value)
##         l = col.wrapper.wrap(s)
##         if len(l) == 0:
##             return ['']
##         return l
    

    def _writeLine(self,rpt,cellValues,i):
        l = []
        for j in range(len(rpt.columns)):
            l.append(self.hfill(cellValues[j][i],
                                rpt.columns[j].halign,
                                rpt.columns[j].width
                                ))
        self.write(self.columnSep.join(l) + "\n")

        
    def hfill(self,s,align,width):
        if align == reports.LEFT:
            return s.ljust(width)
        if align == reports.RIGHT:
            return s.rjust(width)
        if align == reports.CENTER:
            return s.center(width)
        raise ConfigError("hfill() : %s" % repr(align))

    def vfill(self,lines,valign,height):
        n = height - len(lines) # negative if too many
        if n == 0: return
        if valign == reports.TOP:
            if n > 0:
                for i in range(n):
                    lines.append("")
            else:
                del lines[n:] # ?
        elif valign == reports.BOTTOM:
            if n > 0:
                for i in range(-n):
                    lines.insert(0,"")
            else:
                del lines[0:n] # ?
        elif valign == reports.CENTER:
            raise NotImplementedError
        else:
            raise ConfigError("vfill() : %s" % repr(valign))
                


    def p(self,txt):
        self.write(txt+"\n")
