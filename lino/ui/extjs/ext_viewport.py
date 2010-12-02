## Copyright 2009-2010 Luc Saffre
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

raise Exception("no longer used")

from django.conf import settings
from . import ext_requests
from lino.utils.jsgen import py2js, js_code, id2js


class Viewport:
  
    def __init__(self,ui,site,*components):
        self.title = site.title
        self.site = site
        self.ui = ui
        #self.main_menu = main_menu
        
        #self.variables = []
        self.components = components
        #self.visibles = []
        #~ for c in components:
            #~ for v in c.ext_variables():
                #~ self.variables.append(v)
            #~ self.components.append(c)
            
        #~ self.variables.sort(lambda a,b:cmp(a.declaration_order,b.declaration_order))
        
        
    def render_to_html(self,request):
        s = """<html><head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title id="title">%s</title>""" % self.title
        s += """
<!-- ** CSS ** -->
<!-- base library -->
<link rel="stylesheet" type="text/css" href="%sextjs/resources/css/ext-all.css" />""" % settings.MEDIA_URL 
        s += """
<!-- overrides to base library -->
<!-- ** Javascript ** -->
<!-- ExtJS library: base/adapter -->
<script type="text/javascript" src="%sextjs/adapter/ext/ext-base.js"></script>""" % settings.MEDIA_URL 
        widget_library = 'ext-all-debug'
        #widget_library = 'ext-all'
        s += """
<!-- ExtJS library: all widgets -->
<script type="text/javascript" src="%sextjs/%s.js"></script>""" % (settings.MEDIA_URL, widget_library)
        if True:
            s += """
<style type="text/css">
/* http://stackoverflow.com/questions/2106104/word-wrap-grid-cells-in-ext-js  */
.x-grid3-cell-inner, .x-grid3-hd-inner {
  white-space: normal; /* changed from nowrap */
}
</style>"""
        if False:
            s += """
<script type="text/javascript" src="%sextjs/Exporter-all.js"></script>""" % settings.MEDIA_URL 

        s += """
<!-- overrides to library -->
<link rel="stylesheet" type="text/css" href="%slino/extjsw/lino.css">""" % settings.MEDIA_URL
        s += """
<script type="text/javascript" src="%slino/extjsw/lino.js"></script>""" % settings.MEDIA_URL
        s += """
<script type="text/javascript" src="%s"></script>""" % (settings.MEDIA_URL + "/".join(self.ui.js_cache_name(self.site)))

        s += """
<!-- page specific -->
<script type="text/javascript">
"""

        #~ uri = request.path
        
        def js():
            yield "Lino.load_master = function(store,caller,record) {"
            #~ yield "  console.log('load_master() mt=',caller.content_type,',mk=',record.id);"
            yield "  store.setBaseParam(%r,caller.content_type);" % ext_requests.URL_PARAM_MASTER_TYPE
            yield "  store.setBaseParam(%r,record.id);" % ext_requests.URL_PARAM_MASTER_PK
            yield "  store.load();" 
            yield "};"
            
        s += py2js(js)
        
        def js():
            yield "Lino.search_handler = function(caller) { return function(field, e) {"
            yield "  if(e.getKey() == e.RETURN) {"
            # yield "    console.log('keypress',field.getValue(),store)"
            yield "    caller.main_grid.getStore().setBaseParam('%s',field.getValue());" % ext_requests.URL_PARAM_FILTER
            yield "    caller.main_grid.getStore().load({params: { start: 0, limit: caller.pager.pageSize }});" 
            yield "  }"
            yield "}};"
        
        s += py2js(js)
        
        s += """
Ext.onReady(function(){ """

        #~ for c in self.components:
            #~ for ln in c.js_declare():
                #~ s += "\n" + ln

        d = dict(layout='border')
        d.update(items=js_code(py2js([js_code('Lino.main_menu')]+list(self.components))))
        s += """
  Lino.main_menu = new Ext.Toolbar({region:'north',height:27});
  Lino.viewport = new Ext.Viewport(%s);""" % py2js(d)
        s += """
  Lino.viewport.render('body');
  Lino.load_main_menu();
  Ext.QuickTips.init();
  Lino.run_permalink();
        """
        s += "\n}); // end of onReady()"
        s += "\n</script></head><body></body></html>"
        return s
