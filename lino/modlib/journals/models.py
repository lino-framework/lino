## Copyright 2009-2012 Luc Saffre
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

raise Exception("merged into lino.modlib.ledger")

import logging
logger = logging.getLogger(__name__)

import os
import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _

from lino import dd
from lino import mixins
from lino.utils.babel import babelattr, BabelCharField
#~ from lino.modlib.documents import models as documents
#~ from lino import mixins
from lino.utils import mti
from lino.utils.choicelists import ChoiceList


class DocumentError(Exception):
    pass
  



class Journaled(mti.MultiTableBase):
    """
    A Journaled is a numbered document in a Journal.
      
    """
    
    class Meta:
        abstract = True
        unique_together = ['journal','year','number']
        
    journal = JournalRef()
    #~ year = YearRef()
    year = Years.field()
    number = DocumentRef(blank=True)
    
    def __unicode__(self):
        #~ if self.id is None:
            #~ return "(Unsaved %s document (journal=%r,number=%r))" % (
              #~ self.__class__,self.journal,self.number)
            #~ return "%s#%d (%d)" % (self.journal.id,self.number, self.id)
        return "%s %s/%s (%d)" % (self.journal,self.year,self.number,self.id)
        #~ return babelattr(self.journal,'printed_name') % self.number
        
    #~ def before_save(self):
        #~ pass
        
    def save(self,*args,**kw):
        #~ print 'Journaled.save'
        #~ self.before_save()
        r = super(Journaled,self).save(*args,**kw)
        self.after_save()
        return r
        
    def after_save(self):
        #logger.info("Saved document %s",self)
        pass
        
        
class ModifiedMixin(dd.Model):
  
    class Meta:
        abstract = True
        
    last_modified = models.DateTimeField(auto_now=True)
  
    def get_last_modified_time(self):
        return self.last_modified 

class Sendable(dd.Model):
  
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

          



        

class Journals(dd.Table):
    model = Journal
    order_by = ["seqno"]
    column_names = "id name doctype force_sequence *"
    
    
class DocumentsByJournal(dd.Table):
    order_by =  ["number"]
    master_key = 'journal' # see django issue 10808
    
    def get_title(self,renderer):
        return "todo: journals.models.DocumentsByJournal.get_title()"
        return "%s (journal %s)" % (
          renderer.master_instance.name,
          renderer.master_instance.id)
    
    
class unused_DocumentsByJournal(dd.Table):
    order_by = ["number"]
    #master = Journal
    master_key = 'journal' # see django issue 10808
    
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
        dd.Table.__init__(self,**params)


#~ __all__ = ['Journal']