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
import traceback
import types
import cPickle as pickle
import cgi
from lino.utils import ucsv
from urllib import urlencode

from dateutil import parser as dateparser

from django.db import models
from django.conf import settings
from django.http import HttpResponse
from django.utils import simplejson
from django.core.serializers.json import DjangoJSONEncoder
#from django.utils import html
from django.utils.translation import ugettext as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.core import exceptions

import lino
from lino import reports
from lino import actions
from lino import layouts, forms
from lino.utils import menus, actors
from lino.utils import constrain

UNDEFINED = "nix"

EXT_CHAR_WIDTH = 9
EXT_CHAR_HEIGHT = 22

URL_PARAM_MASTER_TYPE = 'mt'
URL_PARAM_MASTER_PK = 'mk'
# URL_PARAM_MASTER_GRID = 'mg'
URL_PARAM_FILTER = 'query'
URL_PARAM_CHOICES_PK = "ck"

CHOICES_TEXT_FIELD = 'text'
CHOICES_VALUE_FIELD = 'value'
CHOICES_HIDDEN_SUFFIX = "Hidden"

def build_url(*args,**kw):
    url = "/".join(args)  
    if len(kw):
        url += "?" + urlencode(kw)
    return url
        

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

def authenticated_user(user):
    if user.is_anonymous():
        return None
    return user
        
      
class ActionContext(actions.ActionContext):
    def __init__(self,request,*args,**kw):
        actions.ActionContext.__init__(self,ui,*args,**kw)
        self.request = request
        self.confirmed = self.request.POST.get('confirmed',None)
        if self.confirmed is not None:
            self.confirmed = int(self.confirmed)
        self.confirms = 0
        #print 'ActionContext.__init__()', self.confirmed, self.selected_rows
        
    def get_user(self):
        return authenticated_user(self.request.user)
        
    def get_report_request(self):
        raise NotImplementedError()
        
class GridActionContext(ActionContext):
    def __init__(self,request,*args,**kw):
        ActionContext.__init__(self,request,*args,**kw)
        assert isinstance(self.actor,reports.Report)
        selected = self.request.POST.get('selected',None)
        if selected:
            self.selected_rows = [
              self.actor.model.objects.get(pk=pk) for pk in selected.split(',') if pk]
        else:
            self.selected_rows = []
        
    def get_report_request(self):
        rh = self.actor.get_handle(self.ui)
        return ViewReportRequest(self.request,rh)
        
      

def id2js(s):
    return s.replace('.','_')
  
class js_code:
    "A string that py2js will represent as is, not between quotes."
    def __init__(self,s):
        self.s = s
    #~ def __repr__(self):
        #~ return self.s
  
def py2js(v,**kw):
    # lino.log.debug("py2js(%r,%r)",v,kw)
        
    if isinstance(v,menus.Menu):
        if v.parent is None:
            return py2js(v.items)
            #kw.update(region='north',height=27,items=v.items)
            #return py2js(kw)
        kw.update(text=v.label,menu=dict(items=v.items))
        return py2js(kw)
        
    if isinstance(v,menus.MenuItem):
        handler = "function(btn,evt){Lino.do_action(undefined,%r,%r,{})}" % (v.actor.get_url(ui),id2js(v.actor.actor_id))
        return py2js(dict(text=v.label,handler=js_code(handler)))
        #~ if v.args:
            #~ handler = "function(btn,evt) {%s.show(btn,evt,%s);}" % (
                #~ id2js(v.actor.actor_id),
                #~ ",".join([py2js(a) for a in v.args]))
        #~ else:
            #~ handler = "function(btn,evt) {%s.show(btn,evt);}" % id2js(v.actor.actor_id)
        #~ return py2js(dict(text=v.label,handler=js_code(handler)))
    if isinstance(v,Variable):
        return v.as_ext(**kw)
        
    assert len(kw) == 0, "py2js() : value %r not allowed with keyword parameters" % v
    if type(v) is types.GeneratorType:
        return "\n".join([ln for ln in v])
    if callable(v):
        raise Exception("Please call the function yourself")
        return "\n".join([ln for ln in v(**kw)])

    if isinstance(v,js_code):
        return v.s
    if v is None:
        return 'null'
    if isinstance(v,(list,tuple)): # (types.ListType, types.TupleType):
        return "[ %s ]" % ", ".join([py2js(x) for x in v])
    if isinstance(v,dict): # ) is types.DictType:
        return "{ %s }" % ", ".join([
            "%s: %s" % (k,py2js(v)) for k,v in v.items()])
    if isinstance(v,bool): # types.BooleanType:
        return str(v).lower()
    if isinstance(v, (int, long)):
        return str(v)
    if isinstance(v, float):
        return repr(v)
    #return simplejson.encoder.encode_basestring(v)
    #print repr(v)
    return simplejson.dumps(v,cls=DjangoJSONEncoder) # http://code.djangoproject.com/ticket/3324
            


DECLARE_INLINE = 0
DECLARE_VAR = 1
DECLARE_THIS = 2

class Variable(object):
    declare_type = DECLARE_THIS
    #declare_type = DECLARE_INLINE
    ext_suffix = ''
    value_template = "%s"
    
    def __init__(self,name,value):
        self.name = name
        self.value = value
        self.ext_name = id2js(name) + self.ext_suffix
        
    def js_declare(self):
        for v in self.subvars():
            for ln in v.js_declare():
                yield ln
        value = self.as_ext_value()
        if self.declare_type == DECLARE_INLINE:
            pass
        elif self.declare_type == DECLARE_VAR:
            yield "var %s = %s;" % (self.ext_name,value)
        elif self.declare_type == DECLARE_THIS:
            yield "this.%s = %s;" % (self.ext_name,value)
            
    def js_run(self,rr):
        for v in self.subvars():
            for ln in v.js_run(rr):
                yield ln
                
    def subvars(self):
        return []
            
    def as_ext(self):
        if self.declare_type == DECLARE_INLINE:
            return self.as_ext_value()
        if self.declare_type == DECLARE_THIS:
            return "this." + self.ext_name
        return self.ext_name

    def as_ext_value(self):
        return self.value_template % py2js(self.value)
        
class Component(Variable): # better name? JSObject? Scriptable?
    
    def __init__(self,name,**options):
        Variable.__init__(self,name,options)
        
    def as_ext_value(self):
        value = self.ext_options()
        return self.value_template % py2js(value)
        
    def ext_options(self,**kw):
        kw.update(self.value)
        return kw
        

class StoreField(object):

    def __init__(self,field,**options):
        self.field = field
        options['name'] = field.name
        self.options = options
        
    def as_js(self):
        return py2js(self.options)
        
    def obj2json(self,obj,d):
        #d[self.field.name] = getattr(obj,self.field.name)
        #v = getattr(obj,self.field.name)
        #d[self.field.name] = self.field.value_to_string(obj)
        d[self.field.name] = self.field.value_from_object(obj)
        
    def get_from_form(self,instance,post_data):
        v = post_data.get(self.field.name)
        #~ if v == '' and self.field.null:
            #~ v = None
        if v == '':
            v = self.field.get_default()
        try:
            instance[self.field.name] = self.field.to_python(v)
        except exceptions.ValidationError,e:
            lino.log.exception("%s = %r : %s",self.field.name,v,e)
            raise 
        #setattr(instance,self.field.name,v)
        
        
class BooleanStoreField(StoreField):
    def __init__(self,field,**kw):
        kw['type'] = 'boolean'
        StoreField.__init__(self,field,**kw)
    def get_from_form(self,instance,post_data):
        v = post_data.get(self.field.name)
        if v == 'true':
            v = True
        else:
            v = False
        instance[self.field.name] = v

class DateStoreField(StoreField):
  
    def __init__(self,field,date_format,**kw):
        self.date_format = date_format
        kw['type'] = 'date'
        StoreField.__init__(self,field,**kw)
        
    def obj2json(self,obj,d):
        value = getattr(obj,self.field.name)
        if value is not None:
            value = value.ctime() # strftime('%Y-%m-%d')
            #print value
            d[self.field.name] = value
            
    def get_from_form(self,instance,post_data):
        v = post_data.get(self.field.name)
        if v == '' and self.field.null:
            v = None
        if v is not None:
            #print v
            v = dateparser.parse(v,fuzzy=True)
        instance[self.field.name] = v

class unused_IntegerStoreField(StoreField):
  
    def __init__(self,field,**kw):
        kw['type'] = 'int'
        StoreField.__init__(self,field,**kw)
        
    def get_from_form(self,instance,post_data):
        v = post_data.get(self.field.name)
        if v == '':
            v = None
            #~ if self.field.default is models.NOT_PROVIDED:
                #~ v = None
            #~ else:
                #~ v = self.field.default
        else:
            v = int(v)
        instance[self.field.name] = v

class MethodStoreField(StoreField):
  
    def obj2json(self,obj,d):
        meth = getattr(obj,self.field.name)
        #lino.log.debug('MethodStoreField.obj2json() %s',self.field.name)
        d[self.field.name] = meth()
        
    def get_from_form(self,instance,post_data):
        pass
        #raise Exception("Cannot update a virtual field")


class OneToOneStoreField(StoreField):
        
    def get_from_form(self,instance,post_data):
        #v = values.get(self.field.name,None)
        v = post_data.get(self.field.name)
        if v == '' and self.field.null:
            v = None
        if v is not None:
            v = self.field.rel.to.objects.get(pk=v)
        instance[self.field.name] = v
        
    def obj2json(self,obj,d):
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
        s += "," + repr(self.field.name+CHOICES_HIDDEN_SUFFIX)
        return s 
        
    def get_from_form(self,instance,post_data):
        #v = post_data.get(self.name,None)
        #v = post_data.get(self.field.name+"Hidden",None)
        v = post_data.get(self.field.name+CHOICES_HIDDEN_SUFFIX)
        #print self.field.name,"=","%s.objects.get(pk=%r)" % (self.model.__name__,v)
        #v = post_data.getlist(self.field.name)
        #print "%s=%r" % (self.field.name, v)
        if v == '': # and self.field.null:
            v = None
        if v is not None:
            try:
                v = self.field.rel.to.objects.get(pk=v)
            except self.field.rel.to.DoesNotExist,e:
                #print "[get_from_form]", v, values.get(self.field.name)
                # lino.log.debug("[%r,%r] : %s",v,text,e)
                v = None
        instance[self.field.name] = v


    def obj2json(self,obj,d):
        try:
            v = getattr(obj,self.field.name)
        except self.field.rel.to.DoesNotExist,e:
            v = None
        if v is None:
            d[self.field.name+CHOICES_HIDDEN_SUFFIX] = None
            d[self.field.name] = None
        else:
            d[self.field.name+CHOICES_HIDDEN_SUFFIX] = v.pk
            d[self.field.name] = unicode(v)
        



class Store(Component):
    declare_type = DECLARE_THIS
    #declare_type = DECLARE_VAR
    #declare_type = DECLARE_INLINE
    ext_suffix = "_store"
    value_template = "new Ext.data.JsonStore(%s)"
    
    def __init__(self,rh,**options):
        assert isinstance(rh,reports.ReportHandle)
        Component.__init__(self,id2js(rh.report.actor_id),**options)
        self.rh = rh
        self.report = rh.report
        fields = set()
        for layout in rh.layouts:
            for fld in layout._store_fields:
                assert fld is not None
                fields.add(fld)
        self.pk = self.report.model._meta.pk
        assert self.pk is not None, "Cannot make Store for %s because %s has no pk" % (
          self.report.actor_id,self.report.model)
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
            return StoreField(fld,type='int')
            #~ return IntegerStoreField(fld)
        if isinstance(fld,models.AutoField):
            return StoreField(fld,type='int')
            #~ return IntegerStoreField(fld)
        if isinstance(fld,models.BooleanField):
            return BooleanStoreField(fld)
        return StoreField(fld)
        #~ else:
            #~ kw['type'] = DATATYPES.get(fld.__class__,'auto')
            #~ kw['dateFormat'] = 'Y-m-d'
            #~ kw['name'] = fld.name
            #~ yield kw

      
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
        proxy = dict(url=self.rh.get_absolute_url(),method='GET')
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
        d.update(listeners=dict(exception=js_code("Lino.on_store_exception")))
        return d
        
    def get_from_form(self,post_values):
        instance = {}
        for f in self.fields:
            if not f.field.primary_key:
                f.get_from_form(instance,post_values)
        return instance
                    
        

class ColumnModel(Component):
    declare_type = DECLARE_THIS
    #declare_type = DECLARE_VAR
    #declare_type = DECLARE_INLINE
    ext_suffix = "_cols"
    value_template = "new Ext.grid.ColumnModel(%s)"
    #declaration_order = 2
    
    def __init__(self,grid):
        self.grid = grid
        Component.__init__(self,grid.name)
        self.columns = [GridColumn(e) for e in self.grid.elements]
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
        
    def subvars(self):
        for col in self.columns:
            yield col.editor
            yield col
        
        
    def ext_options(self):
        #self.report.setup()
        d = Component.ext_options(self)
        #d.update(columns=[e.get_column_options() for e in self.grid.elements])
        d.update(columns=self.columns)
        #d.update(defaultSortable=True)
        return d
        
class GridColumn(Component):
    declare_type = DECLARE_VAR
    ext_suffix = "_col"
    value_template = "new Ext.grid.Column(%s)"
    
    def __init__(self,editor,**kw):
        Component.__init__(self,editor.name,**kw)
        self.editor = editor
        self.value_template = editor.grid_column_template
    
        #~ if self.editable:
            #~ editor = self.get_field_options()
        
    def ext_options(self,**kw):
        kw = Component.ext_options(self,**kw)
        kw.update(self.editor.get_column_options())
        kw.update(editor=self.editor)
        return kw
        
class VisibleComponent(Component):
    width = None
    height = None
    preferred_width = 10
    preferred_height = 1
    flex = None
    
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
        yield self
        
    def debug_lines(self):
        sep = ","
        cols = "name label __class__ labelAlign vertical width preferred_width height preferred_height flex".split()
        yield sep.join(cols) 
        for e in self.walk():
            yield sep.join([str(getattr(e,n,"N/A")) for n in cols])
            
        
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
    xtype = None # set by subclasses
    grid_column_template = "new Ext.grid.Column(%s)"
    
    def __init__(self,lh,name,**kw):
        #lino.log.debug("LayoutElement.__init__(%r,%r)", lh.layout,name)
        #self.parent = parent
        VisibleComponent.__init__(self,name,**kw)
        self.lh = lh
        if lh is not None:
            assert isinstance(lh,layouts.LayoutHandle)
            #assert isinstance(layout,Layout), "%r is not a Layout" % layout
            #self.ext_name = layout.name + "_" + name + self.ext_suffix
            #self.ext_name = name
            #~ if self.declared:
                #~ self.layout.report.add_variable(self)
                

        
    def get_property(self,name):
        v = getattr(self,name,None)
        if self.parent is None or v is not None:
            return v
        return self.parent.get_property(name)
        
        
    def get_column_options(self,**kw):
        kw.update(
          dataIndex=self.name, 
          editable=self.editable,
          header=unicode(self.label) if self.label else self.name,
          sortable=self.sortable
          )
        w = self.width or self.preferred_width
        kw.update(width=w*EXT_CHAR_WIDTH)
        return kw    
        
    #~ def as_ext_column(self):
        #~ return py2js(self.get_column_options())
        
    def set_parent(self,parent):
        assert self.parent is None
        self.parent = parent
        if self.label:
            if parent.labelAlign == layouts.LABEL_ALIGN_TOP:
                self.preferred_height += 1
            elif parent.labelAlign == layouts.LABEL_ALIGN_LEFT:
                self.preferred_width += len(self.label)
        if parent.vertical:
            self.flex = self.height or self.preferred_height
        else:
            self.flex = self.width or self.preferred_width

    def ext_options(self,**kw):
        kw = VisibleComponent.ext_options(self,**kw)
        if self.flex is not None:
            kw.update(flex=self.flex)
        #~ if self.width is None:
            #~ """
            #~ an element without explicit width will get flex=1 when in a hbox, otherwise anchor="100%".
            #~ """
            #~ if self.parent is not None:
                #~ if self.parent.vertical:
                    #~ kw.update(anchor="100%")
                #~ else:
                    #~ kw.update(flex=1)
            #~ else:
                #~ lino.log.warning("%s %s : parent is None",self.__class__.__name__,self.ext_name)
        #~ else:
            #~ kw.update(width=self.ext_width())
        #~ if self.height is not None:
            #~ kw.update(height=self.height * EXT_CHAR_HEIGHT)
        if self.xtype is not None:
            kw.update(xtype=self.xtype)
        return kw
        
    def js_column_lines(self,grid):
        return []
        
    #~ def ext_width(self):
        #~ if self.width is None:
            #~ return None
        #~ #if self.parent.labelAlign == 'top':
        #~ return max(self.width,self.label_width) * EXT_CHAR_WIDTH + self.xpadding
        
class InputElement(LayoutElement):
    #declare_type = DECLARE_INLINE
    declare_type = DECLARE_THIS
    #declare_type = DECLARE_VAR
    ext_suffix = "_input"
    xtype = 'textfield'
    preferred_height = 1
    field = None 
    
    def __init__(self,lh,input,**kw):
        #lino.log.debug("InputElement.__init__(%r,%r)",lh,input)
        LayoutElement.__init__(self,lh,input.name,**kw)
        assert isinstance(lh.layout,layouts.FormLayout), "%s is not a FormLayout" % lh.name
        self.input = input
        
    def ext_options(self,**kw):
        kw = LayoutElement.ext_options(self,**kw)
        kw.update(self.input.options)
        kw.update(name=self.name)
        kw.update(id=self.name)
        #kw.update(xtype='textfield')
        panel_options = dict(xtype='container',layout='form',items=kw)
        panel_options.update(maxHeight=self.preferred_height*EXT_CHAR_HEIGHT)
        return panel_options
        
class ButtonElement(LayoutElement):
    #declare_type = DECLARE_INLINE
    #declare_type = DECLARE_THIS
    declare_type = DECLARE_VAR
    ext_suffix = "_btn"
    xtype = 'button'
    preferred_height = 1

    def __init__(self,lh,name,action,**kw):
        #lino.log.debug("ButtonElement.__init__(%r,%r,%r)",lh,name,action)
        LayoutElement.__init__(self,lh,name,**kw)
        assert isinstance(lh.layout,layouts.Layout), "%s is not a Layout" % lh.name
        self.action = action
        
    def ext_options(self,**kw):
        #kw = super(StaticTextElement,self).ext_options(**kw)
        kw = LayoutElement.ext_options(self,**kw)
        #kw.update(xtype=self.xtype)
        label = self.action.label or self.name
        kw.update(text=label)
        kw.update(maxHeight=self.preferred_height*EXT_CHAR_HEIGHT)
        kw.update(maxWidth=len(label)*EXT_CHAR_WIDTH)
        kw.update(id=self.name)
        if self.lh.default_button == self:
            kw.update(plugins='defaultButton')
        kw.update(handler=js_code('Lino.form_action(this,%r,%s,%r)' % (
          self.name,py2js(self.action.needs_validation),self.lh.ui.get_button_url(self))))
        return kw


class StaticTextElement(LayoutElement):
    #declare_type = DECLARE_INLINE
    #declare_type = DECLARE_THIS
    declare_type = DECLARE_VAR
    xtype = 'label'
    
    def __init__(self,lh,name,text,**kw):
        LayoutElement.__init__(self,lh,name,**kw)
        self.text = text

    def ext_options(self,**kw):
        #kw = super(StaticTextElement,self).ext_options(**kw)
        kw = LayoutElement.ext_options(self,**kw)
        #kw.update(xtype=self.xtype)
        kw.update(html=self.text.text)
        return kw
        
class Spacer(LayoutElement):
    declare_type = DECLARE_INLINE
    #xtype = 'label'
    value_template = "new Ext.Spacer(%s)"
    
        
class VirtualFieldElement(LayoutElement):
    def __init__(self,lh,name,gfk,**kw):
        assert isinstance(gfk,generic.GenericForeignKey)
        self.gfk = gfk
        LayoutElement.__init__(self,lh,name,label=name,**kw)
        #print "20091210", name,gfk
        
    def ext_options(self,**kw):
        kw = LayoutElement.ext_options(self,**kw)
        kw.update(maxHeight=self.preferred_height*EXT_CHAR_HEIGHT)
    
        
        
class FieldElement(LayoutElement):
    #declare_type = DECLARE_INLINE
    #declare_type = DECLARE_THIS
    declare_type = DECLARE_VAR
    stored = True
    #declaration_order = 3
    ext_suffix = "_field"
    
    def __init__(self,lh,field,**kw):
        assert field.name, Exception("field %r has no name!" % field)
        LayoutElement.__init__(self,lh,field.name,label=field.verbose_name,**kw)
        self.field = field
        self.editable = field.editable and not field.primary_key
        
    #~ def get_column_options(self,**kw):
        #~ kw = LayoutElement.get_column_options(self,**kw)
        #~ if self.editable:
            #~ fo = self.get_field_options()
            #~ kw.update(editor=fo)
        #~ return kw    
        
    def get_field_options(self,**kw):
        if self.xtype:
            kw.update(xtype=self.xtype)
        kw.update(name=self.name)
        kw.update(anchor="100%")
        #kw.update(style=dict(padding='0px'),color='green')
        if self.label:
            kw.update(fieldLabel=unicode(self.label))
        if not self.field.blank:
            kw.update(allowBlank=False)
        if not self.editable:
            kw.update(readOnly=True)
        #kw.update(maxHeight=self.preferred_height*EXT_CHAR_HEIGHT)
        return kw
        
    def ext_options(self,**kw):
        """
        ExtJS renders fieldLabels only if the field's Container has layout 'form', so we create a panel around each field
        """
        kw = LayoutElement.ext_options(self,**kw)
        kw.update(self.get_field_options())
        h = self.preferred_height*EXT_CHAR_HEIGHT
        kw.update(minHeight=h)
        kw.update(height=h)
        #kw.update(flex=0)
        #kw.update(xtype='panel',layout='form') 
        #kw.update(style=dict(padding='0px'),color='green')
        #kw.update(hideBorders=True)
        #kw.update(margins='0')
        return kw
        #~ kw.update(xtype='container',layout='form')
        #~ kw.update(items=self.get_field_options())
        #~ return kw
    
        
        
class TextFieldElement(FieldElement):
    xtype = 'textarea'
    #width = 60
    preferred_width = 60
    preferred_height = 3

class CharFieldElement(FieldElement):
    xtype = "textfield"
    sortable = True
  
    def __init__(self,*args,**kw):
        FieldElement.__init__(self,*args,**kw)
        self.preferred_width = min(20,self.field.max_length)
        #~ if self.width is None and self.field.max_length < 10:
            #~ # "small" texfields should not be expanded, so they get an explicit width
            #~ self.width = self.field.max_length
            
    def get_field_options(self,**kw):
        kw = FieldElement.get_field_options(self,**kw)
        kw.update(maxLength=self.field.max_length)
        return kw

        
class ForeignKeyElement(FieldElement):
    #xtype = "combo"
    sortable = True
    #width = 20
    value_template = "new Ext.form.ComboBox(%s)"
    
    def __init__(self,*args,**kw):
        FieldElement.__init__(self,*args,**kw)
        #self.report = self.lh.link.report.get_field_choices(self.field)
        self.report = reports.get_model_report(self.field.rel.to)
        #self.report = rd.get_handle(self.lh.ui)
        #self.rh = self.report.get_handle(self.lh.ui)
        #self.lh.needs_store(self.rh)
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
        
    def unused_get_column_options(self,**kw):
        kw = FieldElement.get_column_options(self,**kw)
        #kw.update(dataIndex=self.name+CHOICES_HIDDEN_SUFFIX)
        #js = "function(v, meta, rec, row, col, store) {return rec.data.%s}" % (self.name+CHOICES_HIDDEN_SUFFIX)
        # js = "function(v, meta, rec, row, col, store) {return v.text}" 
        #js = "function(v, meta, rec, row, col, store) {return v[1]}" 
        #kw.update(renderer=js_code('Lino.ForeignKeyRenderer(%r)' % (self.name+"Hidden") ))
        #kw.update(renderer=js_code(js))
        return kw    
        
    def store_options(self,**kw):
        proxy = dict(url=ui.get_choices_url(self),method='GET')
        kw.update(proxy=js_code(
          "new Ext.data.HttpProxy(%s)" % py2js(proxy)
        ))
        # a JsonStore without explicit proxy sometimes used method POST
        # d.update(url=self.rr.get_absolute_url(json=True))
        # d.update(method='GET')
        # kw.update(autoLoad=True)
        kw.update(totalProperty='count')
        kw.update(root='rows')
        kw.update(id=CHOICES_VALUE_FIELD) # self.report.model._meta.pk.name)
        kw.update(fields=[CHOICES_VALUE_FIELD,CHOICES_TEXT_FIELD])
        #~ kw.update(listeners=dict(exception=js_code("Lino.on_store_exception")))
        listeners = dict(exception=js_code("Lino.on_store_exception"))
        kw.update(listeners=listeners)
        return kw
      
        
    def get_field_options(self,**kw):
        # see blog 20100222
        kw = FieldElement.get_field_options(self,**kw)
        kw.update(mode='remote')
        #setup_report(self.report)
        #kw.update(store=self.rh.store)
        sto = self.store_options()
        #print repr(sto)
        kw.update(store=js_code("new Ext.data.JsonStore(%s)" % py2js(sto)))
        #kw.update(store=js_code(self.store.as_ext_value(request)))
        kw.update(hiddenName=self.name+CHOICES_HIDDEN_SUFFIX)
        kw.update(valueField=CHOICES_VALUE_FIELD) #self.report.model._meta.pk.name)
        #kw.update(valueField='id')
        #kw.update(valueField=self.name)
        kw.update(triggerAction='all')
        #kw.update(listeners=dict(beforequery=js_code("function(qe) {console.log('beforequery',qe); return true;}")))
        
        kw.update(submitValue=True)
        kw.update(displayField=CHOICES_TEXT_FIELD) # self.report.display_field)
        kw.update(typeAhead=True)
        kw.update(minChars=2) # default 4 is to much
        kw.update(queryDelay=300) # default 500 is maybe slow
        kw.update(queryParam=URL_PARAM_FILTER)
        kw.update(typeAhead=True)
        #kw.update(typeAheadDelay=300) # default 500 is maybe slow
        kw.update(selectOnFocus=True) # select any existing text in the field immediately on focus.
        kw.update(resizable=True)
        kw.update(pageSize=self.report.page_length)
        kw.update(emptyText='Select a %s...' % self.report.model.__name__)
        # test whether field has a %s_choices() method
        if self.lh.link.report.get_field_choices_meth(self.field): 
            kw.update(contextParam=URL_PARAM_CHOICES_PK)
            #kw.update(lazyInit=True)
        return kw
        
    def js_column_lines(self,grid):
        yield "%s.add_row_listener(function(sm,rowIndex,record) {" % grid
        #yield "  console.log('20100124b',this,client_job);"
        yield "  %s.setQueryContext(record.data.id)});" % self.as_ext()
        #yield "client_job.add_row_listener(function(sm,rowIndex,record) {console.log('20100124b',this)},this);"
        

        
            
class DateFieldElement(FieldElement):
    xtype = 'datefield'
    data_type = 'date' # for store column
    sortable = True
    preferred_width = 8 
    # todo: DateFieldElement.preferred_width should be computed from Report.date_format
    grid_column_template = "new Ext.grid.DateColumn(%s)"
    
    def get_column_options(self,**kw):
        kw = FieldElement.get_column_options(self,**kw)
        #kw.update(xtype='datecolumn')
        kw.update(format=self.lh.link.report.date_format)
        return kw
    
class IntegerFieldElement(FieldElement):
    xtype = 'numberfield'
    sortable = True
    preferred_width = 5
    data_type = 'int' 

class DecimalFieldElement(FieldElement):
    xtype = 'numberfield'
    sortable = True
    data_type = 'float' 
    grid_column_template = "new Ext.grid.NumberColumn(%s)"
    
    def __init__(self,*args,**kw):
        FieldElement.__init__(self,*args,**kw)
        self.preferred_width = min(5,self.field.max_digits) \
                + self.field.decimal_places
                
    def get_column_options(self,**kw):
        kw = FieldElement.get_column_options(self,**kw)
        #kw.update(xtype='numbercolumn')
        kw.update(align='right')
        fmt = "0,000"
        if self.field.decimal_places > 0:
            fmt += "." + ("0" * self.field.decimal_places)
        kw.update(format=fmt)
        return kw
        
                

class BooleanFieldElement(FieldElement):
  
    xtype = 'checkbox'
    data_type = 'boolean' 
    grid_column_template = "new Ext.grid.BooleanColumn(%s)"
    #~ def __init__(self,*args,**kw):
        #~ FieldElement.__init__(self,*args,**kw)
        
    def get_column_options(self,**kw):
        kw = FieldElement.get_column_options(self,**kw)
        #kw.update(xtype='booleancolumn')
        kw.update(trueText=self.lh.link.report.boolean_texts[0])
        kw.update(falseText=self.lh.link.report.boolean_texts[1])
        kw.update(undefinedText=self.lh.link.report.boolean_texts[2])
        return kw
        
    def get_from_form(self,instance,values):
        """
        standard HTML submits checkboxes of a form only when they are checked.
        So if the field is not contained in values, we take False as value.
        """
        instance[self.name] = values.get(self.name,False)



class MethodElement(FieldElement):
    stored = True
    editable = False

    def __init__(self,lh,name,meth,return_type,**kw):
        assert isinstance(lh,layouts.LayoutHandle)
        # uh, this is tricky...
        return_type.name = name
        return_type._return_type_for_method = meth
        FieldElement.__init__(self,lh,return_type)
        delegate = MainPanel.field2elem(lh,return_type,**kw)
        for a in ('ext_options','get_column_options','get_field_options','grid_column_template'):
            setattr(self,a,getattr(delegate,a))
        

class Container(LayoutElement):
    #ext_template = 'lino/includes/element.js'
    #ext_container = 'Ext.Panel'
    vertical = False
    hpad = 1
    is_fieldset = False
    
    #declare_type = DECLARE_INLINE
    #declare_type = DECLARE_THIS
    #declare_type = DECLARE_VAR
    declare_type = DECLARE_THIS
    
    
    def __init__(self,lh,name,*elements,**kw):
        self.has_frame = lh.layout.has_frame
        self.labelAlign = lh.layout.label_align
        self.elements = elements
        LayoutElement.__init__(self,lh,name,**kw)
        
    def subvars(self):
        return self.elements
            
    def walk(self):
        for e in self.elements:
            for el in e.walk():
              yield el
        yield self
        

    def pprint(self,level=0):
        margin = "  " * level
        s = margin + str(self) + ":\n"
        # self.__class__.__name__
        for e in self.elements:
            for ln in e.pprint(level+1).splitlines():
                s += ln + "\n"
        return s




class Panel(Container):
    ext_suffix = "_panel"
    
    def __init__(self,lh,name,vertical,*elements,**kw):
        self.vertical = vertical
        Container.__init__(self,lh,name,*elements,**kw)
        for e in elements:
            if not isinstance(e,LayoutElement):
                raise Exception("%r is not a LayoutElement" % e)
            e.set_parent(self)
            if isinstance(e,FieldElement):
                self.is_fieldset = True
                #~ if self.label_width < e.label_width:
                    #~ self.label_width = e.label_width
                if e.label:
                    w = len(e.label) + 1 # +1 for the ":"
                    if self.label_width < w:
                        self.label_width = w
            
        w = h = 0
        for e in elements:
            ew = e.width or e.preferred_width
            eh = e.height or e.preferred_height
            if self.vertical:
                h += e.flex
                w = max(w,ew)
            else:
                w += e.flex
                h = max(h,eh)
        self.preferred_height = h
        self.preferred_width = w
        
        
        
    def ext_options(self,**d):
        d = Container.ext_options(self,**d)
        #d.update(xtype='panel')
        d.update(xtype='container')
        d.update(pack='end')
        #d.update(margins='0')
        #d.update(style=dict(padding='0px'))
        
        d.update(items=self.elements)
        #l = [e.as_ext() for e in self.elements ]
        #d.update(items=js_code("[\n  %s\n]" % (", ".join(l))))
        #d.update(items=js_code("this.elements"))
        
        if len(self.elements) == 1:
            d.update(layout='fit')
        elif self.vertical:
            #align = 'left'
            align = 'stretch'
            #align = 'stretchmax'
            d.update(layout='vbox',layoutConfig=dict(align=align))
        else:
            #align = 'top'
            align = 'stretch'
            #align = 'stretchmax'
            d.update(layout='hbox',layoutConfig=dict(align=align))
            
        if self.is_fieldset:
            d.update(labelWidth=self.label_width * EXT_CHAR_WIDTH)
            
        if self.vertical:
            #d.update(frame=self.has_frame)
            d.update(frame=True)
            d.update(bodyBorder=False)
            d.update(border=False)
            d.update(labelAlign=self.labelAlign)
            #d.update(style=dict(padding='0px'),color='green')
        else:
            d.update(frame=False)
            #d.update(bodyBorder=False)
            d.update(border=False)
            
        return d
        

class TabPanel(Container):
    value_template = "new Ext.TabPanel(%s)"
    #~ def __init__(self,lh,name,*elements,**options):
        #~ Container.__init__(self,lh,name,*elements,**options)
        #~ self.width = self.elements[0].ext_width() or 300
    

    def ext_options(self):
        d = dict(
          xtype="tabpanel",
          #region="east",
          split=True,
          activeTab=0,
          width=300,
          #items=js_code("[%s]" % ",".join([l.ext_name for l in self.layouts]))
          items=self.elements
        )
        return d
        

#~ class DataElementMixin:
    #~ "common for Grids, Details and Forms"
  

class GridElement(Container): #,DataElementMixin):
    #value_template = "new Ext.grid.EditorGridPanel(%s)"
    value_template = "new Lino.GridPanel(%s)"
    ext_suffix = "_grid"
    
    def __init__(self,lh,name,rh,*elements,**kw):
        """
        Note: lh is the owning layout handle, rh is the report being managed by this Grid.
        """
        assert isinstance(rh,reports.ReportHandle), "%r is not a ReportHandle!" % rh
        if len(elements) == 0:
            elements = rh.row_layout._main.elements
        w = 0
        for e in elements:
            w += (e.width or e.preferred_width)
        self.preferred_width = constrain(w,10,120)
        
        Container.__init__(self,lh,name,*elements,**kw)
        #DataElementMixin.__init__(self,rh)
        #self.dl = rh
        
        # override Container's height algorithm
        self.preferred_height = rh.report.page_length 
        ADD_GRID_HEIGHT = 4 # experimental value...
        if self.height:
            self.height += ADD_GRID_HEIGHT
        else:
            self.preferred_height += ADD_GRID_HEIGHT
        
        self.rh = rh
        self.report = rh.report
        lh.needs_store(rh)
        self.column_model = ColumnModel(self)
        
          
    def subvars(self):
        """
        GridElement, unlike Container, doesn't generate the declaration of its elements 
        because self.column_model does this indirectly.
        """
        #self.setup()
        #yield self.rh.store
        yield self.column_model

    def ext_options(self):
        #~ self.setup()
        d = LayoutElement.ext_options(self)
        d.update(clicksToEdit=2)
        d.update(viewConfig=dict(
          #autoScroll=True,
          #autoFill=True,
          #forceFit=True,
          #enableRowBody=True,
          showPreview=True,
          scrollOffset=200,
          emptyText="Nix gefunden!"
        ))
        #d.update(autoScroll=True)
        #d.update(fitToFrame=True)
        d.update(emptyText="Nix gefunden...")
        d.update(store=self.rh.store) # js_code(self.rh.store.ext_name))
        d.update(colModel=self.column_model)
        d.update(title=self.rh.report.label)
        #d.update(colModel=js_code('this.cols'))
        #d.update(colModel=js_code(self.column_model.ext_name))
        #d.update(autoHeight=True)
        #d.update(layout='fit')
        d.update(enableColLock=False)
        return d
            
      
        
class M2mGridElement(GridElement):
    def __init__(self,lh,field,*elements,**kw):
        self.field = field
        rpt = reports.get_model_report(field.rel.to)
        rh = rpt.get_handle(lh.ui)
        GridElement.__init__(self,lh,id2js(rpt.actor_id),rh,*elements,**kw)
  

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
    (models.EmailField, CharFieldElement),
)
    
class MainPanel:
  
    def __init__(self):
    #~ def __init__(self,dl):
        #~ self.dl = dl # DataLink (i.e. a ReportHandle or a FormHandle)
        self.keys = None
        self.buttons = None
        self.cmenu = None
        
    def subvars(self):
        self.setup()
        for rh in self.lh._needed_stores:
            yield rh.store
        yield self.buttons
        yield self.keys
        yield self.cmenu
  
  
    def get_datalink(self):
        raise NotImplementedError
        
    def setup(self):
        if self.keys:
            return
        #setup_report(self.report)
        keys = []
        buttons = []
        dl = self.get_datalink()
        for a in dl.get_actions():
            h = js_code("Lino.grid_action(this,'%s','%s')" % (
                  a.name, 
                  dl.get_absolute_url(grid_action=a.name)))
            buttons.append(dict(text=a.label,handler=h))
            if a.key:
                keys.append(dict(
                  handler=h,
                  key=a.key.keycode,ctrl=a.key.ctrl,alt=a.key.alt,shift=a.key.shift))
                  
        details = dl.get_details()
        if len(details):
            # the first detail window can be opend with Ctrl+ENTER 
            key = actions.RETURN(ctrl=True)
            lh = details[0]
            keys.append(dict(
              handler=js_code("Lino.show_slave(this,%r,%s)" % (lh.get_absolute_url(run=True),py2js(lh.label))),
              key=key.keycode,ctrl=key.ctrl,alt=key.alt,shift=key.shift))

            for lh in details[1:]: # self.rh.layouts[2:]:
                buttons.append(dict(
              handler=js_code("Lino.show_slave(this,%r,%s)" % (lh.get_absolute_url(run=True),py2js(lh.label))),
                  text=lh.layout.label))
              
        slaves = dl.get_slaves()
        for rh in slaves:
            #rh = sl.get_handle(self.lh.ui)
            buttons.append(dict(
              handler=js_code("Lino.show_slave(this,%r,%s)" % (rh.row_layout.get_absolute_url(run=True),py2js(rh.report.label))),
              #handler=js_code("Lino.show_slave(this,%r)" % id2js(rh.row_layout.name)),
              text = rh.report.label,
            ))
            
        self.keys = Variable(self.ext_name+'_keys',keys)
        self.buttons = Variable(self.ext_name+'_buttons',buttons)
        self.cmenu = Variable('cmenu',js_code("new Ext.menu.Menu(%s)" % py2js(self.buttons)))
        
    def js_job_constructor(self,rr,**kw):
    
        yield "function(caller) {"
        yield "  var client_job = this;" 
        for ln in self.js_declare():
            yield "  " + ln
            
        yield "  this.window = new Ext.Window(%s);" % py2js(kw)
        # for permalink:
        yield "  this.window._permalink = %s;" % py2js(id2js(self.lh.name))
        #~ yield "  console.log(4);"
        yield "  this.stop = function() {"
        yield "     this.window.close();"
        yield "  }"
        yield "  if (caller) {"
        yield "    caller.window.on('close',function() {"
        #yield "      console.log('close',caller,this);"
        yield "      this.stop();"
        yield "    },this);"
        yield "  }"
        
            
        for ln in self.js_run(rr):
            yield "  " + ln
            
        for e in self.lh.walk():
            for ln in e.js_column_lines('this.main_grid'):
                yield ln
                
        yield "  this.window.show();"
        yield "  this.window.syncSize();"
        yield "  this.window.focus();"
        yield "}"
            
    @classmethod
    def field2elem(cls,lh,field,**kw):
        for cl,x in _field2elem:
            if isinstance(field,cl):
                return x(lh,field,**kw)
        lino.log.warning("No LayoutElement for %s",field.__class__)
        raise NotImplementedError("field %r" % field)


class WrappingMainPanel(MainPanel):
    "Inherited by DetailMainPanel and FormMainPanel (not GridPanel)"
    
    @classmethod
    def field2elem(cls,lh,field,**kw):
        e = MainPanel.field2elem(lh,field,**kw)
        ct = Container(lh,field.name+"_ct",e,items=e,xtype='container',layout='form')
        ct.field = field
        return ct

class GridMainPanel(GridElement,MainPanel):
    #declare_type = DECLARE_VAR
    def __init__(self,lh,name,vertical,*elements,**kw):
        'ignore the "vertical" arg'
        #lh.report.setup()
        self.pager = None
        MainPanel.__init__(self)
        GridElement.__init__(self,lh,name,lh.link,*elements,**kw)
        #~ if self.height is None:
            #~ self.height = self.preferred_height
        #~ if self.width is None:
            #~ self.width = self.preferred_width
        #lino.log.debug("GridMainPanel.__init__() %s",self.name)
        
    def subvars(self):
        for e in GridElement.subvars(self):
            yield e
        for e in MainPanel.subvars(self):
            yield e
        yield self.pager
        
    def get_datalink(self):
        return self.rh
        
    def ext_options(self,**kw):
        self.setup()
        kw = GridElement.ext_options(self,**kw)
        # d = Layout.ext_options(self,request)
        # d = dict(title=request._lino_report.get_title()) 
        #kw.update(title=request._lino_request.get_title()) 
        #kw.update(title=self.layout.label)
        #kw.update(title=self.report.get_title(None)) 
        #kw.update(region='center',split=True)
        del kw['title']
        kw.update(selModel=js_code("new Ext.grid.RowSelectionModel({singleSelect:false})"))
        kw.update(tbar=self.pager)
        kw.update(bbar=self.buttons)
        return kw
        
    #~ def js_declare(self):
        #~ for ln in GridElement.js_declare(self):
            #~ yield ln
            
        
    def js_declare(self):
        self.setup()
        for ln in Container.js_declare(self):
            yield ln
        yield "%s.on('afteredit', Lino.grid_afteredit(this,'%s','%s'));" % (
          self.as_ext(),
          self.rh.get_absolute_url(grid_afteredit=True),
          self.rh.store.pk.name)
        yield "%s.on('cellcontextmenu', Lino.cell_context_menu(this));" % self.as_ext()
        # recalculate page size when size changes
        yield "%s.on('resize', function() {" % self.as_ext()
        yield "    this.pager.pageSize = %s.calculatePageSize() || 10;" % self.as_ext()
        yield "    this.refresh();"
        yield "  }, this, {delay:500});"
        # first load with "offset" and "limit" params
        yield "%s.on('render', function() {" % self.as_ext()
        yield "  this.pager.pageSize = %s.calculatePageSize() || 10;" % self.as_ext()
        yield "  this.refresh();"
        #yield "  %s.load({params:{limit:this.pager.pageSize,start:this.pager.cursor}});" % self.rh.store.as_ext()
        yield "}, this, {delay:100});"
        
    def setup(self):
        if self.pager:
            return
        MainPanel.setup(self)
        # searchString thanks to http://www.extjs.com/forum/showthread.php?t=82838
        def js_keypress():
            yield "function(field, e) {"
            # searching starts when user presses ENTER.
            yield "  if(e.getKey() == e.RETURN) {"
            # yield "    console.log('keypress',field.getValue(),store)"
            #    // var searchString = Ext.getCmp('seachString').getValue();
            yield "    store.setBaseParam('%s',field.getValue());" % URL_PARAM_FILTER
            yield "    store.load({params: { start: 0, limit: this.pager.pageSize }});" 
            yield "  }"
            yield "}"
        search_field = dict(
            id = 'seachString',
            fieldLabel = 'Search',
            xtype = 'textfield',
            enableKeyEvents = True, # required if you need to detect key-presses
            #listeners = dict(keypress=dict(handler=keypress,scope=js_code('this')))
            listeners = dict(keypress=js_keypress(),scope=js_code('this'))
        )
        dl = self.get_datalink()
        buttons = [search_field]
        #export_csv = dict(xtype='exportbutton',store=self.dl.store) #,scope=js_code('this'))
        #export_csv = dict(text="CSV",handler=js_code("function(){console.log('not implemented')}"),scope=js_code('this'))
        export_csv = dict(text=_("Download"),handler=js_code(
          "function() {window.open(%r);}" % dl.get_absolute_url(csv=True)))
        buttons.append(export_csv)
        tbar = dict(
          store=self.rh.store,
          displayInfo=True,
          pageSize=self.report.page_length,
          prependButtons=True,
          items=buttons, 
        )
        self.pager = Variable('pager',js_code("new Ext.PagingToolbar(%s)" % py2js(tbar)))
        
    def js_run(self,rr):
        #yield "this.refresh = function() { this.%s.getStore().load()}" % self.ext_name
        yield "this.refresh = function() { "
        #yield "  this.pager.pageSize = %s.calculatePageSize() || 10;" % self.as_ext()
        yield "  %s.getStore().load({params:{limit:this.pager.pageSize,start:this.pager.cursor}});" % self.as_ext()
        yield "}"
        yield "this.get_current_record = function() { return this.main_grid.getSelectionModel().getSelected()};"
        yield "this.get_selected = function() {"
        yield "  var sel_pks = '';"
        yield "  var sels = this.main_grid.getSelectionModel().getSelections();"
        yield "  for(var i=0;i<sels.length;i++) { sel_pks += sels[i].id + ','; };"
        yield "  return sel_pks;"
        yield "}"
        
        yield "var grid = this.main_grid;"
        yield "var store = grid.getStore();"
        if self.lh.link.report.master is None:
            yield "  store.load();" 
        else:
            master_type = ContentType.objects.get_for_model(self.lh.link.report.model).pk
            yield "  if (caller) {"
            yield "    caller.main_grid.add_row_listener("
            yield "      function(sm,rowIndex,record) { "
            yield "        var p = { %s:record.id, %s:%r };" % (
              URL_PARAM_MASTER_PK,URL_PARAM_MASTER_TYPE,master_type)
            yield "        store.load({params:p});" 
            yield "    })"
            yield "  } else {"
            if rr.master_instance is None:
                mpk = None
            else:
                mpk = rr.master_instance.pk
            yield "    store.load({params:{ %s:%s, %s:%r }});" % (
              URL_PARAM_MASTER_PK,py2js(mpk),URL_PARAM_MASTER_TYPE,master_type)
            yield "  }"
          
            # der folgende fall ist noch nicht uebernommen:
            #~ yield "    if(master) {"
            #~ yield "      %s.setBaseParam(%r,master);" % (self.store.as_ext(),URL_PARAM_MASTER_PK)
            #~ yield "      %s.load();" % self.store.as_ext()
            
        #~ for col in self.column_model.columns:
            #~ for ln in col.editor.js_column_lines(self.as_ext()):
                #~ yield ln
        
        # the following doesn't work and i don't understand why
        #~ yield "  this.window.on('show',function() {"
        #~ yield "    grid.focus();"
        #~ yield "  });"
        #~ yield "  grid.on('viewready',function() {"
        #~ #yield "    console.log('on render');"
        #~ #yield "    grid.getView().focusRow(1);"
        #~ yield "    grid.getSelectionModel().selectFirstRow();"
        #~ #yield "    grid.getView().focusEl.focus();"
        #~ yield "  });"



class DetailMainPanel(Panel,WrappingMainPanel):
#~ class DetailMainPanel(DataElementMixin,Panel,WrappingMainPanel):
    declare_type = DECLARE_THIS
    value_template = "new Ext.form.FormPanel(%s)"
    def __init__(self,lh,name,vertical,*elements,**kw):
        self.rh = lh.link
        self.report = self.rh.report
        MainPanel.__init__(self)
        #~ DataElementMixin.__init__(self,lh.link)
        Panel.__init__(self,lh,name,vertical,*elements,**kw)
        #lh.needs_store(self.rh)
        
    def get_datalink(self):
        return self.rh
        
    #~ def subvars(self):
        #~ for e in DataElementMixin.subvars(self):
            #~ yield e
            
    def subvars(self):
        for e in MainPanel.subvars(self):
            yield e
        for e in Panel.subvars(self):
            yield e
            
    def ext_options(self):
        self.setup()
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
            }) """ % self.rh.store.ext_name))
        #d.update(items=js_code(self._main.as_ext(request)))
        #d.update(items=js_code("[%s]" % ",".join([e.as_ext() for e in self.elements])))
        d.update(items=self.elements)
        d.update(autoHeight=False)
        d.update(bbar=self.buttons)
        #d.update(standardSubmit=True)
        return d
        
    def js_declare(self):
        #yield "console.log(10);"
        yield "this.refresh = function() { if(caller) caller.refresh(); };"
        yield "this.get_current_record = function() { return this.current_record;};"
        yield "this.get_selected = function() {"
        yield "  return this.current_record.id;"
        yield "}"
        yield "if(caller) {"
        #yield "  this.add_row_listener = function(fn,scope){caller.add_row_listener(fn,scope)};"
        yield "  this.main_grid = caller.main_grid;"
        yield "}else{"
        #yield "  this.add_row_listener = function(fn,scope) {};"
        yield "  this.main_grid = undefined;"
        yield "}"
        for ln in Panel.js_declare(self):
            yield ln
        #yield "console.log(11);"
        #yield "mastergrid = Ext.getCmp()"
        #yield "var slaves = [ %s ];" % ','.join([slave.rh.store.as_ext() for slave in self.lh.slave_grids])
        yield "var load_record = this.load_record = function(record) {"
        #yield "function load_record (record) {"
        #yield "  console.log('DetailMainPanel-%s.load_record()',record);" % self.report
        #name = id2js(self.lh.name) + '.' + self.lh._main.ext_name
        #name = 'this.' + self.lh._main.ext_name
        #name = self.as_ext()
        #yield "  this.current_pk = record.data.id;" 
        yield "  this.current_record = record;" 
        yield "  %s.form.loadRecord(record);" % self.as_ext()
        yield "  var p = { %s: record.id }" % URL_PARAM_MASTER_PK
        #yield "  var p = { %s: record.data.%s }" % (URL_PARAM_MASTER_PK,self.rh.store.pk.name)
        mt = ContentType.objects.get_for_model(self.report.model).pk
        yield "  p[%r] = %r;" % (URL_PARAM_MASTER_TYPE,mt)
        for slave in self.lh.slave_grids:
            yield "  %s.load({params:p});" % slave.rh.store.as_ext()
        #yield "  for(i=0;i++;i<slaves.length) { console.log('load slave',slaves[i],p); slaves[i].load({params:p}) };"
        yield "};"
        yield "if(this.main_grid) {"
        yield "  this.main_grid.add_row_listener("
        yield "    function(sm,rowIndex,record) { this.load_record(record); },this);"
        
        
        #~ yield "%s.addListener('load',function(store,rows,options) { " % self.report.store.ext_name
        #~ yield "  %s.form.loadRecord(rows[0]);" % self.ext_name
        #~ for slave in self.lh.slave_grids:
            #~ yield "  %s.load({params: { master: rows[0].data['%s'] } });" % (
                 #~ slave.report.store.ext_name,
                 #~ self.report.store.pk.name)
                 #~ #slave.store.name,request._lino_report.lh.pk.name)
        #~ yield "});"
      
        keys = []
        buttons = []

        #main_name = id2js(self.lh.link.row_layout.name) + '.' + 'main_grid'
        key = actions.PAGE_UP
        js = js_code("function() {this.main_grid.getSelectionModel().selectPrevious()}")
        keys.append(dict(
          handler=js,
          scope=js_code('this'),
          key=key.keycode,ctrl=key.ctrl,alt=key.alt,shift=key.shift))
        buttons.append(dict(handler=js,scope=js_code('this'),text="Previous"))

        key = actions.PAGE_DOWN
        js = js_code("function() {this.main_grid.getSelectionModel().selectNext()}")
        keys.append(dict(
          handler=js,
          scope=js_code('this'),
          key=key.keycode,ctrl=key.ctrl,alt=key.alt,shift=key.shift))
        buttons.append(dict(handler=js,scope=js_code('this'),text="Next"))
        if len(keys):
            #yield "console.log(%s);" % self.as_ext()
            #yield "console.log(%s.comp);" % self.as_ext()
            yield "  %s.keys = %s;" % (self.as_ext(),py2js(keys))
        
        for btn in buttons:
            yield "  %s.addButton(%s);" % (self.as_ext(),py2js(btn))
    
        yield "}"
        
        # the following also if caller was false

        buttons = []

        url = self.rh.get_absolute_url(submit=True)
        js = js_code("Lino.form_submit(this,'%s',this.main_grid.getStore(),'%s')" % (
                url,self.rh.store.pk.name))
        buttons.append(dict(handler=js,text='Submit'))
        
        for btn in buttons:
            yield "%s.addButton(%s);" % (self.as_ext(),py2js(btn))
    
    def js_run(self,rr):
        yield "if(this.main_grid) {"
        yield "  var sels = this.main_grid.getSelectionModel().getSelections()"
        yield "  if(sels.length > 0) this.load_record(sels[0]);"
        yield "}"
        

class FormMainPanel(Panel,WrappingMainPanel):
    value_template = "new Ext.form.FormPanel(%s)"
    
    def __init__(self,lh,name,vertical,*elements,**kw):
        #DataElementMixin.__init__(self,lh.link)
        Panel.__init__(self,lh,name,vertical,*elements,**kw)
        MainPanel.__init__(self)

    def get_datalink(self):
        return self.lh.link
        
    def ext_options(self,**d):
        d = Panel.ext_options(self,**d)
        #d.update(title=self.lh.label)
        #d.update(region='east',split=True) #,width=300)
        d.update(autoScroll=True)
        #d.update(items=js_code("[%s]" % ",".join([e.as_ext() for e in self.elements])))
        d.update(items=self.elements)
        d.update(autoHeight=False)
        return d
        
    def subvars(self):
        for e in DataElementMixin.subvars(self):
            yield e
        for e in Panel.subvars(self):
            yield e
            

    def js_run(self,rr):
        yield "  this.get_values = function() {"
        yield "    var v = {};"
        for e in self.lh.link.inputs:
            yield "    v[%r] = this.main_panel.getForm().findField(%r).getValue();" % (e.name,e.name)
        yield "    return v;"
        yield "  };"


class Viewport:
  
    def __init__(self,title,*components):
        self.title = title
        #self.main_menu = main_menu
        
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
        widget_library = 'ext-all-debug'
        #widget_library = 'ext-all'
        s += """
<!-- ExtJS library: all widgets -->
<script type="text/javascript" src="%s%s.js"></script>""" % (settings.EXTJS_URL,widget_library)
        if True:
            s += """
<style type="text/css">
/* http://stackoverflow.com/questions/2106104/word-wrap-grid-cells-in-ext-js  */
.x-grid3-cell-inner, .x-grid3-hd-inner {
  white-space: normal; /* changed from nowrap */
}
</style>"""
        if True:
            s += """
<script type="text/javascript" src="%s/Exporter-all.js"></script>""" % settings.EXTJS_URL

        if False:
            s += """
<!-- overrides to library -->
<link rel="stylesheet" type="text/css" href="/media/lino.css">
<script type="text/javascript" src="/media/lino.js"></script>"""
        s += """
<!-- page specific -->
<script type="text/javascript">
Ext.namespace('Lino');
Lino.on_store_exception = function (store,type,action,options,reponse,arg) {
  // console.log("Ha! on_store_exception() was called!");
  console.log("on_store_exception:",store,type,action,options,reponse,arg);
};
Lino.save_window_config = function(caller,url) {
  return function(event,toolEl,panel,tc) {
    // console.log(panel.id,panel.getSize(),panel.getPosition());
    var pos = panel.getPosition();
    var size = panel.getSize();
    var w = size['width'] * 100 / Lino.viewport.getWidth();
    var h = size['height'] * 100 / Lino.viewport.getHeight();
    // Lino.do_action(url,'save_window_config',{h:Math.round(h),w:Math.round(w),max:panel.maximized});
    Lino.do_action(caller,url,'save_window_config',{
      x:pos[0],y:pos[1],h:size['height'],w:size['width'],
      max:panel.maximized});
  }
};

Lino.form_submit = function (job,url,store,pkname) {
  // console.log("Lino.form_submit:",job);
  return function(btn,evt) {
    p = {};
    // p[pkname] = store.getAt(0).data.id;
    // p[pkname] = job.current_pk;
    p[pkname] = job.get_current_record().id;
    // console.log('Lino.form_submit',p);
    job.main_panel.form.submit({
      clientValidation: false,
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


Lino.grid_afteredit = function (caller,url,pk) {
  return function(e) {
    /*
    e.grid - This grid
    e.record - The record being edited
    e.field - The field name being edited
    e.value - The value being set
    e.originalValue - The original value for the field, before the edit.
    e.row - The grid row index
    e.column - The grid column index
    */
    var p = e.record.data;
    // var p = {};
    p['grid_afteredit_colname'] = e.field;
    p[e.field] = e.value;
    // console.log(e);
    // add value used by ForeignKeyStoreField CHOICES_HIDDEN_SUFFIX
    p[e.field+'Hidden'] = e.value;
    // p[pk] = e.record.data[pk];
    // console.log("grid_afteredit:",e.field,'=',e.value);
    Ext.Ajax.request({
      waitMsg: 'Please wait...',
      url: url,
      params: p, 
      success: function(response) {
        // console.log('success',response.responseText);
        var result=Ext.decode(response.responseText);
        // console.log(result);
        if (result.success) {
          caller.main_grid.getStore().commitChanges(); // get rid of the red triangles
          caller.main_grid.getStore().reload();        // reload our datastore.
        } else {
          Ext.MessageBox.alert('Action failed',result.msg);
        }
      },
      failure: function(response) {
        // console.log(response);
        Ext.MessageBox.alert('Action failed','Lino server did not respond to Ajax request '+url);
      }
    })
  }
};

// Lino.jobs = Array();
// Lino.active_job = undefined;

Lino.do_action = function(caller,url,name,params) {
  // console.log('Lino.do_action()',name,params,reload);
  var doit = function(confirmed) {
    params['confirmed'] = confirmed;
    Ext.Ajax.request({
      waitMsg: 'Running action "' + name + '". Please wait...',
      url: url,
      params: params, 
      success: function(response){
        // console.log('raw response:',response.responseText);
        var result = Ext.decode(response.responseText);
        // console.log('got response:',result);
        if(result.success) {
          if (result.msg) Ext.MessageBox.alert('Success',result.msg);
          if (result.html) { new Ext.Window({html:result.html}).show(); };
          if (result.window) { new Ext.Window(result.window).show(); };
          if (result.call) {
            var job = new result.call(caller);
            // Lino.active_job = Lino.jobs.length;
            // Lino.jobs[Lino.jobs.length] = job;
            // job.run();
            // console.log(Lino.jobs);
          };
          if (result.redirect) { window.open(result.redirect); };
          if (result.must_reload && caller) caller.refresh();
          // Lino.last_result = result;
        } else {
          if (result.msg) Ext.MessageBox.alert('Action failed',result.msg);
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
        if (result.stop_caller && caller) caller.stop();
        if (result.refresh_menu) Lino.load_main_menu();
      },
      failure: function(response){
        // console.log(response);
        Ext.MessageBox.alert('Error','Lino.do_action() could not connect to the server.');
      }
    });
  };
  doit(0);
};

Lino.grid_action = function(caller,name,url) {
  // console.log("grid_action()",caller,name,url);
  return function(event) {
    Lino.do_action(caller,url,name,{selected:caller.get_selected()});
  };
};
Lino.show_slave = function (caller,url,name) { 
  // console.log('show_slave()',caller,url,name)
  return function(btn,evt) {
    // p = caller.main_grid.getStore().baseParams;
    // console.log('show_detail',name,url,p)
    // Lino.do_action(caller,url,name,p);
    Lino.do_action(caller,url,name,{});
  }
};
""" 

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
};"""
        #uri = request.build_absolute_uri()
        uri = request.path
        s += """
Lino.goto_permalink = function () {
    var windows = "";
    var sep = '';
    Ext.WindowMgr.each(function(win){
      if(!win.hidden) {windows+=sep+win._permalink;sep=","}
    });
    document.location = "%s?show=" + windows;
};""" % uri

        s += """
Lino.form_action = function (caller,name,needs_validation,url) { 
  return function(btn,evt) {
    // console.log('Lino.form_action()',caller,name,needs_validation);
    if (needs_validation && !caller.main_panel.form.isValid()) {
        Ext.MessageBox.alert('error',"One or more fields contain invalid data.");
        return;
    }
    Lino.do_action(caller,url,name,caller.get_values());
  }
};

Lino.main_menu = new Ext.Toolbar({});

// Path to the blank image should point to a valid location on your server
Ext.BLANK_IMAGE_URL = '%sresources/images/default/s.gif';""" % settings.EXTJS_URL

        s += """
Lino.GridPanel = Ext.extend(Ext.grid.EditorGridPanel,{
  afterRender : function() {
    Lino.GridPanel.superclass.afterRender.call(this);
    // this.getView().mainBody.focus();
    // console.log(20100114,this.getView().getRows());
    // if (this.getView().getRows().length > 0) {
    //  this.getView().focusRow(1);
    // }
    var tbar = this.getTopToolbar();
    // tbar.on('change',function() {this.getView().focusRow(1);},this);
    // tbar.on('change',function() {this.getSelectionModel().selectFirstRow();this.getView().mainBody.focus();},this);
    // tbar.on('change',function() {this.getView().mainBody.focus();},this);
    // tbar.on('change',function() {this.getView().focusRow(1);},this);
    this.nav = new Ext.KeyNav(this.getEl(),{
      pageUp: function() {tbar.movePrevious(); },
      pageDown: function() {tbar.moveNext(); },
      home: function() {tbar.moveFirst(); },
      end: function() {tbar.moveLast(); },
      scope: this
    });
  },
  // pageSize depends on grid height (Trying to remove scrollbar)
  // Thanks to Christophe Badoit on http://www.extjs.net/forum/showthread.php?t=82647
  calculatePageSize : function() {
    if (!this.rendered) { return false; }
    var row = this.view.getRow(0);
    var rowHeight;
    if (!row) { 
        rowHeight = 41;
    } else {
        rowHeight = Ext.get(row).getHeight();
    }
    // var height = this.getView().scroller.getHeight();
    // console.log('scroller',this.getView().scroller.getHeight());
    // console.log('scroller',this.getView().scroller.getHeight());
    // console.log('mainBody',this.getView().mainBody.getHeight());
    // console.log('getInnerHeight',this.getInnerHeight());
    // console.log('getFrameHeight',this.getFrameHeight());
    var height = this.getView().scroller.getHeight()
    // height -= this.getFrameHeight();
    var ps = Math.floor(height / rowHeight);
    ps -= 1; // extra row
    return (ps > 1 ? ps : false);
  },
  postEditValue : function(value, originalValue, r, field){
    value = Lino.GridPanel.superclass.postEditValue.call(this,value,originalValue,r,field);
    console.log('GridPanel.postEdit()',value, originalValue, r, field);
    return value;
  },
  add_row_listener : function(fn,scope) {
    this.getSelectionModel().addListener('rowselect',fn,scope);
  }
  });

Lino.cell_context_menu = function(job) {
  return function(grid,row,col,e) {
    // console.log('contextmenu',grid,row,col,e);
    e.stopEvent();
    grid.getView().focusRow(row);
    if(!job.cmenu.el){job.cmenu.render(); }
    var xy = e.getXY();
    xy[1] -= job.cmenu.el.getHeight();
    job.cmenu.showAt(xy);
  }
}

        """
        s += """
Lino.on_load_menu = function(response) {
  // console.log('success',response.responseText);
  // console.log('on_load_menu before',Lino.main_menu);
  var p = Ext.decode(response.responseText);
  // console.log('on_load_menu p',p);
  // Lino.viewport.hide();
  // Lino.viewport.remove(Lino.main_menu);
  Lino.main_menu.removeAll();
  Lino.main_menu.add(p);
  // Lino.main_menu = new Ext.Toolbar(p);"""
        #d.update(autoScroll=True)
        #~ d.update(items=js_code(
            #~ "[Lino.main_menu,"+",".join([
                  #~ c.as_ext() for c in self.components]) +"]"))
                    
        s += """
  // console.log('on_load_menu after',Lino.main_menu);"""
        s += """
  // Lino.viewport.add(Lino.main_menu);""" 
        #~ items = "[Lino.main_menu,"+",".join([
                  #~ c.as_ext() for c in self.components]) +"]"
        #~ s += """
  #~ Lino.viewport.add(%s);""" % py2js(self.components)
        s += """
  Lino.viewport.doLayout();
  // console.log('on_load_menu viewport',Lino.viewport);
  // Lino.viewport.show();
  i = Lino.main_menu.get(0);
  if (i) i.focus();"""
        s += """
};"""
        s += """
        
Lino.load_main_menu = function() {
  Ext.Ajax.request({
    waitMsg: 'Loading main menu...',
    url: '/menu',
    success: Lino.on_load_menu,
    failure: function(response) {
      // console.log(response);
      Ext.MessageBox.alert('error','could not connect to the LinoSite.');
    }
  });
};


(function(){
    var ns = Ext.ns('Ext.ux.plugins');

    /**
     * @class Ext.ux.plugins.DefaultButton
     * @extends Object
     *
     * Plugin for Button that will click() the button if the user presses ENTER while
     * a component in the button's form has focus.
     *
     * @author Stephen Friedrich
     * @date 09-DEC-2009
     * @version 0.1
     *
     */
    ns.DefaultButton =  Ext.extend(Object, {
        init: function(button) {
            button.on('afterRender', setupKeyListener, button);
        }
    });

    function setupKeyListener() {
        var formPanel = this.findParentByType('form');
        new Ext.KeyMap(formPanel.el, {
            key: Ext.EventObject.ENTER,
            shift: false,
            alt: false,
            fn: function(keyCode, e){
                if(e.target.type === 'textarea' && !e.ctrlKey) {
                    return true;
                }

                this.el.select('button').item(0).dom.click();
                return false;
            },
            scope: this
        });
    }

    Ext.ComponentMgr.registerPlugin('defaultButton', ns.DefaultButton);

})(); 


/*
Feature request developed in http://extjs.net/forum/showthread.php?t=75751
*/
Ext.override(Ext.form.ComboBox, {
    // queryContext : null, 
    // contextParam : null, 
    setValue : function(v){
        // if(this.name == 'country') console.log('country ComboBox.setValue()',v);
        var text = v;
        if(this.valueField){
          if(v === null) { 
              // console.log(this.name,'.setValue',v,'no lookup needed, value is null');
              v = null;
          }else{
            // if(this.mode == 'remote' && !Ext.isDefined(this.store.totalLength)){
            if(this.mode == 'remote' && ( this.lastQuery === null || (!Ext.isDefined(this.store.totalLength)))){
                // console.log(this.name,'.setValue',v,'must wait for load');
                this.store.on('load', this.setValue.createDelegate(this, arguments), null, {single: true});
                if(this.store.lastOptions === null || this.lastQuery === null){
                    var params;
                    if(this.valueParam){
                        params = {};
                        params[this.valueParam] = v;
                    }else{
                        var q = this.allQuery;
                        this.lastQuery = q;
                        this.store.setBaseParam(this.queryParam, q);
                        params = this.getParams(q);
                    }
                    // console.log(this.name,'.setValue',v,' : call load() with params ',params);
                    this.store.load({params: params});
                }else{
                    // console.log(this.name,'.setValue',v,' : but store is loading',this.store.lastOptions);
                }
                return;
            }else{
                // console.log(this.name,'.setValue',v,' : store is loaded, lastQuery is "',this.lastQuery,'"');
            }
            var r = this.findRecord(this.valueField, v);
            if(r){
                text = r.data[this.displayField];
            }else if(this.valueNotFoundText !== undefined){
                text = this.valueNotFoundText;
            }
          }
        }
        this.lastSelectionText = text;
        if(this.hiddenField){
            this.hiddenField.value = v;
        }
        Ext.form.ComboBox.superclass.setValue.call(this, text);
        this.value = v;
    },
    getParams : function(q){
        // p = Ext.form.ComboBox.superclass.getParams.call(this, q);
        // causes "Ext.form.ComboBox.superclass.getParams is undefined"
        var p = {};
        //p[this.queryParam] = q;
        if(this.pageSize){
            p.start = 0;
            p.limit = this.pageSize;
        }
        // now my code:
        if(this.queryContext) 
            p[this.contextParam] = this.queryContext;
        return p;
    },
    setQueryContext : function(qc){
        if(this.contextParam) {
            console.log(this.name,'.setQueryContext',this.contextParam,'=',qc);
            if(this.queryContext != qc) {
                this.queryContext = qc;
                // delete this.lastQuery;
                this.lastQuery = null;
    }   }   }
});


/*
Ext.override(Ext.form.ComboBox, {
    setValue : function(v){
        // if(this.name == 'country') 
        // if(! v) { v = { text:'', value:undefined }};
        if(! v) { v = [undefined, '']};
        var text = v;
        this.lastSelectionText = v[1];
        if(this.hiddenField){
            this.hiddenField.value = v[0];
        }
        Ext.form.ComboBox.superclass.setValue.call(this, v[1]);
        this.value = v;
    },
    getValue : function(){
        v = Ext.form.ComboBox.superclass.getValue.call(this);
    },
    onSelect : function(record, index){
        if(this.fireEvent('beforeselect', this, record, index) !== false){
            this.setValue([record.data[this.valueField], record.data[this.displayField]]);
            this.collapse();
            this.fireEvent('select', this, record, index);
        }
    },
    beforeBlur : function(){
        var val = this.getRawValue(),
            rec = this.findRecord(this.displayField, val);
        if(!rec && this.forceSelection){
            if(val.length > 0 && val != this.emptyText){
                this.el.dom.value = Ext.isEmpty(this.lastSelectionText) ? '' : this.lastSelectionText;
                this.applyEmptyText();
            }else{
                this.clearValue();
            }
        }else{
            if(rec){
                val = [rec.get(this.valueField),rec.get(this.displayField)];
            }else{
                val = [undefined, '']
            }
            this.setValue(val);
        }
    },
    clearValue : function(){
        if(this.hiddenField){
            this.hiddenField.value = '';
        }
        this.setRawValue('');
        this.lastSelectionText = '';
        this.applyEmptyText();
        this.value = [undefined, ''];
    },

});
*/

"""   

        s += """
Ext.onReady(function(){ """

        for c in self.components:
            for ln in c.js_declare():
                s += "\n" + ln
            
        d = dict(layout='border')
        d.update(items=js_code(py2js([js_code('Lino.main_menu')]+list(self.components))))
        s += """
  Lino.main_menu = new Ext.Toolbar({region:'north',height:27});
  Lino.viewport = new Ext.Viewport(%s);""" % py2js(d)
        s += """
  Lino.viewport.render('body');""" 
    
        s += """
  Lino.load_main_menu();"""
        
        s += """
  var windows = Lino.gup('show').split(',');
  for(i=0;i<windows.length;i++) {
    // console.log(windows[i]);
    // if(windows[i]) eval(windows[i]+".show()");
    if(windows[i]) Lino.do_action(undefined,'/permalink_do/'+windows[i],windows[i],{});
  }
        """
        s += "\n}); // end of onReady()"
        s += "\n</script></head><body></body></html>"
        return s
            
            


class BaseViewReportRequest(reports.ReportRequest):
    
    def __init__(self,request,rh,*args,**kw):
        kw.update(rh.report.params)
        self.request = request
        kw = self.parse_req(request,rh,**kw)
        reports.ReportRequest.__init__(self,rh,*args,**kw)
        self.store = rh.store
        request._lino_request = self
        
    def parse_req(self,request,rh,**kw):
        quick_search = request.GET.get(URL_PARAM_FILTER,None)
        if quick_search:
            kw.update(quick_search=quick_search)
        offset = request.GET.get('start',None)
        if offset:
            kw.update(offset=offset)
        limit = request.GET.get('limit',None)
        if limit:
            kw.update(limit=limit)
        kw.update(user=request.user)
        return kw
      
    def get_absolute_url(self,**kw):
        if self.limit != self.__class__.limit:
            kw.update(limit=self.limit)
        if self.offset is not None:
            kw.update(start=self.offset)
        return self.report.get_absolute_url(**kw)
        
    def render_to_json(self):
        rows = [ self.obj2json(row) for row in self.queryset ]
        total_count = self.total_count
        #lino.log.debug('%s.render_to_json() total_count=%d extra=%d',self,total_count,self.extra)
        # add extra blank row(s):
        for i in range(0,self.extra):
            row = self.create_instance()
            rows.append(self.obj2json(row))
            total_count += 1
        return dict(count=total_count,rows=rows)
        

class CSVReportRequest(BaseViewReportRequest):
    extra = 0
    
    def get_absolute_url(self,**kw):
        kw['csv'] = True
        return BaseViewReportRequest.get_absolute_url(self,**kw)
        
    def render_to_csv(self):
        response = HttpResponse(mimetype='text/csv')
        w = ucsv.UnicodeWriter(response)
        names = [] # fld.name for fld in self.fields]
        fields = []
        for col in self.rh.row_layout._main.column_model.columns:
            names.append(col.editor.field.name)
            fields.append(col.editor.field)
        w.writerow(names)
        for row in self.queryset:
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

        
  
class ChoicesReportRequest(BaseViewReportRequest):
    extra = 0
    
    def __init__(self,request,rh,fldname,*args,**kw):
        #self.recipient_report = rh.report
        self.fieldname = fldname
        fld, remote, direct, m2m = rh.report.model._meta.get_field_by_name(fldname)
        #fld = rpt.model._meta.get_field_by_name(fldname)
        assert direct
        self.rec_field = fld
        #called_rpt = reports.get_model_report(fld.rel.to)
        #rh = rpt.get_handle(ui)
        BaseViewReportRequest.__init__(self,request,rh,*args,**kw)
        
    #~ def parse_req(self,request,rh,**kw):
        #~ kw = BaseViewReportRequest.parse_req(self,request,rh,**kw)
        #~ kw['extra'] = 0
        #~ return kw
          
    def get_queryset(self,**kw):
        pk = self.request.GET.get(URL_PARAM_CHOICES_PK,None)
        return self.report.get_field_choices(self.rec_field,pk,**kw)
        #return self.report.get_queryset(self,master_instance=self.master_instance,**kw)
        
    def get_absolute_url(self,**kw):
        kw['choices_for_field'] = self.fieldname
        return BaseViewReportRequest.get_absolute_url(self,**kw)
        
    def obj2json(self,obj,**kw):
        kw[CHOICES_TEXT_FIELD] = unicode(obj)
        #kw['__unicode__'] = unicode(obj)
        kw[CHOICES_VALUE_FIELD] = obj.pk # getattr(obj,'pk')
        #kw[self.fieldname] = obj.pk 
        return kw
          
    #~ rh = 
    #~ req = ChoicesReportRequest(rpt,request)
    #~ pk = request.GET.get(URL_PARAM_CHOICES_PK,None)
    #~ choices_filter = rpt.get_field_choices(pk)
    #~ qs = rpt.get_queryset
    #~ choices = rpt.get_choice_field
    #~ model = models.get_model(app_label,modname)
    #~ field = model._meta.get_field_by_name(fldname)
    #~ get_field_choices
    #~ rpt = field._lino_choices_report
    #~ #kw['colname'] = request.POST['colname']
    #~ return json_report_view_(request,rpt,**kw)
        
  
class ViewReportRequest(BaseViewReportRequest):
  
    editing = 0
    selector = None
    sort_column = None
    sort_direction = None
    
    def parse_req(self,request,rh,**kw):
        kw = BaseViewReportRequest.parse_req(self,request,rh,**kw)
        if rh.report.master is not None and not kw.has_key('master_instance'):
            pk = request.GET.get(URL_PARAM_MASTER_PK,None)
            if pk == UNDEFINED:
                pk = None
            if pk == '':
                pk = None
            if pk is None:
                kw.update(master_instance=None)
            else:
                if rh.report.master is ContentType:
                    mt = request.GET.get(URL_PARAM_MASTER_TYPE)
                    master_model = ContentType.objects.get(pk=mt).model_class()
                else:
                    master_model = rh.report.master
                try:
                    m = master_model.objects.get(pk=pk)
                except master_model.DoesNotExist,e:
                    lino.log.warning(
                      "There's no %s with primary key %r",
                      master_model.__name__,pk)
                else:
                    kw.update(master_instance=m)
        sort = request.GET.get('sort',None)
        if sort:
            self.sort_column = sort
            sort_dir = request.GET.get('dir','ASC')
            if sort_dir == 'DESC':
                sort = '-'+sort
                self.sort_direction = 'DESC'
            kw.update(order_by=sort)
        
        layout = request.GET.get('layout',None)
        if layout:
            kw.update(layout=rh.layouts[int(layout)])
        return kw
        
        
    def get_user(self):
        return authenticated_user(self.request.user)

    def get_absolute_url(self,**kw):
        if self.master_instance is not None:
            kw.update(master_instance=self.master_instance)
        if self.sort_column is not None:
            kw.update(sort=self.sort_column)
        if self.sort_direction is not None:
            kw.update(dir=self.sort_direction)
        if self.layout is not self.rh.layouts[1]:
            kw.update(layout=self.layout.index)
        return BaseViewReportRequest.get_absolute_url(self,**kw)

    def obj2json(self,obj,**kw):
        #lino.log.debug('obj2json(%s)',obj.__class__)
        #lino.log.debug('obj2json(%r)',obj)
        for fld in self.store.fields:
            fld.obj2json(obj,kw)
        #lino.log.debug('  -> %r',kw)
        return kw
            




from django.conf.urls.defaults import patterns, url, include

class SaveWindowConfig(actions.Command): # actors.Actor): # actions.Action):
    def run(self,context,name):
        h = int(context.request.POST.get('h'))
        w = int(context.request.POST.get('w'))
        maximized = context.request.POST.get('max')
        if maximized == 'true':
            maximized = True
        else:
            maximized = False
        x = int(context.request.POST.get('x'))
        y = int(context.request.POST.get('y'))
        context.confirm("Save %r window config (%r,%r,%r,%r,%r)\nAre you sure?" % (name,x,y,h,w,maximized))
        #context.confirm("%r,%r,%r,%r : Are you sure?!" % (name,h,w,maximized))
        ui.window_configs[name] = (x,y,w,h,maximized)
        #ui.window_configs[name] = (w,h,maximized)
        ui.save_window_configs()


def permalink_do_view(request,name=None):
    name = name.replace('_','.')
    actor = actors.get_actor(name)
    context = ActionContext(request,actor,None)
    context.run()
    return json_response(context.response)

def save_win_view(request,name=None):
    #print 'save_win_view()',name
    actor = SaveWindowConfig()
    context = ActionContext(request,actor,None,name)
    context.run()
    return json_response(context.response)

def menu_view(request):
    from lino import lino_site
    s = py2js(lino_site.get_menu(request))
    return HttpResponse(s, mimetype='text/html')


def act_view(request,app_label=None,actor=None,action=None,**kw):
    actor = actors.get_actor2(app_label,actor)
    #action = actor.get_action(action)
    context = ActionContext(request,actor,action)
    context.run()
    return json_response(context.response)

def unused_form_view(request,app_label=None,formname=None,actname=None,**kw):
    action = actors.get_actor2(app_label,formname)
    if actname is not None:
        action = getattr(action,actname)
    context = ActionContext(action,request)
    context.run()
    return json_response(context.response)

def unused_action_view(request,app_label=None,actname=None,**kw):
    action = actors.get_actor2(app_label,actname)
    context = ActionContext(action,request)
    context.run()
    return json_response(context.response)

def choices_view(request,app_label=None,rptname=None,fldname=None,**kw):
    rpt = actors.get_actor2(app_label,rptname)
    kw['choices_for_field'] = fldname
    return json_report_view_(request,rpt,**kw)
    
    
def grid_afteredit_view(request,**kw):
    kw['colname'] = request.POST['grid_afteredit_colname']
    kw['submit'] = True
    return json_report_view(request,**kw)

def form_submit_view(request,**kw):
    kw['submit'] = True
    return json_report_view(request,**kw)

def list_report_view(request,**kw):
    #kw['simple_list'] = True
    return json_report_view(request,**kw)
    
def csv_report_view(request,**kw):
    kw['csv'] = True
    return json_report_view(request,**kw)
    
    
def json_report_view(request,app_label=None,rptname=None,**kw):
    rpt = actors.get_actor2(app_label,rptname)
    return json_report_view_(request,rpt,**kw)

def json_report_view_(request,rpt,grid_action=None,colname=None,submit=None,choices_for_field=None,csv=False):
    if not rpt.can_view.passes(request):
        return json_response_kw(success=False,
            msg="User %s cannot view %s." % (request.user,rpt))
    if grid_action:
        #~ a = rpt.get_action(grid_action)
        #~ if a is None:
            #~ return json_response_kw(
                #~ success=False,
                #~ msg="Report %s has no action %r" % (rpt,grid_action))
        context = GridActionContext(request,rpt,grid_action)
        context.run()
        #d = a.get_response(rptreq)
        return json_response(context.response)
            
    rh = rpt.get_handle(ui)
    if choices_for_field:
        rptreq = ChoicesReportRequest(request,rh,choices_for_field)
    elif csv:
        rptreq = CSVReportRequest(request,rh,choices_for_field)
        return rptreq.render_to_csv()
    else:
        rptreq = ViewReportRequest(request,rh)
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
    d = rptreq.render_to_json()
    return json_response(d)
    
def json_response_kw(**kw):
    return json_response(kw)
    
def json_response(x):
    #s = simplejson.dumps(kw,default=unicode)
    #return HttpResponse(s, mimetype='text/html')
    s = py2js(x)
    #lino.log.debug("json_response() -> %r", s)
    return HttpResponse(s, mimetype='text/html')



from lino.ui import base

class ExtUI(base.UI):
    _response = None
    
    
    window_configs_file = os.path.join(settings.PROJECT_DIR,'window_configs.pck')
                
    def __init__(self):
        #self.StaticText = StaticText
        self.GridElement = GridElement
        self.VirtualFieldElement = VirtualFieldElement
        self.MethodElement = MethodElement
        self.ButtonElement = ButtonElement
        self.Panel = Panel
        self.Store = Store
        self.Spacer = Spacer
        self.StaticTextElement = StaticTextElement
        #self.ActionContext = ActionContext
        self.InputElement = InputElement
        self.window_configs = {}
        if os.path.exists(self.window_configs_file):
            lino.log.info("Loading %s...",self.window_configs_file)
            wc = pickle.load(open(self.window_configs_file,"rU"))
            #lino.log.debug("  -> %r",wc)
            if type(wc) is dict:
                self.window_configs = wc
        else:
            lino.log.warning("window_configs_file %s not found",self.window_configs_file)
            
    def save_window_configs(self):
        f = open(self.window_configs_file,'wb')
        pickle.dump(self.window_configs,f)
        f.close()
        self._response = None



    def main_panel_class(self,layout):
        if isinstance(layout,layouts.RowLayout) : 
            return GridMainPanel
        if isinstance(layout,layouts.PageLayout) : 
            return DetailMainPanel
        if isinstance(layout,layouts.FormLayout) : 
            return FormMainPanel
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
            viewport = Viewport(lino_site.title,comp)
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
            (r'^csv/(?P<app_label>\w+)/(?P<rptname>\w+)$', csv_report_view),
            (r'^grid_action/(?P<app_label>\w+)/(?P<rptname>\w+)/(?P<grid_action>\w+)$', json_report_view),
            (r'^submit/(?P<app_label>\w+)/(?P<rptname>\w+)$', form_submit_view),
            (r'^grid_afteredit/(?P<app_label>\w+)/(?P<rptname>\w+)$', grid_afteredit_view),
            (r'^form/(?P<app_label>\w+)/(?P<actor>\w+)/(?P<action>\w+)$', act_view),
            (r'^form/(?P<app_label>\w+)/(?P<actor>\w+)$', act_view),
            (r'^action/(?P<app_label>\w+)/(?P<actor>\w+)$', act_view),
            (r'^choices/(?P<app_label>\w+)/(?P<rptname>\w+)/(?P<fldname>\w+)$', choices_view),
            (r'^save_win/(?P<name>\w+)$', save_win_view),
            (r'^permalink_do/(?P<name>\w+)$', permalink_do_view),
            
        )

    def get_action_url(self,a,**kw):
        url = "/action/" + a.app_label + "/" + a.name 
        #url = "/action/" + a.actor_id # app_label + "/" + a.name 
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
        #~ url = "/form/" + a.app_label + "/" + a.name + "/" + btn.name
        #~ if len(kw):
            #~ url += "?" + urlencode(kw)
        #~ return url
        
    def get_choices_url(self,fke,**kw):
        return build_url("/choices",fke.lh.link.report.app_label,fke.lh.link.report.name,fke.field.name,**kw)
        
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
            kw[URL_PARAM_MASTER_PK] = master_instance.pk
            mt = ContentType.objects.get_for_model(master_instance.__class__).pk
            kw[URL_PARAM_MASTER_TYPE] = mt
        if len(kw):
            url += "?" + urlencode(kw)
        return url
        
    def window_options(self,lh,**kw):
        name = id2js(lh.name)
        kw.update(title=lh.get_title(self))
        # kw.update(closeAction='hide')
        kw.update(maximizable=True)
        #kw.update(id=name)
        url = '/save_win/' + name
        js = 'Lino.save_window_config(this,%r)' % url
        kw.update(tools=[dict(id='save',handler=js_code(js))])
        kw.update(layout='fit')
        kw.update(items=lh._main)
        if lh.start_focus is not None:
            kw.update(defaultButton=lh.start_focus.name)
        wc = self.window_configs.get(name,None)
        #kw.update(defaultButton=self.lh.link.inputs[0].name)
        if wc is None:
            if lh.height is None:
                kw.update(height=300)
            else:
                kw.update(height=lh.height*EXT_CHAR_HEIGHT + 7*EXT_CHAR_HEIGHT)
            if lh.width is None:
                kw.update(width=400)
            else:
                kw.update(width=lh.width*EXT_CHAR_WIDTH + 10*EXT_CHAR_WIDTH)
        else:
            assert len(wc) == 5
            kw.update(x=wc[0])
            kw.update(y=wc[1])
            kw.update(width=wc[2])
            kw.update(height=wc[3])
            #kw.update(width=js_code('Lino.viewport.getWidth()*%d/100' % wc[0]))
            #kw.update(height=js_code('Lino.viewport.getHeight()*%d/100' % wc[1]))
            kw.update(maximized=wc[4])
        return kw
            
        
    def view_report(self,context,**kw):
        """
        called from Report.view()
        """
        rpt = context.actor
        rh = self.get_report_handle(rpt)
        rr = ViewReportRequest(context.request,rh)
        lh = rr.layout 
        # kw['defaultButton'] = js_code('this.main_grid')
        kw = self.window_options(lh,**kw)
        context.response.update(call=lh._main.js_job_constructor(rr,**kw))
        
        
    def view_form(self,context,**kw):
        "called from Form.run()"
        frm = context.actor
        fh = self.get_form_handle(frm)
        #fh.setup()
        lh = fh.lh
        kw = self.window_options(lh,**kw)
        rr = None
        context.response.update(call=lh._main.js_job_constructor(rr,**kw))
        
            
    
ui = ExtUI()


