#----------------------------------------------------------------------
# $Id: session.py,v 1.14 2004/07/31 07:13:46 lsaffre Exp $
# Copyright: (c) 2003-2004 Luc Saffre
# License:	 GPL
#----------------------------------------------------------------------

from datasource import Datasource, DataCell
#from forms import ContextForm
from lino.misc.attrdict import AttrDict
from lino.adamo import InvalidRequestError
#from center import center
#import center


class BabelLang:
	def __init__(self,index,id):
		self.index = index
		self.id = id

	def __repr__(self):
		return "<BabelLang %s(%d)>" % (self.id,self.index)



	


class Context:
	"interface class"
	def getBabelLangs(self):
		raise NotImplementedError


			
class Session(Context):
	"""
	A Session is if a machine starts Adamo
	"""
	_dataCellFactory = DataCell
	#_windowFactory = lambda x: x
	
	def __init__(self,**kw):
		#self.app = app
		self._user = None
		self.db = None
		self.schema = None
		self.tables = None
		self.forms = None
		#center().addSession(self)
		self.use(**kw)

	def hasAuth(self,*args,**kw):
		return True
			
		
	def use(self,db=None,langs=None):
		# if necessary, stop using current db
		if db != self.db and self.db is not None:
			#self.db.removeSession(self)
			if self._user is not None:
				self.logout()
		if db is None:
			self.schema = None
			self.tables = None
			self.forms = None
			self.db = None
		else:
			# start using new db
			self.schema = db.schema # shortcut
			self.db = db
			self.tables = AttrDict(factory=self.openTable)
			self.forms = AttrDict(factory=self.openForm)
			if langs is None:
				langs = db.getDefaultLanguage()
			#self.db.addSession(self)
				
		if langs is not None:
			self.setBabelLangs(langs)
		
		#self._formStack = []

## 	def spawn(self,**kw):
## 		kw.setdefault('db',self.db)
## 		kw.setdefault('langs',self.getLangs())
## 		return center.center().createSession(**kw)

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

	def getLangs(self):
		return " ".join([lng.id for lng in self._babelLangs])
	
	def openTable(self,name):
		try:
			store = self.db._stores[name]
		except KeyError,e:
			#except AttributeError,e:
			raise InvalidRequestError("no such table: "+name)
		return Datasource(self,store)
	
	def getDatasource(self,name):
		return getattr(self.tables,name)

	def showForm(self,formName,modal=False,**kw):
		raise NotImplementedError

	def showReport(self,ds,showTitle=True,**kw):
		raise NotImplementedError

	def end(self):
		self.use()
		

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
		
	
	def onBeginSession(self):
		self.schema.onBeginSession(self)
		
	
	def openForm(self,formName,*args,**values):
		#print "openForm()" + formName
		cl = getattr(self.schema.forms,formName)
		frm = cl(self,*args,**values)
		#frm.init()
		return frm
	
	def onLogin(self):
		return self.db.schema.onLogin(self)
	
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
			self.info("%s : %d rows" % (q._table.getTableName(), len(q)))
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
		
		


class WebSession(Session):
	
	def __init__(self,**kw):
		Session.__init__(self,**kw)
		self._messages = []

	def errorMessage(self,msg):
		self._messages.append(msg)

	def notifyMessage(self,msg):
		self._messages.append(msg)

	def popMessages(self):
		l = self._messages
		self._messages = []
		return l

		
		
		
