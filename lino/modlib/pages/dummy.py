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


from django.conf import settings
from lino.utils import AttrDict

appname,version,url = settings.LINO.using().next()

DUMMY_INDEX = AttrDict(
    ref="index",
    language='en',
    title=settings.LINO.title,
    abstract=None,
    body="""<p>
Welcome to the <b>%(title)s</b> site.
We are running <a href="%(url)s">%(appname)s</a> version %(version)s.
[=LINO.get_application_description()]
""" % dict(
    title=settings.LINO.title,
    appname=appname,
    version=version,
    url=url))
    
DUMMY_INDEX.body += """</p>
<p>
You are currently seeing the <strong>plain web content</strong> 
section,
which contains just this default index page 
because this site hasn't been configured to show something else here.
</p>

<p>
To see what Lino really adds to a Django site, 
you should go to the <strong>admin</strong> section.

In the admin section you will probably want to 
use the <strong>Log in</strong> button in the upper right corner 
and log in. This demo site has 
[=LINO.modules.users.UsersOverview.request().get_total_count()] 
users configured, they all have "1234" as password:

[="".join(['<li><strong>%s</strong> : %s, %s, %s</li>' % (\
  u.username, u, u.profile, babel.LANGUAGE_DICT.get(u.language)) \
  for u in LINO.modules.users.UsersOverview.request()])]

<p>
Your feedback is welcome to lino-users@googlegroups.com
or directly to the person who invited you.
</p>
<p align="center"><button onclick="document.location='/admin/'">admin</button>
</p>
"""

#~ </p><p>
#~ [=LINO.modules.users.UsersOverview.to_html()]



def lookup(ref): 
    if ref == 'index':
        return DUMMY_INDEX
    
