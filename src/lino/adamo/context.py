#----------------------------------------------------------------------
# $Id: area.py,v 1.14 2004/07/31 07:13:46 lsaffre Exp $
# Copyright: (c) 2003-2004 Luc Saffre
# License:	 GPL
#----------------------------------------------------------------------

raise "no longer used"

## from datasource import Datasource, DataCell
## #from forms import ContextForm
## from lino.misc.attrdict import AttrDict
## from lino.misc import console
## from lino.adamo import InvalidRequestError
## from lino.database import Context

## class Context:
## 	"""
## 	A Context is a Session of a user in a database.
## 	user can be anonymous.
## 	database can be None if no database is selected.
## 	"""
	
## 	def __init__(self,db,langs=None):
## 		self._db = db
## 		#self.forms = AttrDict()
		
## 		#self._datasources = {}
## 			#self._datasources[name] = ds

## ## 		self.forms = AttrDict()
## ## 		for name,frm in db.schema.forms.items():
## ## 			self.forms.define(name,ContextForm(frm,self))


## ## 	def beginSession(self,d=None):
## ## 		sess = Session()
## ## 		sess.beginContext(self)
## ## 		if d is not None:
## ## 			sess.installto(d)
## ## 		return sess

## 	def getLabel(self):
## 		return self._db.getLabel()

## ## 	def openForm(self,name):
## ## 		form = getattr(self._db.schema.forms,name)
## ## 		formRow = form.open(self)
## ## 		return formRow

## 	def getContentRoot(self):
## 		return self._db.schema.getContentRoot(self)

## 	def getRenderer(self,rsc,req,writer=None):
## 		return self._db.schema._contextRenderer(rsc,req,self,writer)
	
## 	def getContext(self):
## 		return self
	


## 	def commit(self):
## 		self._db.commit()

## 	def shutdown(self):
## 		self._db.shutdown()

		


## 	def __getattr__(self,name):
##   		try:
##   			return self._datasources[name]
##   		except KeyError,e:
## 			#print self._datasources
##   			raise AttributeError, \
## 					"%s instance has no attribute %s" % (
## 				self.__class__.__name__,name)


