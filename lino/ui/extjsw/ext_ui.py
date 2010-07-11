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

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

import lino
from lino.utils import ucsv
from lino.utils import mixins
from lino.utils import choosers
from lino import actions, layouts #, commands
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
from lino.modlib.properties import models as properties

from django.conf.urls.defaults import patterns, url, include
from lino.utils.mixins import PrintAction

from lino.core.coretools import app_labels

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

def elem2rec(request,ah,elem):
    return dict(id=elem.pk,
      data=ah.store.row2dict(elem),
      disabled_fields=[ext_elems.form_field_name(f) for f in ah.report.disabled_fields(request,elem)],
      title=unicode(elem))

            
    
def handle_list_request(request,rh):
    if not rh.report.can_view.passes(request.user):
        msg = "User %s cannot view %s." % (request.user,rh.report)
        return http.HttpResponseForbidden()
    a = rh.report.default_action
    #~ a = rh.report.list_action
    ar = ext_requests.ViewReportRequest(request,rh,a)
    if request.method == 'POST':
        """
        Wikipedia:
        Create a new entry in the collection where the ID is assigned automatically by the collection. 
        The ID created is usually included as part of the data returned by this operation. 
        """
        #~ data = rh.store.get_from_form(request.POST)
        #~ instance = ar.create_instance(**data)
        instance = ar.create_instance()
        rh.store.form2obj(request.POST,instance)
        instance.save(force_insert=True)
        return json_response_kw(success=True,msg="%s has been created" % instance)
        
        
    if request.method == 'GET':
        fmt = request.GET.get('fmt',None)
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
            
        if fmt is None:
            #~ if rh.report.use_layouts:
                #~ def row2dict(row):
                    #~ d = {}
                    #~ for fld in rh.store.fields:
                        #~ fld.obj2json(row,d)
                    #~ return d
            #~ else:
                #~ row2dict = rh.report.row2dict
            #~ rows = [ row2dict(row,{}) for row in ar.queryset ]
            
            rows = [ ar.row2dict(row) for row in ar.queryset ]
            total_count = ar.total_count
            #lino.log.debug('%s.render_to_dict() total_count=%d extra=%d',self,total_count,self.extra)
            # add extra blank row(s):
            #~ for i in range(0,ar.extra):
            if ar.extra:
                row = ar.create_instance()
                d = ar.row2dict(row)
                d[rh.report.model._meta.pk.name] = -99999
                rows.append(d)
                total_count += 1
            return json_response_kw(count=total_count,rows=rows,title=unicode(ar.get_title()))


    raise Http404("Method %s not supported for container %s" % (request.method,rh))
    
    
def handle_element_request(request,ah,elem):
    if not ah.report.can_view.passes(request.user):
        msg = "User %s cannot view %s." % (request.user,ah.report)
        return http.HttpResponseForbidden()
    if request.method == 'DELETE':
        elem.delete()
        return HttpResponseDeleted()
    if request.method == 'PUT':
        data = http.QueryDict(request.raw_post_data)
        try:
            ah.store.form2obj(data,elem)
        except exceptions.ValidationError,e:
            return json_response_kw(success=False,msg=unicode(e))
        try:
            elem.save(force_update=True)
        except IntegrityError,e:
            #~ print unicode(elem)
            lino.log.exception(e)
            return json_response_kw(success=False,
                  msg=_("There was a problem while saving your data:\n%s") % e)
        return json_response_kw(success=True,
              msg="%s has been saved" % elem)
              
    if request.method == 'GET':
        fmt = request.GET.get('fmt',None)
        if fmt is None:
            return json_response_kw(id=elem.pk,
              data=ah.store.row2dict(elem),
              disabled_fields=[ext_elems.form_field_name(f) for f in ah.report.disabled_fields(request,elem)],
              title=unicode(elem))
        if fmt == 'picture':
            pm = mixins.get_print_method('picture')
        else:
            pm = elem.get_print_method(fmt)
            if pm is None:
                raise Http404("%r has no print method (fmt=%r)" % (elem,fmt))
        target = pm.get_target_url(elem)
        if target is None:
            raise Http404("%s could not build %r" % (pm,elem))
        return http.HttpResponseRedirect(target)
    raise Http404("Method %r not supported for elements of %s" % (request.method,ah.report))
        


class ExtUI(base.UI):
    _response = None
    name = 'extjsw'
    verbose_name = "ExtJS with Windows"
    window_configs_file = os.path.join(settings.PROJECT_DIR,'window_configs.pck')
    Panel = ext_elems.Panel
    
    USE_WINDOWS = False  # If you change this, then change also Lino.USE_WINDOWS in lino.js

    def __init__(self):
        self.window_configs = {}
        if os.path.exists(self.window_configs_file):
            lino.log.info("Loading %s...",self.window_configs_file)
            wc = pickle.load(open(self.window_configs_file,"rU"))
            #lino.log.debug("  -> %r",wc)
            if type(wc) is dict:
                self.window_configs = wc
        else:
            lino.log.warning("window_configs_file %s not found",self.window_configs_file)
            
    def create_layout_element(self,lh,panelclass,name,**kw):
        
        if name == "_":
            return ext_elems.Spacer(lh,name,**kw)
            
        de = reports.get_data_elem(lh.layout.datalink,name)
        
        if isinstance(de,properties.Property):
            return self.create_prop_element(lh,de,**kw)
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
                if isinstance(value,layouts.StaticText):
                    return ext_elems.StaticTextElement(lh,name,value)
                if isinstance(value,layouts.DataView):
                    return ext_elems.DataViewElement(lh,name,value)
                    #~ return ext_elems.TemplateElement(lh,name,value)
                if isinstance(value,mixins.PicturePrintMethod):
                    return ext_elems.PictureElement(lh,name,value)
                #~ if isinstance(value,layouts.PropertyGrid):
                    #~ return ext_elems.PropertyGridElement(lh,name,value)
                raise KeyError("Cannot handle value %r in %s.%s." % (value,lh.layout._actor_name,name))
        msg = "Unknown element %r referred in layout %s" % (name,lh.layout)
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
        if isinstance(layout,layouts.ListLayout) : 
            return ext_elems.GridMainPanel
        #~ if isinstance(layout,layouts.TabLayout) : 
            #~ return ext_elems.TabMainPanel
        if isinstance(layout,layouts.DetailLayout) : 
            return ext_elems.DetailMainPanel
        #~ if isinstance(layout,layouts.FormLayout) : 
            #~ return ext_elems.FormMainPanel
        raise Exception("No element class for layout %r" % layout)
            

    
    def save_window_config(self,a,wc):
        self.window_configs[str(a)] = wc
        a.window_wrapper.config.update(wc=wc)
        f = open(self.window_configs_file,'wb')
        pickle.dump(self.window_configs,f)
        f.close()
        lino.log.debug("save_window_config(%r) -> %s",wc,a)
        from lino.lino_site import lino_site
        self.build_lino_js(lino_site)
        #~ lh = actors.get_actor(name).get_handle(self)
        #~ if lh is not None:
            #~ lh.window_wrapper.try_apply_window_config(wc)
        #~ self._response = None

    def load_window_config(self,action,**kw):
    #~ def load_window_config(self,name):
        wc = self.window_configs.get(str(action),None)
        if wc is not None:
            lino.log.debug("load_window_config(%r) -> %s",str(action),wc)
            for n in ('x','y','width','height'):
                if wc.get(n,0) is None:
                    del wc[n]
                    #~ raise Exception('invalid window configuration %r' % wc)
            kw.update(**wc)
        return kw

  
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
            (r'^api/(?P<app_label>\w+)/(?P<actor>\w+)$', self.api_list_view),
            #~ (r'^api/(?P<app_label>\w+)/(?P<actor>\w+)\.(?P<fmt>\w+)$', self.api_list_view),
            #~ (r'^api/(?P<app_label>\w+)/(?P<actor>\w+)/(?P<pk>[-\w]+)\.(?P<fmt>\w+)$', self.api_element_view),
            (r'^api/(?P<app_label>\w+)/(?P<actor>\w+)/(?P<pk>.+)$', self.api_element_view),
            #~ (r'^api/(?P<app_label>\w+)/(?P<actor>\w+)/(?P<pk>\w+)/(?P<method>\w+)$', self.api_element_view),
            #~ (r'^api/(?P<app_label>\w+)/(?P<actor>\w+)/(?P<action>\w+)$', self.api_view),
            (r'^window_configs/(?P<wc_name>.+)$', self.window_configs_view),
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
        

    def index_view(self, request):
        if self._response is None:
            lino.log.debug("building extjs._response...")
            from lino.lino_site import lino_site
            #~ index = ext_elems.VisibleComponent("index",
            if self.USE_WINDOWS:
                index = dict(
                    xtype="panel",
                    html=lino_site.index_html.encode('ascii','xmlcharrefreplace'),
                    layout='fit',
                    autoScroll=True,
                    #~ autoHeight=True,
                    #width=50000,
                    #height=50000,
                    region="center")
            else:
                index = dict(
                    xtype="panel",
                    items=dict(layout='fit',html=lino_site.index_html.encode('ascii','xmlcharrefreplace')),
                    id="main_area",
                    region="center",
                    layout='fit',
                    #~ layout='form',
                    )
            konsole = jsgen.Component("konsole",
                #~ xtype="panel",
                split=True,
                collapsible=True,
                autoScroll=True,
                title=_("Console"),
                id="konsole",
                html='Console started',
                height=100,
                region="south")
            vp = ext_viewport.Viewport(self,lino_site,konsole,index)
            s = vp.render_to_html(request)
            self._response = HttpResponse(s)
        return self._response

    def menu_view(self,request):
        from lino.lino_site import lino_site
        #~ from lino import lino_site
        return json_response_kw(success=True,
          message=(_("Welcome on Lino server %r, user %s") % (lino_site.title,request.user)),
          load_menu=lino_site.get_site_menu(request.user))
        #~ s = py2js(lino_site.get_menu(request))
        #~ return HttpResponse(s, mimetype='text/html')

    def old_api_list_view(self,request,app_label=None,actor=None,fmt=None):
        """
        GET : List the members of the collection. 
        PUT : Replace the entire collection with another collection. 
        POST : Create a new entry in the collection where the ID is assigned automatically by the collection. 
               The ID created is included as part of the data returned by this operation. 
        DELETE : Delete the entire collection.
        (Source: http://en.wikipedia.org/wiki/Restful)
        """
        actor = actors.get_actor2(app_label,actor)
        ah = actor.get_handle(self)
        return handle_list_request(request,ah)
        
    def old_api_element_view(self,request,app_label=None,actor=None,pk=None):
        """
        GET : Retrieve a representation of the addressed member of the collection expressed in an appropriate MIME type.
        PUT : Update the addressed member of the collection or create it with the specified ID. 
        POST : Treats the addressed member as a collection and creates a new subordinate of it. 
        DELETE : Delete the addressed member of the collection. 
        (Source: http://en.wikipedia.org/wiki/Restful)
        """
        rpt = actors.get_actor2(app_label,actor)
        ah = rpt.get_handle(self)
        if pk == '-99999':
            ar = ext_requests.ViewReportRequest(request,ah,ah.report.default_action)
            #~ ar = ext_requests.ViewReportRequest(request,ah,ah.report.list_action)
            instance = ar.create_instance()
        else:
            try:
                instance = rpt.model.objects.get(pk=pk)
            except rpt.model.DoesNotExist:
                raise Http404("%s %s does not exist." % (rpt,pk))
        return handle_element_request(request,ah,instance)
        #~ raise Http404("Unknown request method %r " % request.method)
        
        
    def api_list_view(self,request,app_label=None,actor=None):
    #~ def api_list_view(self,request,app_label=None,actor=None,fmt=None):
        """
        GET : List the members of the collection. 
        PUT : Replace the entire collection with another collection. 
        POST : Create a new entry in the collection where the ID is assigned automatically by the collection. 
               The ID created is included as part of the data returned by this operation. 
        DELETE : Delete the entire collection.
        (Source: http://en.wikipedia.org/wiki/Restful)
        """
        rpt = actors.get_actor2(app_label,actor)
        rh = rpt.get_handle(self)
        
        if not rh.report.can_view.passes(request.user):
            msg = _("User %s cannot view %s.") % (request.user,rh.report)
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
            rh.store.form2obj(request.POST,instance)
            try:
                instance.full_clean()
            except exceptions.ValidationError, e:
                return json_response_kw(success=False,msg="Failed to save %s : %s" % (instance,e))
            #~ print instance, instance.pk
            instance.save(force_insert=True)
            #~ except models.IntegrityError,e:
                #~ json_response_kw(success=False,msg="Failed to save %s : %e" % (instance,e))
            return json_response_kw(success=True,msg="%s has been created" % instance)
            
            
        if request.method == 'GET':
            fmt = request.GET.get('fmt',None)
            a = rpt.get_action(fmt)
            #~ if fmt  == 'grid':
            if a is not None:
                kw = {}
                #~ kw.update(title=unicode(rh.get_title(None)))
                kw.update(title=unicode(a.get_list_title(rh)))
                params = dict(region='center')
                main = js_code('Lino.%s(%s)' % (a,py2js(params)))
                return HttpResponse(self.html_page(request,main,**kw))
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
            #~ if fmt is None:
                #~ if rh.report.use_layouts:
                    #~ def row2dict(row):
                        #~ d = {}
                        #~ for fld in rh.store.fields:
                            #~ fld.obj2json(row,d)
                        #~ return d
                #~ else:
                    #~ row2dict = rh.report.row2dict
                #~ rows = [ row2dict(row,{}) for row in ar.queryset ]
                
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
                return json_response_kw(count=total_count,rows=rows,title=unicode(ar.get_title()))


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
            
        #~ 20100706    
        #~ if pk == '-99999':
            #~ ar = ext_requests.ViewReportRequest(request,ah,ah.report.list_action)
            #~ elem = ar.create_instance()
        #~ else:
        try:
            elem = rpt.model.objects.get(pk=pk)
        except rpt.model.DoesNotExist:
            raise Http404("%s %s does not exist." % (rpt,pk))
                
        if request.method == 'DELETE':
            elem.delete()
            return HttpResponseDeleted()
            
        if request.method == 'PUT':
            data = http.QueryDict(request.raw_post_data)
            try:
                ah.store.form2obj(data,elem)
            except exceptions.ValidationError,e:
                return json_response_kw(success=False,msg=unicode(e))
            try:
                elem.save(force_update=True)
            except IntegrityError,e:
                #~ print unicode(elem)
                lino.log.exception(e)
                return json_response_kw(success=False,
                      msg=_("There was a problem while saving your data:\n%s") % e)
            return json_response_kw(success=True,
                  msg="%s has been saved" % elem)
                  
        if request.method == 'GET':
            fmt = request.GET.get('fmt',None)
            if fmt is None:
                return json_response(elem2rec(elem))
            a = rpt.get_action(fmt)
            #~ if fmt == 'detail':
            if a is not None:
                if isinstance(a,actions.OpenWindowAction):
                    kw = {}
                    #~ kw.update(title=unicode(elem))
                    kw.update(title=unicode(a.get_elem_title(elem)))
                    #~ kw.update(content_type=rh.content_type)
                    #~ tbar=ext_elems.Toolbar(
                      #~ items=self.site.get_site_menu(request.user),
                      #~ region='north',height=29)# renderTo='tbar')
                    #~ print 20100624, a.window_wrapper_u.main
                    params = dict(data_record=elem2rec(request,ah,elem),region='center')
                    main = js_code('Lino.%s(%s)' % (a,py2js(params)))
                    #~ return HttpResponse(self.html_page(tbar,a.window_wrapper_u.main,**kw))
                    return HttpResponse(self.html_page(request,main,**kw))
                    
                if isinstance(a,PrintAction):
                    pm = elem.get_print_method()
                    if pm is None:
                        raise Http404("%r has no print method (fmt=%r)" % (elem,fmt))
                    target = pm.get_target_url(elem)
                    if target is None:
                        raise Http404("%s could not build %r" % (pm,elem))
                    return http.HttpResponseRedirect(target)
                  
                raise NotImplementedError("%r action %r is not implemented)" % (elem,fmt))
              
        raise Http404("Method %r not supported for elements of %s" % (request.method,ah.report))
        
        
        
        
    def js_cache_name(self,site):
        return ('cache','js','site.js')
        
    def setup_site(self,site):
        base.UI.setup_site(self,site) # will create a.window_wrapper for all actions
        self.build_lino_js(site)
        
    def build_lino_js(self,site):
        #~ for app_label in site.
        fn = os.path.join(settings.MEDIA_ROOT,*self.js_cache_name(site)) 
        #~ fn = r'c:\temp\dsbe.js'
        lino.log.info("Generating %s ...", fn)
        f = open(fn,'w')
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
          
        
    def window_configs_view(self,request,wc_name=None,**kw):
        if request.method == 'POST':
            params = request.POST
            wc = dict()
            #~ name = str(ar.ah.report)
            wc['height'] = parse_int(params.get('height'))
            wc['width'] = parse_int(params.get('width'))
            wc['maximized'] = parse_bool(params.get('maximized'))
            wc['x'] = parse_int(params.get('x'))
            wc['y'] = parse_int(params.get('y'))
            cw = params.getlist('column_widths')
            assert type(cw) is list, "cw is %r (expected list)" % cw
            wc['column_widths'] = [parse_int(w,100) for w in cw]
            a = actors.resolve_action(wc_name)
            if a is None:
                return json_response_kw(success=False,
                  message=_(u'%r : no such action') % wc_name)
            self.save_window_config(a,wc)
            return json_response_kw(success=True,
              message=_(u'Window config %s has been saved (%r)') % (a,wc))
  
      
    def unused_ui_view(self,request,app_label=None,actor=None,action=None,**kw):
        actor = actors.get_actor2(app_label,actor)
        ah = actor.get_handle(self)
        a = ah.get_action(action)
        if a is None:
            msg = "No action %s in %s" % (action,ah)
            #~ print msg
            raise Http404(msg)
        #~ if request.method == 'GET':
            #~ assert a.window_wrapper is not None, "%r %s has no window_wrapper" % (a,a)
            #~ return json_response_kw(success=True,js_code=a.window_wrapper.js_render)
            
        
    def choices_view(self,request,app_label=None,rptname=None,fldname=None,**kw):
        rpt = actors.get_actor2(app_label,rptname)
        rh = rpt.get_handle(self)
        field = rpt.model._meta.get_field(fldname)
        chooser = choosers.get_for_field(field)
        if chooser:
            qs = chooser.get_request_choices(request)
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
        else:
            def row2dict(obj,d):
                if type(obj) is list or type(obj) is tuple:
                    d[ext_requests.CHOICES_TEXT_FIELD] = unicode(obj[1])
                    d[ext_requests.CHOICES_VALUE_FIELD] = obj[1]
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

    def get_form_action_url(self,fh,action,**kw):
        #~ a = btn.lh.datalink.actor
        #~ a = action.actor
        return self.build_url("form",fh.layout.app_label,fh.layout._actor_name,action.name,**kw)
        
    def get_choices_url(self,fke,**kw):
        return self.build_url("choices",
            fke.lh.layout.datalink_report.app_label,
            fke.lh.layout.datalink_report._actor_name,
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

    def show_action_window(self,ar,action):
        ar.response.update(js_code = action.window_wrapper.js_render)
        #~ ar.show_window(action.window_wrapper.js_render)

    #~ def show_properties(self,ar,**kw):
        #~ ar.show_window(ar.rh.properties.window_wrapper.js_render)
        
        
    #~ def view_form(self,dlg,**kw):
        #~ "called from ViewForm.run_in_dlg()"
        #~ frm = dlg.actor
        #~ fh = self.get_form_handle(frm)
        #~ yield dlg.show_window(fh.window_wrapper.js_render).over()
        
    def py2js_converter(self,v):
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
            #~ if a.actor.master is not None:
                #~ return None
                #~ raise Exception("action_window_wrapper() for slave report %s" % a.actor)
                #~ return ext_windows.GridSlaveWrapper(h,a)
            return ext_windows.GridMasterWrapper(h,a)
            #~ else:
                #~ return ext_windows.GridSlaveWrapper(self,a.name,a)
        if isinstance(a,actions.InsertRow):
            return ext_windows.InsertWrapper(h,a)
            
        if isinstance(a,actions.ShowDetailAction):
            return ext_windows.DetailWrapper(h,a)

        #~ if isinstance(a,layouts.ShowDetailAction):
            #~ return ext_windows.LayoutDetailWrapper(h,a)

            
        #~ if isinstance(a,properties.PropsEdit):
            #~ return None
            
        #~ if isinstance(a,properties.PropertiesAction):
            #~ return ext_windows.PropertiesWrapper(h,a)
        if isinstance(a,actions.SlaveGridAction):
            return ext_windows.GridSlaveWrapper(h,a) # a.name,a.slave.default_action)
            
        #~ if isinstance(a,actions.SlaveDetailAction): # not tested
            #~ return ext_windows.DetailSlaveWrapper(self,a)
            
        
        
        
    def setup_handle(self,h):
        #~ if isinstance(h,layouts.TabPanelHandle):
            #~ h._main = ext_elems.TabPanel([l.get_handle(self) for l in h.layouts])
          
        if isinstance(h,reports.ReportHandle):
            lino.log.debug('ExtUI.setup_handle() %s',h.report)
            #~ h.choosers = chooser.get_choosers_for_model(h.report.model,chooser.FormChooser)
            #~ h.report.add_action(ext_windows.SaveWindowConfig(h.report))
            if h.report.use_layouts:
                h.store = ext_store.Store(h)
                    
            else:
                h.store = None
                
            for a in h.get_actions():
                a.window_wrapper = self.action_window_wrapper(a,h)
            
    def source_dir(self):
        return os.path.abspath(os.path.dirname(__file__))
        
    def a2btn(self,a,**kw):
        if isinstance(a,actions.SubmitDetail):
            #~ kw.update(client_side=True)
            #~ kw.update(scope=js_code('this'))
            kw.update(handler=js_code('Lino.submit_detail'))
        elif isinstance(a,actions.SubmitInsert):
            #~ kw.update(client_side=True)
            #~ kw.update(scope=js_code('this'))
            kw.update(handler=js_code('Lino.submit_insert'))
        else:
            kw.update(handler=js_code("Lino.%s" % a))
        kw.update(
          opens_a_slave=a.opens_a_slave,
          name=a.name,
          label=unicode(a.label),
        )
        return kw
        
#~ ui = ExtUI()

#~ jsgen.register_converter(ui.py2js_converter)
