#----------------------------------------------------------------------
# ID:        $Id: report.py,v 1.15 2004/07/31 07:13:46 lsaffre Exp $
# Copyright: (c) 2003-2004 Luc Saffre
# License:	 GPL
#----------------------------------------------------------------------

import types

from lino.misc.descr import Describable
#from paramset import ParamOwner
from datasource import Datasource, DataColumnList



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

	def config(self, rowHeight=3, columnWidths=None, **kw):
		self.rowHeight = rowHeight
		self.columnWidths = columnWidths
		if columnWidths is not None:
			i = 0
			for item in columnWidths.split():
				self._columns[i].preferredWidth = int(item)
				i += 1

		Datasource.config(self,**kw)

	def setdefaults(self,kw):
		kw.setdefault('columnWidths',self.columnWidths)
		kw.setdefault('rowHeight',self.rowHeight)
		Datasource.setdefaults(self,kw)

	def createColumnList(self,columnNames):
 		# overridden from Datasource
		return ReportColumnList(self._store,
										self._session,
										columnNames)
	
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

