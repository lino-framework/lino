#----------------------------------------------------------------------
# $Id: database.py $
# Copyright: (c) 2003-2004 Luc Saffre
# License:	 GPL
#----------------------------------------------------------------------

from lino.misc.descr import Describable
from lino.adamo import DataVeto

#from ui import UI
from dbds.sqlite_dbd import Connection

from session import Context, BabelLang

#from query import DatasourceColumnList
from tim2lino import TimMemoParser
from store import Store


class Database(Context,Describable):
	
	def __init__(self, app,schema,
					 name=None,
					 langs=None,
					 label=None,
					 doc=None):
		self._supportedLangs = []
		if langs is None:
			langs = 'en'
		for lang_id in langs.split():
			self._supportedLangs.append(
				BabelLang(len(self._supportedLangs), lang_id) )
		Describable.__init__(self,name,label,doc)
		
		self._memoParser = TimMemoParser(self)

		self._app = app
		self._sessions = []
		#assert hasattr(ui,'progress')
		self.schema = schema
		#self._contexts = []
		self._stores = {}

	def getBabelLangs(self):
		return self._supportedLangs

	def removeSession(self,session):
		self._sessions.remove(session)

	def addSession(self,session):
		self._sessions.append(session)
	
	def getDefaultLanguage(self):
		return self._supportedLangs[0].id

	def findBabelLang(self,lang_id):
		for lang in self._supportedLangs:
			if lang.id == lang_id:
				return lang
		"""
		index -1 means that values in this language should be ignored
		"""
		return BabelLang(-1,lang_id)
		#raise "%s : no such language code in %s" % (lang_id, repr(self))
		
	def memo2html(self,renderer,txt):
		if txt is None:
			return ''
		txt = txt.strip()
		self._memoParser.parse(renderer,txt)
		#return self.memoParser.html

		
	def getStoresById(self):
		l = []
 		for table in self.schema.getTableList():
			try:
				l.append(self._stores[table.getTableName()])
			except KeyError:
				pass
		return l

	def startup(self,conn,flt=None):

 		for table in self.schema.getTableList(flt):
 			self._stores[table.getTableName()] = Store(conn, self, table)
	


	def update(self,otherdb):
		self._stores.update(otherdb._stores)
## 		l = list(self._stores)
## 		for store in otherdb._stores:
## 			if l.
## 		self._stores = tuple(l)

	
## 	def beginContext(self,langs=None):
## 		ctx = Context(self,langs)
## 		self._contexts.append(ctx)
## 		return ctx

## 	def endContext(self,ctx):
## 		assert self._contexts[-1] is ctx
## 		self._contexts.pop()
## 		#ctx.commit()

## 	def beginSession(self,context=None):
##  		if context is None:
##  			context = self.beginContext()
## 		sess = ConsoleSession()
## 		sess.setContext(context)
## 		return sess

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
		self._app.console.progress("Application shutdown "+ str(self))
 		#self.commit()
		for sess in self._sessions:
			#sess.beforeShutdown()
			self.removeSession(sess)
		for store in self.getStoresById():
			store.beforeShutdown()
			
		self._app.removeDatabase(self)
	
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
	def __init__(self,
					 sess,
					 schema,
					 verbose=False,
					 langs=None,
					 label=None,
					 filename="tmp.db",
					 isTemporary=True):



		Database.__init__(self,
								sess,
								schema,
								langs=langs,
								label=label)

		
		self._connection = Connection(filename="tmp.db",
												schema=schema,
												isTemporary=isTemporary)

		self.startup(self._connection)

	def shutdown(self):
		Database.shutdown(self)
		self._connection.close()
		self._connection = None

	def commit(self):	
		Database.commit(self)
		self._connection.commit()
		
		


