#----------------------------------------------------------------------
# $Id: database.py $
# Copyright: (c) 2003-2004 Luc Saffre
# License:	 GPL
#----------------------------------------------------------------------

from lino.misc.descr import Describable

from ui import UI
from dbds.sqlite_dbd import Connection

from context import Context

from query import ColumnList

class ConnectedTable:
	"""
	(previously called "Store", "Area",...)
	One instance per Database and Table.
	Instanciates row proxy objects.
	"""
	def __init__(self,conn,db,table):
		#q = self.defineQuery(None)
		#q = Query(self,None)
		#BaseDatasource.__init__(self,db,table)
		self._db = db
		#from database import Context
		#assert isinstance(db,Context)
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
		self._peekQuery = ColumnList(self) #,table.getPeekColumnNames())
		
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





class BabelLang:
	def __init__(self,index,id):
		self.index = index
		self.id = id

	def __repr__(self):
		return "<BabelLang %s(%d)>" % (self.id,self.index)



			
class Database(Describable):
	
	def __init__(self,ui,schema,
					 name=None,
					 langs=None,
					 label=None,
					 doc=None):
		
		self._babelLangs = []
		if langs is None:
			langs = 'en'
		for lang_id in langs.split():
			self._babelLangs.append( BabelLang(len(self._babelLangs),
														  lang_id) )

		
		Describable.__init__(self,name,label,doc)

		self.ui = ui
		assert hasattr(ui,'progress')
		self.schema = schema
		self._contexts = []
		self._stores = {}

	def getStoresById(self):
		l = []
 		for table in self.schema.getTableList():
			try:
				l.append(self._stores[table.getTableName()])
			except KeyError:
				pass
		return l

	def startup(self,conn,flt=None):

		l = []
 		for table in self.schema.getTableList(flt):
 			self._stores[table.getTableName()] = ConnectedTable(conn,
																				 self,
																				 table)
	


	def update(self,otherdb):
		self._stores.update(otherdb._stores)
## 		l = list(self._stores)
## 		for store in otherdb._stores:
## 			if l.
## 		self._stores = tuple(l)

	def getDefaultLanguage(self):
		return self._babelLangs[0].id
		#return self.LANG[self._defaultLanguage]
		#return self._defaultLanguage

## 	def setDefaultLanguage(self,id):
## 		self._defaultLanguage = self.LANG[id]

	def getBabelLangs(self):
		return self._babelLangs
	
	def findBabelLang(self,lang_id):
		for lang in self._babelLangs:
			if lang.id == lang_id:
				return lang
		"""
		index -1 means that values in this language should be ignored
		"""
		return BabelLang(-1,lang_id)
		#raise "%s : no such language code in %s" % (lang_id, repr(self))
		
	
	def beginContext(self,langs=None):
		ctx = Context(self,langs)
		self._contexts.append(ctx)
		return ctx

	def endContext(self,ctx):
		assert self._contexts[-1] is ctx
		self._contexts.pop()
		#ctx.commit()

## 	def beginSession(self,context=None):
## 		sess = Session()
## 		if context is None:
## 			context = self.beginContext()
## 		session.setContext(context)
## 		return session		

	def createTables(self):
 		for store in self.getStoresById():
			store.createTable()
 		#for store in self._stores:
		#	store._table.populate(store)
			#store.flush()

##		def connect(self,conn):
##			self.__dict__['conn'] = conn

	def commit(self):	
		#self.schema.commit(self)
		#assert conn is not None
		for store in self.getStoresById():
			#if store._table.getTableName() == "NATIONS":
			#	print "commit"+str(store._table.getTableName())
			store.beforeCommit()
		
	#def flush(self):
	#	for store in self._stores:
	#		store.flush()
		#self.conn.commit()

	#def disconnect(self):

 	def shutdown(self):
		self.ui.progress("shutdown "+ str(self))
 		#self.commit()
		for store in self.getStoresById():
			store.beforeShutdown()
	
	def restart(self):
		self.shutdown()
		self.startup()

			
	def checkIntegrity(self):
		ctx = self.beginContext()
		retval = ctx.checkIntegrity()
		self.endContext(ctx)
		return retval
		

## 	def beginSession(self,d=None):
## 		#assert not d.has_key('__context__')
## 		ctx = self.beginContext()
## 		return ctx.beginSession(d)
		
## 	def getAreaDict(self):
## 		return self._areas

## 	def __str__(self):
## 		return "%s database connected to %s" % (str(self.schema),
## 															 str(self.conn))

## 	def datasource(self,query,**kw):
## 		area = self._areas[query.leadTable.name]
## 		if len(kw) > 0:
## 			query = query.child(**kw)
## 		return Datasource(area,query,**kw)



class QuickDatabase(Database):
	"Database instance with only one connection"
	def __init__(self,schema, verbose=False,
					 langs=None,
					 label=None,
					 filename="tmp.db",
					 isTemporary=True):
	
		ui = UI(verbose=verbose)

		schema.startup(ui)

		self._connection = Connection(filename="tmp.db",
												schema=schema,
												isTemporary=isTemporary)

		Database.__init__(self,
								ui,
								schema,
								langs=langs,
								label=label)

		ui.addDatabase(self) #'tmp', conn,schema, label=label)
		self.startup(self._connection)

	def shutdown(self):
		Database.shutdown(self)
		self._connection.close()
		self._connection = None

	def commit(self):	
		Database.commit(self)
		self._connection.commit()
		
		


