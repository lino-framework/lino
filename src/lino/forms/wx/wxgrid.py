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

import wx
import wx.grid

#from lino.adamo.rowattrs import Pointer

#pointerDataType = "Pointer"


class MyDataTable(wx.grid.PyGridTableBase):

    def __init__(self, editor):
        wx.grid.PyGridTableBase.__init__(self)
        self.editor = editor
        #self.report = report
        self.ds = editor.ds
        self.columns = self.ds.getVisibleColumns()
        self.loadData()

    def loadData(self):
        self.rows = [ [str(cell) for cell in row]
                      for row in self.ds]
        #self.rows = [row for row in self.report]

    def GetNumberRows(self): return len(self.rows) + 1
    def GetNumberCols(self): return len(self.columns)
        
    def IsEmptyCell(self, row, col):
        
        """ bool IsEmptyCell(int row, int col) -- Returning a true value
        will result in the cell being "blank". No renderer or editor
        will be assigned, the table will not be asked for the
        corresponding value. Navigation keys will skip the cell,
        programmatic selection using the wxGrid::MoveCursor*Block
        commands will also skip the cell.  """
        
        return False
        # required
        #r = (self.GetValue(row,col) is None) 
        #print "IsEmptyCell(%d,%d) --> %s" % (row, col,repr(r))
        #return r

          
    # Get/Set values in the table.  The Python version of these
    # methods can handle any data-type, (as long as the Editor and
    # Renderer understands the type too,) not just strings as in the
    # C++ version.
    def GetValue(self, rowIndex, colIndex):
        "required"
        try:
            return self.rows[rowIndex][colIndex]
            # ret = self.columns[colIndex].GetCellValue(row)
        except IndexError:
            return None

    def SetValue(self, rowIndex, colIndex, value):
        "required"
        #print "SetValue(%d,%d,%s)" % (rowIndex, colIndex, repr(value))
        try:
##             row = self.ds[rowIndex]
##             #dc = self.ds.getColumn(colIndex)
##             #v = dc.rowAttr.parse(value)
##             #dc.setValueFromString(value)
##             cell = row[colIndex]
##             cell.setValueFromString(value)
##             #row.setCellValue(colIndex, value)
##             #row[colIndex] = value
##             self.rows[rowIndex][colIndex] = cell.format()
            self.rows[rowIndex][colIndex] = value
        except IndexError:
            row = [None] * len(self.columns)
            raise "todo: append row"
        
##     def GetTypeName(self,row,col):
##         rowAttr = self.columns[col].rowAttr
##         if isinstance(rowAttr,Pointer):
##             #print "Pointer"
##             return pointerDataType
##         return "string"
    


    def GetColLabelValue(self, col):
        "Called when the grid needs to display labels"
        #print "GetColLabelValue(%d) -> %s" % (col, self.columns[col].name)
        return self.columns[col].getLabel()

##  def ResetView(self, grid):
##      """
##      (wxGrid) -> Reset the grid view.      Call this to
##      update the grid if rows and columns have been added or deleted
##      """
##      grid.BeginBatch()
##      for current, new, delmsg, addmsg in [
##          (self._rows, self.GetNumberRows(),
##           wx.GRIDTABLE_NOTIFY_ROWS_DELETED,
##           wx.GRIDTABLE_NOTIFY_ROWS_APPENDED),
##          (self._cols, self.GetNumberCols(),
##           wx.GRIDTABLE_NOTIFY_COLS_DELETED,
##           wx.GRIDTABLE_NOTIFY_COLS_APPENDED),
##          ]:
##          if new < current:
##              msg = wx.GridTableMessage(self,delmsg,new,current-new)
##              grid.ProcessTableMessage(msg)
##          elif new > current:
##              msg = wx.GridTableMessage(self,addmsg,new-current)
##              grid.ProcessTableMessage(msg)
##              self.UpdateValues(grid)
##      grid.EndBatch()

##      self._rows = self.GetNumberRows()
##      self._cols = self.GetNumberCols()
##      # update the column rendering plugins
##      self._updateColAttrs(grid)

##      # update the scrollbars and the displayed part of the grid
##      grid.AdjustScrollbars()
##      grid.ForceRefresh()


##  def DeleteRows(self, rows):
##      """
##      rows -> delete the rows from the dataset
##      rows hold the row indices
##      """
##      deleteCount = 0
##      rows = rows[:]
##      rows.sort()
##      for i in rows:
##          self.data.pop(i-deleteCount)
##          # we need to advance the delete count
##          # to make sure we delete the right rows
##          deleteCount += 1

    def setOrderBy(self,colIndexes):
        print __name__, colIndexes
        cn = " ".join([self.columns[i].name for i in colIndexes])
        print __name__,cn
        self.ds.configure(orderBy=cn)
        self.loadData()


class DataGridCtrl(wx.grid.Grid):
    def __init__(self, parent, editor):
        wx.grid.Grid.__init__(self, parent, -1)
        self.table = MyDataTable(editor)
        self.SetTable(self.table,True)
        self.SetRowLabelSize(0)
        self.SetMargins(0,0)
        self.AutoSizeColumns(True)
        
        wx.grid.EVT_GRID_CELL_LEFT_DCLICK(self,
                                          self.OnLeftDClick)
        wx.grid.EVT_GRID_LABEL_RIGHT_CLICK(self,
                                           self.OnLabelRightClicked)


    
    
    def OnLeftDClick(self, evt):
        # start cell editor on doubleclick, not only on second click.
        if self.CanEnableCellControl():
             self.EnableCellEditControl()

    def OnLabelRightClicked(self, evt):
        # Did we click on a row or a column?
        row, col = evt.GetRow(), evt.GetCol()
        if row == -1: self.colPopup(col, evt)
        elif col == -1:
            print "OnLabelRightClicked(%d,%d)" % (row,col)
            return
            self.rowPopup(row, evt)

    def Reset(self):
        """reset the view based on the data in the table.   Call
        this when rows are added or destroyed"""
        self.table.ResetView(self)


    def colPopup(self, col, evt):
        """(col, evt) -> display a popup menu when a column label is
        right clicked"""
        x = self.GetColSize(col)/2
        menu = wx.Menu()
        sortID = wx.NewId()

        xo, yo = evt.GetPosition()
        #self.SelectCol(col)
        #cols = self.GetSelectedCols()
        #print cols
        #self.Refresh()
        #menu.Append(id1, "Delete Col(s)")
        menu.Append(sortID, "set SortColumn(s)")

##      def delete(event, self=self, col=col):
##          cols = self.GetSelectedCols()
##          self._table.DeleteCols(cols)
##          self.Reset()

        def setSortColumn(event, self=self):
            #print "setSortColumn"
            self.table.setOrderBy(self.GetSelectedCols())
            self.ForceRefresh()
            #print "ForceRefresh"

        #EVT_MENU(self, id1, delete)
        #if len(cols) == 1:
        wx.EVT_MENU(self, sortID, setSortColumn)
        self.PopupMenu(menu, wx.Point(xo, 0))
        menu.Destroy()
             
    def rowPopup(self, row, evt):
        
        """display a popup menu when a row label is right clicked"""
        
        appendID = wx.NewId()
        deleteID = wx.NewId()
        x = self.GetRowSize(row)/2
        if not self.GetSelectedRows():
            self.SelectRow(row)
        xo, yo = evt.GetPosition()
        menu = wxMenu()
        menu.Append(appendID, "Append Row")
        menu.Append(deleteID, "Delete Row(s)")

        def append(event, self=self, row=row):
            self.table.AppendRow(row)
            self.Reset()

        def delete(event, self=self, row=row):
            rows = self.GetSelectedRows()
            self.table.DeleteRows(rows)
            self.Reset()

        EVT_MENU(self, appendID, append)
        EVT_MENU(self, deleteID, delete)
        self.PopupMenu(menu, wxPoint(x, yo))
        menu.Destroy()

        
        
        
