class Connection:

	def onTableSetup(self,table):
		pass
	
	def create_table(self,table):
		pass
	
	def commit(self):
		pass
	
	def close(self):
		pass

	
	def executeCreateTable(self,table):
		pass
	
	def executeSelect(self,query,
							limit=None,
							offset=None):
		raise NotImplementedError
		
	def executeCount(self,query):
		raise NotImplementedError
	
	def executeGetLastId(self,table,knownId=()):
		raise NotImplementedError
		
	def executeInsert(self,table,row):
		raise NotImplementedError
	
	def executeUpdate(self,table,row):
		raise NotImplementedError
	
	def executePeek(self,table,id):
		raise NotImplementedError
	

## 	def getConnection(self):
## 		return self.conn

## 	def newCursor(self,query):
## 		return self.conn.newCursor(query)

##		def ui_shutdown(self,ui):
##			return ui.confirm("Shutdown",
##									"Are you sure?",
##									self.shutdown,
##									None)


## 	def commit_row(self,cursor,row):
## 		if row.IsDirty():
## 			if row.IsNew():
## 				self.executeInsert(cursor,row)
## 				row.SetNew(False)
## 			else:
## 				self.executeUpdate(cursor,row)
## 			row.SetDirty(False)
## 		#else:
## 		#	 raise "No changes need to be commited"
## 		# self.commit_row(self.row)


		
