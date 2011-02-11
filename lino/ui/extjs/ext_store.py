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

import logging
logger = logging.getLogger(__name__)

import datetime
#~ from dateutil import parser as dateparser

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
  
    form2obj_default = None
    "because checkboxes are not submitted when they are off"
    
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
        
    def column_names(self):
        yield self.options['name']
        
    def parse_form_value(self,v):
        #~ if self.field.blank and v == '':
            #~ return None
        return self.field.to_python(v)
        
    def value_from_object(self,request,obj):
        return self.field.value_from_object(obj)
        
    def obj2list(self,request,obj):
        return [self.value_from_object(request,obj)]
        
    def obj2dict(self,request,obj,d):
        d[self.field.name] = self.value_from_object(request,obj)

    def form2obj(self,instance,post_data,is_new):
        v = post_data.get(self.field.name,self.form2obj_default)
        if v is None:
            return
        if v == '' and self.field.null:
            # e.g. id field may be empty
            # but don't do this for charfields with blank=True (and not null=True)
            v = None
        v = self.parse_form_value(v)
        if not is_new and self.field.primary_key and instance.pk is not None:
            if instance.pk == v:
                return
            raise exceptions.ValidationError({
              self.field.name:_("Existing primary key value %r may not be modified.") % instance.pk})
        setattr(instance,self.field.name,v)
        #~ try:
            #~ setattr(instance,self.field.name,v)
        #~ except exceptions.ValidationError,e:
            #~ logger.exception("%s = %r : %s",self.field.name,v,e)
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

    def form2obj(self,instance,post_data,is_new):
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
  
    form2obj_default = 'off'
    
    def __init__(self,field,**kw):
        kw['type'] = 'boolean'
        StoreField.__init__(self,field,**kw)
        
    def parse_form_value(self,v):
        if v in ('true','on'):
            return True
        if v in ('false','off'):
            return False
        raise Exception("Got invalid form value %r for %s" % (v,self.field.name))


class AutoStoreField(StoreField):
    def __init__(self,field,**kw):
        kw['type'] = 'int'
        StoreField.__init__(self,field,**kw)
  
    def form2obj(self,instance,post_data,is_new):
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
    #~ def __init__(self,field,**kw):
        #~ self.date_format = date_format
        kw['type'] = 'date'
        kw['dateFormat'] = date_format # 'Y-m-d'
        StoreField.__init__(self,field,**kw)
        
    def parse_form_value(self,v):
        #~ print '20101024 DateStoreField 1', v
        if v:
            v = reports.parse_js_date(v,self.field.name)
            #~ v = dateparser.parse(v,fuzzy=True)
            #~ ? v = datetime.date(v.year,v.month,v.day)
        else:
            v = None
        #~ print '20101024 DateStoreField 2', v
        return v


class FileFieldStoreField(StoreField):
  
    def value_from_object(self,request,obj):
        ff = self.field.value_from_object(obj)
        return ff.name
        
class MethodStoreField(StoreField):
  
    def value_from_object(self,request,obj):
        unbound_meth = self.field._return_type_for_method
        assert unbound_meth.func_code.co_argcount == 2, (self.field.name, unbound_meth.func_code.co_varnames)
        #~ print self.field.name
        return unbound_meth(obj,request)
        
    def obj2list(self,request,obj):
        return [self.value_from_object(request,obj)]
        
    def obj2dict(self,request,obj,d):
        #~ logger.debug('MethodStoreField.obj2dict() %s',self.field.name)
        d[self.field.name] = self.value_from_object(request,obj)
        
    def get_from_form(self,instance,post_data):
        pass
        
    def form2obj(self,instance,post_data,is_new):
        pass
        #raise Exception("Cannot update a virtual field")

#~ class SlaveSummaryField(MethodStoreField):
  
    #~ def obj2dict(self,request,obj,d):
        #~ meth = getattr(obj,self.field.name)
        #~ #logger.debug('MethodStoreField.obj2dict() %s',self.field.name)
        #~ d[self.field.name] = self.slave_report.()

class OneToOneStoreField(StoreField):
        
    def form2obj(self,instance,post_data,is_new):
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
        
    def column_names(self):
        yield self.options['name']
        yield self.options['name'] + ext_requests.CHOICES_HIDDEN_SUFFIX
        
    def form2obj(self,instance,post_data,is_new):
        assert not self.field.primary_key
        v = post_data.get(self.field.name+ext_requests.CHOICES_HIDDEN_SUFFIX,None)
        if v is None:
            return
        if v in ('','undefined'): 
            v = None
        if v is not None:
            v = self.parse_form_value(v)
        if v is None:
            if not self.field.blank:
                raise exceptions.ValidationError("field may not be empty")
                #~ raise exceptions.ValidationError({self.field.name: "field may not be empty"})
                #~ print "20101021 cannot set empty value for", self.field.name
                #~ return # 20101021
            if not self.field.null:
                """field is blank but will be set by full_clean. 
                Django refuses to explicitly assign None to a non-nullable field.
                """
                return
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
          
        fields = []
        list_fields = self.collect_fields(fields,rh.get_list_layout())
        detail_fields = self.collect_fields(fields,*rh.get_detail_layouts())
        
        self.fields = []
        self.list_fields = []
        self.detail_fields = []
        
        #~ for df in list_fields | detail_fields: # set union
        for df in fields: 
            sf = self.create_field(df)
            if sf:
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
            self.fields.append(sf)
            self.list_fields.append(sf)
            self.detail_fields.append(sf)
        #~ self.fields.append(PropertiesStoreField)
        #~ self.fields_dict = dict([(f.field.name,f) for f in self.fields])
        
        self.fields = tuple(self.fields)
        self.list_fields = tuple(self.list_fields)
        self.detail_fields = tuple(self.detail_fields)
        
          
    def collect_fields(self,all_fields,*layouts):
        #~ fields = set()
        fields = []
        def add(f):
            fields.append(f)
            if f not in all_fields:
                all_fields.append(f)
        for layout in layouts:
            for fld in layout._store_fields:
                assert fld is not None
                add(fld)
                #~ fields.add(fld)
        if not self.pk in fields:
            #~ fields.add(self.pk)
            add(self.pk)
        return fields
        
    def create_field(self,fld):
        meth = getattr(fld,'_return_type_for_method',None)
        if meth is not None:
            # uh, this is tricky...
            return MethodStoreField(fld)
        #~ if isinstance(fld,fields.HtmlBox):
            #~ ...
        if isinstance(fld,models.FileField):
            return FileFieldStoreField(fld)
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
        if choosers.uses_simple_values(fld):
            return StoreField(fld,**kw)
        else:
            return ComboStoreField(fld,**kw)

    def form2obj(self,form_values,instance,is_new):
        for f in self.fields:
            try:
                f.form2obj(instance,form_values,is_new)
            #~ except exceptions.ValidationError,e:
            except Exception,e:
                raise exceptions.ValidationError({f.field.name:e})
            
    def row2list(self,request,row):
        assert isinstance(request,reports.ReportActionRequest)
        l = []
        for fld in self.list_fields:
            l += fld.obj2list(request,row)
        return l
      
    def column_names(self):
        l = []
        for fld in self.list_fields:
            l += fld.column_names()
        return l
        

    def row2dict(self,request,row):
        assert isinstance(request,reports.ReportActionRequest)
        d = {}
        for f in self.detail_fields:
            f.obj2dict(request,row,d)
        return d

            
