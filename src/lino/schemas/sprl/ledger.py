from lino.adamo import *

#from lino.adamo.table import Table
#from lino.adamo.datatypes import *
from addrbook import Partners
from sales import Invoices

class Bookings(Table):
   def init(self):
      self.seq = Field(INT)
      self.date = Field(DATE)
      self.amount = Field(AMOUNT)
      self.dc = Field(BOOL)

      self.invoice = Pointer(Invoices)
      self.partner = Pointer(Partners)
      self.setPrimaryKey("invoice seq")
   
