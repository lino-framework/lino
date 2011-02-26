"""

A Strange Problem
=================

This testcase may also be useful as an overview on how Lino handles Documents and Journals.

The following works only if you have issue 10808 solved:

  >>> ORD = Order.create_journal("ORD",name="Orders")
  >>> print ORD.create_document()
  ORD#1 (1)
  >>> INV = Invoice.create_journal("INV",name="Invoices")
  >>> print INV.create_document()
  INV#1 (1)
  

"""

from django.db import models

class AbstractDocument(models.Model):
    
    class Meta:
        abstract = True
        
    last_modified = models.DateTimeField(auto_now=True)


DOCTYPES = []
DOCTYPE_CHOICES = []

def register_doctype(docclass):
    type_id = len(DOCTYPE_CHOICES)
    DOCTYPE_CHOICES.append((type_id,docclass.__name__))
    DOCTYPES.append(docclass)
    docclass.doctype = type_id
    return type_id

def get_doctype(cl):
    i = 0
    for c in DOCTYPES:
        if c is cl:
            return i
        i += 1
    return None


    
class Journal(models.Model):
  
    id = models.CharField(max_length=4,primary_key=True)
    name = models.CharField(max_length=100)
    doctype = models.IntegerField() #choices=DOCTYPE_CHOICES)
    
    def __unicode__(self):
        return self.id
        
    def get_doc_model(self):
        return DOCTYPES[self.doctype]

    def create_document(self,**kw):
        cl = self.get_doc_model()
        kw.update(journal=self)
        doc = cl(**kw)
        doc.full_clean()
        doc.save()
        return doc
        
    def get_next_number(self):
        self.save()
        cl = self.get_doc_model()
        d = cl.objects.filter(journal=self).aggregate(
            models.Max('number'))
        number = d['number__max']
        if number is None:
            return 1
        return number + 1
        
    
def JournalRef(**kw):
    return models.ForeignKey(Journal,**kw)

def DocumentRef(**kw):
    return models.IntegerField(**kw)

    
    
class JournaledAbstractDocument(AbstractDocument):
  
    journal = JournalRef()
    number = DocumentRef()
    
    
    class Meta:
        abstract = True
        
    @classmethod
    def create_journal(cls,id,**kw):
        doctype = get_doctype(cls)
        jnl = Journal(doctype=doctype,id=id,**kw)
        jnl.save()
        return jnl
        
    @classmethod
    def get_journals(cls):
        doctype = get_doctype(cls)
        return Journal.objects.filter(doctype=doctype).order_by('pos')
            
    
    def __unicode__(self):
        if self.id is None:
            return "(Unsaved %s document (journal=%r,number=%r))" % (
              self.__class__,self.journal,self.number)
        return "%s#%s (%d)" % (self.journal,self.number,self.id)
        
    def full_clean(self,*args,**kw):
        if self.number is None:
            self.number = self.journal.get_next_number()
        super(JournaledAbstractDocument,self).full_clean(*args,**kw)
        
    #~ def save(self,*args,**kw):
        #~ self.before_save()
        #~ r = super(AbstractDocument,self).save(*args,**kw)
        #~ self.after_save()
        #~ return r
        
    #~ def after_save(self):
        #~ pass
    
    
class LedgerDocument(JournaledAbstractDocument):
    
    value_date = models.DateField(auto_now=True) 
    ledger_remark = models.CharField("Remark for ledger",
      max_length=200,blank=True)



class SalesDocument(JournaledAbstractDocument):
    
    creation_date = models.DateField(auto_now=True) 

    #~ def before_save(self):
        #~ JournaledAbstractDocument.before_save(self)
        # ...
        
class Order(SalesDocument):
    valid_until = models.DateField(auto_now=True) 

class Invoice(LedgerDocument,SalesDocument):
    due_date = models.DateField("Payable until",blank=True,null=True)
    
    #~ def before_save(self):
        # ...
        #~ super(Invoice,self).before_save()

#~ class Invoice(LedgerDocument):
    #~ due_date = models.DateField(auto_now=True) 
    
    #~ def before_save(self):
        #~ # ...
        #~ super(Invoice,self).before_save()


register_doctype(Order)
register_doctype(Invoice)
