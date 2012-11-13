# -*- coding: UTF-8 -*-
## Copyright 2012 Luc Saffre
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
This is a "reloadable" fixture. If you say::

  python manage.py loaddata web
  
it will overwrite existing web pages.

"""

import datetime
from django.conf import settings
#~ from lino.utils.instantiator import Instantiator
from lino import dd
from lino.utils import babel

pages = dd.resolve_app('pages')

def page(ref,title,body):
    page = pages.lookup(ref)
    if page is None:
    #~ qs = pages.Page.objects.filter(ref=ref)
    #~ if qs.count() == 0:
        return pages.Page(ref=ref,title=title,body=body)
    #~ if qs.count() == 1:
    #~ obj = qs[0]
    page.title = title
    page.body = body
    return page


def objects():
    yield page("hello","Hello","""\
The hello page.    
    """)
    
