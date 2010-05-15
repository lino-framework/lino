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
This defines AbstractDocument which knows how to "print" a document.


"""


import os
import sys
import datetime


from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

import lino
lino.log.debug(__file__+' : started')
from lino import reports

from lino.modlib.documents.utils import Printable

class DocumentError(Exception):
    pass

  
class AbstractDocument(models.Model,Printable):
    
    class Meta:
        abstract = True
        
    last_modified = models.DateTimeField(auto_now=True)
    sent_time = models.DateTimeField(blank=True,null=True)
    
    def get_child_model(self):
        raise NotImplementedError
        #return self.__class__
        # implementation example SalesDocument in lino.apps.journals
        
    def get_child_instance(self):
        model = self.get_child_model()
        if model is self.__class__:
            return self
        related_name = model.__name__.lower()
        return getattr(self,related_name)
        
    def get_last_modified_time(self):
        return self.last_modified 

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
            
    
lino.log.debug(__file__+' : done')
