# -*- coding: utf-8 -*-
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

from django.test import TestCase
from lino.django.utils.validatingmodel import TomModel, ModelValidationError
from lino.django.utils.reports import Report
from lino.django.utils.render import ViewReportRenderer
from django.db import models
from django.forms.models import modelform_factory, formset_factory
from django.conf import settings

from lino.django.journals import models as journals
# Journal, Document, register_doctype, DocumentError

class Document(journals.AbstractDocument):
    pass
    
class Order(Document):
    pass
journals.register_doctype(Order)

class Invoice(Document):
    pass
journals.register_doctype(Invoice)


class JournalsTest(TestCase):
  
    def test01(self):
      
        # create two journals and some documents::

        ORD = journals.create_journal("ORD",Order)
        INV = journals.create_journal("INV",Invoice,force_sequence=True)
        #~ INV = journals.Journal(id="INV",name="Invoices",
          #~ doctype=journals.get_doctype(Invoice),        
          #~ force_sequence=True)
        #~ INV.save()
        
        ORD.create_document() # Order(journal=ORD).save()
        INV.create_document() # Invoice(journal=INV).save()
        ORD.create_document() # Order(journal=ORD).save()
        ORD.create_document() # Order(journal=ORD).save()
        INV.create_document() # Invoice(journal=INV).save()
        s = "\n".join(unicode(doc) for doc in Document.objects.all())
        #print s
        self.assertEqual(s,u"""\
ORD#1 (1)
INV#1 (2)
ORD#2 (3)
ORD#3 (4)
INV#2 (5)""")

        # You can delete any Order, leaving a hole in the sequence, 
        # and this number will not be reused.

        Document.objects.get(pk=1).delete()
        
        doc = ORD.create_document() # Order(journal=ORD)
        self.assertEqual(unicode(doc),u"ORD#4 (6)")
        
        # For invoices,``force_sequence=True`` means that it is not allowed to
        # delete documents in the middle because this would leave a hole in the
        # sequence:

        try:
            Document.objects.get(pk=2).delete()
        except journals.DocumentError,e:
            pass
        else:
            self.fail("expected DocumentError")

        # It's okay to delete the last invoice of a journal. 

        doc = Document.objects.get(pk=5)
        self.assertEqual(unicode(doc),u"INV#2 (5)")
  
        doc.delete()
        
        doc = INV.create_document() # Invoice(journal=INV)
        #doc.save()
        self.assertEqual(unicode(doc),u"INV#2 (7)")

        # Here is again the list of documents in the database after these
        # operations::

        s = "\n".join(unicode(doc) for doc in Document.objects.all())
        #print s
        self.assertEqual(s,"""\
INV#1 (2)
ORD#2 (3)
ORD#3 (4)
ORD#4 (6)
INV#2 (7)""")
      
        
