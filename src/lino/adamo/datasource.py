#----------------------------------------------------------------------
# ID:        $Id: datasource.py,v 1.6 2004/07/31 07:13:46 lsaffre Exp $
# Copyright: (c) 2003-2004 Luc Saffre
# License:	 GPL
#----------------------------------------------------------------------

import types

from lino.misc.etc import issequence
from query import ColumnList, BaseColumnList
from datatypes import DataVeto
from report import Report
from rowattrs import FieldContainer, NoSuchField

class Datasource:

	"""
	A Datasource is the central handle for a stream of data. 
	"""
	
	def __init__(self, session, store, clist=None, **kw):
		self.rowcount = None
		self._session = session
		#self._context = context
		self._store = store
		#self._query = query
		if clist is None:
			clist = store._peekQuery
		assert clist.leadTable is store._table
		self._clist = clist
		#self.report = clist.report

		self._db = store._db # shortcut
		self._table = store._table # shortcut
		self._schema = self._db.schema # shortcut
		self._connection = store._connection # shortcut

		store.registerDatasource(self)
		
		for name in ('startDump','stopDump'):
			setattr(self,name,getattr(store._connection,name))

		self._samples = {}
		
		self.config(**kw)

	def config(self,viewName=None,**kw):
		"""
		
		note: _config() is a separate method because the viewName
		parameter may control the default values for the other keywords.
		
		"""
		self._viewName = viewName
		if viewName is not None:
			view = self._table.getView(viewName)
			if view is None:
				raise KeyError,viewName+": no such view"
			for k,v in view.items():
				kw.setdefault(k,v)
		self._config(**kw)
		
		
	def _config(self,
				  columnNames=None,
				  orderBy=None,
				  sqlFilters=None,
				  search=None,
				  samples=None,
				  label=None,
				  **kw):
		self._label = label
		if columnNames is not None:
			self._clist = ColumnList(self._store,columnNames)
		self.setOrderBy(orderBy)
		self.setFilterExpressions(sqlFilters,search)
		
		if samples is None:
			self.setSamples(**kw)
		else:
			assert len(kw) == 0
			self._samples = {}
			self.setSamples(**samples)

	def apply_GET(self,**kw):
		qryParams = {}
		csvSamples = {}
		for k,v in kw.items():
			if k == 'ob':
				qryParams['orderBy'] = " ".join(v)
			elif k == 'v':
				viewName = v[0]
				if viewName == '':
					viewName = None
				qryParams['viewName'] = viewName
			elif k == 'search':
				qryParams['search'] = v[0]
			elif k == 'flt':
				qryParams['sqlFilters'] = v
				#qryParams['sqlFilters'] = (v[0],)
				#qryParams['filters'] = tuple(l)

			else:
				csvSamples[k] = v[0]
				
		self.config(**qryParams)
		if len(csvSamples) > 0:
			self.setCsvSamples(**csvSamples)

	def get_GET(self):
		p = {}
		if self._orderBy != None:
			p['ob'] = self._orderBy
		if self._viewName != None:
			p['v'] = self._viewName
		if self._search != None:
			p['search'] = self._search
		if self._sqlFilters != None:
			p['flt'] = self._sqlFilters
		for (key,value) in self._samples.items():
			col = self._clist.getColumn(key)
			p[key] = col.format(value,self)
		return p
		
			
## 	def getView(self,viewName):
## 		return self._table.getView(viewName)

	def query(self,columnNames=None,samples=None,**kw):
		
		"""creates a child (a detached copy) of this.  Modifying the
		child won't affect the parent.  columnNames can optionally be
		specified as first (non-keyword) argument.  if arguments are
		given, then they override the corresponding value in the parent.
		
		"""
		#print kw
		kw.setdefault('orderBy',self._orderBy)
		kw.setdefault('search',self._search)
		if self._label is not None:
			kw.setdefault('label',self._label)
		if self._sqlFilters is not None:
			kw.setdefault('sqlFilters',tuple(self._sqlFilters))
		if samples is None:
			for k,v in self._samples.items():
				kw.setdefault(k,v)
		#print kw
		
		clist = self._clist
		if columnNames is not None:
			clist = ColumnList(self._store,columnNames)			
			#clist = clist.child(columnNames)
		#query = self._area._table.query(columnNames=columnNames,**kw)
		ds = Datasource(self._session,
							 self._store,
							 clist,
							 samples=samples,
							 **kw)
		return ds


  	def report(self,name,**kw):
 		return Report(self,name,**kw)

	def getRenderer(self,rsc,req,writer=None):
		return self._schema._datasourceRenderer(rsc,req,
															 self.query(),
															 writer)
	
	def getContext(self):
		return self._session.getContext()

	def getTableName(self):
		return self._table.getTableName()
	
	def getLabel(self):
		if self._label is None:
			lbl = self._table.getLabel()
			if len(self._samples) > 0:
				lbl += " ("
				for (k,v) in self._samples.items():
					col = self._clist.getColumn(k)
					lbl += col.name + "=" \
							 + col.rowAttr.format(v)
				lbl += ")"
			return lbl
		if callable(self._label):
			return self._label(self)
		return self._label
			

	def setOrderBy(self,orderBy):
		#assert type(orderBy) is type('')
		self._orderBy = orderBy
		l = []
 		if orderBy is not None:
 			for colName in orderBy.split():
 				l.append(self._clist.provideColumn(colName))
		self.orderByColumns = tuple(l)

	def setSamples(self,**kw):
		"each value is a Python object"
		self._samples.update(kw)
		for (name,value) in self._samples.items():
			col = self._clist.provideColumn(name)
		return
	
	def setCsvSamples(self,**kw):
		"each value is a string to be parsed by column"
		#self._samples.update(kw)
		for (name,value) in kw.items():
			col = self._clist.provideColumn(name)
			self._samples[name] = col.parse(value,self)
		return
	
	def setSamples_unused(self):
		sampleColumns = []
		atomicSamples = []
		atomicRow = self._clist.makeAtomicRow(self._context) 

		#tmpRow = self._table.Row(self,{},False,pseudo=True)
		
		for (name,value) in self._samples.items():
			col = self._clist.getColumn(name)
			#attr = self._table.getRowAttr(name)
			sampleColumns.append( (col,value) )
			#setattr(tmpRow,name,value)
			#attr.setCellValue(tmpRow,value)
			col.value2atoms(value,atomicRow,self._context)
			
		self.sampleColumns = tuple(sampleColumns)
		
		#atomicRow = self.row2atoms(tmpRow)
		for col,value in self.sampleColumns:
			for atom in col.getAtoms():
				atomicSamples.append((atom,atomicRow[atom.index]))
## 			for aname,atype in attr.getNeededAtoms(self._db):
## 				atomicSamples.append(
## 					(aname,atype, tmpRow.getAtomicValue(aname)) )
				
		self.atomicSamples = tuple(atomicSamples)
		
	def getAtomicSamples(self):
		l = []
		atomicRow = self._clist.makeAtomicRow() 
		for (name,value) in self._samples.items():
			col = self._clist.getColumn(name)
			col.value2atoms(value,atomicRow,self._session.getContext())
			for atom in col.getAtoms():
				l.append((atom,atomicRow[atom.index]))
		return l
			
## 	def setCsvSamples(self,**kw):
## 		"each value is a (comma-separated) string"
## 		sampleColumns = []
## 		atomicSamples = []
## 		tmpRow = self._table.Row(self,{},False,pseudo=True)
## 		for (name,value) in kw.items():
## 			attr = self._table.getRowAttr(name)

## 			rid = value.split(',')
## 			i = 0
## 			for aname,atype in attr.getNeededAtoms(self._db):
## 				tmpRow.setAtomicValue(aname,atype.parse(rid[i]))
## 				i += 1
				
## 			value = attr.getCellValue(tmpRow)
## 			sampleColumns.append( (attr,value) )
## 			self._samples[name] = value
				
## 			for aname,atype in attr.getNeededAtoms(self._db):
## 				atomicSamples.append(
## 					(aname,atype, tmpRow.getAtomicValue(aname)) )
				
## 		self.sampleColumns = tuple(sampleColumns)
## 		self.atomicSamples = tuple(atomicSamples)


	def setSqlFilters(self,*sqlFilters):
		self.setFilterExpressions(sqlFilters,self._search)
		
	def setSearch(self,search):
		self.setFilterExpressions(self._sqlFilters,search)
		
	def getVisibleColumns(self):
		return self._clist.visibleColumns
	
	def getAttrList(self):
		return self._table.getAttrList()
	
	def setFilterExpressions(self, sqlFilters, search):
		"""
		filters must be a sequence of strings containing SQL expressions
		"""
		self._sqlFilters = sqlFilters
		self._search = search
		
		l = []
		if self._sqlFilters is not None:
			assert issequence(self._sqlFilters), repr(self._sqlFilters)
			for expr in self._sqlFilters:
				assert type(expr) == types.StringType
				l.append(expr)
		#self.filterExp = tuple(l)

		if self._search is not None:
			if not issequence(self._search):
				self._search = (self._search,)
			# search is a tuple of strings to search for
			atoms = self._clist.getSearchAtoms()
			for expr in self._search:
				l.append(" OR ".join(
					[a.name+" LIKE '%"+expr+"%'" for a in atoms]))
				
		self.filterExpressions = tuple(l)
		


## 	def __str__(self,):
## 		return self._table.__class__.__name__+"Datasource"

	def __repr__(self,):
		return self._table.__class__.__name__+"Datasource"

	def getAtoms(self):
		return self._clist.getAtoms()


	def getName(self):
		return self._table.getTableName()+"Source"

## 	def getRowId(self,values):
## 		return [values.get(name,None)
## 				  for (name,type) in self._table.getPrimaryAtoms()]

	def executePeek(self,id):
		return self._connection.executePeek(self._clist,id)


	def appendRow(self,*args,**kw):
		#if self._table.getTableName() == "PARTNERS":
		#	print "datasource.py", args
		#	print [col.name for col in self._clist.visibleColumns]
		#self.startDump()
		row = self._table.Row(self,{},True)
		row.lock()
		kw.update(self._samples)
		self._clist.updateRow(row,*args,**kw)
		self.rowcount = None
		self._store.setAutoRowId(row)
		row.unlock()
		self._store.fireUpdate()
		#print self.stopDump()
		return row


	def __getitem__(self,offset):
		row = self.getRowAt(offset)
		if row is None:
			msg = "%s[%d] (%d) rows" % (self._table.getTableName(),
												 offset,len(self))
			raise IndexError,msg
		
		return row

	def getRowAt(self,offset):
		assert type(offset) is types.IntType
		if offset < 0:
			offset = len(self) + offset 
		csr = self.executeSelect(offset=offset,limit=1)
		if csr.rowcount == 0:
			return None
		assert csr.rowcount == 1
		atomicRow = csr.fetchone()
		# d = self._clist.at2d(atomicRow)
		# return self._table.Row(self,d,False)
		return self.atoms2row(atomicRow,False)


	def peek(self,*id):
		assert len(id) == len(self._clist._pkColumns),\
				 "expected %d values but got %s" % \
				 ( len(self._clist._pkColumns), repr(id))
		# flatten the id :
		l = []
		i = 0
		for col in self._clist._pkColumns:
			l += col.rowAttr.value2atoms(id[i],self._session.getContext())
			i+=1
			
## 		i = 0
## 		for atomicValue in id:
## 			if isinstance(atomicValue,DataRow):
## 				l += atomicValue.getRowId()
## 			else:
## 				l.append(atomicValue)
		atomicRow = self._connection.executePeek(self._clist,l)
		if atomicRow is None:
			return None
		#d = self._clist.at2d(atomicRow)
		#return self._table.Row(self,d,False)
		return self.atoms2row(atomicRow,False)

	def getInstance(self,atomicId,new):
		row = self._table.Row(self,{},new)
		i = 0
		for col in self._clist._pkColumns:
			col.atoms2row(atomicId,row)
			#col.setCellValue(row,atomicId[i])
			i+=1
		return row
			
		

## 	def find(self,**knownValues):
## 		atomicRow = self._clist.makeAtomicRow()
## 		flt = []
## 		atoms = []
## 		for k,v in knownValues.items():
## 			col = self._clist.getColumn(k)
## 			col.value2atoms(v,atomicRow,self._context)
## 			atoms += col.getFltAtoms(self._context)
## 		for a in atoms:	
## 			flt.append(self._connection.testEqual(a.name,
## 															  a.type,
## 															  atomicRow[a.index]))
## 		ds = self.query(sqlFilters=(' AND '.join(flt),))
## 		return ds
		
	def find(self,*args,**knownValues):
		flt = []
		i = 0
		for arg in args:
			col = self._clist.visibleColumns[i]
			flt.append(col.getTestEqual(self,arg))
			i+=1
		for k,v in knownValues.items():
			col = self._clist.getColumn(k)
			flt.append(col.getTestEqual(self,v))
		ds = self.query(sqlFilters=(' AND '.join(flt),))
		return ds
		
	def findone(self,**knownValues):
		ds = self.find(**knownValues)
		#print [a.name for a in ds.query._atoms]
		#q = self._table.query(filters=' AND'.join(flt))
		#csr = self._connection.executeSelect(q)
		csr = ds.executeSelect()
		if csr.rowcount != 1:
			#print "findone(%s) found %d rows" % ( repr(knownValues),
			#csr.rowcount))
			return None
			#raise DataVeto("findone(%s) found %d rows" % (
			#	repr(knownValues), csr.rowcount))
		
		atomicRow = csr.fetchone()
		#d = self._clist.at2d(atomicRow)
		#return self._table.Row(self,d,False)
		return self.atoms2row(atomicRow,False)
	

		
	def atoms2row(self,atomicRow,new):
		row = self._table.Row(self,{},new)
		self._clist.atoms2row(atomicRow,row)
		return row
## 		return DataRow(self,atomicRow,new)
## 		assert atomicRow is not None
## 		atomicDict = self._query.at2d(atomicRow)
## 		return self._store.ad2row(atomicDict,new)


	def getSqlSelect(self,**kw):
		return self._connection.getSqlSelect(self,**kw)
		#return self._clist.getSqlSelect(self._connection,**kw)

## 	def setCsvSamples(self,**kw):
## 		self._query.setCsvSamples(self._area,**kw)
		
	def __iter__(self):
		return DataIterator(self)
	
	def iterate(self,**kw):
		
		"""returns an iterator who returns a tuple of atomic values for
		each row"""
		
		return DataIterator(self,**kw)

 	def onStoreUpdate(self):
 		self.rowcount = None
	
	def __len__(self):
		if self.rowcount is None:
			self.rowcount = self._connection.executeCount(self)
		return self.rowcount
		
	def executeSelect(self,**kw):
		return self._connection.executeSelect(self, **kw )

	
			
## 	def tuples(self,**kw):
		
## 		"""returns an iterator who returns a tuple of column values for
## 		each row """
		
## 		return TuplesIterator(self,**kw)

	
## 	def instances(self,**kw):
## 		"returns an iterator who returns an instance for each row"
		
## 		return InstanceIterator(self,**kw)





	
	

## 	def atoms2values(self,atomicRow):
## ##  		return [col.atoms2value(atomicRow,self.area)
## ##  				  for col in self.visibleColumns]
## 		return self._query.atoms2values(atomicRow,self._area)
	
	

## 	def __getslice__(self,a,b):
## 		csr = self.executeSelect( offset=a, limit=b-a)
## 		return csr.fetchall()





## 	def setCellValue(self,rowIndex,colIndex,value):
## 		return self._query.setCellValue(self._area,
## 												 rowIndex,colIndex,
## 												 value)

	
		
		
## 	def getRowLabel(self):
## 		return self._area._table.getRowLabel(self._currentRow)
	
	
## 	def getQueryColumns(self):
## 		return self.query.getColumns()

class DataIterator:

	def __init__(self,ds,**kw):
		self.ds = ds
		self.csr = ds.executeSelect(**kw)
		self.recno = 0
		

		
	def __iter__(self):
		return self
	
	def next(self):
		atomicRow = self.csr.fetchone()
		if atomicRow == None:
			raise StopIteration
		self.recno += 1
		#d = self.ds._clist.at2d(atomicRow)
		#return self.ds._table.Row(self.ds,d,False)
		return self.ds.atoms2row(atomicRow,new=False)


class DataRow:
	def __init__(self,fc,clist,values,dirty=False):
		assert isinstance(fc,FieldContainer)
		assert isinstance(clist,BaseColumnList)
		assert type(values) == types.DictType
		self.__dict__["_values"] = values 
		self.__dict__["_fc"] = fc
		self.__dict__["_clist"] = clist
		self.__dict__["_dirty"] = dirty
		
	def __getattr__(self,name):
		assert self.__dict__.has_key("_fc")
		#print repr(self._fc)
		rowattr = self._fc.getRowAttr(name)
		return rowattr.getCellValue(self)
	
	def __setattr__(self,name,value):
      #def setAtomicValue(self,name,value)
		#assert self._locked
		rowattr = self._fc.getRowAttr(name)
		rowattr.setCellValue(self,value)		
		#self._values[name] = value
		rowattr.afterSetAttr(self)
		self.__dict__['_dirty'] = True

	def getFieldValue(self,name):
		try:
			return self._values[name]
		except KeyError:
			raise NoSuchField,name


	def makeDataCell(self,colIndex,col):
		return self.getSession()._dataCellFactory(self,colIndex,col)


	def setDirty(self):
		self.__dict__["_dirty"] = True

	def __getitem__(self,i):
		col = self._clist.visibleColumns[i]
		return col.getCellValue(self)
		
	def __setitem__(self,i,value):
		col = self._clist.visibleColumns[i]
		assert self._pseudo or self._locked
		col.rowAttr.setCellValue(self,value)
		self.__dict__["_dirty"] = True
		
	def __iter__(self):
		return RowIterator(self,self._clist.visibleColumns)
	
	def __len__(self):
		return len(self._clist.visibleColumns)
	
	def getCells(self,columnNames=None):
		return RowIterator(self,self._clist.getColumns(columnNames))
		
	def update(self,**kw):
		self.lock()
		for (k,v) in kw.items():
			setattr(self,k,v)
		self.validate()
		self.unlock()


	def validate(self):
		pass

	def lock(self):
		pass
	
	def unlock(self):
		pass
	
	
	def isDirty(self):
		return self.__dict__['_dirty']

	def makeComplete(self):
		pass


class StoredDataRow(DataRow):
	# base class for Table.Row
	
	def __init__(self,ds,values,new,pseudo=False):
		"""
		"""
		assert type(new) == types.BooleanType
		DataRow.__init__(self,ds._table,ds._clist,values,dirty=new)
		#self.__dict__["_rowId"] = rowId
		self.__dict__["_ds"] = ds
		self.__dict__["_new"] = new
		self.__dict__["_pseudo"] = pseudo
		self.__dict__["_complete"] = False #ds.isComplete()
		self.__dict__["_locked"] = False
		self.__dict__["_isCompleting"] = False

	def __eq__(self, other):
		if other is None:
			return False
		return self.getRowId() == other.getRowId()
		#return tuple(self.getRowId()) == tuple(other.getRowId())
		
	def __ne__(self, other):
		if other is None:
			return True
		return self.getRowId() != other.getRowId()
		#return tuple(self.getRowId()) == tuple(other.getRowId())
		
	def getRenderer(self,rsc,req,writer=None):
		return self._ds._table._rowRenderer(rsc,req,self,writer)

## 	def writeParagraph(self,parentResponder):
## 		rsp = self.getRenderer(parentResponder.resource,
## 									  parentResponder.request,
## 									  parentResponder._writer)
## 		#assert rsp.request is self.request
## 		rsp.writeParagraph()
	
	def getContext(self):
		return self._ds.getContext()
	
	def getSession(self):
		return self._ds._session
	

	
	def isComplete(self):
		return self._complete
	
	def isNew(self):
		return self._new
	
	def getRowId(self):
		id = [None] * len(self._clist.leadTable.getPrimaryAtoms())
		for col in self._clist._pkColumns:
			col.row2atoms(self,id)
## 		if self._ds._table.getTableName() == "CITIES":
## 			print [(col.name,col.rowAttr) for col in self._ds._clist._pkColumns]
## 			print [atom.name for atom in self._ds._clist._atoms]
## 			print id
		return id
		#return self._ds.getRowId(self._values)
		
	def getLabel(self):
		return str(tuple(self.getRowId()))
		#return self._ds._table.getRowLabel(self)
		
	def getFieldValue(self,name):
		try:
			return self._values[name]
		except KeyError:
			if self._isCompleting:
				return None
			self.makeComplete()
			try:
				return self._values[name]
			except KeyError:
				raise NoSuchField,name


	def _readFromStore(self):
		"""
		make this row complete using a single database lookup
		"""
		assert not self._pseudo,\
				 "%s : readFromStore() called for a pseudo row" % repr(self)
		assert not self._complete,\
				 "%s : readFromStore() called a second time" % repr(self)
		assert not self._isCompleting
		
		# but what if atoms2row() causes __getattr__ to be called
		# again? maybe a switch _isCompleting to check this.
		self.__dict__["_isCompleting"] = True
		
		# print "makeComplete() : %s" % repr(self)
		id = self.getRowId()
		#leadRow = self._ds._store._peekQuery.peek(id)
		#d = self._values
		atomicRow = self._ds._connection.executePeek(
			self._ds._store._peekQuery,id)
		if self._new:
			if atomicRow is not None:
				raise DataVeto("Cannot create another %s row %s" \
									% (self.__class__.__name__, id))
			#for a in self._ds._store._peekQuery.getAtoms():
			for attrname in self._ds._table.getAttrList():
				self._values.setdefault(attrname,None)
		else:
			if atomicRow is None:
				#self.__dict__['_new'] = True
				raise DataVeto("Cannot find %s row %s" \
									% (self._ds._table.getTableName(), id))
			self._ds._store._peekQuery.atoms2row(atomicRow,self)
			#for a in self._ds._store._peekQuery.getAtoms():
			#	self._values.setdefault(a.name,atomicRow[a.index])
			#if self._dirty:
			#	raise "cannot yet call readFromStore() for a dirty row"
				
		#self.__dict__['_values'] = atomicRow
		
		"""maybe a third argument `fillMode` to atoms2dict() which
		indicates whether existing (known) values should be
		overwritten, checked for equality or ignored...	 """

		self.__dict__['_complete'] = True
		self.__dict__["_isCompleting"] = False

	def checkIntegrity(self):
		#if not self._complete:
		self.makeComplete()
		for name,attr in self._ds._table._rowAttrs.items():
			msg = attr.checkIntegrity(self)
			if msg is not None:
				return msg
		
## 	def getAtomicValue(self,i):
## 		return self._values[i]

## 	def atomicValues(self):
## 		return self._values
		

	def getAttrValues(self,columnNames=None):
		l = []
		if columnNames is None:
			q = self._area._query()
			for col in q.getColumns():
				attr = col.rowAttr 
				l.append( (attr,attr.getValueFromRow(self)) )
		else:
			for name in columnNames.split():
				col = q.getColumn(name)
				attr = col.rowAttr
				#attr = self._area._table.__getattr__(name) 
				l.append( (attr,attr.getValueFromRow(self)) )
		return tuple(l)
		
	
	def __repr__(self):
		if self._isCompleting:
			return "Uncomplete " + repr(self._ds) + "Row(" \
					 + str(self._values)+")"
		return self._ds._table.getTableName() + "Row(" + str(self._values)+")"
		#return repr(self._ds) + "Row" + repr(tuple(self.getRowId()))

	def __str__(self):
		return str(self.getLabel())





	def lock(self):
		assert not self._locked
		self.__dict__["_locked"] = True
		self._ds._store.lockRow(self)
			

	def unlock(self):
		assert self._locked, "this row was not locked"
		
		if self._dirty:
			msg = self.validate()
			if msg:
				raise DataVeto(repr(self) + ': ' + msg)
			
		#assert not None in self.getRowId(), "incomplete pk"
		self.__dict__["_locked"] = False
		self._ds._store.unlockRow(self)
		self.writeToStore()
		

	def writeToStore(self):
		#print "commit: ", self
		#assert not self._locked
		#if self._locked:
		#	self.unlock()
		if self._new:
			self._ds._connection.executeInsert(self)
			self.__dict__["_new"] = False
		else:
			if not self._dirty: return
			self._ds._connection.executeUpdate(self)
		self.__dict__["_dirty"] = False
		

			

	def makeComplete(self):
		if self._pseudo or self._complete or self._isCompleting:
			return False
		self._readFromStore()
		return True

	def exists(self):
		if not self._complete:
			self._readFromStore()
		return not self.isNew()

	
	


	def defineMenus(self,win):
		#self.initQuery()
		mb = win.addMenuBar("row","&Row menu")
		mnu = mb.addMenu("&Row")
		mnu.addItem("&Edit",self.mnu_toggleEdit,win)
		# mnu.addItem("&Delete",self.mnu_deleteRow)
		# w.addGrid(self)
		# return mb
		mnu = mb.addMenu("&File")
		mnu.addItem("E&xit",win.close)

	def mnu_toggleEdit(self,win):
		pass

	def vetoDelete(self):
		for name,attr in self._ds._table._rowAttrs.items():
			msg = attr.vetoDeleteIn(self)
			if msg:
				return msg


class RowIterator:

	def __init__(self,row,columns):
		self.row = row
		self.colIndex = 0
		self._columns = columns
		
	def __iter__(self):
		return self
	
	def next(self):
		if self.colIndex == len(self._columns):
			raise StopIteration
		col = self._columns[self.colIndex]
		self.colIndex += 1
		#return DataCell(self.row,col)
		return self.row.makeDataCell(self.colIndex,col) 


class DataCell:
	def __init__(self,row,colIndex,col):
		#self.colIndex = colIndex
		self.row = row
		self.col = col

	def getValue(self):
		return self.col.getCellValue(self.row)
	
	def format(self):
		v = self.col.getCellValue(self.row)
		if v is None:
			return ""
		return self.col.format(v,self.row.getContext())
	
