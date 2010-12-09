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

import logging
logger = logging.getLogger(__name__)

import os
import cgi
import time
#import traceback
import cPickle as pickle
from urllib import urlencode

#~ import Cheetah
from Cheetah.Template import Template as CheetahTemplate

from django import http
from django.db import models
from django.db import IntegrityError
from django.conf import settings
from django.http import HttpResponse, Http404
from django import http
from django.core import exceptions
from django.utils import functional
from django.utils.encoding import force_unicode 

from django.template.loader import get_template
from django.template import RequestContext

from django.utils.translation import ugettext as _
from django.utils import simplejson as json

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.conf.urls.defaults import patterns, url, include


import lino
from . import ext_elems
from . import ext_store
from . import ext_windows
#~ from . import ext_viewport
from . import ext_requests
from lino import actions #, layouts #, commands
from lino import reports
from lino import fields
from lino.ui import base
from lino.core import actors
from lino.utils import dblogger
from lino.utils import ucsv
from lino.utils import choosers
from lino.utils import menus
from lino.utils.config import find_config_file
from lino.utils import jsgen
from lino.utils.jsgen import py2js, js_code, id2js
from lino.mixins import printable

from lino.core.coretools import app_labels

from lino.fields import LANGUAGE_CHOICES
from lino.tools import obj2str

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
        
#~ def element_name(elem):
    #~ return u"%s (#%s in %s.%s)" % (elem,elem.pk,elem._meta.app_label,elem.__class__.__name__)


def parse_bool(s):
    return s == 'true'
    
def parse_int(s,default=None):
    if s is None: return None
    return int(s)

def json_response_kw(msg=None,**kw):
    if msg:
        kw.update(message=msg)
    return json_response(kw)
    
def json_response(x):
    #s = simplejson.dumps(kw,default=unicode)
    #return HttpResponse(s, mimetype='text/html')
    s = py2js(x)
    #~ logger.debug("json_response() -> %r", s)
    # http://dev.sencha.com/deploy/dev/docs/source/BasicForm.html#cfg-Ext.form.BasicForm-fileUpload
    return HttpResponse(s, content_type='text/html')
    return HttpResponse(s, content_type='text/json')
    #~ r = HttpResponse(s, content_type='application/json')
    # see also http://stackoverflow.com/questions/477816/the-right-json-content-type
    #~ return r
    #~ return HttpResponse(s, mimetype='text/html')
    
def error_response(e,message_prefix='',**kw):
    kw.update(success=False)
    if hasattr(e, 'message_dict'):
        kw.update(errors=e.message_dict)
    kw.update(message=message_prefix+unicode(e))
    return json_response(kw)
    

def elem2rec1(ar,rh,elem,**rec):
    rec.update(data=rh.store.row2dict(ar,elem))
    return rec


def elem2rec_detailed(ar,rh,elem,**rec):
    """
    Adds additional information for this record, used only by detail views.
    
    The "navigation information" is a set of pointers to the next, previous, 
    first and last record relativ to this record in this report. 
    (This information can be relatively expensive for records that are towards 
    the end of the report. 
    See :doc:`/blog/2010/0716`,
    :doc:`/blog/2010/0721`,
    :doc:`/blog/2010/1116`,
    :doc:`/blog/2010/1207`.)
    
    recno 0 means "the requested element exists but is not contained in the requested queryset".
    This can happen after changing the quick filter (search_change) of a detail view.
    
    """
    rec = elem2rec1(ar,rh,elem,**rec)
    rec.update(id=elem.pk)
    rec.update(title=unicode(elem))
    if rh.report.disable_delete:
        rec.update(disable_delete=rh.report.disable_delete(ar.request,elem))
    if rh.report.show_prev_next:
        first = None
        prev = None
        next = None
        last = None
        #~ ar = ext_requests.ViewReportRequest(request,rh,rh.report.default_action)
        recno = 0
        if ar.total_count > 0:
            if True:
                # this algorithm is clearly quicker on reports with a few thousand Persons
                id_list = list(ar.queryset.values_list('pk',flat=True))
                assert len(id_list) == ar.total_count, \
                    "len(id_list) is %d while ar.total_count is %d" % (len(id_list),ar.total_count)
                first = id_list[0]
                last = id_list[-1]
                try:
                    i = id_list.index(elem.pk)
                except ValueError:
                    pass
                else:
                    recno = i + 1
                    if i > 0:
                        #~ prev = ar.queryset[i-1]
                        prev = id_list[i-1]
                    if i < ar.total_count - 1:
                        #~ next = ar.queryset[i+1]
                        next = id_list[i+1]
            else:
                first = ar.queryset[0]
                last = ar.queryset.reverse()[0]
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
                            index,next = g.next()
                            break
                except StopIteration:
                    pass
                if first is not None: first = first.pk
                if last is not None: last = last.pk
                if prev is not None: prev = prev.pk
                if next is not None: next = next.pk
        rec.update(navinfo=dict(
            first=first,prev=prev,next=next,last=last,recno=recno,
            message=_("Row %(rowid)d of %(rowcount)d") % dict(rowid=recno,rowcount=ar.total_count)))
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
            #~ logger.info("Loading %s...",self.window_configs_file)
            #~ wc = pickle.load(open(self.window_configs_file,"rU"))
            #~ #logger.debug("  -> %r",wc)
            #~ if type(wc) is dict:
                #~ self.window_configs = wc
        #~ else:
            #~ logger.warning("window_configs_file %s not found",self.window_configs_file)
            
        base.UI.__init__(self,site) # will create a.window_wrapper for all actions
        
        #~ self.welcome_template = get_template('welcome.html')
        
        #~ from django.template.loader import find_template
        #~ source, origin = find_template('welcome.html')
        #~ print source, origin
        
        fn = find_config_file('welcome.html')
        self.welcome_template = CheetahTemplate(file(fn).read())
        
        self.build_site_js()
        
    def create_layout_element(self,lh,panelclass,name,**kw):
        
        if name == "_":
            return ext_elems.Spacer(lh,name,**kw)
            
        de = lh.rh.report.get_data_elem(name)
        #~ de = reports.get_data_elem(lh.layout.datalink,name)
        
        if de is None:
            a = lh.rh.report.get_action(name)
            if isinstance(a,actions.ImageAction):
                return ext_elems.PictureElement(lh,name,a,**kw)
          
        #~ if isinstance(de,properties.Property):
            #~ return self.create_prop_element(lh,de,**kw)
        if isinstance(de,models.Field):
            return self.create_field_element(lh,de,**kw)
        if isinstance(de,generic.GenericForeignKey):
            # create a horizontal panel with 2 comboboxes
            return lh.desc2elem(panelclass,name,de.ct_field + ' ' + de.fk_field,**kw)
            #~ return ext_elems.VirtualFieldElement(lh,name,de,**kw)
        if isinstance(de,reports.Report):
            if isinstance(lh.layout,reports.DetailLayout):
                kw.update(tools=[
                  js_code("Lino.report_window_button(ww,Lino.%s)" % de.default_action)
                ])
                if de.show_slave_grid:
                    e = ext_elems.SlaveGridElement(lh,name,de,**kw)
                    #~ e = ext_elems.GridElement(lh,name,de.get_handle(self),**kw)
                    #~ lh.slave_grids.append(e)
                    return e
                    #~ return ext_elems.GridElementBox(lh,e)
                else:
                    o = dict(drop_zone="FooBar")
                    a = de.get_action('insert')
                    if a is not None:
                        kw.update(ls_bbar_actions=[
                        #~ o.update(bbar=[
                          self.a2btn(a),
                          #~ dict(text="Add",panel_btn_handler=js_code("Lino.show_insert_handler(Lino.%s)" % a))
                          ])
                    field = fields.HtmlBox(verbose_name=de.label,**o)
                    field.name = de._actor_name
                    field._return_type_for_method = de.slave_as_summary_meth(self,'<br>')
                    lh.add_store_field(field)
                    e = ext_elems.HtmlBoxElement(lh,field,**kw)
                    return e
            else:
                #~ field = fields.TextField(verbose_name=de.label)
                field = fields.HtmlBox(verbose_name=de.label)
                field.name = de._actor_name
                field._return_type_for_method = de.slave_as_summary_meth(self,', ')
                lh.add_store_field(field)
                e = ext_elems.HtmlBoxElement(lh,field,**kw)
                return e
        if callable(de):
            rt = getattr(de,'return_type',None)
            if rt is not None:
                return self.create_meth_element(lh,name,de,rt,**kw)
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
                if isinstance(value,printable.PicturePrintMethod):
                    return ext_elems.PictureElement(lh,name,value)
                #~ if isinstance(value,layouts.PropertyGrid):
                    #~ return ext_elems.PropertyGridElement(lh,name,value)
                raise KeyError("Cannot handle value %r in %s.%s." % (value,lh.layout._actor_name,name))
        msg = "Unknown element %r referred in layout %s" % (name,lh.layout)
        #print "[Warning]", msg
        raise KeyError(msg)
        
    def href_to(self,obj):
        return '<a href="%s" target="_blank">%s</a>' % (self.get_detail_url(obj,fmt='detail'),unicode(obj))

    #~ def create_button_element(self,name,action,**kw):
        #~ e = self.ui.ButtonElement(self,name,action,**kw)
        #~ self._buttons.append(e)
        #~ return e
        
    def create_meth_element(self,lh,name,meth,rt,**kw):
        rt.name = name
        rt._return_type_for_method = meth
        #~ kw.update(editable=False)
        e = self.create_field_element(lh,rt,**kw)
        #~ if lh.rh.report.actor_id == 'contacts.Persons':
            #~ print 'ext_ui.py create_meth_element',name,'-->',e
        return e
        #~ e = lh.main_class.field2elem(lh,return_type,**kw)
        #~ assert e.field is not None,"e.field is None for %s.%s" % (lh.layout,name)
        #~ lh._store_fields.append(e.field)
        #~ return e
            
        #~ if rt is None:
            #~ rt = models.TextField()
            
        #~ e = ext_elems.MethodElement(lh,name,meth,rt,**kw)
        #~ assert e.field is not None,"e.field is None for %s.%s" % (lh.layout,name)
        #~ lh._store_fields.append(e.field)
        #~ return e
          
    def create_field_element(self,lh,field,**kw):
        e = lh.main_class.field2elem(lh,field,**kw)
        assert e.field is not None,"e.field is None for %s.%s" % (lh.layout,name)
        lh.add_store_field(e.field)
          #~ lh._store_fields.append(e.field)
        return e
        #return FieldElement(self,field,**kw)
        
    #~ def create_virt_element(self,name,field,**kw):
        #~ e = self.ui.VirtualFieldElement(self,name,field,**kw)
        #~ return e
        
    #~ def field2elem(self,lh,field,**kw):
        #~ # used also by lino.ui.extjs.ext_elem.MethodElement
        #~ return lh.main_class.field2elem(lh,field,**kw)
        #~ # return self.ui.field2elem(self,field,**kw)
        
    #~ def create_prop_element(self,lh,prop,**kw):
        #~ ...
      


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
        #~ logger.debug("save_window_config(%r) -> %s",wc,a)
        #~ self.build_site_js()
        #~ lh = actors.get_actor(name).get_handle(self)
        #~ if lh is not None:
            #~ lh.window_wrapper.try_apply_window_config(wc)
        #~ self._response = None

    #~ def load_window_config(self,action,**kw):
        #~ wc = self.window_configs.get(str(action),None)
        #~ if wc is not None:
            #~ logger.debug("load_window_config(%r) -> %s",str(action),wc)
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
        #~ c = RequestContext(request,dict(site=self.site,lino=lino))
        self.welcome_template.ui = self
        self.welcome_template.user = request.user
        self.welcome_template.site = self.site
        self.welcome_template.lino = lino
        #~ main=ext_elems.ExtPanel(
        main=dict(
          id="main_area",
          xtype='container',
          region="center",
          layout='fit',
          #~ html=self.welcome_template.render(c),
          html=unicode(self.welcome_template),
          #~ html=self.site.index_html.encode('ascii','xmlcharrefreplace'),
        )
        #~ if not on_ready:
            #~ on_ready = [
              #~ 'new Lino.IndexWrapper({html:%s}).show();' % 
                #~ py2js(self.site.index_html.encode('ascii','xmlcharrefreplace'))]
            #~ main.update(items=dict(layout='fit',html=self.site.index_html.encode('ascii','xmlcharrefreplace')))
        #~ main.update(id='main_area',region='center')
        yield '<html><head>'
        yield '<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />'
        #~ title = kw.get('title',None)
        #~ if title:
        yield '<title id="title">%s</title>' % self.site.title
        #~ yield '<!-- ** CSS ** -->'
        #~ yield '<!-- base library -->'
        yield '<link rel="stylesheet" type="text/css" href="%sextjs/resources/css/ext-all.css" />' % settings.MEDIA_URL 
        #~ yield '<!-- overrides to base library -->'
        if settings.USE_GRIDFILTERS:
            #~ yield '<link rel="stylesheet" type="text/css" href="%sextjs/examples/ux/css/RowEditor.css" />' % settings.MEDIA_URL 
            yield '<link rel="stylesheet" type="text/css" href="%sextjs/examples/ux/statusbar/css/statusbar.css" />' % settings.MEDIA_URL 
            yield '<link rel="stylesheet" type="text/css" href="%sextjs/examples/ux/gridfilters/css/GridFilters.css" />' % settings.MEDIA_URL 
            yield '<link rel="stylesheet" type="text/css" href="%sextjs/examples/ux/gridfilters/css/RangeMenu.css" />' % settings.MEDIA_URL 
            
        yield '<link rel="stylesheet" type="text/css" href="%sextjs/examples/ux/fileuploadfield/css/fileuploadfield.css" />' % settings.MEDIA_URL 
        
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

        if settings.USE_GRIDFILTERS:
            #~ yield '<script type="text/javascript" src="%sextjs/examples/ux/RowEditor.js"></script>' % settings.MEDIA_URL
            yield '<script type="text/javascript" src="%sextjs/examples/ux/statusbar/StatusBar.js"></script>' % settings.MEDIA_URL
            yield '<script type="text/javascript" src="%sextjs/examples/ux/gridfilters/menu/RangeMenu.js"></script>' % settings.MEDIA_URL
            yield '<script type="text/javascript" src="%sextjs/examples/ux/gridfilters/menu/ListMenu.js"></script>' % settings.MEDIA_URL
            yield '<script type="text/javascript" src="%sextjs/examples/ux/gridfilters/GridFilters.js"></script>' % settings.MEDIA_URL
            yield '<script type="text/javascript" src="%sextjs/examples/ux/gridfilters/filter/Filter.js"></script>' % settings.MEDIA_URL
            yield '<script type="text/javascript" src="%sextjs/examples/ux/gridfilters/filter/StringFilter.js"></script>' % settings.MEDIA_URL
            yield '<script type="text/javascript" src="%sextjs/examples/ux/gridfilters/filter/DateFilter.js"></script>' % settings.MEDIA_URL
            yield '<script type="text/javascript" src="%sextjs/examples/ux/gridfilters/filter/ListFilter.js"></script>' % settings.MEDIA_URL
            yield '<script type="text/javascript" src="%sextjs/examples/ux/gridfilters/filter/NumericFilter.js"></script>' % settings.MEDIA_URL
            yield '<script type="text/javascript" src="%sextjs/examples/ux/gridfilters/filter/BooleanFilter.js"></script>' % settings.MEDIA_URL
            
        yield '<script type="text/javascript" src="%sextjs/examples/ux/fileuploadfield/FileUploadField.js"></script>' % settings.MEDIA_URL

        #~ yield '<!-- overrides to library -->'
        yield '<script type="text/javascript" src="%slino/extjs/lino.js"></script>' % settings.MEDIA_URL
        yield '<script type="text/javascript" src="%s"></script>' % (
            settings.MEDIA_URL + "/".join(self.site_js_parts()))

        #~ yield '<!-- page specific -->'
        yield '<script type="text/javascript">'

        yield 'Ext.onReady(function(){'
        #~ yield "console.time('onReady');"
        
        #~ yield "Lino.load_mask = new Ext.LoadMask(Ext.getBody(), {msg:'Immer mit der Ruhe...'});"
          
        if True:
            
            win = dict(
              layout='fit',
              #~ maximized=True,
              items=main,
              #~ closable=False,
              bbar=dict(xtype='toolbar',items=js_code('Lino.status_bar')),
              #~ title=self.site.title,
              tbar=self.site.get_site_menu(request.user),
            )
            
            for ln in jsgen.declare_vars(win):
                yield ln
            yield '  new Ext.Viewport({layout:"fit",items:%s}).render("body");' % py2js(win)
        else:
          
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
                collapsed=True,
                autoScroll=True,
                title=_("Console"),
                id="konsole",
                #~ html=_('Console started'),
                height=100,
                region="south")
            ]  
            for ln in jsgen.declare_vars(comps):
                yield '  ' + ln
            yield '  var viewport = new Ext.Viewport({layout:"border",items:%s});' % py2js(comps)
            
        yield '  Ext.QuickTips.init();'
        
        for ln in on_ready:
            yield ln
        
        #~ yield "console.timeEnd('onReady');"
        yield "}); // end of onReady()"
        yield '</script></head><body id="body">'
        #~ yield '<div id="tbar"/>'
        #~ yield '<div id="main"/>'
        #~ yield '<div id="bbar"/>'
        #~ yield '<div id="konsole"></div>'
        yield "</body></html>"
        
    def site_js_lines(self):
        yield """// site.js --- generated %s by Lino version %s.""" % (time.ctime(),lino.__version__)
        yield "Ext.BLANK_IMAGE_URL = '%sextjs/resources/images/default/s.gif';" % settings.MEDIA_URL
        yield "LANGUAGE_CHOICES = %s;" % py2js(list(LANGUAGE_CHOICES))
        yield "MEDIA_URL = %r;" % settings.MEDIA_URL
        yield "Lino.status_bar = new Ext.ux.StatusBar({defaultText:'Lino version %s.'});" % lino.__version__
        
            

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

    def form2obj_and_save(self,request,rh,data,elem,is_new): # **kw2save):
        #~ logger.debug('form2obj_and_save %r', data)
        
        # store normal form data (POST or PUT)
        try:
            rh.store.form2obj(data,elem)
        except exceptions.ValidationError,e:
           return error_response(e)
           #~ return error_response(e,_("There was a problem while validating your data : "))
        
        if not is_new:
            dblogger.log_changes(request,elem)
            
        if hasattr(elem,'before_save'): # see :doc:`/blog/2010/0804`
            elem.before_save()
        #~ print '20101024a', elem.card_valid_from
        try:
            elem.full_clean()
        except exceptions.ValidationError, e:
            return error_response(e) #,_("There was a problem while validating your data : "))
            #~ return json_response_kw(success=False,msg="Failed to save %s : %s" % (elem,e))
            
        #~ print '20101024b', elem.card_valid_from

        kw2save = {}
        #~ kw2resp = {}
        if is_new:
            kw2save.update(force_insert=True)
            #~ kw2resp.update(close=True)
        else:
            kw2save.update(force_update=True)
            #~ kw2resp.update(refresh=True)
            
        try:
            elem.save(**kw2save)
        except IntegrityError,e:
            #~ print unicode(elem)
            #~ logger.exception(e)
            return error_response(e) # ,_("There was a problem while saving your data : "))
            #~ return json_response_kw(success=False,
                  #~ msg=_("There was a problem while saving your data:\n%s") % e)
        
        if is_new:
            dblogger.log_created(request,elem)
            
        return self.success_response(_("%s has been saved.") % obj2str(elem))
        #~ return self.success_response(_("%s has been saved.") % obj2str(elem),**kw2resp)


        
    def detail_config_view(self,request,app_label=None,actor=None):
        rpt = actors.get_actor2(app_label,actor)
        if not rpt.can_config.passes(request.user):
            msg = _("User %(user)s cannot configure %(report)s.") % dict(user=request.user,report=rpt)
            return http.HttpResponseForbidden(msg)
        if request.method == 'GET':
            tab = int(request.GET.get('tab','0'))
            return json_response_kw(success=True,tab=tab,desc=rpt.model._lino_detail_layouts[tab]._desc)
        if request.method == 'PUT':
            PUT = http.QueryDict(request.raw_post_data)
            tab = int(PUT.get('tab',0))
            desc = PUT.get('desc',None)
            if desc is None:
                return json_response_kw(success=False,message="desc is mandatory")
            rh = rpt.get_handle(self)
            try:
                rh.update_detail(tab,desc)
            except Exception,e:
                return json_response_kw(success=False,message=unicode(e))
            self.build_site_js()
            return json_response_kw(success=True)
            #detail_layout
      
    def grid_config_view(self,request,app_label=None,actor=None):
        rpt = actors.get_actor2(app_label,actor)
        if not rpt.can_config.passes(request.user):
            msg = _("User %(user)s cannot configure %(report)s.") % dict(user=request.user,report=rpt)
            return error_response(msg)
            #~ return http.HttpResponseForbidden(msg)
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
            msg = rpt.save_config()
            self.build_site_js()            
            return self.success_response(msg)
            #~ return json_response_kw(success=True)
            
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
        
        #~ if not rh.report.can_view.passes(request.user):
            #~ msg = _("User %(user)s cannot view %(report)s.") % dict(user=request.user,report=rpt)
            #~ return http.HttpResponseForbidden()
        if request.method == 'POST':
            #~ data = rh.store.get_from_form(request.POST)
            #~ instance = ar.create_instance(**data)
            #~ ar = ext_requests.ViewReportRequest(request,rh,rh.report.list_action)
            ar = ext_requests.ViewReportRequest(request,rh,rh.report.default_action)
            instance = ar.create_instance()
            # store uploaded files. 
            # html forms cannot send files with PUT or GET, only with POST
            if rh.report.handle_uploaded_files is not None:
                rh.report.handle_uploaded_files(request,instance)
            return self.form2obj_and_save(request,rh,request.POST,instance,True)
            
        if request.method == 'GET':
            fmt = request.GET.get('fmt',None)
            a = rpt.get_action(fmt)
            if a is not None:
                kw = {}
                ar = ext_requests.ViewReportRequest(request,rh,a)
                params = dict(base_params=self.request2kw(ar))

                if isinstance(a,actions.InsertRow):
                    elem = ar.create_instance()
                    rec = elem2rec1(ar,rh,elem,title=ar.get_title())
                    rec.update(phantom=True)
                    params.update(data_record=rec)

                kw.update(on_ready=['Lino.%s(undefined,%s);' % (a,py2js(params))])
                #~ print '20101024 on_ready', params
                return HttpResponse(self.html_page(request,**kw))
                
            ar = ext_requests.ViewReportRequest(request,rh,rh.report.default_action)

            if fmt == 'csv':
                response = HttpResponse(mimetype='text/csv')
                response['Content-Disposition'] = 'attachment; filename=tmp.csv'
                w = ucsv.UnicodeWriter(response)
                names = [] # fld.name for fld in self.fields]
                fields = []
                for e in ar.ah.list_layout._main.columns:
                #~ for col in ar.ah.list_layout._main.column_model.columns:
                    names.append(e.field.name)
                    fields.append(e.field)
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
                        #logger.debug("20100202 %r.%s is %r",row,fld.name,v)
                        values.append(v)
                    w.writerow(values)
                return response
                
            if fmt == 'json':
                rows = [ ar.row2list(row) for row in ar.queryset ]
                #~ rows = [ ar.row2dict(row) for row in ar.queryset ]
                total_count = ar.total_count
                #logger.debug('%s.render_to_dict() total_count=%d extra=%d',self,total_count,self.extra)
                # add extra blank row(s):
                #~ for i in range(0,ar.extra):
                if ar.extra:
                    row = ar.create_instance()
                    d = ar.row2list(row)
                    #~ d = ar.row2dict(row)
                    #~ 20100706 d[rh.report.model._meta.pk.name] = -99999
                    rows.append(d)
                    total_count += 1
                return json_response_kw(count=total_count,
                  rows=rows,
                  title=unicode(ar.get_title()),
                  gc_choices=rpt.grid_configs)


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
        #~ if not ah.report.can_view.passes(request.user):
            #~ msg = "User %s cannot view %s." % (request.user,ah.report)
            #~ return http.HttpResponseForbidden()
            
        elem = None
        
        if pk != '-99999':
            try:
                elem = rpt.model.objects.get(pk=pk)
            except ValueError:
                msg = "Invalid primary key %r for %s.%s." % (pk,rpt.model._meta.app_label,rpt.model.__name__)
                raise Http404(msg)
            except rpt.model.DoesNotExist:
                raise Http404("%s %s does not exist." % (rpt,pk))
                
        if request.method == 'DELETE':
            if rpt.disable_delete is not None:
                msg = rpt.disable_delete(request,elem)
                if msg is not None:
                    return error_response(msg)
                    
            dblogger.log_deleted(request,elem)
            
            try:
                elem.delete()
            except Exception,e:
                dblogger.exception(e)
                msg = _("Failed to delete %(record)s : %(error)s.") % dict(record=obj2str(elem),error=e)
                #~ msg = "Failed to delete %s." % element_name(elem)
                return error_response(msg)
                #~ raise Http404(msg)
            return HttpResponseDeleted()
            
        if request.method == 'PUT':
            if elem is None:
                return eror.message('Tried to PUT on element -99999')
            data = http.QueryDict(request.raw_post_data)
            #~ fmt = data.get('fmt',None)
            return self.form2obj_and_save(request,ah,data,elem,False) # force_update=True)
            
        ar = ext_requests.ViewReportRequest(request,ah,ah.report.default_action)
        
        if pk == '-99999':
            elem = ar.create_instance()
            
            
        if request.method == 'GET':
            fmt = request.GET.get('fmt',None)
            if pk == '-99999':
                datarec = elem2rec1(ar,ah,elem)
                datarec.update(title=_("Insert into %s...") % ah.report.label)
            else:
                datarec = elem2rec_detailed(ar,ah,elem)
            if fmt is None or fmt == 'json':
                return json_response(datarec)
            a = rpt.get_action(fmt)
            if a is not None:
                if isinstance(a,actions.OpenWindowAction):
                    params = dict(data_record=datarec)
                    params.update(base_params=self.request2kw(ar))
                    if a.window_wrapper.tabbed:
                        tab = request.GET.get('tab',None)
                        if tab is not None: 
                            tab = int(tab)
                            params.update(active_tab=tab)
                    return HttpResponse(self.html_page(request,on_ready=['Lino.%s(undefined,%s);' % (a,py2js(params))]))
                    
                if isinstance(a,actions.RedirectAction):
                    target = a.get_target_url(elem)
                    if target is None:
                        raise Http404("%s failed for %r" % (a,elem))
                    return http.HttpResponseRedirect(target)
                    
                if isinstance(a,actions.RowAction):
                    try:
                        return a.run(self,elem)
                    except Exception,e:
                        msg = _("Action %(action)s failed for %(record)s: %(error)s") % dict(
                            action=a,
                            record=obj2str(elem),
                            error=e)
                        logger.info(msg)
                        logger.exception(e)
                        return error_response(e,msg)
                  
                raise NotImplementedError("Action %s is not implemented)" % a)
                
            raise Http404("%s has no action %r" % (ah.report,fmt))
              
        return error_response("Method %r not supported for elements of %s" % (request.method,ah.report))
        #~ raise Http404("Method %r not supported for elements of %s" % (request.method,ah.report))
        
        
    def error_response(self,*args,**kw):
        kw.update(success=False)
        return error_response(*args,**kw)
        
    def success_response(self,*args,**kw):
        kw.update(success=True)
        return json_response_kw(*args,**kw)
        
    def site_js_parts(self):
    #~ def js_cache_name(self):
        return ('cache','js','site.js')
        
    def build_site_js(self):
        """Generate the :xfile:`site.js`.
        """
        #~ for app_label in site.
        fn = os.path.join(settings.MEDIA_ROOT,*self.site_js_parts()) 
        #~ fn = r'c:\temp\dsbe.js'
        logger.info("Generating %s ...", fn)
        f = open(fn,'w')
        for ln in self.site_js_lines():
            f.write(ln+'\n')
        for rpt in reports.master_reports + reports.slave_reports + reports.generic_slaves.values():
            rh = rpt.get_handle(self) # make sure that setup_handle is called (which adds the window_wrapper)
            f.write("Ext.namespace('Lino.%s')\n" % rpt)
            for a in rpt.get_actions():
                if a.window_wrapper is not None:
                    #~ print a, "..."
                    f.write('Lino.%s = ' % a )
                    for ln in a.window_wrapper.js_render():
                        f.write(ln + "\n")
                    f.write("\n")
        f.close()
        logger.info("Generated %s ...", fn)
          
        
        
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
        if chooser:
            if chooser.simple_values:
                def row2dict(obj,d):
                    #~ d[ext_requests.CHOICES_TEXT_FIELD] = unicode(obj)
                    d[ext_requests.CHOICES_VALUE_FIELD] = unicode(obj)
                    return d
            elif chooser.instance_values:
                # same code as for ForeignKey
                def row2dict(obj,d):
                    d[ext_requests.CHOICES_TEXT_FIELD] = unicode(obj)
                    d[ext_requests.CHOICES_VALUE_FIELD] = obj.pk # getattr(obj,'pk')
                    return d
            else:
                def row2dict(obj,d):
                    d[ext_requests.CHOICES_TEXT_FIELD] = unicode(obj[1])
                    d[ext_requests.CHOICES_VALUE_FIELD] = obj[0]
                    return d
        elif isinstance(field,models.ForeignKey):
            def row2dict(obj,d):
                d[ext_requests.CHOICES_TEXT_FIELD] = unicode(obj)
                d[ext_requests.CHOICES_VALUE_FIELD] = obj.pk # getattr(obj,'pk')
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
                          message="%s has been saved" % instance)
                except Exception,e:
                    logger.exception(e)
                    #traceback.format_exc(e)
                    return error_response(e) #,_("There was a problem while saving your data : "))
                    #~ return error_response(e)
                    #~ return json_response_kw(success=False,msg="Exception occured: "+cgi.escape(str(e)))
        # otherwise it's a simple list:
        #~ print 20100406, rptreq
        d = rptreq.render_to_dict()
        return json_response(d)
        

    def get_choices_url(self,fke,**kw):
        return self.build_url("choices",
            fke.lh.rh.report.app_label,
            fke.lh.rh.report._actor_name,
            fke.field.name,**kw)
        
    def request2kw(self,rr,**kw):
        if rr.master_instance is not None:
            kw[ext_requests.URL_PARAM_MASTER_PK] = rr.master_instance.pk
            mt = ContentType.objects.get_for_model(rr.master_instance.__class__).pk
            kw[ext_requests.URL_PARAM_MASTER_TYPE] = mt
        return kw
        
    def get_request_url(self,rr,*args,**kw):
        kw = self.request2kw(rr,**kw)
        return self.build_url('api',rr.report.app_label,rr.report._actor_name,*args,**kw)
        
    def get_detail_url(self,obj,*args,**kw):
        rpt = obj.__class__._lino_model_report
        return self.build_url('api',rpt.app_label,rpt._actor_name,str(obj.pk),*args,**kw)
      
    def py2js_converter(self,v):
        if v is LANGUAGE_CHOICES:
            return js_code('LANGUAGE_CHOICES')
        if isinstance(v,Exception):
            return unicode(v)
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


    def get_actor_url(self,actor,*args,**kw):
        return self.build_url("api",actor.app_label,actor._actor_name,*args,**kw)
        
        
    def action_window_wrapper(self,a,h):
        #~ if isinstance(a,actions.DeleteSelected): return ext_windows.DeleteRenderer(self,a)
        #~ if isinstance(a,actions.UpdateRowAction): return ext_windows.UpdateRowRenderer(self,a)
          
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
            logger.debug('ExtUI.setup_handle() %s',h.report)
            if h.report.model is None:
                return
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
        #~ elif isinstance(a,actions.UpdateRowAction):
            #~ kw.update(panel_btn_handler=js_code('Lino.update_row_handler(%r)' % a.name))
        elif isinstance(a,actions.ShowDetailAction):
            #~ kw.update(panel_btn_handler=js_code('Lino.show_detail_handler()'))
            kw.update(panel_btn_handler=js_code('Lino.show_detail_handler(Lino.%s)' % a))
        elif isinstance(a,actions.InsertRow):
            kw.update(panel_btn_handler=js_code("Lino.show_insert_handler(Lino.%s)" % a))
        elif isinstance(a,actions.DeleteSelected):
            kw.update(panel_btn_handler=js_code("Lino.delete_selected" % a))
        #~ elif isinstance(a,actions.RedirectAction):
            #~ kw.update(panel_btn_handler=js_code("Lino.show_download_handler(%r)" % a.name))
        elif isinstance(a,actions.RowAction):
            kw.update(panel_btn_handler=js_code("Lino.row_action_handler(%r)" % a.name))
        else:
            kw.update(panel_btn_handler=js_code("Lino.%s" % a))
        kw.update(
          text=unicode(a.label),
        )
        return kw
        
#~ ui = ExtUI()

#~ jsgen.register_converter(ui.py2js_converter)
