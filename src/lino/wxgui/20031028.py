import wx
import wx.grid


class Report:
	
	def __init__(self):
		self.rows = []
		self.rows.append((1,"Luc","Eupen"))
		self.rows.append((2,"Lennart","Tallinn"))
		self.rows.append((3,"Bill","Redmont"))

		self.columns = []
		self.columns.append("Id")
		self.columns.append("Name")
		self.columns.append("Town")
		
	def getLabel(self):
		return "Famous people"




class MyDataTable(wx.grid.PyGridTableBase):

	def __init__(self, report):
		wx.grid.PyGridTableBase.__init__(self)
		self.report = report
		self.columns = report.columns
		self.rows = report.rows
		self.cellattrs = []
		for col in self.columns:
			cellattr = wx.grid.GridCellAttr()
			cellattr.SetEditor(wx.grid.GridCellTextEditor())
			cellattr.SetRenderer(wx.grid.GridCellStringRenderer())
			self.cellattrs.append(cellattr)

	def GetNumberRows(self): return len(self.rows) + 1
	def GetNumberCols(self): return len(self.columns)
		
## 	def IsEmptyCell(self, row, col):
## 		"required"
## 		#print "IsEmptyCell(%d,%d) -> %d" % (row, col, len(self.columns))
## 		return self.GetValue(row,col) is None # self.data[row][col]

	def GetValue(self, rowIndex, colIndex):
		#ret = ''
		try:
			return self.rows[rowIndex][colIndex]
			# ret = self.columns[colIndex].GetCellValue(row)
		except IndexError:
			return None

	def GetAttr(self,r,c,x):
		"overridden to handle attributes directly in the table"
		print "GetAttr(%d,%d,%d) -> %s" % (r, c, x, repr(self.cellattrs[c]))
		return self.cellattrs[c]
		
	def GetColLabelValue(self, col):
		"Called when the grid needs to display labels"
		return self.columns[col]

		
class RptGrid(wx.grid.Grid):
	def __init__(self, parent, report):
		wx.grid.Grid.__init__(self, parent, -1)
		table = MyDataTable(report)
		self.SetTable(table,True)
		
## 		i = 0
## 		for attr in table.cellattrs:
## 			 self.SetColAttr(i,attr)
## 			 i += 1
			
		# some options of wxGrid:
		self.SetRowLabelSize(0)
		self.SetMargins(0,0)
		#print "RptGrid.__init__()"
		#self.AutoSizeColumns(True)
		
## 		wx.grid.EVT_GRID_CELL_LEFT_DCLICK(self, self.OnLeftDClick)

## 	def OnLeftDClick(self, evt):
## 		if self.CanEnableCellControl():
## 			 self.EnableCellEditControl()
		
		
class RptFrame(wx.Frame):
	def __init__(self, parent, id, report):
		title = report.getLabel()
		wx.Frame.__init__(self, parent, id, title)
  		self.grid = RptGrid(self,report)
	
	


class MyApp(wx.App):

	def __init__(self,report):
		self.report = report
		wx.App.__init__(self,0)
		
	def OnInit(self):
		wx.InitAllImageHandlers()
		frame = RptFrame(None,-1,self.report)
		# frame = MainFrame(None, -1, self.ui)
		frame.Show()
		self.SetTopWindow(frame)
		return True



if __name__ == '__main__':

	report = Report()
	app = MyApp(report)
	app.MainLoop()
	
	# GetAttr(2,2,0) -> wxPython wrapper for DELETED wxGridCellAttr object! (The C++ object no longer exists.)
	
	
