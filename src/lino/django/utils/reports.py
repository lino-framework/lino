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
from django.utils import simplejson

from django.http import HttpResponse
#from django.core import serializers
#from django.shortcuts import render_to_response
#from django.utils import simplejson
from django.utils.safestring import mark_safe

from . import layouts, extjs, perms, urls

from lino.django.utils.sites import lino_site

# maps Django field types to a tuple of default paramenters
# each tuple contains: minWidth, maxWidth, is_filter
#~ WIDTHS = {
    #~ models.IntegerField : (2,10,False),
    #~ models.CharField : (10,50,True),
    #~ models.TextField :  (10,50,True),
    #~ models.BooleanField : (10,10,True),
    #~ models.ForeignKey : (5,40,False),
    #~ models.AutoField : (2,10,False),
#~ }


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
    
UNDEFINED = "nix"
    
class ActionEvent(Exception):
    pass
    
class MustConfirm(ActionEvent):
    pass
    
class Action:
    label = None
    name = None
    def __init__(self,report):
        if self.label is None:
            self.label = self.__class__.__name__
        if self.name is None:
            self.name = self.label
        self.report = report
        
    def do_run(self,request):
        context = ActionContext(self,request)
        try:
            msg = self.run(context)
            if msg is None:
                msg = "Completed"
            d = dict(success=True,msg=msg)
        except MustConfirm,e:
            d = dict(success=False,confirm=str(e))
        except Exception,e:
            d = dict(success=False,msg=str(e))
        d.update(must_reload=context.must_reload)
        return d
        
    def run(self,context):
        raise NotImplementedError
    def before_run(self,renderer):
        pass
        
class ActionContext:
    def __init__(self,action,request):
        #self.request = request
        selected = request.POST.get('selected',None)
        if selected:
            self.selected_rows = [
              action.report.model.objects.get(pk=pk) for pk in selected.split(',') if pk]
        else:
            self.selected_rows = []
        self.confirmed = request.POST.get('confirmed',None)
        if self.confirmed is not None:
            self.confirmed = int(self.confirmed)
        self.confirms = 0
        self.must_reload = False
        print 'Actioncontext.__init__()', self.confirmed, self.selected_rows
        
    def refresh(self):
        self.must_reload = True
        
    def confirm(self,msg):
        print "ActionContext.confirm()", msg
        self.confirms += 1
        if self.confirmed >= self.confirms:
            return
        raise MustConfirm(msg)
        
class DeleteSelected(Action):
    label = "Delete"
    def run(self,context):
        if len(context.selected_rows) == 0:
            return "No rows selected. Nothing to do."
        context.confirm("Delete %d rows. Are you sure?" % len(context.selected_rows))
        for row in context.selected_rows:
            #print "DELETE:", row
            row.delete()
        context.refresh()

    


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
    r = ViewReportRequest(request,rpt)
    return r.render_to_html()
    #return lino_site.ext_view(request,*rpt.ext_components())
    
    #return r.render_to_response()
    
    
def view_report_as_json(request,app_label=None,rptname=None):
    rpt = get_report(app_label,rptname)
    if rpt is None:
        return json_response(success=False,
            msg="%s : no such report" % rptname)
    if not rpt.can_view.passes(request):
        return json_response(success=False,
            msg="User %s cannot view %s : " % (request.user,rptname))
    r = ViewReportRequest(request,rpt)
    #request._lino_report = r
    s = r.render_to_json()
    return HttpResponse(s, mimetype='text/html')


def view_action(request,app_label=None,rptname=None,action=None):
    rpt = get_report(app_label,rptname)
    if rpt is None:
        return json_response(success=False,
            msg="%s : no such report" % rptname)
    if not rpt.can_view.passes(request):
        return json_response(success=False,
            msg="User %s cannot view %s : " % (request.user,rptname))
    r = ViewReportRequest(request,rpt)
    d = None
    for a in rpt._actions:
        if a.name == action:
            d = a.do_run(request)
            break
    if d is None:
        d = dict(success=False,msg="Not implemented")
    s = simplejson.dumps(d,default=unicode)
    return HttpResponse(s, mimetype='text/html')


def view_report_save(request,app_label=None,rptname=None):
    rpt = get_report(app_label,rptname)
    if rpt is None:
        return json_response(success=False,
            msg="%s : no such report" % rptname)
    if not rpt.can_change.passes(request):
        return json_response(success=False,
            msg="User %s cannot update data in %s : " % (request.user,rptname))
    #~ r = render.ViewReportRequest(request,rpt)
    #~ if r.instance is None:
        #~ print request.GET
        #~ return json_response(success=False,
            #~ msg="tried to update more than one row")
    pk = request.POST.get(rpt.store.pk.name,None)
    #pk = request.POST.get('pk',None)
    if pk == UNDEFINED:
        pk = None
    try:
        if pk is None:
            #return json_response(success=False,msg="No primary key was specified")
            instance = rpt.model()
        else:
            instance = rpt.model.objects.get(pk=pk)
        #print "foo",request.POST
        #20090916 rpt.setup()
        #print "Updating", instance, "using", request.POST
        for f in rpt.store.fields:
            if not f.field.primary_key:
                #print "reports.view_report_save()",f.field.name
                f.update_from_form(instance,request.POST)
        instance.save()
        return json_response(success=True,
              msg="%s has been saved" % instance)
    except Exception,e:
        traceback.print_exc(e)
        return json_response(success=False,msg="Exception occured: "+str(e))
    
def json_response(**kw):
    s = "{%s}" % extjs.dict2js(kw)
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
        
    #~ todo = [m._lino_model_report for m in models.get_models()]
    #~ while len(todo):
        #~ print "Setting up %d model reports..." % len(todo)
        #~ again = todo
        #~ todo = []
        #~ for rpt in again:
            #~ if not rpt.setup():
                #~ todo.append(rpt)
        #~ if len(again) == len(todo):
            #~ raise Exception("Could not setup reports %s" % todo)
            
          
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
    actions = [ DeleteSelected ]
    
    def __init__(self):
      
        if self.model is None:
            self.model = self.queryset.model
        if self.label is None:
            self.label = self.__class__.__name__
        if self.name is None:
            self.name = self.__class__.__name__
        #~ if self.mode is not None:
            #~ self.name += "_" + self.mode
            
            
        self._setup_done = False
        self._setup_doing = False
        
        #self.setup()
        
        #register_report(self)
        # print "Report.__init__() done:", self.name
        
    def setup(self):
        if self._setup_done:
            return True
        if self._setup_doing:
            print "[Warning] %s.setup() called recursively" % self.name
            return False
        self._setup_doing = True
        
        if self.master:
            self.fk = _get_foreign_key(self.master,
              self.model,self.fk_name)
            #self.name = self.fk.rel.related_name
        
        #~ if self.form_class is None:
            #~ self.form_class = modelform_factory(self.model)
        choice_layout = layouts.RowLayout(self,0,self.display_field)
        self.choice_store = extjs.Store(self,[choice_layout],mode='choice',autoLoad=True)
        
        if self.row_layout_class is None:
            self.row_layout = layouts.RowLayout(self,1,self.columnNames)
        else:
            assert self.columnNames is None
            self.row_layout = self.row_layout_class(self,1)
            
        l = [ self.row_layout ]
        index = 2
        for lc in self.page_layouts:
            l.append(lc(self,index))
            index += 1
            
        self.store = extjs.Store(self,l) #,autoLoad=True
        
        self._actions = [cl(self) for cl in self.actions]
        
        
        self._setup_doing = False
        self._setup_done = True
        
        #print "Report.setup() done:", self.name
        return True
        
        
        
    def unused_ext_components(self):
        if len(self.store.layouts) == 2:
            for s in self.store.layouts:
                yield s._main
        else:
            yield self.store.layouts[0]._main
            comps = [l._main for l in self.store.layouts[1:]]
            yield extjs.TabPanel(None,"EastPanel",*comps)
            
        #~ yield self.layouts[0]._main
        #~ if len(self.layouts) == 2:
            #~ yield self.layouts[1]._main
        #~ else:
            #~ comps = [l._main for l in self.layouts[1:]]
            #~ yield layouts.TabPanel(None,"EastPanel",*comps)

        
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
            assert master_instance is None, "This Report doesn't accept a master"
        else:
            if master_instance is None:
                qs = qs.filter(**{"%s__exact" % self.fk.name:None})
            else:
                if not isinstance(master_instance,self.master):
                    raise Exception("%r is not a %s" % (master_instance,self.master.__name__))
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
    
    def ajax_update(self,request):
        print request.POST
        return HttpResponse("1", mimetype='text/x-json')


    def as_text(self, *args,**kw):
        from . import renderers_text 
        r = renderers_text.TextReportRequest(self,*args,**kw)
        return r.render()
        
    #~ def as_html(self, **kw):
        #~ return render.HtmlReportRequest(self,**kw).render_to_string()
        
    #~ def get_row_actions(self,renderer):
        #~ l = []
        #~ #l.append( ('dummy',self.dummy) )
        #~ if self.can_change.passes(renderer.request):
            #~ l.append( ('delete',self.delete_selected) )
        #~ return l
            
    #~ def delete_selected(self,renderer):
        #~ for row in renderer.selected_rows():
            #~ print "DELETE:", row.instance
            #~ row.instance.delete()
        #~ renderer.must_refresh()

        
def report_factory(model):
    return type(model.__name__+"Report",(Report,),dict(model=model))
    
        
        
        
class ReportRequest:
    limit = None
    offset = None
    master_instance = None
    instance = None
    
    def __init__(self,report,
            master_instance=None,
            offset=None,limit=None,
            mode=None,
            **kw):
        #from lino.django.tom.reports import Report
        #assert isinstance(report,Report)
        self.report = report
        report.setup()
        self.name = report.name+"Renderer"
        self.mode = mode
        if mode == 'choice':
            self.store = report.choice_store
        else:
            self.store = report.store
        #if master_instance is not None:
        self.master_instance = master_instance
        #print self.__class__.__name__, "__init__()"
        #self.params = params
        self.queryset = report.get_queryset(master_instance,**kw)
        
        if isinstance(self.queryset,models.query.QuerySet):
            self.total_count = self.queryset.count()
        else:
            # a Report may override get_queryset() and return a list
            self.total_count = len(self.queryset)
        
        if offset is not None:
            self.queryset = self.queryset[int(offset):]
            self.offset = offset
            
        if limit is None:
            limit = report.page_length
        if limit is not None:
            self.queryset = self.queryset[:int(limit)]
            self.limit = limit
            
        self.page_length = report.page_length
            
        #self.actions = self.report.get_row_actions(self)

    def get_title(self):
        return self.report.get_title(self)

    def obj2json(self,obj):
        d = {}
        for fld in self.store.fields:
            fld.write_to_form(obj,d)
            #d[e.name] = e.value2js(obj)
        return d
            
    def render_to_json(self):
        rows = [ self.obj2json(row) for row in self.queryset ]
        total_count = self.total_count
        if True: # add one empty row
            d = {}
            for fld in self.store.fields:
                d[fld.field.name] = None
            d[self.report.store.pk.name] = UNDEFINED
            rows.append(d)
            total_count += 1
        d = dict(count=total_count,rows=rows)
        s = simplejson.dumps(d,default=unicode)
        return s
        #print s
        #return HttpResponse(s, mimetype='text/html')
        

class ViewReportRequest(ReportRequest):
  
    editing = 0
    selector = None
    sort_column = None
    sort_direction = None
    
    def __init__(self,request,report,*args,**kw):
      
        self.params = report.param_form(request.GET)
        if self.params.is_valid():
            kw.update(self.params.cleaned_data)
        if report.master is not None:
            pk = request.GET.get('master',None)
            if pk == UNDEFINED:
                pk = None
            if pk is None:
                kw.update(master_instance=None)
            else:
                try:
                    kw.update(master_instance=report.master.objects.get(pk=pk))
                except report.master.DoesNotExist,e:
                    print "[Warning] There's no %s with %s=%r" % (
                      report.master.__name__,report.master._meta.pk.name,pk)
        sort = request.GET.get('sort',None)
        if sort:
            self.sort_column = sort
            sort_dir = request.GET.get('dir','ASC')
            if sort_dir == 'DESC':
                sort = '-'+sort
                self.sort_direction = 'DESC'
            kw.update(order_by=sort)
        
        #self.json = request.GET.get('json',False)
        
        offset = request.GET.get('start',None)
        if offset:
            kw.update(offset=offset)
        limit = request.GET.get('limit',None)
        if limit:
            kw.update(limit=limit)
        #~ layout = request.GET.get('layout',None)
        #~ if layout:
            #~ kw.update(layout=int(layout))
        mode = request.GET.get('mode',None)
        if mode:
            kw.update(mode=mode)

        #print "ViewReportRequest.__init__() 1",report.name
        self.request = request
        ReportRequest.__init__(self,report,*args,**kw)
        #print "ViewReportRequest.__init__() 2",report.name
        #self.is_main = is_main
        request._lino_request = self
        

    def get_absolute_url(self,**kw):
        if self.master_instance is not None:
            kw.update(master_instance=self.master_instance)
        if self.limit != self.__class__.limit:
            kw.update(limit=self.limit)
        if self.offset is not None:
            kw.update(start=self.offset)
        if self.sort_column is not None:
            kw.update(sort=self.sort_column)
        if self.sort_direction is not None:
            kw.update(dir=self.sort_direction)
        #~ if self.layout.index != 0:
            #~ kw.update(layout=self.layout.index)
        if self.mode is not None:
            kw.update(mode=self.mode)
        return self.report.get_absolute_url(**kw)

    def render_to_html(self):
        if len(self.store.layouts) == 2:
            comps = [l._main for l in self.store.layouts]
        else:
            tabs = [l._main for l in self.store.layouts[1:]]
            comps = [self.store.layouts[0]._main,extjs.TabPanel(None,"EastPanel",*tabs)]
        return lino_site.ext_view(self.request,*comps)
        #return self.report.viewport.render_to_html(self.request)



        
class PdfManyReportRenderer(ViewReportRequest):

    def render(self,as_pdf=True):
        template = get_template("lino/grid_print.html")
        context=dict(
          report=self,
          title=self.get_title(),
        )
        html  = template.render(Context(context))
        if not (pisa and as_pdf):
            return HttpResponse(html)
        result = cStringIO.StringIO()
        pdf = pisa.pisaDocument(cStringIO.StringIO(
          html.encode("ISO-8859-1")), result)
        if pdf.err:
            raise Exception(cgi.escape(html))
        return HttpResponse(result.getvalue(),mimetype='application/pdf')
        
    def rows(self):
        rownum = 1
        for obj in self.queryset:
            yield Row(self,obj,rownum,None)
            rownum += 1

  
class PdfOneReportRenderer(ViewReportRequest):
    #detail_renderer = PdfManyReportRenderer

    def render(self,as_pdf=True):
        if as_pdf:
            return self.row.instance.view_pdf(self.request)
            #~ if False:
                #~ s = render_to_pdf(self.row.instance)
                #~ return HttpResponse(s,mimetype='application/pdf')
            #~ elif pisa:
                #~ s = as_printable(self.row.instance,as_pdf=True)
                #~ return HttpResponse(s,mimetype='application/pdf')
        else:
            return self.row.instance.view_printable(self.request)
            #~ result = as_printable(self.row.instance,as_pdf=False)
            #~ return HttpResponse(result)



