from lino.adamo import *

#from lino.adamo.table import Table
#from lino.adamo.datatypes import *

from business import PartnerDocuments

class Products(Table):
   def init(self):
      self.addField('id',ROWID)
      self.addField('name',STRING)
      self.addField('price',PRICE)

   
