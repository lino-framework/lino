#----------------------------------------------------------------------
# $Id: database.py $
# Copyright: (c) 2003-2004 Luc Saffre
# License:	 GPL
#----------------------------------------------------------------------

from lino.adamo import DataVeto
#from datasource import Datasource
from query import DataColumnList

class Store:
	"""
	(aka ConnectedTable, Store, Area,...)
	One instance per Database and Table.
	Distributes auto-incrementing keys for new rows.
	"""
	def __init__(self,conn,db,table):
		self._db = db
		self._table = table
		self._schema = db.schema # shortcut
		self._connection = conn # shortcut
		self._lockedRows = []
		
		self._datasources = []
		
		if len(self._table.getPrimaryAtoms()) == 1:
			self._lastId = None
		else:
			self._lastId = {}

		#self._queries = {}
		#self._peekQuery = self.defineQuery(None)
		self._peekQuery = DataColumnList(self,db)
		
		self._table.onConnect(self)
		#self._peekQuery = ...
		#self._peekDS = Datasource(self,self._peekQuery)


	def getTable(self):
		return self._table
		#return self.schema.getTable(self._table.getTableId())
	

	def registerDatasource(self,ds):
		self._datasources.append(ds)

	def fireUpdate(self):
		for ds in self._datasources:
			ds.onStoreUpdate()

		
		
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





