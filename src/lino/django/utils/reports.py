## Copyright 2003-2009 Luc Saffre

## This file is part of the Lino project.

## Lino is free software; you can redistribute it and/or modify it
## under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.

## Lino is distributed in the hope that it will be useful, but WITHOUT
## ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
## or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public
## License for more details.

## You should have received a copy of the GNU General Public License
## along with Lino; if not, write to the Free Software Foundation,
## Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

import traceback

from django.db import models
from django import forms
from django.conf.urls.defaults import patterns, url, include
from django.forms.models import modelform_factory
from django.forms.models import _get_foreign_key
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse
#from django.core import serializers
#from django.shortcuts import render_to_response
#from django.utils import simplejson
from django.utils.safestring import mark_safe

from . import layouts, render, perms, urls
from lino.django.utils.editing import is_editing
from lino.django.utils.sites import lino_site
from lino.django.utils.requests import get_redirect, redirect_to

# maps Django field types to a tuple of default paramenters
# each tuple contains: minWidth, maxWidth, is_filter
WIDTHS = {
    models.IntegerField : (2,10,False),
    models.CharField : (10,50,True),
    models.TextField :  (10,50,True),
    models.BooleanField : (10,10,True),
    models.ForeignKey : (5,40,False),
    models.AutoField : (2,10,False),
}


def base_attrs(cl):
    #~ if cl is Report or len(cl.__bases__) == 0:
        #~ return
    #~ myattrs = set(cl.__dict__.keys())
    for b in cl.__bases__:
        for k in base_attrs(b):
            yield k
        for k in b.__dict__.keys():
            yield k
            
            
#~ class SetupNotDone(Exception):
    #~ pass 


class ReportParameterForm(forms.Form):
    #~ pgn = forms.IntegerField(required=False,label="Page number") 
    #~ pgl = forms.IntegerField(required=False,label="Rows per page")
    flt = forms.CharField(required=False,label="Text filter")
    #~ fmt = forms.ChoiceField(required=False,label="Format",choices=(
      #~ ( 'form', "editable form" ),
      #~ ( 'show', "read-only display" ),
      #~ ( 'text', "plain text" ),
    #~ ))
    

#        
#  Report
#        

#~ _report_classes = {}

#~ def get_report(name):
    #~ return _report_classes[name]
    
#~ def get_reports():
    #~ return _report_classes
    
#model_reports = {}
#_slave_reports = {}
#_reports = {}

# name : ( class , instance )

"""
Each Report subclass definition found
"""

def rc_name(rptclass):
    return rptclass.app_label + '.' + rptclass.__name__

def register_report_class(rptclass):
    #_reports.append(cls)
    rptclass.app_label = rptclass.__module__.split('.')[-2]
    #print "register_report_class()", rptclass.app_label + '.' + rptclass.__name__
    if rptclass.model is None:
        print "register", rc_name(rptclass), ": model is None" 
        return
    if rptclass.master is None:
        #print "%s : master is None" % rptclass.__name__
        if rptclass.use_as_default_report:
            print "register", rc_name(rptclass), ": model_report for", rptclass.model.__name__
            rptclass.model._lino_model_report_class = rptclass
        else:
            print "register", rc_name(rptclass), ": not used as model_report"
        return
    slaves = getattr(rptclass.master,"_lino_slaves",None)
    if slaves is None:
        slaves = {}
        setattr(rptclass.master,'_lino_slaves',slaves)
    slaves[rptclass.__name__] = rptclass()
    print "register", rc_name(rptclass), ": slave for %s" % rptclass.master.__name__
    

#~ def register_report(rpt):
    #~ if _reports.has_key(rpt.name):
        #~ print "[Warning] %s used for models %s and %s" % (rpt.name,rpt.model,_reports[rpt.name].model)
        #~ return
    #~ _reports[rpt.name] = rpt
    
    #~ if rpt.model is None:
        #~ return
    #~ if rpt.master is not None:
        #~ return
    #~ if rpt.exclude is not None:
        #~ return
    #~ if rpt.filter is not None:
        #~ return
    #~ if hasattr(rpt.model,'_lino_model_report'):
        #~ print "[Warning] Ignoring %s" % rpt #.__name__
        #~ return
    #~ rpt.model._lino_model_report = self
    #~ db_table = rpt.model._meta.db_table
    #~ if model_reports.has_key(db_table):
        #~ print "[Warning] Ignoring %s" % rpt #.__name__
        #~ return
    #~ model_reports[db_table] = rpt
    
#~ def get_report(rptname):
    #~ rpt = _reports.get(rptname,None)
    #~ #rpt.setup()
    #~ return rpt
    
def get_report(app_label,rptname):
    app = models.get_app(app_label)
    rptclass = getattr(app,rptname,None)
    if rptclass is None:
        print "No report %s in application %r" % (rptname,app)
        return None
    return rptclass()
    


def view_report_as_ext(request,app_label=None,rptname=None):
    rpt = get_report(app_label,rptname)
    if rpt is None:
        return urls.sorry(request,"%s : no such report" % rptname)
    if not rpt.can_view.passes(request):
        return urls.sorry(request)
    r = render.ViewReportRenderer(request,rpt)
    request._lino_renderer = r
    return lino_site.ext_view(request,*rpt.ext_components())
    
    #return r.render_to_response()
    
    
def view_report_as_json(request,app_label=None,rptname=None):
    rpt = get_report(app_label,rptname)
    if rpt is None:
        return json_response(success=False,
            msg="%s : no such report" % rptname)
    if not rpt.can_view.passes(request):
        return json_response(success=False,
            msg="User %s cannot view %s : " % (request.user,rptname))
    r = render.ViewReportRenderer(request,rpt)
    request._lino_renderer = r
    #request._lino_report = r
    s = r.render_to_json()
    return HttpResponse(s, mimetype='text/html')

def view_report_save(request,app_label=None,rptname=None):
    rpt = get_report(app_label,rptname)
    if rpt is None:
        return json_response(success=False,
            msg="%s : no such report" % rptname)
    rpt.setup()
    d = dict()
    if not rpt.can_change.passes(request):
        return json_response(success=False,
            msg="User %s cannot update data in %s : " % (request.user,rptname))
    #~ r = render.ViewReportRenderer(request,rpt)
    #~ if r.instance is None:
        #~ print request.GET
        #~ return json_response(success=False,
            #~ msg="tried to update more than one row")
    pk = request.POST.get('pk',None)
    if pk is None:
        return json_response(success=False,msg="No primary key was specified")
    #print "foo",request.POST
    try:
        layout = rpt.layouts[int(request.POST.get('layout'))]
        instance = rpt.model.objects.get(pk=pk)
        for e in layout.ext_store_fields:
            e.update_from_form(instance,request.POST)
        #~ for k,v in request.POST.items():
            #~ setattr(instance,k,v)
        instance.save()
        return json_response(success=True,
              msg="%s has been saved" % instance)
    except Exception,e:
        traceback.print_exc(e)
        return json_response(success=False,msg="Exception occured: "+str(e))
    
def json_response(**kw):
    s = "{%s}" % layouts.dict2js(kw)
    print "json_response()", s
    return HttpResponse(s, mimetype='text/html')
    
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
    print "reports.setup() : ------------------------------"
    i = 0
    for model in models.get_models():
        i += 1
        rc = getattr(model,'_lino_model_report_class',None)
        if rc is None:
            model._lino_model_report_class = report_factory(model)
        print i,model._meta.db_table,rc_name(model._lino_model_report_class)
        model._lino_model_report = model._lino_model_report_class()
        model._lino_model_report.setup()
    print "reports.setup() : done ------------------------- (%d models)" % i
        
    #~ for rpt in _reports.values():
        #~ rpt.setup()
        


def get_slave(model,name):
    for b in (model,) + model.__bases__:
        d = getattr(b,"_lino_slaves",None)
        if d:
            rpt = d.get(name,None)
            if rpt is not None:
                rpt.setup()
                return rpt
                
    #~ for b in model.__bases__:
        #~ d = getattr(b,"_lino_slaves",{})
        #~ if d.has_key(name): return d[name]
    #~ return None
    
#~ def get_combo_report(model):
    #~ rpt = getattr(model,'_lino_choices',None)
    #~ if rpt: return rpt
    #~ rc = model._lino_model_report_class
    #~ rpt = rc(columnNames=rc.display_field,mode='choices',page_length=None)
    #~ model._lino_choices = rpt
    #~ return rpt

def get_model_report(model):
    rpt = getattr(model,'_lino_model_report',None)
    if rpt: return rpt
    rptclass = getattr(model,'_lino_model_report_class',None)
    if rptclass is None:
        rptclass = report_factory(model)
        model._lino_model_report_class = rptclass
    model._lino_model_report = rptclass()
    return model._lino_model_report

class ReportMetaClass(type):
    def __new__(meta, classname, bases, classDict):
        cls = type.__new__(meta, classname, bases, classDict)
        if classname != 'Report':
            if cls.typo_check:
                myattrs = set(cls.__dict__.keys())
                for attr in base_attrs(cls):
                    myattrs.discard(attr)
                if len(myattrs):
                    print "[Warning]: %s defines new attribute(s) %s" % (cls,",".join(myattrs))
            register_report_class(cls)
        return cls
        
    def __init__(cls, name, bases, dict):
        type.__init__(cls,name, bases, dict)
        cls.instance = None 

    def __call__(cls,*args,**kw):
        if cls.instance is None:
            cls.instance = type.__call__(cls,*args, **kw)
        return cls.instance




class Report:
    __metaclass__ = ReportMetaClass
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
    name = None
    form_class = None
    master = None
    fk_name = None
    help_url = None
    #master_instance = None
    page_length = 10
    display_field = '__unicode__'
    boolean_texts = ('Ja','Nein',' ')
    date_format = 'd.m.y'
    
    page_layouts = (layouts.PageLayout ,)
    _page_layouts = None
    row_layout_class = None
    
    can_view = perms.always
    can_add = perms.is_authenticated
    can_change = perms.is_authenticated
    can_delete = perms.is_authenticated

    typo_check = True
    url = None
    #_slaves = None
    # mode = None # suffix to create unique names 'choices'
    # json = False
    
    # __shared_state = {} 
    
    def __init__(self):
      
        # self.__dict__ = self.__shared_state
        
        #~ for k,v in kw.items():
            #~ if hasattr(self,k):
                #~ setattr(self,k,v)
            #~ else:
                #~ print "[Warning] Ignoring attribute %s" % k
            
        #self._inlines = self.inlines()
        
        if self.model is None:
            self.model = self.queryset.model
        if self.label is None:
            self.label = self.__class__.__name__
        if self.name is None:
            self.name = self.__class__.__name__
        #~ if self.mode is not None:
            #~ self.name += "_" + self.mode
            
        #self.choices_stores = {}
            
        self._setup_done = False
        self._setup_doing = False
        
        #self.setup()
        
        #register_report(self)
        # print "Report.__init__() done:", self.name
        
    def setup(self):
        if self._setup_done:
            return
        if self._setup_doing:
            print "[Warning] %s.setup() called recursively" % self.name
            return 
        self._setup_doing = True
        #~ if self.form_class is None:
            #~ self.form_class = modelform_factory(self.model)
        choice_layout = layouts.RowLayout(self,0,self.display_field)
        self.choice_store = layouts.Store(self,[choice_layout],mode='choice') 
        
        if self.row_layout_class is None:
            self.row_layout = layouts.RowLayout(self,1,self.columnNames)
        else:
            assert self.columnNames is None
            self.row_layout = self.row_layout_class(self,1)
            
            
        #self.columns = [e for e in self.row_layout.walk() if isinstance(e,FieldElement)]
        
        if self.master:
            self.fk = _get_foreign_key(self.master,
              self.model,self.fk_name)
            #self.name = self.fk.rel.related_name
        l = [ self.row_layout ]
        index = 2
        for lc in self.page_layouts:
            l.append(lc(self,index))
            index += 1
            
        #~ if len(self.page_layouts) == 1:
            #~ self.page_layout = self.page_layouts[0](self)
        #~ else:
            #~ self.page_layout = layouts.TabbedPageLayout(self,
              #~ self.page_layouts)
        #~ self._page_layouts = [
              #~ layout(self) for layout in self.page_layouts]
        
        self.store = layouts.Store(self,l)
        
        self._setup_doing = False
        self._setup_done = True
        
        print "Report.setup() done:", self.name
        
            
            
        
       
          
        #~ if hasattr(self.model,'slaves'):
            #~ #self.slaves = [ rpt(name=k) for k,v in self.model.slaves().items() ]
        #~ else:
            #~ self.slaves = []
                
    #~ def get_model(self):
        #~ assert self.queryset is not None,"""
        #~ if you set neither model nor queryset in your Report, 
        #~ then you must override get_model(). Example: journals.DocumentsByJournal
        #~ """
        #~ return self.queryset.model
        
    #~ def get_label(self):
        #~ return self.__class__.__name__
        
    def get_slave(self,name):
        return get_slave(self.model,name)
        #l = self.slaves() # to populate
        #return self._slaves.get(name,None)
        
    def get_field_choices(self,field):
        return get_model_report(field.rel.to)
        #return get_combo_report(field.rel.to)
        # TODO : if hasattr(self,"%s_choices" % field.name)...
        #~ rpt = self.choices_stores.get(field,None)
        #~ if rpt is None:
            #~ rpt = get_combo_report(field.rel.to)
            #~ self.choices_stores[field] = rpt
        #~ return rpt
        
    #~ def slaves(self):
        #~ hier: und zwar die slaves in diesem report (nicht alle slaves des modells)
      
        #~ if self._slaves is None:
            #~ self._slaves = {}
            #~ for cl in slave_reports(self.model):
                #~ rpt = cl()
                #~ self._slaves[rpt.name] = rpt
            #print "reports.Report.slaves()", self.__class__.__name__, ":", self._slaves
        #~ return self._slaves.values()
        
        
    #~ def column_headers(self):
        #~ self.setup()
        #~ for e in self.columns:
            #~ yield e.label
            
    def get_title(self,renderer):
        #~ if self.title is None:
            #~ return self.label
        return self.title or self.label
        
        
    def get_queryset(self,master_instance=None,flt=None,order_by=None):
        if self.queryset is not None:
            qs = self.queryset
        else:
            qs = self.model.objects.all()
        if self.master is None:
            assert master_instance is None
        else:
            #~ if master_instance is None:
                #~ master_instance = self.master_instance
            assert isinstance(master_instance,self.master), "%r is not a %s" % (master_instance,self.master)
            #print qs
            #print qs.model
            qs = qs.filter(**{self.fk.name:master_instance})
            #~ if self.fk.limit_choices_to:
                #~ qs = qs.filter(**self.fk.limit_choices_to)

        if self.filter:
            qs = qs.filter(**self.filter)
        if self.exclude:
            qs = qs.exclude(**self.exclude)
        if flt is not None:
            l = []
            q = models.Q()
            for field in self.model._meta.fields:
                if isinstance(field,models.CharField):
                    q = q | models.Q(**{
                      field.name+"__contains": flt})
            qs = qs.filter(q)
        order_by = order_by or self.order_by
        if order_by:
            qs = qs.order_by(*order_by.split())
        #~ print "Report.get_queryset()", qs
        #~ from django.db.models.query import QuerySet
        #~ if not isinstance(qs,QuerySet):
            #~ raise Exception(
              #~ "%s is not a QuerySet but a %s:" % (qs, type(qs)))
        return qs
        
    def create_instance(self,renderer):
        i = self.model()
        # todo...
        return i
        
    def getLabel(self):
        return self.label
        
    def get_absolute_url(self,*args,**kw):
        return urls.get_report_url(self,*args,**kw)
    
    def ext_components(self):
        if len(self.store.layouts) == 2:
            for s in self.store.layouts:
                yield s._main
        else:
            yield self.store.layouts[0]._main
            comps = [l._main for l in self.store.layouts[1:]]
            yield layouts.TabPanel(None,"EastPanel",*comps)
            
        #~ yield self.layouts[0]._main
        #~ if len(self.layouts) == 2:
            #~ yield self.layouts[1]._main
        #~ else:
            #~ comps = [l._main for l in self.layouts[1:]]
            #~ yield layouts.TabPanel(None,"EastPanel",*comps)

    def ajax_update(self,request):
        print request.POST
        return HttpResponse("1", mimetype='text/x-json')


    def as_text(self, *args,**kw):
        from . import renderers_text 
        return renderers_text.TextReportRenderer(self,*args,**kw).render()
        
    #~ def as_html(self, **kw):
        #~ return render.HtmlReportRenderer(self,**kw).render_to_string()
        
    def get_row_actions(self,renderer):
        l = []
        #l.append( ('dummy',self.dummy) )
        if self.can_change.passes(renderer.request):
            l.append( ('delete',self.delete_selected) )
        return l
            
    def delete_selected(self,renderer):
        for row in renderer.selected_rows():
            print "DELETE:", row.instance
            row.instance.delete()
        renderer.must_refresh()

        
def report_factory(model):
    return type(model.__name__+"Report",(Report,),dict(model=model))
    
        