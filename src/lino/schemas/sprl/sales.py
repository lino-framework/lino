from lino.adamo import *

#from lino.adamo.table import Table
#from lino.adamo.datatypes import *

from business import PartnerDocuments
from addrbook import Partners
from products import Products

class Invoices(PartnerDocuments):
	
	def init(self):
		PartnerDocuments.init(self)
		self.addField('zziel',DATE)
		self.addField('amount',AMOUNT)
		self.addField('inverted',BOOL)
		#self.addRowMethod("close")
		self.addPointer('partner',Partners).setDetail('invoices')

	class Instance(PartnerDocuments.Instance):
		
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
		self.addField('line',INT)
		self.addField('unitPrice',AMOUNT)
		self.addField('qty',INT)
		self.addField('remark',STRING)
		
		self.addPointer('invoice',Invoices).setDetail('lines')
		self.addPointer('product',Products).setDetail('invoiceLines')
		
		self.setPrimaryKey("invoice line")

	class Instance(Table.Instance):
		def after_product(self):
			self.unitPrice = self.product.price

