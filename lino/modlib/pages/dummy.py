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

#~ print 20121219, __file__


import logging
logger = logging.getLogger(__name__)

import cgi
import copy

from django.conf import settings

from lino.utils import AttrDict
from lino.utils import babel
from lino.utils import iif
from lino.utils.xmlgen import html as xghtml
#~ from lino.utils import memo

#~ from django.utils.translation import set_language
#~ from lino.utils.babel import get_language, set_language


#~ from lino import dd

#~ appname,version,url = settings.LINO.using().next()

#~ class DummyPage(AttrDict):
class DummyPage(object):
    pages_dict = {} # used as class variable
    ref = None
    #~ language = 'en'
    language = None 
    abstract = None
    body = None
    special = False
    def __init__(self,ref=None,title=None,**kw):
        self.ref = ref
        self.title = title or settings.LINO.title
        for k,v in kw.items():
            assert hasattr(self,k)
            setattr(self,k,v)
        if self.language is None:
            #~ self.language = babel.DEFAULT_LANGUAGE
            self.language = ''
        if self.ref is not None:
            r = self.pages_dict.setdefault(self.ref,{})
            r[self.language] = self
        #~ logger.info("20121205 DummyPages %r,%r,%r",self.ref,self.language,
            #~ self.pages_dict.keys())
        #~ return self

    def __unicode__(self):
        return "%s -> %s (%s)" % (self.ref,self.title,self.language)

class unused_Parser: # (memo.Parser):
  
    #~ <body style="font-family:Arial;padding:2em;background-color:wheat;">
    page_template = """\
    <html>
    <head>
    <title>[=title]</title>
    </head>
    <body style="font-family:Arial;padding:2em;color:black;background-color:#c7dffc;">
    <h1>[=title]</h1>
    [=parse(node.body)]
    </body>
    </html>
    """
  
  
    def __init__(self,*args,**kw):
        memo.Parser.__init__(self,*args,**kw)
        self.register_command('url',self.url2html)
        self.register_command('ref',self.ref2html)
        self.register_command('include',self.inc2html)
        self.register_command('sidebar',self.sidebar2html)
        self.register_command('header',self.header2html)
        self.register_command('footer',self.footer2html)
        self.register_command('ul',self.ul2html)
      
  
    def url2html(self,s):
        if not s: return "XXX"
        chunks = s.split(None,1)
        url = chunks[0]
        if len(chunks) == 1:
            text = url
        else:
            text = chunks[1]
        return '<a href="%s">%s</a>' % (url,text)
            

    def ref2html(self,s):
        if not s: return "XXX"
        chunks = s.split(None,1)
        if len(chunks) == 1:
            ref = chunks[0]
            page = self.lookup_page(ref,babel.get_language())
            return '<a href="%s">%s</a>' % (page.ref,page.title)
        elif len(chunks) == 2:
            ref,text = chunks
            url = '/' + ref
            return '<a href="%s">%s</a>' % (url,text)
        raise NotImplementedError(chunks)
            
    def sidebar2html(self,ref): return settings.LINO.get_sidebar_html(**self.context)
    def header2html(self,ref): return settings.LINO.get_header_html(**self.context)
    def footer2html(self,ref): return settings.LINO.get_footer_html(**self.context)
        
    def inc2html(self,ref):
        page = self.lookup_page(ref,babel.get_language())
        return page.body
        
    def ul2html(self,action_spec):
        a = settings.LINO.modules.resolve(action_spec)
        ar = a.request()
        E = xghtml.E
        return E.tostring(E.ul(*[obj.as_list_item(ar) for obj in ar]))




#~ def page(ref,language=None,strict=False): 
def lookup(ref,language=None,strict=False): 
    #~ logger.info("20121205 lookup %r %r,%r",ref,language,DummyPage.pages_dict)
    r = DummyPage.pages_dict.get(ref)
    if r is None: return None
    #~ if language is None:
        #~ language = babel.get_language()
    p = r.get(language) 
    if p: return p
    if not strict:
        p = r.get('') 
        if p: return p
        if language != babel.DEFAULT_LANGUAGE:
            return r.get(babel.DEFAULT_LANGUAGE)
    
def create_page(**kw):
    #~ logger.info("20121219 dummy create_page %s %s",kw['ref'],kw.get('language'))
    return DummyPage(**kw)

def page(ref,language='en',title=None,body=None,**kw):
    """
    Instantiator shortcut for use in fixtures.
    """
    if title is not None: kw.update(title=title)
    if body is not None: kw.update(body=body)
    if language is None: language = ''
    kw.update(language=language)
    page = lookup(ref,language,True)
    if page is None:
        #~ qs = pages.Page.objects.filter(ref=ref)
        #~ if qs.count() == 0:
        return create_page(ref=ref,**kw)
    #~ if qs.count() == 1:
    #~ obj = qs[0]
    for k,v in kw.items():
        setattr(page,k,v)
    #~ page.title = title
    #~ page.body = body
    #~ logger.info("20121219 updated %s %s",ref,language)
    return page
    
    
#~ def get_sidebar_html(site,request=None,node=None,**context):
    #~ return ''
  
        
from lino.core.web import render_node

def get_all_pages():
    for ref2pages in DummyPage.pages_dict.values():
        for page in ref2pages.values():
            yield page


if not settings.LINO.is_installed('pages'):
    # fill DummyPage.pages_dict at import by running the std fixture
    from lino.modlib.pages.fixtures import std
    for p in std.objects():
        pass
        