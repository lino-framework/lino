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

from django.db import models
from django.conf import settings
from django.http import HttpResponse
from django.core import exceptions

from django.utils.translation import ugettext as _

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

import lino
from lino import actions, layouts
from lino.ui import base
from lino.utils import actors
from lino.utils import menus
from lino.utils.jsgen import py2js, js_code, id2js
from lino.ui.extjs import ext_elems, ext_requests, ext_store
from lino.ui.extjs import ext_viewport
#from lino.modlib.properties.models import Property
from lino.modlib.properties import models as properties

from django.conf.urls.defaults import patterns, url, include



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




class SaveWindowConfig(actions.Command):
  
    #~ def run_in_dlg(self,dlg,name):
    def run_in_dlg(self,dlg):
        #~ h = int(context.request.POST.get('h'))
        #~ w = int(context.request.POST.get('w'))
        name = dlg.get('name')
        h = int(dlg.get('h'))
        w = int(dlg.get('w'))
        maximized = dlg.get('max')
        if maximized == 'true':
            maximized = True
        else:
            maximized = False
        x = int(dlg.get('x'))
        y = int(dlg.get('y'))
        yield dlg.confirm("Save %r window config (%r,%r,%r,%r,%r)\nAre you sure?" % (name,x,y,h,w,maximized))
        #~ ui.window_configs[name] = (x,y,w,h,maximized)
        #~ ui.save_window_configs()
        ui.save_window_config(name,(x,y,w,h,maximized))
        yield dlg.notify("Window config %r has been saved" % name).over()


#~ def permalink_do_view(request,name=None):
    #~ name = name.replace('_','.')
    #~ actor = actors.get_actor(name)
    #~ context = ext_requests.ActionContext(request,ui,actor,None)
    #~ context.run()
    #~ return json_response(context.response)

#~ def save_win_view(request,name=None):
    #~ #print 'save_win_view()',name
    #~ actor = SaveWindowConfig()
    #~ context = ext_requests.ActionContext(request,ui,actor,None,name)
    #~ context.run()
    #~ return json_response(context.response)





"""
def menu2js(ui,v,**kw):    
    if isinstance(v,menus.Menu):
        if v.parent is None:
            return menu2js(ui,v.items,**kw)
            #kw.update(region='north',height=27,items=v.items)
            #return py2js(kw)
        kw.update(text=v.label,menu=dict(items=v.items))
        return menu2js(ui,kw)
        
    if isinstance(v,menus.MenuItem):
        url = ui.get_action_url(v.actor)
        handler = "function(btn,evt){Lino.do_action(undefined,%r,%r,{})}" % (url,id2js(v.actor.actor_id))
        return py2js(dict(text=v.label,handler=js_code(handler)))
        #~ if v.args:
            #~ handler = "function(btn,evt) {%s.show(btn,evt,%s);}" % (
                #~ id2js(v.actor.actor_id),
                #~ ",".join([py2js(a) for a in v.args]))
        #~ else:
            #~ handler = "function(btn,evt) {%s.show(btn,evt);}" % id2js(v.actor.actor_id)
        #~ return py2js(dict(text=v.label,handler=js_code(handler)))
        
    return py2js(v,**kw)        
"""  
    


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
            
        de = lh.link.get_data_elem(name)
        
        if isinstance(de,models.Field):
            return self.create_field_element(lh,de,**kw)
        if isinstance(de,generic.GenericForeignKey):
            return ext_elems.VirtualFieldElement(lh,name,de,**kw)
            
        from lino import reports
        
        if isinstance(de,reports.Report):
            e = ext_elems.GridElement(lh,name,de.get_handle(self),**kw)
            lh.slave_grids.append(e)
            return e
        if isinstance(de,actions.Action):
            e = ext_elems.ActionElement(lh,name,de,**kw)
            lh._buttons.append(e)
            return e
            
        from lino import forms
        
        if isinstance(de,forms.Input):
            e = ext_elems.InputElement(lh,de,**kw)
            if not lh.start_focus:
                lh.start_focus = e
            return e
        if callable(de):
            return self.create_meth_element(lh,name,de,**kw)
            
        if not name in ('__str__','__unicode__','name','label'):
            value = getattr(lh.layout,name,None)
            if value is not None:
                if isinstance(value,basestring):
                    return lh.desc2elem(panelclass,name,value,**kw)
                if isinstance(value,layouts.StaticText):
                    return ext_elems.StaticTextElement(lh,name,value)
                #~ if isinstance(value,layouts.PropertyGrid):
                    #~ return ext_elems.PropertyGridElement(lh,name,value)
                raise KeyError("Cannot handle value %r in %s.%s." % (value,lh.layout.name,name))
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
        
    def create_field_element(self,lh,field,**kw):
        e = lh.main_class.field2elem(lh,field,**kw)
        assert e.field is not None,"e.field is None for %s.%s" % (lh.layout,name)
        lh._store_fields.append(e.field)
        return e
        #return FieldElement(self,field,**kw)
        


    def main_panel_class(self,layout):
        if isinstance(layout,layouts.RowLayout) : 
            return ext_elems.GridMainPanel
        if isinstance(layout,layouts.PageLayout) : 
            return ext_elems.DetailMainPanel
        if isinstance(layout,layouts.FormLayout) : 
            return ext_elems.FormMainPanel
        raise Exception("No element class for layout %r" % layout)
            

    
    def save_window_config(self,name,wc):
        self.window_configs[name] = wc
        f = open(self.window_configs_file,'wb')
        pickle.dump(self.window_configs,f)
        f.close()
        self._response = None

    def get_window_config(self,name):
        return self.window_configs.get(name,None)

  
    def get_urls(self):
        return patterns('',
            (r'^$', self.index_view),
            (r'^menu$', self.menu_view),
            (r'^submit_property$', self.submit_property_view),
            (r'^list/(?P<app_label>\w+)/(?P<rptname>\w+)$', self.list_report_view),
            (r'^csv/(?P<app_label>\w+)/(?P<rptname>\w+)$', self.csv_report_view),
            (r'^grid_action/(?P<app_label>\w+)/(?P<rptname>\w+)/(?P<grid_action>\w+)$', self.json_report_view),
            (r'^grid_afteredit/(?P<app_label>\w+)/(?P<rptname>\w+)$', self.grid_afteredit_view),
            (r'^submit/(?P<app_label>\w+)/(?P<rptname>\w+)$', self.form_submit_view),
            (r'^form/(?P<app_label>\w+)/(?P<actor>\w+)/(?P<action>\w+)$', self.act_view),
            (r'^form/(?P<app_label>\w+)/(?P<actor>\w+)$', self.act_view),
            (r'^action/(?P<app_label>\w+)/(?P<actor>\w+)$', self.act_view),
            (r'^step_dialog$', self.step_dialog_view),
            (r'^abort_dialog$', self.abort_dialog_view),
            (r'^choices/(?P<app_label>\w+)/(?P<rptname>\w+)/(?P<fldname>\w+)$', self.choices_view),
            #~ (r'^save_win/(?P<name>\w+)$', self.save_win_view),
            (r'^save_window_config$', self.save_window_config_view),
            (r'^permalink_do/(?P<name>\w+)$', self.permalink_do_view),
            #~ (r'^props/(?P<app_label>\w+)/(?P<model_name>\w+)$', self.props_view),
            # (r'^props$', self.props_view),
        )
        

    def index_view(self, request):
        if self._response is None:
            lino.log.debug("building extjs._response...")
            from lino.lino_site import lino_site
            comp = ext_elems.VisibleComponent("index",
                xtype="panel",
                html=lino_site.index_html.encode('ascii','xmlcharrefreplace'),
                autoScroll=True,
                #width=50000,
                #height=50000,
                region="center")
            vp = ext_viewport.Viewport(lino_site.title,comp)
            s = vp.render_to_html(request)
            self._response = HttpResponse(s)
        return self._response

    def menu_view(self,request):
        from lino import lino_site
        return json_response(lino_site.get_menu(request))
        #~ s = py2js(lino_site.get_menu(request))
        #~ return HttpResponse(s, mimetype='text/html')

    def act_view(self,request,app_label=None,actor=None,action=None,**kw):
        actor = actors.get_actor2(app_label,actor)
        dlg = ext_requests.Dialog(request,self,actor,action)
        return self.start_dialog(dlg)
        
    def start_dialog(self,dlg):
        r = dlg._start().as_dict()
        lino.log.debug('ExtUI.start_dialog(%s) -> %r',dlg,r)
        return json_response(r)
        
    def step_dialog_view(self,request):
        return self.json_dialog_view_(request,'_step')
        
    def abort_dialog_view(self,request):
        return self.json_dialog_view_(request,'_abort')
        
    def json_dialog_view_(self,request,meth_name,**kw):
        dialog_id = long(request.POST.get('dialog_id'))
        dlg = actions.get_dialog(dialog_id)
        if dlg is None:
            return json_response(actions.DialogResponse(
              alert_msg=_('No dialog %r running on this server.' % dialog_id)
              ).as_dict())
        if dlg.request.user != request.user:
            #~ print 20100218, dlg.request.user, '!=', request.user
            return json_response(actions.DialogResponse(
              alert_msg=_('Dialog %r ist not for you.' % dialog_id)
              ).as_dict())
        dlg.request = request
        m = getattr(dlg,meth_name)
        r = m().as_dict()
        lino.log.debug('%s.%s() -> %r',dlg,meth_name,r)
        return json_response(r)
        
    def submit_property_view(self,request):
        rpt = properties.PropValuesByOwner()
        if not rpt.can_change.passes(request):
            return json_response_kw(success=False,
                msg="User %s cannot edit %s." % (request.user,rpt))
        rh = rpt.get_handle(self)
        rr = ext_requests.BaseViewReportRequest(request,rh)
        name = request.POST.get('name')
        value = request.POST.get('value')
        try:
            p = properties.Property.objects.get(pk=name)
        except properties.Property.DoesNotExist:
            return json_response_kw(success=False,
                msg="No property named %r." % name)
        p.set_value_for(rr.master_instance,value)
        return json_response_kw(success=True,msg='%s : %s = %r' % (rr.master_instance,name,value))
    
        
    def permalink_do_view(self,request,name=None):
        name = name.replace('_','.')
        actor = actors.get_actor(name)
        dlg = ext_requests.Dialog(request,self,actor,None)
        return self.start_dialog(dlg)

    def save_window_config_view(self,request):
        actor = SaveWindowConfig()
        dlg = ext_requests.Dialog(request,self,actor,None)
        return self.start_dialog(dlg)
        
    #~ def save_win_view(self,request,name=None):
        #~ #print 'save_win_view()',name
        #~ actor = SaveWindowConfig()
        #~ dlg = ext_requests.Dialog(request,self,actor,None,name)
        #~ return self.start_dialog(dlg)
        

    #~ def props_view(self,request,**kw):
        #~ rh = properties.PropValuesByOwner().get_handle(self)
        #~ rr = ext_requests.ViewReportRequest(request,rh)
        #~ r = rr.render_to_json()
        #~ return json_response(r)
        

    def choices_view(self,request,app_label=None,rptname=None,fldname=None,**kw):
        rpt = actors.get_actor2(app_label,rptname)
        kw['choices_for_field'] = fldname
        return self.json_report_view_(request,rpt,**kw)
        
        
    def grid_afteredit_view(self,request,**kw):
        kw['colname'] = request.POST['grid_afteredit_colname']
        kw['submit'] = True
        return self.json_report_view(request,**kw)

    def form_submit_view(self,request,**kw):
        kw['submit'] = True
        return self.json_report_view(request,**kw)

    def list_report_view(self,request,**kw):
        #kw['simple_list'] = True
        return self.json_report_view(request,**kw)
        
    def csv_report_view(self,request,**kw):
        kw['csv'] = True
        return self.json_report_view(request,**kw)
        
    def json_report_view(self,request,app_label=None,rptname=None,**kw):
        rpt = actors.get_actor2(app_label,rptname)
        return self.json_report_view_(request,rpt,**kw)

    def json_report_view_(self,request,rpt,grid_action=None,colname=None,submit=None,choices_for_field=None,csv=False):
        if not rpt.can_view.passes(request):
            return self.json_response_kw(success=False,
                msg="User %s cannot view %s." % (request.user,rpt))
        if grid_action:
            dlg = ext_requests.GridDialog(request,self,rpt,grid_action)
            return self.start_dialog(dlg)
                
        rh = rpt.get_handle(self)
        if choices_for_field:
            rptreq = ext_requests.ChoicesReportRequest(request,rh,choices_for_field)
        elif csv:
            rptreq = ext_requests.CSVReportRequest(request,rh)
            return rptreq.render_to_csv()
        else:
            rptreq = ext_requests.ViewReportRequest(request,rh)
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
        d = rptreq.render_to_dict()
        return json_response(d)
        

        

    def get_action_url(self,a,**kw):
        url = "/action/" + a.app_label + "/" + a.name 
        if len(kw):
            url += "?" + urlencode(kw)
        return url
        
    def get_form_url(self,fh,**kw):
        url = "/form/" + fh.form.app_label + "/" + fh.form.name 
        if len(kw):
            url += "?" + urlencode(kw)
        return url
        
    def get_button_url(self,btn,**kw):
        a = btn.lh.link.actor
        return build_url("/form",a.app_label,a.name,btn.name,**kw)
        
    def get_choices_url(self,fke,**kw):
        return build_url("/choices",fke.lh.link.report.app_label,fke.lh.link.report.name,fke.field.name,**kw)
        
    #~ def get_props_url(self,model,**kw):
        #~ return build_url('/props')
        
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
        url += rh.report.app_label + "/" + rh.report.name
        if grid_action:
            url += "/" + grid_action
        if master_instance is not None:
            kw[ext_requests.URL_PARAM_MASTER_PK] = master_instance.pk
            mt = ContentType.objects.get_for_model(master_instance.__class__).pk
            kw[ext_requests.URL_PARAM_MASTER_TYPE] = mt
        if len(kw):
            url += "?" + urlencode(kw)
        return url
        
        
        
        
        
    def view_report(self,dlg,**kw):
        """
        called from Report.view()
        """
        rpt = dlg.actor
        rh = self.get_report_handle(rpt)
        rr = ext_requests.ViewReportRequest(dlg.request,rh)
        #~ layout = dlg.request.GET.get('layout')
        #~ if layout is None:
            #~ lh = rh.layouts[rpt.default_layout]
        #~ else:
            #~ lh = rh.layouts[int(layout)]
        #lh = rr.layout 
        # kw['defaultButton'] = js_code('this.main_grid')
        #~ kw = self.window_options(lh,**kw)
        lh = rr.layout
        job = ext_elems.Reaction(rr) #,lh._main)
        yield dlg.exec_js(job.as_ext_value).over()
        #~ yield dlg.exec_js(lh._main.js_job_constructor(rr)).over()
        
        
    def view_form(self,dlg,**kw):
        "called from ViewForm.run_in_dlg()"
        frm = dlg.actor
        fh = self.get_form_handle(frm)
        fr = ext_requests.ViewFormRequest(dlg.request,fh)
        #fh.setup()
        lh = fh.lh
        #~ kw = self.window_options(lh,**kw)
        #rr = None
        job = ext_elems.Reaction(fr) #,fr.lh._main)
        yield dlg.exec_js(job.as_ext_value).over()
     #~ yield dlg.exec_js(lh._main.js_job_constructor(fr)).over()
        
        
    def setup_report(self,rh):
        if rh.report.use_layouts:
            rh.store = ext_store.Store(rh)
        else:
            rh.store = None
        #~ props = properties.Property.properties_for_model(rh.report.model)
        pw = ext_elems.PropertiesWindow(self,rh.report.model)
        if not pw.has_properties():
            pw = None
        rh.properties_window = pw
        #~ if rh.report.model._lino_properties_window.has_properties():
            #~ rh.props = ext_elems.PropertiesWindow(self,rh.report.model,props)
            #~ rh.props = props
        #~ else:
            #~ rh.props = None

    def setup_form(self,fh):
        fh.properties_window = None

ui = ExtUI()