## Copyright 2003-2008 Luc Saffre 

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
from cStringIO import StringIO

from lino.gendoc.gendoc import GenericDocument
from lino.reports.constants import *
from lino.console import syscon
from lino.misc.etc import assert_pure

class PlainDocument(GenericDocument):
    """
    Usage example:

    >>> doc=PlainDocument(lineWidth=41)
    >>> doc.h1("Title")
    >>> doc.par("Foo, bar and baz. " * 4)
    >>> print unicode(doc).strip()
    Title
    -----
    Foo, bar and baz. Foo, bar and baz. Foo,
    bar and baz. Foo, bar and baz.
    
    
    """
    def __init__(self,
                 writer=None,
                 columnSep='|',
                 lineWidth=79,
                 columnHeaderSep='-',
                 **kw):
        if writer is None:
            writer=StringIO()
            #writer=syscon.getSystemConsole().toolkit.stdout
            #writer=syscon.getSystemConsole()
        assert hasattr(writer,'write')
        self._writer = writer
        self.columnSep = columnSep
        self.columnHeaderSep = columnHeaderSep
        self.lineWidth=lineWidth
    
    def write(self,txt):
        self._writer.write(txt)
##         try:
##             self._writer.write(txt)
##         except UnicodeEncodeError,e:
##             raise "FooException: could not write %r to %r" % (
##                 txt, self._writer)
        
    def __unicode__(self):
        return self._writer.getvalue()
    
    def report(self,rpt):
        #print __file__, rpt.iterator._filters
        # initialize...
        rpt.beginReport(lineWidth=self.lineWidth,
                        columnSepWidth=len(self.columnSep))
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
            self.vfill(cell,TOP,headerHeight)
            
        for i in range(headerHeight):
            self._writeRptLine(rpt,headerCells,i)
                               
        l = [ self.columnHeaderSep * col.width
              for col in rpt.columns]
        self.write("+".join(l) + "\n")
        
        #print __file__,rpt.iterator._filters
        # iterate...

        for row in rpt.rows():
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
                self._writeRptLine(rpt,wrappedCells,0)
            else:
                # vfill each cell:
                for j in range(len(rpt.columns)):
                    self.vfill(wrappedCells[j],
                               rpt.columns[j].datatype.valign,
                               rowHeight)

                for i in range(rowHeight):
                    self._writeRptLine(rpt,wrappedCells,i)
            
        # renderFooter
        
        rpt.endReport()

    
##     def formatReportCell(self,col,value):
##         s = Document.formatReportCell(self,col,value)
##         l = col.wrapper.wrap(s)
##         if len(l) == 0:
##             return ['']
##         return l
    

    def _writeRptLine(self,rpt,cellValues,i):
        l = []
        for j in range(len(rpt.columns)):
            assert_pure(cellValues[j][i])
            l.append(self.hfill(cellValues[j][i],
                                rpt.columns[j].datatype.halign,
                                rpt.columns[j].width))
        s=self.columnSep.join(l)
        self.write(s.rstrip() + "\n")

        
    def hfill(self,s,align,width):
        if align == LEFT:
            return s.ljust(width)
        if align == RIGHT:
            return s.rjust(width)
        if align == CENTER:
            return s.center(width)
        raise ConfigError("hfill() : %s" % repr(align))

    def vfill(self,lines,valign,height):
        n = height - len(lines) # negative if too many
        if n == 0: return
        if valign == TOP:
            if n > 0:
                for i in range(n):
                    lines.append("")
            else:
                del lines[n:] # ?
        elif valign == BOTTOM:
            if n > 0:
                for i in range(-n):
                    lines.insert(0,"")
            else:
                del lines[0:n] # ?
        elif valign == CENTER:
            raise NotImplementedError
        else:
            raise ConfigError("vfill() : %s" % repr(valign))
                


    def par(self,text):
        w=TextWrapper(self.lineWidth)
        l=w.wrap(text)
        for ln in l:
            self.write(ln.rstrip()+"\n")
        self.write("\n")

    def heading(self,level,text,**kw):
        self.write("\n"+text+"\n" + "-" * len(text) + "\n")

def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()

