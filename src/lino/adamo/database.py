from area import Store
#from widgets import Window
from lino.misc.descr import Describable

from datasource import Datasource
from tim2lino import TimMemoParser
#from widgets import Widget

from ui import UI
from dbds.sqlite_dbd import Connection


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
		#if label is None:
		#	label = "Unnamed Lino Database"
		
		self._babelLangs = []
		if langs is None:
			langs = 'en'
		for lang_id in langs.split():
			self._babelLangs.append( BabelLang(len(self._babelLangs),
														  lang_id) )

		
		Describable.__init__(self,name,label,doc)

		self.ui = ui
		assert hasattr(ui,'progress')
		#self.name = name
		#self.conn = conn
		self.schema = schema
		self._contexts = []
		self._stores = {}
		#self.startup()

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
			#l.append(Store(conn,self,table))
 			self._stores[table.getTableName()] = Store(conn,self,table)
## 			#print "%s.setupConnection()" % table.getName()
						
		#self._stores = tuple(l)

## 	def __str__(self):
## 		if self.name is not None:
## 			return self.name
## 		return str(self.__class__)
	

		
## 		schema.defineMenus(self)

		#self._defaultLanguage = lang_id

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
		

	def installto(self,d):
		#assert not d.has_key('__context__')
		ctx = self.beginContext()
		d['__context__'] = ctx
		d['setBabelLangs'] = ctx.setBabelLangs
		#d['commit'] = ctx.commit
		d.update(ctx._datasources)

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
		
		


class Context:
	
	def __init__(self,db,langs=None):
		self._db = db
		self._datasources = {}

		if langs is None:
			langs = db.getDefaultLanguage()
		self.setBabelLangs(langs)

		for name,store in db._stores.items():
			ds = Datasource(self,store)
			self._datasources[name] = ds

		self._memoParser = TimMemoParser(self)

	def getLabel(self):
		return self._db.getLabel()

	def memo2html(self,renderer,txt):
		if txt is None:
			return ''
		txt = txt.strip()
		self._memoParser.parse(renderer,txt)
		#return self.memoParser.html


	def getAreaDict(self):
		return self._datasources

	def getDatasources(self):
		return self._datasources.values()

	def getBabelLangs(self):
		return self._babelLangs

	def setBabelLangs(self,langs):
		"string containing a space-separated list of babel language codes"
		self.commit()
		self._babelLangs = []
		for lang_id in langs.split():
			self._babelLangs.append(self._db.findBabelLang(lang_id))
		if self._babelLangs[0].index == -1:
			raise "First item of %s must be one of %s" % (
				repr(langs), repr(self._db.getBabelLangs()))


	def commit(self):
		self._db.commit()

		
	def checkIntegrity(self):
		msgs = []
		for q in self._datasources.values():
			print "%s : %d rows" % (q._table.getTableName(), len(q))
			l = len(q)
			for row in q:
				#row = q.atoms2instance(atomicRow)
				msg = row.checkIntegrity()
				if msg is not None:
					msgs.append("%s[%s] : %s" % (
						q._table.getTableName(),
						str(row.getRowId()),
						msg))
			#store.flush()
		return msgs
		



	def __getattr__(self,name):
  		try:
  			return self._datasources[name]
  		except KeyError,e:
			print self._datasources
  			raise AttributeError, \
					"%s instance has no attribute %s" % (
				self.__class__.__name__,str(e))

