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

from django.conf import settings
from lino import dd

pages = dd.resolve_app('pages')

def objects():
    yield pages.page("index",'en',"Welcome","""\
Welcome to this great site about [ref life], the universe and everything.
    """)
    
    yield pages.page("about",'en',"About","""\
This website is a virgin 
[url http://lino-framework.org/autodoc/lino.apps.cms.html Lino CMS] 
site which has not yet been configured.
    """)
    
    yield pages.page("life",None,"Life","""\
This page is about life.
    """)
    
    #~ yield pages.page("admin","Admin","""\
#~ Here you can configure this great website.""")
    
    p = pages.page('footer',None,"Footer","""\
Copyright &copy; 1789 The Great Site""")
    yield p
    settings.LINO.update_site_config(footer_page=p)
    
    p = pages.page('header',None,"Header","""\
[url /admin/ Admin]""")
    yield p
    settings.LINO.update_site_config(header_page=p)
    
    p = pages.page('sidebar',None,"Sidebar","""\
[url / Home]
<br>[ref about]
<br>[url /admin/ Admin]
    """)
    yield p
    settings.LINO.update_site_config(sidebar_page=p)
    