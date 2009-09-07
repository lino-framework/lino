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
            
            
class SetupNotDone(Exception):
    pass 


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
_reports = {}

def register_report_class(rptclass):
    #_reports.append(cls)
    if rptclass.model is None:
        #print "%s : model is None" % rptclass.__name__
        return
    if rptclass.master is None:
        #print "%s : master is None" % rptclass.__name__
        if hasattr(rptclass.model,'_lino_model_report_class'):
            #print "[Warning] %s" % rptclass #.__name__
            return
        #print "%s : model report is %s" % (rptclass.model.__name__,rptclass)
        rptclass.model._lino_model_report_class = rptclass
        return
    slaves = getattr(rptclass.master,"_lino_slaves",None)
    if slaves is None:
        slaves = {}
        setattr(rptclass.master,'_lino_slaves',slaves)
    slaves[rptclass.__name__] = rptclass
    #print "%s : slave for %s" % (rptclass.__name__, rptclass.master.__name__)
    

def register_report(rpt):
    if _reports.has_key(rpt.name):
        print "[Warning] %s used for models %s and %s" % (rpt.name,rpt.model,_reports[rpt.name].model)
        return
    _reports[rpt.name] = rpt
    
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
    
def get_report(rptname):
    rpt = _reports.get(rptname,None)
    #rpt.setup()
    return rpt


def view_report_as_json(request,rptname=None):
    """
    """
    rpt = get_report(rptname)
    if rpt is None:
        return json_response(success=False,
            msg="%s : no such report" % rptname)
    if not rpt.can_view.passes(request):
        return json_response(success=False,
            msg="User %s cannot view %s : " % (request.user,rptname))
    r = render.ViewReportRenderer(request,rpt)
    #request._lino_report = r
    s = r.render_to_json()
    return HttpResponse(s, mimetype='text/html')

def view_report_as_ext(request,rptname=None):
    """
    """
    #~ url = get_redirect(request)
    #~ if url is not None:
        #~ return HttpResponseRedirect(url)
    rpt = get_report(rptname)
    if rpt is None:
        return urls.sorry(request)
    if not rpt.can_view.passes(request):
        return urls.sorry(request)
    r = render.ViewReportRenderer(request,rpt)
    request._lino_report = r
    return lino_site.ext_view(request,*rpt.ext_components())
    
    #return r.render_to_response()
    
    
def view_report_save(request,rptname=None):
    """
    """
    rpt = get_report(rptname)
    rpt.setup()
    d = dict()
    if rpt is None:
        return json_response(success=False,
            msg="%s : no such report" % rptname)
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
    for model in models.get_models():
        rc = getattr(model,'_lino_model_report_class',None)
        if rc is None:
            model._lino_model_report_class = report_factory(model)
        
    for rpt in _reports.values():
        rpt.setup()
        

def old_setup():
    """
    - Each model can receive a number of "slaves". 
      slaves are reports that display detail data for a known instance of that model (their master).
      They are stored in a dictionary called '_lino_slaves'.
      
    - For each model we want to find out the "model report", 
      This will be used when displaying a single object. 
      And the "choices report" for a foreignkey field is also currently simply the pointed model's
      model_report.
      `_lino_model_report`

    
    """
    todo = [ m for m in models.get_models()]
    while True:
        len_todo = len(todo)
        print "[Note] reports.setup() : %d reports" % len_todo
        todo = _try_setup(todo)
        if len(todo) == 0:
            return
        if len(todo) == len_todo:
            raise RuntimeError("Failed to setup %d models: %s" % (len_todo,todo))
    #~ for model in models.get_models():
        #~ model._lino_combo = Report(model=model,columnNames='__str__')


def _old_try_setup(todo):
    try_again = []
    for model in todo:
        try:
            rc = getattr(model,'_lino_model_report_class',None)
            if rc is None:
                #~ if hasattr(rc,'__unicode__'):
                model._lino_combo = Report(model=model,columnNames='__str__')
                model._lino_model_report = Report(model=model)
                print "[Note] Using default report for model %s" % model._meta.db_table
                #~ else:
                    #~ print "[Note] No report for model %s" % model._meta.db_table
            else:
                model._lino_combo = rc(columnNames=rc.display_field)
                model._lino_model_report = rc()
                print "[Note] %s : reports.setup() ok" % model._meta.db_table
        except SetupNotDone,e:
            print "[Note]", model, ":", e
            try_again.append(model)
    return try_again
            
        
        #~ model._lino_slaves = {}
        #~ for rc in reports.report_classes:
            #~ ...
            #~ model._lino_slaves[rpt.name] = rpt
    
#~ def slave_reports(model):
    #~ d = getattr(model,"_lino_slaves",{})
    #~ for b in model.__bases__:
        #~ l += getattr(b,"_lino_slaves",[])
    #~ return l
    #return _slave_reports.get(model,[])

def get_slave(model,name):
    d = getattr(model,"_lino_slaves",{})
    #print d
    if d.has_key(name): return d[name]
    for b in model.__bases__:
        d = getattr(b,"_lino_slaves",{})
        if d.has_key(name): return d[name]
    return None
    
def get_combo_report(model):
    rpt = getattr(model,'_lino_choices',None)
    if rpt: return rpt
    rc = model._lino_model_report_class
    rpt = rc(columnNames=rc.display_field,mode='choices',page_length=None)
    model._lino_choices = rpt
    return rpt

def get_model_report(model):
    rpt = getattr(model,'_lino_model_report',None)
    if rpt: return rpt
    model._lino_model_report = model._lino_model_report_class()
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




class Report:
    __metaclass__ = ReportMetaClass
    queryset = None 
    model = None
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
    master_instance = None
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
    mode = None # suffix to create unique names 'choices'
    json = False
    
    def __init__(self,**kw):
        for k,v in kw.items():
            if hasattr(self,k):
                setattr(self,k,v)
            else:
                print "[Warning] Ignoring attribute %s" % k
            
        #self._inlines = self.inlines()
        
        if self.model is None:
            self.model = self.queryset.model
        if self.label is None:
            self.label = self.__class__.__name__
        if self.name is None:
            self.name = self.__class__.__name__
        if self.mode is not None:
            self.name += "_" + self.mode
            
        self._setup_done = False
        self._setup_doing = False
        
        register_report(self)
        # print "Report.__init__() done:", self.name
        
    def setup(self):
        if self._setup_done:
            return
        if self._setup_doing:
            return
        self._setup_doing = True
        #~ if self.form_class is None:
            #~ self.form_class = modelform_factory(self.model)
        if self.row_layout_class is None:
            self.row_layout = layouts.RowLayout(self,0,self.columnNames)
        else:
            assert self.columnNames is None
            self.row_layout = self.row_layout_class(self,0)
            
        #self.columns = [e for e in self.row_layout.walk() if isinstance(e,FieldElement)]
        
        if self.master:
            self.fk = _get_foreign_key(self.master,
              self.model,self.fk_name)
            #self.name = self.fk.rel.related_name
        self.layouts = [ self.row_layout ]
        index = 1
        for lc in self.page_layouts:
            self.layouts.append(lc(self,index))
            index += 1
            
        #~ if len(self.page_layouts) == 1:
            #~ self.page_layout = self.page_layouts[0](self)
        #~ else:
            #~ self.page_layout = layouts.TabbedPageLayout(self,
              #~ self.page_layouts)
        #~ self._page_layouts = [
              #~ layout(self) for layout in self.page_layouts]
        
        self.store = layouts.Store(self)
        
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
        
    def get_choices(self,field):
        # TODO : if hasattr(self,"%s_choices" % field.name)...
        return get_combo_report(field.rel.to)
        
    #~ def slaves(self):
        #~ hier: und zwar die slaves in diesem report (nicht alle slaves des modells)
      
        #~ if self._slaves is None:
            #~ self._slaves = {}
            #~ for cl in slave_reports(self.model):
                #~ rpt = cl()
                #~ self._slaves[rpt.name] = rpt
            #print "reports.Report.slaves()", self.__class__.__name__, ":", self._slaves
        #~ return self._slaves.values()
        
        
    def column_headers(self):
        self.setup()
        for e in self.columns:
            yield e.label
            
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
            if master_instance is None:
                master_instance = self.master_instance
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
    
    #~ def get_row_print_template(self,instance):
        #~ return instance._meta.db_table + "_print.html"
        
    #~ def page_layout(self,i=0):
        #~ if self._page_layouts is None:
            #~ self._page_layouts = [ 
              #~ l(self.model) for l in self.page_layouts]
        #~ return self._page_layouts[i]

    #~ def can_view(self,request,row=None):
        #~ return True
        
    #~ def can_add(self,request,row=None):
        #~ return True
        
    #~ def can_change(self,request,row=None):
        #~ return request.user.is_authenticated()
        
        
    #~ def __unicode__(self):
        #~ #return unicode(self.as_text())
        #~ return unicode("%d row(s)" % self.queryset.count())
    
    def unused_get_urls(self,name):
        if self.url:
            raise RuntimError("Report.get_urls() called again.")
        self.url = "/" + name
        l = []
        l.append(url(r'^%s/(\d+)$' % name, self.view_one))
        #l.append(url(r'^%s/(\d+)/(.+)$' % name, self.view_one_slave))
        l.append(url(r'^%s$' % name, self.view_many))
        #l.append(url(r'^%s/(\d+)/pdf$' % name, self.pdf_one))
        #l.append(url(r'^%s/pdf$' % name, self.pdf_many))
        #l.append(url(r'^%s/flexigrid$' % name, self.flexigrid))
        l.append(url(r'^%s/update$' % name, self.ajax_update))
        #l.append(url(r'^%s/(\d+)/print$' % name, self.print_one))
        #l.append(url(r'^%s/print$' % name, self.print_many))
        #l.append(url(r'^%s/json$' % name, self.json))
        #l.append(url(r'^%s/(\d+)/json$' % name, self.json_one))
        return l

        
    def ext_components(self):
        if len(self.layouts) == 2:
            return [ self.store ] + self.layouts
        return [ self.store, self.layouts[0], layouts.TabbedPanel("EastPanel",self.layouts[1:]) ]
        #~ tabitems = self.layouts[1:]
        #~ tabpanel = layouts.Component("EastPanel",xtype="tabpanel",
          #~ region="east",
          #~ items=layouts.js_code("[%s]" % ",".join([l.name for l in tabitems])))
        #~ return [tabpanel]

    def unused_view_many(self,request):
        #~ msg = "Hello, "+unicode(request.user)
        #~ print msg
        #~ request.user.message_set.create(msg)
        r = render.ViewReportRenderer(request,self)
        #~ if is_editing(request) and self.can_change.passes(request):
            #~ r = render.EditManyReportRenderer(request,True,self)
        #~ else:
            #~ r = render.ListViewReportRenderer(request,True,self)
        return r.render_to_response()
        
    #~ def renderer(self,request):
        #~ return render.ListViewReportRenderer(request,False,self)
        
            
    def unused_view_one(self,request,**kw):
        #print "Report.view_one()", request.path
        if not self.can_view.passes(request):
            return urls.sorry(request)
        r = render.ViewOneReportRenderer(request,True,self,**kw)
        #~ if is_editing(request) and self.can_change.passes(request):
            #~ r = render.EditOneReportRenderer(row_num,request,True,self,**kw)
        #~ else:
            #~ r = render.ViewOneReportRenderer(row_num,request,True,self,**kw)
        return r.render_to_response()

    #~ def view_one_slave(self,request,row_num,slave_name):
        #~ if not self.can_view.passes(request):
            #~ return render.sorry(request)
        #~ r = render.ViewOneReportRenderer(row_num,request,True,self)
        #~ sl = r.get_slave(slave_name)
        #~ slr = render.ListViewReportRenderer(request,True,sl)
        #~ return slr.render_to_response()

    #~ def pdf_one(self,request,row):
        #~ if not self.can_view.passes(request):
            #~ return urls.sorry(request)
        #~ return render.PdfOneReportRenderer(row,request,True,self).render()
        
    #~ def pdf_many(self, request):
        #~ if not self.can_view.passes(request):
            #~ return urls.sorry(request)
        #~ return render.PdfManyReportRenderer(request,True,self).render()

        
    def old_json(self, request):
        #print "json:", self
        if not self.can_view.passes(request):
            return None
        qs = self.get_queryset()
        sort = request.GET.get('sort',None)
        if sort:
            sort_dir = request.GET.get('dir','ASC')
            if sort_dir == 'DESC':
                sort = '-'+sort
            qs = qs.order_by(sort)
        offset = request.GET.get('start',None)
        if offset:
            lqs = qs[int(offset):]
        else:
            lqs = qs
        limit = request.GET.get('limit',self.page_length)
        if limit:
            lqs = lqs[:int(limit)]
        rows = [ self.obj2json(row) for row in lqs ]
        d = dict(count=qs.count(),rows=rows)
        s = simplejson.dumps(d,default=unicode)
        #print s
        return HttpResponse(s, mimetype='text/html')
        
        
    #~ def json_one(self,request,row):
        #~ if not self.can_view.passes(request):
            #~ return None
        #~ qs = self.get_queryset()
        #~ rows = [ self.obj2json(qs[int(row)]) ]
        #~ d = dict(count=qs.count(),rows=rows)
        #~ s = simplejson.dumps(d,default=unicode)
        #~ #print s
        #~ return HttpResponse(s, mimetype='text/html')
        
        
    def ajax_update(self,request):
        print request.POST
        return HttpResponse("1", mimetype='text/x-json')

    #~ def flexigrid(self, request):
        #~ if not self.can_view.passes(request):
            #~ return render.sorry(request)
        #~ r = render.FlexigridRenderer(request,True,self)
        #~ return r.render_to_response()
        
    def unused_print_many(self, request):
        if not self.can_view.passes(request):
            return urls.sorry(request)
        return render.PdfManyReportRenderer(request,True,self).render(as_pdf=False)

    def unused_print_one(self,request,row):
        if not self.can_view.passes(request):
            return urls.sorry(request)
        return render.PdfOneReportRenderer(row,request,True,self).render(as_pdf=False)

    def as_text(self, *args,**kw):
        from lino.django.utils.renderers_text import TextReportRenderer
        return TextReportRenderer(self,*args,**kw).render()
        
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
    
        