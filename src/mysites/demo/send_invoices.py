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

from lino.django.utils.sites import lino_site
from lino.django.igen.models import Document

        
def main():
    for name,url,version in lino_site.thanks_to():
        print name,version, "<%s>" % url
        
    q = [o for o in Document.objects.filter(sent_date__exact=None).exclude(user__exact=None)]
    if len(q) == 0:
        print "Nothing to do"
        return
    print "%d documents to send: " % len(q) + ", ".join(str(d) for d in q)
    #~ for d in q:
        #~ print d
    if not syscon.confirm("Call send() on these documents?"):
        return
    for d in q:
        d.send()

if __name__ == "__main__":
    main()
