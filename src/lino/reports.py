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


import traceback
#import logging ; logger = logging.getLogger('lino.reports')

from django.conf import settings
from django.utils.importlib import import_module
from django.utils.translation import ugettext as _

from django.db import models
from django.db.models.query import QuerySet
from django import forms
from django.conf.urls.defaults import patterns, url, include
from django.forms.models import modelform_factory
from django.forms.models import _get_foreign_key
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType


from django.http import HttpResponse
#from django.core import serializers
#from django.shortcuts import render_to_response
#from django.utils import simplejson
from django.utils.safestring import mark_safe

try:
    # l:\snapshot\xhtml2pdf
    import ho.pisa as pisa
except ImportError:
    pisa = None




import lino
from lino import layouts
from lino import actions
from lino.utils import perms, menus
from lino.core import datalinks
from lino.core import actors
#~ from lino.core import action_requests
from lino.ui import base

from lino.modlib.tools import resolve_model, resolve_field, get_app, model_label
from lino.core.coretools import get_slave, get_model_report, data_elems, get_data_elem

#~ from lino.modlib import field_choices

def base_attrs(cl):
    #~ if cl is Report or len(cl.__bases__) == 0:
        #~ return
    #~ myattrs = set(cl.__dict__.keys())
    for b in cl.__bases__:
        for k in base_attrs(b):
            yield k
        for k in b.__dict__.keys():
            yield k


def add_quick_search_filter(qs,search_text):
    if not isinstance(qs,QuerySet): 
        # TODO: filter also simple lists 
        return qs
    q = models.Q()
    for field in qs.model._meta.fields:
        if isinstance(field,models.CharField):
            kw = {field.name+"__contains": search_text}
            q = q | models.Q(**kw)
    return qs.filter(q)
        

def rc_name(rptclass):
    return rptclass.app_label + '.' + rptclass.__name__
    
master_reports = []
slave_reports = []
generic_slaves = {}

def register_report(rpt):
    #rptclass.app_label = rptclass.__module__.split('.')[-2]
    if rpt.typo_check:
        myattrs = set(rpt.__class__.__dict__.keys())
        for attr in base_attrs(rpt.__class__):
            myattrs.discard(attr)
        if len(myattrs):
            lino.log.warning("%s defines new attribute(s) %s", rpt.__class__, ",".join(myattrs))
    
    if rpt.model is None:
        lino.log.debug("%s is an abstract report", rpt)
        return
        
    #~ rpt = cls()
    if rpt.master is None:
        master_reports.append(rpt)
        if rpt.use_as_default_report:
            lino.log.debug("register %s : model_report for %s", rpt.actor_id, model_label(rpt.model))
            rpt.model._lino_model_report = rpt
        else:
            lino.log.debug("register %s: not used as model_report",rpt.actor_id)
    elif rpt.master is ContentType:
        lino.log.debug("register %s : generic slave for %r", rpt.actor_id, rpt.fk_name)
        generic_slaves[rpt.actor_id] = rpt
    else:
        slave_reports.append(rpt)

    
    
def discover():
    """
    - Each model can receive a number of "slaves". 
      Slaves are reports whose data depends on an instance of another model (their master).
      
    - For each model we want to find out the "model report" ot "default report".
      The "choices report" for a foreignkey field is also currently simply the pointed model's
      model_report.
      `_lino_model_report`

    """
    
    lino.log.info("Analyzing Reports...")
    lino.log.debug("Register Report actors...")
    for rpt in actors.actors_dict.values():
        if isinstance(rpt,Report) and rpt.__class__ is not Report:
            register_report(rpt)
            
    lino.log.debug("Instantiate model reports...")
    for model in models.get_models():
        rpt = getattr(model,'_lino_model_report',None)
        if rpt is None:
            rpt = report_factory(model)
            register_report(rpt)
            model._lino_model_report = rpt
            
    lino.log.debug("Analyze %d slave reports...",len(slave_reports))
    for rpt in slave_reports:
        slaves = getattr(rpt.master,"_lino_slaves",None)
        if slaves is None:
            slaves = {}
            rpt.master._lino_slaves = slaves
        slaves[rpt.actor_id] = rpt
        lino.log.debug("%s: slave for %s",rpt.actor_id, rpt.master.__name__)
    lino.log.debug("Assigned %d slave reports to their master.",len(slave_reports))
        
    #~ lino.log.debug("Setup model reports...")
    #~ for model in models.get_models():
        #~ model._lino_model_report.setup()
        
    #~ lino.log.debug("Instantiate property editors...")
    #~ for model in models.get_models():
        #~ pw = ext_elems.PropertiesWindow(model)
        #~ model._lino_properties_window = pw
            
    lino.log.debug("reports.setup() done")

class GridEdit(actions.OpenWindowAction):
  
    name = 'grid'
    
    def __init__(self,rpt):
        self.label = rpt.label
        actions.Action.__init__(self,rpt)

        
        
        

class InsertRow(actions.RowsAction):
    label = _("Insert")
    name = 'insert'
    key = actions.INSERT # (ctrl=True)
    
    def run_action(self,ar):
        #~ rr = dlg.get_request()
        #~ for r in rr.insert_row(self): 
            #~ yield r
            
        #~ if ar.rh.detail_link is None:
            #~ raise Exception("This report has no detail layout")
        
        row = ar.create_instance()
        
        return ar.show_detail(row)
        
        #~ layout = layouts.get_detail_layout(row.__class__)
        
        #~ if layout is None:
        #~ dl = RowDataLink(rr.ui,row)
        #~ dl.setup()
        #~ lh = layout.get_handle(rr.ui)
        #~ return rr.show_window(dl,lh)
        
        #~ fh = actions.FormHandle(lh,dl)
        #~ yield dlg.show_modal_form(fh)
        #~ while True:
            #~ if dlg.modal_exit != 'ok':
                #~ yield dlg.cancel()
            #~ print dlg.params
            #~ if row.update(dlg.params):
                #~ row.save()
                #~ yield dlg.refresh_caller().over()
        
    def old_run_in_dlg(self,dlg):
        yield dlg.confirm(_("Insert new row. Are you sure?"))
        rr = dlg.get_request()
        row = rr.create_instance()
        row.save()
        yield dlg.refresh_caller().over()
        
        
  
class DeleteSelected(actions.RowsAction):
    needs_selection = True
    label = _("Delete")
    name = 'delete'
    key = actions.DELETE # (ctrl=True)
    
        
    def run_action(self,rr):
        if len(dlg.selected_rows) == 1:
            msg = _("Deleted row %s") % dlg.selected_rows[0]
        else:
            msg = _("Deleted %d rows") % len(dlg.selected_rows)
            
        for row in dlg.selected_rows:
            row.delete()
        return rr.refresh_caller().notify(_("Success") + ": " + msg)
        
class DetailAction(actions.ToggleWindowAction):
    name = 'detail'
    def __init__(self,actor,layout):
        self.layout = layout
        self.label = layout.label
        actions.ToggleWindowAction.__init__(self,actor)
        
                
class SlaveGridAction(actions.ToggleWindowAction):
  
    def __init__(self,actor,slave):
        assert isinstance(slave,Report)
        self.slave = slave # .get_handle(ah.ui)
        self.name = slave._actor_name
        #~ print 20100415,self.name
        self.label = slave.button_label
        actions.ToggleWindowAction.__init__(self,actor)
        
        

class ReportHandle(datalinks.DataLink,base.Handle): #,actors.ActorHandle):
  
    #~ properties = None
    
    #~ detail_link = None
    
    
    def __init__(self,ui,report):
        #lino.log.debug('ReportHandle.__init__(%s)',rd)
        assert isinstance(report,Report)
        self.report = report
        self._layouts = None
        #~ actors.ActorHandle.__init__(self,report)
        datalinks.DataLink.__init__(self,ui)
        base.Handle.__init__(self,ui)
        if self.report.use_layouts:
            self.list_layout = self.report.list_layout.get_handle(self.ui)
        
  
    def __str__(self):
        return str(self.report) + 'Handle'
            
    def setup_layouts(self):
        if self._layouts is not None:
            return
        #~ self.default_action = self.report.default_action(self)
        if self.report.use_layouts:
            self._layouts = [ self.list_layout ] + [ dtl.layout.get_handle(self.ui) for dtl in self.report.details ]
            #~ if len(self.details) > 0:
                #~ self.detail_link = DetailDataLink(self,self.details[0])
                
                
        else:
            self._layouts = []
            
        #~ base.Handle.setup(self)    
        #~ if self.report.use_layouts:
            #~ def lh(layout_class,*args,**kw):
                #~ return layouts.LayoutHandle(self,layout_class(),*args,**kw)
            
            #~ self.choice_layout = lh(layouts.RowLayout,0,self.report.display_field)
            
            #~ index = 1
            #~ self.list_layout = lh(layouts.RowLayout,index,self.report.column_names)
            
            #~ self.layouts = [ self.choice_layout, self.row_layout ]
            #~ index = 2
            #~ for lc in self.report.page_layouts:
                #~ self.layouts.append(lh(lc,index))
                #~ index += 1
        #~ else:
            #~ self.choice_layout = None
            #~ self.row_layout = None
            #~ self.layouts = []
            
        
    #~ def get_default_layout(self):
        #~ return self.layouts[self.report.default_layout]
        
    #~ def get_create_layout(self):
        #~ return self.layouts[2]
        
    def submit_elems(self):
        return []
        
    def get_layout(self,i):
        self.setup_layouts()
        return self._layouts[i]
        
    def get_used_layouts(self):
        self.setup_layouts()
        return self._layouts
        
        
    def get_absolute_url(self,*args,**kw):
        return self.ui.get_report_url(self,*args,**kw)
        
    def data_elems(self):
        for de in data_elems(self.report.model._meta): yield de
          
    def get_data_elem(self,name):
        return get_data_elem(self.report.model,name)
        
    def get_action(self,name):
        return self.report.get_action(name)
    def get_actions(self):
        return self.report.get_actions()
        
    def get_details(self):
        return self.report.details
        #~ return self.layouts[1:]
          
    def get_slaves(self):
        return [ sl.get_handle(self.ui) for sl in self.report._slaves ]
            
    def get_title(self,rr):
        return self.report.get_title(rr)
        
    #~ def request(self,**kw):
        #~ return self.ui.get_report_ar(self,**kw)
        
    def request(self,*args,**kw):
        ar = ReportActionRequest(self,self.report.data_action)
        ar.setup(*args,**kw)
        return ar
        
        
            

#~ class RowHandle(datalinks.DataLink):
class unused_DetailDataLink(datalinks.DataLink):
  
    def __init__(self,rh,lh):
        self.rh = rh
        self.lh = lh
        #~ self.rh = get_model_report(row.__class__).get_handle(ui)
        #~ RowHandle.__init__(self,ui,[actions.Cancel(), actions.OK()])
        datalinks.DataLink.__init__(self,rh.ui,[actions.Cancel(), actions.OK()])
        self.inputs = []
        self.row = None
        
    def get_queryset(self,rr):
        return [ self.row ]
        
    #~ def before_step(self,dlg):
        #~ d = self.rh.store.get_from_form(dlg.params)
        #~ dlg.params.update(**d)
        #~ for i in self.rh.store.inputs:
            #~ if isinstance(i,List):
                #~ v = dlg.request.POST.getlist(i.name)
            #~ else:
                #~ v = dlg.request.POST.get(i.name)
            #~ dlg.params[i.name] = v
            
    def data_elems(self):
        return self.rh.data_elems()
        #~ for de in self.rh.data_elems(): yield de
          
    def get_data_elem(self,name):
        return self.rh.get_data_elem(name)
        
    def get_title(self,dlg):
        return unicode(self.row)
        
    #~ def submit_elems(self):
        #~ for name in data_elems(self.row._meta): yield name
        
    #~ def setup(self):
        #~ self.list_layout = rpt.get_handle(self.ui)
        #~ self.details = [ pl.get_handle(self.ui) for pl in rpt.detail_layouts ]
        #~ self.layouts = [ self.list_layout ] + self.details
        #~ self.ui.setup_report(self)
        


class DataAction(actions.Action):
    #~ response_format = 'json' # ext_requests.FMT_JSON
    name = 'data'
    
    def get_queryset(self,ar):
        return self.actor.get_queryset(ar)
        
    def get_title(self,ar):
        return self.actor.get_title(ar)
        
    def render_to_dict(self,ar):
        rows = [ ar.row2dict(row,{}) for row in ar.queryset ]
        #~ rows = []
        #~ for row in self.queryset:
            #~ d = self.row2dict(row,{})
            #~ rows.append(d)
        total_count = ar.total_count
        #lino.log.debug('%s.render_to_dict() total_count=%d extra=%d',self,total_count,self.extra)
        # add extra blank row(s):
        for i in range(0,ar.extra):
            row = ar.create_instance()
            #~ d = self.row2dict(row,{})
            #~ rows.append(d)
            rows.append(ar.row2dict(row,{}))
            total_count += 1
        #~ print 20100420, rows
        return dict(count=total_count,rows=rows,title=ar.get_title())
        
class ChoicesAction(DataAction):
  
    def __init__(self,rpt,fldname):
        self.name = fldname+'_choices'
        self.fieldname = fldname
        DataAction.__init__(self,rpt)
  
    
    def get_queryset(self,ar):
        kw = {}
        for k,v in ar.request.GET.items():
            kw[str(k)] = v
        chooser = ar.rh.choosers[self.fieldname]
        qs = chooser.get_choices(**kw)
        if ar.quick_search is not None:
            qs = add_quick_search_filter(qs,ar.quick_search)
        return qs # self.queryset = qs
        
    def row2dict(self,obj,d):
        d[CHOICES_TEXT_FIELD] = unicode(obj)
        #d['__unicode__'] = unicode(obj)
        d[CHOICES_VALUE_FIELD] = obj.pk # getattr(obj,'pk')
        #d[self.fieldname] = obj.pk 
        return d
    


class ReportActionRequest(actions.ActionRequest): # was ReportRequest
    limit = None
    offset = None
    master_instance = None
    master = None
    instance = None
    extra = None
    layout = None
    
    def __init__(self,rh,action):
    #~ def __init__(self,rpt,action,ui):
        assert isinstance(rh,ReportHandle)
        self.report = rh.report
        self.ui = rh.ui
        # Subclasses (e.g. BaseViewReportRequest) may set `master` before calling ReportRequest.__init__()
        if self.master is None:
            self.master = rh.report.master
        #~ actions.ActionRequest.__init__(self,rpt,action,ui)
        actions.ActionRequest.__init__(self,rh,action)
        #~ self.rh = self.ah
      
    def __str__(self):
        return self.__class__.__name__ + '(' + self.report.actor_id + ",%r,...)" % self.master_instance

    def setup(self,
            master=None,
            master_instance=None,
            offset=None,limit=None,
            layout=None,user=None,
            extra=None,quick_search=None,
            order_by=None,
            selected_rows=None,
            **kw):
        self.user = user
        self.quick_search = quick_search
        self.order_by = order_by
        if selected_rows is not None:
            self.selected_rows = selected_rows
        
        if master is None:
            master = self.report.master
            # master might still be None
        self.master = master
        
        kw.update(self.report.params)
        self.params = kw
        self.master_kw = self.report.get_master_kw(master_instance)
        self.master_instance = master_instance
        if self.extra is None:
            if extra is None:
                if self.master_kw is None:
                    extra = 0
                elif self.report.can_add.passes(self):
                    extra = 1
                else:
                    extra = 0
            self.extra = extra
        if self.report.use_layouts:
            if layout is None:
                layout = self.ah._layouts[self.report.default_layout]
            else:
                layout = self.ah._layouts[layout]
            self.layout = layout
        self.report.setup_request(self)
        self.queryset = self.get_queryset()
        #~ self.setup_queryset()
        #~ lino.log.debug(unicode(self))
        # get_queryset() may return a list
        if isinstance(self.queryset,models.query.QuerySet):
            self.total_count = self.queryset.count()
        else:
            self.total_count = len(self.queryset)
        
        if offset is not None:
            self.queryset = self.queryset[offset:]
            self.offset = offset
            
        #~ if limit is None:
            #~ limit = self.report.page_length
            
        """
        Report.page_length is not a default value for ReportRequest.limit
        For example CSVReportRequest wants all rows.
        """
        if limit is not None:
            self.queryset = self.queryset[:limit]
            self.limit = limit
            
        self.page_length = self.report.page_length

    def get_queryset(self):
        # overridden by ChoicesReportRequest
        return self.action.get_queryset(self)
        #~ return self.report.get_queryset(master_instance=self.master_instance,**kw)
        
    def get_title(self):
        return self.action.get_title(self)
        
    def __iter__(self):
        return self.queryset.__iter__()
        
    def __len__(self):
        return self.queryset.__len__()
        
    def create_instance(self,**kw):
        kw.update(self.master_kw)
        #lino.log.debug('%s.create_instance(%r)',self,kw)
        return self.report.create_instance(self,**kw)
        
    def get_user(self):
        raise NotImplementedError
        
    def render_to_dict(self):
        return self.action.render_to_dict(self)
        
    def row2dict(self,row,d):
        # overridden in extjs.ext_requests.ViewReportRequest
        return self.report.row2dict(row,d)
        
    #~ def run_action(self,ar):
        #~ ar.show_action_window(self) 
        


        
        


class Report(actors.Actor,base.Handled): # actions.Action): # 
    default_action_class = GridEdit
    _handle_class = ReportHandle
    #~ _handle_selector = base.UI
    params = {}
    field = None
    queryset = None 
    model = None
    use_as_default_report = True
    order_by = None
    filter = None
    exclude = None
    title = None
    column_names = None
    hide_columns = None
    #~ hide_fields = None
    #label = None
    #~ param_form = ReportParameterForm
    #default_filter = ''
    #name = None
    form_class = None
    master = None
    #~ slaves = None
    fk_name = None
    help_url = None
    #master_instance = None
    page_length = 10
    display_field = '__unicode__'
    #date_format = 'Y-m-d'
    #date_format = '%d.%m.%y'
    
    #~ page_layout = None # (layouts.PageLayout ,)
    #~ row_layout_class = None
    
    date_format = 'd.m.y'
    boolean_texts = (_('Yes'),_('No'),' ')
    
    can_view = perms.always
    can_add = perms.is_authenticated
    can_change = perms.is_authenticated
    can_delete = perms.is_authenticated
    
    #~ default_action = GridEdit
    default_layout = 0
    
    typo_check = True
    url = None
    
    use_layouts = True
    
    button_label = None
    
    details = []
    
    
    def __init__(self):
        if self.model is None:
            if self.queryset is not None:
                self.model = self.queryset.model
            # raise Exception(self.__class__)
        else:
            self.model = resolve_model(self.model,self.app_label,self)
        if self.model is not None:
            self.app_label = self.model._meta.app_label
            self.actions = self.actions + [ DeleteSelected, InsertRow ]
            m = getattr(self.model,'setup_report',None)
            if m:
                m(self)
                
        
        actors.Actor.__init__(self)
        base.Handled.__init__(self)
        
        #~ lino.log.debug("Report.__init__() %s", self)
        
        if self.fk_name:
            #~ self.master = resolve_model(self.master,self.app_label)
            try:
                fk, remote, direct, m2m = self.model._meta.get_field_by_name(self.fk_name)
                assert direct
                assert not m2m
                master = fk.rel.to
            except models.FieldDoesNotExist,e:
                #~ lino.log.debug("FieldDoesNotExist in %r._meta.get_field_by_name(%r)",self.model,self.fk_name)
                master = None
                for vf in self.model._meta.virtual_fields:
                    if vf.name == self.fk_name:
                        fk = vf
                        master = ContentType
            if master is None:
                raise Exception("%s : no master for fk_name %r in %s" % (
                    self,self.fk_name,self.model.__name__))
            self.master = master
            self.fk = fk
        else:
            assert self.master is None
        #~ elif self.master:
            #~ lino.log.warning("DEPRECATED: replace %s.master by fk_name" % self.actor_id)
            #~ #assert isinstance(self.master,object), "%s.master is a %r" % (self.name,self.master)
            #~ assert issubclass(self.master,models.Model), "%s.master is a %r" % (self.actor_id,self.master)
            #~ self.fk = _get_foreign_key(self.master,self.model) #,self.fk_name)
        
        
        #self.setup()
        
        #register_report(self)
        
        
    @classmethod
    def spawn(cls,suffix,**kw):
        kw['app_label'] = cls.app_label
        return type(cls.__name__+str(suffix),(cls,),kw)
        
    def do_setup(self):
      
        self.default_action = self.default_action_class(self)
        self.data_action = DataAction(self)
        
        actions = [ ac(self) for ac in self.actions ]
          
        if self.model is not None:
            self.list_layout = layouts.list_layout_factory(self)
            self.detail_layouts = getattr(self.model,'_lino_layouts',[])
            if hasattr(self.model,'_lino_slaves'):
                self._slaves = self.model._lino_slaves.values()
            else:
                self._slaves = []
                
        
            if self.use_layouts:
                self.details = [ DetailAction(self,pl) for pl in self.detail_layouts ]
                actions += self.details
                #~ for dtl in self.details:
                    #~ actions.append(dtl)
                #~ else:
                    #~ print 'no detail in %s : %r' % (report,report.detail_layouts)
            
                
        if self.model is not None:
          
            self.content_type = ContentType.objects.get_for_model(self.model).pk
            
            for slave in self._slaves:
                actions.append(SlaveGridAction(self,slave))
                
            from lino.modlib.properties import models as properties
            a = properties.PropertiesAction(self)
            actions.append(a)
            
        actions.append(self.default_action)
        actions.append(self.data_action)
        self.set_actions(actions)
                
        if self.button_label is None:
            self.button_label = self.label

        
    # implements actions.Action
    def unused_get_url(self,ui,**kw):
        kw['run'] = True
        rh = self.get_handle(ui)
        return rh.get_absolute_url(**kw)
        #return ui.get_report_url(rh,**kw)
        
        
    #~ def get_action(self,name):
        #~ for a in self.actions:
            #~ if a.name == name:
                #~ return a
        #~ return actors.Actor.get_action(self,name)
              
    def add_actions(self,*args):
        """Used in Model.setup_report() to specify actions for each report on
        this model."""
        self.actions += args
        #~ for a in more_actions:
            #~ self._actions.append(a)
        
    #~ def unused_ext_components(self):
        #~ if len(self.store.layouts) == 2:
            #~ for s in self.store.layouts:
                #~ yield s._main
        #~ else:
            #~ yield self.store.layouts[0]._main
            #~ comps = [l._main for l in self.store.layouts[1:]]
            #~ yield extjs.TabPanel(None,"EastPanel",*comps)
            
        #~ yield self.layouts[0]._main
        #~ if len(self.layouts) == 2:
            #~ yield self.layouts[1]._main
        #~ else:
            #~ comps = [l._main for l in self.layouts[1:]]
            #~ yield layouts.TabPanel(None,"EastPanel",*comps)

    def data_elems(self):
        for de in data_elems(self.model._meta): yield de
          
    def get_data_elem(self,name):
        return get_data_elem(self.model,name)
        
    def get_details(self):
        return self.details
            
    def get_title(self,rr):
        #~ if self.title is None:
            #~ return self.label
        title = self.title or self.label
        if rr is not None and self.master is not None:
            title += ": " + unicode(rr.master_instance)
        return title
        
    #~ def get_queryset(self,master_instance=None,quick_search=None,order_by=None,**kw):
    def get_queryset(self,rr):
        if self.queryset is not None:
            qs = self.queryset
        else:
            qs = self.model.objects.all()
        kw = self.get_master_kw(rr.master_instance,**rr.params)
        if kw is None:
            return []
        if len(kw):
            qs = qs.filter(**kw)

        if self.filter:
            qs = qs.filter(**self.filter)
        if self.exclude:
            qs = qs.exclude(**self.exclude)
              
        if rr.quick_search is not None:
            #~ qs = add_quick_search_filter(qs,self.model,rr.quick_search)
            qs = add_quick_search_filter(qs,rr.quick_search)
        order_by = rr.order_by or self.order_by
        if order_by:
            qs = qs.order_by(*order_by.split())
        return qs
        
        
    def setup_request(self,req):
        pass
        
    def get_master_kw(self,master_instance,**kw):
        #lino.log.debug('%s.get_master_kw(%r) master=%r',self,kw,self.master)
        if self.master is None:
            assert master_instance is None, "Report %s doesn't accept a master" % self.actor_id
        elif self.master is ContentType:
            if master_instance is None:
                kw[self.fk.ct_field] = None,
                kw[self.fk.fk_field] = None
            else:
                ct = ContentType.objects.get_for_model(master_instance.__class__)
                kw[self.fk.ct_field] = ct
                kw[self.fk.fk_field] = master_instance.pk
        else:
            if master_instance is None:
                if not self.fk.null:
                    return # cannot add rows to this report
                kw[self.fk.name] = master_instance
                
                #kw["%s__exact" % self.fk.name] = None
            elif not isinstance(master_instance,self.master):
                raise Exception("%r is not a %s" % (master_instance,self.master.__name__))
            else:
                kw[self.fk.name] = master_instance
        return kw
        
    def create_instance(self,req,**kw):
        instance = self.model(**kw)
        m = getattr(instance,'on_create',None)
        if m:
            m(req)
        #self.on_create(instance,req)
        return instance
        
    #~ def on_create(self,instance,req):
        #~ pass
        
    def getLabel(self):
        return self.label
        
    #~ def __str__(self):
        #~ return rc_name(self.__class__)
        
    def ajax_update(self,request):
        print request.POST
        return HttpResponse("1", mimetype='text/x-json')


    def as_text(self, *args,**kw):
        from lino.ui import console
        return console.ui.report_as_text(self)
        
    @classmethod
    def unused_register_page_layout(cls,layout):
        if cls.page_layout is not None:
            lino.warning('Detail layout %s in %s overridden by %s',
              cls.page_layout,cls,layout)
        cls.page_layout = layout
        #~ cls.page_layout = tuple(cls.page_layouts) + layouts
        
    #~ def render_to_dict(self,**kw):
        #~ rh = self.get_handle(None) # ReportHandle(None,self)
        #~ rr = self.request(None,**kw)
        #~ return rr.render_to_dict()
        
    def request(self,ui,**kw):
        return self.get_handle(ui).request(**kw)

    def row2dict(self,row,d):
        """
        Overridden by lino.modlib.properties.PropValuesByOwner.
        See also lino.ui.extjs.ext_requests.ViewReportRequest.
        """
        for n in self.column_names.split():
            d[n] = getattr(row,n)
        return d
        
        
def report_factory(model):
    lino.log.debug('report_factory(%s) -> app_label=%r',model.__name__,model._meta.app_label)
    cls = type(model.__name__+"Report",(Report,),dict(model=model,app_label=model._meta.app_label))
    return actors.register_actor(cls())

#~ def choice_report_factory(model,field):
    #~ clsname = model.__name__+"_"+field.name+'_'+"Choices"
    #~ fldname = model._meta.app_label+'.'+model.__class__.__name__+'.'+field.name
    #~ return type(clsname,(Report,),dict(field=fldname,app_label=model._meta.app_label,column_names='__unicode__'))



