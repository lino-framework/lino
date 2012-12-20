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
from lino.utils import memo

#~ from django.utils.translation import set_language
#~ from lino.utils.babel import get_language, set_language
from lino.utils.xmlgen import html as xghtml


#~ from lino import dd

#~ appname,version,url = settings.LINO.using().next()

#~ class DummyPage(AttrDict):
class DummyPage(object):
    pages_dict = {} # used as class variable
    ref = None
    language = None # 'en'
    abstract = None
    body = None
    def __init__(self,ref=None,title=None,**kw):
        self.ref = ref
        self.title = title or settings.LINO.title
        for k,v in kw.items():
            assert hasattr(self,k)
            setattr(self,k,v)
        if self.language is None:
            self.language = babel.DEFAULT_LANGUAGE
        if self.ref is not None:
            r = self.pages_dict.setdefault(self.ref,{})
            r[self.language] = self
        #~ logger.info("20121205 DummyPages %r,%r,%r",self.ref,self.language,
            #~ self.pages_dict.keys())
        #~ return self


class Parser(memo.Parser):
  
    #~ <body style="font-family:Arial;padding:2em;background-color:wheat;">
    page_template = """\
    <html>
    <head>
    <title>[=title]</title>
    </head>
    <body style="font-family:Arial;padding:2em;color:black;background-color:#c7dffc;">
    <h1>[=title]</h1>
    [=parse(obj.body)]
    </body>
    </html>
    """
  
  
    def __init__(self,*args,**kw):
        memo.Parser.__init__(self,*args,**kw)
        self.register_command('url',self.url2html)
        self.register_command('ref',self.ref2html)
        self.register_command('include',self.inc2html)
        self.register_command('ul',self.ul2html)
      
    def lookup_page(self,ref,language=None,strict=False): 
        #~ logger.info("20121205 lookup %r %r",ref,babel.get_language())
        r = DummyPage.pages_dict.get(ref)
        if r is None: return None
        #~ if language is None:
            #~ language = babel.get_language()
        p = r.get(language) 
        if p: return p
        if not strict and language != babel.DEFAULT_LANGUAGE:
            return r.get(babel.DEFAULT_LANGUAGE)
        
        #~ if ref == 'index':
            #~ if get_language() == 'fr':
                #~ return WEB_INDEX_FR
            #~ elif get_language() == 'de':
                #~ return WEB_INDEX_DE
            #~ return WEB_INDEX
        #~ if ref == 'admin':
            #~ return ADMIN_INDEX

    def create_page(self,**kw):
        #~ logger.info("20121219 dummy create_page %s %s",kw['ref'],kw.get('language'))
        return DummyPage(**kw)

    def instantiate_page(self,ref,language='en',title=None,body=None,**kw):
        """
        Instantiator shortcut for use in fixtures.
        """
        if title is not None: kw.update(title=title)
        if body is not None: kw.update(body=body)
        if language is None: language = ''
        kw.update(language=language)
        #~ lang = kw.get('language')
        #~ if lang is None:
            #~ kw.update(language=babel.DEFAULT_LANGUAGE)
            #~ babel.set_language(None)
        #~ else:
            #~ babel.set_language(lang)
        #~ page = None
        #~ if language in babel.AVAILABLE_LANGUAGES:
            #~ r = DummyPage.pages_dict.get(ref)
            #~ if r is not None: 
                #~ page = r.get(language) 
            # babel.set_language(language)
        page = self.lookup_page(ref,language,True)
        if page is None:
            #~ qs = pages.Page.objects.filter(ref=ref)
            #~ if qs.count() == 0:
            return self.create_page(ref=ref,**kw)
        #~ if qs.count() == 1:
        #~ obj = qs[0]
        for k,v in kw.items():
            setattr(page,k,v)
        #~ page.title = title
        #~ page.body = body
        #~ logger.info("20121219 updated %s %s",ref,language)
        return page
        
  
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
            
    def inc2html(self,ref):
        page = self.lookup_page(ref,babel.get_language())
        return page.body
        
    def ul2html(self,action_spec):
        a = settings.LINO.modules.resolve(action_spec)
        ar = a.request()
        E = xghtml.E
        return E.tostring(E.ul(*[obj.as_list_item(ar) for obj in ar]))
        


    def render(self,obj,template=None):
        context = dict(
            obj=obj,
            settings=settings,
            LINO=settings.LINO,
            cgi=cgi,
            babel=babel,
            iif=iif,
            E=xghtml.E,
            title=cgi.escape(obj.title))
            
        def parse(s):
            return self.parse(s,**context)
        context.update(parse=parse)
        
        #~ if not obj.body:
            #~ context.update(body=obj.abstract)
            
        if template is None:
            template = self.page_template
            
        def func():        
            return self.parse(template,**context)
        
        if obj.language:
            return babel.run_with_language(obj.language,func)
            
        return func()
            

MEMO_PARSER = Parser()

page = MEMO_PARSER.instantiate_page
lookup = MEMO_PARSER.lookup_page
render = MEMO_PARSER.render




if not settings.LINO.is_installed('pages'):
    from lino.modlib.pages.fixtures import web
    for p in web.objects():
        pass