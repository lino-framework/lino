#----------------------------------------------------------------------
# $Id: rowattrs.py,v 1.23 2004/07/31 07:13:46 lsaffre Exp $
# Copyright: (c) 2003-2004 Luc Saffre
# License:	 GPL
#----------------------------------------------------------------------

import types
from copy import copy

from lino.misc.compat import *
from lino.misc.descr import Describable
from lino.misc.etc import issequence
from datatypes import DataVeto, StartupDelay

#def nop(*args):
#	pass



class RowAttribute(Describable):
	def __init__(self,width=None,label=None,doc=None):
		Describable.__init__(self,None,label,doc)
		#self._label = label
		self._isMandatory = False
		self._owner = None
		#self._name = None
		self._width = width
		
	def afterSetAttr(self,row):
		pass
		"""called after setting this value for this attribute in this
		row. Automatically replaced by after_xxx table method.
		Override this to modify other attributes who depend on this
		one.	"""

	def vetoDeleteIn(self,row):
		pass

	def format(self,v):
		return str(v)
		
	def parse(self,s):
		return s
		
		
	def onTableInit1(self,owner,name):
		assert self._owner is None
		self._owner = owner
		#self._name = name
		self.setName(name)

	def onTableInit2(self,table,schema):
		pass
		#self.owner = table
		
 	def onTableInit3(self,table,schema):
		pass

	def onAreaInit(self,area):
		pass
	
	def setSticky(self):
		self.sticky = True

	def setMandatory(self):
		self._isMandatory = True

	def onAppend(self,row):
		pass

	def validate(self,row,value):
		return value

	def checkIntegrity(self,row):
		pass

	def getAttrName(self):
		return self._name
	
## 	def __str__(self):
## 		return self._name

	def __repr__(self):
		return "<%s %s.%s>" % (self.__class__.__name__,
									  self._owner.getTableName(),
									  self._name)

	def getDefaultValue(self,row):
		return None

	def setCellValue(self,row,value):
		row._values[self._name] = value
		
	def getCellValue(self,row):
		# overridden by Detail
		try:
			return row._values[self._name]
		except KeyError:
			if row._isCompleting:
				return None
			row.makeComplete()
			try:
				return row._values[self._name]
			except KeyError:
				raise AttributeError,self._name

	
	def getFltAtoms(self,colAtoms,context):
		return colAtoms

	def getTestEqual(self,ds, colAtoms,value):
		raise NotImplementedError


	
## 	def getCellValue(self,row):
## 	#def getCellValue(self,row,col):
## 		raise NotImplementedError
	
	
	def row2atoms(self,row):
		"""fill into atomicRow the atomic data necessary to represent
		this column"""
		#rowValues = row._values
		#assert type(rowValues) is types.DictType
## 		if len(atomicRow) <= colAtoms[0].index:
## 			raise "atomicRow is %s\nbut index is %d" % (
## 				repr(atomicRow),colAtoms[0].index)
		#value = getattr(row,self._name)
		value = row._values.get(self._name)
## 		try:
## 			value = rowValues[self._name]
## 		except KeyError:
## 			value = None
## 		if isinstance(self,Pointer):
## 			print value
		return self.value2atoms(value, row._ds._context)

		
## 		value = row._values[self._name]
## 		return self.value2atoms(value,atomicRow,colAtoms)
	
	def value2atoms(self,value,context):
		print self,value
		raise NotImplementedError
	
	
	def atoms2row(self,atomicRow,colAtoms,row):
		atomicValues = [atomicRow[atom.index]
							 for atom in colAtoms]
		row._values[self._name] = self.atoms2value(atomicValues,
																 row._ds._context)

	#
	# change atoms2value(self,atomicRow,colAtoms,context)
	# to atoms2value(self,atomicValues,context)
	#
	def atoms2value(self,atomicValues,context):
		raise NotImplementedError

		
## 	def atoms2dict(self,atomicRow,valueDict,colAtoms,area):
## 		# overridden by Detail to do nothing
## 		valueDict[self._name] = self.atoms2value(atomicRow,colAtoms,area)
		
	
	def getNeededAtoms(self,db):
		return ()

## 	def getValueFromRow(self,row):
## 		try:
## 			return row._values[self._name]
## 		except KeyError,e:
## 			row._readFromStore()
## 			return row._values[self._name]
## 		#return row._values[name]

		


class Field(RowAttribute):
	"""
	
	A Field is a component which represents an atomic piece of data.
	A field will have a value of a certain type.
	
	"""
	def __init__(self,type,**kw):
		RowAttribute.__init__(self,**kw)
		self.type = type
		#self.visibility = 0
		#self.format = format

	def format(self,v):
		return self.type.format(v)
		
	def parse(self,s):
		return self.type.parse(s)
		
## 	def asFormCell(self,renderer,value,size=None):
## 		renderer.renderValue(value,self.type,size)
		
	def getNeededAtoms(self,db):
		return ((self._name, self.type),)
		#return (query.provideAtom(self.name, self.type),)

## 	def getCellValue(self,row):
## 		return row.getAtomicValue(self._name)
## 	def setCellValue(self,row,value):
## 		row._values[self._name] = value
## 		self.afterSetAttr(row)

	
## 	def getCellValue(self,col,row):
## 		colAtoms = col.getAtoms()
## 		assert len(colAtoms) == 1
		#return self._values[colAtoms[0].index]
		#return row.getAtomicValue(colAtoms[0].name)
	
## 	def setCellValue(self,col,row,value):
## 		colAtoms = col.getAtoms()
## 		assert len(colAtoms) == 1
## 		row.setAtomicValue(colAtoms[0].name,value)

	def value2atoms(self,value,context):
		#assert issequence(atomicRow), repr(atomicRow)
		#assert issequence(colAtoms)
		#assert len(colAtoms) == 1
		#atomicRow[colAtoms[0].index] = value
		return (value,)


	def getTestEqual(self,ds, colAtoms,value):
		assert len(colAtoms) == 1
		a = colAtoms[0]
		return ds._connection.testEqual(a.name,a.type,value)

## 	def value2dict(self,value,valueDict):
## 		valueDict[self.name] = value
		
		
	def atoms2value(self,atomicValues,context):
		assert len(atomicValues) == 1
		return atomicValues[0]
		
	
	def getPreferredWidth(self):
		return self.type.width



class BabelField(Field):

	def getNeededAtoms(self,db):
		assert db is not None,\
				 "tried to use BabelField for primary key?"
		l = []
		for lang in db.getBabelLangs(): #langs: #schema.getSupportedLangs():
			l.append( (self._name+"_"+lang.id, self.type) )
		return l
		#return (query.provideAtom(self.name, self.type),)


	def getSupportedLangs(self):
		return self._owner._schema.getSupportedLangs()

	
## 	def dict2atoms(self,rowValues,atomicRow,colAtoms):
## 		assert len(colAtoms) == len(self.getSupportedLangs())
## 		#self.value2atoms(rowValues[self.name],atomicRow,colAtoms)
## 		try:
## 			value = rowValues[self._name]
## 		except KeyError:
## 			value = None
## 		return self.value2atoms(value,atomicRow,colAtoms)

## 	def validate(self,row,value):
## 		if not issequence(value):
## 			raise "must be a sequence"
## 		if len(value) != len(self.getSupportedLangs()):
## 			raise "got %d instead of %d values" % (\
## 			len(value), len(self.getSupportedLangs()))
## 		return value
	
## 		else:
## 			l = [None for lang_id in self.owner.schema.langs]
## 			#l[row._area.getBabelIndex()] = value
## 			l[ds.getBabelIndex()] = value
## 			return tuple(l)

## 	def getValueFromRow(self,row):
## 		v = RowAttribute.getValueFromRow(self,row)
## 		if v is None:
## 			return self.owner.schema.babelNone
## 		return v
		#return v[row._area.getBabelIndex()]
## 		if ds is None:
## 			return v[0]
## 		return v[ds.getBabelIndex()]
		
## 	#def setCellValue(self,col,ds,atomicRow,value):
## 	def setCellValue(self,col,row,value):
## 		atoms = col.getAtoms()
## 		langs = row._ds._context.getBabelLangs()
## 		if len(langs) > 1:
## 			assert issequence(value), "%s is not a sequence" % repr(value)
## 			assert len(value) == len(langs), \
## 					 "%s expects %d values but got %s" % (repr(col),
## 																	  len(langs),
## 																	  repr(value))
## 			i = 0
## 			for (index,lang_id) in langs:
## 				if index != -1:
## 					atom = atoms[index]
## 					row.setAtomicValue(atom.name,value[i])
## 					#atomicRow[atom.index] = value[i]
## 				i += 1
## 		else:
## 			assert not issequence(value)
## 			index = langs[0][0]
## 			atom = atoms[index]
## 			row.setAtomicValue(atom.name,value)
## 			#atomicRow[atom.index] = value
		
## 	def getCellValue(self,col,row):
## 		atoms = col.getAtoms()
## 		langs = row._ds._context.getBabelLangs()
## 		if len(langs) > 1:
## 			l = []
## 			for (index,lang_id) in langs:
## 				if index != -1:
## 					atom = atoms[index]
## 					l.append(row.getAtomicValue(atom.name))
## 				else:
## 					l.append(None)
## 			return l
## 		else:
## 			index = langs[0][0]
## 			atom = atoms[index]
## 			return row.getAtomicValue(atom.name)
	
		
##  	def row2atoms(self,row,atomicRow,colAtoms):
## 		value = getattr(row,self._name)
## 		return self.value2atoms(value,atomicRow,colAtoms,
## 										row._ds._context)
	
	def setCellValue(self,row,value):
		langs = row._ds._context.getBabelLangs()
		values = Field.getCellValue(self,row)
		if values is None:
			values = [None] * len(row._ds._db.getBabelLangs())
			row._values[self._name] = values
		if len(langs) > 1:
			assert issequence(value), "%s is not a sequence" % repr(value)
			assert len(value) == len(langs), \
					 "%s expects %d values but got %s" % (self._name,
																	  len(langs),
																	  repr(value))
			i = 0
			for lang in langs:
				if lang.index != -1:
					values[lang.index] = value[i]
				i += 1
		else:
			assert not issequence(value)
			index = langs[0].index
			assert not index == -1
			values[index] = value
			
		
	def getCellValue(self,row):
		langs = row._ds._context.getBabelLangs()
		dblangs = row._ds._db.getBabelLangs()
		values = Field.getCellValue(self,row)
		if values is None:
			values = [None] * len(dblangs)
		else:
			assert issequence(values), "%s is not a sequence" % repr(values)
			assert len(values) == len(dblangs), \
					 "Expected %d values but got %s" % ( len(dblangs),
																	 repr(values))
		
		if len(langs) > 1:
			l = []
			for lang in langs:
				if lang.index != -1:
					l.append(values[lang.index])
				else:
					l.append(None)
			return l
		else:
			index = langs[0].index
			assert not index == -1
			return values[index]
		
	def getTestEqual(self,ds, colAtoms,value):
		langs = ds._context.getBabelLangs()
		lang = langs[0] # ignore secondary languages
		a = colAtoms[lang.index]
		return ds._connection.testEqual(a.name,a.type,value)

	#def value2atoms(self,value,atomicRow,colAtoms,context):
	def value2atoms(self,value,context):
		# value is a sequence with all langs of db
		dblangs = context._db.getBabelLangs()
		rv = [None] * len(dblangs)
		#langs = context.getBabelLangs()
		if value is None:
			return rv
## 			for lang in dblangs:
## 				atomicRow[colAtoms[lang.index].index] = None
## 			return 
		assert issequence(value), "%s is not a sequence" % repr(value)
		assert len(value) == len(dblangs), \
				 "Expected %d values but got %s" % ( len(dblangs),
																 repr(value))
		i = 0
		for lang in dblangs:
			#atomicRow[colAtoms[lang.index].index] = value[i]
			rv[lang.index] = value[i]
			i += 1

		return rv
			
 	def atoms2row(self,atomicRow,colAtoms,row):
		langs = row._ds._context.getBabelLangs()
		dblangs = row._ds._db.getBabelLangs()
		values = Field.getCellValue(self,row)
		if values is None:
			values = [None] * len(dblangs)
			row._values[self._name] = values
		for lang in dblangs:
			#if lang.index != -1:
			value = atomicRow[colAtoms[lang.index].index]
			values[lang.index] = value
		#row._values[self._name] = l
	
##  	def atoms2row(self,atomicRow,colAtoms,row):
## 		langs = row._ds._context.getBabelLangs()
## 		if len(langs) > 1:
## 			l = []
## 			for lang in langs:
## 				if lang.index != -1:
## 					value = atomicRow[colAtoms[lang.index].index]
## 					l.append(value)
## 				else:
## 					l.append(None)
## 			row._values[self._name] = tuple(l)
## 		else:
## 			index = langs[0].index
## 			assert index != -1
## 			value = atomicRow[colAtoms[index].index]
## 			row._values[self._name] = value
	
	def getFltAtoms(self,colAtoms,context):
		l = []
		langs = context.getBabelLangs()
		for lang in langs:
			if lang.index != -1:
				l.append(colAtoms[lang.index])
		return l

	

	


	

class Pointer(RowAttribute):
	"""
	
	A Pointer links from this to another table.
	
	"""
	def __init__(self, toClass,**kw):
		RowAttribute.__init__(self,**kw)
		self._toClass = toClass
		
		# joins are sticky by default:
		self.sticky = True
		
		self.dtlName = None
		self.dtlColumnNames = None
		self.dtlKeywords = None
		self._neededAtoms = None

	def setDetail(self,name,columnNames=None,**kw):
		self.dtlName = name
		self.dtlColumnNames = columnNames
		self.dtlKeywords = kw
		
	def onTableInit1(self,owner,name):
		RowAttribute.onTableInit1(self,owner,name)
		if self.dtlName is None:
			self.setDetail(owner.getTableName().lower()+'_by_'+self._name)
			
	def onTableInit2(self,fromTable,schema):
		#RowAttribute.onTableInit2(self,fromTable,schema)
		self._toTables = schema.findImplementingTables(self._toClass)
		assert len(self._toTables) > 0, \
				 "%s.%s : found no tables implementing %s" % \
				 (fromTable.getName(),
				  str(self),
				  str(self._toClass))
		#if len(self._toTables) > 1:
		#	print "rowattrs.py:", repr(self)

	def onTableInit3(self,fromTable,schema):
			
		for toTable in self._toTables:
			toTable.addDetail(self,
									self.dtlName,
									self.dtlColumnNames,
									**self.dtlKeywords)
## 			dtl = Detail(self,
## 							 columnNames=self.dtlColumnNames,
## 							 **self.dtlKeywords)
## 			setattr(toTable,self.dtlName,dtl)
			# toTable.addDetail(self.detail)
			
			
	def getNeededAtoms(self,db):
		
		""" The toTable is possibly not yet enough initialized to tell
		me her primary atoms. In this case getPrimaryAtoms() will raise
		StartupDelay which will be caught in Schema.startup() """
		
		if self._neededAtoms is None:
			neededAtoms = []
			if len(self._toTables) > 1:
				#neededAtoms.append((self.name+"_tableId",AREATYPE))
				i = 0
				for toTable in self._toTables:
					for (name,type) in toTable.getPrimaryAtoms():
						neededAtoms.append(
							(self._name + toTable.getTableName()+"_" + name,
							 type) )
					i += 1
			else:
				for (name,type) in self._toTables[0].getPrimaryAtoms():
					neededAtoms.append( (self._name + "_" + name,
												type) )

			self._neededAtoms = tuple(neededAtoms)
		return self._neededAtoms

	def checkIntegrity(self,row):
		pointedRow = self.getCellValue(row)
		if pointedRow is None:
			return # ok

		if pointedRow._ds.peek(*pointedRow.getRowId()) is None:
			return "%s points to non-existing row %s" % (
				self._name,str(pointedRow.getRowId()))
		

					

## 	def asFormCell(self,renderer,value,size=None):
## 		renderer.renderLink(
## 			url=renderer.uriToRow(value),
## 			label=value.getLabel())
		

	def getPreferredWidth(self):
		# TODO: 
		return 10
	
		#w = 0
		#for pk in self._toTable.getPrimaryKey():
		#	w += pk.getPreferredWidth()
		#return w

		
## 	def findTableId(self,area):
## 		i = 0
## 		for toTable in self._toTables:
## 			if toTable.name == area._table.name:
## 				return i
## 			i+=1
## 		raise "findTableId() failed"

	def _findToTable(self,tableId):
		for toTable in self._toTables:
			if toTable.getTableId() == tableId:
				return toTable
		raise "not found %d" % tableId

	
## 	def value2atoms(self,value,atomicRow,colAtoms,context):
## 		pointedRow = value
## 		#print repr(pointedRow)
## 		if pointedRow is None:
## 			for atom in colAtoms:
## 				atomicRow[atom.index] = None
## 			return
		
## 		if len(self._toTables) > 1:
## 			#print "rowattrs.py : woa"
## 			tableId = pointedRow._ds._table.getTableId()
## 			colAtoms = self._reduceColAtoms(tableId,colAtoms)

## 		id = pointedRow.getRowId()
## 		# print 20040617, repr(pointedRow), id
## 		assert len(id) == len(colAtoms),\
## 				 "len(%s) != len(%s)" % (repr(id),repr(colAtoms))
## 		i = 0
## 		for atom in colAtoms:
## 			atomicRow[atom.index] = id[i]
## 			i += 1

	def value2atoms(self,value,context):
		pointedRow = value
		#print repr(pointedRow)
		if pointedRow is None:
			return [None] * len(self._neededAtoms)
		
		if len(self._toTables) == 1:
			return pointedRow.getRowId()
		else:
			rv = [None] * len(self._neededAtoms)
			i = 0
			tableId = pointedRow._ds._table.getTableId()
			rid = pointedRow.getRowId()
			for toTable in self._toTables:
				if toTable.getTableId() == tableId:
					ai = 0
					for a in toTable.getPrimaryAtoms():
						rv[i] = rid[ai]
						i+=1
						ai+=1
					return rv
				else:
					i += len(toTable.getPrimaryAtoms())


	def atoms2value(self,atomicValues,ctx):
		#ctx = row._ds._context
		if len(self._toTables) > 1:
			toTable = self._findUsedToTable(atomicValues)
			if toTable is None:
				return None
			atomicValues = self._reduceAtoms(toTable.getTableId(),
														atomicValues)
			toArea = getattr(ctx,toTable.getTableName())
		else:
			toTable = self._toTables[0]
			areaName = toTable.getTableName()
			toArea = getattr(ctx,areaName)
		
## 		atomicId = []
## 		for atom in colAtoms:
## 			v = atomicRow[atom.index]
## 			if v is None:
## 				return None
## 			atomicId.append(v)
		if None in atomicValues:
			return None
		try:
			return toArea.getInstance(atomicValues,False)
		except DataVeto,e:
			return str(e)
	
## 	def makeRowInstance(self,ds,atomicRow,atoms):
## 		row = self.
	
	def _findUsedToTable(self,atomicValues):
		i = 0
		for toTable in self._toTables:
			for justLoop in toTable.getPrimaryAtoms():
				#if atomicRow[colAtoms[i].index] is not None:
				if atomicValues[i] is not None:
					return toTable
				i += 1
		return None
	
	def _reduceAtoms(self,tableId,atomicValues):
		"""
			
		We want only the atoms for this tableId.  Example: if there
		are 3 possible tables (tableId may be 0,1 or 2) and pklen
		is 2, then there are 2*3 = 6 atoms.
			
			  tableId 0 -> I want atoms 0 and 1  -> [0:2]
			  tableId 1 -> I want atoms 2 and 3  -> [2:4]
			  tableId 2 -> I want atoms 4 and 5  -> [4:7]
			  
		"""
			
		# the first atom is the tableId
		for toTable in self._toTables:
			pklen = len(toTable.getPrimaryAtoms())
			if toTable.getTableId() == tableId:
				return atomicValues[:pklen]
			else:
				atomicValues = atomicValues[pklen:]
		raise "invalid tableId %d" % tableId
	
## 	def atoms2value(self,atomicRow,colAtoms,area):
## 		assert len(colAtoms) == len(self._neededAtoms)
## 		if len(self._toTables) > 1:
## 			#print colAtoms
## 			# first atom is the tableId. pop it off
## 			toTable = self._findUsedToTable(atomicRow,colAtoms)
## 			if toTable is None:
## 				return None
## 			colAtoms = self._reduceColAtoms(toTable.getTableId(),
## 													  colAtoms)
## 			#colAtoms = colAtoms[1:]
## 			#toTable = self._findToTable(tableId)
## 			toArea = getattr(area._db,toTable.getTableName())

## 			#pklen = len(toTable.getPrimaryAtoms())
## 			#start = tableId*pklen
## 			#print [a.name for a in colAtoms]
## 			#print tableId
## 			#colAtoms = colAtoms[start:start+pklen]
## 			#print [a.name for a in colAtoms]
## 		else:
## 			areaName = self._toTables[0].getTableName()
## 			toArea = getattr(area._db,areaName)
		
## 		id = []
## 		for atom in colAtoms:
## 			v = atomicRow[atom.index]
## 			if v is None:
## 				#print atomicRow
## 				#print [(a.name,a.index) for a in colAtoms]
## 				#raise "This should not happen ?"
## 				return None
## 			id.append(v) 
## 		id = tuple(id)
## 		try:
## 			return toArea.provideRowInstance(id,new=False)
## 		except DataVeto,e:
## 			return str(e)
			
	#def getToTable(self):
	#	return self._toTable
	

		
class Detail(RowAttribute):
 	def __init__(self,pointer,label=None,doc=None,**kw):
		
		#assert not kw.has_key(pointer.name)
		self.pointer = pointer
## 		#assert isinstance(slaveTable,Table)
  		RowAttribute.__init__(self,label=label,doc=doc)
## 		self._slaveClass = slaveClass
		#self.name = name
		#self.fromTable = table
		#assert isinstance(slaveClass,types.ClassType)
		#self._slaveClass = slaveClass
		kw[self.pointer._name] = None
		self._queryParams = kw
		#self.query = None
		
	def vetoDeleteIn(self,row):
		detailDs = self.getCellValue(row)
		if len(detailDs) == 0:
			return 
		#return "%s : %s not empty (contains %d rows)" % (
		#	str(row),self.name,len(ds))
		return "%s : %s not empty" % (str(row),self._name)
			
	def validate(self,row,value):
		raise "cannot set value of a detail"
	
## 	def asFormCell(self,renderer,value,size=None):
## 		renderer.asParagraph(value)

	def onAreaInit(self,area):
		area.defineQuery(self._name,self._queryParams)
		
## 				if hasattr(value,'asFormCell'):
## 					value.asFormCell(renderer)
## 				else:
## 					type = getattr(attr,'type',None)
## 					renderer.renderValue(value,type)
		
##   	def onTableInit3(self,table,schema):
##  		self.query = self.pointer._owner.defineQuery(self._name,
## 																	**self._kw)
		
		# don't del self._kw because a Detail can exist in more than one
		# table...
		
## ## 		self.query = self.pointer._toTables[0].provideQuery(
## ## 			self.name, **self.kw)

	def row2atoms(self,row):
		return ()
	
	def atoms2row(self,atomicRow,colAtoms,row):
		pass
	
	def atoms2value(self,atomicRow,colAtoms,context):
		assert len(colAtoms) == 0
		raise "cannot"
		
## 	def getValueFromRow(self,row):
## 		return DetailInstance(self,row)


## 	class DetailValue:
## 		def __init__(self,area

	def getCellValue(self,row): 
		kw = dict(self._queryParams)
		#ptrCol = ds._query.getColumn(self.pointer._name)
		kw[self.pointer._name] = row
 		slaveSource = getattr(row._ds._context,
									 self.pointer._owner.getTableName())
		return slaveSource.query(**kw)
		#return row._area.query(self._name,**kw)
		#return q.datasource(ds._area._db)
		
## 	def getValueFromRow(self,row):
## 		kw = dict(self._queryParams)
## 		kw[self.pointer._name] = row
## 		db = row._ds._area._db
## 		#area = self.pointer._owner.defineQuery(self._name,
## 		#slaveArea = getattr(row._area._db,
## 		#						  self.pointer.owner.name)
## 		# from area import Area
## 		# assert isinstance(dtlArea,Area)
## 		# kw.update(self.kw)
## 		#return self.query.datasource(row._area._db,**kw)
## 		#q = self.query.child(**kw)
## 		q = self.query.child(**kw)
## 		# q = copy(self.query)
## 		# q.setSamples(**kw)
## 		return q.datasource(row._area._db)
## 		#return slaveArea.report(**kw)
## 		q = slaveArea.query(**kw)
## 		rpt = q.report()
## 		return rpt

	
	
## 	def onTableInit3(self,table,schema):
## 		slaveTables = schema.findImplementingTables(self._slaveClass)
## ## 		if len(slaveTables) != 1:
## ## 			raise "%s is implemented by %s" % (str(self._slaveClass),
## ## 														  str(slaveTables))
## 		self.slaveTable= slaveTables[0]
## 		for (name,attr) in self.slaveTable._rowAttrs.items():
## 			if isinstance(attr,Pointer):
## 				for cl in table._rowMixins:
## 					if attr._toClass == cl:
## 						self.pointer = attr
## 						return
## ## 					else:
## ## 						print "%s != %s" % (
## ## 							repr(cl),
## ## 							repr(attr._toClass))
## 		raise 'there is no pointer from %s to %s' % (
## 			self.slaveTable.name, table.name)
		
	
## 	def report(self,row,**kw):
## 		q = self.query()
## 		return q.report(**kw)
	
## 	for toTable in self._toTables:
## 		toTable.addRowMethod(self._detailName,query)
		
		
		
## ##			self.slaveTable = slaveTable
		
## ##			# the fields themselves don't yet exist during initialization
## ##			# so we just store the name
## 		self.pointer = pointer
## ##			# self.columnList = columnList
		
## ##			# self.price = 3
## ##			self.isDefaultColumn = False


## 	def onTableInit2(self,table,schema):
## 		l = schema.findImplementingTables(self._slaveClass)
## 		if len(l) == 1:
## 			self._slaveTable = l[0]
## 		else:
## 			raise "%s.%s : found %d tables implementing %s" % \
## 					(table.getName(),
## 					 str(self),
## 					 len(l),
## 					 str(self._toClass))
		
## 		del self._slaveClass

## 	def dict2atoms(self,valueDict,atomicRow,colAtoms):
## 		pass

## 	def caller(self,row):
## 		samples={}
## 		samples[self.pointer.name] = getattr(row,self.name)
## 		return row._area.instances(samples)
	
	
## 	def atoms2value(self,atomicRow,colAtoms,area):
## 		return self.caller
	


	


## class DetailInstance:
## 	def __init__(self,detail,row):
## 		raise "not used"
## 		self.detail = detail
## 		self.row = row

## 	def asLabel(self,renderer):
## 		q = self.query()
## 		rpt = q.report()
## 		return rpt.asLabel(renderer)

## 	def query(self,**kw):
## 		assert not kw.has_key(self.detail.pointer.name)
## 		kw[self.detail.pointer.name] = self.row
## 		slaveArea = getattr(self.row._area._db,
## 								  self.detail.pointer.owner.name)
## 		# from area import Area
## 		# assert isinstance(dtlArea,Area)
## 		kw.update(self.detail.kw)
## 		return slaveArea.query(**kw)
	
## ## 	def query(self,**kw):
## ## 		return self.detail.query(self.row,**kw)
		


class Vurt(RowAttribute):
	"""
	
	A Vurt (virtual field) is a method 
	
	"""
	def __init__(self,func,type,**kw):
		RowAttribute.__init__(self,**kw)
		self._func = func
		self.type = type

	def format(self,v):
		return self.type.format(v)
		
	def parse(self,s):
		raise "not allowed"
		
	def value2atoms(self,value,context):
		raise "not allowed"


	def getPreferredWidth(self):
		return self.type.width


	def setCellValue(self,row,value):
		raise "not allowed"
		
	def getCellValue(self,row):
		return self._func(row)
	
	def atoms2row(self,atomicRow,colAtoms,row):
		pass
	
