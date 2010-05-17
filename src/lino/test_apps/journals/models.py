"""
Trying whether test is being run:
  >>> print "foo"
  bar

Shortcut to create Journal instances:

  >>> ORD = Order.create_journal("ORD")
  >>> INV = Invoice.create_journal("INV")

If you have a Journal, then you can create documents:

  >>> ORD.create_document()
  <Order: ORD#1 (1)>
  >>> INV.create_document()
  <Invoice: INV#1 (2)>
  >>> ORD.create_document()
  <Order: ORD#2 (3)>
  >>> ORD.create_document()
  <Order: ORD#3 (4)>
  >>> INV.create_document()
  <Invoice: INV#2 (5)>
  
Note how the documents have an internal pk that doesn't depend on their Journal:

  >>> s = "\n".join(unicode(doc) for doc in Document.objects.all())
  >>> print s
  ORD#1 (1)
  INV#1 (2)
  ORD#2 (3)
  ORD#3 (4)
  INV#2 (5)


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

#~ from django.db import models
from lino.modlib.journals import models as journals

    
#~ class Document(models.Model):
class Document(journals.AbstractDocument):
    pass #customer = models.ForeignKey(Customer,blank=True,null=True)
    
class Order(Document):
    pass

class Invoice(Document):
    pass

journals.register_doctype(Order)
journals.register_doctype(Invoice)

