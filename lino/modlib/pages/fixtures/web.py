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

pages = dd.resolve_app('pages')

def page(ref,title,body):
    qs = pages.Page.objects.filter(ref=ref)
    if qs.count() == 0:
        return pages.Page(ref=ref,title=title,body=body)
    elif qs.count() == 1:
        obj = qs[0]
        obj.title = title
        obj.body = body
        return obj
        

def objects():
    yield page("index","Welcome","""\
<p>
Welcome to the <b>[=settings.LINO.title]</b> site.
</p><p>
[=settings.LINO.help_text]
</p><p>
You are currently seeing the "plain web content" section,
which contains just this default index page 
because it hasn't been configured to show something else.
</p><p>To see what Lino really adds to a Django site, 
you should go to the <a href="/admin/">admin</a> section
and log in using the button in the upper right corner.
This demo site has 
[=settings.LINO.modules.users.UsersOverview.request().get_total_count()] 
users configured, they all have "1234" as password:

[=settings.LINO.modules.users.UsersOverview.to_html()]

<p>Enjoy! 
Any feedback is welcome to lino-users@googlegroups.com
or directly to the person who invited you.
</p>


""")

