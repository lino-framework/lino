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

from django.db import models
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
from lino.utils import perms, menus, actors

from lino.modlib.tools import resolve_model, resolve_field, get_app

def base_attrs(cl):
    #~ if cl is Report or len(cl.__bases__) == 0:
        #~ return
    #~ myattrs = set(cl.__dict__.keys())
    for b in cl.__bases__:
        for k in base_attrs(b):
            yield k
        for k in b.__dict__.keys():
            yield k

    
def add_quick_search_filter(qs,model,search_text):
    q = models.Q()
    for field in model._meta.fields:
        if isinstance(field,models.CharField):
            kw = {field.name+"__contains": search_text}
            q = q | models.Q(**kw)
    return qs.filter(q)
        


class ReportParameterForm(forms.Form):
    #~ pgn = forms.IntegerField(required=False,label="Page number") 
    #~ pgl = forms.IntegerField(required=False,label="Rows per page")
    flt = forms.CharField(required=False,label="Text filter")
    #~ fmt = forms.ChoiceField(required=False,label="Format",choices=(
      #~ ( 'form', "editable form" ),
      #~ ( 'show', "read-only display" ),
      #~ ( 'text', "plain text" ),
    #~ ))
    


def rc_name(rptclass):
    return rptclass.app_label + '.' + rptclass.__name__
    
master_reports = []
slave_reports = []
generic_slaves = {}

def register_report(cls):
    #rptclass.app_label = rptclass.__module__.split('.')[-2]
    if cls.typo_check:
        myattrs = set(cls.__dict__.keys())
        for attr in base_attrs(cls):
            myattrs.discard(attr)
        if len(myattrs):
            lino.log.warning("%s defines new attribute(s) %s", cls, ",".join(myattrs))
    
    if cls.model is None:
        lino.log.debug("%s is an abstract report", cls)
        return
        
    rpt = cls()
    if rpt.master is None:
        master_reports.append(rpt)
        if rpt.use_as_default_report:
            lino.log.debug("register %s : model_report for %r", rpt.actor_id, rpt.model)
            rpt.model._lino_model_report = rpt
        else:
            lino.log.debug("register %s: not used as model_report",rpt.actor_id)
    elif rpt.master is ContentType:
        lino.log.debug("register %s : generic slave for %r", rpt.actor_id, rpt.fk_name)
        generic_slaves[rpt.actor_id] = rpt
    else:
        slave_reports.append(rpt)

    
def setup():
    """
    - Each model can receive a number of "slaves". 
      Slaves are reports that display detail data for a known instance of that model (their master).
      They are stored in a dictionary called '_lino_slaves'.
      
    - For each model we want to find out the "model report" ot "default report".
      The "choices report" for a foreignkey field is also currently simply the pointed model's
      model_report.
      `_lino_model_report`

    """
    lino.log.debug("Register Report actors...")
    for cls in actors.actors_dict.values():
        if issubclass(cls,Report) and cls is not Report:
            register_report(cls)
    
    lino.log.debug("Instantiate model reports...")
    for model in models.get_models():
        rpt = getattr(model,'_lino_model_report',None)
        if rpt is None:
            cls = report_factory(model)
            register_report(cls)
            model._lino_model_report = cls()
            
    lino.log.debug("Analyze %d slave reports...",len(slave_reports))
    for rpt in slave_reports:
        slaves = getattr(rpt.master,"_lino_slaves",None)
        if slaves is None:
            slaves = {}
            #~ setattr(rpt.master,'_lino_slaves',slaves)
            rpt.master._lino_slaves = slaves
        slaves[rpt.actor_id] = rpt
        lino.log.debug("%s: slave for %s",rpt.actor_id, rpt.master.__name__)
    lino.log.debug("Assigned %d slave reports to their master.",len(slave_reports))
        
    lino.log.debug("Setup model reports...")
    for model in models.get_models():
        model._lino_model_report.setup()
        
    #~ lino.log.debug("Instantiate property editors...")
    #~ for model in models.get_models():
        #~ pw = ext_elems.PropertiesWindow(model)
        #~ model._lino_properties_window = pw
            
    lino.log.debug("reports.setup() done")

def get_slave(model,name):
    try:
        rpt = actors.get_actor(name)
    except KeyError:
        return None
    if rpt.master is not ContentType:
        assert issubclass(model,rpt.master), "%s.master is %r,\nmust be subclass of %r" % (name,rpt.master,model)
    return rpt
    #~ rpt = generic_slaves.get(name,None)
    #~ if rpt is not None:
        #~ return rpt
    #~ for b in (model,) + model.__bases__:
        #~ d = getattr(b,"_lino_slaves",None)
        #~ if d:
            #~ rpt = d.get(name,None)
            #~ if rpt is not None:
                #~ return rpt

def get_model_report(model):
    return model._lino_model_report

class ViewReport(actions.Action):
    def run_in_dlg(self,dlg):
        return dlg.ui.view_report(dlg)
        

class Report(actors.Actor): # actions.Action): # 
    #__metaclass__ = ReportMetaClass
    params = {}
    field = None
    queryset = None 
    model = None
    use_as_default_report = True
    order_by = None
    filter = None
    exclude = None
    title = None
    columnNames = None
    #label = None
    param_form = ReportParameterForm
    #default_filter = ''
    #name = None
    form_class = None
    master = None
    slaves = None
    fk_name = None
    help_url = None
    #master_instance = None
    page_length = 10
    display_field = '__unicode__'
    boolean_texts = ('Ja','Nein',' ')
    #date_format = 'Y-m-d'
    date_format = 'd.m.y'
    #date_format = '%d.%m.%y'
    
    page_layouts = (layouts.PageLayout ,)
    row_layout_class = None
    
    can_view = perms.always
    can_add = perms.is_authenticated
    can_change = perms.is_authenticated
    can_delete = perms.is_authenticated
    
    default_action = ViewReport()
    default_layout = 1
    
    typo_check = True
    url = None
    actions = []
    
    use_layouts = True
    
    def __init__(self):
        actors.Actor.__init__(self)
        #actions.Action.__init__(self)
        lino.log.debug("Report.__init__() %s", self.actor_id)
        self._handles = {}
        self._setup_done = False
        self._setup_doing = False
        #~ self.actions = self.actions + [ actions.ShowProperties(), actions.DeleteSelected(), actions.InsertRow() ]
        self.actions = self.actions + [ actions.DeleteSelected(), actions.InsertRow() ]
        
        #~ if self.field is None:
        if self.model is None:
            if self.queryset is not None:
                self.model = self.queryset.model
            # raise Exception(self.__class__)
        else:
            self.model = resolve_model(self.model,self.app_label,self)
        
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
        
    def setup(self):
        if self._setup_done:
            return True
        if self._setup_doing:
            if True: # severe error handling
                raise Exception("%s.setup() called recursively" % self.actor_id)
            else:
                lino.log.warning("%s.setup() called recursively" % self.actor_id)
                return False
        self._setup_doing = True
        
        #self._actions = [cl(self) for cl in self.actions]
        
        setup = getattr(self.model,'setup_report',None)
        if setup:
            setup(self)
        
        if hasattr(self.model,'_lino_slaves'):
            if self.slaves is None:
                #self._slaves = [sl() for sl in self.model._lino_slaves.values()]
                self._slaves = self.model._lino_slaves.values()
            else:
                raise Exception("20091120 no longer possible")
                self._slaves = []
                for slave_name in self.slaves.split():
                    sl = get_slave(self.model,slave_name)
                    if sl is None:
                        lino.log.info(
                            "[Warning] invalid name %s in %s.slaves" % (
                                slave_name,self.actor_id))
                    self._slaves.append(sl)
        else:
            self._slaves = []

        self._setup_doing = False
        self._setup_done = True
        lino.log.debug("Report.setup() done: %s", self.actor_id)
        return True
        
    # implements actions.Action
    def get_url(self,ui,**kw):
        kw['run'] = True
        rh = self.get_handle(ui)
        return rh.get_absolute_url(**kw)
        #return ui.get_report_url(rh,**kw)
        
        
    # implements actors.Actor
    def get_handle(self,ui):
        #~ assert isinstance(ui,BaseUI)
        return ui.get_report_handle(self)
        
    def get_action(self,name):
        for a in self.actions:
            if a.name == name:
                return a
        return actors.Actor.get_action(self,name)
              
    def add_actions(self,*args):
        """Used in Model.setup_report() to specify actions for each report that uses 
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

        
            
    def get_title(self,rr):
        #~ if self.title is None:
            #~ return self.label
        
            
        title = self.title or self.label
        if self.master is not None:
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
            qs = add_quick_search_filter(qs,self.model,rr.quick_search)
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
        
    def get_field_choices_meth(self,fld):
        # used also in extjs to test whether this field does have context-sensitive choices
        methname = fld.name + "_choices"
        return getattr(self.model,methname,None)
        
    def get_field_choices(self,fld,pk,quick_search=None):
        # pk is the primary key of the "receiving" instance (who is asking for a list of choices)
        # query is a string typed by user to filter the choices
        meth = self.get_field_choices_meth(fld)
        choices = None
        if meth is not None:
            try:
                #recipient = fld.rel.to.objects.get(pk=pk)
                recipient = self.model.objects.get(pk=pk)
            except self.model.DoesNotExist:
                pass
            else:
                choices = meth(recipient)
        if choices is None:
            choices = fld.rel.to.objects.all()
        if quick_search is not None:
            choices = add_quick_search_filter(choices,fld.rel.to,quick_search)
        return choices
        # return get_model_report(field.rel.to)
        #return field._lino_choice_report
        #~ rpt = getattr(field,'_lino_choice_report',None)
        #~ if rpt is None:
            #~ return get_model_report(field.rel.to)
        #~ return rpt
        
        
    @classmethod
    def register_page_layout(cls,*layouts):
        cls.page_layouts = tuple(cls.page_layouts) + layouts
        
    def row2dict(self,row,d):
        "Overridden by lino.modlib.properties.PropValuesByOwner"
        for n in self.columnNames.split():
            d[n] = getattr(row,n)
        return d
        
    def render_to_dict(self,**kw):
        rh = ReportHandle(None,self)
        rr = rh.request(**kw)
        return rr.render_to_dict()

        
def report_factory(model):
    lino.log.debug('report_factory(%s) -> app_label=%r',model.__name__,model._meta.app_label)
    return type(model.__name__+"Report",(Report,),dict(model=model,app_label=model._meta.app_label))

#~ def choice_report_factory(model,field):
    #~ clsname = model.__name__+"_"+field.name+'_'+"Choices"
    #~ fldname = model._meta.app_label+'.'+model.__class__.__name__+'.'+field.name
    #~ return type(clsname,(Report,),dict(field=fldname,app_label=model._meta.app_label,columnNames='__unicode__'))

def get_unbound_meth(cl,name):
    meth = getattr(cl,name,None)
    if meth is not None:
        return meth
    for b in cl.__bases__:
        meth = getattr(b,name,None)
        if meth is not None:
            return meth

class ReportHandle(layouts.DataLink):
    def __init__(self,ui,report):
        #lino.log.debug('ReportHandle.__init__(%s)',rd)
        layouts.DataLink.__init__(self,ui,report.actor_id)
        assert isinstance(report,Report)
        #self._rd = rd
        self.actor = self.report = report
        #~ for n in 'get_fields', 'get_slave','try_get_field','try_get_meth',
                  #~ 'get_title'):
            #~ setattr(self,n,getattr(report,n))
        self.content_type = ContentType.objects.get_for_model(self.report.model).pk
            
    def __str__(self):
        return self.report.name + 'Handle'
            
    def setup(self):
        if self.report.use_layouts:
            def lh(layout_class,*args,**kw):
                return layouts.LayoutHandle(self,layout_class(),*args,**kw)
            
            self.choice_layout = lh(layouts.RowLayout,0,self.report.display_field)
            
            index = 1
            if self.report.row_layout_class is None:
                self.row_layout = lh(layouts.RowLayout,index,self.report.columnNames)
            else:
                assert self.report.columnNames is None
                self.row_layout = lh(self.report.row_layout_class,index)
                
            self.layouts = [ self.choice_layout, self.row_layout ]
            index = 2
            for lc in self.report.page_layouts:
                self.layouts.append(lh(lc,index))
                index += 1
        self.ui.setup_report(self)
        
    def get_absolute_url(self,*args,**kw):
        return self.ui.get_report_url(self,*args,**kw)
        
    def data_elems(self):
        for f in self.report.model._meta.fields: yield f.name
        for f in self.report.model._meta.many_to_many: yield f.name
        for f in self.report.model._meta.virtual_fields: yield f.name
        # todo: for slave in self.report.slaves
          
    def get_data_elem(self,name):
        try:
            return self.report.model._meta.get_field(name)
        except models.FieldDoesNotExist,e:
            pass
        rpt = get_slave(self.report.model,name)
        if rpt is not None: return rpt
        m = get_unbound_meth(self.report.model,name)
        if m is not None: return m
        
        for vf in self.report.model._meta.virtual_fields:
            if vf.name == name:
                return vf
                
    def get_actions(self):
        return self.report.actions
        
    def get_details(self):
        return self.layouts[1:]
          
    def get_slaves(self):
        return [ sl.get_handle(self.ui) for sl in self.report._slaves ]
            
    def get_title(self,rr):
        return self.report.get_title(rr)
        
    def request(self,**kw):
        rr = ReportRequest(self)
        rr.setup(**kw)
        return rr
        
    
class ReportRequest:
    """
    An instance of this will be created for every request.
    
    """
    limit = None
    offset = None
    master_instance = None
    master = None
    instance = None
    extra = None
    layout = None
    
    def __init__(self,rh):
        assert isinstance(rh,ReportHandle)
        self.report = rh.report
        self.rh = rh
        self.ui = rh.ui
        # Subclasses (e.g. BaseViewReportRequest) may set `master` before calling ReportRequest.__init__()
        if self.master is None:
            self.master = rh.report.master
      
    def __str__(self):
        return self.__class__.__name__ + '(' + self.report.actor_id + ",%r,...)" % self.master_instance

    def setup(self,
            master=None,
            master_instance=None,
            offset=None,limit=None,
            layout=None,user=None,
            extra=None,quick_search=None,
            order_by=None,
            **kw):
        self.user = user
        self.quick_search = quick_search
        self.order_by = order_by
        
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
                layout = self.rh.layouts[self.report.default_layout]
            else:
                layout = self.rh.layouts[layout]
                #~ assert isinstance(layout,layouts.LayoutHandle), \
                    #~ "Value %r is not a LayoutHandle" % layout
            self.layout = layout
        self.report.setup_request(self)
        self.setup_queryset()
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

    def get_title(self):
        return self.report.get_title(self)
        
    def __iter__(self):
        return self.queryset.__iter__()
        
    def create_instance(self,**kw):
        kw.update(self.master_kw)
        #lino.log.debug('%s.create_instance(%r)',self,kw)
        return self.report.create_instance(self,**kw)
        
    def get_user(self):
        raise NotImplementedError
        
    def setup_queryset(self):
        # overridden by ChoicesReportRequest
        self.queryset = self.report.get_queryset(self)
        #~ return self.report.get_queryset(master_instance=self.master_instance,**kw)
        
    def render_to_dict(self):
        rows = [ self.row2dict(row,{}) for row in self.queryset ]
        #~ rows = []
        #~ for row in self.queryset:
            #~ d = self.row2dict(row,{})
            #~ rows.append(d)
        total_count = self.total_count
        #lino.log.debug('%s.render_to_dict() total_count=%d extra=%d',self,total_count,self.extra)
        # add extra blank row(s):
        for i in range(0,self.extra):
            row = self.create_instance()
            #~ d = self.row2dict(row,{})
            #~ rows.append(d)
            rows.append(self.row2dict(row,{}))
            total_count += 1
        return dict(count=total_count,rows=rows,title=self.report.get_title(self))
        
    def row2dict(self,row,d):
        # overridden in extjs.ViewReport
        return self.report.row2dict(row,d)
        


