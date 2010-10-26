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
"""

Defines the `Store` class and its fields 

"""

from dateutil import parser as dateparser

from django.db import models
from django.core import exceptions
from django.utils.translation import ugettext as _

from lino.utils import jsgen 
from lino.utils.jsgen import py2js, Component, id2js, js_code
from . import ext_requests

import lino
from lino import reports
#~ from lino.modlib.properties import models as properties
from lino.utils import choosers

class StoreField(object):
  
    list_values_count = 1
    "Necessary to compute :attr:`Store.pk_index`."
    
    def __init__(self,field,**options):
        self.field = field
        options['name'] = field.name
        self.options = options
        
    def __repr__(self):
        return self.__class__.__name__ + ' ' + self.field.name
        
    def as_js(self):
        return py2js(self.options)
        
    def parse_form_value(self,v):
        return self.field.to_python(v)
        
    def obj2list(self,request,obj):
        return [self.field.value_from_object(obj)]
        
    def obj2dict(self,request,obj,d):
        if True:
            d[self.field.name] = self.field.value_from_object(obj)
        else:
            try:
                d[self.field.name] = self.field.value_from_object(obj)
            except ValueError,e:
                lino.log.exception(e)

    def form2obj(self,instance,post_data):
        v = post_data.get(self.field.name,None)
        if v is None:
            return
        #~ if v == '': # and self.field.null:
            #~ # e.g. id field may be empty
            #~ v = None
        v = self.parse_form_value(v)
        if self.field.primary_key and instance.pk:
            if instance.pk == v:
                return
            raise exceptions.ValidationError({
              self.field.name:_("Existing primary key value %r may not be modified.") % instance.pk})
        setattr(instance,self.field.name,v)
        #~ try:
            #~ setattr(instance,self.field.name,v)
        #~ except exceptions.ValidationError,e:
            #~ lino.log.exception("%s = %r : %s",self.field.name,v,e)
            #~ raise 

class DisabledFieldsStoreField(StoreField):
    """
    See :doc:`/blog/2010/0803`
    """
    def __init__(self,store):
        self.options = dict(name='disabled_fields')
        self.store = store
        #~ self.report = report
        
    def parse_form_value(self,v):
        pass
        
    def value_from_object(self,request,obj):
        l = [ f.name for f in self.store.report.disabled_fields(request,obj)]
        if obj.pk is not None:
            l.append(self.store.pk.name)
        return l
        
    def obj2list(self,request,obj):
        return [self.value_from_object(request,obj)]
      
    def obj2dict(self,request,obj,d):
        d.update(disabled_fields=self.value_from_object(request,obj))

    def form2obj(self,instance,post_data):
        pass

        
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
        
class AutoStoreField(StoreField):
    def __init__(self,field,**kw):
        kw['type'] = 'int'
        StoreField.__init__(self,field,**kw)
  
    def form2obj(self,instance,post_data):
        pass
        
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
        
    def unused_obj2dict(self,request,obj,d): # date conversion done by py2js
        value = getattr(obj,self.field.name)
        if value is not None:
            value = value.strftime(self.date_format)
            #~ value = value.ctime() # strftime('%Y-%m-%d')
            #print value
            d[self.field.name] = value
            
    def parse_form_value(self,v):
        #~ print '20101024 DateStoreField 1', v
        if v:
            v = dateparser.parse(v,fuzzy=True)
        else:
            v = None
        #~ print '20101024 DateStoreField 2', v
        return v


class MethodStoreField(StoreField):
  
    def value_from_object(self,request,obj):
        unbound_meth = self.field._return_type_for_method
        return unbound_meth(obj)
        
    def obj2list(self,request,obj):
        return [self.value_from_object(request,obj)]
        
    def obj2dict(self,request,obj,d):
        #~ lino.log.debug('MethodStoreField.obj2dict() %s',self.field.name)
        d[self.field.name] = self.value_from_object(request,obj)
        
    def get_from_form(self,instance,post_data):
        pass
        
    def form2obj(self,instance,post_data):
        pass
        #raise Exception("Cannot update a virtual field")

#~ class SlaveSummaryField(MethodStoreField):
  
    #~ def obj2dict(self,request,obj,d):
        #~ meth = getattr(obj,self.field.name)
        #~ #lino.log.debug('MethodStoreField.obj2dict() %s',self.field.name)
        #~ d[self.field.name] = self.slave_report.()

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
        
    def value_from_object(self,request,obj):
        try:
            v = getattr(obj,self.field.name)
        except self.field.rel.to.DoesNotExist,e:
            v = None
        if v is None:
            return None
        return v.pk
      
    def obj2list(self,request,obj):
        return [self.value_from_object(request,obj)]
        
    def obj2dict(self,request,obj,d):
        d[self.field.name] = self.value_from_object(request,obj)
        
class ComboStoreField(StoreField):
  
    list_values_count = 2
    
    def as_js(self):
        s = StoreField.as_js(self)
        s += "," + repr(self.field.name+ext_requests.CHOICES_HIDDEN_SUFFIX)
        return s 
        
    def form2obj(self,instance,post_data):
        assert not self.field.primary_key
        v = post_data.get(self.field.name+ext_requests.CHOICES_HIDDEN_SUFFIX,None)
        if v is None:
            return
        if v in ('','undefined'): 
            v = None
        if v is None:
            if not self.field.blank:
                raise exceptions.ValidationError("field may not be empty")
                #~ raise exceptions.ValidationError({self.field.name: "field may not be empty"})
                #~ print "20101021 cannot set empty value for", self.field.name
                #~ return # 20101021
        else:
            v = self.parse_form_value(v)
        setattr(instance,self.field.name,v)

    def obj2list(self,request,obj):
        value,text = self.get_value_text(obj)
        return [text,value]
        
    def obj2dict(self,request,obj,d):
        value,text = self.get_value_text(obj)
        d[self.field.name] = text
        d[self.field.name+ext_requests.CHOICES_HIDDEN_SUFFIX] = value
        
    def get_value_text(self,obj):
        v = getattr(obj,self.field.name)
        if v is None or v == '':
            return (None, None)
        ch = choosers.get_for_field(self.field) 
        if ch is not None:
            return (v, ch.get_text_for_value(v,obj))
        for i in self.field.choices:
            if i[0] == v:
                return (v, unicode(i[1]))
        return (v, _("%r (invalid choice)") % v)
        
class ForeignKeyStoreField(ComboStoreField):
        
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
            

#~ class ChoicesStoreField(ComboStoreField):
  
    #~ def get_value_text(self,obj):
        #~ v = getattr(obj,self.field.name)
        #~ if v is None or v == '':
            #~ return (None, None)
        #~ for i in self.field.choices:
            #~ if i[0] == v:
                #~ return (v, unicode(i[1]))
        #~ return (v, _("%r (invalid choice)") % v)
        
#~ class ChooserStoreField(ComboStoreField):
    #~ """
    #~ This will be used only for non-fk fields with chooser; 
    #~ ForeignKey fields will get a ForeignKeyStoreField even if they have a chooser.
    #~ """
  


class Store:
    """
    
    Represents an :extjs:`Ext.data.JsonStore`.
    
    """
    #declare_type = jsgen.DECLARE_THIS
    #~ declare_type = jsgen.DECLARE_VAR
    #~ declare_type = jsgen.DECLARE_INLINE
    #~ ext_suffix = "_store"
    #~ value_template = "new Ext.data.JsonStore(%s)"
    
    def __init__(self,rh,**options):
        assert isinstance(rh,reports.ReportHandle)
        #~ Component.__init__(self,id2js(rh.report.actor_id),**options)
        self.rh = rh
        self.report = rh.report
        self.pk = self.report.model._meta.pk
        assert self.pk is not None, "Cannot make Store for %s because %s has no pk" % (
          self.report.actor_id,self.report.model)
        
        list_fields = self.collect_fields(rh.get_list_layout())
        detail_fields = self.collect_fields(*rh.get_detail_layouts())
        
        self.fields = []
        self.list_fields = []
        self.detail_fields = []
        
        for df in list_fields | detail_fields: # set union
            sf = self.create_field(df)
            self.fields.append(sf)
            if df in list_fields:
                self.list_fields.append(sf)
            if df in detail_fields:
                self.detail_fields.append(sf)
            
        
        #~ fields = list(fields)
        #~ self.pk_index = fields.index(self.pk)
        #~ self.fields = [ self.create_field(fld) for fld in fields ]
        self.pk_index = 0
        for fld in self.list_fields:
            if fld.field == self.pk:
                break
            self.pk_index += fld.list_values_count
        #~ if self.report.actor_id == 'contacts.Persons':
            #~ print 'ext_store 20101017:\n', '\n'.join([str(f) for f in self.fields])
        if rh.report.disabled_fields:
            sf = DisabledFieldsStoreField(self)
            self.list_fields.append(sf)
            self.detail_fields.append(sf)
        #~ self.fields.append(PropertiesStoreField)
        #~ self.fields_dict = dict([(f.field.name,f) for f in self.fields])
          
    def collect_fields(self,*layouts):
        fields = set()
        for layout in layouts:
            for fld in layout._store_fields:
                assert fld is not None
                fields.add(fld)
        if not self.pk in fields:
            fields.add(self.pk)
        return fields
        
    def create_field(self,fld):
        meth = getattr(fld,'_return_type_for_method',None)
        if meth is not None:
            # uh, this is tricky...
            return MethodStoreField(fld)
        #~ if isinstance(fld,fields.HtmlBox):
            #~ ...
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
        if isinstance(fld,models.AutoField):
            return AutoStoreField(fld)
            #~ kw.update(type='int')
        kw = {}
        if isinstance(fld,models.SmallIntegerField):
            kw.update(type='int')
        if isinstance(fld,models.IntegerField):
            kw.update(type='int')
        #~ if fld.choices:
            #~ return ChoicesStoreField(fld,**kw)
        #~ ch = choosers.get_for_field(fld)
        #~ if ch.simple_values:
            #~ return StoreField(fld,**kw)
        #~ else:
            #~ return ChooserStoreField(fld,**kw)
        if choosers.uses_simple_values(fld):
            return StoreField(fld,**kw)
        else:
            return ComboStoreField(fld,**kw)
        #~ if choosers.get_for_field(fld) is not None:
            #~ return ChooserStoreField(fld,**kw)
        #~ else:
            #~ return StoreField(fld,**kw)

      
    def form2obj(self,form_values,instance):
        for f in self.fields:
            try:
                f.form2obj(instance,form_values)
            except exceptions.ValidationError,e:
                raise exceptions.ValidationError({f.field.name:e})
        #~ for p in properties.Property.properties_for_model(instance.__class__):
            #~ p.form2obj(instance,form_values)
            
    def row2list(self,request,row):
        l = []
        for fld in self.list_fields:
            l += fld.obj2list(request,row)
        return l
      

    def row2dict(self,request,row):
        d = {}
        for f in self.detail_fields:
            #~ if not f.field.primary_key:
            f.obj2dict(request,row,d)
        return d

            
    def unused_ext_options(self):
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
        
    def unused_js_after_body(self):
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
            
            
        
