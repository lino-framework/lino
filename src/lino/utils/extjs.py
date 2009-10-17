## Copyright 2009 Luc Saffre

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
import types
#import logging ; logger = logging.getLogger("lino.extjs")

from dateutil import parser as dateparser

#from django import forms
from django.db import models
from django.conf import settings
from django.http import HttpResponse
from django.utils import simplejson

#from django.utils.safestring import mark_safe
#from django.utils.text import capfirst
#from django.template.loader import render_to_string

from lino.utils.sites import lino_site

from . import reports, menus

EXT_CHAR_WIDTH = 9
EXT_CHAR_HEIGHT = 12

def define_vars(variables,indent=0):
    sep = "\n" + ' ' * indent
    s = ''
    for v in variables:
        #lino_site.log.debug("define_vars() : %s", v.ext_name)
        for ln in v.ext_lines_before():
            s += sep + ln 
        s += sep + "var %s = %s;" % (v.ext_name,v.as_ext_value())
        for ln in v.ext_lines_after():
            s += sep + ln 
    return s


def dict2js(d):
    return ", ".join(["%s: %s" % (k,py2js(v)) for k,v in d.items()])

class ReportRenderer:
    def __init__(self,report,**kw):
        setup_report(report)
        self.ext_name = report.app_label + "_" + report.name
        self.options = kw
        self.report = report
        self.windows = [ LayoutWindow(layout) 
            for layout in report.layouts[1:] ]
        
    def ext_lines(self):
        yield define_vars([self.report.store])
        yield "%s.addListener({exception: function(a,b,c) { " % self.report.store.ext_name
        yield "  console.log(a,b,c);"
        yield "  Ext.MessageBox.alert('Exception in %s','no data');" % self.report.store.ext_name
        yield "}});"
        yield ''
        for win in self.windows:
            yield "var %s_win;" % win.name
            for ln in win.ext_lines():
                yield ln
            yield '// end of window %s' % win.name
            yield ''
  
class LayoutWindow:
    def __init__(self,layout,**kw):
        self.options = kw
        self.layout = layout
        #self.ext_name = report.app_label + "_" + report.name
        self.name = layout.name
        
    def ext_lines(self):
        self.options.update(title=self.layout.get_title())
        self.options.update(closeAction='hide')
        self.options.update(maximizable=True)
        self.options.update(id=self.name)
        self.options.update(layout='fit')
        self.options.update(height=300,width=800)
        self.options.update(items=self.layout._main)
        #kw.update(maximized=True)
        if self.layout.report.master is not None:
            yield "function %s(btn,event,master,master_grid) { " % self.name
        else:
            yield "function %s(btn,event) { " % self.name
        yield "  if(!%s_win){" % self.name
        yield define_vars(self.layout._main.ext_variables(),indent=4)
        yield "    %s_win = new Ext.Window( %s );" % (self.name,py2js(self.options))
        
        if isinstance(self.layout._main,MainGridElement):
            yield "%s_win.grid = %s;" % (self.name,self.layout._main.ext_name)
        
        yield "  }"
        if self.layout.report.master is None:
            yield "  %s.load();" % self.layout.report.store.ext_name
        else:
            yield "  if(master) {"
            yield "    %s.setBaseParam('master',master);" % self.layout.report.store.ext_name
            yield "    %s.load();" % self.layout.report.store.ext_name
            #yield "    %s.load({master:master});" % self.layout.report.store.ext_name
            yield "  } else {"
            yield "    master_grid.getSelectionModel().addListener('rowselect',function(sm,rowIndex,record) {"
            yield "      console.log(rowIndex,record);" 
            yield "      %s.load({params:{master:record.id}});" % self.layout.report.store.ext_name
            #~ yield "      %s.load({params:{master:record.data.%s}});" % (
                #~ self.layout.report.store.ext_name,self.layout.report.store.pk.name)
            yield "    })"
            yield "  }"
        yield "  %s_win.show();" % self.name
        yield "}\n"
      
#~ def get_report_windows(rpt,**kw):
    #~ setup_report(rpt)
    #~ for layout in rpt.layouts[1:]:
        #~ yield LayoutWindow(layout,**kw)
        
      

def py2js(v,**kw):
    #logger.debug("py2js(%r,%r)",v,kw)
    #~ if isinstance(v,reports.Report):
        #~ self = v
        #~ setup_report(self)
        #~ s = ''
        #~ for layout in self.layouts[1:]:
            #~ kw.update(items=layout._main)
            #~ kw.update(title=layout.get_title())
            #~ kw.update(closeAction='hide')
            #~ kw.update(maximizable=True)
            #~ #kw.update(maximized=True)
            #~ if self.master is not None:
                #~ s += "function %s(btn,event,master,master_grid) { " % layout.name
            #~ else:
                #~ s += "function %s(btn,event) { " % layout.name
            #~ s += "\n  var win;\n  if(!win){"
            #~ s += define_vars(layout._main.ext_variables(),indent=4)
            #~ s += "\n    win = new Ext.Window( %s );" % py2js(kw)
            #~ if self.master is not None:
                #~ s += "\n    if(master)"
                #~ s += "\n      %s.setBaseParam('master',master);" % layout.store.ext_name
                #~ s += "\n    else {"
                #~ s += "\n      master_grid.getSelectionModel().addListener('rowselect',function(sm,rowIndex,record) {"
                #~ s += "\n        %s.load({params:{master:record.data.%s}});" % (layout.store.ext_name,layout.store.pk.name)
                #~ s += "\n      })"
                #~ s += "\n    }"
            #~ s += "\n    %s.addListener(" % layout.store.ext_name
            #~ s += "{exception: function() { Ext.MessageBox.alert('exception','no data');win.hide();}});"
            #~ s += "\n  }"
            #~ if self.master is None:
                #~ s += "\n  %s.load();" % layout.store.ext_name
            #~ s += "\n  win.show();"
            #~ s += "\n}\n"
            
        #~ return s
        
        
    if isinstance(v,menus.Menu):
        if v.parent is None:
            kw.update(region='north',height=27,items=v.items)
            return "new Ext.Toolbar(%s);" % py2js(kw)
        kw.update(text=v.label,menu=dict(items=v.items))
        return py2js(kw)
        
    if isinstance(v,menus.MenuItem):
        ext_name = v.actor.app_label + "_" + v.actor.name + "1"
        if v.args:
            handler = "function(btn,evt) {%s(btn,evt,%s);}" % (
                ext_name,
                ",".join([py2js(a) for a in v.args]))
        else:
            handler = ext_name
        return py2js(dict(text=v.label,handler=js_code(handler)))
    if isinstance(v,Component):
        return v.as_ext(**kw)
        
    assert len(kw) == 0, "py2js() : value %r cannot get keyword parameters" % v
    if type(v) is types.ListType:
        return "[ %s ]" % ", ".join([py2js(x) for x in v])
    if type(v) is types.DictType:
        return "{ %s }" % ", ".join([
            "%s: %s" % (k,py2js(v)) for k,v in v.items()])
    if type(v) is types.BooleanType:
        return str(v).lower()
    if type(v) is unicode:
        return repr(v.encode('utf8'))
    return repr(v)
            
class js_code:
    "A string that py2js will represent as is, not between quotes."
    def __init__(self,s):
        self.s = s
    def __repr__(self):
        return self.s
        
        
        
        
        
        
def setup_report(rpt):
    "adds ExtJS specific stuff to a Report instance"
    rpt.setup()
    if False: # not hasattr(rpt,'choice_store'):
        #rpt.choice_store = Store(rpt,rpt.choice_layout,mode='choice',autoLoad=True)
        for layout in rpt.layouts:
            if not hasattr(layout,'choice_store'):
                layout.store = Store(rpt,layout) #,autoLoad=True
        #~ rpt.variables = []
        #~ for layout in rpt.layouts:
            #~ layout.store = Store(rpt,layout) #,autoLoad=True
            #~ for v in layout._main.ext_variables():
                #~ rpt.variables.append(v)
        #~ tabs = [l._main for l in rpt.store.layouts]
        #~ comp = TabPanel(None,"MainPanel",*tabs)
        #~ rpt.variables.append(comp)
        #~ rpt.variables.sort(lambda a,b:cmp(a.declaration_order,b.declaration_order))
        
        
        
def grid_afteredit_view(request,**kw):
    kw['colname'] = request.POST['colname']
    return json_report_view(request,**kw)
    
def form_submit_view(request,**kw):
    #kw['submit'] = True
    return json_report_view(request,**kw)

def list_report_view(request,**kw):
    kw['simple_list'] = True
    return json_report_view(request,**kw)

def json_report_view(request,app_label=None,rptname=None,
                     action=None,colname=None,simple_list=False):
    rpt = reports.get_report(app_label,rptname)
    if rpt is None:
        return json_response(success=False,
            msg="%s : no such report" % rptname)
    if not rpt.can_view.passes(request):
        return json_response(success=False,
            msg="User %s cannot view %s : " % (request.user,rptname))
    rptreq = reports.ViewReportRequest(request,rpt)
    if action:
        for a in rpt._actions:
            if a.name == action:
                d = a.get_response(rptreq)
                return json_response(**d)
        return json_response(
            success=False,
            msg="Report %r has no action %r" % (rpt.name,action))
    if simple_list:
        d = rptreq.render_to_json()
        return json_response(**d)

    pk = request.POST.get(rptreq.report.store.pk.name) #,None)
    #~ if pk == reports.UNDEFINED:
        #~ pk = None
    try:
        if pk in ('', None):
            #return json_response(success=False,msg="No primary key was specified")
            instance = rpt.model()
        else:
            instance = rpt.model.objects.get(pk=pk)
            
        for f in rptreq.report.store.fields:
            if not f.field.primary_key:
                f.update_from_form(instance,request.POST)
                    
        instance.save()
        return json_response(success=True,
              msg="%s has been saved" % instance)
    except Exception,e:
        traceback.print_exc(e)
        return json_response(success=False,msg="Exception occured: "+str(e))
    
def json_response(**kw):
    s = simplejson.dumps(kw,default=unicode)
    #return HttpResponse(s, mimetype='text/html')
    #s = py2js(kw)
    #print "json_response()", s
    return HttpResponse(s, mimetype='text/html')
    
def unused_view_report_as_json(request,app_label=None,rptname=None):
    rpt = reports.get_report(app_label,rptname)
    if rpt is None:
        return json_response(success=False,
            msg="%s : no such report" % rptname)
    if not rpt.can_view.passes(request):
        return json_response(success=False,
            msg="User %s cannot view %s : " % (request.user,rptname))
    r = reports.ViewReportRequest(request,rpt)
    #request._lino_report = r
    s = r.render_to_json()
    return HttpResponse(s, mimetype='text/html')
    
        
      
class Component:
    declared = False
    ext_suffix = ''
    value_template = "{ %s }"
    declaration_order = 9
    
    def __init__(self,name,**options):
        self.name = name
        self.options = options
        self.ext_name = name + self.ext_suffix        
        
    def ext_lines_after(self):
        return []
    def ext_lines_before(self):
        return []
        
    def ext_variables(self):
        if self.declared:
            yield self
        
    def ext_options(self,**kw):
        kw.update(self.options)
        return kw
        
    def as_ext_value(self):
        options = self.ext_options()
        return self.value_template % dict2js(options)
        
    def as_ext(self):
        if self.declared:
            return self.ext_name
        else:
            return self.as_ext_value()


class StoreField:

    def __init__(self,field,**options):
        self.field = field
        options['name'] = field.name
        self.options = options
        
    def as_js(self):
        return py2js(self.options)
        
    def write_to_form(self,obj,d):
        d[self.field.name] = getattr(obj,self.field.name)
    def update_from_form(self,instance,values):
        v = values.get(self.field.name)
        if v == '' and self.field.null:
            v = None
        setattr(instance,self.field.name,v)
        
class BooleanStoreField(StoreField):
    def __init__(self,field,**kw):
        kw['type'] = 'boolean'
        StoreField.__init__(self,field,**kw)
    def update_from_form(self,instance,values):
        v = values.get(self.field.name)
        if v == 'true':
            v = True
        else:
            v = False
        setattr(instance,self.field.name,v)

class DateStoreField(StoreField):
  
    def __init__(self,field,date_format,**kw):
        self.date_format = date_format
        kw['type'] = 'date'
        StoreField.__init__(self,field,**kw)
        
    def write_to_form(self,obj,d):
        value = getattr(obj,self.field.name)
        if value is not None:
            value = value.ctime() # strftime('%Y-%m-%d')
            #print value
            d[self.field.name] = value
            
    def update_from_form(self,instance,values):
        v = values.get(self.field.name)
        if v == '' and self.field.null:
            v = None
        if v is not None:
            print v
            v = dateparser.parse(v,fuzzy=True)
        setattr(instance,self.field.name,v)

class MethodStoreField(StoreField):
  
    def write_to_form(self,obj,d):
        meth = getattr(obj,self.field.name)
        d[self.field.name] = meth()
        
    def update_from_form(self,instance,values):
        pass
        #raise Exception("Cannot update a virtual field")


class OneToOneStoreField(StoreField):
        
    def update_from_form(self,instance,values):
        #v = values.get(self.field.name,None)
        v = values.get(self.field.name)
        if v == '' and self.field.null:
            v = None
        if v is not None:
            v = self.field.rel.to.objects.get(pk=v)
        setattr(instance,self.field.name,v)
        
    def write_to_form(self,obj,d):
        try:
            v = getattr(obj,self.field.name)
        except self.field.rel.to.DoesNotExist,e:
            v = None
        if v is None:
            d[self.field.name] = None
        else:
            d[self.field.name] = v.pk
        

class ForeignKeyStoreField(StoreField):
        
    def as_js(self):
        s = StoreField.as_js(self)
        s += "," + repr(self.field.name+"Hidden")
        return s 
        
    def update_from_form(self,instance,values):
        #v = values.get(self.name,None)
        #v = values.get(self.field.name+"Hidden",None)
        v = values.get(self.field.name+"Hidden")
        #print self.field.name,"=","%s.objects.get(pk=%r)" % (self.model.__name__,v)
        if v == '' and self.field.null:
            v = None
        if v is not None:
        #if len(v):
            try:
                v = self.field.rel.to.objects.get(pk=v)
            except self.field.rel.to.DoesNotExist,e:
                print "[update_from_form]", v, values.get(self.field.name)
        setattr(instance,self.field.name,v)
        
    def write_to_form(self,obj,d):
        try:
            v = getattr(obj,self.field.name)
        except self.field.rel.to.DoesNotExist,e:
            v = None
        if v is None:
            d[self.field.name+"Hidden"] = None
            d[self.field.name] = None
        else:
            d[self.field.name] = unicode(v)
            d[self.field.name+"Hidden"] = v.pk
        



class Store(Component):
    value_template = "new Ext.data.JsonStore({ %s })"
    declared = True
    ext_suffix = "_store"
    declaration_order = 1
    
    def __init__(self,report,**options):
        Component.__init__(self,report.app_label+"_"+report.name,**options)
        self.report = report
        #self.layout = layout
        #self.mode = mode
        
        fields = set()
        for layout in report.layouts:
            for fld in layout._store_fields:
                assert fld is not None, "%s"
                fields.add(fld)
                  
        self.pk = self.report.model._meta.pk
        assert self.pk is not None, "Cannot make Store for %s because %s has no pk" % (
          self.report.name,self.report.model)
        
        if not self.pk in fields:
            fields.add(self.pk)
            
        self.fields = [self.create_field(fld) for fld in fields]
          
        
    def create_field(self,fld):
        meth = getattr(fld,'_return_type_for_method',None)
        if meth is not None:
            # uh, this is tricky...
            return MethodStoreField(fld)
        if isinstance(fld,models.ManyToManyField):
            return StoreField(fld)
            #raise NotImplementedError
        if isinstance(fld,models.OneToOneField):
            return OneToOneStoreField(fld)
        if isinstance(fld,models.ForeignKey):
            #related_rpt = self.report.get_field_choices(fld)
            #self.related_stores.append(related_rpt.choice_store)
            return ForeignKeyStoreField(fld)
            #yield dict(name=fld.name)
            #yield dict(name=fld.name+"Hidden")
        if isinstance(fld,models.DateField):
            #return StoreField(fld,type="date",dateFormat='Y-m-d')
            #return StoreField(fld,type="date",dateFormat=self.report.date_format)
            return DateStoreField(fld,self.report.date_format)
        if isinstance(fld,models.IntegerField):
            return StoreField(fld,type="int")
        if isinstance(fld,models.AutoField):
            return StoreField(fld,type="int")
        if isinstance(fld,models.BooleanField):
            return BooleanStoreField(fld)
        return StoreField(fld)
        #~ else:
            #~ kw['type'] = DATATYPES.get(fld.__class__,'auto')
            #~ kw['dateFormat'] = 'Y-m-d'
            #~ kw['name'] = fld.name
            #~ yield kw

            
    def get_absolute_url(self,**kw):
        #~ if request._lino_request.report == self.report:
            #~ return request._lino_request.get_absolute_url(**kw)
        #~ else:
        #~ if self.report.master is not None:
            #~ kw.update(master=js_code('master'))
        #kw.update(layout=self.layout.index)
        return self.report.get_absolute_url(**kw)
        #~ if request._lino_report.report == self.report:
            #~ #rr = request._lino_report
            #~ layout = self.layout
            #~ url = request._lino_report.get_absolute_url(json=True)
        #~ else:
            #~ # it's a slave
            #~ layout = request._lino_report.report.row_layout
            #~ #rr = self.report.renderer()
            #~ url = self.report.get_absolute_url(json=True)
      
    def ext_options(self):
        d = Component.ext_options(self)
        #self.report.setup()
        #data_layout = self.report.layouts[self.layout_index]
        d.update(storeId=self.ext_name)
        d.update(remoteSort=True)
        #~ if self.report.master is None:
            #~ d.update(autoLoad=True)
        #~ else:
            #~ d.update(autoLoad=False)
        #url = self.report.get_absolute_url(json=True,mode=self.mode)
        #url = self.get_absolute_url(json=True)
        #self.report.setup()
        proxy = dict(url=self.get_absolute_url(simple_list=True),method='GET')
        d.update(proxy=js_code(
          "new Ext.data.HttpProxy(%s)" % py2js(proxy)
        ))
        # a JsonStore without explicit proxy sometimes used method POST
        # d.update(url=self.rr.get_absolute_url(json=True))
        # d.update(method='GET')
        d.update(totalProperty='count')
        d.update(root='rows')
        d.update(id=self.pk.name)
        d.update(fields=[js_code(f.as_js()) for f in self.fields])
        #d.update(listeners=dict(exception=js_code("on_store_exception")))
        return d
        
        

class ColumnModel(Component):
    declared = True
    ext_suffix = "_cols"
    value_template = "new Ext.grid.ColumnModel({ %s })"
    declaration_order = 2
    
    def __init__(self,grid):
        self.grid = grid
        Component.__init__(self,grid.name)
        #grid.layout.report.add_variable(self)

        #Element.__init__(self,layout,report.name+"_cols"+str(layout.index))
        #Element.__init__(self,layout,report.name+"_cols")
        #self.report = report
        
        #~ columns = []
        #~ for e in layout.walk():
            #~ if isinstance(e,FieldElement):
                #~ columns.append(e)
        #~ self.columns = columns
        
    #~ def __init__(self,layout,report):
        #~ self.layout = layout # the owning layout
        #~ self.report = report
        #~ self.name = report.name
        
        
    def ext_options(self):
        #self.report.setup()
        d = Component.ext_options(self)
        #editing = self.layout.report.can_change.passes(request)
        #l = [e.as_ext_column(request) for e in self.report.columns]
        #d.update(columns=js_code("[ %s ]" % ", ".join(l)))
        #~ self.columns = []
        #~ for e in self.grid.walk():
            #~ if isinstance(e,FieldElement):
                #~ self.columns.append(e)
                
        #~ d.update(columns=[js_code(e.as_ext_column(request)) for e in self.columns])
        d.update(columns=[js_code(e.as_ext_column()) for e in self.grid.elements])
        #d.update(defaultSortable=True)
        return d
        

class VisibleComponent(Component):
    width = None
    height = None
    
    def __init__(self,name,width=None,height=None,label=None,**kw):
        Component.__init__(self,name,**kw)
        if width is not None:
            self.width = width
        if height is not None:
            self.height = height
        if label is not None:
            self.label = label
    

    def __str__(self):
        "This shows how elements are specified"
        if self.width is None:
            return self.name
        if self.height is None:
            return self.name + ":%d" % self.width
        return self.name + ":%dx%d" % (self.width,self.height)
        
    def pprint(self,level=0):
        return ("  " * level) + self.__str__()
        
    def walk(self):
        return [ self ]
        
class LayoutElement(VisibleComponent):
    stored = False
    ext_name = None
    ext_suffix = ""
    data_type = None 
    parent = None # will be set by Container
    
    label = None
    label_width = 0 
    editable = False
    sortable = False
    xpadding = 5
    preferred_width = 10
    
    def __init__(self,layout,name,**kw):
        #print "Element.__init__()", layout,name
        #self.parent = parent
        VisibleComponent.__init__(self,name,**kw)
        self.layout = layout
        if layout is not None:
            #assert isinstance(layout,Layout), "%r is not a Layout" % layout
            self.ext_name = layout.name + "_" + name + self.ext_suffix
            #~ if self.declared:
                #~ self.layout.report.add_variable(self)
                

        
    def get_property(self,name):
        v = getattr(self,name,None)
        if self.parent is None or v is not None:
            return v
        return self.parent.get_property(name)
        
    #~ def get_width(self):
        #~ return self.width
        
    #~ def set_width(self,w):
        #~ self.width = w
        
    #~ def as_ext(self):
        #~ s = self.ext_editor(label=True)
        #~ if s is not None:
            #~ return mark_safe(s)
        #~ return self.name
        
    def get_column_options(self,**kw):
        kw.update(
          dataIndex=self.name, 
          editable=self.editable,
          header=unicode(self.label) if self.label else self.name,
          sortable=self.sortable
          )
        if self.editable:
            editor = self.get_field_options()
            kw.update(editor=js_code(py2js(editor)))
        if self.width:
            kw.update(width=self.width * EXT_CHAR_WIDTH)
        else:
            assert self.preferred_width is not None,"%s : preferred_width" % self.ext_name
            kw.update(width=self.preferred_width * EXT_CHAR_WIDTH)
        return kw    
        
    def as_ext_column(self):
        kw = self.get_column_options()
        return "{ %s }" % dict2js(kw)
        
    #~ def as_ext_column(self,request):
        #~ d = dict(
          #~ dataIndex=self.name, 
          #~ header=unicode(self.label) if self.label else self.name,
          #~ sortable=self.sortable)
        #~ if self.width:
            #~ d.update(width=self.width * EXT_CHAR_WIDTH)
        #~ if request._lino_report.editing and self.editable:
            #~ fo = self.get_field_options(request)
            #~ # del fo['fieldLabel']
            #~ d.update(editor=js_code("{ %s }" % dict2js(fo)))
        #~ return "{ %s }" % dict2js(d)
    
    def ext_options(self):
        d = VisibleComponent.ext_options(self)
        if self.width is None:
            """
            an element without explicit width will get flex=1 when in a hbox, otherwise anchor="100%".
            """
            #if isinstance(self.parent,HBOX):
            assert self.parent is not None, "%s %s : parent is None!?" % (self.__class__.__name__,self.ext_name)
            if self.parent.vertical:
                d.update(anchor="100%")
            else:
                d.update(flex=1)
        else:
            d.update(width=self.ext_width())
        if self.height is not None:
            d.update(height=(self.height+2) * EXT_CHAR_HEIGHT)
        return d
        
    def ext_width(self):
        if self.width is None:
            return None
        #if self.parent.labelAlign == 'top':
        return max(self.width,self.label_width) * EXT_CHAR_WIDTH + self.xpadding
        #return (self.width + self.label_width) * EXT_CHAR_WIDTH + self.xpadding
        
        
    #~ def as_ext(self):
        #~ try:
            #~ context = dict(
              #~ element = self
            #~ )
            #~ return render_to_string(self.ext_template,context)
        #~ except Exception,e:
            #~ traceback.print_exc(e)
        
    #~ def ext_column(self,editing):
        #~ s = """
        #~ {
          #~ dataIndex: '%s', 
          #~ header: '%s', 
          #~ sortable: true,
        #~ """ % (self.name, self.label)
        #~ if self.width:
            #~ s += " width: %d, " % (self.width * 10)
        #~ if editing and self.editable:
            #~ s += " editor: %s, " % self.ext_editor(label=False)
        #~ s += " } "
        #~ return s
        
        
    #~ def ext_editor(self,label=False):
        #~ s = " new Ext.form.TextField ({ " 
        #~ s += " name: '%s', " % self.name
        #~ if label:
            #~ s += " fieldLabel: '%s', " % self.label
        #~ s += " disabled: true, " 
        #~ s += """
          #~ }) """
        #~ return s
        

class StaticText(LayoutElement):
    def __init__(self,text):
          self.text = text
    def render(self,row):
        return self.text
          
#~ django2ext = (
    #~ (models.TextField, 'Ext.form.TextArea'),
    #~ (models.CharField, 'Ext.form.TextField'),
    #~ (models.DateField, 'Ext.form.DateField'),
    #~ (models.IntegerField, 'Ext.form.NumberField'),
    #~ (models.DecimalField, 'Ext.form.NumberField'),
    #~ (models.BooleanField, 'Ext.form.Checkbox'),
    #~ (models.ForeignKey, 'Ext.form.ComboBox'),
    #~ (models.AutoField, 'Ext.form.NumberField'),
#~ )


#~ def ext_class(field):
    #~ for cl,x in django2ext:
        #~ if isinstance(field,cl):
            #~ return x
            
#~ _ext_options = (
    #~ (models.TextField, dict(xtype='textarea')),
    #~ (models.CharField, dict(xtype='textfield')),
    #~ (models.DateField, dict(xtype='datefield')),
    #~ (models.IntegerField, dict(xtype='numberfield')),
    #~ (models.DecimalField, dict(xtype='numberfield')),
    #~ (models.BooleanField, dict(xtype='checkbox')),
    #~ (models.ForeignKey, dict(xtype='combo')),
    #~ (models.AutoField, dict(xtype='numberfield')),
#~ )
            
#~ def ext_options(field):
    #~ for cl,x in _ext_options:
        #~ if isinstance(field,cl):
            #~ return x

class FieldElement(LayoutElement):
    declared = True
    stored = True
    declaration_order = 3
    #name_suffix = "field"
    def __init__(self,layout,field,**kw):
        LayoutElement.__init__(self,layout,field.name,label=field.verbose_name,**kw)
        self.field = field
        self.editable = field.editable and not field.primary_key
        
    def get_column_options(self,**kw):
        kw = LayoutElement.get_column_options(self,**kw)
        if self.editable:
        #if request._lino_request.editing and self.editable:
            fo = self.get_field_options()
            kw.update(editor=js_code("{ %s }" % dict2js(fo)))
        return kw    
        

    #~ def value2js(self,obj):
        #~ return getattr(obj,self.name)
        
    #~ def render(self,row):
        #~ return row.render_field(self)
        
    #~ def ext_editor(self,label=False):
        #~ cl = ext_class(self.field)
        #~ if not cl:
            #~ print "no ext editor class for field ", \
              #~ self.field.__class__.__name__, self
            #~ return None
        #~ s = " new %s ({ " % cl
        #~ s += " name: '%s', " % self.name
        #~ if label:
            #~ s += " fieldLabel: '%s', " % self.label
        #~ if not self.field.blank:
            #~ s += " allowBlank: false, "
        #~ if isinstance(self.field,models.CharField):
            #~ s += " maxLength: %d, " % self.field.max_length
        #~ s += """
          #~ }) """
        #~ return s
        
    def get_field_options(self,**kw):
        kw.update(xtype=self.xtype,name=self.name)
        kw.update(anchor="100%")
        #kw.update(style=dict(padding='0px'),color='green')
        if self.label:
            kw.update(fieldLabel=unicode(self.label))
        if not self.field.blank:
            kw.update(allowBlank=False)
        if not self.editable:
            kw.update(readOnly=True)
        return kw
        
    def get_panel_options(self,**kw):
        d = LayoutElement.ext_options(self,**kw)
        d.update(xtype='panel',layout='form')
        #d.update(style=dict(padding='0px'),color='green')
        #d.update(hideBorders=True)
        #d.update(margins='0')
        return d

    def ext_options(self,**kw):
        """
        ExtJS renders fieldLabels only if the field's container has layout 'form', so we create a panel around each field
        """
        fo = self.get_field_options()
        po = self.get_panel_options()
        po.update(items=js_code("[ { %s } ]" % dict2js(fo)))
        return po
        
class TextFieldElement(FieldElement):
    xtype = 'textarea'
    #width = 60
    preferred_width = 60
    #~ def __init__(self,*args,**kw):
        #~ FieldElement.__init__(self,*args,**kw)
        #~ assert self.name != '__unicode__'


class CharFieldElement(FieldElement):
    xtype = "textfield"
    sortable = True
  
    def __init__(self,*args,**kw):
        FieldElement.__init__(self,*args,**kw)
        self.preferred_width = min(20,self.field.max_length)
        if self.width is None and self.field.max_length < 10:
            # "small" texfields should not be expanded, so they get an explicit width
            self.width = self.field.max_length
            
    def get_field_options(self,**kw):
        kw = FieldElement.get_field_options(self,**kw)
        kw.update(maxLength=self.field.max_length)
        return kw

        
class ForeignKeyElement(FieldElement):
    xtype = "combo"
    sortable = True
    #width = 20
    
    def __init__(self,*args,**kw):
        FieldElement.__init__(self,*args,**kw)
        self.report = self.layout.report.get_field_choices(self.field)
        #~ if self.editable:
            #~ setup_report(self.choice_report)
            #self.store = rpt.choice_store
            #self.layout.choice_stores.append(self.store)
            #self.report.setup()
            #self.store = Store(rpt,autoLoad=True)
            #self.layout.report.add_variable(self.store)
      
    #~ def ext_variables(self):
        #~ #yield self.store
        #~ setup_report(self.report)
        #~ yield self.report.choice_layout.store
        #~ yield self
        
    def get_field_options(self,**kw):
        kw = FieldElement.get_field_options(self,**kw)
        if self.editable:
            setup_report(self.report)
            kw.update(store=js_code(self.report.store.ext_name))
            #kw.update(store=js_code(self.store.as_ext_value(request)))
            kw.update(hiddenName=self.name+"Hidden")
            kw.update(valueField=self.report.store.pk.attname)
            #kw.update(valueField=self.name)
            """
            valueField: The underlying data value name to bind to this ComboBox (defaults to undefined if mode = 'remote' or 'field2' if transforming a select or if the field name is autogenerated based on the store configuration).

Note: use of a valueField requires the user to make a selection in order for a value to be mapped. See also hiddenName, hiddenValue, and displayField.
            """
            kw.update(displayField=self.report.display_field)
            kw.update(typeAhead=True)
            #kw.update(lazyInit=False)
            kw.update(mode='remote')
            kw.update(selectOnFocus=True)
            #kw.update(pageSize=self.store.report.page_length)
            
        kw.update(triggerAction='all')
        kw.update(emptyText='Select a %s...' % self.report.model.__name__)
        return kw
        
    #~ def value2js(self,obj):
        #~ v = getattr(obj,self.name)
        #~ if v is not None:
            #~ return v.pk
        
    #~ def as_store_field(self):
        #~ return "{ %s },{ %s }" % (
          #~ dict2js(dict(name=self.name)),
          #~ dict2js(dict(name=self.name+"Hidden"))
        #~ )

        
            
class DateFieldElement(FieldElement):
    xtype = 'datefield'
    data_type = 'date' # for store column
    sortable = True
    preferred_width = 8 
    # todo: DateFieldElement.preferred_width should be computed from Report.date_format
    
    def get_column_options(self,**kw):
        kw = FieldElement.get_column_options(self,**kw)
        kw.update(xtype='datecolumn')
        kw.update(format=self.layout.report.date_format)
        return kw
    
class IntegerFieldElement(FieldElement):
    xtype = 'numberfield'
    sortable = True
    width = 8
    data_type = 'int' 

class DecimalFieldElement(FieldElement):
    xtype = 'numberfield'
    sortable = True
    data_type = 'float' 
    
    def __init__(self,*args,**kw):
        FieldElement.__init__(self,*args,**kw)
        if self.width is None:
            self.width = min(10,self.field.max_digits) \
                + self.field.decimal_places
                
    def get_column_options(self,**kw):
        kw = FieldElement.get_column_options(self,**kw)
        kw.update(xtype='numbercolumn')
        kw.update(align='right')
        fmt = "0,000"
        if self.field.decimal_places > 0:
            fmt += "." + ("0" * self.field.decimal_places)
        kw.update(format=fmt)
        return kw
        
                

class BooleanFieldElement(FieldElement):
  
    xtype = 'checkbox'
    data_type = 'boolean' 
    
    #~ def __init__(self,*args,**kw):
        #~ FieldElement.__init__(self,*args,**kw)
        
    def get_column_options(self,**kw):
        kw = FieldElement.get_column_options(self,**kw)
        kw.update(xtype='booleancolumn')
        kw.update(trueText=self.layout.report.boolean_texts[0])
        kw.update(falseText=self.layout.report.boolean_texts[1])
        kw.update(undefinedText=self.layout.report.boolean_texts[2])
        return kw
        
    def update_from_form(self,instance,values):
        """
        standard HTML submits checkboxes of a form only when they are checked.
        So if the field is not contained in values, we take False as value.
        """
        setattr(instance,self.name,values.get(self.name,False))

  
class MethodElement(FieldElement):
    stored = True
    editable = False

    def __init__(self,layout,name,meth,**kw):
        # uh, this is tricky...
        #self.meth = meth
        field = getattr(meth,'return_type',None)
        if field is None:
            field = models.TextField(max_length=200)
            #meth.return_type = field
        #~ else:
            #~ print "MethodElement", field.name
        field.name = name
        field._return_type_for_method = meth
        FieldElement.__init__(self,layout,field)
        delegate = field2elem(layout,field,**kw)
        for a in ('ext_width','ext_options',
          'get_column_options','get_field_options'):
            setattr(self,a,getattr(delegate,a))
        

class Container(LayoutElement):
    #ext_template = 'lino/includes/element.js'
    #ext_container = 'Ext.Panel'
    vertical = False
    hpad = 1
    is_fieldset = False
    preferred_width = None
    
    # ExtJS options
    frame = True
    labelAlign = 'top'
    #labelAlign = 'left'
    
    def __init__(self,layout,name,*elements,**kw):
        LayoutElement.__init__(self,layout,name,**kw)
        #print self.__class__.__name__, elements
        #self.label = kw.get('label',self.label)
        self.elements = elements
        for e in elements:
            if not isinstance(e,LayoutElement):
                raise Exception("%r is not a LayoutElement" % e)
        #~ self.elements = []
        #~ for elem in elements:
            #~ assert elem is not None
            #~ if type(elem) == str:
                #~ if "\n" in elem:
                    #~ lines = []
                    #~ for line in elem.splitlines():
                        #~ line = line.strip()
                        #~ if len(line) > 0 and not line.startswith("#"):
                            #~ lines.append(layout,line)
                        #~ self.elements.append(VBOX(layout,None,*lines))
                #~ else:
                    #~ for name in elem.split():
                        #~ if not name.startswith("#"):
                            #~ self.elements.append(layout[name])
            #~ else:
                #~ self.elements.append(elem)
        self.compute_width()
        
        # some more analysis:
        for e in self.elements:
            e.parent = self
            if isinstance(e,FieldElement):
                self.is_fieldset = True
                #~ if self.label_width < e.label_width:
                    #~ self.label_width = e.label_width
                if e.label:
                    w = len(e.label) + 1 # +1 for the ":"
                    if self.label_width < w:
                        self.label_width = w
            if e.width == self.width:
                """
                e was the width-giving element for this container.
                remove e's width to avoid padding differences.
                """
                e.width = None
        lino_site.log.debug("%s.%s %s : elements = %s",self.layout.name,self.__class__.__name__,self.name,self.elements)
                
    def compute_width(self,unused_insist=False):
        """
        If all children have a width (in case of a horizontal container), 
        or (in a vertical layout) if at at least one element has a width, 
        then my width is also known.
        """
        if self.width is None:
            #print self, "compute_width..."
            w = 0
            xpadding = self.xpadding
            for e in self.elements:
                ew = e.width or e.preferred_width
                #~ ew = e.width
                #~ if ew is None and insist:
                    #~ ew = e.preferred_width
                if self.vertical:
                    if ew is not None:
                        if w < ew:
                            w = ew
                            xpadding = e.xpadding
                        # w = max(w,e.width) # + self.hpad*2)
                else:
                    if ew is None:
                        return # don't set this container's width since at least one element is flexible
                    w += ew # + self.hpad*2
                    xpadding += e.xpadding
            if w > 0:
                self.width = w
                self.xpadding = xpadding
                
        
    #~ def children(self):
        #~ return self.elements
        
    def walk(self):
        l = [ self ]
        for e in self.elements:
            l += e.walk()
        return l
        
    #~ def __str__(self):
        #~ s = Element.__str__(self)
        #~ # self.__class__.__name__
        #~ s += "(%s)" % (",".join([str(e) for e in self.elements]))
        #~ return s

    def pprint(self,level=0):
        margin = "  " * level
        s = margin + str(self) + ":\n"
        # self.__class__.__name__
        for e in self.elements:
            for ln in e.pprint(level+1).splitlines():
                s += ln + "\n"
        return s

    #~ def render(self,row):
        #~ try:
            #~ context = dict(
              #~ element = BoundElement(self,row),
              #~ renderer = row.renderer
            #~ )
            #~ return render_to_string(self.template,context)
        #~ except Exception,e:
            #~ traceback.print_exc(e)
            #~ raise
            #~ #print e
            #~ #return mark_safe("<PRE>%s</PRE>" % e)
            
    def ext_options(self):
        d = LayoutElement.ext_options(self)
        if self.is_fieldset:
            d.update(labelWidth=self.label_width * EXT_CHAR_WIDTH)
        #if not self.is_fieldset:
        #d.update(frame=self.get_property('frame'))
        d.update(frame=self.frame)
        d.update(border=False)
        d.update(labelAlign=self.get_property('labelAlign'))
        l = [e.as_ext() for e in self.elements ]
        d.update(items=js_code("[\n  %s\n]" % (", ".join(l))))
        return d
            
    #~ def as_ext(self,request,**kw):
        #~ options = self.ext_options(request)
        #~ options.update(kw)
        #~ s = "{ "
        #~ s += ", ".join(["%s: %s" % (k,py2js(v,k)) for k,v in options.items()])
        #~ s += ", items: [\n  %s\n]" % (", ".join([e.as_ext(request) for e in self.elements]))
        #~ #s += extra
        #~ s += " }\n"
        #~ return mark_safe(s)
        
    def ext_variables(self):
        for e in self.elements:
            for v in e.ext_variables():
                yield v
        if self.declared:
            yield self
        
    def ext_lines_after(self):
        for e in self.elements:
            for v in e.ext_lines_after():
                yield v
                
    def ext_lines_before(self):
        for e in self.elements:
            for v in e.ext_lines_before():
                yield v
                


class Panel(Container):
    declared = True
    ext_suffix = "_panel"
        
    def __init__(self,layout,name,vertical,*elements,**kw):
        self.vertical = vertical
        Container.__init__(self,layout,name,*elements,**kw)
        
    def ext_options(self,**d):
        d = Container.ext_options(self,**d)
        d.update(xtype='panel')
        #d.update(margins='0')
        #d.update(style=dict(padding='0px'))
        d.update(style=dict(padding='0px'))
        if len(self.elements) == 1:
            d.update(layout='fit')
        elif self.vertical:
            d.update(layout='anchor')
        else:
            d.update(layout='hbox')
        return d
        

class TabPanel(Container):
    declared = True
    value_template = "new Ext.TabPanel({ %s })"
    def __init__(self,layout,name,*elements,**options):
        Container.__init__(self,layout,name,*elements,**options)
        #~ self.layouts = layouts
        self.width = self.elements[0].ext_width() or 300
    

    def ext_options(self):
        d = dict(
          xtype="tabpanel",
          #region="east",
          split=True,
          activeTab=0,
          width=self.width,
          #items=js_code("[%s]" % ",".join([l.ext_name for l in self.layouts]))
          items=[js_code(e.as_ext()) for e in self.elements]
        )
        return d


class GridElement(Container):
    value_template = "new Ext.grid.EditorGridPanel({ %s })"
    declared = True
    ext_suffix = "_grid"

    def __init__(self,layout,name,report,*elements,**kw):
        """
        Note: layout is the owning layout. 
        In case of a slave grid, layout.report is the master.
        """
        if len(elements) == 0:
            elements = report.row_layout._main.elements
        Container.__init__(self,layout,name,*elements,**kw)
        #LayoutElement.__init__(self,layout,report.name)
        self.report = report
        #self.row_layout = row_layout
        #~ if store is None:
            #~ store = Store(layout,report)
        #self.store = report.row_layout.store
        self.column_model = ColumnModel(self)
        self.preferred_width = 80

      
    def ext_variables(self):
        setup_report(self.report)
        #yield self.report.row_layout.store
        #~ for rpt in self.report.choices_stores.values():
            #~ yield rpt.store
        for e in self.elements:
            for v in e.ext_variables():
                yield v
        yield self.column_model
        yield self
        
    def ext_options(self):
        setup_report(self.report)
        #print self.name, self.layout.detail_reports
        #rpt = self.slave
        #r = rpt.renderer(request)
        # print rpt
        d = LayoutElement.ext_options(self)
        #editing = self.report.can_change.passes(request)
        #if request._lino_request.editing:
        d.update(clicksToEdit=2)
            #~ d.update(xtype='editorgrid')
        #~ else:
            #~ d.update(xtype='grid')
        #d.update(store=self.store)
        #d.update(colModel=self.column_model)
        d.update(viewConfig=js_code(py2js(dict(
          #autoScroll=True,
          #autoFill=True,
          #forceFit=True,
          #enableRowBody=True,
          showPreview=True,
          scrollOffset=200,
          emptyText="Nix gefunden!"
        ))))
        #d.update(autoScroll=True)
        #d.update(fitToFrame=True)
        d.update(emptyText="Nix gefunden...")
        d.update(store=js_code(self.report.store.ext_name))
        d.update(colModel=js_code(self.column_model.ext_name))
        #d.update(autoHeight=True)
        #d.update(layout='fit')
        d.update(enableColLock=False)
        d.update(selModel=js_code("new Ext.grid.RowSelectionModel({singleSelect:false})"))
        
        #~ if len(keys):
            #~ d['keys'] = keys
        #~ d.update(tbar=js_code("""new Ext.PagingToolbar({
          #~ store: %s,
          #~ displayInfo: true,
          #~ pageSize: %d,
          #~ prependButtons: false,
          #~ items: %s
        #~ }) """ % (self.report.row_layout.store.ext_name,self.report.page_length,py2js(buttons))))
        tbar = dict(
          store=self.report.store,
          displayInfo=True,
          pageSize=self.report.page_length,
          prependButtons=False,
        )
        d.update(tbar=js_code("new Ext.PagingToolbar(%s)" % py2js(tbar)))
        #~ d.update(tbar=js_code("""new Ext.PagingToolbar({
          #~ store: %s,
          #~ displayInfo: true,
          #~ pageSize: %d,
          #~ prependButtons: false,
        #~ }) """ % (self.report.row_layout.store.ext_name,self.report.page_length)))
        return d
            
    #~ def value2js(self,obj):
        #~ return "1"
        
      
      
    def ext_lines_after(self):
      
        keys = []
        buttons = []
        for a in self.report._actions:
            h = js_code("grid_action(%s,'%s','%s')" % (
                  self.ext_name, a.name, self.report.store.get_absolute_url(action=a.name)))
            buttons.append(dict(text=a.label,handler=h))
            if a.key:
                #keys.append(dict(handler=js_code("%s_action" % a.name),key=a.key))
                keys.append(dict(
                  handler=h,
                  #handler=js_code("%s_action" % a.name),
                  key=a.key.keycode,ctrl=a.key.ctrl,alt=a.key.alt,shift=a.key.shift))
        # Ctrl+ENTER in a grid opens all detail windows
        #~ key = reports.RETURN(ctrl=True)
        #~ keys.append(dict(
          #~ handler=js_code("%s_detail" % self.report.name),
          #~ key=key.keycode,ctrl=key.ctrl,alt=key.alt,shift=key.shift))

        key = reports.RETURN(ctrl=True)
        layout = self.report.layouts[2]
        keys.append(dict(
          handler=js_code("show_detail(%s,%s)" % (self.ext_name,layout.name)),
          key=key.keycode,ctrl=key.ctrl,alt=key.alt,shift=key.shift))

        for layout in self.report.layouts[2:]:
            buttons.append(dict(
              handler=js_code("show_detail(%s,%s)" % (self.ext_name,layout.name)),
              text=layout.label))
              
        for slave in self.report._slaves:
            buttons.append(dict(
              handler=js_code("function(btn,evt) {%s_%s1(btn,evt,undefined,%s)}" % (slave.app_label,slave.name,self.ext_name)),
              text = slave.label
            ))
            
        yield "%s.keys = %s;" % (self.ext_name,py2js(keys))
        yield "%s.getTopToolbar().addButton(%s);" % (self.ext_name,py2js(buttons))
        #~ for k in buttons:
            #~ yield "%s.getTopToolbar().addButton(%s);" % (self.ext_name,py2js(k))
            
        #~ d = {}
        #~ for e in self.report.row_layout.store.fields:
            #~ d[e.field.name] = js_code('oGrid_event.record.data.%s' % e.field.name)
        yield "%s.on('afteredit', grid_afteredit(%s,'%s','%s'));" % (
          self.ext_name,self.ext_name,
          self.report.store.get_absolute_url(grid_afteredit=True),
          self.report.store.pk.name)
          
            
      
        #~ s = """
#~ function %s_afteredit(oGrid_event){""" % self.ext_name
        #~ s += """
  #~ Ext.Ajax.request({
    #~ waitMsg: 'Please wait...',
    #~ url: '%s',""" % self.report.row_layout.store.get_absolute_url(save=True)
        #~ d = {}
        #~ for e in self.report.row_layout.store.fields:
            #~ d[e.field.name] = js_code('oGrid_event.record.data.%s' % e.field.name)
        #~ s += """
    #~ params: { %s }, """ % dict2js(d)
    
        #~ s += """
    #~ success: function(response){
      #~ // console.log('success',response.responseText);
      #~ var result=Ext.decode(response.responseText);
      #~ // console.log(result);
      #~ if (result.success) {
        #~ %s.commitChanges(); // get rid of the red triangles
        #~ %s.reload();        // reload our datastore.
      #~ } else {
        #~ Ext.MessageBox.alert(result.msg);
      #~ }
    #~ },
    #~ failure: function(response){
      #~ // console.log(response);
      #~ Ext.MessageBox.alert('error','could not connect to the database. retry later');		
    #~ }
  #~ });
#~ };""" % (self.report.row_layout.store.ext_name,self.report.row_layout.store.ext_name)
        #~ yield s
        #~ yield "%s.on('afteredit', %s_afteredit);" % (self.ext_name,self.ext_name)

              
            #~ s = """%s.getTopToolbar().addButton({""" % self.ext_name
            #~ s += "text:'%s', " % action.label
            #~ s += """ handler: %s_action}); """ % action.name
            #~ yield s
  
        
class M2mGridElement(GridElement):
    def __init__(self,layout,field,*elements,**kw):
        self.field = field
        from . import reports
        rpt = reports.get_model_report(field.rel.to)
        GridElement.__init__(self,layout,rpt.name,rpt,*elements,**kw)
  

  
class MainGridElement(GridElement):
    def __init__(self,layout,name,vertical,*elements,**kw):
        # ignore the "vertical" arg
        #layout.report.setup()
        GridElement.__init__(self,layout,name,layout.report,*elements,**kw)
        #print "MainGridElement.__init__()",self.ext_name
        
    def ext_options(self):
        d = GridElement.ext_options(self)
        # d = Layout.ext_options(self,request)
        # d = dict(title=request._lino_report.get_title()) 
        #d.update(title=request._lino_request.get_title()) 
        #d.update(title=self.layout.label)
        #d.update(title=self.report.get_title(None)) 
        #d.update(region='center',split=True)
        return d
        
    def ext_lines_after(self):
        for s in GridElement.ext_lines_after(self):
            yield s
        # rowselect is currently not used. maybe in the future.
        s = """
function %s_rowselect(grid, rowIndex, e) {""" % self.ext_name
        s += """
    var row = %s.getAt(rowIndex);""" % self.report.store.ext_name
        for layout in self.report.layouts[1:]:
            s += """
    %s.form.loadRecord(row);""" % layout._main.ext_name
            for slave in layout.slave_grids:
                setup_report(slave.report)
                s += """  
    %s.load({params: { master: row.id } });""" % slave.report.store.ext_name
    
        s += "\n};"
        #yield s
        #yield "%s.getSelectionModel().on('rowselect', %s_rowselect);" % (self.ext_name,self.ext_name)




class MainPanel(Panel):
    value_template = "new Ext.form.FormPanel({ %s })"
    def __init__(self,layout,name,vertical,*elements,**kw):
        self.report = layout.report
        Panel.__init__(self,layout,name,vertical,*elements,**kw)
        
        
    #~ def ext_variables(self):
        #~ yield self.layout.store
        #~ for v in Panel.ext_variables(self):
            #~ yield v
        
    def ext_options(self):
        d = Panel.ext_options(self)
        #d.update(title=self.layout.label)
        #d.update(region='east',split=True) #,width=300)
        d.update(autoScroll=True)
        if False:
            d.update(tbar=js_code("""new Ext.PagingToolbar({
              store: %s,
              displayInfo: true,
              pageSize: 1,
              prependButtons: true,
            }) """ % self.report.store.ext_name))
        #d.update(items=js_code(self._main.as_ext(request)))
        d.update(items=js_code("[%s]" % ",".join([e.as_ext() for e in self.elements])))
        d.update(autoHeight=False)
        return d
        
        
    def ext_lines_after(self):
        yield "%s_win.grid.getSelectionModel().addListener('rowselect'," % self.layout.report.row_layout.name
        yield "  function(sm,rowIndex,record) { "
        yield "    %s.form._lino_pk = record.data.id;" % self.ext_name
        yield "    %s.form.loadRecord(record);" % self.ext_name
        for slave in self.layout.slave_grids:
            yield "  %s.load({params: { master: record.data.%s } });" % (
                 slave.report.store.ext_name,
                 self.report.store.pk.name)
        yield "});"
        
        #~ yield "%s.addListener('load',function(store,rows,options) { " % self.report.store.ext_name
        #~ yield "  %s.form.loadRecord(rows[0]);" % self.ext_name
        #~ for slave in self.layout.slave_grids:
            #~ yield "  %s.load({params: { master: rows[0].data['%s'] } });" % (
                 #~ slave.report.store.ext_name,
                 #~ self.report.store.pk.name)
                 #~ #slave.store.name,request._lino_report.layout.pk.name)
        #~ yield "});"
        
        
      
        keys = []
        buttons = []

        key = reports.PAGE_UP
        js = js_code("function() {%s_win.grid.getSelectionModel().selectPrevious()}" % self.layout.report.row_layout.name)
        keys.append(dict(
          handler=js,
          key=key.keycode,ctrl=key.ctrl,alt=key.alt,shift=key.shift))
        buttons.append(dict(handler=js,text="Previous"))

        key = reports.PAGE_DOWN
        js = js_code("function() {%s_win.grid.getSelectionModel().selectNext()}" % self.layout.report.row_layout.name)
        keys.append(dict(
          handler=js,
          key=key.keycode,ctrl=key.ctrl,alt=key.alt,shift=key.shift))
        buttons.append(dict(handler=js,text="Next"))
        if len(keys):
            yield "%s.keys = %s;" % (self.ext_name,py2js(keys))
        
        
        url = self.report.store.get_absolute_url(submit=True)
        js = js_code("form_submit(%s.form,'%s',%s,'%s')" % (
                self.ext_name,url,self.report.store.ext_name,self.report.store.pk.name))
        buttons.append(dict(handler=js,text='Submit'))
        
        for btn in buttons:
            yield "%s.addButton(%s);" % (self.ext_name,py2js(btn))
    
        


_field2elem = (
    (models.TextField, TextFieldElement),
    (models.CharField, CharFieldElement),
    (models.DateField, DateFieldElement),
    (models.IntegerField, IntegerFieldElement),
    (models.DecimalField, DecimalFieldElement),
    (models.BooleanField, BooleanFieldElement),
    (models.ManyToManyField, M2mGridElement),
    (models.ForeignKey, ForeignKeyElement),
    (models.AutoField, IntegerFieldElement),
)
            
def field2elem(layout,field,**kw):
    for cl,x in _field2elem:
        if isinstance(field,cl):
            return x(layout,field,**kw)
    if True:
        raise NotImplementedError("field %s (%s)" %(field.name,field.__class__))
    print "[Warning] No LayoutElement for %s" % field.__class__
            



#~ class Window(VisibleComponent):
    #~ declared = True
    #~ ext_suffix = "_detail"
    #~ value_template = "new Ext.Window({ %s })"

    #~ def __init__(self,report,layouts,**kw):
        #~ print "Window.__init__()", report
        #~ VisibleComponent.__init__(self,report.name+"_win",**kw)
        #~ #self.layouts = layouts
        #~ #self.report = report
        #~ self.store = Store(report,layouts)

    #~ def ext_options(self):
        #~ d = VisibleComponent.ext_options(self)
        #~ tabs = [l._main for l in self.store.layouts]
        #~ d.update(items=TabPanel(None,"MainPanel",*tabs))
        #~ d.update(title=self.layout.label)
        #~ return d
        
    #~ def ext_lines(self):
        #~ yield ".show();"



class Viewport:
  
    def __init__(self,title,main_menu,*components):
        self.title = title
        self.main_menu = main_menu
        
        self.variables = []
        self.components = []
        #self.visibles = []
        for c in components:
            for v in c.ext_variables():
                self.variables.append(v)
            #~ if isinstance(c,VisibleComponent):
                #~ self.visibles.append(c)
            self.components.append(c)
            
        self.variables.sort(lambda a,b:cmp(a.declaration_order,b.declaration_order))
        
    #~ def add_component(self,c):
        #~ if c.declared:
            #~ l = self.variables.get(c.__class__,None)
            #~ if l is None:
                #~ l = []
                #~ self.variables[c.__class__] = l
            #~ l.append(c)
        #~ self.components.append(c)
        #~ if isinstance(c,VisibleComponent):
            #~ self.visibles.append(c)
        
        
    def render_to_html(self,request):
        s = """<html><head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title id="title">%s</title>""" % self.title
        s += """
<!-- ** CSS ** -->
<!-- base library -->
<link rel="stylesheet" type="text/css" href="%sresources/css/ext-all.css" />""" % settings.EXTJS_URL
        s += """
<!-- overrides to base library -->
<!-- ** Javascript ** -->
<!-- ExtJS library: base/adapter -->
<script type="text/javascript" src="%sadapter/ext/ext-base.js"></script>""" % settings.EXTJS_URL
        #widget_library = 'ext-all-debug'
        widget_library = 'ext-all'
        s += """
<!-- ExtJS library: all widgets -->
<script type="text/javascript" src="%s%s.js"></script>""" % (settings.EXTJS_URL,widget_library)
        s += """
<!-- overrides to library -->
<link rel="stylesheet" type="text/css" href="/media/lino.css">
<script type="text/javascript" src="/media/lino.js"></script>
<!-- page specific -->
<script type="text/javascript">

function on_store_exception(store,type,action,options,reponse,arg) {
  // console.log("Ha! on_store_exception() was called!");
  // console.log("params:",store,type,action,options,reponse,arg);
};

function form_submit(form,url,store,pkname) {
  return function(btn,evt) {
    // console.log(store);
    p = {};
    // p[pkname] = store.getAt(0).data.id;
    p[pkname] = form._lino_pk
    form.submit({
      url: url, 
      failure: function(form, action) {
        // console.log("form:",form);
        Ext.MessageBox.alert('Submit failed!', 
        action.result ? action.result.msg : '(undefined action result)');
      }, 
      params: p, 
      waitMsg: 'Saving Data...', 
      success: function (form, action) {
        Ext.MessageBox.alert('Saved OK',
          action.result ? action.result.msg : '(undefined action result)');
          store.reload();
      }
    })
  } 
}

function grid_afteredit(grid,url,pk) {
  return function(e) {
    /*
    e.grid - This grid
    e.record - The record being edited
    e.field - The field name being edited
    e.value - The value being set
    e.originalValue - The original value for the field, before the edit.
    e.row - The grid row index
    e.column - The grid column index
    
    Note: the line {{{p[e.field+'Hidden'] = e.value;}}} is there for ForeignKeyStoreField.
    
    */
    var p = e.record.data;
    // var p = {};
    p['colname'] = e.field;
    p[e.field] = e.value;
    // console.log(e);
    p[e.field+'Hidden'] = e.value;
    // p[pk] = e.record.data[pk];
    Ext.Ajax.request({
      waitMsg: 'Please wait...',
      url: url,
      params: p, 
      success: function(response) {
        // console.log('success',response.responseText);
        var result=Ext.decode(response.responseText);
        // console.log(result);
        if (result.success) {
          grid.getStore().commitChanges(); // get rid of the red triangles
          grid.getStore().reload();        // reload our datastore.
        } else {
          Ext.MessageBox.alert(result.msg);
        }
      },
      failure: function(response) {
        // console.log(response);
        Ext.MessageBox.alert('error','could not connect to the database. retry later');		
      }
    })
  }
}


function grid_action(grid,name,url) {
  // console.log("foo",grid,name,url);
  return function(oGrid_event) {
    // console.log("bar",oGrid_event);
    var sel_pks = '';
    var must_reload = false;
    var sels = grid.getSelectionModel().getSelections();
    // console.log(sels);
    for(var i=0;i<sels.length;i++) { sel_pks += sels[i].id + ','; };
    var doit = function(confirmed) {
      Ext.Ajax.request({
        waitMsg: 'Running action "' + name + '". Please wait...',
        url: url,
        params: { confirmed:confirmed,selected:sel_pks }, 
        success: function(response){
          // console.log('raw response:',response.responseText);
          var result = Ext.decode(response.responseText);
          // console.log('got response:',result);
          if(result.success) {
            if (result.msg) Ext.MessageBox.alert('success',result.msg);
            if (result.html) { new Ext.Window({html:result.html}).show(); };
            if (result.window) { new Ext.Window(result.window).show(); };
            if (result.redirect) { window.open(result.redirect); };
            if (result.must_reload) grid.getStore().load(); 
          } else {
            if(result.confirm) Ext.Msg.show({
              title: 'Confirmation',
              msg: result.confirm,
              buttons: Ext.Msg.YESNOCANCEL,
              fn: function(btn) {
                if (btn == 'yes') {
                    // console.log(btn);
                    doit(confirmed+1);
                }
              }
            })
          }
        },
        failure: function(response){
          // console.log(response);
          Ext.MessageBox.alert('error','Could not connect to the server.');
        }
      });
    };
    doit(0);
  };
}"""
        uri = request.build_absolute_uri()

        s += """
function goto_permalink() {
    var windows = "";
    var sep = '';
    Ext.WindowMgr.each(function(win){
      if(!win.hidden) {windows+=sep+win.getId();sep=","}
    });
    document.location = "%s?open=" + windows;
}""" % uri
        s += """

function show_detail(grid,fn) { 
  return function(btn,evt) {
    p = grid.getStore().baseParams;
    fn(btn,evt,p['master']);
  }
}


// Path to the blank image should point to a valid location on your server
Ext.BLANK_IMAGE_URL = '%sresources/images/default/s.gif';""" % settings.EXTJS_URL
        s += """
Ext.onReady(function(){ """
        
        #~ for mi in self.main_menu.get_items():
            #~ l = mi.parents()
            #~ l.reverse()
            #~ l.append(mi)
            #~ s += "\n\n// menu command [%s]" % " / ".join([i.label for i in l])
            #~ s += "\n" + py2js(mi.actor) + "\n"
            
        rpts = [ ReportRenderer(rptclass()) 
            for rptclass in reports.master_reports + reports.slave_reports]
        for rpt in rpts:
            for ln in rpt.ext_lines():
                s += "\n" + ln
                
        s += "\nvar main_menu = " + py2js(self.main_menu)
        
        s += define_vars(self.variables,indent=2)
                
        d = dict(layout='border')
        #d.update(autoScroll=True)
        d.update(items=js_code(
            "[main_menu,"+",".join([
                  c.as_ext() for c in self.components]) +"]"))
        s += "\nnew Ext.Viewport(%s).render('body');" % py2js(d)
 
        s += """
function gup( name )
{
  // Thanks to http://www.netlobo.com/url_query_string_javascript.html
  name = name.replace(/[\[]/,"\\\[").replace(/[\]]/,"\\\]");
  var regexS = "[\\?&]"+name+"=([^&#]*)";
  var regex = new RegExp( regexS );
  var results = regex.exec( window.location.href );
  if( results == null )
    return "";
  else
    return results[1];
}        
var windows = gup('open').split(',');
for(i=0;i<windows.length;i++) {
  console.log(windows[i]);
  if(windows[i]) eval(windows[i]+"()");
}
main_menu.get(0).focus();
        """
        s += "\n}); // end of onReady()"
        s += "\n</script></head><body></body></html>"
        return s
            
            

