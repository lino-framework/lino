#----------------------------------------------------------------------
# $Id: area.py,v 1.14 2004/07/31 07:13:46 lsaffre Exp $
# Copyright: (c) 2003-2004 Luc Saffre
# License:	 GPL
#----------------------------------------------------------------------

import types
import warnings

from datatypes import DataVeto, AutoIncType
from query import ColumnList
#from datasource import Datasource
#from row import WritableRow
from report import Report

from lino.misc.descr import Describable

class Store:
	"""
	This is a connected or opened Table.
	One instance per Database and Table.
	Does not cache the rows (see CachedStore)
	Instanciates row proxy objects.
	"""
	def __init__(self,conn,db,table):
		#q = self.defineQuery(None)
		#q = Query(self,None)
		#BaseDatasource.__init__(self,db,table)
		self._db = db
		self._table = table
		self._schema = db.schema # shortcut
		self._connection = conn # shortcut
		#self._cachedRows = {}
		self._lockedRows = []
		#self._dirtyRows = {}
		
		self._datasources = []
		
		if len(self._table.getPrimaryAtoms()) == 1:
			self._lastId = None
		else:
			self._lastId = {}

		#self._queries = {}
		#self._peekQuery = self.defineQuery(None)
		self._peekQuery = ColumnList(self,table.getPeekColumnNames())
		
		self._table.onConnect(self)
		#self._peekQuery = ...
		#self._peekDS = Datasource(self,self._peekQuery)

## 	def defineQuery(self,name,**kw):
## 		assert not self._queries.has_key(name), \
## 				 "%s : duplicate query definition %s" % (str(self), name)
##  		q = ColumnList(self,name,**kw)
##  		self._queries[name] = q
##  		return q
## ## 		try:
## ## 			return self._queries[name]
## ## 		except KeyError,e:
## ## 			q = Query(self,name,**kw)
## ## 			self._queries[name] = q
## ## 			return q
		

##  	def getQuery(self,name=None):
## 		return self._queries[name]
## ## 		q = self._queries[name]
## ## 		if len(kw) == 0:
## ## 			return q
## ## 		return q.child(name,**kw)


## 	def getBabelLangs(self):
## 		return self._db._babelLangs

	def getTable(self):
		return self._table
		#return self.schema.getTable(self._table.getTableId())
	
## 	def query(self,columnNames=None,**kw):
## 		"""creates a temporary query.
## 		columnNames can be specified as argument"""
## 		#q = self._table.query(None,columnNames=columnNames,**kw)
## 		q = self._query.child(None,columnNames=columnNames,**kw)
## 		return Datasource(self,q)
		
	def removeFromCache(self,row):
		pass
	
	def addToCache(self,row):
		pass

 	def beforeCommit(self):
		#assert len(self._lockedRows) == 0
		for row in self._lockedRows:
			row.writeToStore()
		
 	def beforeShutdown(self):
		assert len(self._lockedRows) == 0
## 		for row in self._dirtyRows.values():
## 			row.commit()
## 		self._dirtyRows = {}
	
	def createTable(self):
		# print "CREATE TABLE " + self.getName()
		self._connection.executeCreateTable(self._peekQuery)
		#self._table.populate(self)

		

	def lockRow(self,row):
		# todo: use getLock() / releaseLock()
		self.removeFromCache(row)
		self._lockedRows.append(row)
		
	def unlockRow(self,row):
		self.addToCache(row)
		self._lockedRows.remove(row)
		#row.writeToStore()
		#if row.isDirty():
		#	key = tuple(row.getRowId())
		#	self._dirtyRows[key] = row

	def unlockall(self):
		for row in self._lockedRows:
			row.unlock()
		assert len(self._lockedRows) == 0
	

	def setAutoRowId(self,row):
		"get auto-incremented row id"
		autoIncCol = self._peekQuery._pkColumns[-1]
		#assert isinstance(autoIncCol.rowAttr.type,AutoIncType)
		assert len(autoIncCol._atoms) == 1
		autoIncAtom = autoIncCol._atoms[0]
		
		pka = self._table.getPrimaryAtoms()
		id = row.getRowId()
		#id = atomicRow[:len(pka)]
		#print "area.py:%s" % repr(id)
		front, tail = id[:-1], id[-1]
		if None in front:
			raise DataVeto("Incomplete primary key %s for table %s" %(
				repr(id),self._table.getTableName()))
		#tailAtomicName = pka[-1][0]
		#tailType = pka[-1][1]

		# get or set self._lastId
		if len(front):
			# self._lastId is a dict
			x = self._lastId
			for i in front[:-1]:
				try:
					x = x[i]
				except KeyError:
					x[i] = {}
					x = x[i]
			# x is now the bottom-level dict
			i = front[-1]
			if not x.has_key(i):
				x[i] = self._connection.executeGetLastId(self._table,front)
				if x[i] is None:
					x[i] = 0
			if tail is None:
				x[i] += 1
				id[-1] = x[i]
			elif tail > x[i]:
				x[i] = tail
				
		else:
			if self._lastId is None:
				self._lastId = self._connection.executeGetLastId(
					self._table,front)
				if self._lastId is None:
					self._lastId = 0
			if tail is None:
				if type(self._lastId) == type(''):
					self._lastId = str(int(self._lastId)+1)
				else:
					self._lastId += 1
				id[-1] = self._lastId
			elif tail > self._lastId:
				self._lastId = tail

		if tail is None:
			#row.setAtomicValue(pka[-1][0],id[-1])
			#atomicRow[len(pka)-1] = id[-1]
			autoIncCol.setCellValue(row,id[-1])
		#return tuple(id)

		
## 	def provideRow(self,**knownValues):
		
## 		""" provide the row instance defined by knownValues.  If it did
## 		not exist, create it persistently.  knownValues must contain
## 		enough information to construct the rowId.  (later: Raise
## 		DataVeto if there is an existing row with same rowId but
## 		contradicting other knownValues.)
		
## 		"""
## 		id = self._table.values2id(knownValues)
## 		if None in id:
## 			raise DataVeto("uncomplete primary key given")
## 		id = tuple(id)
## 		return self.provideRowInstance(id,None,knownValues)

## ## 	def appendRow(self,**knownValues):
## ## 		"""create a persistant row in this table."""

## ## 		for k in knownValues.keys():
## ## 			attr = self._table.getRowAttr(k)
## ## 		id = self._table.values2id(knownValues)

## ## 		return self.storeRow(id,knownValues)
		
## 	def storeNewRow(self,atomicRow):
## 		# id must be a list (at least if not complete)
## 		# only last element of id may be None (ie to be automatically filled)
	
## ##  		if len(self._lockedRows):
## ##  			raise Exception("cannot append : %d rows are locked" % \
## ##  								 len(self._lockedRows))

## 		id = self.setAutoRowId(atomicRow)
		
## 		row = self.provideRowInstance(id,True,knownValues)

## 		assert row.isDirty()
## 		assert row.isNew()
## 		assert id == row.getRowId()
## 		row.lock()
## 		self._table.onAppend(row)
## 		row.unlock()
## 		return row

	
## 	def provideRowInstance(self,id,new,knownValues=None):
## 		"""
## 		returns the unique row from this table with primary key [id]
## 		"""
## 		assert type(id) == types.TupleType
## 		try:
## 			row = self._cachedRows[id]
## 		except KeyError:
## 			pass
## ## 			print "id %s not in %s" % (repr(id),
## ## 												repr(self._cachedRows.keys()))
## 		else:
## 			if new is not None:
## 				if new:
## 					raise DataVeto(
## 						"Cannot create %s row with existing id %s"
## 						% (self.getName(),str(id)))
## ## 				assert not new,\
## ## 						 "%s : requested 'new' row did exist" % str(id)
			
## 			# TODO: integrity check whether knownValues agree with
## 			# foundValues
## 			return row
		
## 		if new is None:
## 			atomicRow = self.executePeek(id)
## 			# caller doesn't know whether row exists
## 			complete = True
## 			if atomicRow is None:
## 				new = True
## 			else:
## 				new = False
## 				#q = self._table.provideQuery()
## 				self._peekQuery.atoms2dict(atomicRow, knownValues,self)
## 		else:
## 			assert type(new) == types.BooleanType
## 			complete = False

## 		#assert complete is new
## 		row = WritableDataRow(self,atomicRow,new)

		
## 		assert row.getRowId() == id,\
## 				 "%s : %s != %s" % (self.getName(),
## 										  row.getRowId(),id)

## 		self._cachedRows[id] = row
		
## 		if new and knownValues:
## 			row.lock()
## 			for k in knownValues.keys():
## 				self._table._rowAttrs[k].onSetAttr(row)
## 			row.unlock()
		
## 		# print "Table.peek() cached %s:%s" % (self.getName(),str(id))
## 		return row





## 	def ad2row(self,atomicDict,new):
## 		atomicRow = self._query.ad2t(atomicDict)
## 		return self.atoms2row(atomicRow,new)
	
## 	def atoms2row(self,atomicRow,new):
## 		id = tuple(self._setAutoRowId(atomicRow))
## 		#id = tuple(self.getRowId(atomicRow))
## 		return self._getRowInstance(id,atomicRow,new)

## 	def key2row(self,id,new):
## 		atomicRow = self._query.makeAtomicRow()
## 		atomicRow[0:len(id)] = id
## 		print "%s.key2row(%s)" % (repr(self),repr(atomicRow))
## 		return self._getRowInstance(id,atomicRow,new)
	
##   	def datasource(self,**kw):
## 		# a detail field of a row returns this function
##   		query = self._table.provideQuery()
##   		return Datasource(self,query,**kw)
	
	#def report(self,**kw):
	#	return Report(area=self,**kw)
	





	



## class DataRow:

## 	def __init__(self,ds,storedRow):
## 		self._ds = ds
## 		self._storedRow = storedRow
