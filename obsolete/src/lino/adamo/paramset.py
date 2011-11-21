#----------------------------------------------------------------------
# ID:        $Id: paramset.py,v 1.3 2004/06/12 03:06:50 lsaffre Exp $
# Copyright: (c) 2003-2004 Luc Saffre
# License:	 GPL
#----------------------------------------------------------------------

class ParamOwner:
	paramNames = {}
	
	def configure(self,**kw):

		#self.params = ParamSet(self.paramNames)
		
		for k in self.paramNames.keys():
			v = kw.pop(k,None)
			setattr(self,k,v)
			
		self.onConfigure(kw)
				
	def child(self,**kw):
		for k in self.paramNames.keys():
			kw.setdefault(k,getattr(self,k))
			
		
	def myParams(self):
		d = {}
		for k in self.paramNames.keys():
			d[k] = getattr(self,k)
		return d
