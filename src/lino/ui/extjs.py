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
import types

from dateutil import parser as dateparser

from django.db import models
from django.conf import settings
from django.http import HttpResponse
from django.utils import simplejson

import lino
from lino import reports
from lino import layouts
from lino.utils import menus

UNDEFINED = "nix"

EXT_CHAR_WIDTH = 9
EXT_CHAR_HEIGHT = 12

def define_vars(variables,indent=0,prefix="var "):
    template = "var %s = %s;"
    sep = "\n" + ' ' * indent
    s = ''
    for v in variables:
        #lino.log.debug("define_vars() : %s", v.ext_name)
        for ln in v.ext_lines_before():
            s += sep + ln 
        s += sep + template % (v.ext_name,v.as_ext_value())
        for ln in v.ext_lines_after():
            s += sep + ln 
    return s


def dict2js(d):
    return ", ".join(["%s: %s" % (k,py2js(v)) for k,v in d.items()])
      
      
class ActionContext:
    def __init__(self,action,rptreq):
        self.request = rptreq.request
        selected = self.request.POST.get('selected',None)
        if selected:
            self.selected_rows = [
              action.report.model.objects.get(pk=pk) for pk in selected.split(',') if pk]
        else:
            self.selected_rows = []
        self.confirmed = self.request.POST.get('confirmed',None)
        if self.confirmed is not None:
            self.confirmed = int(self.confirmed)
        self.confirms = 0
        self._response = dict(success=True,must_reload=False,msg=None)
        #print 'ActionContext.__init__()', self.confirmed, self.selected_rows
        
    def refresh(self):
        self._response.update(must_reload=True)
        
    def redirect(self,url):
        self._response.update(redirect=url)
        
    def setmsg(self,msg=None):
        if msg is not None:
            self._reponse.update(msg=msg)
        
    def error(self,msg=None):
        self._response.update(success=False)
        self.setmsg(msg)
        raise ActionEvent() # MustConfirm(msg)
        
    def confirm(self,msg):
        #print "ActionContext.confirm()", msg
        self.confirms += 1
        if self.confirmed >= self.confirms:
            return
        self._response.update(confirm=msg,success=False)
        raise ActionEvent() # MustConfirm(msg)
        
      

class ReportRenderer:
    def __init__(self,report,**kw):
        assert isinstance(report,reports.Report)
        self.report = ui.get_report_handle(report)
        self.ext_name = report.app_label + "_" + report.name
        self.options = kw
        self.windows = [ WindowRenderer(l) for l in self.report.layouts[1:] ]
        
    #~ def ext_globals(self):
        #~ for win in self.windows:
            #~ yield "var %s_win;" % win.name
            #~ for ln in win.ext_lines():
                #~ yield ln
            #~ yield '// end of window %s' % win.name
            #~ yield ''
  
    def js_lines(self):
        if False:
            store = self.report.store
            for ln in store.js_lines():
                yield ln
            yield "%s.addListener({exception: function(a,b,c) { " % store.as_ext()
            yield "  // console.log(a,b,c);"
            yield "  Ext.MessageBox.alert('Exception in %s','no data');" % store.as_ext()
            yield "}});"
            yield ''
        for win in self.windows:
            yield '// window %s' % win.name
            for ln in win.js_lines():
                yield ln
            yield ''
        
        
        
class WindowRenderer:
    def __init__(self,layout,**kw):
        assert isinstance(layout,layouts.LayoutHandle)
        self.options = kw
        self.layout = layout
        self.store = layout.report.store
        #self.ext_name = report.app_label + "_" + report.name
        self.name = layout.name
        
    def js_lines(self):
        self.options.update(title=self.layout.get_title())
        self.options.update(closeAction='hide')
        self.options.update(maximizable=True)
        self.options.update(id=self.name)
        self.options.update(layout='fit')
        self.options.update(height=300,width=400)
        self.options.update(items=self.layout._main)
        #self.options.update(items=js_code("this.%s" % self.layout._main.ext_name))
        #kw.update(maximized=True)
        yield "var %s = new function() {" % self.name
        #yield "  this.name = '%s';" % self.name
        for ln in self.layout._main.js_lines():
            yield "  " + ln
        #~ for v in self.layout._main.ext_variables():
            #~ yield "  this.%s = %s;" % (v.ext_name,v.as_ext_value())
        #yield define_vars(self.layout._main.ext_variables(),indent=2,prefix="this.")
        yield "  this.comp = new Ext.Window( %s );" % py2js(self.options)
        yield "  this.show = function(btn,event,master,master_grid) {"
        #yield "    console.log('show',this);" 
        if self.layout.report._rd.master is None:
            yield "    %s.load();" % self.store.as_ext()
        else:
            yield "    if(master) {"
            yield "      %s.setBaseParam('master',master);" % self.store.as_ext()
            yield "      %s.load();" % self.store.as_ext()
            #yield "      this.store.load({master:master});" 
            yield "    } else {"
            #yield "      console.log('show() master_grid=',master_grid);"
            yield "      master_grid.comp.getSelectionModel().addListener('rowselect',function(sm,rowIndex,record) {"
            #yield "        console.log(rowIndex,record);" 
            yield "        %s.load({params:{master:record.id}});" % self.store.as_ext()
            yield "      });"
            yield "    }"
        yield "    this.comp.show();"
        yield "  };"
        
        yield "}();"
        
        #~ if self.layout.report.master is not None:
            #~ yield "function %s(btn,event,master,master_grid) { " % self.name
        #~ else:
            #~ yield "function %s(btn,event) { " % self.name
        #~ yield "  if(!%s_win){" % self.name
        #~ yield define_vars(self.layout._main.ext_variables(),indent=4)
        #~ yield "    %s_win = new Ext.Window( %s );" % (self.name,py2js(self.options))
        
        #~ if isinstance(self.layout._main,MainGridElement):
            #~ yield "%s_win.grid = %s;" % (self.name,self.layout._main.ext_name)
        
        #~ yield "  }"
        #~ if self.layout.report.master is None:
            #~ yield "  %s.load();" % self.layout.report.store.ext_name
        #~ else:
            #~ yield "  if(master) {"
            #~ yield "    %s.setBaseParam('master',master);" % self.layout.report.store.ext_name
            #~ yield "    %s.load();" % self.layout.report.store.ext_name
            #~ yield "  } else {"
            #~ yield "    master_grid.getSelectionModel().addListener('rowselect',function(sm,rowIndex,record) {"
            #~ yield "      // console.log(rowIndex,record);" 
            #~ yield "      %s.load({params:{master:record.id}});" % self.layout.report.store.ext_name
            #~ yield "    })"
            #~ yield "  }"
        #~ yield "  %s_win.show();" % self.name
        #~ yield "}\n"
      
#~ def get_report_windows(rpt,**kw):
    #~ setup_report(rpt)
    #~ for layout in rpt.layouts[1:]:
        #~ yield LayoutWindow(layout,**kw)
        
def menu_view(request):
    from lino import lino_site
    s = py2js(lino_site.get_menu())
    return HttpResponse(s, mimetype='text/html')


def py2js(v,**kw):
    #lino.log.debug("py2js(%r,%r)",v,kw)
        
    if isinstance(v,menus.Menu):
        if v.parent is None:
            kw.update(region='north',height=27,items=v.items)
            return py2js(kw)
        kw.update(text=v.label,menu=dict(items=v.items))
        return py2js(kw)
        
    if isinstance(v,menus.MenuItem):
        ext_name = v.actor.app_label + "_" + v.actor.name + "1" + ".show"
        if v.args:
            handler = "function(btn,evt) {%s(btn,evt,%s);}" % (
                ext_name,
                ",".join([py2js(a) for a in v.args]))
        else:
            handler = "function(btn,evt) {%s(btn,evt);}" % ext_name
            #handler = ext_name
        return py2js(dict(text=v.label,handler=js_code(handler)))
    if isinstance(v,Component):
        return v.as_ext(**kw)
        
    assert len(kw) == 0, "py2js() : value %r not allowed with keyword parameters" % v
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
        
        
        
        
        
        
#~ def setup_report(rpt):
    #~ "adds ExtJS specific stuff to a Report instance"
    #~ rpt.setup()
    #~ if False: # not hasattr(rpt,'choice_store'):
        #~ #rpt.choice_store = Store(rpt,rpt.choice_layout,mode='choice',autoLoad=True)
        #~ for layout in rpt.layouts:
            #~ if not hasattr(layout,'choice_store'):
                #~ layout.store = Store(rpt,layout) #,autoLoad=True
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
    rh = rpt.get_handle(ui)
    rptreq = ViewReportRequest(request,rh)
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
    


DECLARE_INLINE = 0
DECLARE_VAR = 1
DECLARE_THIS = 2

class Component: # better name? JSObject? Scriptable?
    #declared = False
    declare_type = DECLARE_INLINE
    ext_suffix = ''
    value_template = "{ %s }"
    #declaration_order = 9
    has_comp = False
    
    def __init__(self,name,**options):
        self.name = name
        self.options = options
        self.ext_name = name + self.ext_suffix
        
    #~ def ext_lines_after(self):
        #~ return []
    #~ def ext_lines_before(self):
        #~ return []
        
    def js_lines(self):
        if self.declare_type == DECLARE_INLINE:
            pass
        elif self.declare_type == DECLARE_VAR:
            yield "var %s = %s;" % (self.ext_name,self.as_ext_value())
        elif self.declare_type == DECLARE_THIS:
            yield "this.%s = %s;" % (self.ext_name,self.as_ext_value())
            
    def ext_options(self,**kw):
        kw.update(self.options)
        return kw
        
    def as_ext_value(self):
        options = self.ext_options()
        return self.value_template % dict2js(options)
        
    def as_ext(self):
        if self.declare_type == DECLARE_INLINE:
            return self.as_ext_value()
        if self.declare_type == DECLARE_THIS:
            name = "this." + self.ext_name
        else:
            name = self.ext_name
        if self.has_comp:
            return name + ".comp"
        else:
            return name


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
    declare_type = DECLARE_VAR
    ext_suffix = "_store"
    value_template = "new Ext.data.JsonStore({ %s })"
    
    def __init__(self,report,**options):
        assert isinstance(report,reports.ReportHandle)
        Component.__init__(self,report._rd.app_label+"_"+report._rd.name,**options)
        self.report = report
        
        fields = set()
        for layout in report.layouts:
            for fld in layout._store_fields:
                assert fld is not None, "%s"
                fields.add(fld)
        self.pk = self.report._rd.model._meta.pk
        assert self.pk is not None, "Cannot make Store for %s because %s has no pk" % (
          self.report._rd.name,self.report._rd.model)
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
            return DateStoreField(fld,self.report._rd.date_format)
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
        #d.update(listeners=dict(exception=js_code("Lino.on_store_exception")))
        return d
        
        

class ColumnModel(Component):
    declare_type = DECLARE_VAR
    ext_suffix = "_cols"
    value_template = "new Ext.grid.ColumnModel({ %s })"
    #declaration_order = 2
    
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
            assert isinstance(layout,layouts.LayoutHandle)
            #assert isinstance(layout,Layout), "%r is not a Layout" % layout
            #self.ext_name = layout.name + "_" + name + self.ext_suffix
            self.ext_name = name
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
        return py2js(self.get_column_options())
        #~ kw = self.get_column_options()
        #~ return "{ %s }" % dict2js(kw)
        
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
        
        
        


class FieldElement(LayoutElement):
    declare_type = DECLARE_THIS
    stored = True
    #declaration_order = 3
    name_suffix = "_field"
    xtype = None # set by subclasses
    
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
        rd = self.layout.report.get_field_choices(self.field)
        self.report = rd.get_handle(self.layout.ui)
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
            #setup_report(self.report)
            kw.update(store=self.report.store)
            #kw.update(store=js_code(self.store.as_ext_value(request)))
            kw.update(hiddenName=self.name+"Hidden")
            kw.update(valueField=self.report.store.pk.attname)
            #kw.update(valueField=self.name)
            """
            valueField: The underlying data value name to bind to this ComboBox (defaults to undefined if mode = 'remote' or 'field2' if transforming a select or if the field name is autogenerated based on the store configuration).

Note: use of a valueField requires the user to make a selection in order for a value to be mapped. See also hiddenName, hiddenValue, and displayField.
            """
            kw.update(displayField=self.report._rd.display_field)
            kw.update(typeAhead=True)
            #kw.update(lazyInit=False)
            kw.update(mode='remote')
            kw.update(selectOnFocus=True)
            #kw.update(pageSize=self.store.report.page_length)
            
        kw.update(triggerAction='all')
        kw.update(emptyText='Select a %s...' % self.report._rd.model.__name__)
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
        kw.update(format=self.layout.report._rd.date_format)
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
        kw.update(trueText=self.layout.report._rd.boolean_texts[0])
        kw.update(falseText=self.layout.report._rd.boolean_texts[1])
        kw.update(undefinedText=self.layout.report._rd.boolean_texts[2])
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
        assert isinstance(layout,layouts.LayoutHandle)
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
        delegate = layout.ui.field2elem(layout,field,**kw)
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
    
    declare_type = DECLARE_THIS
    
    # ExtJS options
    frame = True
    labelAlign = 'top'
    #labelAlign = 'left'
    
    
    def __init__(self,lui,name,*elements,**kw):
        LayoutElement.__init__(self,lui,name,**kw)
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
        #lino.log.debug("%s.%s %s : elements = %s",self.layout.name,self.__class__.__name__,self.name,self.elements)
                
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
        #d.update(items=js_code(py2js(self.elements)))
        d.update(items=js_code("[\n  %s\n]" % (", ".join(l))))
        #d.update(items=js_code("this.elements"))
        return d
        
    def js_lines(self):
        assert self.declare_type == DECLARE_THIS
        if self.has_comp:
            yield "this.%s = new function(parent) {" % self.ext_name
            #yield "  this._parent = parent;" 
            for e in self.elements:
                for ln in e.js_lines():
                    yield "  "+ln
            yield "  this.comp = %s;" % self.as_ext_value()
            yield "}(this);"
        else:
            for e in self.elements:
                for ln in e.js_lines():
                    yield ln
            yield "this.%s = %s;" % (self.ext_name,self.as_ext_value())
            
            


class Panel(Container):
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
    ext_suffix = "_grid"
    has_comp = True

    def __init__(self,lui,name,report,*elements,**kw):
        assert isinstance(report,reports.ReportHandle), "%r is not a ReportHandle!" % report
        """
        Note: lui is the owning layout ui. 
        In case of a slave grid, lui.layout.report is the master.
        """
        if len(elements) == 0:
            elements = report.row_layout._main.elements
        Container.__init__(self,lui,name,*elements,**kw)
        self.report = report
        self.column_model = ColumnModel(self)
        self.preferred_width = 80
        self.keys = None
        
    def setup(self):
        if self.keys:
            return
        #setup_report(self.report)
        keys = []
        buttons = []
        for a in self.report._rd._actions:
            h = js_code("Lino.grid_action(this,'%s','%s')" % (
                  a.name, 
                  self.report.store.get_absolute_url(action=a.name)))
            buttons.append(dict(text=a.label,handler=h))
            if a.key:
                keys.append(dict(
                  handler=h,
                  key=a.key.keycode,ctrl=a.key.ctrl,alt=a.key.alt,shift=a.key.shift))
        # the first detail window can be opend with Ctrl+ENTER 
        key = reports.RETURN(ctrl=True)
        layout = self.report.layouts[2]
        keys.append(dict(
          handler=js_code("Lino.show_detail(this,%r)" % layout.name),
          key=key.keycode,ctrl=key.ctrl,alt=key.alt,shift=key.shift))

        for layout in self.report.layouts[2:]:
            buttons.append(dict(
              handler=js_code("Lino.show_detail(this,%r)" % layout.name),
              text=layout._ld.label))
              
        for sl in self.report._rd._slaves:
            slave = sl.get_handle(self.layout.ui)
            buttons.append(dict(
              handler=js_code("Lino.show_slave(this,%r)" % slave.row_layout.name),
              text = slave._rd.label,
            ))
            
        self.keys = keys
        self.buttons = buttons
        
        
    def js_lines(self):
        """
        a grid doesn't generate the declaration of its elements 
        because its column_model does this indirectly
        """
        self.setup()
        #~ for ln in Container.js_lines(self):
            #~ yield ln
        yield "this.%s = new function() {" % self.ext_name
        #yield "this.cols = %s;" % self.column_model.as_ext_value()
        for ln in self.column_model.js_lines():
            yield "  " + ln
        yield "  var buttons = %s;" % py2js(self.buttons)
        yield "  var keys = %s;" % py2js(self.keys)
        yield "  this.comp = %s;" % self.as_ext_value()
        yield "  this.comp.on('afteredit', Lino.grid_afteredit(this,'%s','%s'));" % (
          self.report.store.get_absolute_url(grid_afteredit=True),
          self.report.store.pk.name)
        yield "}();"
        #yield "%s.keys = %s;" % (self.ext_name,py2js(self.keys))
        #yield "%s.getTopToolbar().addButton(%s);" % (self.ext_name,py2js(self.buttons))
          

    def ext_options(self):
        self.setup()
        d = LayoutElement.ext_options(self)
        d.update(clicksToEdit=2)
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
        d.update(colModel=self.column_model)
        #d.update(colModel=js_code('this.cols'))
        #d.update(colModel=js_code(self.column_model.ext_name))
        #d.update(autoHeight=True)
        #d.update(layout='fit')
        d.update(enableColLock=False)
        d.update(selModel=js_code("new Ext.grid.RowSelectionModel({singleSelect:false})"))
        
        tbar = dict(
          store=self.report.store,
          displayInfo=True,
          pageSize=self.report._rd.page_length,
          prependButtons=False,
          items=js_code('buttons'),
        )
        d.update(tbar=js_code("new Ext.PagingToolbar(%s)" % py2js(tbar)))
        return d
            
      
    #~ def ext_lines_after(self):
        #~ self.setup()
          
      
        
class M2mGridElement(GridElement):
    def __init__(self,lui,field,*elements,**kw):
        self.field = field
        rpt = reports.get_model_report(field.rel.to)
        rh = rpt.get_handle(lui.ui)
        GridElement.__init__(self,lui,rpt.name,rh,*elements,**kw)
  

  
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
        
    def unused_js_lines(self):
        # rowselect is currently not used. maybe in the future.
        for ln in GridElement.js_lines(self):
            yield ln
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
    def __init__(self,lui,name,vertical,*elements,**kw):
        self.report = lui.report
        Panel.__init__(self,lui,name,vertical,*elements,**kw)
        
        
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
        
        
    def js_lines(self):
        for ln in Panel.js_lines(self):
            yield ln
        yield "%s.main.comp.getSelectionModel().addListener('rowselect'," % self.layout.report.row_layout.name
        yield "  function(sm,rowIndex,record) { "
        #yield "    console.log(this);"
        name = self.layout.name
        yield "    %s.main.form._lino_pk = record.data.id;" % name
        yield "    %s.main.form.loadRecord(record);" % name
        for slave in self.layout.slave_grids:
            yield "  %s.load({params: { master: record.data.%s } });" % (
                 slave.report.store.as_ext(),
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
        js = js_code("function() {%s.main.comp.getSelectionModel().selectPrevious()}" % self.layout.report.row_layout.name)
        keys.append(dict(
          handler=js,
          key=key.keycode,ctrl=key.ctrl,alt=key.alt,shift=key.shift))
        buttons.append(dict(handler=js,text="Previous"))

        key = reports.PAGE_DOWN
        js = js_code("function() {%s.main.comp.getSelectionModel().selectNext()}" % self.layout.report.row_layout.name)
        keys.append(dict(
          handler=js,
          key=key.keycode,ctrl=key.ctrl,alt=key.alt,shift=key.shift))
        buttons.append(dict(handler=js,text="Next"))
        if len(keys):
            #yield "console.log(%s);" % self.as_ext()
            #yield "console.log(%s.comp);" % self.as_ext()
            yield "%s.keys = %s;" % (self.as_ext(),py2js(keys))
        
        
        url = self.report.store.get_absolute_url(submit=True)
        js = js_code("Lino.form_submit(%s.form,'%s',%s,'%s')" % (
                self.as_ext(),url,self.report.store.as_ext(),self.report.store.pk.name))
        buttons.append(dict(handler=js,text='Submit'))
        
        for btn in buttons:
            yield "%s.addButton(%s);" % (self.as_ext(),py2js(btn))
    
        




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
        
        #self.variables = []
        self.components = components
        #self.visibles = []
        #~ for c in components:
            #~ for v in c.ext_variables():
                #~ self.variables.append(v)
            #~ self.components.append(c)
            
        #~ self.variables.sort(lambda a,b:cmp(a.declaration_order,b.declaration_order))
        
        
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
        if False:
            s += """
<!-- overrides to library -->
<link rel="stylesheet" type="text/css" href="/media/lino.css">
<script type="text/javascript" src="/media/lino.js"></script>"""
        s += """
<!-- page specific -->
<script type="text/javascript">
Ext.namespace('Lino');
// Lino.on_store_exception = function (store,type,action,options,reponse,arg) {
  // console.log("Ha! on_store_exception() was called!");
  // console.log("params:",store,type,action,options,reponse,arg);
// };

Lino.form_submit = function (form,url,store,pkname) {
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
};

Lino.show_slave = function(master_win,slave_name) {
  return function(btn,evt) {
    slave_win = eval(slave_name);
    slave_win.show(btn,evt,undefined,master_win);
  }
}
                      


Lino.grid_afteredit = function (gridwin,url,pk) {
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
          gridwin.comp.getStore().commitChanges(); // get rid of the red triangles
          gridwin.comp.getStore().reload();        // reload our datastore.
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
};


Lino.grid_action = function(gridwin,name,url) {
  // console.log("grid_action.this=",this);
  // console.log("grid_action.gridwin=",gridwin);
  // console.log("foo",grid,name,url);
  return function(event) {
    // 'this' is the button who called this handler
    // console.log("grid_action.this = ",this);
    // console.log("grid_action.event = ",event);
    var sel_pks = '';
    var must_reload = false;
    var sels = gridwin.comp.getSelectionModel().getSelections();
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
            if (result.must_reload) gridwin.comp.getStore().load(); 
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
};"""
        uri = request.build_absolute_uri()

        s += """
Lino.gup = function( name )
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
};
Lino.goto_permalink = function () {
    var windows = "";
    var sep = '';
    Ext.WindowMgr.each(function(win){
      if(!win.hidden) {windows+=sep+win.getId();sep=","}
    });
    document.location = "%s?open=" + windows;
};""" % uri

        s += """
Lino.show_detail = function (grid,wrappername) { 
  return function(btn,evt) {
    p = grid.comp.getStore().baseParams;
    w = eval(wrappername);
    w.show(btn,evt,p['master']);
  }
};

Lino.main_menu = {};

// Path to the blank image should point to a valid location on your server
Ext.BLANK_IMAGE_URL = '%sresources/images/default/s.gif';""" % settings.EXTJS_URL

        rpts = [ ReportRenderer(rptclass()) 
            for rptclass in reports.master_reports + reports.slave_reports]
              
        #~ for rpt in rpts:
            #~ for ln in rpt.ext_globals():
                #~ s += "\n" + ln
                
        for rpt in rpts:
            for ln in rpt.report.store.js_lines():
                s += "\n" + ln
                
                
        for rpt in rpts:
            for ln in rpt.js_lines():
                s += "\n" + ln
                
        
        s += """
Lino.on_load_menu = function(response) {
  // console.log('success',response.responseText);
  var p = Ext.decode(response.responseText);
  Lino.main_menu = new Ext.Toolbar(p);"""
        d = dict(layout='border')
        #d.update(autoScroll=True)
        d.update(items=js_code(
            "[Lino.main_menu,"+",".join([
                  c.as_ext() for c in self.components]) +"]"))
        s += """
  new Ext.Viewport(%s).render('body');""" % py2js(d)
        s += """
  Lino.main_menu.get(0).focus();"""
        s += """
};"""
    

        s += """
Ext.onReady(function(){ """

        for c in self.components:
            for ln in c.js_lines():
                s += "\n" + ln
            
        #~ s += define_vars(self.variables,indent=2)
    
        s += """
Ext.Ajax.request({
  waitMsg: 'Loading main menu...',
  url: '/menu',
  success: Lino.on_load_menu,
  failure: function(response) {
    // console.log(response);
    Ext.MessageBox.alert('error','could not connect to the LinoSite.');
  }
});"""
        
        s += """
var windows = Lino.gup('open').split(',');
for(i=0;i<windows.length;i++) {
  // console.log(windows[i]);
  if(windows[i]) eval(windows[i]+"()");
}
        """
        s += "\n}); // end of onReady()"
        s += "\n</script></head><body></body></html>"
        return s
            
            



class ViewReportRequest(reports.ReportRequest):
  
    editing = 0
    selector = None
    sort_column = None
    sort_direction = None
    
    def __init__(self,request,report,*args,**kw):
      
        self.params = report._rd.param_form(request.GET)
        if self.params.is_valid():
            kw.update(self.params.cleaned_data)
        if report._rd.master is not None:
            pk = request.GET.get('master',None)
            if pk == UNDEFINED:
                pk = None
            if pk is None:
                kw.update(master_instance=None)
            else:
                try:
                    kw.update(master_instance=report._rd.master.objects.get(pk=pk))
                except report._rd.master.DoesNotExist,e:
                    print "[Warning] There's no %s with %s=%r" % (
                      report._rd.master.__name__,report._rd.master._meta.pk.name,pk)
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
        #~ mode = request.GET.get('mode',None)
        #~ if mode:
            #~ kw.update(mode=mode)

        #print "ViewReportRequest.__init__() 1",report.name
        self.request = request
        
        reports.ReportRequest.__init__(self,report,*args,**kw)
        self.store = self.report.store
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
        #if self.layout.index != 0:
        #    kw.update(layout=self.layout.index)
        #~ if self.mode is not None:
            #~ kw.update(mode=self.mode)
        return self.report.get_absolute_url(**kw)

    #~ def unused_render_to_html(self):
        #~ if len(self.store.layouts) == 2:
            #~ comps = [l._main for l in self.store.layouts]
        #~ else:
            #~ tabs = [l._main for l in self.store.layouts[1:]]
            #~ comps = [self.store.layouts[0]._main,extjs.TabPanel(None,"EastPanel",*tabs)]
        #~ return lino_site.ext_view(self.request,*comps)
        #return self.report.viewport.render_to_html(self.request)


    def obj2json(self,obj):
        d = {}
        for fld in self.store.fields:
            fld.write_to_form(obj,d)
            #d[e.name] = e.value2js(obj)
        return d
            
    def render_to_json(self):
        rows = [ self.obj2json(row) for row in self.queryset ]
        total_count = self.total_count
        # add one empty row:
        for i in range(0,self.extra):
        #if self.layout.index == 1: # currently only in a grid
            row = self.report._rd.create_instance(self)
            rows.append(self.obj2json(row))
            #~ d = {}
            #~ for fld in self.store.fields:
                #~ d[fld.field.name] = None
            #~ # d[self.store.pk.name] = UNDEFINED
            #~ rows.append(d)
            total_count += 1
        return dict(count=total_count,rows=rows)
        

        
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



from django.conf.urls.defaults import patterns, url, include


class ExtUI(reports.UI):
    _response = None
    
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
                
    def __init__(self):
        #self.StaticText = StaticText
        self.GridElement = GridElement
        self.MethodElement = MethodElement
        self.Panel = Panel
        self.Store = Store
        
    def field2elem(self,lui,field,**kw):
        for cl,x in self._field2elem:
            if isinstance(field,cl):
                return x(lui,field,**kw)
        if True:
            raise NotImplementedError("field %s (%s)" % (field.name,field.__class__))
        lino.log.warning("No LayoutElement for %s",field.__class__)
                

    def main_panel_class(self,layout):
        if isinstance(layout,layouts.RowLayout) : 
            return MainGridElement    
        if isinstance(layout,layouts.PageLayout) : 
            return MainPanel
        raise Exception("No element class for layout %r" % layout)
            

    
    def index(self, request):
        if self._response is None:
            from lino.lino_site import lino_site
            from django.http import HttpResponse
            lino.log.debug("building extjs._response...")
            comp = VisibleComponent("index",
                xtype="panel",
                html=lino_site.index_html.encode('ascii','xmlcharrefreplace'),
                autoScroll=True,
                #width=50000,
                #height=50000,
                region="center")
            viewport = Viewport(lino_site.title,lino_site.get_menu(),comp)
            s = viewport.render_to_html(request)
            self._response = HttpResponse(s)
        #s = layouts.ext_viewport(request,self.title,self._menu,*components)
        #windows = request.GET.get('open',None)
        #print "absolute_uri",request.build_absolute_uri()
        return self._response
    #index = never_cache(index)

  
    def get_urls(self):
        return patterns('',
            #(r'^o/(?P<db_table>\w+)/(?P<pk>\w+)$', view_instance),
            #(r'^r/(?P<app_label>\w+)/(?P<rptname>\w+)$', reports.view_report_as_ext),
            #(r'^json/(?P<app_label>\w+)/(?P<rptname>\w+)$', extjs.view_report_as_json),
            (r'^$', self.index),
            (r'^menu$', menu_view),
            (r'^list/(?P<app_label>\w+)/(?P<rptname>\w+)$', list_report_view),
            (r'^action/(?P<app_label>\w+)/(?P<rptname>\w+)/(?P<action>\w+)$', json_report_view),
            (r'^submit/(?P<app_label>\w+)/(?P<rptname>\w+)$', form_submit_view),
            (r'^grid_afteredit/(?P<app_label>\w+)/(?P<rptname>\w+)$', grid_afteredit_view),
            
        )

    def get_report_url(self,report,master_instance=None,
            simple_list=False,submit=False,grid_afteredit=False,action=None,**kw):
        if simple_list:
            url = "/list/"
        elif grid_afteredit:
            url = "/grid_afteredit/"
        elif submit:
            url = "/submit/"
        elif action:
            url = "/action/"
        else:
            raise "one of json, save or action must be True"
            #url = "/r/"
        url += report._rd.app_label + "/" + report._rd.name
        if action:
            url += "/" + action
        #~ app_label = report.__class__.__module__.split('.')[-2]
        #~ if mode == 'choices':
            #~ url = '/choices/%s/%s' % (app_label,report.model.__name__)
        #~ else:
            #~ url = '/%s/%s/%s' % (mode,app_label,report.__class__.__name__)
        #~ if master_instance is None:
            #~ master_instance = report.master_instance
        if master_instance is not None:
            kw['master'] = master_instance.pk
        #~ if mode is not None:
            #~ kw['mode'] = mode
        if len(kw):
            url += "?"+urlencode(kw)
        return url
            
    
ui = ExtUI()