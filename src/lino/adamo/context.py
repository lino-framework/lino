#----------------------------------------------------------------------
# $Id: area.py,v 1.14 2004/07/31 07:13:46 lsaffre Exp $
# Copyright: (c) 2003-2004 Luc Saffre
# License:	 GPL
#----------------------------------------------------------------------

from datasource import Datasource
from tim2lino import TimMemoParser
from forms import ContextForm
from lino.misc.attrdict import AttrDict
from lino.adamo import InvalidRequestError

class Context:
	"""
	A Context is a Session of a user in a database.
	user can be anonymous.
	database can be None if no database is selected.
	"""
	
	def __init__(self,db,langs=None):
		self._db = db
		self.forms = AttrDict()
		
		self._memoParser = TimMemoParser(self)

		if langs is None:
			langs = db.getDefaultLanguage()
		self.setBabelLangs(langs)

		#self._datasources = {}
		self.tables = AttrDict()
		for name,store in db._stores.items():
			ds = Datasource(self,store)
			self.tables.define(name,ds)
			#self._datasources[name] = ds

		self.forms = AttrDict()
		for name,frm in db.schema.forms.items():
			self.forms.define(name,ContextForm(frm,self))


## 	def beginSession(self,d=None):
## 		sess = Session()
## 		sess.beginContext(self)
## 		if d is not None:
## 			sess.installto(d)
## 		return sess

	def getLabel(self):
		return self._db.getLabel()

	def getDatasource(self,name):
		try:
			return getattr(self.tables,name)
		except AttributeError,e:
			raise InvalidRequestError("no such table: "+name)

## 	def openForm(self,name):
## 		form = getattr(self._db.schema.forms,name)
## 		formRow = form.open(self)
## 		return formRow

	def getContentRoot(self):
		return self._db.schema.getContentRoot(self)

	def getRenderer(self,rsc,req,writer=None):
		return self._db.schema._contextRenderer(rsc,req,self,writer)
	
	def getContext(self):
		return self
	
	def memo2html(self,renderer,txt):
		if txt is None:
			return ''
		txt = txt.strip()
		self._memoParser.parse(renderer,txt)
		#return self.memoParser.html


## 	def getAreaDict(self):
## 		return self._datasources

## 	def getDatasources(self):
## 		return self._datasources.values()

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

	def shutdown(self):
		self._db.shutdown()

		
	def checkIntegrity(self):
		msgs = []
		for q in self.tables:
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
		



## 	def __getattr__(self,name):
##   		try:
##   			return self._datasources[name]
##   		except KeyError,e:
## 			#print self._datasources
##   			raise AttributeError, \
## 					"%s instance has no attribute %s" % (
## 				self.__class__.__name__,name)


class AbstractSession:
	def __init__(self,db=None):
		self.context = None
		self.schema = None
		self.tables = None
		self.db = None
		self.forms = AttrDict()
		#self._formStack = []
		
		self._user = None

		if db is not None:
			self.use(db)
		#self._userId = None
		#self._pwd = None
		#self.notifyMessage("Lino Session started")
		#print "Lino Session started"

	def progress(self,msg):
		raise NotImplementedError
		
	def errorMessage(self,msg):
		raise NotImplementedError

	def notifyMessage(self,msg):
		raise NotImplementedError

	def use(self,db):
		self.setContext(db.beginContext())

	def installto(self,d):
		d['__session__'] = self
		d['setBabelLangs'] = self.context.setBabelLangs
		self.context.tables.installto(d)
		
	def setContext(self,context):
		if self.context is context:
			return
		if self.context is not None:
			self.endContext()
		self.beginContext(context)
			
	def beginContext(self,context):
		#assert len(self._formStack) == 0
		assert self.context is None
		self.context = context
		self.schema = context._db.schema # shortcut
		self.db = context._db # shortcut
		self.tables = context.tables # shortcut
		self.forms = AttrDict()
		#self.connection = context._db._connection

		for name in ('commit', 'shutdown', 'setBabelLangs'):
			setattr(self,name,getattr(context,name))
			
		#for name in ('startDump', 'stopDump'):
		#	setattr(self,name,getattr(context._db._connection,name))
		# only QuickDatabase knows her connection! 
		
		#self._formStack = []
		#self.openForm('login')
		self.schema.onStartSession(self)
		#self.notifyMessage("beginContext()")
		
	def endContext(self):
		if self._user is not None:
			self.logout()
		self.context = None
		#self._formStack = []
	
	def openForm(self,formName):
		#print "openForm()" + formName
		tpl = getattr(self.context.forms,formName)
		frm = tpl.open(self)
		self.forms.define(formName,frm)
		#self._formStack.append(frm)
		return frm

	def closeForm(self,formName):
		del self.forms._values[formName]
	
## 	def getCurrentForm(self):
## 		if len(self._formStack) > 0:
## 			return self._formStack[-1]

	def getUser(self):
		return self._user

	def login(self,user):
		if self._user is not None:
			self.logout()
		self._user = user
		

	def logout(self):
 		assert self._user is not None
 		self._user = None

## 	def startSession(self):
## 		if self.context is not None:
## 			self.context.schema.onStartSession(self)
		
		
class ConsoleSession(AbstractSession):
	def __init__(self,**kw):
		AbstractSession.__init__(self,**kw)

	def errorMessage(self,msg):
		print msg

	def notifyMessage(self,msg):
		print msg
		
	def progress(self,msg):
		print msg

class WebSession(AbstractSession):
	
	def __init__(self,**kw):
		AbstractSession.__init__(self,**kw)
		self._messages = []

	def errorMessage(self,msg):
		self._messages.append(msg)

	def notifyMessage(self,msg):
		self._messages.append(msg)

	def popMessages(self):
		l = self._messages
		self._messages = []
		return l

		
		
		
