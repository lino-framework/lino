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
The dummy module for `pages`.
"""

import logging
logger = logging.getLogger(__name__)

import cgi
import copy

from django.conf import settings

from lino.utils import AttrDict
from lino.utils import babel
from lino.utils.memo import Parser

from django.utils.translation import get_language

#~ appname,version,url = settings.LINO.using().next()

#~ class DummyPage(AttrDict):
class DummyPage(object):
    pages_dict = {} # used as class variable
    ref = None
    language = None # 'en'
    abstract = None
    body = None
    def __init__(self,ref,title=None,**kw):
        self.ref = ref
        self.title = title or settings.LINO.title
        for k,v in kw.items():
            assert hasattr(self,k)
            setattr(self,k,v)
    #~ def __new__(cls,*args,**kw):
        #~ self = AttrDict.__new__(cls,*args,**kw)
        r = self.pages_dict.setdefault(self.ref,{})
        r[self.language] = self
        #~ logger.info("20121205 DummyPages %r,%r,%r",self.ref,self.language,
            #~ self.pages_dict.keys())
        #~ return self


def lookup(ref): 
    #~ logger.info("20121205 lookup %r",get_language())
    r = DummyPage.pages_dict[ref]
    return r.get(get_language()) or r[None]
    
    #~ if ref == 'index':
        #~ if get_language() == 'fr':
            #~ return WEB_INDEX_FR
        #~ elif get_language() == 'de':
            #~ return WEB_INDEX_DE
        #~ return WEB_INDEX
    #~ if ref == 'admin':
        #~ return ADMIN_INDEX
    
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
        


WEB_INDEX = DummyPage("index",
    body="""\
<p>
Welcome to the <b>[=LINO.title]</b> site.
We are running <a href="[=LINO.url]">[=LINO.short_name]</a> 
version [=LINO.version], [=LINO.description]
</p>
""")
    
WEB_INDEX_FR = DummyPage("index",
    language='fr',
    body=u"""\
<p>
Bienvenue sur <b>[=LINO.title]</b>.
Ce site utilise <a href="[=LINO.url]">[=LINO.short_name]</a> 
version [=LINO.version], [=LINO.description]
</p>
""")
    
WEB_INDEX_DE = DummyPage("index",
    language='de',
    body=u"""\
<p>
Willkommen auf <b>[=LINO.title]</b>.
Diese Site benutzt <a href="[=LINO.url]">[=LINO.short_name]</a> 
version [=LINO.version], [=LINO.description]
</p>
""")
    
#~ ADMIN_INDEX = copy.copy(WEB_INDEX)
#~ ADMIN_INDEX.update(ref='admin')

ADMIN_INDEX = DummyPage("admin",
    body=WEB_INDEX.body)
ADMIN_INDEX_DE = DummyPage("admin",
    language='de',
    body=WEB_INDEX_DE.body)
ADMIN_INDEX_FR = DummyPage("admin",
    language='fr',
    body=WEB_INDEX_FR.body)

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

#~ else:
  
    #~ ADMIN_INDEX.body = WEB_INDEX.body
  

if settings.LINO.admin_url:
  
    ADMIN_INDEX.body += """
    <p>
    You have entered the admin section. 
    </p>
    """
    
ADMIN_INDEX.body += """
<p>
You will now probably want to 
use the <strong>Login</strong> button in the upper right corner 
and log in. 
</p><p>
This demo site has 
[=LINO.modules.users.UsersOverview.request().get_total_count()] 
users configured, they all have "1234" as password:
</p>
"""
ADMIN_INDEX_DE.body += u"""
<p>
Bitte klicken Sie jetzt auf <strong>Anmelden</strong> in der oberen rechten 
Bildschirmecke, um sich anzumelden.
</p><p>
Auf dieser Demo-Site gibt es
[=LINO.modules.users.UsersOverview.request().get_total_count()] 
Benutzer, die alle "1234" als Passwort haben:
</p>
"""

ADMIN_INDEX_FR.body += u"""
<p>
Veuillez cliquer maintenant sur le bouton <strong>Login</strong> 
dans le coin supérieur droit de l'écran.
</p><p>
Sur ce site démo il y a 
[=LINO.modules.users.UsersOverview.request().get_total_count()] 
utilisateurs, tous avec "1234" comme mot de passe:
</p>
"""

users = """
<ul>
[="".join(['<li><strong>%s</strong> : %s, %s, <strong>%s</strong></li>' % (\
  u.username, u, u.profile, babel.LANGUAGE_DICT.get(u.language)) \
  for u in LINO.modules.users.UsersOverview.request()])] 
</ul>
"""
ADMIN_INDEX.body += users
ADMIN_INDEX_DE.body += users
ADMIN_INDEX_FR.body += users


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

WEB_INDEX_DE.body += u"""
<p>
Viel Spaß!
Reaktionen und Kommentare sind willkommen an lino-users@googlegroups.com
oder direkt die Person, die Sie eingeladen hat.
</p>
"""

WEB_INDEX_FR.body += """
<p>
Enjoy!
Your feedback is welcome to lino-users@googlegroups.com
or directly to the person who invited you.
</p>
"""


#~ WEB_INDEX.body += """
#~ <iframe src="https://www.facebook.com/plugins/like.php?href=[=LINO.site_url]"
        #~ scrolling="no" frameborder="0"
        #~ style="border:none; width:450px; height:80px"></iframe>
#~ """



