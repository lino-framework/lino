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

import wx
import wx.grid

from lino.adamo.exceptions import RowLockFailed


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
        


class MyDataTable(wx.grid.PyGridTableBase):

    def __init__(self, editor):
        wx.grid.PyGridTableBase.__init__(self)
        self.editor = editor
        self.columns = self.editor.rpt.columns
        self._load()

    def _load(self):
        #print "wxgrid._load()"
        self.rows=[]
        if self.editor.enabled:
            #doc=self.editor.form
            #self.cells = []
            self.rows = [row for row in self.editor.rpt.rows()]
            self.rows.append(self.editor.rpt.createRow(len(self.rows)))
            #print "loaded %d rows" % len(self.rows)
        
    def _refresh(self):
        #print "wxgrid._refresh()"
        oldlen=len(self.rows)
        #self._load()
        self.resetRows(self.editor.wxctrl,oldlen)
        #self._updateValues(self.editor.wxctrl)

##     def refresh(self,oldlen=None):
##         if oldlen is None:
##             oldlen = self.GetNumberRows()
##         #self._load()
##         self.resetRows(self.editor.wxctrl,oldlen)
##         self.updateValues(self.editor.wxctrl)

    def GetNumberRows(self): return len(self.rows)
    def GetNumberCols(self): return len(self.columns)

    def _updateValues(self, grid):
        """Update all displayed values.
        
        Send an event to the grid to redisplay all of the cells

        """
        #print "wxgrid._updateValues()"
        
        
        msg = wx.grid.GridTableMessage(
            self, wx.grid.GRIDTABLE_REQUEST_VIEW_GET_VALUES)
        grid.ProcessTableMessage(msg)


    def resetRows(self, grid, before):
        """
        (Grid) -> Reset the grid view.   Call this to
        update the grid if rows and columns have been added or deleted
        """
        grid.BeginBatch()

        current = self.GetNumberRows()

        #print "wxgrid.resetRows(%d,%d)" % (before,current)
             
        if current < before:
            msg = wx.grid.GridTableMessage(
                self,
                wx.grid.GRIDTABLE_NOTIFY_ROWS_DELETED,
                current,before-current)
            grid.ProcessTableMessage(msg)
        elif current > before:
            msg = wx.grid.GridTableMessage(
                self,
                wx.grid.GRIDTABLE_NOTIFY_ROWS_APPENDED,
                current-before)
            grid.ProcessTableMessage(msg)
            
        self._updateValues(grid)

        grid.EndBatch()

        # update the column rendering plugins
        #self._updateColAttrs(grid)

        # update the scrollbars and the displayed part of the grid
        grid.AdjustScrollbars()
        grid.ForceRefresh()


##         # The scroll bars aren't resized (at least on windows)
##         # Jiggling the size of the window rescales the scrollbars
##         h,w = grid.GetSize()
##         grid.SetSize((h+1, w))
##         grid.SetSize((h, w))
##         grid.ForceRefresh()
    
        
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
        #if rowIndex == 0 and colIndex == 0:
        #    print "wxgrid.GetValue(0,0)"
        #if rowIndex == len(self.cells): return "."
        r=self.rows[rowIndex]
        v=r.values[colIndex]
        #if colIndex==1 and rowIndex == 0:
        #    print "GetValue()",v
        if v is None: return ""
        return self.columns[colIndex].format(v)

    def SetValue(self, rowIndex, colIndex, value):
        "required"
        assert self.editor.enabled
        # wieso frm.editing=True ?
        #frm=self.editor.getForm()
        #if not frm.editing:
        #    frm.editing=True
        
##         if not self.editor.rpt.canWrite():
##             return
        
##         if rowIndex == len(self.cells):
##             raise "not yet done"
## ##             args = [None] * len(self.columns)
## ##             args[colIndex] = value
## ##             row = self.editor.rpt.appendRowForEditing(*args)
## ##             self.rows.append(row)
##         else:
##             row = self.cells[rowIndex]
        col=self.columns[colIndex]

        if len(value) == 0:
            v=None
        else:
            #v=col.parse(value,self.editor.rpt.query)
            v=col.parse(value)
            
        #print "SetValue(%d,%d,%s)" % (rowIndex, colIndex, repr(v))
        
        row=self.rows[rowIndex]
        row.lock()
        col.setCellValue(row,v)
        row.unlock()
        
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



## class MyCellEditor(wx.grid.PyGridCellEditor):
## ##     def __init__(self, log):
## ##         self.log = log
## ##         self.log.write("MyCellEditor ctor\n")
## ##         gridlib.PyGridCellEditor.__init__(self)


##     def Create(self, parent, id, evtHandler):
##         """
##         Called to create the control, which must derive from wx.Control.
##         *Must Override*
##         """
##         console.message("MyCellEditor: Create")
##         self._frm = wx.TextCtrl(parent, id, "")
##         self._tc.SetInsertionPoint(0)
##         self.SetControl(self._tc)

##         if evtHandler:
##             self._tc.PushEventHandler(evtHandler)


## ##     def SetSize(self, rect):
## ##         """
## ##         Called to position/size the edit control within the cell rectangle.
## ##         If you don't fill the cell (the rect) then be sure to override
## ##         PaintBackground and do something meaningful there.
## ##         """
## ##         self.log.write("MyCellEditor: SetSize %s\n" % rect)
## ##         self._tc.SetDimensions(rect.x, rect.y, rect.width+2, rect.height+2,
## ##                                wx.SIZE_ALLOW_MINUS_ONE)


##     def Show(self, show, attr):
##         """
##         Show or hide the edit control.  You can use the attr (if not None)
##         to set colours or fonts for the control.
##         """
##         console.message("MyCellEditor: Show(self, %s, %s)" % (show,
##                                                               attr))
##         #self.base_Show(show, attr)


##     def PaintBackground(self, rect, attr):
##         """
##         Draws the part of the cell not occupied by the edit control.  The
##         base  class version just fills it with background colour from the
##         attribute.  In this class the edit control fills the whole cell so
##         don't do anything at all in order to reduce flicker.
##         """
##         console.message("MyCellEditor: PaintBackground")


##     def BeginEdit(self, row, col, grid):
##         """
##         Fetch the value from the table and prepare the edit control
##         to begin editing.  Set the focus to the edit control.
##         *Must Override*
##         """
##         self.startValue = grid.GetTable().GetValue(row, col)
##         console.message("MyCellEditor: BeginEdit (%d,%d) : %s" % (
##             row, col, self.startValue))
## ##         self._tc.SetValue(self.startValue)
## ##         self._tc.SetInsertionPointEnd()
## ##         self._tc.SetFocus()

## ##         # For this example, select the text
## ##         self._tc.SetSelection(0, self._tc.GetLastPosition())


##     def EndEdit(self, row, col, grid):
##         """
##         Complete the editing of the current cell. Returns True if the value
##         has changed.  If necessary, the control may be destroyed.
##         *Must Override*
##         """
##         console.message("MyCellEditor: EndEdit (%d,%d)" % (row, col))
##         changed = False

## ##         val = self._tc.GetValue()
        
## ##         if val != self.startValue:
## ##             changed = True
## ##             grid.GetTable().SetValue(row, col, val) # update the table

## ##         self.startValue = ''
## ##         self._tc.SetValue('')
##         return changed


##     def Reset(self):
##         """
##         Reset the value in the control back to its starting value.
##         *Must Override*
##         """
##         console.message("MyCellEditor: Reset")
##         #self._tc.SetValue(self.startValue)
##         #self._tc.SetInsertionPointEnd()


## ##     def IsAcceptedKey(self, evt):
## ##         """
## ##         Return True to allow the given key to start editing: the base class
## ##         version only checks that the event has no modifiers.  F2 is special
## ##         and will always start the editor.
## ##         """
## ##         self.log.write("MyCellEditor: IsAcceptedKey: %d\n" % (evt.GetKeyCode()))

## ##         ## Oops, there's a bug here, we'll have to do it ourself..
## ##         ##return self.base_IsAcceptedKey(evt)

## ##         return (not (evt.ControlDown() or evt.AltDown()) and
## ##                 evt.GetKeyCode() != wx.WXK_SHIFT)


##     def StartingKey(self, evt):
##         """
##         If the editor is enabled by pressing keys on the grid, this will be
##         called to let the editor do something about that first key if desired.
##         """
##         console.message(
##             "MyCellEditor: StartingKey %d" % evt.GetKeyCode())
##         key = evt.GetKeyCode()
##         ch = None
##         if key in [ wx.WXK_NUMPAD0, wx.WXK_NUMPAD1,
##                     wx.WXK_NUMPAD2, wx.WXK_NUMPAD3, 
##                     wx.WXK_NUMPAD4, wx.WXK_NUMPAD5,
##                     wx.WXK_NUMPAD6, wx.WXK_NUMPAD7, 
##                     wx.WXK_NUMPAD8, wx.WXK_NUMPAD9
##                     ]:

##             ch = ch = chr(ord('0') + key - wx.WXK_NUMPAD0)

##         elif key < 256 and key >= 0 and chr(key) in string.printable:
##             ch = chr(key)
##             if not evt.ShiftDown():
##                 ch = ch.lower()

##         if ch is not None:
##             # For this example, replace the text.  Normally we would append it.
##             #self._tc.AppendText(ch)
##             self._tc.SetValue(ch)
##             self._tc.SetInsertionPointEnd()
##         else:
##             evt.Skip()


##     def StartingClick(self):
##         """
##         If the editor is enabled by clicking on the cell, this method will be
##         called to allow the editor to simulate the click on the control if
##         needed.
##         """
##         console.message("MyCellEditor: StartingClick")


##     def Destroy(self):
##         """final cleanup"""
##         console.message("MyCellEditor: Destroy")
##         self.base_Destroy()


##     def Clone(self):
##         """
##         Create a new object which is the copy of this one
##         *Must Override*
##         """
##         console.message("MyCellEditor: Clone")
##         return MyCellEditor()




class DataGridCtrl(wx.grid.Grid):
    # used by lino.forms.wx.wxtoolkit.DataGrid
    def __init__(self, parent, editor):
        wx.grid.Grid.__init__(self, parent, -1)
        self.table = MyDataTable(editor)
        self.SetTable(self.table,True)
        if True:
            self.SetRowLabelSize(0)
        self.SetMargins(0,0)
        self.AutoSizeColumns(True)
        self.SetSizeHints(400,200)
        
        wx.grid.EVT_GRID_CELL_LEFT_DCLICK(self,
                                          self.OnLeftDClick)
        wx.grid.EVT_GRID_LABEL_RIGHT_CLICK(self,
                                           self.OnLabelRightClicked)

        self.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)


    def OnKeyDown(self, evt):
        
        if evt.KeyCode() == wx.WXK_RETURN:
            if evt.ControlDown():
                #rpt=self.table.editor.rpt
                #frm = self.table.editor.getForm()
                #frm.session.showDataForm(rpt)
                evt.Skip()
                return

            if self.table.editor.choosing:
                frm = self.table.editor.getForm()
                ds = self.table.editor.rpt
                l = self.getSelectedRows()
                if len(l) == 1:
                    self.table.editor.setChosenRow(ds[l[0]])
                    frm.close()
                    return
                else:
                    ui.status("no single row selected!")

            self.DisableCellEditControl()

            if not self.MoveCursorRight(evt.ShiftDown()):
                newRow = self.GetGridCursorRow() + 1

                if newRow < self.GetTable().GetNumberRows():
                    self.SetGridCursor(newRow, 0)
                    self.MakeCellVisible(newRow, 0)
                else:
                    pass
##         elif evt.KeyCode() == wx.WXK_F1:
##             if evt.ControlDown() or evt.ShiftDown() or evt.AltDown():
##                 evt.Skip()
##                 return
##             colIndex = self.GetGridCursorCol()
##             col = self.table.columns[colIndex]
##             frm = self.table.editor.getForm()
##             row = frm.getCurrentRow()
            
##             if col.showSelector(frm,row.item):
##                 self.refresh()
##                 return
##             #print "F1 in column", col.name
##             evt.Skip()
        else:
            evt.Skip()
            return

    def getSelectedCol(self):
        colIndex = self.GetGridCursorCol()
        return self.table.columns[colIndex]

    def getSelectedRow(self):
        return self.table.rows[self.GetGridCursorRow()]

    def getSelectedRows(self):
        lt = self.GetSelectionBlockTopLeft()
        lb = self.GetSelectionBlockBottomRight()
        if len(lt) == 0:
            return [self.GetGridCursorRow()]
        assert len(lb) == len(lt)
        #print lt, lb
        l = []
        for i in range(len(lt)):
            t = lt[i][0]
            b = lb[i][0]
            l += range(t,b+1)
        #l = [i for i in range(t[0],b[0]) ]
        #print "selected rows:", l
        """note: self.GetSelectedCells()
        is always empty in normal selection mode
        """
        return l
    
##         l = self.GetSelectedCells()
##         print len(l), "cells selected"
##         if len(l) == 0:
##             return [self.GetGridCursorRow()]
##         return l

##     def refresh(self):
##         self.table.refresh(self)
        
##     def reload(self):
##         self.table.reload(self)
        
    def OnLeftDClick(self, evt):
        # start cell editor on doubleclick, not only on second click.
        if self.CanEnableCellControl():
             self.EnableCellEditControl()

    def OnLabelRightClicked(self, evt):
        # Did we click on a row or a column?
        row, col = evt.GetRow(), evt.GetCol()
        if row == -1:
            self.colPopup(col, evt)
        elif col == -1:
            print "OnLabelRightClicked(%d,%d)" % (row,col)
            return
        self.rowPopup(row, evt)

##     def Reset(self):
##         """reset the view based on the data in the table.   Call
##         this when rows are added or destroyed"""
##         self.table.ResetView(self)


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
            self.setOrderBy(self.GetSelectedCols())
            self.ForceRefresh()
            #print "ForceRefresh"

        #EVT_MENU(self, id1, delete)
        #if len(cols) == 1:
        wx.EVT_MENU(self, sortID, setSortColumn)
        self.PopupMenu(menu, wx.Point(xo, 0))
        menu.Destroy()
             
    def setOrderBy(self,colIndexes):
        #print __name__, colIndexes
        cols=[self.columns[i] for i in colIndexes]
        #print __name__,cn
        self.rpt.sortColumns=tuple(cols)
        self._load()
        self._refresh()
##     def setOrderBy(self,colIndexes):
##         #print __name__, colIndexes
##         cn = " ".join([self.columns[i].name for i in colIndexes])
##         #print __name__,cn
##         self.editor.rpt.setOrderBy(cn)
##         self.reload()

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

        
        
        
