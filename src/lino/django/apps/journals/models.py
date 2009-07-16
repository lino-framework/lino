## Copyright 2009 Luc Saffre.
## This file is part of the Lino project. 

## Lino is free software; you can redistribute it and/or modify it
## under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.

## Lino is distributed in the hope that it will be useful, but WITHOUT
## ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
## or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public
## License for more details.

## You should have received a copy of the GNU General Public License
## along with Lino; if not, write to the Free Software Foundation,
## Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA


"""
lino.django.apps.journals
-------------------------

This defines the models Journal and AbstractDocument.

A journal is a sequence of numbered documents in accounting applications.
A Journal instance knows the model used for documents in this journal.
A Document instance can look at its journal to find out which subclass 
of Document it is.

"""

#~ __app_label__ = "journals"

import os
from django.db import models
from lino.django.apps.documents import models as documents

class DocumentError(Exception):
    pass
  

#~ DOCTYPE_CLASSES = []
#~ DOCTYPE_CHOICES = []

#~ def register_doctype(docclass):
    #~ i = 0
    #~ for cl in DOCTYPE_CLASSES:
        #~ if cl == docclass:
            #~ return i
        #~ i += 1
    #~ type_id = len(DOCTYPE_CHOICES)
    #~ DOCTYPE_CHOICES.append((type_id,docclass.__name__))
    #~ DOCTYPE_CLASSES.append(docclass)
    #~ return type_id

#~ def get_doctype(cl):
    #~ i = 0
    #~ for c in DOCTYPE_CLASSES:
        #~ if c == cl:
            #~ return i
        #~ i += 1
    

JOURNALS = {}

class Journal:
    def __init__(self,docclass,id,name=None):
        if JOURNALS.has_key(id):
            raise ConfigurationError("Duplicate definition of journal %s" % id)
        assert id is not None
        assert len(id) > 0
        assert issubclass(docclass,AbstractDocument)
        self.id = id
        self.docclass = docclass
        if name is None:
            name = id
        self.name = name
        self.seq_num = len(JOURNALS)
        JOURNALS[id] = self
        #print self.seq_num,":",self.id,self.__class__.__name__,self.docclass
        
    def create_document(self,**kw):
        #cl = DOCTYPE_CLASSES[self.doctype]
        #print self.id
        #print self.docclass
        doc = self.docclass(journal=self.id,**kw)
        #print doc
        #print doc.journal
        doc.save()
        return doc
        
    def get_next_number(self):
        #cl = DOCTYPE_CLASSES[self.doctype]
        d = self.docclass.objects.filter(journal=self.id).aggregate(
            models.Max('number'))
        number = d['number__max']
        if number is None:
            return 1
        return number + 1
        
    def __unicode__(self):
        return self.id
        
    def pre_delete_document(self,doc):
        pass
        
def get_journal(id):
    return JOURNALS[id]
    
def get_journals_by_docclass(cls):
    #from lino.django.utils.sites import lino_site # ensure setup
    #print 'JOURNALS:', JOURNALS
    return [jnl for jnl in JOURNALS.values() if jnl.docclass == cls]
      
def get_journal_by_docclass(cls,num=0):
    l = get_journals_by_docclass(cls)
    if len(l) > num:
        return l[num]
    raise RuntimeError("No journal %s in lino_settings.py" % cls.__name__)
      
    
def JournalRef(**kw):
    return models.CharField(max_length=4,choices=JOURNALS,**kw)

def DocumentRef(**kw):
    return models.IntegerField(**kw)


class AbstractDocument(documents.AbstractDocument):
  
    journal = JournalRef()
    #idjnl = models.CharField(max_length=4,choices=JOURNALS)
    #journal = models.ForeignKey(Journal)
    number = DocumentRef()
    
    journal_class = Journal
    
    class Meta:
        abstract = True
        
    @classmethod
    def create_journal(cls,*args,**kw):
        #doctype = register_doctype(cls)
        #jcl = self.journal._meta.rel.to.__class__
        #print jcl, " == ", cls.journal_class
        jnl = cls.journal_class(cls,*args,**kw)
        #jnl.save()
        return jnl
        
    def get_journal(self):
        return JOURNALS[self.journal]
    
    def __unicode__(self):
        if self.id is None:
            return "(Unsaved %s document)" % self.journal
            #~ return "%s#%d (%d)" % (self.journal.id,self.number, self.id)
        return "%s#%d (%d)" % (self.journal,self.number,self.id)
        
    def before_save(self):
        #~ assert self.journal is not None
        #~ assert JOURNALS.has_key(self.journal)
        jnl = self.get_journal()
        if self.number is None:
            self.number = jnl.get_next_number()
        
    def save(self,*args,**kw):
        self.before_save()
        r = super(AbstractDocument,self).save(*args,**kw)
        self.after_save()
        return r
        
    def after_save(self):
        pass
        
    def delete(self):
        jnl = self.get_journal()
        jnl.pre_delete_document(self)
        return super(AbstractDocument,self).delete()
        
    def get_child_model(self):
        jnl = self.get_journal()
        return jnl.docclass
        #return DOCTYPE_CLASSES[jnl.doctype]
        
    def pdf_filename(self):
        return os.path.join(self.pdf_root(),
          self.journal,
          str(self.number))+'.pdf'
          
          
      



##
## report definitions
##        
        
from lino.django.utils import reports
#~ from lino.django.utils.layouts import PageLayout 

#~ class Journals(reports.Report):
    #~ model = Journal
    #~ order_by = "id"
    #~ columnNames = "id name doctype lastnum"
    
class DocumentsByJournal(reports.Report):
    "abstract Report"
    order_by = "number"
    def __init__(self,jnl,*args,**kw):
        self.jnl = jnl
        super(DocumentsByJournal,self).__init__(*args,**kw)
        
    def get_title(self,renderer):
        return "Documents in journal " + self.jnl.name
        
    def get_queryset(self,master_instance,flt=None):
        qs = super(DocumentsByJournal,self).get_queryset(
                     master_instance,flt)
        return qs.filter(journal__exact=self.jnl.id)
        

def lino_setup(lino):
    pass
    #~ m = lino.add_menu("config","~Configuration")
    #~ m.add_action(Journals())

