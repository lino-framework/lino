## Copyright 2009 Luc Saffre 

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

from lino.console import syscon
from lino.django.apps.sales import models as sales
from lino.django.utils.sites import lino_site

def thanks_to():
    for name,url,version in lino_site.thanks_to():
        print name,version, "<%s>" % url

        
def make_invoices(make_until=None):
    #~ rpt = sales.PendingOrders()
    #~ print rpt.as_text()
    
    q = [o for o in sales.Order.objects.pending(make_until)]
    s = "make_invoices(make_until=%r):\n" % make_until
    for o in q:
        i = o.make_invoice(make_until)
        s += "%s -> %s\n" % (o,i)
    if len(q) == 0:
        s += "Nothing to do.\n"
    else:
        s += "%d invoices have been issued.\n" % len(q)
    return s
    
    

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

