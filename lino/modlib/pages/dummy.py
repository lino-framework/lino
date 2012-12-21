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
    special = False
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


class unused_Parser(memo.Parser):
  
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
    #~ logger.info("20121205 lookup %r %r",ref,babel.get_language())
    r = DummyPage.pages_dict.get(ref)
    if r is None: return None
    #~ if language is None:
        #~ language = babel.get_language()
    p = r.get(language) 
    if p: return p
    if not strict and language != babel.DEFAULT_LANGUAGE:
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
    
    
#~ self-made, inspired by http://de.selfhtml.org/css/layouts/mehrspaltige.htm
unused_SELFHTML_PAGE_TEMPLATE = """\
<html>
<head>
<title>[=title]</title>
<style type="text/css">
body {
  font-family:Arial;
  color:black;
  background-color:#c7dffc;
  padding:0em;
  margin:0em;
}
div#left_sidebar {
  float: left; width: 16em;
  background-color:#c0d0f0;
  padding:6pt;
}
div#main_area {
  margin-left: 16em;
  min-width: 14em; 
  padding:2em;
}
</style>
</head>
<body>
<div id="left_sidebar">%s</div>
<div id="main_area">
<h1>[=title]</h1>
[=parse(obj.body)]
<div id="footer">
[include footer]
</div>
</div>
</body>
</html>
"""

# https://github.com/joshuaclayton/blueprint-css/wiki/Quick-start-tutorial

def stylesheet(*args):
    url = settings.LINO.ui.media_url(*args) 
    return '<link rel="stylesheet" type="text/css" href="%s" />' % url

def unused_BLUEPRINT_PAGE_TEMPLATE(site):
    yield "<html><head>"
    yield "<title>[=title]</title>"
    p = site.ui.media_url('blueprint','screen.css')
    yield '<link rel="stylesheet" href="%s" type="text/css" media="screen, projection">' % p
    p = site.ui.media_url('blueprint','print.css')
    yield '<link rel="stylesheet" href="%s" type="text/css" media="print">' % p
    yield '<!--[if lt IE 8]>'
    p = site.ui.media_url('blueprint','ie.css')
    yield '  <link rel="stylesheet" href="%s" type="text/css" media="screen, projection">'
    yield '<![endif]-->'
    p = site.ui.media_url('lino','blueprint.css')
    yield '<link rel="stylesheet" href="%s" type="text/css">' % p
    yield '</head><body><div class="container">'
    
    if settings.LINO.site_config.header_page:
        yield '<div class="span-24 header">'
        yield settings.LINO.site_config.header_page.body
        yield '</div>'
        
    main_width = 24

    #~ html = settings.LINO.
    #~ if settings.LINO.site_config.sidebar_page:
    if settings.LINO.sidebar_width:
        main_width -= settings.LINO.sidebar_width
        yield '<div class="span-%d border">[sidebar]</div>' % settings.LINO.sidebar_width
        #~ yield settings.LINO.site_config.sidebar_page.body
        #~ yield '</div>'

    yield '<div class="span-%d last">' % main_width
    yield '<h1>[=title]</h1>'
    yield '[=parse(obj.body)]'
    yield '</div>'

    if settings.LINO.site_config.footer_page:
        yield '<div class="span-24 footer">'
        yield settings.LINO.site_config.footer_page.body
        yield '</div>'
    yield '</div></body></html>'
    
def unused_memoparser_bootstrap_page_template(site):
    yield '<!DOCTYPE html>'
    yield '<html language="en"><head>'
    yield '<meta charset="utf-8"/>'
    yield "<title>[=title]</title>"
    p = site.ui.media_url('bootstrap','css','bootstrap.css')
    yield '<link rel="stylesheet" href="%s" type="text/css">' % p
    p = site.ui.media_url('lino','bootstrap.css')
    yield '<link rel="stylesheet" href="%s" type="text/css">' % p
    yield '</head><body><div class="container-fluid">'
    if True:
        yield '  <div class="row-fluid header">[header]</div>'
    #~ if site.site_config.header_page:
        #~ yield '  <div class="row-fluid header">'
        #~ yield settings.LINO.site_config.header_page.body
        #~ yield '  </div>'
    yield '  <div class="row-fluid">'
    main_width = 12
    
    #~ if site.site_config.sidebar_page:
    if settings.LINO.sidebar_width:
        main_width -= settings.LINO.sidebar_width
        yield '<div class="span%d">[sidebar]</div>' % settings.LINO.sidebar_width
        #~ main_width -= 2
        #~ yield '    <div class="span2">'
        #~ yield site.site_config.sidebar_page.body
        #~ yield '    </div>'
        
    yield '    <div class="span%d">' % main_width
    #~ yield '<h1>[=title]</h1>'
    yield '[=iif(node.title,E.h1(node.title),"")]'
    yield '[=parse(node.body)]'
    yield '    </div>'
    yield '  </div>'
    if True: # site.site_config.footer_page:
        yield '  <div class="row-fluid footer">[footer]</div>'
        #~ yield '  <div class="row-fluid footer">'
        #~ yield settings.LINO.site_config.footer_page.body
        #~ yield '  </div>'
    
    yield '</div></body></html>'
    
    
    


def bootstrap_page_template(site):
    yield '<!DOCTYPE html>'
    yield '<html language="en"><head>'
    yield '<meta charset="utf-8"/>'
    yield "<title>{{node.title}}</title>"
    p = site.ui.media_url('bootstrap','css','bootstrap.css')
    yield '<link rel="stylesheet" href="%s" type="text/css">' % p
    p = site.ui.media_url('lino','bootstrap.css')
    yield '<link rel="stylesheet" href="%s" type="text/css">' % p
    yield '</head><body><div class="container-fluid">'
    if True:
        yield '  <div class="row-fluid header">{{header}}</div>'
    #~ if site.site_config.header_page:
        #~ yield '  <div class="row-fluid header">'
        #~ yield settings.LINO.site_config.header_page.body
        #~ yield '  </div>'
    yield '  <div class="row-fluid">'
    main_width = 12
    
    #~ if site.site_config.sidebar_page:
    if settings.LINO.sidebar_width:
        main_width -= settings.LINO.sidebar_width
        yield '<div class="span%d">{{sidebar}}</div>' % settings.LINO.sidebar_width
        #~ main_width -= 2
        #~ yield '    <div class="span2">'
        #~ yield site.site_config.sidebar_page.body
        #~ yield '    </div>'
        
    yield '    <div class="span%d">' % main_width
    #~ yield '<h1>[=title]</h1>'
    yield '{% if node.title%}<h1>{{node.title}}</h1>{% endif %}'
    yield '{{parse(node.body)}}'
    yield '    </div>'
    yield '  </div>'
    if True: # site.site_config.footer_page:
        yield '  <div class="row-fluid footer">{{footer}}</div>'
        #~ yield '  <div class="row-fluid footer">'
        #~ yield settings.LINO.site_config.footer_page.body
        #~ yield '  </div>'
    
    yield '</div></body></html>'
    


from jinja2 import Template


def site_setup(site):
    site.PAGE_TEMPLATE = Template('\n'.join(list(bootstrap_page_template(settings.LINO))))
    
def get_sidebar_html(site,request=None,node=None,**context):
    return ''
  
            
def render(request,node,template=None,**context):
    def parse(s):
        #~ print 20121221, s
        return Template(s).render(**context)
        
    def as_ul(action_spec):
        a = settings.LINO.modules.resolve(action_spec)
        ar = a.request()
        E = xghtml.E
        return E.tostring(E.ul(*[obj.as_list_item(ar) for obj in ar]))
        
    context.update(
        node=node,
        settings=settings,
        LINO=settings.LINO,
        cgi=cgi,
        babel=babel,
        parse=parse,
        as_ul=as_ul,
        iif=iif,
        E=xghtml.E,
        #~ title=cgi.escape(node.title)
        )
    context.update(sidebar=settings.LINO.get_sidebar_html(**context))
    context.update(header=settings.LINO.get_header_html(**context))
    context.update(footer=settings.LINO.get_footer_html(**context))
        
    #~ def parse(s):
        #~ return self.parse(s,**context)
    #~ context.update(parse=parse)
    
    #~ if not obj.body:
        #~ context.update(body=obj.abstract)
        
    if template is None:
        template = settings.LINO.PAGE_TEMPLATE
        
    return template.render(**context)


#~ MEMO_PARSER = Parser()

  
  
#~ NODE_PARSER = Parser()

#~ page = MEMO_PARSER.instantiate_page
#~ lookup = MEMO_PARSER.lookup_page
#~ render = MEMO_PARSER.render




if not settings.LINO.is_installed('pages'):
    from lino.modlib.pages.fixtures import web
    for p in web.objects():
        pass