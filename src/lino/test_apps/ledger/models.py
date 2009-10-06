"""

>>> ledger.Account(pk="4000").save()
>>> ledger.Account(pk="7000").save()
>>> ledger.Account(pk="4510").save()

>>> ORD = Order.create_journal("ORD")
>>> INV = Invoice.create_journal("INV",
...       account=ledger.get_account('customers'))
        
>>> ORD.create_document()
<Order: ORD#1 (1)>
>>> INV.create_document()
<Invoice: INV#1 (2)>

"""

"""
>>> ORD.create_document()
<Order: ORD#2 (3)>
>>> ORD.create_document()
<Order: ORD#3 (4)>
>>> INV.create_document()
<Invoice: INV#2 (5)>
>>> s = "\n".join(unicode(doc) for doc in Document.objects.all())
>>> print s
ORD#1 (1)
INV#1 (2)
ORD#2 (3)
ORD#3 (4)
INV#2 (5)

You can delete any Order, leaving a hole in the sequence, 
and this number will not be reused.

>>> Document.objects.get(pk=1).delete()
        
>>> doc = ORD.create_document() # Order(journal=ORD)
>>> doc
ORD#4 (6)
        
For invoices it is not allowed to delete documents in the
middle because this would leave a hole in the sequence:

>>> Document.objects.get(pk=2).get_child_instance().delete()


It's okay to delete the last invoice of a journal. 

>>> doc = Document.objects.get(pk=5)
>>> print doc
INV#2 (5)
  
>>> doc.delete()
        
>>> doc = INV.create_document() # Invoice(journal=INV)
>>> print doc
INV#2 (7)

Here is again the list of documents in the database after these
operations::

>>> s = "\n".join(unicode(doc) for doc in Document.objects.all())
>>> print s
INV#1 (2)
ORD#2 (3)
ORD#3 (4)
ORD#4 (6)
INV#2 (7)

20090704 : new method get_child_instance()

>>> s = ''
>>> for gen_doc in Document.objects.all():
>>>     spec_doc = gen_doc.get_child_instance()
>>>     s += "%s : %s\n" % (spec_doc,spec_doc.__class__.__name__)
>>> print s
INV#1 (2) : Invoice
ORD#2 (3) : Order
ORD#3 (4) : Order
ORD#4 (6) : Order
INV#2 (7) : Invoice

"""

from django.db import models
from lino.apps.journals import models as journals
from lino.apps.ledger import models as ledger

class Customer(models.Model):
    pass
    
class Document(journals.AbstractDocument):
    customer = models.ForeignKey(Customer,blank=True,null=True)
    
class Order(Document):
    pass

class Invoice(Document,ledger.LedgerDocument):
    pass



