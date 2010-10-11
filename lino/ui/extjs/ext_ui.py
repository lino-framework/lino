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


import os
import cgi
#import traceback
import cPickle as pickle
from urllib import urlencode

from django import http
from django.db import models
from django.db import IntegrityError
from django.conf import settings
from django.http import HttpResponse, Http404
from django import http
from django.core import exceptions
from django.utils import functional

from django.utils.translation import ugettext as _
from django.utils import simplejson as json

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

import lino
from lino.utils import ucsv
from lino.utils import mixins
from lino.utils import choosers
from lino import actions #, layouts #, commands
from lino import reports        
from lino.ui import base
#~ from lino import diag
#~ from lino import forms
from lino.core import actors
#~ from lino.core import action_requests
from lino.utils import menus
#~ from lino.utils import build_url
from lino.utils import jsgen
from lino.utils.jsgen import py2js, js_code, id2js
from . import ext_elems
from . import ext_store
from . import ext_windows
from . import ext_viewport
from . import ext_requests
#from lino.modlib.properties.models import Property
#~ from lino.modlib.properties import models as properties

from django.conf.urls.defaults import patterns, url, include
from lino.utils.mixins import PrintAction

from lino.core.coretools import app_labels

from lino.modlib.fields import LANGUAGE_CHOICES

#~ from lino.ui.extjs.ext_windows import WindowConfig # 20100316 backwards-compat window_confics.pck 

class HttpResponseDeleted(HttpResponse):
    status_code = 204
    
def prepare_label(mi):
    label = unicode(mi.label) # trigger translation
    n = label.find(mi.HOTKEY_MARKER)
    if n != -1:
        label = label.replace(mi.HOTKEY_MARKER,'')
        #label=label[:n] + '<u>' + label[n] + '</u>' + label[n+1:]
    return label
        


def parse_bool(s):
    return s == 'true'
    
def parse_int(s,default=None):
    if s is None: return None
    return int(s)

def json_response_kw(**kw):
    return json_response(kw)
    
def json_response(x):
    #s = simplejson.dumps(kw,default=unicode)
    #return HttpResponse(s, mimetype='text/html')
    s = py2js(x)
    #lino.log.debug("json_response() -> %r", s)
    return HttpResponse(s, mimetype='text/html')

def elem2rec1(request,rh,elem,**rec):
    rec.update(data=rh.store.row2dict(request,elem))
    return rec
      
def elem2rec_detailed(request,rh,elem,**rec):
    rec = elem2rec1(request,rh,elem,**rec)
    rec.update(id=elem.pk)
    rec.update(title=unicode(elem))
    first = None
    prev = None
    next = None
    last = None
    if rh.report.show_prev_next:
      ar = ext_requests.ViewReportRequest(request,rh,rh.report.default_action)
      recno = 0
      if ar.total_count > 0:
          first = ar.queryset[0]
          last = ar.queryset.reverse()[0]
          if first is not None: first = first.pk
          if last is not None: last = last.pk
          if ar.total_count > 200:
              #~ TODO: check performance
              pass
          g = enumerate(ar.queryset) # a generator
          try:
              while True:
                  index, item = g.next()
                  if item == elem:
                      if index > 0:
                          prev = ar.queryset[index-1]
                      recno = index + 1
                      i,next = g.next()
                      break
          except StopIteration:
              pass
          if prev is not None: prev = prev.pk
          if next is not None: next = next.pk
      rec.update(navinfo=dict(first=first,prev=prev,next=next,last=last,msg="Row %d of %d" % (recno,ar.total_count)))
    return rec
            
    
    


class ExtUI(base.UI):
    _response = None
    name = 'extjs'
    verbose_name = "ExtJS with Windows"
    #~ window_configs_file = os.path.join(settings.PROJECT_DIR,'window_configs.pck')
    Panel = ext_elems.Panel
    
    #~ USE_WINDOWS = False  # If you change this, then change also Lino.USE_WINDOWS in lino.js

    def __init__(self,site):
        jsgen.register_converter(self.py2js_converter)
        #~ self.window_configs = {}
        #~ if os.path.exists(self.window_configs_file):
            #~ lino.log.info("Loading %s...",self.window_configs_file)
            #~ wc = pickle.load(open(self.window_configs_file,"rU"))
            #~ #lino.log.debug("  -> %r",wc)
            #~ if type(wc) is dict:
                #~ self.window_configs = wc
        #~ else:
            #~ lino.log.warning("window_configs_file %s not found",self.window_configs_file)
            
        base.UI.__init__(self,site) # will create a.window_wrapper for all actions
        self.build_site_js()
        
    def create_layout_element(self,lh,panelclass,name,**kw):
        
        if name == "_":
            return ext_elems.Spacer(lh,name,**kw)
            
        de = lh.rh.report.get_data_elem(name)
        #~ de = reports.get_data_elem(lh.layout.datalink,name)
        
        if de is None:
            a = lh.rh.report.get_action(name)
            if isinstance(a,actions.ImageAction):
                return ext_elems.PictureElement(lh,name,a)
          
        #~ if isinstance(de,properties.Property):
            #~ return self.create_prop_element(lh,de,**kw)
        if isinstance(de,models.Field):
            return self.create_field_element(lh,de,**kw)
        if isinstance(de,generic.GenericForeignKey):
            # create a horizontal panel with 2 comboboxes
            return lh.desc2elem(panelclass,name,de.ct_field + ' ' + de.fk_field,**kw)
            #~ return ext_elems.VirtualFieldElement(lh,name,de,**kw)
        if callable(de):
            return self.create_meth_element(lh,name,de,**kw)
        if isinstance(de,reports.Report):
            e = ext_elems.SlaveGridElement(lh,name,de,**kw)
            #~ e = ext_elems.GridElement(lh,name,de.get_handle(self),**kw)
            lh.slave_grids.append(e)
            return e
            #~ return ext_elems.GridElementBox(lh,e)
        #~ if isinstance(de,forms.Input):
            #~ e = ext_elems.InputElement(lh,de,**kw)
            #~ if not lh.start_focus:
                #~ lh.start_focus = e
            #~ return e
        if not name in ('__str__','__unicode__','name','label'):
            value = getattr(lh.layout,name,None)
            if value is not None:
                if isinstance(value,basestring):
                    return lh.desc2elem(panelclass,name,value,**kw)
                if isinstance(value,reports.StaticText):
                    return ext_elems.StaticTextElement(lh,name,value)
                if isinstance(value,reports.DataView):
                    return ext_elems.DataViewElement(lh,name,value)
                    #~ return ext_elems.TemplateElement(lh,name,value)
                if isinstance(value,mixins.PicturePrintMethod):
                    return ext_elems.PictureElement(lh,name,value)
                #~ if isinstance(value,layouts.PropertyGrid):
                    #~ return ext_elems.PropertyGridElement(lh,name,value)
                raise KeyError("Cannot handle value %r in %s.%s." % (value,lh.layout._actor_name,name))
        msg = "Unknown element %r referred in layout %s" % (name,lh)
        #print "[Warning]", msg
        raise KeyError(msg)
        
    #~ def create_button_element(self,name,action,**kw):
        #~ e = self.ui.ButtonElement(self,name,action,**kw)
        #~ self._buttons.append(e)
        #~ return e
          
    def create_meth_element(self,lh,name,meth,**kw):
        rt = getattr(meth,'return_type',None)
        if rt is None:
            rt = models.TextField()
        e = ext_elems.MethodElement(lh,name,meth,rt,**kw)
        assert e.field is not None,"e.field is None for %s.%s" % (lh.layout,name)
        lh._store_fields.append(e.field)
        return e
          
    #~ def create_virt_element(self,name,field,**kw):
        #~ e = self.ui.VirtualFieldElement(self,name,field,**kw)
        #~ return e
        
    #~ def field2elem(self,lh,field,**kw):
        #~ # used also by lino.ui.extjs.ext_elem.MethodElement
        #~ return lh.main_class.field2elem(lh,field,**kw)
        #~ # return self.ui.field2elem(self,field,**kw)
        
    #~ def create_prop_element(self,lh,prop,**kw):
        #~ ...
      
    def create_field_element(self,lh,field,**kw):
        e = lh.main_class.field2elem(lh,field,**kw)
        assert e.field is not None,"e.field is None for %s.%s" % (lh.layout,name)
        lh._store_fields.append(e.field)
        return e
        #return FieldElement(self,field,**kw)
        


    def main_panel_class(self,layout):
        if isinstance(layout,reports.ListLayout) : 
            return ext_elems.GridMainPanel
        #~ if isinstance(layout,layouts.TabLayout) : 
            #~ return ext_elems.TabMainPanel
        if isinstance(layout,reports.DetailLayout) : 
            return ext_elems.DetailMainPanel
        #~ if isinstance(layout,layouts.FormLayout) : 
            #~ return ext_elems.FormMainPanel
        raise Exception("No element class for layout %r" % layout)
            

    
    #~ def save_window_config(self,a,wc):
        #~ self.window_configs[str(a)] = wc
        #~ #a.window_wrapper.config.update(wc=wc)
        #~ a.window_wrapper.update_config(wc)
        #~ f = open(self.window_configs_file,'wb')
        #~ pickle.dump(self.window_configs,f)
        #~ f.close()
        #~ lino.log.debug("save_window_config(%r) -> %s",wc,a)
        #~ self.build_site_js()
        #~ lh = actors.get_actor(name).get_handle(self)
        #~ if lh is not None:
            #~ lh.window_wrapper.try_apply_window_config(wc)
        #~ self._response = None

    #~ def load_window_config(self,action,**kw):
        #~ wc = self.window_configs.get(str(action),None)
        #~ if wc is not None:
            #~ lino.log.debug("load_window_config(%r) -> %s",str(action),wc)
            #~ for n in ('x','y','width','height'):
                #~ if wc.get(n,0) is None:
                    #~ del wc[n]
                    #~ #raise Exception('invalid window configuration %r' % wc)
            #~ kw.update(**wc)
        #~ return kw

  
    def get_urls(self):
        urlpatterns = patterns('',
            (r'^$', self.index_view))
        urlpatterns += patterns('',
            (r'^$', self.index_view),
            (r'^menu$', self.menu_view),
            #~ (r'^list/(?P<app_label>\w+)/(?P<rptname>\w+)$', self.list_report_view),
            (r'^grid_action/(?P<app_label>\w+)/(?P<rptname>\w+)/(?P<grid_action>\w+)$', self.json_report_view),
            #~ (r'^grid_afteredit/(?P<app_label>\w+)/(?P<rptname>\w+)$', self.grid_afteredit_view),
            (r'^submit/(?P<app_label>\w+)/(?P<rptname>\w+)$', self.form_submit_view),
            (r'^grid_config/(?P<app_label>\w+)/(?P<actor>\w+)$', self.grid_config_view),
            (r'^detail_config/(?P<app_label>\w+)/(?P<actor>\w+)$', self.detail_config_view),
            (r'^api/(?P<app_label>\w+)/(?P<actor>\w+)$', self.api_list_view),
            #~ (r'^api/(?P<app_label>\w+)/(?P<actor>\w+)\.(?P<fmt>\w+)$', self.api_list_view),
            #~ (r'^api/(?P<app_label>\w+)/(?P<actor>\w+)/(?P<pk>[-\w]+)\.(?P<fmt>\w+)$', self.api_element_view),
            (r'^api/(?P<app_label>\w+)/(?P<actor>\w+)/(?P<pk>.+)$', self.api_element_view),
            #~ (r'^api/(?P<app_label>\w+)/(?P<actor>\w+)/(?P<pk>\w+)/(?P<method>\w+)$', self.api_element_view),
            #~ (r'^api/(?P<app_label>\w+)/(?P<actor>\w+)/(?P<action>\w+)$', self.api_view),
            #~ (r'^window_configs/(?P<wc_name>.+)$', self.window_configs_view),
            #~ (r'^grid_configs/(?P<wc_name>.+)$', self.window_configs_view),
            #~ (r'^ui/(?P<app_label>\w+)/(?P<actor>\w+)/(?P<action>\w+)$', self.ui_view),
            (r'^choices/(?P<app_label>\w+)/(?P<rptname>\w+)/(?P<fldname>\w+)$', self.choices_view),
        )
        #~ urlpatterns += patterns('',         
            #~ (r'^api/', include('lino.api.urls')),
        
        #~ from django_restapi.model_resource import Collection
        #~ from django_restapi import responder
        #~ from django_restapi.resource import Resource
        
        #~ for a in ('contacts.Persons','contacts.Companies','projects.Projects'):
            #~ rpt = actors.get_actor(a)
            #~ rr = rpt.request(self)
            #~ rsc = Collection(
                #~ queryset = rr.queryset,
                #~ permitted_methods = ('GET', 'POST', 'PUT', 'DELETE'),
                #~ responder = responder.JSONResponder(paginate_by=rr.limit)
            #~ )
            #~ urlpatterns += patterns('',
               #~ url(r'^json/%s/%s/(.*?)/?$' % (rpt.app_label,rpt._actor_name), rsc),
            #~ )

        #~ class MainMenu(Resource):
            #~ def read(self, request):
                #~ return self.menu_view(request)
                
        #~ urlpatterns += patterns('',
           #~ url(r'^menu$' , MainMenu()),
        #~ )
        
        return urlpatterns
        

    def html_page(self,request,on_ready=[],**kw):
        #~ main=ext_elems.ExtPanel(
        main=dict(
          id="main_area",
          xtype='container',
          region="center",
          layout='fit',
          html=self.site.index_html.encode('ascii','xmlcharrefreplace'),
        )
        #~ if not on_ready:
            #~ on_ready = [
              #~ 'new Lino.IndexWrapper({html:%s}).show();' % 
                #~ py2js(self.site.index_html.encode('ascii','xmlcharrefreplace'))]
            #~ main.update(items=dict(layout='fit',html=self.site.index_html.encode('ascii','xmlcharrefreplace')))
        #~ main.update(id='main_area',region='center')
        comps = [
          #~ ext_elems.Toolbar(
          dict(xtype='toolbar',
            items=self.site.get_site_menu(request.user),
            region='north',height=29),
          main,
          #~ jsgen.Component("konsole",
          dict(
            #~ xtype="panel",
            split=True,
            collapsible=True,
            autoScroll=True,
            title=_("Console"),
            id="konsole",
            #~ html=_('Console started'),
            height=100,
            region="south")
        ]  
        yield '<html><head>'
        yield '<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />'
        #~ title = kw.get('title',None)
        #~ if title:
        yield '<title id="title">%s</title>' % self.site.title
        #~ yield '<!-- ** CSS ** -->'
        #~ yield '<!-- base library -->'
        yield '<link rel="stylesheet" type="text/css" href="%sextjs/resources/css/ext-all.css" />' % settings.MEDIA_URL 
        #~ yield '<!-- overrides to base library -->'
        yield '<link rel="stylesheet" type="text/css" href="%sextjs/examples/ux/gridfilters/css/GridFilters.css" />' % settings.MEDIA_URL 
        yield '<link rel="stylesheet" type="text/css" href="%sextjs/examples/ux/gridfilters/css/RangeMenu.css" />' % settings.MEDIA_URL 
        yield '<link rel="stylesheet" type="text/css" href="%slino/extjs/lino.css">' % settings.MEDIA_URL
         
        #~ yield '<!-- ** Javascript ** -->'
        #~ yield '<!-- ExtJS library: base/adapter -->'
        yield '<script type="text/javascript" src="%sextjs/adapter/ext/ext-base.js"></script>' % settings.MEDIA_URL 
        if settings.DEBUG:
            widget_library = 'ext-all-debug'
        else:
            widget_library = 'ext-all'
        #~ yield '<!-- ExtJS library: all widgets -->'
        yield '<script type="text/javascript" src="%sextjs/%s.js"></script>' % (settings.MEDIA_URL, widget_library)
        #~ if True:
            #~ yield '<style type="text/css">'
            #~ # http://stackoverflow.com/questions/2106104/word-wrap-grid-cells-in-ext-js 
            #~ yield '.x-grid3-cell-inner, .x-grid3-hd-inner {'
            #~ yield '  white-space: normal;' # /* changed from nowrap */
            #~ yield '}'
            #~ yield '</style>'
        if False:
            yield '<style type="text/css">'
            #~ yield '.x-item-disabled, .x-tree-node-disabled, .x-date-disabled {'
            yield '.x-item-disabled {'
            yield '  color: blue; opacity:.90;' 
            yield '}'
            yield '</style>'
        if False:
            yield '<script type="text/javascript" src="%sextjs/Exporter-all.js"></script>' % settings.MEDIA_URL 
            
        yield '<script type="text/javascript" src="%sextjs/examples/ux/gridfilters/menu/RangeMenu.js"></script>' % settings.MEDIA_URL
        yield '<script type="text/javascript" src="%sextjs/examples/ux/gridfilters/menu/ListMenu.js"></script>' % settings.MEDIA_URL
        yield '<script type="text/javascript" src="%sextjs/examples/ux/gridfilters/GridFilters.js"></script>' % settings.MEDIA_URL
        yield '<script type="text/javascript" src="%sextjs/examples/ux/gridfilters/filter/Filter.js"></script>' % settings.MEDIA_URL
        yield '<script type="text/javascript" src="%sextjs/examples/ux/gridfilters/filter/StringFilter.js"></script>' % settings.MEDIA_URL
        yield '<script type="text/javascript" src="%sextjs/examples/ux/gridfilters/filter/DateFilter.js"></script>' % settings.MEDIA_URL
        yield '<script type="text/javascript" src="%sextjs/examples/ux/gridfilters/filter/ListFilter.js"></script>' % settings.MEDIA_URL
        yield '<script type="text/javascript" src="%sextjs/examples/ux/gridfilters/filter/NumericFilter.js"></script>' % settings.MEDIA_URL
        yield '<script type="text/javascript" src="%sextjs/examples/ux/gridfilters/filter/BooleanFilter.js"></script>' % settings.MEDIA_URL
             

        #~ yield '<!-- overrides to library -->'
        yield '<script type="text/javascript" src="%slino/extjs/lino.js"></script>' % settings.MEDIA_URL
        yield '<script type="text/javascript" src="%s"></script>' % (
            settings.MEDIA_URL + "/".join(self.site_js_parts()))

        #~ yield '<!-- page specific -->'
        yield '<script type="text/javascript">'

        yield 'Ext.onReady(function(){'
        #~ yield "console.time('onReady');"
        yield "Ext.BLANK_IMAGE_URL = '%sextjs/resources/images/default/s.gif';" % settings.MEDIA_URL
        for ln in jsgen.declare_vars(comps):
            yield '  ' + ln
            
        yield '  var viewport = new Ext.Viewport({layout:"border",items:%s});' % py2js(comps)
        yield '  Ext.QuickTips.init();'
        
        for ln in on_ready:
            yield ln
        
        #~ yield "console.timeEnd('onReady');"
        yield "}); // end of onReady()"
        yield "</script></head><body>"
        #~ yield '<div id="tbar"/>'
        #~ yield '<div id="main"/>'
        #~ yield '<div id="bbar"/>'
        yield '<div id="konsole"></div>'
        yield "</body></html>"
        
            

    def index_view(self, request,**kw):
        #~ from lino.lino_site import lino_site
        #~ kw.update(title=lino_site.title)
        #~ mnu = py2js(lino_site.get_site_menu(request.user))
        #~ print mnu
        #~ tbar=ext_elems.Toolbar(items=lino_site.get_site_menu(request.user),region='north',height=29)# renderTo='tbar')
        return HttpResponse(self.html_page(request,**kw))
        #~ html = '\n'.join(self.html_page(request,main,konsole,**kw))
        #~ return HttpResponse(html)


    def menu_view(self,request):
        from lino.lino_site import lino_site
        #~ from lino import lino_site
        return json_response_kw(success=True,
          message=(_("Welcome on Lino server %(title)r, user %(user)s") % dict(
            title=lino_site.title,
            user=request.user)),
          load_menu=lino_site.get_site_menu(request.user))
        #~ s = py2js(lino_site.get_menu(request))
        #~ return HttpResponse(s, mimetype='text/html')

    def form2obj_and_save(self,ah,data,elem,**kw):
        try:
            ah.store.form2obj(data,elem)
        except exceptions.ValidationError,e:
            return json_response_kw(success=False,msg=unicode(e))
            
        if hasattr(elem,'before_save'): # see :doc:`/blog/2010/0804`
            elem.before_save()
            
        try:
            elem.full_clean()
        except exceptions.ValidationError, e:
            return json_response_kw(success=False,msg="Failed to save %s : %s" % (elem,e))

        try:
            elem.save(**kw)
        except IntegrityError,e:
            #~ print unicode(elem)
            lino.log.exception(e)
            return json_response_kw(success=False,
                  msg=_("There was a problem while saving your data:\n%s") % e)
        return json_response_kw(success=True,
              msg="%s has been saved" % elem)


        
    def detail_config_view(self,request,app_label=None,actor=None):
        rpt = actors.get_actor2(app_label,actor)
        if not rpt.can_config.passes(request.user):
            msg = _("User %(user)s cannot configure %(report)s.") % dict(user=request.user,report=rpt)
            return http.HttpResponseForbidden(msg)
        if request.method == 'GET':
            tab = int(request.GET.get('tab','0'))
            return json_response_kw(success=True,tab=tab,desc=rpt.detail_layouts[tab]._desc)
        if request.method == 'PUT':
            PUT = http.QueryDict(request.raw_post_data)
            tab = int(PUT.get('tab',0))
            desc = PUT.get('desc',None)
            if desc is None:
                return json_response_kw(success=False,msg="desc is mandatory")
            rh = rpt.get_handle(self)
            rh.update_detail(tab,desc)
            self.build_site_js()            
            return json_response_kw(success=True)
            #detail_layout
      
    def grid_config_view(self,request,app_label=None,actor=None):
        rpt = actors.get_actor2(app_label,actor)
        if not rpt.can_config.passes(request.user):
            msg = _("User %(user)s cannot configure %(report)s.") % dict(user=request.user,report=rpt)
            return http.HttpResponseForbidden(msg)
        if request.method == 'PUT':
            PUT = http.QueryDict(request.raw_post_data)
            gc = dict(
              widths=[int(x) for x in PUT.getlist('widths')],
              columns=[str(x) for x in PUT.getlist('columns')],
              hidden_cols=[str(x) for x in PUT.getlist('hidden_cols')],
            )
            
            filter = PUT.get('filter',None)
            if filter is not None:
                filter = json.loads(filter)
                gc['filters'] = [ext_requests.dict2kw(flt) for flt in filter]
            
            name = PUT.get('name',None)
            if name is None:
                name = ext_elems.DEFAULT_GC_NAME                 
            else:
                name = str(name)
                
            gc.update(label=PUT.get('label',name))
            
            rpt.grid_configs[name] = gc
            rpt.save_config()
            self.build_site_js()            
            return json_response_kw(success=True)
            
        raise NotImplementedError
        
        
    def api_list_view(self,request,app_label=None,actor=None):
        """
        - GET : List the members of the collection. 
        - PUT : Replace the entire collection with another collection. 
        - POST : Create a new entry in the collection where the ID is assigned automatically by the collection. 
          The ID created is included as part of the data returned by this operation. 
        - DELETE : Delete the entire collection.
        (Source: http://en.wikipedia.org/wiki/Restful)
        """
        rpt = actors.get_actor2(app_label,actor)
        rh = rpt.get_handle(self)
        
        if not rh.report.can_view.passes(request.user):
            msg = _("User %(user)s cannot view %(report)s.") % dict(user=request.user,report=rpt)
            return http.HttpResponseForbidden()
        if request.method == 'POST':
            """
            Wikipedia:
            Create a new entry in the collection where the ID is assigned automatically by the collection. 
            The ID created is usually included as part of the data returned by this operation. 
            """
            #~ data = rh.store.get_from_form(request.POST)
            #~ instance = ar.create_instance(**data)
            #~ ar = ext_requests.ViewReportRequest(request,rh,rh.report.list_action)
            ar = ext_requests.ViewReportRequest(request,rh,rh.report.default_action)
            instance = ar.create_instance()
            return self.form2obj_and_save(rh,request.POST,instance,force_insert=True)
            
            #~ rh.store.form2obj(request.POST,instance)
            #~ if hasattr(instance,'before_save'): # see :doc:`/blog/2010/0804`
                #~ instance.before_save()
            #~ try:
                #~ instance.full_clean()
            #~ except exceptions.ValidationError, e:
                #~ return json_response_kw(success=False,msg="Failed to save %s : %s" % (instance,e))
            #~ instance.save(force_insert=True)
            #~ return json_response_kw(success=True,msg="%s has been created" % instance)
            
            
        if request.method == 'GET':
            fmt = request.GET.get('fmt',None)
            a = rpt.get_action(fmt)
            if a is not None:
                kw = {}
                if isinstance(a,actions.InsertRow):
                    ar = ext_requests.ViewReportRequest(request,rh,a)
                    elem = ar.create_instance()
                    rec = elem2rec1(request,rh,elem,title=ar.get_title())
                    rec.update(phantom=True)
                    params = dict(data_record=rec)
                    kw.update(on_ready=['Lino.%s(undefined,%s);' % (a,py2js(params))])
                else:
                    kw.update(on_ready=['Lino.%s();' % a])
                return HttpResponse(self.html_page(request,**kw))
                
            ar = ext_requests.ViewReportRequest(request,rh,rh.report.default_action)

            if fmt == 'csv':
                response = HttpResponse(mimetype='text/csv')
                w = ucsv.UnicodeWriter(response)
                names = [] # fld.name for fld in self.fields]
                fields = []
                for col in ar.ah.list_layout._main.column_model.columns:
                    names.append(col.editor.field.name)
                    fields.append(col.editor.field)
                w.writerow(names)
                for row in ar.queryset:
                    values = []
                    for fld in fields:
                        # uh, this is tricky...
                        meth = getattr(fld,'_return_type_for_method',None)
                        if meth is not None:
                            v = meth(row)
                        else:
                            v = fld.value_to_string(row)
                        #lino.log.debug("20100202 %r.%s is %r",row,fld.name,v)
                        values.append(v)
                    w.writerow(values)
                return response
                
            if fmt == 'json':
                rows = [ ar.row2dict(row) for row in ar.queryset ]
                total_count = ar.total_count
                #lino.log.debug('%s.render_to_dict() total_count=%d extra=%d',self,total_count,self.extra)
                # add extra blank row(s):
                #~ for i in range(0,ar.extra):
                if ar.extra:
                    row = ar.create_instance()
                    d = ar.row2dict(row)
                    #~ 20100706 d[rh.report.model._meta.pk.name] = -99999
                    rows.append(d)
                    total_count += 1
                return json_response_kw(count=total_count,rows=rows,title=unicode(ar.get_title()),gc_choices=rpt.grid_configs)


        raise Http404("Method %s not supported for container %s" % (request.method,rh))
    
    
        
        
    def api_element_view(self,request,app_label=None,actor=None,pk=None):
        """
        GET : Retrieve a representation of the addressed member of the collection expressed in an appropriate MIME type.
        PUT : Update the addressed member of the collection or create it with the specified ID. 
        POST : Treats the addressed member as a collection and creates a new subordinate of it. 
        DELETE : Delete the addressed member of the collection. 
        (Source: http://en.wikipedia.org/wiki/Restful)
        """
        rpt = actors.get_actor2(app_label,actor)
        ah = rpt.get_handle(self)
        if not ah.report.can_view.passes(request.user):
            msg = "User %s cannot view %s." % (request.user,ah.report)
            return http.HttpResponseForbidden()
        
        if pk == '-99999':
            ar = ext_requests.ViewReportRequest(request,ah,ah.report.default_action)
            elem = ar.create_instance()
        else:
            try:
                elem = rpt.model.objects.get(pk=pk)
            except rpt.model.DoesNotExist:
                raise Http404("%s %s does not exist." % (rpt,pk))
                
        if request.method == 'DELETE':
            elem.delete()
            return HttpResponseDeleted()
            
        if request.method == 'PUT':
            data = http.QueryDict(request.raw_post_data)
            return self.form2obj_and_save(ah,data,elem,force_update=True)
            
        if request.method == 'GET':
            fmt = request.GET.get('fmt',None)
            datarec = elem2rec_detailed(request,ah,elem)
            if pk == '-99999':
                datarec.update(title=_("Insert into %s...") % ah.report.label)
            if fmt is None or fmt == 'json':
                return json_response(datarec)
            a = rpt.get_action(fmt)
            if a is not None:
                if isinstance(a,actions.OpenWindowAction):
                    params = dict(data_record=datarec)
                    if a.window_wrapper.tabbed:
                        tab = request.GET.get('tab',None)
                        if tab is not None: 
                            tab = int(tab)
                            params.update(active_tab=tab)
                    return HttpResponse(self.html_page(request,on_ready=['Lino.%s(undefined,%s);' % (a,py2js(params))]))
                    
                if isinstance(a,actions.RedirectAction):
                    target = a.get_target_url(elem)
                    if target is None:
                        raise Http404("%s could not build %r" % (a,elem))
                    return http.HttpResponseRedirect(target)
                  
                raise NotImplementedError("Action %s is not implemented)" % a)
                
            raise Http404("%s has no action %r" % (ah.report,fmt))
              
        raise Http404("Method %r not supported for elements of %s" % (request.method,ah.report))
        
        
        
    def site_js_parts(self):
    #~ def js_cache_name(self):
        return ('cache','js','site.js')
        
    def build_site_js(self):
        #~ for app_label in site.
        fn = os.path.join(settings.MEDIA_ROOT,*self.site_js_parts()) 
        #~ fn = r'c:\temp\dsbe.js'
        lino.log.info("Generating %s ...", fn)
        f = open(fn,'w')
        f.write("""
        // site.js --- 
        // Don't edit. This file is generated at each server start.
        """)
        f.write("""
        LANGUAGE_CHOICES = %s;
        """ % py2js(list(LANGUAGE_CHOICES)))
        for rpt in reports.master_reports + reports.slave_reports:
            f.write("Ext.namespace('Lino.%s')\n" % rpt)
            for a in rpt.get_actions():
                if a.window_wrapper is not None:
                    #~ print a, "..."
                    f.write('Lino.%s = ' % a )
                    for ln in a.window_wrapper.js_render():
                        f.write(ln + "\n")
                    f.write("\n")
        f.close()
          
        
        
    def choices_view(self,request,app_label=None,rptname=None,fldname=None,**kw):
        rpt = actors.get_actor2(app_label,rptname)
        rh = rpt.get_handle(self)
        field = rpt.model._meta.get_field(fldname)
        chooser = choosers.get_for_field(field)
        if chooser:
            qs = chooser.get_request_choices(request)
            assert qs is not None, "%s.%s_choices() returned None" % (rpt.model,fldname)
        elif field.choices:
            qs = field.choices
        elif isinstance(field,models.ForeignKey):
            qs = field.rel.to.objects.all()
        else:
            raise Http404("No choices for %s" % fldname)
        #~ for k,v in request.GET.items():
            #~ kw[str(k)] = v
        #~ chooser = rh.choosers[fldname]
        #~ qs = chooser.get_choices(**kw)
        quick_search = request.GET.get(ext_requests.URL_PARAM_FILTER,None)
        if quick_search is not None:
            qs = reports.add_quick_search_filter(qs,quick_search)
        if isinstance(field,models.ForeignKey):
            def row2dict(obj,d):
                d[ext_requests.CHOICES_TEXT_FIELD] = unicode(obj)
                d[ext_requests.CHOICES_VALUE_FIELD] = obj.pk # getattr(obj,'pk')
                return d
        elif chooser:
            if chooser.simple_values:
                def row2dict(obj,d):
                    #~ d[ext_requests.CHOICES_TEXT_FIELD] = unicode(obj)
                    d[ext_requests.CHOICES_VALUE_FIELD] = unicode(obj)
                    return d
            else:
                def row2dict(obj,d):
                    d[ext_requests.CHOICES_TEXT_FIELD] = unicode(obj[1])
                    d[ext_requests.CHOICES_VALUE_FIELD] = obj[0]
                    return d
        else:
            def row2dict(obj,d):
                if type(obj) is list or type(obj) is tuple:
                    d[ext_requests.CHOICES_TEXT_FIELD] = unicode(obj[1])
                    d[ext_requests.CHOICES_VALUE_FIELD] = obj[0]
                else:
                    d[ext_requests.CHOICES_TEXT_FIELD] = unicode(obj)
                    d[ext_requests.CHOICES_VALUE_FIELD] = unicode(obj)
                return d
        rows = [ row2dict(row,{}) for row in qs ]
        return json_response_kw(count=len(rows),rows=rows,title=_('Choices for %s') % fldname)
        

    def form_submit_view(self,request,**kw):
        kw['submit'] = True
        return self.json_report_view(request,**kw)

    def list_report_view(self,request,**kw):
        #kw['simple_list'] = True
        return self.json_report_view(request,**kw)
        
    #~ def csv_report_view(self,request,**kw):
        #~ kw['csv'] = True
        #~ return self.json_report_view(request,**kw)
        
    def json_report_view(self,request,app_label=None,rptname=None,**kw):
        rpt = actors.get_actor2(app_label,rptname)
        return self.json_report_view_(request,rpt,**kw)

    def json_report_view_(self,request,rpt,grid_action=None,colname=None,submit=None,choices_for_field=None,csv=False):
        if not rpt.can_view.passes(request):
            msg = "User %s cannot view %s." % (request.user,rpt)
            raise Http404(msg)
            #~ return json_response_kw(success=False,msg=msg)
                
        rh = rpt.get_handle(self)
        
        if grid_action:
            a = rpt.get_action(grid_action)
            assert a is not None, "No action %s in %s" % (grid_action,rh)
            ar = ext_requests.ViewReportRequest(request,rh,a)
            return json_response(ar.run())
            #~ return json_response(ar.run().as_dict())
                
        if choices_for_field:
            rptreq = ext_requests.ChoicesReportRequest(request,rh,choices_for_field)
        elif csv:
            rptreq = ext_requests.CSVReportRequest(request,rh,rpt.default_action)
            return rptreq.render_to_csv()
        else:
            rptreq = ext_requests.ViewReportRequest(request,rh,rpt.default_action)
            if submit:
                pk = request.POST.get(rh.store.pk.name) #,None)
                #~ if pk == reports.UNDEFINED:
                    #~ pk = None
                try:
                    data = rh.store.get_from_form(request.POST)
                    if pk in ('', None):
                        #return json_response(success=False,msg="No primary key was specified")
                        instance = rptreq.create_instance(**data)
                        instance.save(force_insert=True)
                    else:
                        instance = rpt.model.objects.get(pk=pk)
                        for k,v in data.items():
                            setattr(instance,k,v)
                        instance.save(force_update=True)
                    return json_response_kw(success=True,
                          msg="%s has been saved" % instance)
                except Exception,e:
                    lino.log.exception(e)
                    #traceback.format_exc(e)
                    return json_response_kw(success=False,msg="Exception occured: "+cgi.escape(str(e)))
        # otherwise it's a simple list:
        #~ print 20100406, rptreq
        d = rptreq.render_to_dict()
        return json_response(d)
        

        
    #~ def get_actor_url(self,actor,action_name,**kw):
        #~ return build_url("/api",actor.app_label,actor._actor_name,action_name,**kw)

    def get_actor_url(self,actor,**kw):
        return self.build_url("api",actor.app_label,actor._actor_name,**kw)

    def unused_get_form_action_url(self,fh,action,**kw):
        #~ a = btn.lh.datalink.actor
        #~ a = action.actor
        return self.build_url("form",fh.layout.app_label,fh.layout._actor_name,action.name,**kw)
        
    def get_choices_url(self,fke,**kw):
        return self.build_url("choices",
            fke.lh.rh.report.app_label,
            fke.lh.rh.report._actor_name,
            fke.field.name,**kw)
        
    def get_report_url(self,rh,master_instance=None,
            submit=False,grid_afteredit=False,grid_action=None,run=False,csv=False,**kw):
        #~ lino.log.debug("get_report_url(%s)", [rh.name,master_instance,
            #~ simple_list,submit,grid_afteredit,action,kw])
        if grid_afteredit:
            url = "/grid_afteredit/"
        elif submit:
            url = "/submit/"
        elif grid_action:
            url = "/grid_action/"
        elif run:
            url = "/action/"
        elif csv:
            url = "/csv/"
        else:
            url = "/list/"
        url += rh.report.app_label + "/" + rh.report._actor_name
        if grid_action:
            url += "/" + grid_action
        if master_instance is not None:
            kw[ext_requests.URL_PARAM_MASTER_PK] = master_instance.pk
            mt = ContentType.objects.get_for_model(master_instance.__class__).pk
            kw[ext_requests.URL_PARAM_MASTER_TYPE] = mt
        if len(kw):
            url += "?" + urlencode(kw)
        return url
        
        
        
    #~ def show_report(self,ar,rh,**kw):
        #~ ar.show_window(rh.window_wrapper.js_render)

    #~ def show_detail(self,ar):
        #~ ar.show_window(ar.action.window_wrapper.js_render)

    #~ def show_action_window(self,ar,action):
        #~ ar.response.update(js_code = action.window_wrapper.js_render)
        #~ ar.show_window(action.window_wrapper.js_render)

    #~ def show_properties(self,ar,**kw):
        #~ ar.show_window(ar.rh.properties.window_wrapper.js_render)
        
        
    #~ def view_form(self,dlg,**kw):
        #~ "called from ViewForm.run_in_dlg()"
        #~ frm = dlg.actor
        #~ fh = self.get_form_handle(frm)
        #~ yield dlg.show_window(fh.window_wrapper.js_render).over()
        
        
    def py2js_converter(self,v):
        if v is LANGUAGE_CHOICES:
            return js_code('LANGUAGE_CHOICES')
        if isinstance(v,menus.Menu):
            if v.parent is None:
                return v.items
                #kw.update(region='north',height=27,items=v.items)
                #return py2js(kw)
            return dict(text=prepare_label(v),menu=dict(items=v.items))
        if isinstance(v,menus.MenuItem):
            #~ handler = "function(btn,evt){Lino.do_action(undefined,%r,%r,{})}" % (v.actor.get_url(lino_site.ui),id2js(v.actor.actor_id))
            #~ url = build_url("/ui",v.action.actor.app_label,v.action.actor._actor_name,v.action.name)
            #~ handler = "function(btn,evt){Lino.do_action(undefined,{url:%r})}" % url
            #~ handler = "function(btn,evt){new Lino.%s().show()}" % v.action
            handler = "function(btn,evt){Lino.%s(undefined,%s)}" % (v.action,py2js(v.params))
            return dict(text=prepare_label(v),handler=js_code(handler))
        return v


    def get_action_url(self,action,fmt=None,**kw):
        #~ if isinstance(action,properties.PropertiesAction):
            #~ action = properties.PropValuesByOwner().default_action
        #~ if isinstance(action,reports.SlaveGridAction):
            #~ action = action.slave.default_action
            #~ return build_url("/api",action.actor.app_label,action.actor._actor_name,action.name,**kw)
        if fmt:
            name = action.name+'.'+fmt
        else:
            name = action.name
        return self.build_url("api",action.actor.app_label,action.actor._actor_name,name,**kw)
        #~ url = "/action/" + a.app_label + "/" + a._actor_name 
        #~ if len(kw):
            #~ url += "?" + urlencode(kw)
        #~ return url
        
        
        
        
    def action_window_wrapper(self,a,h):
        if isinstance(a,PrintAction): return ext_windows.DownloadRenderer(self,a)
        if isinstance(a,actions.DeleteSelected): return ext_windows.DeleteRenderer(self,a)
          
        if isinstance(a,actions.GridEdit):
            return ext_windows.GridMasterWrapper(h,a)
            
        if isinstance(a,actions.InsertRow):
            return ext_windows.InsertWrapper(h,a)
            
        if isinstance(a,actions.ShowDetailAction):
            return ext_windows.DetailWrapper(h,a)

        
        
        
    def setup_handle(self,h):
        #~ if isinstance(h,layouts.TabPanelHandle):
            #~ h._main = ext_elems.TabPanel([l.get_handle(self) for l in h.layouts])
          
        if isinstance(h,reports.ReportHandle):
            lino.log.debug('ExtUI.setup_handle() %s',h.report)
            #~ h.choosers = chooser.get_choosers_for_model(h.report.model,chooser.FormChooser)
            #~ h.report.add_action(ext_windows.SaveWindowConfig(h.report))
            h.store = ext_store.Store(h)
                    
            for a in h.get_actions():
                a.window_wrapper = self.action_window_wrapper(a,h)
            
    def source_dir(self):
        return os.path.abspath(os.path.dirname(__file__))
        
    def a2btn(self,a,**kw):
        if isinstance(a,actions.SubmitDetail):
            kw.update(panel_btn_handler=js_code('Lino.submit_detail'))
        elif isinstance(a,actions.SubmitInsert):
            kw.update(panel_btn_handler=js_code('Lino.submit_insert'))
        elif isinstance(a,actions.ShowDetailAction):
            kw.update(panel_btn_handler=js_code('Lino.show_detail_handler(Lino.%s)' % a))
        elif isinstance(a,actions.InsertRow):
            kw.update(panel_btn_handler=js_code("Lino.show_insert_handler(Lino.%s)" % a))
        else:
            kw.update(panel_btn_handler=js_code("Lino.%s" % a))
        kw.update(
          text=unicode(a.label),
        )
        return kw
        
#~ ui = ExtUI()

#~ jsgen.register_converter(ui.py2js_converter)
