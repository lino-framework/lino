#----------------------------------------------------------------------
# $Id: sqlite_dbd.py,v 1.13 2004/06/12 03:06:51 lsaffre Exp $
# Copyright: (c) 2003-2004 Luc Saffre
# License:	 GPL
#----------------------------------------------------------------------

import os
import warnings
warnings.filterwarnings("ignore",
								"DB-API extension",
								UserWarning,
								"sqlite")

import sqlite
from types import TupleType
from lino.misc.console import confirm

# from lino.adamo.cursor import CursorMixin
from lino.adamo.sql import SqlConnection
# from lino.row import IntelliRow
		

class Connection(SqlConnection):
	
	def __init__(self,filename,schema,isTemporary=False):
		self.schema = schema
		self.dbapi = sqlite
		self._isTemporary = isTemporary
		self._filename = filename
		self._dump = None
		if filename:
			if isTemporary and os.path.exists(filename):
				os.remove(filename)
## 				while True:
## 					try:
## 						os.remove(filename)
## 						break
## 					except OSError,e:
## 						if not confirm(str(e)+"; retry?"):
## 							raise
				#assert not os.path.exists(filename)
			try:
				self._dbconn = sqlite.connect(filename)
			except sqlite.DatabaseError,e:
				raise filename + ":" +str(e)


	def __str__(self):
		filename = self._filename
		if filename is None:
			filename = '(stdout)'
		return "%s (SQLite)" % filename
		
		
		#print "SQLite database : " + os.path.abspath(filename)
		# self._dbcursor = self._dbconn.cursor()

	def startDump(self):
		self._dump = ""

	def stopDump(self):
		s = self._dump 
		self._dump = None
		return s

	def isVirtual(self):
		return self._filename is None

	def sql_exec(self,sql):
		if self._dump is not None:
			self._dump += sql + ";\n"
		if self._filename is None:
			print sql+";"
			return
		csr = sqlite.Cursor(self._dbconn,TupleType)
		#print "sqlite_dbd.py:" + sql
		try:
##				if "PARTNERS" in sql:
##					print "sqlite_dbd.py:" + sql
			csr.execute(sql)
			return csr
		except sqlite.DatabaseError,e:
			raise sqlite.DatabaseError,sql + "\n" + str(e)

	def commit(self):
		#print "commit"
		self._dbconn.commit()

	def close(self):
		self._dbconn.close()
		#self._dbconn = None
		if self._isTemporary and self._filename is not None:
			os.remove(self._filename)


  

## 	def executeCreateTable(self,table):
		
## 		try:
## 			self.sql_exec("DROP TABLE %s" % table.getName())
## 		except sqlite.DatabaseError:
## 			pass
## 		SqlConnection.executeCreateTable(self,table)


	def checkDatabaseSchema(self,db):
		# not yet usable
		csr = self.sql_exec("""\
		SELECT * FROM sqlite_master
			WHERE type='table'
		UNION ALL
		SELECT * FROM sqlite_temp_master
		WHERE type='table' '
		ORDER BY name;
		""")
		print csr
