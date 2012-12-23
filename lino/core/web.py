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

"""

import cgi
from jinja2 import Template

from jinja2 import Environment, PackageLoader

from django.conf import settings

from lino.utils import babel
from lino.utils import iif
from lino.utils.xmlgen import html as xghtml
    
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
    if site.sidebar_width:
        main_width -= site.sidebar_width
        yield '<div class="span%d">{{sidebar}}</div>' % site.sidebar_width
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
    


#~ jinja_env = Environment(loader=PackageLoader('lino', 'templates'))
jinja_env = Environment(trim_blocks=False)

def build_page_template(site):
    #~ return Template('\n'.join(list(bootstrap_page_template(site))))
    return jinja_env.from_string('\n'.join(list(bootstrap_page_template(site))))


def render(request,node,template=None,**context):
    def parse(s):
        #~ print 20121221, s
        #~ return Template(s).render(**context)
        return jinja_env.from_string(s).render(**context)
        
    def as_ul(action_spec):
        a = settings.LINO.modules.resolve(action_spec)
        ar = a.request()
        E = xghtml.E
        return E.tostring(E.ul(*[obj.as_list_item(ar) for obj in ar]))
        
    context.update(
        node=node,
        settings=settings,
        LINO=settings.LINO,
        #~ site=settings.LINO,
        #~ cgi=cgi,
        #~ babel=babel,
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

