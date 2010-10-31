## Copyright 2009-2010 Luc Saffre
## This file is part of the Lino project.
## Lino is free software; you can redistribute it and/or modify 
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 3 of the License, or
## (at your option) any later version.
## Lino is distributed in the hope that it will be useful, 
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
## GNU General Public License for more details.
## You should have received a copy of the GNU General Public License
## along with Lino; if not, see <http://www.gnu.org/licenses/>.


"""
This module defines the models Journal and AbstractDocument.

A journal is a sequence of numbered documents.
A Journal instance knows the model used for documents in this journal.
An AbstractDocument instance can look at its journal to find out which subclass it is.

See lino.testapps.journals for more documentation.

"""

import os
#import logging ; logger = logging.getLogger('lino.apps.journals')

from django.db import models
import lino
from lino import reports
#~ from lino.modlib.documents import models as documents
from lino.utils import mixins
from lino.utils.printable import Printable


class DocumentError(Exception):
    pass
  

DOCTYPES = []
DOCTYPE_CHOICES = []

def register_doctype(docclass,rptclass=None):
    #assert not docclass in DOCTYPE_CLASSES
    #~ i = 0
    #~ for cl in DOCTYPE_CLASSES:
        #~ if cl == docclass:
            #~ return i
        #~ i += 1
    type_id = len(DOCTYPE_CHOICES)
    DOCTYPE_CHOICES.append((type_id,docclass.__name__))
    DOCTYPES.append((docclass,rptclass))
    docclass.doctype = type_id
    return type_id

def get_doctype(cl):
    i = 0
    for c,r in DOCTYPES:
        if c is cl:
            return i
        i += 1
    return None
    

class Journal(models.Model):
  
    id = models.CharField(max_length=4,primary_key=True)
    name = models.CharField(max_length=100)
    doctype = models.IntegerField() #choices=DOCTYPE_CHOICES)
    force_sequence = models.BooleanField(default=False)
    #account = models.ForeignKey(ledger.Account,blank=True,null=True)
    account = models.CharField(max_length=6,blank=True)
    pos = models.IntegerField()
    
    def get_doc_model(self):
        #print self,DOCTYPE_CLASSES, self.doctype
        return DOCTYPES[self.doctype][0]

    def get_doc_report(self):
        return DOCTYPES[self.doctype][1]()

    def unused_get_doc_report(self,**kw):
        kw['master_instance'] = self
        rptclass = DOCTYPES[self.doctype][1].spawn(self.id,master=self.__class__,params=kw)
        return rptclass()

    def create_document(self,**kw):
        cl = self.get_doc_model()
        kw.update(journal=self)
        try:
            doc = cl(**kw)
        except TypeError,e:
            #~ print 20100804, cl
            raise
        #~ doc.full_clean()
        #~ doc.save()
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
        
    #~ def __init__(self,docclass,id,name=None):
        #~ if JOURNALS.has_key(id):
            #~ raise RuntimeError("Duplicate definition of journal %s" % id)
        #~ assert id is not None
        #~ assert len(id) > 0
        #~ assert issubclass(docclass,AbstractDocument)
        #~ self.id = id
        #~ self.docclass = docclass
        #~ if name is None:
            #~ name = id
        #~ self.name = name
        #~ self.seq_num = len(JOURNALS)
        #~ JOURNALS[id] = self
        #print self.seq_num,":",self.id,self.__class__.__name__,self.docclass
        
    #~ def create_document(self,**kw):
        #~ doc = self.docclass(journal=self.id,**kw)
        #~ doc.save()
        #~ return doc
        
    #~ def get_next_number(self):
        #~ #cl = DOCTYPE_CLASSES[self.doctype]
        #~ d = self.docclass.objects.filter(journal=self.id).aggregate(
            #~ models.Max('number'))
        #~ number = d['number__max']
        #~ if number is None:
            #~ return 1
        #~ return number + 1
        
    def __unicode__(self):
        return self.id
        
    def save(self,*args,**kw):
        self.before_save()
        r = super(Journal,self).save(*args,**kw)
        self.after_save()
        return r
        
    def after_save(self):
        pass
        
    def before_save(self):
        if not self.name:
            self.name = self.id
        if not self.pos:
            self.pos = self.__class__.objects.all().count() + 1
      
        
    def pre_delete_document(self,doc):
        #print "pre_delete_document", doc.number, self.get_next_number()
        if self.force_sequence:
            if doc.number + 1 != self.get_next_number():
                raise DocumentError(
                  "%s is not the last document in journal" % unicode(doc)
                  )
                  
def JournalRef(**kw):
    kw.update(null=True) # Django Ticket #12708
    return models.ForeignKey(Journal,**kw)

def DocumentRef(**kw):
    return models.IntegerField(**kw)


class Journaled(mixins.MultiTableBase):
    """
    A model that subclasses Journaled must provide 2 fields::
    
      journal = journals.JournalRef()
      number = journals.DocumentRef()
      
    """
    
    class Meta:
        abstract = True
        
    journal = JournalRef()
    number = DocumentRef()
    
    @classmethod
    def create_journal(cls,id,**kw):
        doctype = get_doctype(cls)
        jnl = Journal(doctype=doctype,id=id,**kw)
        #jcl = self.journal._meta.rel.to.__class__
        #print jcl, " == ", cls.journal_class
        #jnl = cls.journal_class(cls,*args,**kw)
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
            #~ return "%s#%d (%d)" % (self.journal.id,self.number, self.id)
        return "%s#%s (%d)" % (self.journal,self.number,self.id)
        
    def full_clean(self,*args,**kw):
        if self.number is None:
            self.number = self.journal.get_next_number()
        super(Journaled,self).full_clean(*args,**kw)
        
    def before_save(self):
        pass
        #~ assert self.journal is not None
        #~ assert JOURNALS.has_key(self.journal)
        #jnl = self.get_journal()
        #~ print 'Journaled.before_save', self.number
        
    def save(self,*args,**kw):
        #~ print 'Journaled.save'
        self.before_save()
        r = super(Journaled,self).save(*args,**kw)
        self.after_save()
        return r
        
    def after_save(self):
        #lino.log.info("Saved document %s",self)
        pass
        
    def delete(self):
        #jnl = self.get_journal()
        self.journal.pre_delete_document(self)
        return super(AbstractDocument,self).delete()
        
    def get_child_model(self):
        ## overrides Typed
        return DOCTYPES[self.journal.doctype][0]
        
        
class ModifiedMixin(models.Model):
  
    class Meta:
        abstract = True
        
    last_modified = models.DateTimeField(auto_now=True)
  
    def get_last_modified_time(self):
        return self.last_modified 

class Sendable(models.Model):
  
    """
    A model that subclasses Sendable must provide 1 field::
    
      sent_time = models.DateTimeField(blank=True,null=True)
      
    """
    
    class Meta:
        abstract = True
        
    sent_time = models.DateTimeField(blank=True,null=True)
    
    def html_templates(self):
        # when using pisa
        model = self.get_child_model()
        return [
          '%s_pisa.html' % self.journal,
          '%s_pisa.html' % model.__name__.lower(),
          'document_pisa.html'
        ]

    def can_send(self):
        return True
      
    def must_send(self):
        if not self.can_send():
            return False
        return self.sent_time is None
        
        
    def send(self,simulate=True):
        self.make_pdf()
        if False:
            result = render.print_instance(self,as_pdf=True)
            #print result
            fn = "%s%d.pdf" % (self.journal.id,self.id)
            file(fn,"w").write(result)
        if not simulate:
            # todo : here we should really send it
            self.sent_time = datetime.datetime.now()
            self.save()
            
    
        
        
        
    def pdf_filename(self):
        return self.journal.id + "/" + str(self.number) + '.pdf'
        #return os.path.join(self.journal.id,str(self.number)) + '.pdf'

          



##
## report definitions
##        
        

class Journals(reports.Report):
    model = Journal
    order_by = "id"
    column_names = "id name doctype force_sequence"
    
    
class DocumentsByJournal(reports.Report):
    order_by = "number"
    fk_name = 'journal' # see django issue 10808
    
    def get_title(self,renderer):
        return "todo: journals.models.DocumentsByJournal.get_title()"
        return "%s (journal %s)" % (
          renderer.master_instance.name,
          renderer.master_instance.id)
    
    
class unused_DocumentsByJournal(reports.Report):
    order_by = "number"
    #master = Journal
    fk_name = 'journal' # see django issue 10808
    
    def __init__(self,journal,**kw):
        self.journal = journal
        rpt = journal.get_doc_report()
        #self.inlines = rpt.inlines
        params = dict(
          label=self.journal.name,
          name=self.journal.id,
          model=rpt.model,
          page_layouts=rpt.page_layouts,
          master_instance=journal,
          title=u"%s (journal %s)" % (journal.name,journal.id),
          column_names=rpt.column_names,
        )
        params.update(kw)
        reports.Report.__init__(self,**params)


#~ __all__ = ['Journal']