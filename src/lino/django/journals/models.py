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
lino.django.journals
--------------------

This defines two models Journal and Document.

A journal is a sequence of numbered documents in accounting applications.
A Journal instance knows the model used for documents in this journal.
A Document instance can look at its journal to find out which subclass 
of Document it is.
The journal also manages a counter "lastnum" to control the numbering
of documents. 

"""

from django.db import models

class DocumentError(Exception):
  pass
  
DOCTYPE_CLASSES = []
DOCTYPE_CHOICES = []

def register_doctype(cl):
    n = len(DOCTYPE_CHOICES)
    DOCTYPE_CHOICES.append((n,cl.__name__))
    DOCTYPE_CLASSES.append(cl)

class Journal(models.Model):

    id = models.CharField(max_length=4,primary_key=True)
    name = models.CharField(max_length=100)
    doctype = models.IntegerField(choices=DOCTYPE_CHOICES)
    lastnum = models.IntegerField(blank=True,null=True,default=0)
    force_sequence = models.BooleanField(default=False)
    
    def create_document(self,**kw):
        cl = DOCTYPE_CLASSES[self.doctype]
        if not kw.has_key('number'):
            kw['number'] = self.lastnum + 1
        doc = cl(journal=self,**kw)
        self.lastnum = kw['number'] 
        self.save()
        return doc
        
    def on_delete_document(self,doc):
        if doc.number == self.lastnum:
            #print "foo", self.lastnum
            self.lastnum -= 1
            #print "bar", self.lastnum
            self.save()
        elif self.force_sequence:
            raise DocumentError(
              "%s is not the last document in journal" % unicode(doc)
              )
    
class Document(models.Model):
    
    journal = models.ForeignKey(Journal)
    number = models.IntegerField()
    
    class Meta:
        abstract = True
        
    def __unicode__(self):
        #~ if self.id is None:
            #~ return "(Unsaved %s document)" % self.journal.id
            #~ return "%s#%d (%d)" % (self.journal.id,self.number, self.id)
        return "%s#%d (%d)" % (self.journal.id,self.number, self.id)
        
    def delete(self):
        self.journal.on_delete_document(self)
        #print "Deleting", self
        return super(Document,self).delete()





##
## report definitions
##        
        
from lino.django.utils import reports
from lino.django.utils.layouts import PageLayout 

class Journals(reports.Report):
    model = Journal
    order_by = "id"
    columnNames = "id name doctype lastnum force_sequence"
    

def lino_setup(lino):
    m = lino.add_menu("config","~Configuration")
    m.add_action(Journals())

