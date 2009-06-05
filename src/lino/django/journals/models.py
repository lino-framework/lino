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

This defines two abstract models Journal and Document.

A journal is a sequence of numbered documents in accounting applications.
A Journal instance knows the model used for documents in this journal.
A Document instance can look at its journal to find out which subclass 
of Document it is.

"""

from django.db import models

class DocumentError(Exception):
  pass
  
DOCTYPE_CLASSES = []
DOCTYPE_CHOICES = []

def register_doctype(cl):
    i = len(DOCTYPE_CHOICES)
    DOCTYPE_CHOICES.append((i,cl.__name__))
    DOCTYPE_CLASSES.append(cl)

def get_doctype(cl):
    i = 0
    for c in DOCTYPE_CLASSES:
        if c == cl:
            return i
        i += 1
    
def create_journal(id,cl,**kw):
    jnl = Journal(id=id,doctype=get_doctype(cl),**kw)
    jnl.save()
    return jnl


class Journal(models.Model):

    id = models.CharField(max_length=4,primary_key=True)
    name = models.CharField(max_length=100)
    doctype = models.IntegerField(choices=DOCTYPE_CHOICES)
    #lastnum = models.IntegerField(blank=True,null=True,default=0)
    force_sequence = models.BooleanField(default=False)
    
    def create_document(self,**kw):
        cl = DOCTYPE_CLASSES[self.doctype]
        doc = cl(journal=self,**kw)
        doc.save()
        return doc
        
    def get_next_number(self):
        d = self.document_set.aggregate(models.Max('number'))
        number = d['number__max']
        if number is None:
            return 1
        return number + 1
        
    def pre_delete_document(self,doc):
        if doc.number + 1 != self.get_next_number():
            if self.force_sequence:
                raise DocumentError(
                  "%s is not the last document in journal" % unicode(doc)
                  )
    
class AbstractDocument(models.Model):
    
    class Meta:
        abstract = True
        
    journal = models.ForeignKey(Journal)
    number = models.IntegerField()
    
    def __unicode__(self):
        #~ if self.id is None:
            #~ return "(Unsaved %s document)" % self.journal.id
            #~ return "%s#%d (%d)" % (self.journal.id,self.number, self.id)
        return "%s#%d (%d)" % (self.journal.id,self.number,self.id)
        
    def save(self,*args,**kw):
        assert self.journal is not None
        if self.number is None:
            self.number = self.journal.get_next_number()
        return super(AbstractDocument,self).save(*args,**kw)
        
    def delete(self):
        self.journal.pre_delete_document(self)
        #print "Deleting", self
        return super(AbstractDocument,self).delete()



##
## report definitions
##        
        
#~ from lino.django.utils import reports
#~ from lino.django.utils.layouts import PageLayout 

#~ class Journals(reports.Report):
    #~ model = Journal
    #~ order_by = "id"
    #~ columnNames = "id name doctype lastnum force_sequence"
    

#~ def lino_setup(lino):
    #~ m = lino.add_menu("config","~Configuration")
    #~ m.add_action(Journals())

