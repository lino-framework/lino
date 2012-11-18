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

import cgi
import copy

from django.conf import settings
from lino.utils import AttrDict
from lino.utils import babel
from lino.utils.memo import Parser

#~ appname,version,url = settings.LINO.using().next()

class DummyPage(AttrDict):
    ref = None
    language = 'en'
    abstract = None
    
WEB_INDEX = DummyPage(
    ref="index",
    title=settings.LINO.title,
    body="""<p>
Welcome to the <b>%(title)s</b> site.
We are running <a href="[=LINO.url]">[=LINO.short_name]</a> 
version [=LINO.version], [=LINO.description]
</p>
""" % dict(
    title=settings.LINO.title
    #~ short_name=settings.LINO.short_name,
    #~ version=settings.LINO.version
    ))
    
ADMIN_INDEX = copy.copy(WEB_INDEX)
ADMIN_INDEX.update(ref='admin')

if settings.LINO.admin_url:
  
    if settings.LINO.user_model is None:
        raise Exception("When admin_url is not empty, user_model cannot be None")
        
    WEB_INDEX.body += """
    <p>
    You are currently seeing the <strong>plain web content</strong> section,
    which contains just this default index page 
    because this site hasn't been configured to show something else here.
    </p>

    <p>
    To see what Lino really adds to a Django site, 
    you should go to the <strong>admin</strong> section.
    </p>
    <p align="center"><button onclick="document.location='/admin/'">admin</button></p>
    """

else:
  
    ADMIN_INDEX.body = WEB_INDEX.body
  

if settings.LINO.admin_url:
  
    ADMIN_INDEX.body += """
    <p>
    You have entered the admin section. 
    </p>
    """
    
ADMIN_INDEX.body += """
<p>
You will probably want to 
use the <strong>Login</strong> button in the upper right corner 
and log in. 
</p>
<p>
This demo site has 
[=LINO.modules.users.UsersOverview.request().get_total_count()] 
users configured, they all have "1234" as password:
<ul>
[="".join(['<li><strong>%s</strong> : %s, %s, <strong>%s</strong></li>' % (\
  u.username, u, u.profile, babel.LANGUAGE_DICT.get(u.language)) \
  for u in LINO.modules.users.UsersOverview.request()])] 
</ul>
"""


if settings.LINO.admin_url:
  
    ADMIN_INDEX.body += """
    <p>
    Or you might want to return to the <a href="/">web content section</a>.
    </p>
    """

#~ </p><p>
#~ [=LINO.modules.users.UsersOverview.to_html()]


WEB_INDEX.body += """
<p>
Enjoy!
Your feedback is welcome to lino-users@googlegroups.com
or directly to the person who invited you.
</p>
"""





def lookup(ref): 
    if ref == 'index':
        return WEB_INDEX
    if ref == 'admin':
        return ADMIN_INDEX
    


MEMO_PARSER = Parser()

def render(obj,template):
    context = dict(
        obj=obj,
        settings=settings,
        LINO=settings.LINO,
        cgi=cgi,
        babel=babel,
        title=cgi.escape(obj.title))
        
    def parse(s):
        return MEMO_PARSER.parse(s,**context)
    context.update(parse=parse)
    
    #~ if not obj.body:
        #~ context.update(body=obj.abstract)
        
    def func():        
        return MEMO_PARSER.parse(template,**context)
    
    if obj.language:
        return babel.run_with_language(obj.language,func)
        
    return func()
        
