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

from dateutil import parser as dateparser

from django.db import models
from django.core import exceptions

from lino.utils import jsgen 
from lino.utils.jsgen import py2js, Component, id2js, js_code
from lino.ui.extjs import ext_requests

import lino
from lino import reports
from lino.modlib.properties import models as properties


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
        
    def unused_get_from_form(self,instance,post_data):
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

    def form2obj(self,instance,post_data):
        v = post_data.get(self.field.name,None)
        #~ if v == '' and self.field.null:
            #~ v = None
        if v is None:
            return
        #~ if v == '':
            #~ v = self.field.get_default()
        try:
            setattr(instance,self.field.name,self.field.to_python(v))
        except exceptions.ValidationError,e:
            lino.log.exception("%s = %r : %s",self.field.name,v,e)
            raise 

        
#~ class PropertiesStoreField(StoreField):
#~ class PropertyStoreField(StoreField):
    #~ def __init__(self,field,**kw):
        #~ kw['type'] = ...
        #~ StoreField.__init__(self,field,**kw)
    #~ def get_from_form(self,instance,post_data):
        #~ v = post_data.get(self.field.name)
        #~ if v == 'true':
            #~ v = True
        #~ else:
            #~ v = False
        #~ instance[self.field.name] = v
  
class BooleanStoreField(StoreField):
    def __init__(self,field,**kw):
        kw['type'] = 'boolean'
        StoreField.__init__(self,field,**kw)
        
    #~ def get_from_form(self,instance,post_data):
        #~ v = post_data.get(self.field.name)
        #~ if v == 'true':
            #~ v = True
        #~ else:
            #~ v = False
        #~ instance[self.field.name] = v
        
    def form2obj(self,instance,post_data):
        v = post_data.get(self.field.name,None)
        if v is None:
            return
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
        
    def obj2json(self,obj,d):
        value = getattr(obj,self.field.name)
        if value is not None:
            value = value.ctime() # strftime('%Y-%m-%d')
            #print value
            d[self.field.name] = value
            
    #~ def get_from_form(self,instance,post_data):
        #~ v = post_data.get(self.field.name)
        #~ if v == '' and self.field.null:
            #~ v = None
        #~ if v is not None:
            #~ #print v
            #~ v = dateparser.parse(v,fuzzy=True)
        #~ instance[self.field.name] = v

    def form2obj(self,instance,post_data):
        v = post_data.get(self.field.name,None)
        if v is None:
            return
        if v == '' and self.field.null:
            v = None
        if v is not None:
            #print v
            v = dateparser.parse(v,fuzzy=True)
        setattr(instance,self.field.name,v)

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
        
    def form2obj(self,instance,post_data):
        pass
        #raise Exception("Cannot update a virtual field")


class OneToOneStoreField(StoreField):
        
    def form2obj(self,instance,post_data):
        #v = values.get(self.field.name,None)
        v = post_data.get(self.field.name,None)
        if v == '' and self.field.null:
            v = None
        if v is not None:
            v = self.field.rel.to.objects.get(pk=v)
        setattr(instance,self.field.name,v)
        
    #~ def get_from_form(self,instance,post_data):
        #~ #v = values.get(self.field.name,None)
        #~ v = post_data.get(self.field.name)
        #~ if v == '' and self.field.null:
            #~ v = None
        #~ if v is not None:
            #~ v = self.field.rel.to.objects.get(pk=v)
        #~ instance[self.field.name] = v
        
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
        s += "," + repr(self.field.name+ext_requests.CHOICES_HIDDEN_SUFFIX)
        return s 
        
    #~ def get_from_form(self,instance,post_data):
        #~ #v = post_data.get(self.name,None)
        #~ #v = post_data.get(self.field.name+"Hidden",None)
        #~ v = post_data.get(self.field.name+ext_requests.CHOICES_HIDDEN_SUFFIX)
        #~ #print self.field.name,"=","%s.objects.get(pk=%r)" % (self.model.__name__,v)
        #~ #v = post_data.getlist(self.field.name)
        #~ #print "%s=%r" % (self.field.name, v)
        #~ if v in ('','undefined'): # and self.field.null:
            #~ v = None
        #~ if v is not None:
            #~ try:
                #~ v = self.field.rel.to.objects.get(pk=v)
            #~ except self.field.rel.to.DoesNotExist,e:
                #~ #print "[get_from_form]", v, values.get(self.field.name)
                #~ # lino.log.debug("[%r,%r] : %s",v,text,e)
                #~ v = None
        #~ instance[self.field.name] = v
        
    def form2obj(self,instance,post_data):
        #v = post_data.get(self.name,None)
        #v = post_data.get(self.field.name+"Hidden",None)
        v = post_data.get(self.field.name+ext_requests.CHOICES_HIDDEN_SUFFIX,None)
        if v is None:
            return
        #print self.field.name,"=","%s.objects.get(pk=%r)" % (self.model.__name__,v)
        #v = post_data.getlist(self.field.name)
        #print "%s=%r" % (self.field.name, v)
        if v in ('','undefined'): # and self.field.null:
            v = None
        if v is not None:
            try:
                v = self.field.rel.to.objects.get(pk=v)
            except self.field.rel.to.DoesNotExist,e:
                #print "[get_from_form]", v, values.get(self.field.name)
                # lino.log.debug("[%r,%r] : %s",v,text,e)
                v = None
        setattr(instance,self.field.name,v)


    def obj2json(self,obj,d):
        try:
            v = getattr(obj,self.field.name)
        except self.field.rel.to.DoesNotExist,e:
            v = None
        if v is None:
            #~ d[self.field.name+ext_requests.CHOICES_HIDDEN_SUFFIX] = ''
            #~ d[self.field.name] = ''
            d[self.field.name+ext_requests.CHOICES_HIDDEN_SUFFIX] = None
            d[self.field.name] = None
        else:
            d[self.field.name+ext_requests.CHOICES_HIDDEN_SUFFIX] = v.pk
            d[self.field.name] = unicode(v)
        



class Store(Component):
    #declare_type = jsgen.DECLARE_THIS
    #~ declare_type = jsgen.DECLARE_VAR
    declare_type = jsgen.DECLARE_INLINE
    ext_suffix = "_store"
    value_template = "new Ext.data.JsonStore(%s)"
    
    def __init__(self,rh,**options):
        assert isinstance(rh,reports.ReportHandle)
        Component.__init__(self,id2js(rh.report.actor_id),**options)
        self.rh = rh
        self.report = rh.report
        fields = set()
        for layout in rh.get_used_layouts():
            for fld in layout._store_fields:
                assert fld is not None
                fields.add(fld)
        self.pk = self.report.model._meta.pk
        assert self.pk is not None, "Cannot make Store for %s because %s has no pk" % (
          self.report.actor_id,self.report.model)
        if not self.pk in fields:
            fields.add(self.pk)
        self.fields = [ self.create_field(fld) for fld in fields ]
        #~ self.fields.append(PropertiesStoreField)
        #~ self.fields_dict = dict([(f.field.name,f) for f in self.fields])
          
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
        
    def unused_get_from_form(self,post_values):
        instance = {}
        for f in self.fields:
            if not f.field.primary_key:
                f.get_from_form(instance,post_values)
        return instance
        
    def form2obj(self,form_values,instance):
        for f in self.fields:
            f.form2obj(instance,form_values)
        for p in properties.Property.properties_for_model(instance.__class__):
            p.form2obj(instance,form_values)
            
    def unused_get_from_form(self,form_values):
        instance = {}
        for k,v in form_values.items():
            if k.startswith('property_'):
                name = k[9:]
                print "TODO: get property %r from form" % name
            else:
                f = self.fields_dict.get(k,None)
                if f is None:
                    pass
                else:
                    f.get_from_form(instance,form_values)
        return instance

    def row2dict(self,row):
        d = {}
        for f in self.fields:
            if not f.field.primary_key:
                f.obj2json(row,d)
        return d

    #~ def js_declare(self):
        #~ for ln in Component.js_declare(self):
            #~ yield ln
            
    def js_after_body(self):
        for ln in Component.js_after_body(self):
            yield ln
        if self.report.master is None:
            yield "%s.load();" % self.as_ext()
        else:
            yield "if (caller) {"
            yield "caller.main_grid.add_row_listener("
            yield "  function(sm,rowIndex,record) { Lino.load_master(%s,caller,record)})" % self.as_ext()
            yield "Lino.load_master(%s,caller,caller.get_current_record());" % self.as_ext()
            yield "} else %s.load();" % self.as_ext()
            
            
        
