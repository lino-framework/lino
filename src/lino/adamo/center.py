#----------------------------------------------------------------------
# $Id: center.py$
# Copyright: (c) 2003-2004 Luc Saffre
# License:	 GPL
#----------------------------------------------------------------------

from cStringIO import StringIO

from lino.misc.console import Console
from session import Session


class Center:
	"""
	This is the global singleton object used by adamo.
	User code should call center() to get this instance.
	"""

	def __init__(self,**kw):
		self._databases = []
		self._sessions = []
		self.console = Console(**kw)
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

			

class ConsoleSession(Session):
	def __init__(self,console=None,**kw):
		Session.__init__(self,**kw)
		if console is None:
			console = center().console
		self.console = console
		self._dumping = None
		#for m in console.forwardables:
		#	setattr(self,m,getattr(console,m))

	def info(self,*a):
		return self.console.info(*a)
	def debug(self,*a):
		return self.console.debug(*a)
	def error(self,*a):
		return self.console.error(*a)

	def startDump(self,**kw):
		assert self._dumping is None
		self._dumping = self.console
		self.console = Console(out=StringIO(),**kw)

	def stopDump(self):
		assert self._dumping is not None, "dumping was not started"
		s = self.console.out.getvalue()
		self.console = self._dumping
		self._dumping = None
		return s

	def showForm(self,formName,modal=False,**kw):
		frm = self.openForm(formName,**kw)
		wr = self.console.out.write
		wr(frm.getLabel()+"\n")
		wr("="*len(frm.getLabel())+"\n")
		for cell in frm:
			wr(cell.getLabel() + ":" + cell.format())
			wr("\n")
		
	def showReport(self,ds,showTitle=True,**kw):
		wr = self.console.out.write
		#if len(kw):
		rpt = ds.report(**kw)
		if showTitle:
			wr(rpt.getLabel()+"\n")
			wr("="*len(rpt.getLabel())+"\n")
		columns = rpt.getVisibleColumns()
		wr(" ".join(
			[col.getLabel().ljust(col.getPreferredWidth()) \
			 for col in columns]).rstrip())
		wr("\n")
		wr(" ".join( ["-" * col.getPreferredWidth() \
							  for col in columns]))
		wr("\n")
		for row in rpt:
			l = []
			for cell in row:
				#col = columns[i]
				l.append(cell.format())
			wr(" ".join(l).rstrip())
			wr("\n")

			



_center = None



def start(**kw):
	
	"""This can be invoked once to specify explicit options for the
	Center singleton.  It is not allowed to call it when the Center is
	already instanciated. """
	
	global _center
	assert _center is None
	_center = Center(**kw)

def center():

	""" Returns the global Center singleton.  Instanciates it if this
	is the first call.  """
	
	global _center
	if _center is None:
		start()
	return _center

