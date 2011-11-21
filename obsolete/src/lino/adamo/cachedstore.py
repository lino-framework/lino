#----------------------------------------------------------------------
# $Id: cachedstore.py,v 1.1 2004/06/12 03:13:27 lsaffre Exp $
# Copyright: (c) 2003-2004 Luc Saffre
# License:	 GPL
#----------------------------------------------------------------------

from area import Store, WritableDataRow

class CachedStore(Store):
	
	def __init__(self,db,table):
		Store.__init__(self,db,table)
		self._cachedRows = {}
		
	def _getRowInstance(self,id,atomicRow,new):
		try:
			row = self._cachedRows[id]
		except KeyError:
			row = WritableDataRow(self,atomicRow,new)
			assert self.getRowId(row._values) == id,\
					 "%s != %s" % (repr(self.getRowId(row._values)),repr(id))
			self._cachedRows[id] = row
			return row
		else:
			if new:
				raise DataVeto(
					"Cannot create %s row with existing id %s"
					% (self.getName(),str(id)))
			# TODO: integrity check whether knownValues agree with
			# foundValues
			return row


	def removeFromCache(self,row):
		assert row._area == self
		id = self.getRowId(row._values)
		try:
			del self._cachedRows[id]
		except KeyError:
			raise
			#pass # so it was a newly created row

	def addToCache(self,row):
		assert row._area == self
		id = self.getRowId(row._values)
		if None in id:
			raise Exception(\
					"%s : primary key may not contain None in table %s" \
					% (repr(id),str(self._table)))
		self._cachedRows[id] = row
		
	def commit(self):
		# self.unlockall()
		# print "%s.commit()" % self.getName()
		if len(self._lockedRows):
			warnings.warn("commit: ignored %d locked row(s)" % \
							  len(self._lockedRows))
		for row in self._cachedRows.values():
			# print row
			row.commit()

## 	def freeze(self):
## 		self._frozen = True
		
	def flush(self):
		self.unlockall()
		self.commit()
		self._cachedRows = {}

	def clearCache(self):
		self._cachedRows = {}

	def getCachedRows(self):
		return self._cachedRows


	



