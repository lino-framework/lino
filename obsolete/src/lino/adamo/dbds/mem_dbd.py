from lino.adamo import connection
from lino.adamo.query import Query

class MemoryConnection(connection.Connection):
	def __init__(self,rawData):
		self._atoms = rawData[0]
		self._rawData = rawData[1:]

	def onTableSetup(self,table):
		"convert rawData to cached rows in Table"
		#for atomName in self._atoms:
		#	assert table.hasRowAttr(atomName)
		for r in self._rawData:
			d = {}
			i = 0
			for atomName in self._atoms:
				d[atomName] = r[i]
				i += 1
			table.appendRow(**d)
		#q = Query(table,self._columnList)
		#for r in self._rawData:
		#	q.appendRow(*r)
		del self._rawData
		# del self._columnList

	def executeInsert(self,cursor,row):
		pass
		#id = row.getRowId()
		#assert not self._data.has_key(id)
		#self._data[id] = row
		
	def executeUpdate(self,cursor,row):
		pass
		#id = row.getRowId()
		#assert self._data.has_key(id)
		#self._data[id] = row

	def executeCount(self,query):
		return len(query.leadTable.getCachedRows())
	
	def executeGetLastId(self,table,knownId=()):
		if len(knownId) == 0:
			keys = table.getCachedRows().keys()
			# return max(*keys)
			if len(keys):
				return max(keys)
			return None
		ret = None
		pka = table.getPrimaryAtoms()
		l = []
		for (id,row) in table.getCachedRows().items():
			ok = True
			i = 0
			for value in knownId:
				if getattr(row,pka[i]) != value:
					ok = False
					break
			if ok:
				ret = max(ret,TODO)
				atomicRow = [None] * len(query.getAtoms())
				query.dict2atoms(row.getValues(),atomicRow)
				l.append(atomicRow)
		return ret
		
		
	def executePeek(self,table,id):
		try:
			return table.getCachedRows()[id]
		except KeyError:
			return None
		#return table[id]
		#return self._data[id]

	def executeSelect(self,query,
							limit=None,
							offset=None):
		l = []
		for (id,row) in query.leadTable.getCachedRows().items():
			ok = True
			for (col,value) in query._samples:
				if getattr(row,col) != value:
					ok = False
					break
			if ok:
				atomicRow = [None] * len(query.getAtoms())
				query.dict2atoms(row.getValues(),atomicRow)
				l.append(atomicRow)
		return ListCursor(l)

class ListCursor:
	def __init__(self,lst):
		self._list = lst
		self.rownumber = 0
		self.description = NotImplementedError
		self.rowcount = len(lst)

	def close(self):
		del self._list

	def fetchone(self):
		if self.rownumber == len(self._list):
			raise StopIteration
		self.rownumber += 1
		return self._list[self.rownumber-1]

	
