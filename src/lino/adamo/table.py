#coding: latin1
#----------------------------------------------------------------------
# $Id: table.py,v 1.26 2004/07/31 07:13:46 lsaffre Exp $
# Copyright: (c) 2003-2004 Luc Saffre
# License:	 GPL
#----------------------------------------------------------------------

"""

Baseclass Table and some derived classes (LinkTable, MemoTable, TreeTable, MemoTreeTable, BabelTable)

"""

import types

from lino.misc.compat import *
from lino.misc.descr import Describable

#from lino.adamo import *
from widgets import Command
from datatypes import *
from rowattrs import RowAttribute,\
	  Field, BabelField, Pointer, Detail, FieldContainer
#from query import Query

from lino.misc.etc import issequence
from datasource import StoredDataRow


reservedWords = """\
order
null
isnull
notnull
""".splitlines()

DEFAULT_PRIMARY_KEY = 'id'

class SchemaComponent:
	
	def __init__(self):
		self._schema = None
		self._id = None
		
	def registerInSchema(self,schema,id):
		assert self._schema is None
		self._schema = schema
		self._id = id

	def getSchema(self):
		return self._schema


class Table(FieldContainer,SchemaComponent,Describable):
	"""
	
	Holds meta-information about a data table. There is one instance of
	each database table in a Schema.  Note that the Table does not
	worry about how the data is stored.
	
	
	"""
	
	class Row(StoredDataRow):
		pass

	def __init__(self,name=None,label=None,doc=None):
		SchemaComponent.__init__(self)
		FieldContainer.__init__(self)
		self._pk = None
		self._views = {}
		self._rowRenderer = None
		
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

		self._defaultView = None

## 		ns = { '_table' : self }
## 		self._rowClass = classobj(self.getTableName()+"Row",
## 										  (WritableRow,), ns )

	def init(self):
		raise NotImplementedError

	def cmd_show(self):
		return Command(self.show,label=self.getLabel())

	def show(self,sess):
		sess.openForm(self.getTableName())

	#def getLabel(self):
	#	return self.getTableName()


	def init1(self):
		#print "%s : init1()" % self._tableName
		self.init()
		
		for (name,attr) in self.__dict__.items():
			if isinstance(attr,RowAttribute):
				self.addField(name,attr)
				
		if self._pk == None:
			if not self._rowAttrs.has_key(DEFAULT_PRIMARY_KEY):
				f = Field(ROWID)
				setattr(self,DEFAULT_PRIMARY_KEY,f)
				self.addField(DEFAULT_PRIMARY_KEY,f)
				#self._rowAttrs[DEFAULT_PRIMARY_KEY] = f
			self.setPrimaryKey(DEFAULT_PRIMARY_KEY)

		for name,attr in self._rowAttrs.items():
			attr.onOwnerInit1(self,name)
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
		if self._defaultView is None:
			if self._views.has_key('std'):
				self._defaultView = 'std'
		self._initStatus = 4

			
	def addDetail(self,ptr,name,columnNames,**kw):
		# used by Pointer. onTableInit3()
		#print '%s.addDetail(%s)' % (self.getTableName(),name)
		dtl = Detail(ptr, columnNames=columnNames, **kw)
		self._rowAttrs[name] = dtl
		dtl.setOwner(self,name)
		#dtl.onTableInit2(self,schema)
		#setattr(self,ame,dtl)

	def addView(self,viewName,columnNames=None,**kw):
		if columnNames is not None:
			kw['columnNames'] = columnNames
		self._views[viewName] = kw
		
	def getView(self,viewName):
		return self._views.get(viewName,None)


	def initDatasource(self,ds):
		if ds._viewName is None:
			return
		view = self.getView(ds._viewName)
		if view is None:
			raise KeyError,ds._viewName+": no such view"
		#print "Table.initDatasource(): " + repr(kw)
		ds.config(**view)
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

 	def setColumnList(self,columnList):
		pass
		
 	def setOrderBy(self,orderBy):
		pass

	def getTableId(self):
		return self._id

	def getTableName(self):
		return self._name




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
