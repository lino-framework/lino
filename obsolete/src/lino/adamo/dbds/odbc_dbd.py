import mx.ODBC.Windows as odbc

from lino.adamo.sql import SqlConnection

class Connection(SqlConnection):
	def __init__(self,dsn,isTemporary=False):
		#self.dbapi = sqlite
		self._dbconn = odbc.connect(dsn)
		self._isTemporary = isTemporary
		self._dsn = dsn


		
		
		#print "SQLite database : " + os.path.abspath(filename)
		# self._dbcursor = self._dbconn.cursor()

	def sql_exec(self,sql):
		csr = self._dbconn.cursor()
		try:
			csr.execute(sql)
			return csr
		except odbc.DatabaseError,e:
			raise odbc.DatabaseError,sql + "\n" + str(e)

	def commit(self):
		self._dbconn.commit()

	def close(self):
		self._dbconn.close()
		if self._isTemporary:
			pass
			# os.remove(self._filename)


  

	def executeCreateTable(self,table):
		
		try:
			self.sql_exec("DROP TABLE %s" % table.getName())
		except odbc.DatabaseError:
			pass
		SqlConnection.executeCreateTable(self,table)


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
