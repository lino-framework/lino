from lino.adamo import *
#from lino.adamo.table import Table
#from lino.adamo.datatypes import *
from addrbook import Partners

class Journals(Table):
	def init(self):
		self.id = Field(STRING,width=3)
		self.name = Field(STRING)
		self.tableName = Field( STRING)
		
	class Instance(Table.Instance):
		def getLabel(self):
			return self.name
		



class Years(Table):
	def init(self):
		self.id = Field(INT)
		self.name = Field(STRING)



class Documents(Table):
	def init(self):
		self.seq = Field(INT)
		self.date = Field(DATE)
		self.closed = Field(BOOL)

		self.jnl = Pointer(Journals)
		self.setPrimaryKey("jnl seq")

	class Instance(Table.Instance):
		def getLabel(self):
			return self.jnl.id+"-"+str(self.seq)
		
##		def getNextId(self,jnl):
##			return self.getLastId(jnl.id) + 1
		
class FinancialDocuments(Documents):
	def init(self):
		Documents.init(self)
		self.remark = Field(STRING)
		
class BankStatements(FinancialDocuments):
	def init(self):
		FinancialDocuments.init(self)
		self.balance1 = Field(AMOUNT)
		self.balance2 = Field(AMOUNT)
		
class PartnerDocuments(Documents):
	def init(self):
		Documents.init(self)
		self.remark = Field(STRING)
		self.partner = Pointer(Partners)

		

