#----------------------------------------------------------------------
# ID:        $Id: report.py,v 1.15 2004/07/31 07:13:46 lsaffre Exp $
# Copyright: (c) 2003-2004 Luc Saffre
# License:	 GPL
#----------------------------------------------------------------------

import types

from lino.misc.descr import Describable
#from paramset import ParamOwner
from datasource import Datasource
from query import DataColumnList, DataColumn



class Report(Datasource,Describable):

	#columnClass = ReportColumn

	def __init__(self,
					 session, store, clist=None,
					 name=None,
					 label=None,
					 doc=None,
					 **kw):
		Datasource.__init__(self,session,store,clist,**kw)
		Describable.__init__(self,name,label,doc)

		self.config(**kw)

	def config(self,
				  rowHeight=3,
				  pageNum=None,
				  pageLen=None,
				  columnWidths=None, **kw):
		Datasource.config(self,**kw)
		
		if columnWidths is not None:
			vc = self.getVisibleColumns()
			i = 0
			for item in columnWidths.split():
				vc[i].preferredWidth = int(item)
				i += 1

		self.rowHeight = rowHeight
		self.columnWidths = columnWidths
		self.pageNum = pageNum
		self.pageLen = pageLen
		if self.pageLen is None:
			self.lastPage = 1
		elif len(self) == 0:
			self.lastPage = 1
		else:
			self.lastPage = int((len(self)-1) / self.pageLen) + 1
			"""
			if pageLen is 10:
			- [0..10] rows --> 1 page
			- [11..20] rows --> 2 pages
			- [21..30] rows --> 2 pages
			- 10 rows --> 1 page
			- 11 rows --> 2 pages
			"""

		"""note: pageNum can be None even if pageLen isn't.  This will
		default to either 1 OR lastPage with a future option
		"fromBottom" """
		
	def apply_GET(self,**kw):
		#rptParams = {}
		#dsParams = {}
		p = {}
		for k,v in kw.items():
			if k == 'pg':
				p['pageNum'] = str(v[0])
			elif k == 'pl':
				p['pageLen'] = str(v[0])
			else:
				p[k] = v
		Datasource.apply_GET(self,**p)
		#self.config(**rptParams)
		
	def get_GET(self):
		p = Datasource.get_GET(self)
		if self.pageNum != None:
			p['pg'] = self.pageNum
		if self.pageLen != None:
			p['pl'] = self.pageLen
		return p
		

	def setdefaults(self,kw):
		kw.setdefault('columnWidths',self.columnWidths)
		kw.setdefault('rowHeight',self.rowHeight)
		kw.setdefault('pageNum',self.pageNum)
		kw.setdefault('pageLen',self.pageLen)
		Datasource.setdefaults(self,kw)

	def createColumnList(self,columnNames):
 		# overrides Datasource.createColumnList
		return ReportColumnList(self._store,
										self._session,
										columnNames)
	
	def executeSelect(self,
							limit=None,
							offset=None,**kw):
		# overrides Datasource.executeSelect()
		"""
		modify limit and offset to contain self.pageNum and self.pageLen
		
		"""
		assert limit is None # untested case...
		assert offset is None # untested case...
		if self.pageLen is not None:
			limit = self.pageLen
			if self.pageNum is None:
				self.pageNum=1
			elif self.pageNum < 0:
				self.pageNum = self.lastPage + self.pageNum - 1
			elif self.pageNum > self.lastPage:
				raise "pageNum > lastPage",self.lastPage
			offset = self.pageLen * (self.pageNum-1)
		
		return self._connection.executeSelect(self, limit=limit,
														  offset=offset, **kw )

class ReportColumnList(DataColumnList):
	
	def createColumn(self, colIndex, name, join,fld):
		# overridden from DataColumnList
		return ReportColumn(self,colIndex, name, join,fld)



class ReportColumn(DataColumn,Describable):
	
	def __init__(self,clist,colIndex,name,join,rowAttr,
					 label=None, doc=None,preferredWidth=None):
		if label is None:
			label = name
		DataColumn.__init__(self,clist,colIndex,name,join,rowAttr)
 		Describable.__init__(self, name,label,doc)
		self.preferredWidth = preferredWidth
		

	def getPreferredWidth(self):
		if self.preferredWidth:
			return self.preferredWidth
		return self.rowAttr.getPreferredWidth()

## 	def render(self,value):
## 		return str(value).ljust(self.getPreferredWidth())


## 	def getLabel(self):
## 		return self._label

