#----------------------------------------------------------------------
# $Id: query.py,v 1.22 2004/04/25 18:06:14 lsaffre Exp $
# Copyright: (c) 2003-2004 Luc Saffre
# License:	 GPL
#----------------------------------------------------------------------

import types
from lino.misc.compat import *
from lino.misc.etc import issequence

from datasource import Datasource
from report import Report
from columnlist import ColumnList
from paramset import ParamOwner
import datatypes




class AbstractQuery(ParamOwner):

	paramNames = {
		"columnNames" : None,
		"orderBy" : None,
		"filters" : None,
		"search" : None,
		#"samples" : None,
		"atomicSamples" : None,
		}
	
	def __init__(self,name,**kw):
		self.name = name
		self._reports = {}
		self.configure(**kw)
		
		
	def onConfigure(self, unknownParams):
		
		self.columnList = ColumnList(self)
		self.getColumns = self.columnList.getColumns
		
		l = []
		for name in self.leadTable.getPrimaryKey():
			l.append(self.columnList.provideColumn(name))
		self._pkColumns = tuple(l)

		assert type(self.columnNames) is types.StringType
		l = []
		for colName in self.columnNames.split():
			l.append(self.columnList.provideColumn(colName))
		self.visibleColumns = tuple(l)
			
		l = []
 		if self.orderBy is not None:
 			for colName in self.orderBy.split():
 				l.append(self.columnList.provideColumn(colName))
		self.orderByColumns = tuple(l)

		for colName in unknownParams.keys():
			self.columnList.provideColumn(colName)

		self.columnList.setupAtoms()
		
		#self.atoms2values = self.columnList.atoms2values

		self.setSamples(**unknownParams)
		
		"""values in atomicSamples must be strings to be parsed
		according to atomic type"""

		if False:
		
			l = []
			if self.atomicSamples is not None:
				for (k,v) in self.atomicSamples.items():
					a = self.columnList.getAtom(k)
					l.append( ( a, a.type.parse(v) ) )
			self.atomicSamplesColumns = tuple(l)

		self.onSetFilters()
			
			
## 	def parseSamples(self,**kw):
## 		for n in kw.keys():
## 			self.provideColumn(n)
## 			# just to check

## 	def provideColumn(self,name):
## 		return self.columnList.provideColumn(self.leadTable,name)

	def setSamples(self,**kw):
		samples = []
		l = []
		atomicRow = [None] * len(self.columnList._atoms)
		
		for (name,value) in kw.items():
			col = self.columnList.getColumn(name)
			samples.append( (col,value) )

			col.rowAttr.value2atoms(value,atomicRow,col.getAtoms())
								 
			for atom in col.getAtoms():
				l.append( (atom, atomicRow[atom.index]) )
				
		self.sampleColumns = tuple(l)
		self.samples = tuple(samples)
		

	def setCsvSamples(self,area,**kw):
		"each value is a (comma-separated) string"
		samples = []
		l = []
		atomicRow = [None] * len(self.columnList._atoms)
		for (name,value) in kw.items():
			col = self.columnList.getColumn(name)

			rid = value.split(',')
			i = 0
			for atom in col.getAtoms():
				atomicRow[atom.index] = atom.type.parse(rid[i])
				i += 1
				
			value = col.atoms2value(atomicRow, area)
			samples.append( (col,value) )
				
			for atom in col.getAtoms():
				l.append( (atom, atomicRow[atom.index]) )
				
		self.samples = tuple(samples)
		self.sampleColumns = tuple(l)
		

			

	def setFilter(self,*args):
		self.filters = args
		self.onSetFilters()
		
	def onSetFilters(self):
		"""
		filters must be a sequence of strings containing SQL expressions
		"""
		
		l = []
		if self.filters is not None:
			assert issequence(self.filters), repr(self.filters)
			for expr in self.filters:
				assert type(expr) == types.StringType
				l.append(expr)
		#self.filterExp = tuple(l)

		if self.search is not None:
			if not issequence(self.search):
				self.search = (self.search,)
			# search is a tuple of strings to search for
			atoms = self.getSearchAtoms()
			for expr in self.search:
				l.append(" OR ".join(
					[a.name+" LIKE '%"+expr+"%'" for a in atoms]))
				
		self.filterExpressions = tuple(l)
		

	def atoms2values(self,atomicRow,area):
 		return [col.atoms2value(atomicRow,area)
 				  for col in self.visibleColumns]
	

 	def report(self,name,**kw):
		try:
			r = self._reports[name]
		except KeyError,e:
			
			# todo : here we define a new report. This should be
			# prohibited after schema startup...
			
			r = Report(self,name=name,**kw)
			self._reports[name] = r
			return r
		if len(kw) == 0:
			return r
		return r.child(name,**kw)

	def getName(self):
		return self.name

	def getAtoms(self):
		return self.columnList.getAtoms()


	def appendRow(self,area,*args,**kw):
		"""

		create a persistent row in this Query's leadTable.  args are the
		values of the new Row and must be specified in the order of the
		query's columns.
		
		"""
		if len(args):
			#print __file__, [col.name for col in self.visibleColumns]
			#vc = self.query._columnList.split()
			assert len(args) <= len(self.visibleColumns), \
					 "%d values given, but %d values expected" % \
					 (len(args),len(self.visibleColumns))
			i = 0
			#for colName in vc:
			#	col = self.query.getColumn(colName)
			for col in self.visibleColumns:
				if i == len(args):
					break
				if col.join is None:
					kw[col.rowAttr.name] = args[i]
				else:
					assert args[i] is None, \
							 "cannot appendRow with value outside of leadTable"
				i += 1
				
		
		for (col,value) in self.samples:
			kw[col.rowAttr.name] = value

			
		id = self.values2id(kw)

		return area.storeRow(id,kw)



	def setCellValue(self,area,rowIndex,colIndex,value):
		col = self.visibleColumns[colIndex]
		
		atomicRow = self[rowIndex]
		oldValue = col.atoms2value(atomicRow,area)
		row = self.atoms2instance(atomicRow)
		row.lock()
		setattr(row,col.rowAttr.name,value)
		row.unlock()
		row.commit()
		# print oldValue,value
		

	def getLeadColumnList(self):
		raise NotImplementedError





class Query(AbstractQuery):
	
	def __init__(self, leadTable, name, columnNames=None,**kw):
		self.leadTable = leadTable
		if columnNames is None:
			columnNames = leadTable.getColumnList()
		AbstractQuery.__init__(self,name,columnNames=columnNames,**kw)

	def child(self,name,**kw):
		d = self.myParams()
		for col,value in self.samples:
			d[col.name] = value
		d.update(kw)
## 		if kw.has_key('search'):
## 			print '20040418 :' + str(d)
## 		if self.leadTable.name == 'CITIES':
## 			print d
		return Query(self.leadTable,name,**d)

	def getSearchAtoms(self):
		l = []
		for col in self.visibleColumns:
			if hasattr(col.rowAttr,'type'):
				if isinstance(col.rowAttr.type,datatypes.StringType):
					l += col.getAtoms()
		return tuple(l)
		#return ('title','abstract','body')		
		
## 	def getPrimaryAtoms(self):
## 		return self.leadTable.getPrimaryAtoms()
		
## 	def getLeadColumnList(self):
## 		return self.leadTable.getColumnList()
	
	def atoms2instance(self,atomicRow,area):

		"""returns a leadTable row instance which contains the values of
		the specified atomic row. """

		d = {}
		self.columnList.atoms2dict(atomicRow,d,area)
		#print d
		
		# the primary key atoms of the leadTable are always the first
		# ones
		pklen = len(self.leadTable.getPrimaryAtoms())
		row = area.provideRowInstance(atomicRow[:pklen],
												knownValues=d,
												new=False)
		
		# todo : `fillMode` to indicate that known atoms are expected to
		# match if row was in cache

		
		
		return row

	def getSqlSelect(self,conn,**kw):
		return self.columnList.getSqlSelectTable(conn,
															  self,
															  self.leadTable,
															  **kw)


	def commit(self):
		self.leadTable.commit()

	def datasource(self,db):
		area = getattr(db,self.leadTable.name)
		return Datasource(area,self)
		

	def values2id(self,knownValues):
		"convert dict of knownValues to sequence of pk atoms"
		#print knownValues
		pka = self.leadTable.getPrimaryAtoms()
		
		id = [None] * len(pka)
		#print self.name, knownValues
		for col in self._pkColumns:
			col.dict2atoms(knownValues,id)
		return id


	
	
	def dict2atoms(self,valueDict,atomicRow):
		for col in self.columnList._columns:
			col.dict2atoms(valueDict,atomicRow)
		








## class Filter:
##		def __init__(self,op,value):
		
##			assert op in ('=','>','<','~')
##			self.op = op
##			self.value = value

##		def try(self,testValue):
##			if self.op == "=":
##				return self.value == testValue
##			if self.op == ">":
##				return testValue > self.value
##			if self.op == "<":
##				return testValue < self.value
##			return self.value in testValue
		
	




