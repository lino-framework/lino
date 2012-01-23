## Copyright 2008-2012 Luc Saffre
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

Import model definitions:

  >>> Order = reports.resolve_model('sales.Order')
  >>> Invoice = reports.resolve_model('sales.Invoice')

You can delete any Order, leaving a hole in the sequence.

  >>> Document.objects.get(pk=1).delete()
        
Once there is a hole, this number will not be reused.

  >>> doc = ORD.create_document() # Order(journal=ORD)
  >>> doc
  ORD#4 (6)
        
For invoices it is not allowed to delete documents in the
middle because this would leave a hole in the sequence:

  >>> Document.objects.get(pk=2).get_child_instance().delete()

It's okay to delete the last invoice of a journal. 

  >>> doc = Document.objects.get(pk=5)
  >>> print doc
  INV#2 (5)
  >>> doc.delete()
  >>> doc = INV.create_document() # Invoice(journal=INV)
  >>> print doc
  INV#2 (7)

Here is again the list of documents in the database after these
operations::

  >>> s = "\n".join(unicode(doc) for doc in Document.objects.all())
  >>> print s
  INV#1 (2)
  ORD#2 (3)
  ORD#3 (4)
  ORD#4 (6)
  INV#2 (7)

"""

from django.db import models
from django.utils.translation import ugettext_lazy as _


from lino import dd
from lino import mixins
from lino.models import SiteConfig

#~ from lino.modlib.contacts import models as contacts
#~ from lino.modlib.notes import models as notes
#~ from lino.modlib.cal import models as cal

if True: # dd.is_installed('igen'):

    contacts = dd.get_app('contacts')
    #~ notes = dd.get_app('notes')
    cal = dd.get_app('cal')

    #~ class Person(contacts.Person,contacts.Contact):
    #~ class Person(contacts.Contact,contacts.Born,contacts.Person):
    class Person(contacts.PersonMixin,contacts.Contact,contacts.Born):
        class Meta(contacts.PersonMixin.Meta):
            app_label = 'contacts'
            #~ # see :doc:`/tickets/14`
            verbose_name = _("Person")
            verbose_name_plural = _("Persons")

                  
    class Company(contacts.Contact,contacts.CompanyMixin):
        class Meta(contacts.CompanyMixin.Meta):
            app_label = 'contacts'
            #~ # see :doc:`/tickets/14`
            verbose_name = _("Company")
            verbose_name_plural = _("Companies")
        
    #~ class Note(notes.Note,mixins.Owned):
         #~ class Meta:
            #~ app_label = 'notes'
            # see :doc:`/tickets/14`
            #~ verbose_name = _("Note")
            #~ verbose_name_plural = _("Notes")
            
    #~ class NotesByOwner(dd.Table):
        #~ model = Note
        #~ master_key = 'owner'
     
    class Event(cal.Event):
        class Meta(cal.Event.Meta):
            app_label = 'cal'

    class Task(cal.Task):
        class Meta(cal.Task.Meta):
            app_label = 'cal'
     
     
    dd.inject_field(
        SiteConfig,
        'sales_base_account',
        models.ForeignKey("ledger.Account",
            blank=True,null=True,
            verbose_name=_("Sales base account"),
            related_name='sales_base_sites'),
        """The account where to book base amount of sales.
        """)

    dd.inject_field(
        SiteConfig,
        'sales_vat_account',
        models.ForeignKey("ledger.Account",
            blank=True,null=True,
            verbose_name=_("Sales VAT account"),
            related_name='sales_vat_sites'),
        """The account where to book VAT amount of sales.
        """)

     