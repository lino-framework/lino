from lino.adamo import *
#from lino.adamo.table import Table
#from lino.adamo.datatypes import *
from addrbook import Partners

class Journals(Table):
	def init(self):
		self.addField('id',STRING.child(width=3))
		self.addField('name',STRING)
		self.addField('tableName', STRING)
		
	class Instance(Table.Instance):
		def getLabel(self):
			return self.name
		



class Years(Table):
	def init(self):
		self.addField('id',INT)
		self.addField('name',STRING)



class Documents(Table):
	def init(self):
		self.addField('seq',INT)
		self.addField('date',DATE)
		self.addField('closed',BOOL)

		self.addPointer('jnl',Journals)
		self.setPrimaryKey("jnl seq")

	class Instance(Table.Instance):
		def getLabel(self):
			return self.jnl.id+"-"+str(self.seq)
		
##		def getNextId(self,jnl):
##			return self.getLastId(jnl.id) + 1
		
class FinancialDocuments(Documents):
	def init(self):
		Documents.init(self)
		self.addField('remark',STRING)
		
class BankStatements(FinancialDocuments):
	def init(self):
		FinancialDocuments.init(self)
		self.addField('balance1',AMOUNT)
		self.addField('balance2',AMOUNT)
		
class PartnerDocuments(Documents):
	def init(self):
		Documents.init(self)
		self.addField('remark',STRING)
		self.addPointer('partner',Partners)

		

