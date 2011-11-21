## Copyright 2008-2009 Luc Saffre.
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

import datetime
import dateutil


from django.db import models
#from lino.django.tom import models
from django.utils.safestring import mark_safe

from lino.django.utils.validatingmodel import TomModel, ModelValidationError
from lino.django.utils import render

#from lino.django.utils.journals import Journal
#from lino.django.journals import models as journals
from . import fields, journals

from django.contrib.auth.models import User

def linkto(href,text=None):
    if text is None:
        text=href
    return '<a href="%s">%s</a>' % (href,text)
        
from .countries import Country, Language
from .journals import Journal




##
## report definitions
##        
        
from django import forms

from lino.django.utils import reports
from lino.django.utils import layouts
from lino.django.utils import perms

from . import countries


        
class MakeInvoicesDialog(layouts.Dialog):
    # not yet working
    class form_class(forms.Form):
        today = forms.DateField(label="Generate invoices on")
        order = forms.ModelChoiceField(
            label="(only for this single order:)",
            queryset=Order.objects.all())
    
    intro = layouts.StaticText("""
    <p>This is the first example of a <em>Dialog</em>.</p>
    """)
    
    layout = """
    intro
    today
    order
    simulate ok cancel help
    """
    
    def execute(self,simulate=False):
        orders_seen = 0
        invoices_made = 0
        if self.order is not None: # all orders
            orders = Order.objects.all()
        else:
            orders = ( self.order, )
        for ct in orders:
            orders_seen += 1
            if ct.make_invoice(self.make_until,simulate):
                invoices_made += 1
        if simulate:
            msg = "%d orders would make %d invoices."
        else:
            msg = "%d orders made %d new invoices."
        self.message(msg,orders_seen, invoices_made)
        
    def ok(self):
        return self.execute(simulate=False)
        
    def simulate(self):
        return self.execute(simulate=True)
            
        


def lino_setup(lino):
    pass
    #~ m = lino.add_menu("contacts","~Contacts")
    #~ m.add_action(Companies())
    #~ m.add_action(Persons())
    #~ m.add_action(Contacts(),label="All")
    #~ m = lino.add_menu("prods","~Products")
    #~ m.add_action(Products())
    #~ m.add_action(ProductCats())
    #~ m = lino.add_menu("docs","~Documents",
      #~ can_view=perms.is_authenticated)
    #~ m.add_action(Orders())
    #~ m.add_action(Invoices())
    #~ m.add_action(DocumentsToSign())
    #~ m.add_action(PendingOrders())
    
    #~ m = lino.add_menu("admin","~Administration",
      #~ can_view=perms.is_staff)
    #~ m.add_action(MakeInvoicesDialog())
    
    #~ m = lino.add_menu("config","~Configuration",
      #~ can_view=perms.is_staff)
    #~ m.add_action(InvoicingModes())
    #~ m.add_action(ShippingModes())
    #~ m.add_action(PaymentTerms())
    #~ m.add_action(countries.Languages())
    #~ m.add_action(countries.Countries())


