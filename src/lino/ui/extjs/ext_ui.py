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
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core import exceptions

from django.utils.translation import ugettext as _

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

import lino
from lino.utils import ucsv
from lino import actions, layouts #, commands
from lino import reports        
from lino.ui import base
from lino import diag
from lino import forms
from lino.core import actors
#~ from lino.core import action_requests
from lino.utils import menus
from lino.utils import chooser
from lino.utils import jsgen
from lino.utils.jsgen import py2js, js_code, id2js
from lino.ui.extjs import ext_elems, ext_requests, ext_store, ext_windows
from lino.ui.extjs import ext_viewport
#from lino.modlib.properties.models import Property
from lino.modlib.properties import models as properties

from django.conf.urls.defaults import patterns, url, include
from lino.modlib.documents.utils import PdfAction

#~ from lino.ui.extjs.ext_windows import WindowConfig # 20100316 backwards-compat window_confics.pck 

class HttpResponseDeleted(HttpResponse):
    status_code = 204


def parse_bool(s):
    return s == 'true'
    
def parse_int(s,default=None):
    if s is None: return None
    return int(s)

            

def build_url(*args,**kw):
    url = "/".join(args)
    if len(kw):
        url += "?" + urlencode(kw)
    return url
        
def json_response_kw(**kw):
    return json_response(kw)
    
def json_response(x):
    #s = simplejson.dumps(kw,default=unicode)
    #return HttpResponse(s, mimetype='text/html')
    s = py2js(x)
    #lino.log.debug("json_response() -> %r", s)
    return HttpResponse(s, mimetype='text/html')

            
EMITTERS = {}

class Emitter:    
    fmt = None
    def handle_list_request(self,request,rh):
        raise Http404("%r emitter has not handle_list_request() " % fmt)
    def handle_element_request(self,request,ah,elem):
        raise Http404("%r emitter has not handle_element_request() " % fmt)
        
    
class DefaultEmitter(Emitter):
  
    fmt = None
    
    def handle_list_request(self,request,rh):
        a = rh.report.list_action
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
        raise Http404("Method %s not supported for container %s" % (request.method,rh))
        
    def handle_element_request(self,request,ah,elem):
        if request.method == 'DELETE':
            elem.delete()
            return HttpResponseDeleted()
        if request.method == 'PUT':
            #~ pk = request.POST.get(rh.store.pk.name)
            #~ try:
                #~ instance = ar.report.model.objects.get(pk=pk)
            #~ except ar.report.model.DoesNotExist:
                #~ raise Http404("No primary key %r in %s" % (pk,ar.report))
            PUT = http.QueryDict(request.raw_post_data)
            ah.store.form2obj(PUT,elem)
            #~ data = ah.store.get_from_form(PUT)
            #~ print data
            #~ for k,v in data.items():
                #~ setattr(elem,k,v)
            try:
                elem.save(force_update=True)
            except IntegrityError,e:
                #~ print unicode(elem)
                lino.log.exception(e)
                return json_response_kw(success=False,
                      msg=_("There was a problem while saving your data:\n%s") % e)
                
            return json_response_kw(success=True,
                  msg="%s has been saved" % elem)
        raise Http404("Method %s not supported for element %s of %s" % (request.method,elem,ah))
            
            
        

class pdf_Emitter:
    fmt = 'pdf'
    
    def handle_list_request(self,request,rh):
        raise NotImplementedError()
        
    def handle_element_request(self,request,ah,elem):
        elem.make_pdf()
        return HttpResponseRedirect(elem.pdf_url())
        
        
      
    
class json_Emitter:
  
    fmt = ext_requests.FMT_JSON
    
    def handle_list_request(self,request,rh):
        a = rh.report.list_action
        ar = ext_requests.ViewReportRequest(request,rh,a)
        if request.method == 'GET':
            if rh.report.use_layouts:
                def row2dict(row,d):
                    for fld in rh.store.fields:
                        fld.obj2json(row,d)
                    return d
            else:
                row2dict = rh.report.row2dict
            
            rows = [ row2dict(row,{}) for row in ar.queryset ]
            total_count = ar.total_count
            #lino.log.debug('%s.render_to_dict() total_count=%d extra=%d',self,total_count,self.extra)
            # add extra blank row(s):
            for i in range(0,ar.extra):
                row = ar.create_instance()
                rows.append(row2dict(row,{}))
                total_count += 1
            return json_response_kw(count=total_count,rows=rows,title=ar.get_title())
        
    def handle_element_request(self,request,ah,elem):
        raise NotImplementedError()
        
        
class csv_Emitter:
    fmt = 'csv'
    
    def handle_element_request(self,request,ah,elem):
        raise NotImplementedError()
        
    def handle_list_request(self,request,ah):
        a = ah.report.list_action
        ar = ext_requests.ViewReportRequest(request,ah,a)
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
        
class unused_submit_Emitter:
    fmt = 'submit'
    def handle_element_request(self,request,ah,a):
        ar = ext_requests.ViewReportRequest(request,ah,a)
        pk = request.POST.get(ah.store.pk.name) #,None)
        #~ try:
        data = ah.store.get_from_form(request.POST)
        if pk in ('', None):
            #return json_response(success=False,msg="No primary key was specified")
            instance = ar.create_instance(**data)
            instance.save(force_insert=True)
        else:
            instance = ar.report.model.objects.get(pk=pk)
            for k,v in data.items():
                setattr(instance,k,v)
            instance.save(force_update=True)
        return json_response_kw(success=True,
              msg="%s has been saved" % instance)
        #~ except Exception,e:
            #~ lino.log.exception(e)
            #~ #traceback.format_exc(e)
            #~ return json_response_kw(success=False,msg="Exception occured: "+cgi.escape(str(e)))
        
def register_emitter(e):
    EMITTERS[e.fmt] = e

#~ register_emitter(act_Emitter())
register_emitter(DefaultEmitter())
register_emitter(json_Emitter())
#~ register_emitter(submit_Emitter())
register_emitter(csv_Emitter())
#~ register_emitter(wc_Emitter())
register_emitter(pdf_Emitter())


class ExtUI(base.UI):
    _response = None
    
    window_configs_file = os.path.join(settings.PROJECT_DIR,'window_configs.pck')
    Panel = ext_elems.Panel
                
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
            
        #~ a = lh.datalink.get_action(name)
        #~ if a is not None:
            #~ e = ext_elems.FormActionElement(lh,name,a,**kw)
            #~ lh._buttons.append(e)
            #~ return e
          
        de = reports.get_data_elem(lh.layout.datalink,name)
        
        if isinstance(de,properties.Property):
            return self.create_prop_element(lh,de,**kw)
        if isinstance(de,models.Field):
            return self.create_field_element(lh,de,**kw)
        if isinstance(de,generic.GenericForeignKey):
            return ext_elems.VirtualFieldElement(lh,name,de,**kw)
        if callable(de):
            return self.create_meth_element(lh,name,de,**kw)
        if isinstance(de,reports.Report):
            e = ext_elems.GridElement(lh,name,de,**kw)
            #~ e = ext_elems.GridElement(lh,name,de.get_handle(self),**kw)
            lh.slave_grids.append(e)
            return e
        if isinstance(de,forms.Input):
            e = ext_elems.InputElement(lh,de,**kw)
            if not lh.start_focus:
                lh.start_focus = e
            return e
        if not name in ('__str__','__unicode__','name','label'):
            value = getattr(lh.layout,name,None)
            if value is not None:
                if isinstance(value,basestring):
                    return lh.desc2elem(panelclass,name,value,**kw)
                if isinstance(value,layouts.StaticText):
                    return ext_elems.StaticTextElement(lh,name,value)
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
        if isinstance(layout,layouts.DetailLayout) : 
            return ext_elems.DetailMainPanel
        if isinstance(layout,layouts.FormLayout) : 
            return ext_elems.FormMainPanel
        raise Exception("No element class for layout %r" % layout)
            

    
    def save_window_config(self,a,wc):
        self.window_configs[str(a)] = wc
        a.window_wrapper.config.update(wc=wc)
        f = open(self.window_configs_file,'wb')
        pickle.dump(self.window_configs,f)
        f.close()
        lino.log.debug("save_window_config(%r) -> %s",wc,a)
        #~ lh = actors.get_actor(name).get_handle(self)
        #~ if lh is not None:
            #~ lh.window_wrapper.try_apply_window_config(wc)
        self._response = None

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
            #~ (r'^submit_property$', self.submit_property_view),
            (r'^list/(?P<app_label>\w+)/(?P<rptname>\w+)$', self.list_report_view),
            #~ (r'^csv/(?P<app_label>\w+)/(?P<rptname>\w+)$', self.csv_report_view),
            (r'^grid_action/(?P<app_label>\w+)/(?P<rptname>\w+)/(?P<grid_action>\w+)$', self.json_report_view),
            #~ (r'^grid_afteredit/(?P<app_label>\w+)/(?P<rptname>\w+)$', self.grid_afteredit_view),
            (r'^submit/(?P<app_label>\w+)/(?P<rptname>\w+)$', self.form_submit_view),
            #~ (r'^form/(?P<app_label>\w+)/(?P<actor>\w+)/(?P<action>\w+)$', self.act_view),
            #~ (r'^form/(?P<app_label>\w+)/(?P<actor>\w+)$', self.act_view),
            (r'^api/(?P<app_label>\w+)/(?P<actor>\w+)$', self.api_list_view),
            (r'^api/(?P<app_label>\w+)/(?P<actor>\w+)\.(?P<fmt>\w+)$', self.api_list_view),
            (r'^api/(?P<app_label>\w+)/(?P<actor>\w+)/(?P<pk>\w+)\.(?P<fmt>\w+)$', self.api_element_view),
            (r'^api/(?P<app_label>\w+)/(?P<actor>\w+)/(?P<pk>\w+)$', self.api_element_view),
            #~ (r'^api/(?P<app_label>\w+)/(?P<actor>\w+)/(?P<action>\w+)$', self.api_view),
            (r'^ui/(?P<app_label>\w+)/(?P<actor>\w+)/(?P<action>\w+)$', self.ui_view),
            #~ (r'^action/(?P<app_label>\w+)/(?P<actor>\w+)/(?P<action>\w+)$', self.action_view),
            #~ (r'^action/(?P<app_label>\w+)/(?P<actor>\w+)$', self.action_view),
            #~ (r'^step_dialog$', self.step_dialog_view),
            #~ (r'^abort_dialog$', self.abort_dialog_view),
            (r'^choices/(?P<app_label>\w+)/(?P<rptname>\w+)/(?P<fldname>\w+)$', self.choices_view),
            #~ (r'^save_win/(?P<name>\w+)$', self.save_win_view),
            #~ (r'^save_window_config$', self.save_window_config_view),
            #~ (r'^permalink/(?P<name>\w+)$', self.permalink_do_view),
            #~ (r'^permalink$', self.permalink_do_view),
            #~ (r'^props/(?P<app_label>\w+)/(?P<model_name>\w+)$', self.props_view),
            # (r'^props$', self.props_view),
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
            index = ext_elems.VisibleComponent("index",
                #~ xtype="panel",
                html=lino_site.index_html.encode('ascii','xmlcharrefreplace'),
                autoScroll=True,
                #width=50000,
                #height=50000,
                region="center")
            console = jsgen.Component("konsole",
                #~ xtype="panel",
                split=True,
                collapsible=True,
                title=_("Console"),
                id="konsole",
                html='Console started',
                autoScroll=True,
                height=100,
                region="south")
            vp = ext_viewport.Viewport(lino_site.title,console,index)
            s = vp.render_to_html(request)
            self._response = HttpResponse(s)
        return self._response

    def menu_view(self,request):
        from lino.lino_site import lino_site
        #~ from lino import lino_site
        return json_response_kw(success=True,
          message=(_("Welcome on Lino server %r.") % lino_site.title) + '\n' + diag.thanks_to(),
          load_menu=lino_site.get_menu(request))
        #~ s = py2js(lino_site.get_menu(request))
        #~ return HttpResponse(s, mimetype='text/html')

    def api_list_view(self,request,app_label=None,actor=None,fmt=None):
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
        e = EMITTERS.get(fmt,None)
        if e is None:
            raise Http404("Unknown format %r " % fmt)
        return e.handle_list_request(request,ah)
        
    def api_element_view(self,request,app_label=None,actor=None,pk=None,fmt=None):
        """
        GET : Retrieve a representation of the addressed member of the collection expressed in an appropriate MIME type.
        PUT : Update the addressed member of the collection or create it with the specified ID. 
        POST : Treats the addressed member as a collection and creates a new subordinate of it. 
        DELETE : Delete the addressed member of the collection. 
        (Source: http://en.wikipedia.org/wiki/Restful)
        """
        rpt = actors.get_actor2(app_label,actor)
        instance = rpt.model.objects.get(pk=pk)
        ah = rpt.get_handle(self)
        e = EMITTERS.get(fmt,None)
        if e is None:
            raise Http404("Unknown format %r " % fmt)
        return e.handle_element_request(request,ah,instance)
        #~ raise Http404("Unknown request method %r " % request.method)
        
    def ui_view(self,request,app_label=None,actor=None,action=None,**kw):
        actor = actors.get_actor2(app_label,actor)
        ah = actor.get_handle(self)
        #~ if not action:
            #~ a = actor.default_action
        #~ else:
        a = ah.get_action(action)
        if a is None:
            msg = "No action %s in %s" % (action,ah)
            #~ print msg
            raise Http404(msg)
        if request.method == 'GET':
            assert a.window_wrapper is not None, "%r %s has no window_wrapper" % (a,a)
            return json_response_kw(success=True,js_code=a.window_wrapper.js_render)
            
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
        #~ wc = WindowConfig(str(ar.ah.report),**wc)
        #~ name = str(a)
        ui.save_window_config(a,wc)
        return json_response_kw(success=True,
          message=_(u'Window config %s has been saved (%r)') % (a,wc))
  
        
        
    #~ def start_dialog(self,dlg):
        #~ r = dlg._start().as_dict()
        #~ lino.log.debug('ExtUI.start_dialog(%s) -> %r',dlg,r)
        #~ return json_response(r)
        
    #~ def step_dialog_view(self,request):
        #~ return self.json_dialog_view_(request,'_step')
        
    #~ def abort_dialog_view(self,request):
        #~ return self.json_dialog_view_(request,'_abort')
        
    #~ def json_dialog_view_(self,request,meth_name,**kw):
        #~ dialog_id = long(request.POST.get('dialog_id'))
        #~ dlg = actions.get_dialog(dialog_id)
        #~ if dlg is None:
            #~ return json_response(actions.DialogResponse(
              #~ alert_msg=_('No dialog %r running on this server.' % dialog_id)
              #~ ).as_dict())
        #~ if dlg.request.user != request.user:
            #~ print 20100218, dlg.request.user, '!=', request.user
            #~ return json_response(actions.DialogResponse(
              #~ alert_msg=_('Dialog %r ist not for you.' % dialog_id)
              #~ ).as_dict())
        #~ dlg.request = request
        #~ dlg.set_modal_exit(request.POST.get('last_button'))
        #~ m = getattr(dlg,meth_name)
        #~ r = m().as_dict()
        #~ lino.log.debug('%s.%s() -> %r',dlg,meth_name,r)
        #~ return json_response(r)
        
    #~ def submit_property_view(self,request):
        #~ rpt = properties.PropValuesByOwner()
        #~ if not rpt.can_change.passes(request):
            #~ return json_response_kw(success=False,
                #~ message="User %s cannot edit %s." % (request.user,rpt))
        #~ rh = rpt.get_handle(self)
        #~ rr = ext_requests.BaseViewReportRequest(request,rh,rh.report.default_action)
        #~ name = request.POST.get('name')
        #~ value = request.POST.get('value')
        #~ try:
            #~ p = properties.Property.objects.get(pk=name)
        #~ except properties.Property.DoesNotExist:
            #~ return json_response_kw(success=False,
                #~ message="No property named %r." % name)
        #~ p.set_value_for(rr.master_instance,value)
        #~ return json_response_kw(success=True,msg='%s : %s = %r' % (rr.master_instance,name,value))
    
        
    def unused_permalink_do_view(self,request):
        print request.GET.get('show')
        def js():
            for name in request.GET.get('show'):
                name = name.replace('_','.')
                actor = actors.get_actor(name)
                if actor is None:
                    print "No actor", name
                else:
                    rh = actor.get_handle(self)
                    for ln in rh.window_wrapper.js_render(): 
                        yield ln
                    yield '().show();'
        #~ dlg = ext_requests.Dialog(request,self,actor,None)
        #~ ar = ext_requests.ViewReportRequest(request,actor.get_handle(self),actor.default_action)
        #~ return json_response(ar.run().as_dict())
        return json_response_kw(success=True,exec_js=js)
        #~ return self.start_dialog(dlg)
        

    def unused_save_window_config_view(self,request):
        actor = ext_windows.SaveWindowConfig()
        ah = actor.get_handle(self)
        ar = ext_requests.ViewReportRequest(request,ah,actor.default_action)
        return json_response(ar.run())
        #~ return self.start_dialog(dlg)
        
    def choices_view(self,request,app_label=None,rptname=None,fldname=None,**kw):
        rpt = actors.get_actor2(app_label,rptname)
        rh = rpt.get_handle(self)
        for k,v in request.GET.items():
            kw[str(k)] = v
        chooser = rh.choosers[fldname]
        qs = chooser.get_choices(**kw)
        quick_search = request.REQUEST.get(ext_requests.URL_PARAM_FILTER,None)
        if quick_search is not None:
            qs = reports.add_quick_search_filter(qs,quick_search)
        
        def row2dict(obj,d):
            d[ext_requests.CHOICES_TEXT_FIELD] = unicode(obj)
            d[ext_requests.CHOICES_VALUE_FIELD] = obj.pk # getattr(obj,'pk')
            return d
            
        rows = [ row2dict(row,{}) for row in qs ]
        return json_response_kw(count=len(rows),rows=rows,title=_('Choices for %s') % fldname)
        
        
    #~ def grid_afteredit_view(self,request,**kw):
        #~ kw['colname'] = request.POST['grid_afteredit_colname']
        #~ kw['submit'] = True
        #~ return self.json_report_view(request,**kw)

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
        return build_url("/api",actor.app_label,actor._actor_name,**kw)

    def get_form_action_url(self,fh,action,**kw):
        #~ a = btn.lh.datalink.actor
        #~ a = action.actor
        return build_url("/form",fh.layout.app_label,fh.layout._actor_name,action.name,**kw)
        
    def get_choices_url(self,fke,**kw):
        return build_url("/choices",
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
            return dict(text=v.label,menu=dict(items=v.items))
        if isinstance(v,menus.MenuItem):
            #~ handler = "function(btn,evt){Lino.do_action(undefined,%r,%r,{})}" % (v.actor.get_url(lino_site.ui),id2js(v.actor.actor_id))
            url = build_url("/ui",v.action.actor.app_label,v.action.actor._actor_name,v.action.name)
            handler = "function(btn,evt){Lino.do_action(undefined,{url:%r})}" % url
            return dict(text=v.label,handler=js_code(handler))
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
        return build_url("/api",action.actor.app_label,action.actor._actor_name,name,**kw)
        #~ url = "/action/" + a.app_label + "/" + a._actor_name 
        #~ if len(kw):
            #~ url += "?" + urlencode(kw)
        #~ return url
        
        
        
        
    def action_window_wrapper(self,a,h):
        if isinstance(a,PdfAction): return ext_windows.DownloadRenderer(self,a)
        if isinstance(a,reports.DeleteSelected): return ext_windows.DeleteRenderer(self,a)
          
        if isinstance(a,reports.GridEdit):
            #~ if a.actor.master is not None:
                #~ return None
                #~ raise Exception("action_window_wrapper() for slave report %s" % a.actor)
                #~ return ext_windows.GridSlaveWrapper(h,a)
            return ext_windows.GridMasterWrapper(h,a)
            #~ else:
                #~ return ext_windows.GridSlaveWrapper(self,a.name,a)
        if isinstance(a,reports.DetailAction):
            return ext_windows.DetailSlaveWrapper(self,a)
            
        if isinstance(a,reports.InsertRow):
            return ext_windows.InsertWrapper(h,a)
            
        if isinstance(a,properties.PropsEdit):
            #~ return ext_windows.PropertiesWrapper(self,h,a)
            return None
            
        if isinstance(a,properties.PropertiesAction):
            return ext_windows.PropertiesWrapper(h,a)
        if isinstance(a,reports.SlaveGridAction):
            return ext_windows.GridSlaveWrapper(h,a) # a.name,a.slave.default_action)
        
        
        
    def setup_handle(self,h):
        if isinstance(h,reports.ReportHandle):
            lino.log.debug('ExtUI.setup_handle() %s',h.report)
            h.choosers = chooser.get_choosers_for_model(h.report.model,chooser.FormChooser)
            #~ h.report.add_action(ext_windows.SaveWindowConfig(h.report))
            if h.report.use_layouts:
                h.store = ext_store.Store(h)
                    
            else:
                h.store = None
                
            for a in h.get_actions():
                a.window_wrapper = self.action_window_wrapper(a,h)
            
        
ui = ExtUI()

jsgen.register_converter(ui.py2js_converter)
