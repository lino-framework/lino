from lino.adamo import *

#from lino.adamo.table import Table
#from lino.adamo.datatypes import *

from business import PartnerDocuments
from addrbook import Partners
from products import Products

class Invoices(PartnerDocuments):
	
	def init(self):
		PartnerDocuments.init(self)
		self.zziel = Field(DATE)
		self.amount = Field(AMOUNT)
		self.inverted = Field(BOOL)
		#self.addRowMethod("close")
		self.partner = Pointer(Partners)
		self.partner.setDetail('invoices')

	class Row(PartnerDocuments.Row):
		
		def close(self):
			#print "Invoices.close() : %s lines" % len(self.lines)
			self.lock()
			total = 0
			for line in self.lines:
				total += (line.unitPrice * line.qty)
			self.amount = total
			self.unlock()
		

class InvoiceLines(Table):
	def init(self):
		self.line = Field(INT)
		self.unitPrice = Field(AMOUNT)
		self.qty = Field(INT)
		self.remark = Field(STRING)
		
		self.invoice = Pointer(Invoices)
		self.invoice.setDetail('lines')
		self.product = Pointer(Products)
		self.product.setDetail('invoiceLines')
		
		self.setPrimaryKey("invoice line")

	class Row(Table.Row):
		def after_product(self):
			self.unitPrice = self.product.price

