#coding: latin1
#----------------------------------------------------------------------
# $Id: schema.py,v 1.14 2004/07/31 07:13:46 lsaffre Exp $
# Copyright: (c) 2003-2004 Luc Saffre
# License:	 GPL
#----------------------------------------------------------------------

import types

#from widgets import Form
from forms import FormTemplate, TableForm
#from context import Context #, Session
from database import Database
from table import Table, LinkTable, SchemaComponent
from datatypes import StartupDelay
from datasource import Datasource
from lino.misc.descr import Describable
from lino.misc.attrdict import AttrDict
from center import center



class SchemaPlugin(SchemaComponent,Describable):
	def __init__(self,isActive=True,*args,**kw):
		SchemaComponent.__init__(self)
		Describable.__init__(self,*args,**kw)
		self._isActive = isActive

	def isActive(self):
		return self._isActive
		
	def defineTables(self,schema):
		pass
	def defineMenus(self,schema,context,win):
		pass


class Schema:

	HK_CHAR = '&'
	defaultLangs = ('en',)
	#sessionFactory = Session
	
	def __init__(self,**kw):
		self._startupDone= False
		#self.forms= {
		self._datasourceRenderer= None
		self._contextRenderer= None
		
		self._plugins= []
		self._tables= []
		
		self.plugins = AttrDict()
		self.tables = AttrDict()
		self.forms = AttrDict()

		""" Note: for plugins and tables it is important to keep also a
		sequential list.  """
	
		
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
		assert isinstance(table,Table),\
				 repr(table)+" is not a Table"
		assert not self._startupDone,\
				 "Too late to declare new tables in " + repr(self)
		table.registerInSchema(self,len(self._tables))
		self._tables.append(table)
		name = table.getTableName()
		self.tables.define(name,table)
		
	def addPlugin(self,plugin):
		assert isinstance(plugin,SchemaPlugin),\
				 repr(plugin)+" is not a SchemaPlugin"
		assert not self._startupDone,\
				 "Too late to declare new plugins in " + repr(self)
		plugin.registerInSchema(self,len(self._plugins))
		self._plugins.append(plugin)
		name = plugin.getName()
		self.plugins.define(name,plugin)
		
	def addForm(self,form):
		assert isinstance(form,FormTemplate), \
				 repr(form)+" is not a FormTemplate"
		assert not self._startupDone,\
				 "Too late to declare new forms in " + repr(self)
		form.registerInSchema(self,len(self.forms))
		name = form.getFormName()
		self.forms.define(name,form)
		#assert not self._forms.has_key(name)
		#self._forms[name] = form
		

	def startup(self):
		
		""" startup will be called exactly
		once, after having declared all tables of the database.  """
	
		#self._app = app
		assert not self._startupDone, "double startup"
		#progress = self._app.console.progress
		info = center().console.info
		info("Initializing database schema...")
		#self.defineSystemTables(ui)
		for plugin in self._plugins:
			plugin.defineTables(self)

		info("  Initializing %d tables..." % len(self._tables))

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

			
		for table in self._tables:
			self.addForm(TableForm(table))

			
		# initialize forms...

		info("  Initializing %d forms..." % len(self.forms))

		for form in self.forms.values():
			form.init1()
			
		# self.defineMenus(self,ui)
		
		#if verbose:
		#	print "setupTables() done"
			
		self._startupDone = True
		info("Schema startup okay")
		

	def setLayout(self,layoutModule):
		# initialize layouts...
		assert self._startupDone 
		
		lf = LayoutFactory(layoutModule)
		for table in self._tables:
			wcl = lf.get_wcl(table.Instance)
			assert wcl is not None
			table._rowRenderer = wcl


		self._datasourceRenderer = lf.get_wcl(Datasource)
		self._contextRenderer = lf.get_wcl(Database)

		assert self._datasourceRenderer is not None
		assert self._contextRenderer is not None
		

	
	
	def findImplementingTables(self,toClass):
		l = []
		for t in self._tables:
			if isinstance(t,toClass):
				l.append(t)
				#break
		return l
		

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
	

## 	def onStartUI(self,sess):
## 		# overridden by sprl.Schema
## 		return True

	def onLogin(self,sess):
		return True

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
		
## 		ui.info("Adamo startup...")

## 		ui.info("  Initializing database...")
## 		self.defineSystemTables(ui)
## 		self.defineTables(ui)

## 		ui.info("  Initializing %d tables..." % len(self._tables))

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
			
## 		ui.info("Adamo startup okay")

	
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



class LayoutComponent:
	pass

class LayoutFactory:
	"extracts Layouts from "
	def __init__(self,mod):
		#self._schema = schema
		self._layouts = {}
		for k,v in mod.__dict__.items():
			if type(v) is types.ClassType:
				if issubclass(v,LayoutComponent):
					try:
						hcl = v.handledClass
					except AttributeError:
						pass
					else:
						assert not self._layouts.has_key(hcl),\
								 repr(v) + ": duplicate class handler for " + repr(hcl)
						self._layouts[hcl] = v
						#print k,v.handledClass,v

		for k,v in self._layouts.items():
			print str(k), ":", str(v)
		print len(self._layouts), "class layouts"
		
		# setupSchema()
## 		for table in schema._tables:
## 			if not table._rowAttrs.has_key("writeParagraph"):
## 				wcl = self.get_wcl(table.Row)
## 				assert wcl is not None
## 				from lino.adamo import Vurt, MEMO
## 				table._rowAttrs["writeParagraph"] = Vurt(
## 					wcl.writeParagraph,MEMO)

	def get_bases_widget(self,cl):
		#print "get_bases_widget(%s)" % repr(cl)
		try:
			return self._layouts[cl]
		except KeyError:
			pass #print "no widget for " + repr(cl)

		for base in cl.__bases__:
			try:
				return self._layouts[base]
			except KeyError:
				#print "no widget for " + repr(cl)
				pass
		raise KeyError


	def get_wcl(self,cl):
		#print "get_wcl(%s)" % repr(cl)
		try:
			return self.get_bases_widget(cl)
		except KeyError:
			pass

		for base in cl.__bases__:
			try:
				return self.get_bases_widget(base)
			except KeyError:
				pass
		return None
	
	def get_widget(self,o,*args,**kw):
		#print "get_widget(%s)" % repr(o)
		wcl = self.get_wcl(o.__class__)
		if wcl is None:
			msg = "really no widget for "+repr(o)
			#+" (bases = " + str([repr(b) for b in cl.__bases__])
			raise msg
		#print "--> found widget " + repr(wcl)
		return wcl(o,*args,**kw)

## def get_rowwidget(row):		
## 	cl = get_widget(row._ds._table.__class__)
## 	return cl(row)
		

