#----------------------------------------------------------------------
# $Id: session.py,v 1.14 2004/07/31 07:13:46 lsaffre Exp $
# Copyright: (c) 2003-2004 Luc Saffre
# License:	 GPL
#----------------------------------------------------------------------

from datasource import Datasource, DataCell
#from forms import ContextForm
from lino.misc.attrdict import AttrDict
from lino.adamo import InvalidRequestError
from lino.misc.console import Console


class BabelLang:
	def __init__(self,index,id):
		self.index = index
		self.id = id

	def __repr__(self):
		return "<BabelLang %s(%d)>" % (self.id,self.index)


class Context:
	
	def getBabelLangs(self):
		raise NotImplementedError
	
			
class Application:

	def __init__(self,**kw):
		self._databases = {}
		self.console = Console(**kw)
		
	def addDatabase(self,db):
		#assert db is not None
 		assert not self._databases.has_key(db.getName())
 		self._databases[db.getName()] = db
		
	def getDatabase(self,name):
 		return self._databases[name]
	
	def removeDatabase(self,db):
		del self._databases[db.getName()]
		
	
 	def shutdown(self):
 		for name,db in self._databases.items():
 			db.shutdown()

	def use(self,db=None,**kw):
		self.addDatabase(db)
		sess = ConsoleSession(self.console)
		sess.use(db=db,**kw)
		return sess

class AdamoSession(Context):
	
	def __init__(self,**kw):
		self._dataCellFactory = DataCell
		self._windowFactory = lambda x: x
		self._user = None
		self.db = None
		self.schema = None
		self.tables = None
		self.use(**kw)
			
		
	def use(self,db=None,langs=None):
		# if necessary, stop using current db
		if db != self.db and self.db is not None:
			self.db.removeSession(self)
			if self._user is not None:
				self.logout()
		if db is None:
			self.schema = None
			self.tables = None
			self.db = None
		else:
			# start using new db
			self.schema = db.schema # shortcut
			self.db = db
			self.tables = AttrDict(factory=self.openTable)
			if langs is None:
				langs = db.getDefaultLanguage()
			self.db.addSession(self)
				
		if langs is not None:
			self.setBabelLangs(langs)
		
		self._formStack = []

	def commit(self):
		return self.db.commit()

	def shutdown(self):
		return self.db.shutdown()

	def setBabelLangs(self,langs):
		
		"""langs is a string containing a space-separated list of babel
		language codes"""
		
		self.db.commit()
		self._babelLangs = []
		for lang_id in langs.split():
			self._babelLangs.append(self.db.findBabelLang(lang_id))
		if self._babelLangs[0].index == -1:
			raise "First item of %s must be one of %s" % (
				repr(langs), repr(self.db.getBabelLangs()))

	def getBabelLangs(self):
		return self._babelLangs
	
	def openTable(self,name):
		try:
			store = self.db._stores[name]
		except KeyError,e:
			#except AttributeError,e:
			raise InvalidRequestError("no such table: "+name)
		return Datasource(self,store)
	
	def getDatasource(self,name):
		return getattr(self.tables,name)

	def progress(self,msg):
		raise NotImplementedError
		
	def errorMessage(self,msg):
		raise NotImplementedError

	def notifyMessage(self,msg):
		raise NotImplementedError

	def installto(self,d):
		"""
		deprecated.
		note that installto() will open all tables.
		"""
		d['__session__'] = self
		d['setBabelLangs'] = self.setBabelLangs
		#self.context.tables.installto(d)
		#d.update(
 		for name in self.db._stores.keys():
			d[name] = getattr(self.tables,name)
 		#for name,store in self.db._stores.items():
		#   ds = Datasource(self,store)
		#   self.tables.define(name,ds)
		
## 	def setContext(self,context):
## 		if self.context is context:
## 			return
## 		if self.context is not None:
## 			self.endContext()
## 		self.beginContext(context)
			
## 	def beginContext(self,context):
## 		#assert len(self._formStack) == 0
## 		assert self.context is None
## 		self.context = context
## 		self.schema = context._db.schema # shortcut
## 		self.db = context._db # shortcut
## 		#self.tables = context.tables # shortcut
## 		self.tables = AttrDict(factory=self.openTable)
## 		#self.forms = AttrDict()
## 		#self.connection = context._db._connection

## 		for name in ('commit', 'shutdown', 'setBabelLangs'):
## 			setattr(self,name,getattr(context,name))
			
## 		#for name in ('startDump', 'stopDump'):
## 		#	setattr(self,name,getattr(context._db._connection,name))
## 		# only QuickDatabase knows her connection! 
		
## 		self._formStack = []
## 		#self.openForm('login')
## 		#self.notifyMessage("beginContext()")
		
## 	def getContext(self):
## 		return self.context
	
	def onStartUI(self):
		self.schema.onStartUI(self)
		
	
## 	def endContext(self):
## 		if self._user is not None:
## 			self.logout()
## 		self.context = None
## 		self.tables = None
## 		self.schema = None
## 		self.db = None
## 		self._formStack = []
	
	def openForm(self,formName,**values):
		#print "openForm()" + formName
		tpl = getattr(self.schema.forms,formName)
		frm = tpl.open(self,**values)
		win = self._windowFactory(frm)
		#self.forms.define(formName,frm)
		self._formStack.append(win)
		return win

	def closeForm(self,formName):
		raise NotImplementedError
		#del self.forms._values[formName]
	
	def getCurrentForm(self):
		if len(self._formStack) > 0:
			return self._formStack[-1]

	def getUser(self):
		return self._user

	def login(self,user):
		if self._user is not None:
			self.logout()
		self._user = user
		
	def logout(self):
 		assert self._user is not None
 		self._user = None

	def checkIntegrity(self):
		msgs = []
		#for q in self.tables:
 		for name in self.db._stores.keys():
			q = getattr(self.tables,name)
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
		


## 	def startSession(self):
## 		if self.context is not None:
## 			self.context.schema.onStartSession(self)
		
		
class ConsoleSession(AdamoSession):
	def __init__(self,console,**kw):
		AdamoSession.__init__(self,**kw)
		self.console = console

	def errorMessage(self,msg):
		return self.console.notify(msg)

	def notifyMessage(self,msg):
		return self.console.notify(msg)
		
	def progress(self,msg):
		return self.console.progress(msg)

	def report(self,ds,showTitle=True):
		wr = self.console.out.write
		if showTitle:
			wr(ds.getLabel()+"\n")
			wr("="*len(ds.getLabel())+"\n")
		columns = ds.getVisibleColumns()
		wr(" ".join(
			[col.getLabel().ljust(col.getPreferredWidth()) \
			 for col in columns]).rstrip())
		wr("\n")
		wr(" ".join( ["-" * col.getPreferredWidth() \
							  for col in columns]))
		wr("\n")
		for row in ds: #.iterateAsColumns():
			l = []
			for cell in row:
				col = columns[i]
				l.append(cell.format())
			wr(" ".join(l).rstrip())
			wr("\n")


class WebSession(AdamoSession):
	
	def __init__(self,**kw):
		AdamoSession.__init__(self,**kw)
		self._messages = []

	def errorMessage(self,msg):
		self._messages.append(msg)

	def notifyMessage(self,msg):
		self._messages.append(msg)

	def popMessages(self):
		l = self._messages
		self._messages = []
		return l

		
		
		
