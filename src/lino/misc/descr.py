#----------------------------------------------------------------------
# $Id: descr.py,v 1.3 2004/07/31 07:13:47 lsaffre Exp $
# Copyright: (c) 2003-2004 Luc Saffre
# License:	 GPL
#----------------------------------------------------------------------

#from lino.misc.pset import PropertySet

class Describable:

## 	defaults = {
## 		'label' : None,
## 		'description' : None
## 		}
	
	#def __init__(self,label=None,description=None):
 	#def __init__(self,parent=None,label=None,description=None):
 	def __init__(self,name,label,doc):
##  		if parent is not None:
##  			if label is None:
##  				label = parent.getLabel()
## 			if description is None:
##  				description = parent.getDescription()
		#if name is None:
		#	name = self.__class__.__name__
		self._name = name
			
		if label is None:
			label = "Unlabeled %s instance" % self.__class__.__name__
		self._label = label
		
 		if doc is None:
			#	doc = "(No docstring available for " + label+")"
			doc = self.__doc__
		self._doc = doc
			
## 		self._parent = parent
		
	def getLabel(self):
		"""
		override this if you want to inherit label from somebody else
		"""
		return self._label
	
## 	def getParent(self):
## 		return self._parent

	def setLabel(self,label):
		self._label = label

	def getDoc(self):
		return self._doc
	
	def setDoc(self,doc):
		self._doc = doc

	def setName(self,name):
		self._name = name

	def getName(self):
		return self._name 

	def __str__(self):
		if self._name == self.__class__.__name__:
			return self._name
		return self.__class__.__name__ + " " + str(self._name) 

	def __repr__(self):
		return self.__class__.__name__ + " " + str(self._name) 

