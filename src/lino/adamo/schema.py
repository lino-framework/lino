#coding: latin1
#----------------------------------------------------------------------
# $Id: schema.py,v 1.14 2004/07/31 07:13:46 lsaffre Exp $
# Copyright: (c) 2003-2004 Luc Saffre
# License:	 GPL
#----------------------------------------------------------------------


from lino.misc.pset import PropertySet

from widgets import Window
from table import Table, LinkTable
from datatypes import StartupDelay
from database import Database

#from babel import Language
#from report import Report

#from datatypes import AREA




class Schema(PropertySet):

	HK_CHAR = '&'
	defaultLangs = ('en',)

	defaults = {
		"_startupDone" : False,
		"_tables" : [],
		#"langs" : defaultLangs,
		#"areaType"  : AREA
		}
	
	def __init__(self,**kw):
 		PropertySet.__init__(self,**kw)
		#Window.__init__(self)
		
	#def __init__(self,langs=defaultLangs,**kw):
 		#PropertySet.__init__(self,**kw)
		#self.__dict__['_startupDone'] = False
		#self.__dict__['_tables'] = []
		#self.__dict__['_supportedLangs'] = langs

## 	def __setattr__(self,name,value):
## 		if self.__dict__.has_key(name):
## 			self.__dict__[name] = value
## 			return
## 		self.addTable(value,name)

	def addTable(self,table):
					 #name=None,
					 #label=None,
					 #doc=None):
		assert isinstance(table,Table),\
				 repr(table)+" is not a Table"
		assert not self._startupDone,\
				 "Too late to declare new tables in " + repr(self)
		#if name is not None:
		#	table.setTableName(name)

		table.setTableId(self,len(self._tables))
		self._tables.append(table)
		
	def defineTables(self,ui):
		raise NotImplementedError

	def startup(self,ui=None):
		
		""" startup will be called exactly
		once, after having declared all tables of the database.  """
	
		assert not self._startupDone, "double startup"

		if ui is None:
			from ui import UI
			ui = UI()

		ui.progress("Schema startup...")

		ui.progress("  Initializing database...")
		self.defineSystemTables(ui)
		self.defineTables(ui)

		ui.progress("  Initializing %d tables..." % len(self._tables))

		# loop 1
		for table in self._tables:
			table.init1()
		
		# loop 2
		todo = list(self._tables)
		while len(todo):
			tryagain = []
			somesuccess = False
			for table in todo:
				# print "setupTable", table.getName()
				try:
					table.init2()
					somesuccess = True
				except StartupDelay, e:
					print "StartupDelay:", e # self, self._primaryAtoms
					tryagain.append(table)
			if not somesuccess:
				raise "startup failed"
			todo = tryagain

		# loop 2bis
		#for table in self._tables:
		#	table.defineQuery(None)

		# loop 3 
		for table in self._tables:
			table.init3()

		# loop 4
		for table in self._tables:
			table.init4()


		# self.defineMenus(self,ui)
		
		#if verbose:
		#	print "setupTables() done"
			
		self._startupDone = True
		ui.progress("Schema startup okay")
	
	
	def findImplementingTables(self,toClass):
		l = []
		for t in self._tables:
			if isinstance(t,toClass):
				l.append(t)
				#break
		return l
		
	def defineSystemTables(self,ui):
		pass

## 	def getSupportedLangs(self):
## 		return self.langs

	def getTableList(self,flt=None):
		assert self._startupDone, \
				 "getTableList() before startup()"
		l = []
		for t in self._tables:
			if flt is None or flt(t):
				l.append(t)
		return l
	
	
	def __repr__(self):
		return str(self.__class__)
	
	def __str__(self):
		return str(self.__class__)
	



## class DatabaseSchema(Window,PropertySet):

## 	defaults = {
## 		"startupDone" : False,
## 		"_tables" : [],
## 		"langs" : ("en",),
## 		#"areaType"  : AREA
## 		}

## 	HK_CHAR = '&'

## 	def __init__(self,**kw):
## 		#Window.__init__(self,None,)
## 		PropertySet.__init__(self,**kw)
## ## 		self.startupDone = False
## ## 		self._tables = []
## ## 		self.langs = ("en",)
## ## 		self.areaType = AREA
## 		#self.label=label
## 		#self.options = kw
## ##			self.__dict__['_renderer'] = None
## 		# self.__dict__['_mainWindow'] = None

## ##		def __setattr__(self,name,table):
## ##			#if self.conn is None:
## ##			#	 raise "must connect before declaring tables"
## ##			assert isinstance(table,Table)
## ##			if self.startupDone:
## ##				raise "too late to declare new tables"
## ##			self.tables[name] = table
## ##			table.declare(self,name)
## ##			# globals()[name] = table

## ## 	def __str__(self):
## ## 		return self.label

## 		#self.babelNone = tuple([None] * len(self.langs))
	
## 	def __repr__(self):
## 		return str(self.__class__)
	
## 	def __str__(self):
## 		return str(self.__class__)
	
## 	def defineSystemTables(self,ui):
## 		self.addTable("LANG",
## 						  Language,
## 						  label="Languages")
		
	
## 	def defineTables(self,ui):
## 		raise NotImplementedError
	
## 	def defineMenus(self,ui):
## 		raise NotImplementedError
	
## 	def addTable(self,name,rowClass,label=None):
## 		# assert isinstance(table,Table)
## 		if self.startupDone:
## 			raise "too late to declare new tables"
## 		# table =
## 		self._tables.append(
## 			Table(self, len(self._tables), name,rowClass,label))
		
## 	def addLinkTable(self,
## 						  name,parentClass,childClass,
## 						  rowClass=None):
## 		if self.startupDone:
## 			raise "too late to declare new tables"
## 		self._tables.append(
## 			LinkTable(self,len(self._tables), name,
## 						 parentClass,childClass, rowClass))

## 	def startup(self,ui=None):
		
## 		""" startup will be called exactly
## 		once, after having declared all tables of the database.  """
	
## 		assert not self.startupDone, "double startup"

## 		if ui is None:
## 			from ui import UI
## 			ui = UI()
		
## 		ui.progress("Adamo startup...")

## 		ui.progress("  Initializing database...")
## 		self.defineSystemTables(ui)
## 		self.defineTables(ui)

## 		ui.progress("  Initializing %d tables..." % len(self._tables))

## 		# loop 1
## 		for table in self._tables:
## 			table.init1(self)
		
## 		# loop 2
## 		todo = list(self._tables)
## 		while len(todo):
## 			tryagain = []
## 			somesuccess = False
## 			for table in todo:
## 				# print "setupTable", table.getName()
## 				try:
## 					table.init2(self)
## 					somesuccess = True
## 				except StartupDelay, e:
## 					tryagain.append(table)
## 			if not somesuccess:
## 				raise "startup failed"
## 			todo = tryagain

## 		# loop 2bis
## 		for table in self._tables:
## 			table.defineQuery(None)

## 		# loop 3 
## 		for table in self._tables:
## 			table.init3(self)


## 		# self.defineMenus(self,ui)
		
## 		#if verbose:
## 		#	print "setupTables() done"
			
## 		ui.progress("Adamo startup okay")

	
## 		self.__dict__['startupDone'] = True
	

## ## 	def addReport(self,name,rpt):
## ## 		self.reports[name] = rpt
	
## ##		def setRenderer(self,r):
## ##			self._renderer = r

## ##		def getRenderer(self):
## ##			return self._renderer

## #	def setupTables(self):
		

## 	def getTableList(self):
## 		return self._tables

	
	
## 	def getTable(self,tableId):
## 		try:
## 			return self._tables[tableId]
## 		except KeyError:
## 			raise "%d : no such table in %s" % (tableId, str(self))


## 	def findImplementingTables(self,toClass):
## 		l = []
## 		for t in self._tables:
## 			for mixin in t._rowMixins:
## 				if issubclass(mixin,toClass):
## 					l.append(t)
## 					break
## 				#else:
## 				#	print t, "doesn't implement", toClass
## 		return l
		

			
def connect_sqlite():
	from lino.adamo.dbds.sqlite_dbd import Connection
	return Connection(filename="tmp.db",
							schema=schema,
							isTemporary=True)

def connect_odbc():
	raise ImportError
	"""
	
	odbc does not work. to continue getting it work, uncomment the
	above line and run tests/adamo/4.py to reproduce the following
	error:
	
	DatabaseError: CREATE TABLE PARTNERS (
         id BIGINT,
         lang_id CHAR(3),
         org_id BIGINT,
         person_id BIGINT,
         name VARCHAR(50),
         PRIMARY KEY (id)
)
('37000', -3553, '[Microsoft][ODBC dBASE Driver] Syntaxfehler in Felddefinition.
', 4612)

	"""
	from lino.adamo.dbds.odbc_dbd import Connection
	return Connection(dsn="DBFS")

def connect_mysql():
	raise ImportError
	from lino.adamo.dbds.mysql_dbd import Connection
	return Connection("linodemo")
	

	



## def quickdb(self,schema, verbose=False,
## 				langs=None,
## 				label=None,
## 				filename="tmp.db",
## 				isTemporary=True):
	
## 	from lino.adamo.ui import UI
## 	ui = UI(verbose=verbose)

## 	# start it up
## 	schema.startup(ui)

## 	# Decide which driver to use 
## 	from lino.adamo.dbds.sqlite_dbd import Connection
## 	conn = Connection( filename="tmp.db",
## 							 schema=schema,
## 							 isTemporary=isTemporary)

## 	db = Database(ui, conn, schema,
## 					  langs=langs,
## 					  label=label)

## ## 	for f in (connect_odbc, connect_sqlite, connect_mysql):
## ## 		try:
## ## 			conn = f()
## ## 			break
## ## 		except ImportError:
## ## 			pass

## ## 	db = ui.addDatabase('demo',conn,schema,label="Lino Demo Database")

## 	ui.addDatabase(db) #'tmp', conn,schema, label=label)
## 	return db

