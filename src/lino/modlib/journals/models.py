## Copyright 2009 Luc Saffre
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

"""

import os
#import logging ; logger = logging.getLogger('lino.apps.journals')

from django.db import models
import lino
from lino import reports
from lino.apps.documents import models as documents
#documents = reports.get_app('documents')


class DocumentError(Exception):
    pass
  

DOCTYPES = []
DOCTYPE_CHOICES = []

def register_doctype(docclass,rptclass):
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
        if c == cl:
            return i
        i += 1
    return None
    

#JOURNALS = {}

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

    def get_doc_report(self,**kw):
        #kw['master_instance'] = self
        return DOCTYPES[self.doctype][1]()#(**kw)

    def create_document(self,**kw):
        cl = self.get_doc_model()
        doc = cl(journal=self,**kw)
        doc.save()
        return doc
        
    def get_next_number(self):
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
        
#~ def get_journal(id):
    #~ return JOURNALS[id]
    
#~ def get_journals_by_docclass(cls):
    #~ #from lino.utils.sites import lino_site # ensure setup
    #~ #print 'JOURNALS:', JOURNALS
    #~ return [jnl for jnl in JOURNALS.values() if jnl.docclass == cls]
      
#~ def get_journal_by_docclass(cls,num=0):
    #~ l = get_journals_by_docclass(cls)
    #~ if len(l) > num:
        #~ return l[num]
    #~ raise RuntimeError("No journal %s in lino_settings.py" % cls.__name__)
      
    
def JournalRef(**kw):
    #return models.CharField(max_length=4,choices=JOURNALS,**kw)
    return models.ForeignKey(Journal,**kw)

def DocumentRef(**kw):
    return models.IntegerField(**kw)


class AbstractDocument(documents.AbstractDocument):
  
    journal = JournalRef()
    #idjnl = models.CharField(max_length=4,choices=JOURNALS)
    number = DocumentRef()
    
    #~ journal_class = Journal
    
    class Meta:
        abstract = True
        
        
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
            
        
    #~ def get_journal(self):
        #~ return JOURNALS[self.journal]
    
    #~ @classmethod
    #~ def get_journal_by_docclass(cls,*args,**kw):
        #~ return get_journal_by_docclass(cls,*args,**kw)
        
    def __unicode__(self):
        if self.id is None:
            return "(Unsaved %s document)" % self.__class__
            #~ return "%s#%d (%d)" % (self.journal.id,self.number, self.id)
        return "%s#%s (%d)" % (self.journal,self.number,self.id)
        
    def before_save(self):
        #~ assert self.journal is not None
        #~ assert JOURNALS.has_key(self.journal)
        #jnl = self.get_journal()
        if self.number is None:
            self.number = self.journal.get_next_number()
        
    def save(self,*args,**kw):
        self.before_save()
        r = super(AbstractDocument,self).save(*args,**kw)
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
        return DOCTYPES[self.journal.doctype][0]
        
    def pdf_filename(self):
        return self.journal.id + "/" + str(self.number) + '.pdf'
        #return os.path.join(self.journal.id,str(self.number)) + '.pdf'

    #~ def get_child_model(self):
        #~ jnl = self.get_journal()
        #~ return jnl.docclass
        #~ #return DOCTYPE_CLASSES[jnl.doctype]
        
    #~ def pdf_filename(self):
        #~ return os.path.join(self.pdf_root(),
          #~ self.journal,
          #~ str(self.number))+'.pdf'
          



##
## report definitions
##        
        

class Journals(reports.Report):
    model = Journal
    order_by = "id"
    columnNames = "id name doctype force_sequence"
    
    
class DocumentsByJournal(reports.Report):
    order_by = "number"
    master = Journal
    fk_name = 'journal' # see django issue 10808
    
    def get_title(self,renderer):
        return "todo: journals.models.DocumentsByJournal.get_title()"
        return "%s (journal %s)" % (
          renderer.master_instance.name,
          renderer.master_instance.id)
    
    
class unused_DocumentsByJournal(reports.Report):
    order_by = "number"
    master = Journal
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
          columnNames=rpt.columnNames,
        )
        params.update(kw)
        reports.Report.__init__(self,**params)


__all__ = ['Journal']