#----------------------------------------------------------------------
# $Id: center.py$
# Copyright: (c) 2003-2004 Luc Saffre
# License:	 GPL
#----------------------------------------------------------------------

from cStringIO import StringIO

from lino.misc.console import Console, getSystemConsole
from session import ConsoleSession

_center = None # User code should call getCenter() to get this instance.

class Center:
	"""
	The Center is the global singleton object used by adamo.
	It holds a list of sessions and a list of databases. 
	Each session can have its own console
	"""

	def __init__(self,**kw):
		self._databases = []
		self._sessions = []
		#self._systemConsole = con
		self._sessionFactory = ConsoleSession

	def setSessionFactory(self,sf):
		self._sessionFactory = sf
		
	def createSession(self,**kw):
		sess = self._sessionFactory(**kw)
		self._sessions.append(sess)
		return sess

	def removeSession(self,session):
		self._sessions.remove(session)

##  	def addSession(self,session):
##  		self._sessions.append(session)
	
	def addDatabase(self,db):
		#assert db is not None
		#assert not self._databases.has_key(db.getName())
		#self._databases[db.getName()] = db
		assert not db in self._databases
		self._databases.append(db)
		
## 	def getDatabase(self,name):
##  		return self._databases[name]
	
	def removeDatabase(self,db):
		self._databases.remove(db)
		#del self._databases[db.getName()]
		
	
 	def shutdown(self):
 		#for name,db in self._databases.items():
 		for db in self._databases:
 			db.shutdown()

##    use createSession().use() instead!
## 	def use(self,db=None,**kw):
## 		self.addDatabase(db)
## 		sess = self.createSession()
## 		sess.use(db=db,**kw)
## 		return sess

			

			



def start(**kw):
	
	"""This can be invoked once to specify explicit options for the Center singleton.  
	It is not allowed to call it when the Center is already instanciated.
	"""
	global _center
	assert _center is None
	_center = Center(**kw)
	return _center

def getCenter():

	""" Returns the global Center singleton.  Instanciates it if this
	is the first call.  """
	
	global _center
	if _center is None:
		start()
	return _center

#~ def getSystemConsole():
	#~ return getCenter()._systemConsole

def createSession(**kw):
	return getCenter().createSession(**kw)
	