#----------------------------------------------------------------------
# ID:        $Id: report.py,v 1.15 2004/07/31 07:13:46 lsaffre Exp $
# Copyright: (c) 2003-2004 Luc Saffre
# License:	 GPL
#----------------------------------------------------------------------

import types

from lino.misc.descr import Describable
from paramset import ParamOwner



class Report(ParamOwner):

	paramNames = {
		"label" : None,
		"rowHeight" : 3,
		"description" : None,
		"columnNames" : None,
		"columnWidths" : None,
		}
		
	def __init__(self, ds, name, **kw):

		self.name = name
		self._clist = ds._clist
		self._ds = ds

		self.configure(**kw)

	def onConfigure(self,unknownParams):
		assert len(unknownParams) == 0
		self._columns = []
		if self.columnNames is None:
			for col in self._clist.visibleColumns:
				self.addColumn(col)
		else:
			for colName in self.columnNames.split():
				col = self._clist.columnList.getColumn(colName)
				self.addColumn(col)
			
		if self.columnWidths is not None:
			i = 0
			for item in self.columnWidths.split():
				self._columns[i].preferredWidth = int(item)
				i += 1

## 	def child(self,name,**kw):
## 		d = self.myParams()
## 		d.update(kw)
## 		return Report(self._query,name,**d)

	def getLabel(self):
		if self.label is None:
			return self._ds.getLabel()
		return self.label
		

##  	def execute(self,db,renderer,tpl):
		
## 		ds = db.datasource(self._query)
			
## 		if self.pageLen is None:
## 			self.lastPage = 1
## 		elif len(ds) == 0:
## 			self.lastPage = 1
## 		else:
## 			#rowcount = len(self)
## 			#rowcount = self.area._connection.executeCount(
## 			#	self.query,**kw)
				
## 			#rowCount = self.executeCount
## 			#rowCount = area._connection.executeCount(self.query)
## 			self.lastPage = int((len(ds)-1) / self.pageLen) + 1
## 			"""
## 			if pageLen is 10:
## 			- [0..10] rows --> 1 page
## 			- [11..20] rows --> 2 pages
## 			- [21..30] rows --> 2 pages
## 			- 10 rows --> 1 page
## 			- 11 rows --> 2 pages
## 			"""
## 		pageNum = self.pageNum
		
## 		if self.pageLen is None:
## 			limit = offset = None
## 			rowcount = 0
## 		else:
## 			if pageNum is None:
## 				pageNum=1
## 			elif pageNum < 0:
## 				pageNum = self.lastPage + pageNum - 1
## 			elif pageNum > self.lastPage:
## 				raise "pageNum > lastPage",self.lastPage
## 			rowcount = offset = self.pageLen*(pageNum-1) # +1
## 			limit = self.pageLen
		
## 		tpl.renderHeader(ds,renderer,self,pageNum)
		
## 		for atomicRow in ds.execute(offset=offset,limit=limit):
## 			rowcount += 1
## 			tpl.renderLine(ds,renderer,self,pageNum,
## 								rowcount,atomicRow)

## 		tpl.renderFooter(ds,renderer,self,pageNum)

		
		
	def addColumn(self,queryCol,label=None,preferredWidth=None):
		#queryCol = self.dh.query.getColumn(colName)
		if label is None:
			label = queryCol.name
		col = ReportColumn(queryCol,label,preferredWidth)
		self._columns.append(col)




	def defineMenus(self,win):
		#self.initQuery()
		mb = win.addMenuBar("data","&Data menu")
		mnu = mb.addMenu("&Row")
		mnu.addItem("&Append",self.mnu_appendRow,win)
		# mnu.addItem("&Delete",self.mnu_deleteRow)
		# w.addGrid(self)
		# return mb
		mnu = mb.addMenu("&File")
		mnu.addItem("E&xit",win.close)

	def mnu_appendRow(self,win):
		print win.getSelectedRows()
## 		row = self.appendRow()
## 		ui.message("new row has been created")
## 		return row.ui_openFormWindow(ui)

		
	#def load(self):

## 	def save(self):
## 		assert self.generated
## 		filename = self.name + ".rpt"
## 		f = open(filename)
## 		f.write("self.generated = True\n")
## 		for col in self._columns:
## 			f.write("self.addColumn(name=%s,label=%s,preferredWidth=%d)\n" %
## 					  (repr(col.name), repr(col.getLabel()), col.preferredWidth))

	


 	def getColumns(self):
 		return self._columns



class ReportColumn: #(Describable):
	
	def __init__(self,queryCol,label, preferredWidth,
					 description=None):
## 		Describable.__init__(self,
## 									parent=queryCol.rowAttr,
## 									label=label,
## 									description=description)
## 		assert self._label == label,\
## 				 "%s is not %s" % (repr(self._label),repr(label))
		self.queryCol = queryCol
		if label is None:
			label = queryCol.name
		self._label = label
		self.preferredWidth = preferredWidth
		

	def getPreferredWidth(self):
		if self.preferredWidth:
			return self.preferredWidth
		return self.queryCol.rowAttr.getPreferredWidth()

	def render(self,value):
		return str(value).ljust(self.getPreferredWidth())


	def getLabel(self):
		return self._label

