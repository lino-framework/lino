#coding: latin1
#----------------------------------------------------------------------
# $Id: table.py,v 1.23 2004/04/25 18:06:27 lsaffre Exp $
# Copyright: (c) 2003-2004 Luc Saffre
# License:	 GPL
#----------------------------------------------------------------------

import types

from lino.misc.compat import *
from lino.misc.descr import Describable

from datatypes import *
from rowattrs import Field, BabelField, Pointer, Detail #, RowMethod
from query import Query

from lino.misc.etc import issequence


reservedWords = """\
order
null
isnull
notnull
""".splitlines()

DEFAULT_PRIMARY_KEY = 'id'

class Form:
	def __init__(self,*args,**kw):
		pass
	def setRange(self,rng):
		pass

class Table(Describable):
	def __init__(self,schema,id,name,rowMixin,label=None):
		if label is None:
			label = name
		Describable.__init__(self,None,label=label)
		self.id = id
		self.name = name
		self.schema = schema
		#if conn is None:
		#	conn = db.getConnection()
		#self._connection = conn
		
		#self.indexes = []
		#self.pkSep = '.'
		self._pk = None
		# self.name = None
		self._rowAttrs = {}
		self._queries = {}
		#self._rowMethods = {}
		#self._details = {}
		#self._reports = {}
		#self._findColumns = ()
		#self.peekQuery = None
		
		# self._rowBase = rowClass
		self._rowMixins = []
		if rowMixin is not None:
			if issequence(rowMixin):
				self._rowMixins += rowMixin
			else:
				self._rowMixins.append(rowMixin)
		#self._rowStubs = []

		self._orderBy = None
		self._columnList = None

	def setColumnList(self,columnList):
		self._columnList = columnList
		
	def getColumnList(self):
		return self._columnList
		
	def setOrderBy(self,orderBy):
		self._orderBy = orderBy
		
	def getOrderBy(self):
		return self._orderBy 

	#def setRowMixin(self,mixin=None):
	#	 if mixin is None:
	#		 self._rowBases = (WritableRow,)
	#	 else:
	#		 assert type(mixin) is types.ClassType
	#		 self._rowBases = (mixin,WritableRow)

	def init1(self,schema):
		self._rowMixins = tuple(self._rowMixins)
		for mixin in self._rowMixins:
			#self._rowStubs.append(mixin(self))
			dummy = mixin()
			if hasattr(dummy,'init'):
				dummy.init(self)
		if self._pk == None:
			if not self._rowAttrs.has_key(DEFAULT_PRIMARY_KEY):
				self.addField(DEFAULT_PRIMARY_KEY,ROWID)
			self.setPrimaryKey(DEFAULT_PRIMARY_KEY)
		for attr in self._rowAttrs.values():
			attr.onTableInit1(self,schema)

	def init2(self,schema):
		for attr in self._rowAttrs.values():
			attr.onTableInit2(self,schema)
		if self._columnList is None:
			self._columnList = " ".join(self.getAttrList())
		#if self._orderBy is None:
		#	self._orderBy = 

	def init3(self,schema):
		"called during database startup. Don't override."
		for attr in self._rowAttrs.values():
			attr.onTableInit3(self,schema)
		#for dtl in self._details.values():
		#	dtl.onTableInit3(self,schema)
		#self.provideQuery(None)
		#self._queries[None] = Query(self)
		#for (name,attr) in self._rowAttrs.items():
		#	self.peekQuery.addColumn(attr,name,None,True)
			# col.setupAtoms(self)
			# self.addColumn(comp.getName(),None,self,comp)
		#self.peekQuery.initQuery()
		
				
		#if len(self._rowBases) == 2:
##			for (name,meth) in self.getRowMixin().__dict__.items():
##				if name[0:3] == "on_":
##					attr = self._rowAttrs[name[3:]]
##					attr.onSetAttr = meth

	def isSetup(self):
		return self._queries.has_key(None) #] is not None

 	def onConnect(self,area):
		pass ## conn.onTableSetup(self)

	def populate(self,area):
		for mixin in self._rowMixins:
			dummy = mixin()
			if hasattr(dummy,'populate'):
				dummy.populate(area)
		
					

##		def getRowMixin(self):
##			return self._rowBases[0]

	
##		def link(self,db):
##			"override this method to declare Joins from this Table to others"
##			dummy = self.getRowMixin()
##			if dummy is not None:
##				dummy().link(self,db)

##		def addRowBase(self,rowBase):
##			assert type(rowBase) is types.ClassType
##			self._rowBases.append(rowBase)
	
	def onAppend(self,row):
		"override this to do something whenever a row in this table has been created"
		pass

##		def populateDemo(self):
##			"(deprecated) override this if your table has a default set of demo data"
##			pass
	
	def __str__(self):
		return self.name
	
	def __repr__(self):
		return self.name

	def getName(self):
		return self.name

	def defineQuery(self,name,**kw):
		try:
			return self._queries[name]
		except KeyError,e:
			q = Query(self,name,**kw)
			self._queries[name] = q
			return q
## 		assert not self._queries.has_key(name), \
## 				 "%s : duplicate query definition %s" % (self.name, name)
## 		q = Query(self,name,**kw)
## 		self._queries[name] = q
## 		return q
		

 	def query(self,name=None,**kw):
		q = self._queries[name]
		if len(kw) == 0:
			return q
		return q.child(name,**kw)

## 		#if columnList is not None:
## 		#	q.setColumnList(columnList)
## 		#return q

## 	def report(self,**kw):
## 		#return self.db.reportClass(leadTable=self,**kw)
## 		return Report(self,**kw)
	
	def form(self,**kw):
		#return self.db.reportClass(leadTable=self,**kw)
		return Form(self,**kw)

## 	def provideReport(self,name=None,**kw):
## 		if name is None:
## 			name = "std"
## 		try:
## 			rpt = self._reports[name]
## 			rpt.setDefaultParams(**kw)
## 		except KeyError:
## 			rpt = self.report(name=name,**kw)
## 			self._reports[name] = rpt
## 		return rpt

## 	def addReport(self,name,rpt):
## 		self._reports[name] = rpt


## 	def cursor(self,columnList=None):
## 		q = self.query(columnList)
## 		return q.cursor()

	def getAttrList(self):
		return [ name for name in self._rowAttrs.keys()]
	
			
	def setupPrimaryKey(self):
		"called during startup. Don't override."
		if self._pk == None:
			self.setPrimaryKey("id")
			

	def values2id(self,knownValues):
		q = self.query()
		return q.values2id(knownValues)
	
	def defineMenus(self,win):
		pass
## 		mb = win.addMenuBar("data","&Data menu")
## 		mnu = mb.addMenu("&Row")
## 		mnu.addItem("&Append",self.mnu_appendRow,win)
## 		mnu = mb.addMenu("&File")
## 		mnu.addItem("E&xit",win.close)

		
##		def commitRow(self,row):
##			self.db.commitRow(self,row)
		
##		def instanciateRow(self,*args,**kw):
		
##			"""For internal use. $values$ is a tuple containing an initial
##			value for each component of the table."""
		
##			return apply(self._rowClass,args,kw)


	def addField(self,name,type,**kw):
		"Use this during init(). Don't override."
		if len(kw) :
			type = type.child(**kw)
		f = Field(self,name,type)
		self.addRowAttribute(name,f)
		return f
		
	def addBabelField(self,name,type,**kw):
## 		if len(kw) :
## 			type = type.child(**kw)
## 		f = BabelField(self,name,type)
## 		self.addRowAttribute(name,f)
## 		return f
	
## 		if len(self.schema.langs) == 1:
## 			self.addField(name,type,**kw)
## 		else:
			for lang in self.schema.langs:
				self.addField(name+"_"+lang,type,**kw)
		
	def addPointer(self,name,toClass,detailName=None):
		"Use this during init()"
		#assert isinstance(toTable,Table), \
		#		  "%s is not a Table instance" % repr(toTable)
		p = Pointer(name,toClass)
		return self.addRowAttribute(name,p)
		#if detailName != None:
		#	toTable.addDetail(detailName,self,p)

 	def addDetail(self,dtl):
		return self.addRowAttribute(dtl.name,dtl)
		#self._rowAttrs[dtl.name] = dtl
			
		
## 	def addDetail(self,name,slaveClass,pointer):
## 		#assert isinstance(slaveClass,Table)
## 		#linkTable = app.tables[linkTableName]
## 		dtl = Detail(name,slaveClass,pointer)
## 		self.addRowAttribute(name,dtl)

## 	def addRowMethod(self,name,m):
## 		"f is a function to be called with a Row as argument"
## 		self._rowMethods[name] = m
## 		#addRowAttribute(name,RowMethod(self,name))

	def addRowAttribute(self,name,attr):
		assert not name.lower() in reservedWords,\
				 "%s is a reserved SQL word" % name
		#assert not name in self._rowAttrs.keys(),\
		#		 "duplicate attribute definition %s in %s" % (name,
		#																	 self.name)
		
		assert not self.isSetup(),\
				 "cannot add attribute after setup()"
		self._rowAttrs[name] = attr
		

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

	def getPrimaryAtoms(self):
		atoms = []
		for attrname in self._pk:
			# col = self.findColumn(colname)
			attr = self._rowAttrs[attrname]
			#if attr.getNeededAtoms() is None:
			#	 raise StartupDelay, \
			#			 "%s.%s.getNeededAtoms() is None" \
			#			 % (self.getName(), attr.name)
			# print attr.getNeededAtoms()
			for (name,type) in attr.getNeededAtoms():
				atoms.append((name,type))
		return tuple(atoms)
		
	

	def getRowAttributes(self):
		return self._rowAttrs

## 	def setFindColumns(self,columnList):
## 		if type(columnList) == types.StringType:
## 			columnList = columnList.split()
## 		self._findColumns = tuple(columnList)
		
## 	def getFindFilter(self,what):
## 		# not finished
## 		"override this to specify more appropriate filter"
## 		for (name,attr) in self._rowAttrs.items():
## 			if attr.type is STRING:
## 				return '%s = %s' % (
## 					name, self._connection.value2sql(what, attr.type))
## 		raise "Cannot find() in this table"

## 	def find(self,what):
## 		# not finished
## 		expr = "+' '+".join(self._findColumns) + " = " + \
## 				 self._connection.value2sql(what, STRING)
## 		l = []
## 		q = self.peekQuery.copy()
## 		q.setFilter(expr)
## 		sql = q.getSqlSelect()
## 		for row in q:
## 			l.append(row)
## 		# TODO : peekQuery should not be modifiable by user code
## 		# okay for now because we reset filter manually...
## 		# self.peekQuery.setFilter()
		
## 		if len(l) == 1:
## 			return l[0]
## 		raise ("found %d instead of 1 row using %s" % (len(l), sql))
## 		# return None

	def getTableId(self):
		return self.id


	def __getattr__(self,name):
		return self.getRowAttr(name)

	def getRowAttr(self,name):
		try:
			return self._rowAttrs[name]
		except KeyError,e:
			raise AttributeError, \
					"Table %s has no attribute '%s'" % (self.name, name)



	
## 	def executeSelect(self,query):
## 		return self._connection.executeSelect(query)

	

class LinkTable(Table):
	def __init__(self, schema, id, name,
					 parentClass, childClass,
					 rowClass):
		Table.__init__(self, schema, id, name,rowClass) 
		self._parentClass = parentClass
		self._childClass = childClass 
		

	def init(self):
		Table.init(self)
		self.addPointer("p",self._parentClass)
		self.addPointer("c",self._childClass)
		self.setPrimaryKey("p c")
		del self._parentClass
		del self._childClass
		



