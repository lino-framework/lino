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
from django.utils.translation import ugettext as _

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
        
    def parse_form_value(self,v):
        return self.field.to_python(v)
        
    def obj2json(self,obj,d):
        #d[self.field.name] = getattr(obj,self.field.name)
        #v = getattr(obj,self.field.name)
        #d[self.field.name] = self.field.value_to_string(obj)
        try:
            d[self.field.name] = self.field.value_from_object(obj)
        except ValueError,e:
            print obj.__class__, self.field.name, e
            lino.log.exception(e)

    def form2obj(self,instance,post_data):
        v = post_data.get(self.field.name,None)
        #~ if v == '' and self.field.null:
            #~ v = None
        if v is None:
            return
        v = self.parse_form_value(v)
        if self.field.primary_key and instance.pk is not None:
            if instance.pk == v:
                return
            raise exceptions.ValidationError({self.field.name:_("Primary key %r may not be modified.") % instance.pk})
        try:
            setattr(instance,self.field.name,v)
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
        
    def parse_form_value(self,v):
        if v in ('true','on'):
            return True
        if v in ('false','off'):
            return False
        return None
        
        
    #~ def form2obj(self,instance,post_data):
        #~ v = post_data.get(self.field.name,None)
        #~ if v is None:
            #~ return
        #~ if v in ('true','on'):
            #~ v = True
        #~ else:
            #~ v = False
        #~ setattr(instance,self.field.name,v)
        
        

class DateStoreField(StoreField):
  
    def __init__(self,field,date_format,**kw):
        self.date_format = date_format
        kw['type'] = 'date'
        StoreField.__init__(self,field,**kw)
        
    def unused_obj2json(self,obj,d): # date conversion done by py2js
        value = getattr(obj,self.field.name)
        if value is not None:
            value = value.strftime(self.date_format)
            #~ value = value.ctime() # strftime('%Y-%m-%d')
            #print value
            d[self.field.name] = value
            
    def parse_form_value(self,v):
        return dateparser.parse(v,fuzzy=True)


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
        
class ChoicesStoreField(StoreField):
  
    def as_js(self):
        s = StoreField.as_js(self)
        s += "," + repr(self.field.name+ext_requests.CHOICES_HIDDEN_SUFFIX)
        return s 
        
    def get_value_text(self,obj):
        v = getattr(obj,self.field.name)
        if v is None or v == '':
            return (None, None)
        else:
            for i in self.field.choices:
                if i[0] == v:
                    return (v, unicode(i[1]))
            return (v, _("%r (invalid choice)") % v)
        
    def form2obj(self,instance,post_data):
        assert not self.field.primary_key
        v = post_data.get(self.field.name+ext_requests.CHOICES_HIDDEN_SUFFIX,None)
        if v is None:
            return
        if v in ('','undefined'): 
            v = None
        if v is not None:
            v = self.parse_form_value(v)
        setattr(instance,self.field.name,v)


    def obj2json(self,obj,d):
        value,text = self.get_value_text(obj)
        d[self.field.name+ext_requests.CHOICES_HIDDEN_SUFFIX] = value
        d[self.field.name] = text
        
        
class ForeignKeyStoreField(ChoicesStoreField):
        
    def get_value_text(self,obj):
        try:
            v = getattr(obj,self.field.name)
        except self.field.rel.to.DoesNotExist,e:
            v = None
        if v is None:
            return (None, None)
        else:
            return (v.pk, unicode(v))
            
    def parse_form_value(self,v):
        try:
            return self.field.rel.to.objects.get(pk=v)
        except self.field.rel.to.DoesNotExist,e:
            return None
            



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
        if isinstance(fld,models.OneToOneField):
            return OneToOneStoreField(fld)
        if isinstance(fld,models.ForeignKey):
            return ForeignKeyStoreField(fld)
        if isinstance(fld,models.DateField):
            return DateStoreField(fld,self.report.date_format)
        if isinstance(fld,models.BooleanField):
            return BooleanStoreField(fld)
        kw = {}
        if isinstance(fld,models.SmallIntegerField):
            kw.update(type='int')
        if isinstance(fld,models.IntegerField):
            kw.update(type='int')
        if isinstance(fld,models.AutoField):
            kw.update(type='int')
        if fld.choices:
            return ChoicesStoreField(fld,**kw)
        else:
            return StoreField(fld,**kw)

      
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
        url = "/".join(("/api",self.rh.report.app_label,self.rh.report._actor_name+'.json'))
        proxy = dict(url=url,method='GET')
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
            try:
                f.form2obj(instance,form_values)
            except exceptions.ValidationError,e:
                raise exceptions.ValidationError({f.field.name:e})
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
            #~ if not f.field.primary_key:
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
            
            
        
