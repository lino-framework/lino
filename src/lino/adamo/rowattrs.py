#----------------------------------------------------------------------
# $Id: rowattrs.py,v 1.23 2004/07/31 07:13:46 lsaffre Exp $
# Copyright: (c) 2003-2004 Luc Saffre
# License:	 GPL
#----------------------------------------------------------------------

import types
from copy import copy

from lino.misc.compat import *
from lino.misc.etc import issequence
from datatypes import DataVeto, StartupDelay
from widgets import Action
from lino.misc.descr import Describable
from components import OwnedThing

#def nop(*args):
#	pass

class NoSuchField(DataVeto):
	pass

class RowAttribute(OwnedThing):
	def __init__(self,width=None,label=None,doc=None):
		OwnedThing.__init__(self,label,doc)
		self._width = width
		self._isMandatory = False
		
	def acceptTrigger(self,row,value):
		pass
	
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
		pass
	
	def onTableInit2(self,owner,schema):
		pass
		#self.owner = table
		
 	def onTableInit3(self,owner,schema):
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
		self.acceptTrigger(row,value)
		row._values[self._name] = value
		
	def getCellValue(self,row):
		# overridden by BabelField and Detail
		return row.getFieldValue(self._name)
	
	def getFltAtoms(self,colAtoms,context):
		return colAtoms

	def getTestEqual(self,ds, colAtoms,value):
		raise NotImplementedError


	
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
		#return self.value2atoms(value, row.getContext())
		return self.value2atoms(value, row._ds._db)

		
## 		value = row._values[self._name]
## 		return self.value2atoms(value,atomicRow,colAtoms)
	
	def value2atoms(self,value,db):
		print self,value
		raise NotImplementedError
	
	
	def atoms2row(self,atomicRow,colAtoms,row):
		atomicValues = [atomicRow[atom.index]
							 for atom in colAtoms]
		row._values[self._name] = self.atoms2value(atomicValues,
																 row.getSession())

	#
	# change atoms2value(self,atomicRow,colAtoms,context)
	# to atoms2value(self,atomicValues,context)
	#
	def atoms2value(self,atomicValues,session):
		raise NotImplementedError

		
## 	def atoms2dict(self,atomicRow,valueDict,colAtoms,area):
## 		# overridden by Detail to do nothing
## 		valueDict[self._name] = self.atoms2value(atomicRow,colAtoms,area)
		
	
	def getNeededAtoms(self,ctx):
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
		
	def getNeededAtoms(self,ctx):
		return ((self._name, self.type),)
		#return (query.provideAtom(self.name, self.type),)

	def value2atoms(self,value,db):
		#assert issequence(atomicRow), repr(atomicRow)
		#assert issequence(colAtoms)
		#assert len(colAtoms) == 1
		#atomicRow[colAtoms[0].index] = value
		return (value,)


	def getTestEqual(self,ds, colAtoms,value):
		assert len(colAtoms) == 1
		a = colAtoms[0]
		return ds._connection.testEqual(a.name,a.type,value)

		
	def atoms2value(self,atomicValues,session):
		assert len(atomicValues) == 1
		return atomicValues[0]
		
	
	def getPreferredWidth(self):
		return self.type.width



class BabelField(Field):

	def getNeededAtoms(self,ctx):
		assert ctx is not None,\
				 "tried to use BabelField for primary key?"
		l = []
		for lang in ctx.getBabelLangs(): 
			l.append( (self._name+"_"+lang.id, self.type) )
		return l


	def getSupportedLangs(self):
		return self._owner._schema.getSupportedLangs()

	
	def setCellValue(self,row,value):
		langs = row.getSession().getBabelLangs()
		values = row.getFieldValue(self._name)
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
		langs = row.getSession().getBabelLangs()
		dblangs = row._ds._db.getBabelLangs()
		values = row.getFieldValue(self._name)
		#values = Field.getCellValue(self,row)
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
		langs = ds.getSession().getBabelLangs()
		lang = langs[0] # ignore secondary languages
		a = colAtoms[lang.index]
		return ds._connection.testEqual(a.name,a.type,value)

	#def value2atoms(self,value,atomicRow,colAtoms,context):
	def value2atoms(self,value,db):
		# value is a sequence with all langs of db
		dblangs = db.getBabelLangs()
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
		langs = row.getSession().getBabelLangs()
		dblangs = row._ds._db.getBabelLangs()
		values = row.getFieldValue(self._name)
		#values = Field.getCellValue(self,row)
		if values is None:
			values = [None] * len(dblangs)
			row._values[self._name] = values
		for lang in dblangs:
			#if lang.index != -1:
			value = atomicRow[colAtoms[lang.index].index]
			values[lang.index] = value
		#row._values[self._name] = l
	
	
	def getFltAtoms(self,colAtoms,context):
		l = []
		langs = context.getBabelLangs()
		for lang in langs:
			if lang.index != -1:
				l.append(colAtoms[lang.index])
		return l

	

	
class Match(Field):
	def __init__(self,origin,**kw):
		assert isinstance(origin,Field)
		self._origin = origin
		Field.__init__(self,origin.type,**kw)
		self.getLabel = origin.getLabel

	def __getattr__(self,name):
		return getattr(self._origin,name)

## class Button(RowAttribute,Action):
## 	def __init__(self,meth,label=None,*args,**kw):
## 		RowAttribute.__init__(self,label=label,doc=meth.__doc__)
## 		Action.__init__(self,meth,*args,**kw)
		
## 	def getCellValue(self,row):
## 		return self._func(row)
	


class Pointer(RowAttribute):
	"""
	
	A Pointer links from this to another table.
	
	"""
	def __init__(self, toClass,**kw):
		RowAttribute.__init__(self,**kw)
		self._toClass = toClass
		
		self.sticky = True # joins are sticky by default
		
		self.dtlName = None
		self.dtlColumnNames = None
		self.dtlKeywords = None
		self._neededAtoms = None

	def setDetail(self,name,columnNames=None,**kw):
		self.dtlName = name
		self.dtlColumnNames = columnNames
		self.dtlKeywords = kw
		
	def onTableInit1(self,owner,name):
		if self.dtlName is None:
			self.setDetail(owner.getTableName().lower()+'_by_'+self._name)
			
	def onTableInit2(self,owner,schema):
		self._toTables = schema.findImplementingTables(self._toClass)
		assert len(self._toTables) > 0, \
				 "%s.%s : found no tables implementing %s" % \
				 (owner.getName(),
				  str(self),
				  str(self._toClass))
		#if len(self._toTables) > 1:
		#	print "rowattrs.py:", repr(self)

	def onTableInit3(self,owner,schema):
		
		for toTable in self._toTables:
			toTable.addDetail(self,
									self.dtlName,
									self.dtlColumnNames,
									**self.dtlKeywords)
			
			
	def getNeededAtoms(self,ctx):
		
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
		

	def getPreferredWidth(self):
		# TODO: 
		return 10
		#w = 0
		#for pk in self._toTable.getPrimaryKey():
		#	w += pk.getPreferredWidth()
		#return w

		
	def _findToTable(self,tableId):
		for toTable in self._toTables:
			if toTable.getTableId() == tableId:
				return toTable
		raise "not found %d" % tableId

	
	def value2atoms(self,value,db):
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


	def atoms2value(self,atomicValues,sess):
		#ctx = row._ds._context
		if len(self._toTables) > 1:
			toTable = self._findUsedToTable(atomicValues)
			if toTable is None:
				return None
			atomicValues = self._reduceAtoms(toTable.getTableId(),
														atomicValues)
			toArea = getattr(sess.tables,toTable.getTableName())
		else:
			toTable = self._toTables[0]
			areaName = toTable.getTableName()
			toArea = getattr(sess.tables,areaName)
		
		if None in atomicValues:
			return None
		try:
			return toArea.getInstance(atomicValues,False)
		except DataVeto,e:
			return str(e)
	
	
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
	
	

		
class Detail(RowAttribute):
 	def __init__(self,pointer,label=None,doc=None,**kw):
		
		self.pointer = pointer
  		RowAttribute.__init__(self,label=label,doc=doc)
		kw[self.pointer._name] = None
		self._queryParams = kw
		
	def vetoDeleteIn(self,row):
		detailDs = self.getCellValue(row)
		if len(detailDs) == 0:
			return 
		#return "%s : %s not empty (contains %d rows)" % (
		#	str(row),self.name,len(ds))
		return "%s : %s not empty" % (str(row),self._name)
			
	def validate(self,row,value):
		raise "cannot set value of a detail"
	

	def onAreaInit(self,area):
		area.defineQuery(self._name,self._queryParams)
		

	def row2atoms(self,row):
		return ()
	
	def atoms2row(self,atomicRow,colAtoms,row):
		pass
	
	def atoms2value(self,atomicRow,colAtoms,sess):
		assert len(colAtoms) == 0
		raise "cannot"
		

	def getCellValue(self,row): 
		kw = dict(self._queryParams)
		#kw.setdefault('samples',{})
		#kw['samples'][self.pointer._name] = row
		kw[self.pointer._name] = row
 		slaveSource = getattr(row.getSession().tables,
									 self.pointer._owner.getTableName())
		return slaveSource.query(**kw)
		

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
		
	def value2atoms(self,value,db):
		raise "not allowed"


	def getPreferredWidth(self):
		return self.type.width


	def setCellValue(self,row,value):
		raise "not allowed"
		
	def getCellValue(self,row):
		return self._func(row)
	
	def atoms2row(self,atomicRow,colAtoms,row):
		pass

	
	
class FieldContainer:
	# inherited by Table and FormTemplate
	def __init__(self):
		self._fields = []
		self._rowAttrs = {}
		#self._peekColumnNames = ""

	def addField(self,name,fld):
		self._fields.append(fld)
		self._rowAttrs[name] = fld
		#self._peekColumnNames += name + " "
		fld.setOwner(self,name)
		try:
			meth = getattr(self.Instance,"accept_"+name)
			fld.acceptTrigger = meth
		except AttributeError:
			pass
		
		try:
			meth = getattr(self.Instance,"after_"+name)
			fld.afterSetAttr = meth
		except AttributeError:
			pass

	def getFields(self):
		return self._fields
	
	def __getattr__(self,name):
		return self.getRowAttr(name)
## 		try:
## 			return self.getRowAttr(name)
## 		except NoSuchField,e:
## 			raise AttributeError,e

## 	def getPeekColumnNames(self):
## 		return self._peekColumnNames
	
	def getRowAttr(self,name):
		try:
			return self._rowAttrs[name]
		except KeyError,e:
			#raise NoSuchField, \
			raise AttributeError,\
					"%s has no attribute '%s'" % (repr(self), name)

