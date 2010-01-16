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
from urllib import urlencode

from dateutil import parser as dateparser

from django.db import models
from django.conf import settings
from django.http import HttpResponse
from django.utils import simplejson
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
EXT_CHAR_HEIGHT = 12

URL_PARAM_MASTER_TYPE = 'mt'
URL_PARAM_MASTER_PK = 'mk'
# URL_PARAM_MASTER_GRID = 'mg'
URL_PARAM_FILTER = 'qs'

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
        
class GridActionContext(ActionContext):
    def __init__(self,request,*args,**kw):
        ActionContext.__init__(self,request,*args,**kw)
        selected = self.request.POST.get('selected',None)
        if selected:
            self.selected_rows = [
              self.actor.model.objects.get(pk=pk) for pk in selected.split(',') if pk]
        else:
            self.selected_rows = []
        
        
      

def id2js(s):
  return s.replace('.','_')
  
class js_code:
    "A string that py2js will represent as is, not between quotes."
    def __init__(self,s):
        self.s = s
    #~ def __repr__(self):
        #~ return self.s
  
def py2js(v,**kw):
    #lino.log.debug("py2js(%r,%r)",v,kw)
        
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
        
    if callable(v):
        return "\n".join([ln for ln in v(**kw)])

    assert len(kw) == 0, "py2js() : value %r not allowed with keyword parameters" % v
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
    return simplejson.dumps(v)
            


DECLARE_INLINE = 0
DECLARE_VAR = 1
DECLARE_THIS = 2

class Variable(object):
    declare_type = DECLARE_THIS
    #declare_type = DECLARE_INLINE
    ext_suffix = ''
    value_template = "%s"
    #declared = False
    #declaration_order = 9
    has_comp = False
    
    def __init__(self,name,value):
        self.name = name
        self.value = value
        self.ext_name = id2js(name) + self.ext_suffix
        
    def js_lines(self):
        if self.has_comp:
            def lines():
              yield "new function(parent) {"
              #yield "  this._parent = parent;" 
              for e in self.js_elements():
                  for ln in e.js_lines():
                      yield "  " + ln
              yield "  this.comp = %s;" % self.as_ext_value()
              yield "}(this)"
            value = '\n'.join([ln for ln in lines()])
        else:
            for e in self.js_elements():
                for ln in e.js_lines():
                    yield ln
            value = self.as_ext_value()
        if self.declare_type == DECLARE_INLINE:
            pass
        elif self.declare_type == DECLARE_VAR:
            yield "var %s = %s;" % (self.ext_name,value)
        elif self.declare_type == DECLARE_THIS:
            yield "this.%s = %s;" % (self.ext_name,value)
            
    def as_ext_value(self):
        return self.value_template % py2js(self.value)
        
    def js_elements(self):
        return []
            
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

class Component(Variable): # better name? JSObject? Scriptable?
    
    def __init__(self,name,**options):
        Variable.__init__(self,name,options)
        #~ self.name = name
        #~ self.options = options
        
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
        
    def get_from_form(self,instance,values):
        v = values.get(self.field.name)
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
    def get_from_form(self,instance,values):
        v = values.get(self.field.name)
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
            
    def get_from_form(self,instance,values):
        v = values.get(self.field.name)
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
        
    def get_from_form(self,instance,values):
        v = values.get(self.field.name)
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
        # print 20091208, self.field.name
        d[self.field.name] = meth()
        
    def get_from_form(self,instance,values):
        pass
        #raise Exception("Cannot update a virtual field")


class OneToOneStoreField(StoreField):
        
    def get_from_form(self,instance,values):
        #v = values.get(self.field.name,None)
        v = values.get(self.field.name)
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
        s += "," + repr(self.field.name+"Hidden")
        return s 
        
    def get_from_form(self,instance,values):
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
                print "[get_from_form]", v, values.get(self.field.name)
        instance[self.field.name] = v
        
    def obj2json(self,obj,d):
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
                assert fld is not None, "%s"
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
        if self.editable:
            editor = self.get_field_options()
            kw.update(editor=js_code(py2js(editor)))
        w = self.width or self.preferred_width
        kw.update(width=w*EXT_CHAR_WIDTH)
        return kw    
        
    def as_ext_column(self):
        return py2js(self.get_column_options())
        
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
        
    #~ def ext_width(self):
        #~ if self.width is None:
            #~ return None
        #~ #if self.parent.labelAlign == 'top':
        #~ return max(self.width,self.label_width) * EXT_CHAR_WIDTH + self.xpadding
        
class InputElement(LayoutElement):
    #declare_type = DECLARE_INLINE
    declare_type = DECLARE_THIS
    #declare_type = DECLARE_VAR
    name_suffix = "_input"
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
        return panel_options
        
class ButtonElement(LayoutElement):
    #declare_type = DECLARE_INLINE
    #declare_type = DECLARE_THIS
    declare_type = DECLARE_VAR
    name_suffix = "_btn"
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
        kw.update(text=self.action.label or self.name)
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
        
class VirtualFieldElement(LayoutElement):
    def __init__(self,lh,name,gfk,**kw):
        assert isinstance(gfk,generic.GenericForeignKey)
        self.gfk = gfk
        LayoutElement.__init__(self,lh,name,label=name,**kw)
        #print "20091210", name,gfk
    
        
        
class FieldElement(LayoutElement):
    #declare_type = DECLARE_INLINE
    #declare_type = DECLARE_THIS
    declare_type = DECLARE_VAR
    stored = True
    #declaration_order = 3
    name_suffix = "_field"
    
    def __init__(self,lh,field,**kw):
        assert field.name, Exception("field %r has no name!" % field)
        LayoutElement.__init__(self,lh,field.name,label=field.verbose_name,**kw)
        self.field = field
        self.editable = field.editable and not field.primary_key
        
    def get_column_options(self,**kw):
        kw = LayoutElement.get_column_options(self,**kw)
        if self.editable:
            fo = self.get_field_options()
            kw.update(editor=fo)
        return kw    
        
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
        #d.update(xtype='panel',layout='form') 
        d.update(xtype='container',layout='form')
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
        #po.update(items=js_code("[ { %s } ]" % dict2js(fo)))
        po.update(items=fo)
        return po
        
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
    xtype = "combo"
    sortable = True
    #width = 20
    
    def __init__(self,*args,**kw):
        FieldElement.__init__(self,*args,**kw)
        self.report = self.lh.link.get_field_choices(self.field)
        #self.report = rd.get_handle(self.lh.ui)
        self.rh = self.report.get_handle(self.lh.ui)
        self.lh.needs_store(self.rh)
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
            kw.update(store=self.rh.store)
            #kw.update(store=js_code(self.store.as_ext_value(request)))
            kw.update(hiddenName=self.name+"Hidden")
            kw.update(valueField=self.rh.store.pk.attname)
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
            kw.update(pageSize=self.rh.report.page_length)
            
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
    
    def __init__(self,*args,**kw):
        FieldElement.__init__(self,*args,**kw)
        self.preferred_width = min(5,self.field.max_digits) \
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
        delegate = lh.ui.field2elem(lh,return_type,**kw)
        #~ for a in ('ext_width','ext_options',
          #~ 'get_column_options','get_field_options'):
        for a in ('ext_options','get_column_options','get_field_options'):
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
    #has_comp = True
    declare_type = DECLARE_THIS
    
    
    def __init__(self,lh,name,*elements,**kw):
        self.has_frame = lh.layout.has_frame
        self.labelAlign = lh.layout.label_align
        self.elements = elements
        LayoutElement.__init__(self,lh,name,**kw)
        
    def js_elements(self):
        return self.elements
        #~ for ln in self.elements.js_lines():
            #~ yield ln
            
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

    #~ def ext_options(self):
        #~ d = LayoutElement.ext_options(self)
        #~ return d
        
    #~ def js_lines(self):
        #~ if self.declare_type == DECLARE_THIS and self.has_comp:
            #~ yield "this.%s = new function(parent) {" % self.ext_name
            #~ #yield "  this._parent = parent;" 
            #~ for e in self.elements:
                #~ for ln in e.js_lines():
                    #~ yield "  "+ln
            #~ yield "  this.comp = %s;" % self.as_ext_value()
            #~ yield "}(this);"
        #~ else:
            #~ for e in self.elements:
                #~ for ln in e.js_lines():
                    #~ yield ln
            #~ for ln in LayoutElement.jslines(self):
                #~ yield ln
            #~ #yield "this.%s = %s;" % (self.ext_name,self.as_ext_value())
            
            


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
        
class GridElement(Container):
    #value_template = "new Ext.grid.EditorGridPanel(%s)"
    value_template = "new Lino.GridPanel(%s)"
    ext_suffix = "_grid"
    #has_comp = True    
    
    def __init__(self,lh,name,rh,*elements,**kw):
        assert isinstance(rh,reports.ReportHandle), "%r is not a ReportHandle!" % rh
        """
        Note: lh is the owning layout handle. 
        In case of a slave grid, lh.layout.report is the master.
        """
        if len(elements) == 0:
            elements = rh.row_layout._main.elements
        w = 0
        for e in elements:
            w += (e.width or e.preferred_width)
        self.preferred_width = constrain(w,10,120)
        self.preferred_height = rh.report.page_length + 2 # one line for column headers, another for title bar
        self.keys = None
        Container.__init__(self,lh,name,*elements,**kw)
        self.rh = rh
        self.report = rh.report
        lh.needs_store(rh)
        self.column_model = ColumnModel(self)
        
    def setup(self):
        if self.keys:
            return
        #setup_report(self.report)
        keys = []
        buttons = []
        for a in self.report.actions:
            h = js_code("Lino.grid_action(this,'%s','%s')" % (
                  a.name, 
                  self.rh.get_absolute_url(grid_action=a.name)))
            buttons.append(dict(text=a.label,handler=h))
            if a.key:
                keys.append(dict(
                  handler=h,
                  key=a.key.keycode,ctrl=a.key.ctrl,alt=a.key.alt,shift=a.key.shift))
        if len(self.rh.layouts) > 2:
            # the first detail window can be opend with Ctrl+ENTER 
            key = actions.RETURN(ctrl=True)
            lh = self.rh.layouts[2]
            keys.append(dict(
              handler=js_code("Lino.show_slave(this,%r,%r)" % (lh.get_absolute_url(run=True),lh.label)),
              key=key.keycode,ctrl=key.ctrl,alt=key.alt,shift=key.shift))

            for layout in self.rh.layouts[2:]:
                buttons.append(dict(
              handler=js_code("Lino.show_slave(this,%r,%r)" % (lh.get_absolute_url(run=True),lh.label)),
                  text=layout._ld.label))
              
        for sl in self.report._slaves:
            rh = sl.get_handle(self.lh.ui)
            buttons.append(dict(
              handler=js_code("Lino.show_slave(this,%r,%r)" % (rh.row_layout.get_absolute_url(run=True),rh.report.label)),
              #handler=js_code("Lino.show_slave(this,%r)" % id2js(rh.row_layout.name)),
              text = rh.report.label,
            ))
            
        self.keys = Variable(self.ext_name+'_keys',keys)
        self.buttons = Variable(self.ext_name+'_buttons',buttons)
        self.cmenu = Variable('cmenu',js_code("new Ext.menu.Menu(%s)" % py2js(self.buttons)))
        
        
    def js_lines(self):
        self.setup()
        for ln in Container.js_lines(self):
            yield ln
        yield "%s.on('afteredit', Lino.grid_afteredit(this,'%s','%s'));" % (
          self.as_ext(),
          self.rh.get_absolute_url(grid_afteredit=True),
          self.rh.store.pk.name)
        yield "%s.on('cellcontextmenu', Lino.cell_context_menu(this));" % self.as_ext()
        
          
    def js_elements(self):
        """
        GridElement, though it is a Container, doesn't generate the declaration of its elements 
        because self.column_model does this indirectly.
        """
        self.setup()
        #yield self.rh.store
        yield self.column_model
        yield self.buttons
        yield self.keys
        yield self.cmenu

    def ext_options(self):
        self.setup()
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
        d.update(selModel=js_code("new Ext.grid.RowSelectionModel({singleSelect:false})"))
        #~ def cellcontextmenu():
            #~ yield "Lino.cell_context_menu = function(grid,row,col,e) {"
            #~ yield "  console.log('contextmenu',grid,row,col,e);"
            #~ yield "  e.stopEvent();"
            #~ yield "  if(!this.cmenu.el){this.cmenu.render(); }"
            #~ yield "  var xy = e.getXY();"
            #~ yield "  xy[1] -= this.cmenu.el.getHeight();"
            #~ yield "  this.cmenu.showAt(xy);"
            #~ yield "}"
        #~ d.update(listeners=dict(cellcontextmenu=cellcontextmenu))
        
        tbar = dict(
          store=self.rh.store,
          displayInfo=True,
          pageSize=self.report.page_length,
          prependButtons=False,
          items=self.buttons, # js_code('buttons'),
        )
        d.update(tbar=js_code("new Ext.PagingToolbar(%s)" % py2js(tbar)))
        # searchString thanks to http://www.extjs.com/forum/showthread.php?t=82838
        def keypress():
            yield "function(field, e) {"
            # searching starts when user presses Enter.
            yield "  if(e.getKey() == e.RETURN) {"
            yield "    console.log('keypress',field.getValue(),store)"
            #    // var searchString = Ext.getCmp('seachString').getValue();
            yield "    store.setBaseParam('%s',field.getValue());" % URL_PARAM_FILTER
            yield "    store.load({params: { start: 0, limit: %d }});" % self.report.page_length
            yield "  }"
            yield "}"
        search_field = dict(
            id = 'seachString',
            fieldLabel = 'Search',
            xtype = 'textfield',
            enableKeyEvents = True, # required if you need to detect key-presses
            listeners = dict(keypress=keypress)
        )
        d.update(bbar=[search_field])
        return d
            
      
        
class M2mGridElement(GridElement):
    def __init__(self,lh,field,*elements,**kw):
        self.field = field
        rpt = reports.get_model_report(field.rel.to)
        rh = rpt.get_handle(lh.ui)
        GridElement.__init__(self,lh,id2js(rpt.actor_id),rh,*elements,**kw)
  

  
class GridMainPanel(GridElement):
    #declare_type = DECLARE_VAR
    def __init__(self,lh,name,vertical,*elements,**kw):
        'ignore the "vertical" arg'
        #lh.report.setup()
        GridElement.__init__(self,lh,name,lh.link,*elements,**kw)
        #~ if self.height is None:
            #~ self.height = self.preferred_height
        #~ if self.width is None:
            #~ self.width = self.preferred_width
        #lino.log.debug("GridMainPanel.__init__() %s",self.name)
        
    def ext_options(self):
        d = GridElement.ext_options(self)
        # d = Layout.ext_options(self,request)
        # d = dict(title=request._lino_report.get_title()) 
        #d.update(title=request._lino_request.get_title()) 
        #d.update(title=self.layout.label)
        #d.update(title=self.report.get_title(None)) 
        #d.update(region='center',split=True)
        del d['title']
        return d
        
    def js_lines(self):
        for ln in GridElement.js_lines(self):
            yield ln
            
        yield "this.refresh = function() { this.%s.getStore().load()}" % self.ext_name
        



class DetailMainPanel(Panel):
    declare_type = DECLARE_THIS
    value_template = "new Ext.form.FormPanel(%s)"
    def __init__(self,lh,name,vertical,*elements,**kw):
        self.rh = lh.link
        self.report = self.rh.report
        Panel.__init__(self,lh,name,vertical,*elements,**kw)
        #lh.needs_store(self.rh)
        
    #~ def js_elements(self):
        #~ self.setup()
        #~ yield self.rh.store
        #~ yield self.column_model
        #~ yield self.buttons
        #~ yield self.keys
        
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
            }) """ % self.rh.store.ext_name))
        #d.update(items=js_code(self._main.as_ext(request)))
        #d.update(items=js_code("[%s]" % ",".join([e.as_ext() for e in self.elements])))
        d.update(items=self.elements)
        d.update(autoHeight=False)
        return d
        
    def js_lines(self):
        for ln in Panel.js_lines(self):
            yield ln
        #yield "mastergrid = Ext.getCmp()"
        yield "this.refresh = function() { console.log('DetailMainPanel.refresh() not yet implemented.');};"
        #yield "var slaves = [ %s ];" % ','.join([slave.rh.store.as_ext() for slave in self.lh.slave_grids])
        yield "var load_record = this.load_record = function(record) {"
        #yield "function load_record (record) {"
        #name = id2js(self.lh.name) + '.' + self.lh._main.ext_name
        #name = 'this.' + self.lh._main.ext_name
        name = self.as_ext()
        yield "  this.current_pk = record.data.id;" 
        yield "  %s.form.loadRecord(record);" % name
        yield "  var p = { %s: record.data.id }" % URL_PARAM_MASTER_PK
        #yield "  var p = { %s: record.data.%s }" % (URL_PARAM_MASTER_PK,self.rh.store.pk.name)
        mt = ContentType.objects.get_for_model(self.report.model).pk
        yield "  p[%r] = %r;" % (URL_PARAM_MASTER_TYPE,mt)
        for slave in self.lh.slave_grids:
            yield "  %s.load({params:p});" % slave.rh.store.as_ext()
        #yield "  for(i=0;i++;i<slaves.length) { console.log('load slave',slaves[i],p); slaves[i].load({params:p}) };"
        yield "};"
        yield "if(caller) {"
        yield "  caller.main_grid.getSelectionModel().addListener('rowselect',"
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
        js = js_code("function() {caller.main_grid.getSelectionModel().selectPrevious()}")
        keys.append(dict(
          handler=js,
          key=key.keycode,ctrl=key.ctrl,alt=key.alt,shift=key.shift))
        buttons.append(dict(handler=js,text="Previous"))

        key = actions.PAGE_DOWN
        js = js_code("function() {caller.main_grid.getSelectionModel().selectNext()}")
        keys.append(dict(
          handler=js,
          key=key.keycode,ctrl=key.ctrl,alt=key.alt,shift=key.shift))
        buttons.append(dict(handler=js,text="Next"))
        if len(keys):
            #yield "console.log(%s);" % self.as_ext()
            #yield "console.log(%s.comp);" % self.as_ext()
            yield "  %s.keys = %s;" % (self.as_ext(),py2js(keys))
        
        for btn in buttons:
            yield "  %s.addButton(%s);" % (self.as_ext(),py2js(btn))
    
        yield "}"
        
        keys = []
        buttons = []

        url = self.rh.get_absolute_url(submit=True)
        js = js_code("Lino.form_submit(this,'%s',caller.main_grid.getStore(),'%s')" % (
                url,self.rh.store.pk.name))
        buttons.append(dict(handler=js,text='Submit'))
        
        for btn in buttons:
            yield "  %s.addButton(%s);" % (self.as_ext(),py2js(btn))
    
        

class FormMainPanel(Panel):
    value_template = "new Ext.form.FormPanel(%s)"

    def ext_options(self,**d):
        d = Panel.ext_options(self,**d)
        #d.update(title=self.lh.label)
        #d.update(region='east',split=True) #,width=300)
        d.update(autoScroll=True)
        #d.update(items=js_code("[%s]" % ",".join([e.as_ext() for e in self.elements])))
        d.update(items=self.elements)
        d.update(autoHeight=False)
        return d
        



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
    // console.log(pkname,job);
    p = {};
    // p[pkname] = store.getAt(0).data.id;
    p[pkname] = job.current_pk;
    job.main_panel.form.submit({
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
    p['colname'] = e.field;
    p[e.field] = e.value;
    // console.log(e);
    // add Hidden value used by ForeignKeyStoreField
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
  // console.log("grid_action.this=",this);
  // console.log("grid_action.gridwin=",gridwin);
  // console.log("foo",grid,name,url);
  return function(event) {
    var sel_pks = '';
    var sels = caller.main_grid.getSelectionModel().getSelections();
    for(var i=0;i<sels.length;i++) { sel_pks += sels[i].id + ','; };
    Lino.do_action(caller,url,name,{selected:sel_pks});
  };
};"""

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
      if(!win.hidden) {windows+=sep+win.getId();sep=","}
    });
    document.location = "%s?show=" + windows;
};""" % uri

        s += """
Lino.show_slave = function (caller,url,name) { 
  return function(btn,evt) {
    // p = caller.main_grid.getStore().baseParams;
    // console.log('show_detail',name,url,p)
    // Lino.do_action(caller,url,name,p);
    Lino.do_action(caller,url,name,{});
  }
};
""" 

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

        if False:
            rpts = [ ReportRenderer(rpt) 
                for rpt in reports.master_reports + reports.slave_reports + reports.generic_slaves.values()]
            for rpt in rpts:
                for ln in rpt.report.store.js_lines():
                    s += "\n" + ln
            for rpt in rpts:
                for ln in rpt.js_lines():
                    s += "\n" + ln
        
            dlgs = [ DialogRenderer(dlg) for dlg in layouts.dialogs ]
            for dlg in dlgs:
                for ln in dlg.js_lines():
                    s += "\n" + ln

            acts = [ ActionRenderer(a) for a in actions.global_actions ]
            for a in acts:
                for ln in a.js_lines():
                    s += "\n" + ln


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


"""   

        s += """
Ext.onReady(function(){ """

        for c in self.components:
            for ln in c.js_lines():
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
            
            



class ViewReportRequest(reports.ReportRequest):
  
    editing = 0
    selector = None
    sort_column = None
    sort_direction = None
    
    def __init__(self,request,rh,*args,**kw):
      
        #~ self.params = rh.report.param_form(request.GET)
        #~ if self.params.is_valid():
            #~ kw.update(self.params.cleaned_data)
        kw.update(rh.report.params)
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
        
        quick_search = request.GET.get(URL_PARAM_FILTER,None)
        if quick_search:
            kw.update(quick_search=quick_search)
        offset = request.GET.get('start',None)
        if offset:
            kw.update(offset=offset)
        limit = request.GET.get('limit',None)
        if limit:
            kw.update(limit=limit)
        layout = request.GET.get('layout',None)
        if layout:
            kw.update(layout=rh.layouts[int(layout)])

        #print "ViewReportRequest.__init__() 1",report.name
        self.request = request
        
        reports.ReportRequest.__init__(self,rh,*args,**kw)
        self.store = rh.store
        #print "ViewReportRequest.__init__() 2",report.name
        request._lino_request = self
        
    def get_user(self):
        return authenticated_user(self.request.user)

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
        if self.layout is not self.rh.layouts[1]:
            kw.update(layout=self.layout.index)
        return self.report.get_absolute_url(**kw)

    #~ def unused_render_to_html(self):
        #~ if len(self.store.layouts) == 2:
            #~ comps = [l._main for l in self.store.layouts]
        #~ else:
            #~ tabs = [l._main for l in self.store.layouts[1:]]
            #~ comps = [self.store.layouts[0]._main,extjs.TabPanel(None,"EastPanel",*tabs)]
        #~ return lino_site.ext_view(self.request,*comps)
        #return self.report.viewport.render_to_html(self.request)


    def obj2json(self,obj,**kw):
        #lino.log.debug('obj2json(%s)',obj.__class__)
        #lino.log.debug('obj2json(%r)',obj)
        for fld in self.store.fields:
            fld.obj2json(obj,kw)
        #lino.log.debug('  -> %r',kw)
        return kw
            
    def render_to_json(self):
        rows = [ self.obj2json(row) for row in self.queryset ]
        total_count = self.total_count
        # add extra blank row(s):
        for i in range(0,self.extra):
        #if self.layout.index == 1: # currently only in a grid
            row = self.create_instance()
            rows.append(self.obj2json(row))
            #~ d = {}
            #~ for fld in self.store.fields:
                #~ d[fld.field.name] = None
            #~ # d[self.store.pk.name] = UNDEFINED
            #~ rows.append(d)
            total_count += 1
        return dict(count=total_count,rows=rows)
        

        




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

def choices_view(request,app_label=None,modname=None,fldname=None,**kw):
    model = models.get_model(app_label,modname)
    field = model._meta.get_field_by_name(fldname)
    rpt = field._lino_choices_report
    #kw['colname'] = request.POST['colname']
    return json_report_view_(request,rpt,**kw)
    
def grid_afteredit_view(request,**kw):
    kw['colname'] = request.POST['colname']
    kw['submit'] = True
    return json_report_view(request,**kw)

def form_submit_view(request,**kw):
    kw['submit'] = True
    return json_report_view(request,**kw)

def list_report_view(request,**kw):
    #kw['simple_list'] = True
    return json_report_view(request,**kw)
    
    
def json_report_view(request,app_label=None,rptname=None,**kw):
    rpt = actors.get_actor2(app_label,rptname)
    return json_report_view_(request,rpt,**kw)

def json_report_view_(request,rpt,grid_action=None,colname=None,submit=None):
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
    
    window_configs_file = os.path.join(settings.PROJECT_DIR,'window_configs.pck')
                
    def __init__(self):
        #self.StaticText = StaticText
        self.GridElement = GridElement
        self.VirtualFieldElement = VirtualFieldElement
        self.MethodElement = MethodElement
        self.ButtonElement = ButtonElement
        self.Panel = Panel
        self.Store = Store
        self.StaticTextElement = StaticTextElement
        #self.ActionContext = ActionContext
        self.InputElement = InputElement
        self.window_configs = {}
        if os.path.exists(self.window_configs_file):
            lino.log.info("Loading %s...",self.window_configs_file)
            wc = pickle.load(open(self.window_configs_file,"rU"))
            lino.log.debug("  -> %r",wc)
            if type(wc) is dict:
                self.window_configs = wc
        else:
            lino.log.warning("window_configs_file %s not found",self.window_configs_file)
            
    def save_window_configs(self):
        f = open(self.window_configs_file,'wb')
        pickle.dump(self.window_configs,f)
        f.close()
        self._response = None


        
        
    def field2elem(self,lh,field,**kw):
        #~ if isinstance(field,forms.Input):
            #~ return InputElement(lh,name,field)
      
        for cl,x in self._field2elem:
            if isinstance(field,cl):
                return x(lh,field,**kw)
        if True:
            raise NotImplementedError("field %r" % field)
        lino.log.warning("No LayoutElement for %s",field.__class__)
                

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
            (r'^grid_action/(?P<app_label>\w+)/(?P<rptname>\w+)/(?P<grid_action>\w+)$', json_report_view),
            (r'^submit/(?P<app_label>\w+)/(?P<rptname>\w+)$', form_submit_view),
            (r'^grid_afteredit/(?P<app_label>\w+)/(?P<rptname>\w+)$', grid_afteredit_view),
            (r'^form/(?P<app_label>\w+)/(?P<actor>\w+)/(?P<action>\w+)$', act_view),
            (r'^form/(?P<app_label>\w+)/(?P<actor>\w+)$', act_view),
            (r'^action/(?P<app_label>\w+)/(?P<actor>\w+)$', act_view),
            (r'^choices/(?P<app_label>\w+)/(?P<modname>\w+)/(?P<fldname>\w+)$', choices_view),
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
        url = "/form/" + a.app_label + "/" + a.name + "/" + btn.name
        if len(kw):
            url += "?" + urlencode(kw)
        return url
        
    def get_report_url(self,rh,master_instance=None,
            submit=False,grid_afteredit=False,grid_action=None,run=False,**kw):
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
        
    def layout2kw(self,lh,**kw):
        name = id2js(lh.name)
        kw.update(title=lh.get_title(self))
        #kw.update(closeAction='hide')
        kw.update(maximizable=True)
        kw.update(id=name)
        url = '/save_win/' + name
        js = 'Lino.save_window_config(this,%r)' % url
        kw.update(tools=[dict(id='save',handler=js_code(js))])
        kw.update(layout='fit')
        kw.update(items=lh._main)
        # if lh.layout.default_element is not None:
        #     kw.update(defaultButton=lh.layout.default_element)
        wc = self.window_configs.get(name,None)
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
        kw = self.layout2kw(lh,**kw)
        
        def js_lines():
        
            yield "function(caller) {"
            for nrh in lh._needed_stores:
                for ln in nrh.store.js_lines():
                    yield "  " + ln
            for ln in lh._main.js_lines():
                yield "  " + ln
                
            yield "  this.window = new Ext.Window( %s );" % py2js(kw)
            yield "  this.stop = function() {"
            yield "     this.window.close();"
            yield "  }"
            
                
            if isinstance(lh._main,DetailMainPanel):
                yield "  var sels = caller.main_grid.getSelectionModel().getSelections()"
                yield "  if(sels.length > 0) this.load_record(sels[0]);"
                
            if isinstance(lh._main,GridMainPanel):
                yield "  var grid = this.main_grid;"
                yield "  var store = grid.getStore();"
                if lh.link.report.master is None:
                    yield "  store.load();" 
                else:
                    master_type = ContentType.objects.get_for_model(lh.link.report.model).pk
                    yield "  if (caller) {"
                    yield "    caller.main_grid.getSelectionModel().addListener('rowselect',"
                    yield "      function(sm,rowIndex,record) { "
                    yield "        var p = { %s:record.id, %s:%r };" % (
                      URL_PARAM_MASTER_PK,URL_PARAM_MASTER_TYPE,master_type)
                    # yield "      console.log('on_rowselect',this,p);"
                    yield "        store.load({params:p});" 
                    yield "    })"
                    yield "  } else {"
                    if rr.master_instance is None:
                        mpk = None
                    else:
                        mpk = rr.master_instance.pk
                    yield "    store.load({params:{ %s:%r, %s:%r }});" % (
                      URL_PARAM_MASTER_PK,mpk,URL_PARAM_MASTER_TYPE,master_type)
                    yield "  }"
                  
                    # der folgende fall ist noch nicht uebernommen:
                    #~ yield "    if(master) {"
                    #~ yield "      %s.setBaseParam(%r,master);" % (self.store.as_ext(),URL_PARAM_MASTER_PK)
                    #~ yield "      %s.load();" % self.store.as_ext()
                    
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
            yield "  if (caller) {"
            yield "    caller.window.on('close',function() {"
            yield "      console.log('close',caller,this);"
            yield "      this.stop();"
            yield "    },this);"
            yield "  }"
            yield "  this.window.show();"
            yield "  this.window.focus();"
            yield "}"
            
        context.response.update(call=js_lines)
        
    def view_form(self,context,**kw):
        frm = context.actor
        # called from Form.run()
        fh = self.get_form_handle(frm)
        #fh.setup()
        lh = fh.lh
        kw = self.layout2kw(lh,**kw)
        name = id2js(lh.name)
        def js_lines():
            yield "function(caller) {" 
            for ln in lh._main.js_lines():
                yield "  " + ln
            yield "  this.comp = new Ext.Window( %s );" % py2js(kw)
            yield "  this.get_values = function() {"
            yield "    var v = {};"
            for e in fh.inputs:
                yield "    v[%r] = this.main_panel.getForm().findField(%r).getValue();" % (e.name,e.name)
            yield "    return v;"
            yield "  };"
            yield "  this.stop = function() {"
            yield "     this.comp.close();"
            yield "  }"
            yield "  this.comp.show();"
            yield "}"
      
        context.response.update(call=js_lines)
            
    
ui = ExtUI()


