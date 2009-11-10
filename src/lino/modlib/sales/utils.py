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
make_invoices() creates invoices. 

These new invoices are not yet signed. 
A user must sign them using the web interface before they can be sent.

send_invoices() then "sends" the signed invoices:
  - create a PDF version 
  - send this to a printer (for regular mail channel) 
    or directly via e-mail to the customer.
"""

import os
import datetime

from timtools.console import syscon

import lino
from lino import reports

from lino.modlib.sales import models as sales
#sales = reports.get_app('sales')

        
def make_invoices(make_until=None):
    #~ rpt = sales.PendingOrders()
    #~ print rpt.as_text()
    
    q = [o for o in sales.Order.objects.pending(make_until)]
    lino.log.debug("make_invoices(make_until=%s)",make_until)
    made = []
    for o in q:
        i = o.make_invoice(make_until)
        #s += "%s -> %s\n" % (o,i)
        made.append((o,i))
    return made
    
    

def send_invoices():
    q = [ o.get_child_instance() for o in sales.SalesDocument.objects.all() ]
    q = [ o for o in q if o.must_send() ]
    #~ q = [o for o in sales.SalesDocument.objects.filter(
        #~ sent_time__exact=None).exclude(user__exact=None)]
    if len(q) == 0:
        print "Nothing to do."
        return
    print "%d documents to send: " % len(q) \
      + ", ".join(str(d) for d in q)
    if not syscon.confirm("Send these documents?"):
        return
    for doc in q:
        doc.send()

