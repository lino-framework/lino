#coding: latin1
#----------------------------------------------------------------------
# $Id: table.py,v 1.26 2004/07/31 07:13:46 lsaffre Exp $
# Copyright: (c) 2003-2004 Luc Saffre
# License:	 GPL
#----------------------------------------------------------------------

import types

from lino.misc.compat import *
from lino.misc.descr import Describable

from datatypes import *
from rowattrs import RowAttribute,\
	  Field, BabelField, Pointer, Detail 
#from query import Query

from lino.misc.etc import issequence
from datasource import DataRow


reservedWords = """\
order
null
isnull
notnull
""".splitlines()

DEFAULT_PRIMARY_KEY = 'id'

class Table(Describable):
	
	class Row(DataRow):
		pass

	def __init__(self,name=None,label=None,doc=None):
		self._pk = None
		self._schema = None
		self._rowAttrs = {}
		self._views = {}
		
		if name is None:
			name = self.__class__.__name__
		if label is None:
			label = name
		#self._tableName = name
		Describable.__init__(self,name,label,doc)
		
		#self._label = None
		#self._doc = None
		
		#self._orderBy = None
		#self._columnList = None
		self._initStatus = 0
		#self._rowClass = DataRow

		self._peekColumnNames = ""

## 		ns = { '_table' : self }
## 		self._rowClass = classobj(self.getTableName()+"Row",
## 										  (WritableRow,), ns )

	def init(self):
		raise NotImplementedError

	#def getLabel(self):
	#	return self.getTableName()

	def init1(self):
		#print "%s : init1()" % self._tableName
		self.init()
		
		for (name,attr) in self.__dict__.items():
			if isinstance(attr,RowAttribute):
				self._rowAttrs[name] = attr
				self._peekColumnNames += name + " "
				try:
					meth = getattr(self,"after_"+name)
					attr.afterSetAttr = meth
				except AttributeError:
					pass
				
## 		for (name,attr) in self.__class__.__dict__.items():
##  			if type(attr) is types.ClassType:
## 				if issubclass(attr,DataRow):
## 					self._rowClass = attr
##  			elif type(attr) is types.MethodType:
## 				raise "hurra"
## 			else:
## 				print "foo", name, attr
## 				raise "bla"

		if self._pk == None:
			if not self._rowAttrs.has_key(DEFAULT_PRIMARY_KEY):
				f = Field(ROWID)
				setattr(self,DEFAULT_PRIMARY_KEY,f)
				self._rowAttrs[DEFAULT_PRIMARY_KEY] = f
			self.setPrimaryKey(DEFAULT_PRIMARY_KEY)

		for name,attr in self._rowAttrs.items():
			attr.onTableInit1(self,name)
			try:
				um = getattr(self.Row,"after_"+name)
				attr.afterSetAttr = um
			except AttributeError:
				pass
			
		self._initStatus = 1

	def init2(self):
		#print "%s : try init2()" % self._tableName

		for attr in self._rowAttrs.values():
			attr.onTableInit2(self,self._schema)
## 		if self._columnList is None:
## 			self._columnList = " ".join(self.getAttrList())

		
		atoms = []
		for attrname in self._pk:
			attr = self._rowAttrs[attrname]
			for (name,type) in attr.getNeededAtoms(None):
				atoms.append((name,type))
		self._primaryAtoms = tuple(atoms)
		
		self._initStatus = 2
		#print "%s : init2() done" % self._tableName
			
	def init3(self):
		"called during database startup. Don't override."
		for attr in self._rowAttrs.values():
			attr.onTableInit3(self,self._schema)
		self._initStatus = 3
			
	def init4(self):
		#if self._columnList is None:
		#	self._columnList = " ".join(self.getAttrList())
		self._initStatus = 4

			
	def addDetail(self,ptr,name,columnNames,**kw):
		# used by Pointer. onTableInit3()
		#print '%s.addDetail(%s)' % (self.getTableName(),name)
		dtl = Detail(ptr, columnNames=columnNames, **kw)
		self._rowAttrs[name] = dtl
		dtl.onTableInit1(self,name)
		#dtl.onTableInit2(self,schema)
		#setattr(self,ame,dtl)

	def addView(self,viewName,columnNames=None,**kw):
		if columnNames is not None:
			kw['columnNames'] = columnNames
		self._views[viewName] = kw

	def initDatasource(self,ds):
		if ds._viewName is None:
			return
		kw = self._views[ds._viewName]
		#print "Table.initDatasource(): " + repr(kw)
		ds.config(**kw)
		#print ds._samples
		#print "load() not yet implemented"

		
		
	def getAttrList(self):
		assert self._initStatus >= 3
		return [ name for name in self._rowAttrs.keys()]
	

## 	def values2id(self,knownValues):
## 		q = self.query()
## 		return q.values2id(knownValues)
	
	def setPrimaryKey(self,columnList):
		if type(columnList) == types.StringType:
			columnList = columnList.split()
		self._pk = tuple(columnList)


##		def setPrimaryKey(self,colNames):
##			"Use this during init() if primary key is not 'id'"
##			pk = []
##			for colName in colNames.split():
##				comp = self.findComponent(colName.strip())
##				if comp is None:
##					raise "%s : no such column in Table %s." % \
##							(colName,self.getName())
##				comp.setMandatory()
##				pk.append(comp)
##			self._pk = tuple(pk)
		

	def getPrimaryKey(self):
		"returns a tuple of the names of the columns who are primary key"
		if self._pk == None:
			raise "Table %s : primary key is None!" % self.getName()
		return self._pk # ('id',)

	def onConnect(self,area):
		pass

	def populate(self,area):
		pass

	def onAppend(self,row):
		pass

	def getPrimaryAtoms(self):
		try:
			return self._primaryAtoms
		except AttributeError:
			raise StartupDelay, str(self)+"._primaryAtoms"

	def getPeekColumnNames(self):
		return self._peekColumnNames
		#return " ".join(self.getAttrList())
		
## 		atoms = []
## 		for attrname in self._pk:
## 			# col = self.findColumn(colname)
## 			attr = self._rowAttrs[attrname]
## 			#if attr.getNeededAtoms() is None:
## 			#	 raise StartupDelay, \
## 			#			 "%s.%s.getNeededAtoms() is None" \
## 			#			 % (self.getName(), attr.name)
## 			# print attr.getNeededAtoms()
## 			for (name,type) in attr.getNeededAtoms():
## 				atoms.append((name,type))
## 		return tuple(atoms)
		
			
 	def setColumnList(self,columnList):
		pass
## 		self._columnList = columnList
		
## 	def getColumnList(self):
## 		return self._columnList

		
		
 	def setOrderBy(self,orderBy):
		pass
## 		self._orderBy = orderBy
		
## 	def getOrderBy(self):
## 		return self._orderBy

	def setTableId(self,schema,id):
		assert self._schema is None
		self._schema = schema
		self._id = id

	def getTableId(self):
		return self._id

	def getTableName(self):
		return self._name

## 	def setTableName(self,name):
## 		self._tableName = name

	def getSchema(self):
		return self._schema

##  	def validateRow(self,row):
##  		pass


	def __getattr__(self,name):
		return self.getRowAttr(name)

	def getRowAttr(self,name):
		try:
			return self._rowAttrs[name]
		except KeyError,e:
			raise AttributeError, \
					"%s has no attribute '%s'" % (repr(self), name)



class LinkTable(Table):
	def __init__(self, parentClass, childClass,*args,**kw):
		Table.__init__(self,*args,**kw)
		self._parentClass = parentClass
		self._childClass = childClass 
		

	def init(self):
		# Table.init(self)
		self.p = Pointer(self._parentClass)
		self.c = Pointer(self._childClass)
		self.setPrimaryKey("p c")
		del self._parentClass
		del self._childClass


class MemoTable(Table):
		
	def init(self):
		self.title = Field(STRING)
		self.abstract = Field(MEMO)
		self.body = Field(MEMO)

	class Row(Table.Row):
		
		def getLabel(self):
			return self.title

	

class TreeTable(Table):
		
	def init(self):
		self.seq = Field(INT)
		self.super = Pointer(self.__class__)
		#self.super = Pointer(table._rowMixins[0])
		self.super.setDetail('children')

	class Row(Table.Row):
		def getUpTree(self):
			l = []
			super = self.super
			while super:
				l.insert(0,super)
				super = super.super
			return l

class MemoTreeTable(MemoTable,TreeTable):
	def init(self):
		MemoTable.init(self)
		TreeTable.init(self)

	class Row(MemoTable.Row,TreeTable.Row):
		def getLabel(self):
			return self.title

		
		

class BabelTable(Table):
	
	def init(self):
		self.name = BabelField(STRING)
		
	class Row(Table.Row):
		def getLabel(self):
			return self.name
