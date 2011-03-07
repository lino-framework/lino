====
igen
====



.. currentmodule:: igen

Defined in :srcref:`/lino/sites/igen/models.py`



Import model definitions:

  >>> Order = reports.resolve_model('sales.Order')
  >>> Invoice = reports.resolve_model('sales.Invoice')

You can delete any Order, leaving a hole in the sequence.

  >>> Document.objects.get(pk=1).delete()
        
Once there is a hole, this number will not be reused.

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

  >>> s = "
".join(unicode(doc) for doc in Document.objects.all())
  >>> print s
  INV#1 (2)
  ORD#2 (3)
  ORD#3 (4)
  ORD#4 (6)
  INV#2 (7)




