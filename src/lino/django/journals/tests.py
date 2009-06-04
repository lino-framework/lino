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

from lino.django.journals.models import Journal, Document, register_doctype, DocumentError

class MyDocument(Document):
    pass
    
class Order(MyDocument):
    pass
register_doctype(Order)

class Invoice(MyDocument):
    pass
register_doctype(Invoice)



class TestCase(TestCase):
    def test01(self):
      
        # create two journals and some documents::

        ORD = Journal(id="ORD",name="Orders",doctype=0)
        ORD.save()
        INV = Journal(id="INV",name="Invoices",doctype=1,force_sequence=True)
        INV.save()
        ORD.create_document().save()
        INV.create_document().save()
        ORD.create_document().save()
        ORD.create_document().save()
        INV.create_document().save()
        s = "\n".join(unicode(doc) for doc in MyDocument.objects.all())
        #print s
        self.assertEqual(s,u"""\
ORD#1 (1)
INV#1 (2)
ORD#2 (3)
ORD#3 (4)
INV#2 (5)""")

        # You can delete any Order, leaving a hole in the sequence, 
        # and this number will not be reused.

        self.assertEqual(ORD.lastnum,3)
        MyDocument.objects.get(pk=1).delete()
        self.assertEqual(ORD.lastnum,3)
        
        doc = ORD.create_document()
        doc.save()
        self.assertEqual(unicode(doc),u"ORD#4 (6)")
        
        # For invoices, ``force_sequence=True`` means that it is not allowed to
        # delete documents in the middle because this would leave a hole in the
        # sequence:

        try:
            MyDocument.objects.get(pk=2).delete()
        except DocumentError,e:
            pass
        else:
            self.fail("expected DocumentError")

        # It's okay to delete the last invoice of a journal. 
        # This will also decrement lastnum so that the number will be reused::

        doc = MyDocument.objects.get(pk=5)
        self.assertEqual(unicode(doc),u"INV#2 (5)")
  
        doc.delete()
        INV = Journal.objects.get(id='INV') # re-fetch from db!
        self.assertEqual(INV.lastnum,1)
        
        doc = INV.create_document()
        doc.save()
        self.assertEqual(unicode(doc),u"INV#2 (7)")

        # Here is again the list of documents in the database after these
        # operations::

        s = "\n".join(unicode(doc) for doc in MyDocument.objects.all())
        #print s
        self.assertEqual(s,"""\
INV#1 (2)
ORD#2 (3)
ORD#3 (4)
ORD#4 (6)
INV#2 (7)""")
      
        
