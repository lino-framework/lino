## Copyright 2007 Luc Saffre 

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

from PyQt4 import QtCore


## class GridRow:
    
##     def __init__(self,table,rptrow):
##         self.reportRow=rptrow
##         self.strings=[]
##         for col in table.columns:
##             col = self.columns[colIndex]
##             v=col.getCellValue(rptrow)
##             if v is None:
##                 self.strings.append("")
##             else:
##                 self.strings.append(col.format(v))
        

class DataGridModel(QtCore.QAbstractTableModel):

    def __init__(self, grid):
        self.editor = grid
        self.columns = grid.rpt.columns
        self._load()
        QtCore.QAbstractTableModel.__init__(self)

    def _load(self):
        #print "wxgrid._load()"
        self.rows=[]
        if self.editor.enabled:
            #doc=self.editor.form
            #self.cells = []
            self.rows = [row for row in self.editor.rpt.rows()]
            # Add an empty row at the end
            self.rows.append(self.editor.rpt.createRow(len(self.rows)))
            # print "loaded %d rows" % len(self.rows)
    
    def rowCount(self,parent):
        "Returns the number of rows under the given parent."
        return len(self.rows)
    
    def columnCount(self,parent):
        
        """Returns the number of columns for the children of the given
        parent.

        In most subclasses, the number of columns is independent of
        the parent.
        """        
        return len(self.columns)
    
    def data(self,index,role):
        return "%r,%r" % (index,role)
    

    def headerData(self,section, orientation, role):
        return QtCore.QVariant(str(section))
