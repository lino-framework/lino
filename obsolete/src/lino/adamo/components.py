#----------------------------------------------------------------------
# ID:        $Id: widgets.py,v 1.5 2004/07/31 07:13:46 lsaffre Exp $
# Copyright: (c) 2003-2004 Luc Saffre
# License:	 GPL
#----------------------------------------------------------------------

raise "no longer used"

from lino.misc.descr import Describable

class OwnedThing(Describable):
	def __init__(self,label=None,doc=None):
		Describable.__init__(self,None,label,doc)
		self._owner = None

	def setOwner(self,owner,name):
		assert self._owner is None
		self._owner = owner
		#self._name = name
		self.setName(name)
		
	def onOwnerInit1(self,owner,name):
		pass

