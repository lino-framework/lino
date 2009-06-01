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

import os
import datetime

import settings
from django.core.management import setup_environ
setup_environ(settings)

from lino.console import syscon

from lino.django.utils.sites import site as lino_site
from lino.django.igen.models import Order, PendingOrders

        
def main():
    for name,url,version in lino_site.thanks_to():
        print name,version, "<%s>" % url
        
    rpt = PendingOrders()
    print rpt.as_text()
    
    q = [o for o in Order.objects.pending()]
    if len(q) == 0:
        print "Nothing to do"
        return
    #~ for o in q:
        #~ print o
    if not syscon.confirm("Call make_invoices on these orders?"):
        return
    for o in q:
        i = o.make_invoice()
        print "%s made %s" % (o,i)

if __name__ == "__main__":
    main()
