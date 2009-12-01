## Copyright 2009 Luc Saffre
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

from lino.modlib.tools import resolve_model, resolve_field

def base_attrs(cl):
    #~ if cl is Report or len(cl.__bases__) == 0:
        #~ return
    #~ myattrs = set(cl.__dict__.keys())
    for b in cl.__bases__:
        for k in base_attrs(b):
            yield k
        for k in b.__dict__.keys():
            yield k

    


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

    
def get_app(app_label):
    """
    This is called in models modules instead of "from x.y import models as y"
    It is probably quicker than loading.get_app().
    It doesn't work during loading.appcache._populate().
    Didn't test how they compare in multi-threading cases.
    """
    for app_name in settings.INSTALLED_APPS:
        if app_name.endswith('.'+app_label):
            return import_module('.models', app_name)
    #~ if not emptyOK:
    raise ImportError("No application labeled %r." % app_label)
      
def unused_get_report(app_label,rptname):
    # replaced by actors.get_actor()
    """this method is called for each request, and it does not need to work when the AppCache is populating
    """
    lino.log.debug('reports.get_report(%r,%r)',app_label,rptname)
    #app = models.get_app(app_label)
    app = get_app(app_label)
    #~ if app is None:
        #~ return None
    rptclass = getattr(app,rptname,None)
    if rptclass is None:
        raise ImportError("No report %s in application %r" % (rptname,app))
        #~ lino.log.warning("No report %s in application %r",rptname,app)
        #~ return None
    return rptclass()

    
def setup():
    """
    - Each model can receive a number of "slaves". 
      slaves are reports that display detail data for a known instance of that model (their master).
      They are stored in a dictionary called '_lino_slaves'.
      
    - For each model we want to find out the "model report" ot "default report".
      The "choices report" for a foreignkey field is also currently simply the pointed model's
      model_report.
      `_lino_model_report`

    """
    lino.log.debug("Register Report actors...")
    for cls in actors.actors_dict.values():
        if issubclass(cls,Report) and cls is not Report:
            if cls.typo_check:
                myattrs = set(cls.__dict__.keys())
                for attr in base_attrs(cls):
                    myattrs.discard(attr)
                if len(myattrs):
                    lino.log.warning("%s defines new attribute(s) %s", cls, ",".join(myattrs))
            register_report(cls)
    
    lino.log.debug("Instantiate model reports...")
    i = 0
    for model in models.get_models():
        i += 1
        rpt = getattr(model,'_lino_model_report',None)
        if rpt is None:
            cls = report_factory(model)
            register_report(cls)
            model._lino_model_report = cls()
        lino.log.debug("%d %s %s",i,model._meta.db_table,model._lino_model_report.actor_id)
        #model._lino_model_report = model._lino_model_report_class()
        
    #~ lino.log.debug("Instantiate choice reports...")
    #~ for model in models.get_models():
        #~ for fld in model._meta.fields:
            #~ if isinstance(fld,models.ForeignKey):
                #~ if not hasattr(fld,'_lino_choice_report'):
                    #~ cls = choice_report_factory(model,fld)
                    #~ register_report(cls)
                    #~ fld._lino_choice_report = cls()
        
    lino.log.debug("Analyze %d slave reports...",len(slave_reports))
    for rpt in slave_reports:
        slaves = getattr(rpt.master,"_lino_slaves",None)
        if slaves is None:
            slaves = {}
            setattr(rpt.master,'_lino_slaves',slaves)
        slaves[rpt.actor_id] = rpt
        lino.log.debug("%s: slave for %s",rpt.actor_id, rpt.master.__name__)
    lino.log.debug("Assigned %d slave reports to their master.",len(slave_reports))
        
    lino.log.debug("Setup model reports...")
    for model in models.get_models():
        model._lino_model_report.setup()
        
    lino.log.debug("reports.setup() done (%d models)",i)

def get_slave(model,name):
    try:
        rpt = actors.get_actor(name)
    except KeyError:
        return None
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


class Report(actors.Actor):
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
    label = None
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

    typo_check = True
    url = None
    actions = []
    
    def __init__(self):
        actors.Actor.__init__(self)
        self._handles = {}
        self._setup_done = False
        self._setup_doing = False
        self.actions = self.actions + [ actions.DeleteSelected() ]
        
        #~ if self.field is None:
        if self.model is None:
            if self.queryset is None:
                raise Exception(self.__class__)
            self.model = self.queryset.model
        else:
            self.model = resolve_model(self.model,self.app_label)
        assert issubclass(self.model,models.Model), "%s.model is a %r" % (self.actor_id,self.model)
        
        self.master = resolve_model(self.master,self.app_label)
        
        if self.fk_name:
            try:
                fk, remote, direct, m2m = self.model._meta.get_field_by_name(self.fk_name)
                assert direct
                assert not m2m
                master = fk.rel.to
            except models.FieldDoesNotExist,e:
                master = None
                for vf in self.model._meta.virtual_fields:
                    if vf.name == self.fk_name:
                        fk = vf
                        master = ContentType
            if master is None:
                raise Exeption("No master for fk_name %r in %s" % (self.fk_name,self.model.__name__))
            self.master = master
            self.fk = fk
        elif self.master:
            lino.log.warning("DEPRECATED: replace %s.master by fk_name" % self.actor_id)
            #assert isinstance(self.master,object), "%s.master is a %r" % (self.name,self.master)
            assert issubclass(self.master,models.Model), "%s.master is a %r" % (self.actor_id,self.master)
            self.fk = _get_foreign_key(self.master,self.model) #,self.fk_name)
        
        
        #self.setup()
        
        #register_report(self)
        lino.log.debug("Report.__init__() done: %s", self.actor_id)
        
        
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
        
    def get_handle(self,ui):
        return ui.get_report_handle(self)
        
    def get_fields(self):
        return [ f.name for f in self.model._meta.fields + self.model._meta.many_to_many]
        
    def try_get_field(self,name):
        try:
            return self.model._meta.get_field(name)
        except models.FieldDoesNotExist,e:
            return None
            
    def try_get_meth(self,name):
        def get_unbound_meth(cl,name):
            meth = getattr(cl,name,None)
            if meth is not None:
                return meth
            for b in cl.__bases__:
                meth = getattr(b,name,None)
                if meth is not None:
                    return meth
        return get_unbound_meth(self.model,name)
            
    def get_slave(self,name):
        return get_slave(self.model,name)
        #l = self.slaves() # to populate
        #return self._slaves.get(name,None)
        
    def add_actions(self,*args):
        "May be used in Model.setup_report() to specify actions for each report which uses this model."
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

        
    def get_field_choices(self,field):
        return get_model_report(field.rel.to)
        #return field._lino_choice_report
        #~ rpt = getattr(field,'_lino_choice_report',None)
        #~ if rpt is None:
            #~ return get_model_report(field.rel.to)
        #~ return rpt
        
            
    def get_title(self,renderer):
        #~ if self.title is None:
            #~ return self.label
        return self.title or self.label
        
        
    def get_queryset(self,master_instance=None,quick_search=None,order_by=None,**kw):
        lino.log.debug('%sReport.get_queryset(%r)',self.actor_id,master_instance)
        if self.queryset is not None:
            qs = self.queryset
        else:
            qs = self.model.objects.all()
        kw = self.add_master_kw(master_instance,**kw)
        if len(kw):
            qs = qs.filter(**kw)

        if self.filter:
            qs = qs.filter(**self.filter)
        if self.exclude:
            qs = qs.exclude(**self.exclude)
        if quick_search is not None:
            l = []
            q = models.Q()
            for field in self.model._meta.fields:
                if isinstance(field,models.CharField):
                    q = q | models.Q(**{
                      field.name+"__contains": quick_search})
            qs = qs.filter(q)
        order_by = order_by or self.order_by
        if order_by:
            qs = qs.order_by(*order_by.split())
        return qs
        
    def add_master_kw(self,master_instance,**kw):
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
                kw[self.fk.name] = master_instance
                #kw["%s__exact" % self.fk.name] = None
            elif not isinstance(master_instance,self.master):
                raise Exception("%r is not a %s" % (master_instance,self.master.__name__))
            else:
                kw[self.fk.name] = master_instance
        return kw
        
    def create_instance(self,**kw):
        instance = self.model(**kw)
        self.after_create(instance)
        return instance
        
    def after_create(self,instance):
        pass
        
    def getLabel(self):
        return self.label
        
    def __str__(self):
        return rc_name(self.__class__)
        
    def ajax_update(self,request):
        print request.POST
        return HttpResponse("1", mimetype='text/x-json')


    def as_text(self, *args,**kw):
        from . import renderers_text 
        r = renderers_text.TextReportRequest(self,*args,**kw)
        return r.render()
        
    @classmethod
    def register_page_layout(cls,*layouts):
        cls.page_layouts = tuple(cls.page_layouts) + layouts

        
def report_factory(model):
    lino.log.debug('report_factory(%s) -> app_label=%r',model.__name__,model._meta.app_label)
    return type(model.__name__+"Report",(Report,),dict(model=model,app_label=model._meta.app_label))

#~ def choice_report_factory(model,field):
    #~ clsname = model.__name__+"_"+field.name+'_'+"Choices"
    #~ fldname = model._meta.app_label+'.'+model.__class__.__name__+'.'+field.name
    #~ return type(clsname,(Report,),dict(field=fldname,app_label=model._meta.app_label,columnNames='__unicode__'))


class ReportHandle(layouts.DataLink):
    def __init__(self,ui,report):
        #lino.log.debug('ReportHandle.__init__(%s)',rd)
        layouts.DataLink.__init__(self,ui,report.actor_id)
        assert isinstance(report,Report)
        assert isinstance(ui,UI)
        #self._rd = rd
        self.report = report
        for n in ('get_fields','get_slave','try_get_field','try_get_meth','get_field_choices',
                  'get_title', 'create_instance'):
            setattr(self,n,getattr(report,n))
            
    def setup(self):
        def lh(layout_class,*args,**kw):
            layout = layout_class()
            return layouts.LayoutHandle(self,layout,*args,**kw)
        
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
            
        self.store = self.ui.Store(self)

    def get_absolute_url(self,*args,**kw):
        return self.ui.get_report_url(self,*args,**kw)
    
class ReportRequest:
    """
    An instance of this will be created for every request.
    """
    limit = None
    offset = None
    master_instance = None
    instance = None
    
    def __init__(self,rh,
            master_instance=None,
            offset=None,limit=None,
            extra=1,
            #layout=None,
            **kw):
        lino.log.debug('%sRequest.__init__(%r)',rh.report.actor_id,master_instance)
        assert isinstance(rh,ReportHandle)
        self.report = rh.report
        self.rh = rh
        self.name = rh.report.actor_id+"Request"
        self.extra = extra
        self.master_instance = master_instance
        self.queryset = rh.report.get_queryset(self.master_instance,**kw)
        # Report.get_queryset() may return a list
        if isinstance(self.queryset,models.query.QuerySet):
            self.total_count = self.queryset.count()
        else:
            self.total_count = len(self.queryset)
        
        if offset is not None:
            self.queryset = self.queryset[int(offset):]
            self.offset = offset
            
        if limit is None:
            limit = rh.report.page_length
        if limit is not None:
            self.queryset = self.queryset[:int(limit)]
            self.limit = limit
            
        self.page_length = rh.report.page_length

    def get_title(self):
        return self.report.get_title(self)

    def create_instance(self,**kw):
        kw = self.report.add_master_kw(self.master_instance,**kw)
        return self.report.create_instance(**kw)
        



class UI:
    
    def get_urls():
        pass
        
    def setup_site(self,lino_site):
        pass
    
    def field2elem(self,lui,field,**kw):
        pass
        
    def _get_report_handle(self,app_label,rptname):
        rpt = actors.get_actor(app_label,rptname)
        #rpt = get_report(app_label,rptname)
        return self.get_report_handle(rpt)
        
    def get_report_handle(self,rpt):
        #lino.log.debug('get_report_handle(%s)',rpt)
        rpt.setup()
        h = rpt._handles.get(self,None)
        if h is None:
            h = ReportHandle(self,rpt)
            rpt._handles[self] = h
            h.setup()
        return h
        
    def get_dialog_handle(self,layout):
        assert isinstance(layout,layouts.DialogLayout)
        h = layout._handles.get(self,None)
        if h is None:
            lnk = layouts.DialogLink(self,layout)
            h = layouts.LayoutHandle(lnk,layout,1)
            layout._handles[self] = h
            #h.setup()
        return h
        


