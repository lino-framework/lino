from lino.adamo import *

#from lino.adamo.table import Table
#from lino.adamo.datatypes import *

from business import PartnerDocuments

class Products(Table):
   def init(self):
      self.id = Field(ROWID)
      self.name = Field(STRING)
      self.price = Field(PRICE)

   
