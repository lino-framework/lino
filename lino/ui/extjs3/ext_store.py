## Copyright 2009-2011 Luc Saffre
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

from django.conf import settings
from django.db import models
from django.db.models.fields import NOT_PROVIDED
from django.core import exceptions
from django.utils.translation import ugettext as _
from django.contrib.contenttypes import generic

from lino.utils import jsgen 
from lino.utils.jsgen import py2js, Component, id2js, js_code
#~ from . import ext_requests
from lino.ui import requests as ext_requests

import lino
from lino import reports
from lino import fields
#~ from lino.modlib.properties import models as properties
from lino.utils import choosers
from lino.tools import obj2str
from lino.utils import IncompleteDate

class StoreField(object):
    """
    Base class for the fields of a :class:`Store`.
    """
    form2obj_default = None
    "because checkboxes are not submitted when they are off"
    
    list_values_count = 1
    "Necessary to compute :attr:`Store.pk_index`."
    
    def __init__(self,field,**options):
        self.field = field
        options.update(name=field.name)
        self.options = options
        
    #~ def __repr__(self):
        #~ return self.__class__.__name__ + ' ' + self.field.name
        
    def as_js(self):
        return py2js(self.options)
        
    def column_names(self):
        yield self.options['name']
        
    def value_from_object(self,request,obj):
        #~ if not hasattr(self.field,'value_from_object'):
            #~ raise Exception('%s %s has no method value_from_object?!'%(
              #~ self.field,self.field.name))
        return self.field.value_from_object(obj)
        
    def obj2list(self,request,obj):
        return [self.value_from_object(request,obj)]
        
    def obj2dict(self,request,obj,d):
        d[self.field.name] = self.value_from_object(request,obj)

    def parse_form_value(self,v,obj):
        #~ if v == '' and not self.field.empty_strings_allowed:
            #~ return None
        return self.field.to_python(v)
        
    def extract_form_data(self,post_data):
        return post_data.get(self.field.name,None)
        #~ v = post_data.get(self.field.name,self.form2obj_default)
        #~ if v is None:
            #~ # means that the field wasn't part of the submitted form. don't touch it.
            #~ # except for checkboxes (who unfortunately are not submitted when clear)
            #~ # whose form2obj_default is False instead of None
            #~ return
    #~ v = post_data.get(self.field.name,NOT_PROVIDED)
    #~ if v is NOT_PROVIDED:
        #~ return
        
    def form2obj(self,request,instance,post_data,is_new):
        """
        Test cases:
        - setting a CharField to ''
        - sales.Invoice.number may be blank        
        """
        v = self.extract_form_data(post_data)
        if v is None:
            # means that the field wasn't part of the submitted form. don't touch it.
            return
        if v == '' and not self.field.empty_strings_allowed:
            v = self.form2obj_default
            # the following was wrong: if a field has been posted with empty string, 
            # we don't want it to get the default value! 
            # otherwise checkboxes with default value True can never be unset!
            # charfields have empty_strings_allowed
            # e.g. id field may be empty
            # but don't do this for other cases
            #~ if self.field.default is NOT_PROVIDED:
                #~ v = self.form2obj_default
            #~ else:
                #~ v = self.field.default
        else:
            v = self.parse_form_value(v,instance)
        if not is_new and self.field.primary_key and instance.pk is not None:
            if instance.pk == v:
                return
            raise exceptions.ValidationError({
              self.field.name:_("Existing primary key value %r may not be modified.") % instance.pk})
              
        self.set_value_in_object(request,instance,v)
        #~ print 20110524, __file__, self.field.name, v
        #~ try:
            #~ setattr(instance,self.field.name,v)
        #~ except exceptions.ValidationError,e:
            #~ logger.exception("%s = %r : %s",self.field.name,v,e)
            #~ raise 
        return
        
    def set_value_in_object(self,request,instance,v):
        old_value = self.value_from_object(request,instance)
        #~ old_value = getattr(instance,self.field.attname)
        if old_value != v:
            setattr(instance,self.field.name,v)
            m = getattr(instance,self.field.name + "_changed",None)
            if m is not None:
                m(old_value)


class ComboStoreField(StoreField):
  
    list_values_count = 2
    
    def as_js(self):
        s = StoreField.as_js(self)
        s += "," + repr(self.field.name+ext_requests.CHOICES_HIDDEN_SUFFIX)
        return s 
        
    def column_names(self):
        yield self.options['name']
        yield self.options['name'] + ext_requests.CHOICES_HIDDEN_SUFFIX
        
    def extract_form_data(self,post_data):
        return post_data.get(self.field.name+ext_requests.CHOICES_HIDDEN_SUFFIX,None)
        
    def unused_form2obj(self,request,instance,post_data,is_new):
        assert not self.field.primary_key
        v = post_data.get(self.field.name+ext_requests.CHOICES_HIDDEN_SUFFIX,None)
        #~ logger.info("ComboStoreField.form2obj %s = %r", self.field.name,v)
        if v is None:
            return 
        if v in ('','undefined'): 
            v = None
        if v is not None:
            v = self.parse_form_value(v,instance)
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
        self.set_value_in_object(request,instance,v)
        #~ setattr(instance,self.field.name,v)

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
        
    def get_rel_to(self,obj):
        return self.field.rel.to
        
    def get_value_text(self,obj):
        relto_model = self.get_rel_to(obj)
        if not relto_model:
            logger.info("20111213 ForeignKeyStoreField.get_value_text: no relto_model")
            return (None, None)
        try:
            v = getattr(obj,self.field.name)
        except relto_model.DoesNotExist,e:
            v = None
        if v is None:
            return (None, None)
        else:
            return (v.pk, unicode(v))
            
    def parse_form_value(self,v,obj):
        relto_model = self.get_rel_to(obj)
        if not relto_model:
            #~ logger.info("20111209 get_value_text: no relto_model")
            return
        try:
            return relto_model.objects.get(pk=v)
        except ValueError,e:
            pass
        except relto_model.DoesNotExist,e:
            pass
            
        ch = choosers.get_for_field(self.field)
        #~ if ch and ch.meth.quick_insert_field:
        if ch and ch.can_create_choice:
            o = ch.create_choice(obj,v)
            if o is not None:
                logger.info("Auto-created %s %s",o._meta.verbose_name,o)
                return o
            #~ qs = ch.get_instance_choices(obj)
            #~ print 20110425, qs
            #~ kw = {}
            #~ kw[ch.meth.quick_insert_field] = v
            #~ fk_target = qs.create(**kw)
            # fk_target.save() not necessary
            #~ logger.info("Auto-created %s %s",fk_target.__class__,fk_target)
            #~ return fk_target
            #~ return ch.on_quick_insert(obj,self.field,v)
        #~ else:
            #~ logger.info("Could not find %s#%s",relto_model,v)
        return None
            
class LinkedForeignKeyField(ForeignKeyStoreField):
  
    def unused_get_value_text(self,obj):
        v = self.field.link_field.get_value(obj)
        #~ try:
            #~ v = getattr(obj,self.field.name)
        #~ except self.get_rel_to(obj).DoesNotExist,e:
            #~ v = None
        if v is None:
            return (None, None)
        else:
            return (v.pk, unicode(v))
            
    def get_rel_to(self,obj):
        ct = self.field.get_content_type(obj)
        if ct is None:
            return None
        return ct.model_class()
        
    #~ def value_from_object(self,request,obj):
        #~ other = self.field.link_field.get_value(obj,request)
        #~ if other is None: return ''
        #~ return request.ui.href_to(other)
        


class VirtStoreField(StoreField):
  
    def __init__(self,vf,delegate):
        self.vf = vf
        StoreField.__init__(self,vf.return_type)
        #~ for name in (
              #~ 'form2obj_default',
              #~ 'list_values_count', 'as_js', 'column_names',
              #~ 'parse_form_value',
              #~ 'obj2dict','obj2list'
              #~ ):
            #~ setattr(self,name,getattr(delegate,name))
        self.form2obj_default = delegate.form2obj_default
        # as long as http://code.djangoproject.com/ticket/15497 is open:
        self.parse_form_value = delegate.parse_form_value
        self.set_value_in_object = vf.set_value_in_object
        
        #~ self.delegate = delegate

    #~ def __repr__(self):
        #~ return self.__class__.__name__ + '(' + self.delegate.__class__.__name__ + ') ' + self.field.name
        
    def obj2list(self,request,obj):
        return [self.vf.value_from_object(request,obj)]
        
    def obj2dict(self,request,obj,d):
        v = self.vf.value_from_object(request,obj)
        #~ logger.debug('VirtStoreField.obj2dict() %s = %s',self.field.name,v)
        d[self.field.name] = v
        
    def unused_form2obj(self,request,obj,post_data,is_new):
        #~ logger.info("VirtStoreField.form2obj(%s)", post_data)
        v = self.extract_form_data(post_data)
        #~ v = StoreField.form2obj(self,obj,post_data,is_new)
        #~ v = getattr(obj,self.field.name)
        #~ logger.info("VirtStoreField.%s.form2obj(%s) --> %r", self.field.name, post_data, v)
        self.vf.set_value_in_object(request,obj,v)
        #~ return obj







class PasswordStoreField(StoreField):
  
    def value_from_object(self,request,obj):
        v = super(PasswordStoreField,self).value_from_object(request,obj)
        if v:
            return "*" * len(v)
        return v
        
class GenericForeignKeyField(StoreField):
    def value_from_object(self,request,obj):
        owner = getattr(obj,self.field.name)
        if owner is None: return ''
        return request.ui.href_to(owner)
        #~ return "foo"
        #~ if not hasattr(self.field,'value_from_object'):
            #~ raise Exception('%s %s has no method value_from_object?!'%(
              #~ self.field,self.field.name))
        #~ return self.field.value_from_object(obj)
  
class SpecialStoreField(StoreField):
    field = None 
    name = None
  
    def __init__(self,store):
        self.options = dict(name=self.name)
        self.store = store
        
    def obj2dict(self,request,obj,d):
        #~ d.update(disable_editing=self.value_from_object(request,obj))
        d[self.name] = self.value_from_object(request,obj)

    def parse_form_value(self,v,instance):
        pass
        
    def obj2list(self,request,obj):
        return [self.value_from_object(request,obj)]
      
    def form2obj(self,request,instance,post_data,is_new):
        pass
        #~ raise NotImplementedError
        #~ return instance

class DisabledFieldsStoreField(SpecialStoreField):
    """
    See :doc:`/blog/2010/0803`,
    :doc:`/blog/2011/1003`
    """
    name = 'disabled_fields'
    
    def value_from_object(self,request,obj):
        #~ l = [ f.name for f in self.store.report.disabled_fields(request,obj)]
        l = list(self.store.report.disabled_fields(obj,request))
        # if obj is not new (i.e. has a primary key)
        # disabled also the primary key field
        if obj.pk is not None:
            #~ l.append(self.store.pk.name)
            l.append(self.store.pk.attname)
            # MTI children have "two" primary keys:
            if isinstance(self.store.pk,models.OneToOneField):
                l.append(self.store.pk.rel.field_name)
        return l
        
        
class DisableEditingStoreField(SpecialStoreField):
    """
    A field whose value is the result of the `disable_editing` 
    method on that record.
    New feature since :doc:`/blog/2011/0830`
    """
    name = 'disable_editing'
        
    def value_from_object(self,request,obj):
        return self.store.report.disable_editing(obj,request)
        

        
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

#~ from lino.utils.textfields import extract_summary

#~ class TextStoreField(StoreField):
  
    #~ def value_from_object(self,request,obj):
        #~ v = self.field.value_from_object(obj)
        #~ if request.expand_memos:
            #~ return v
        #~ return extract_summary(v)
  
class BooleanStoreField(StoreField):
    """
    This class wouldn't be necessary if Django's 
    `BooleanField.to_python` method would interpret 
    "on" as a valid `True` value. We had some interesting 
    discussion on this in :djangoticket:`#15497 (BooleanField
    should work for all PostgreSQL expressions)<15497>`. 
    """
  
    form2obj_default = False # 'off'
    
    def __init__(self,field,**kw):
        kw['type'] = 'boolean'
        StoreField.__init__(self,field,**kw)
        
    def parse_form_value(self,v,obj):
        #~ print "20110717 parse_form_value", self.field.name, v, obj
        return ext_requests.parse_boolean(v)


class AutoStoreField(StoreField):
    def __init__(self,field,**kw):
        kw['type'] = 'int'
        StoreField.__init__(self,field,**kw)
  
    def form2obj(self,request,instance,post_data,is_new):
        pass
        #~ assert instance.pk
        #~ return instance
        
        
        

class DateStoreField(StoreField):
  
    def __init__(self,field,**kw):
        kw['type'] = 'date'
        kw['dateFormat'] = settings.LINO.date_format_extjs # date_format # 'Y-m-d'
        StoreField.__init__(self,field,**kw)
        
    def parse_form_value(self,v,obj):
        if v:
            v = datetime.date(*settings.LINO.parse_date(v))
        else:
            v = None
        return v
        

class IncompleteDateStoreField(StoreField):
  
    def parse_form_value(self,v,obj):
        if v:
            v = IncompleteDate(*settings.LINO.parse_date(v))
            #~ v = datetime.date(*settings.LINO.parse_date(v))
        return v

class DateTimeStoreField(StoreField):
  
    def parse_form_value(self,v,obj):
        if v:
            return settings.LINO.parse_datetime(v) 
        return None

class TimeStoreField(StoreField):
  
    def parse_form_value(self,v,obj):
        if v:
            return settings.LINO.parse_time(v) 
        return None


class FileFieldStoreField(StoreField):
  
    def value_from_object(self,request,obj):
        ff = self.field.value_from_object(obj)
        return ff.name
        
class MethodStoreField(StoreField):
  
    def value_from_object(self,request,obj):
        unbound_meth = self.field._return_type_for_method
        assert unbound_meth.func_code.co_argcount >= 2, (self.field.name, unbound_meth.func_code.co_varnames)
        #~ print self.field.name
        return unbound_meth(obj,request)
        
    def obj2list(self,request,obj):
        return [self.value_from_object(request,obj)]
        
    def obj2dict(self,request,obj,d):
        #~ logger.debug('MethodStoreField.obj2dict() %s',self.field.name)
        d[self.field.name] = self.value_from_object(request,obj)
        
    #~ def get_from_form(self,instance,post_data):
        #~ pass
        
    def form2obj(self,request,instance,post_data,is_new):
        pass
        #~ return instance
        #raise Exception("Cannot update a virtual field")




#~ class SlaveSummaryField(MethodStoreField):
  
    #~ def obj2dict(self,request,obj,d):
        #~ meth = getattr(obj,self.field.name)
        #~ #logger.debug('MethodStoreField.obj2dict() %s',self.field.name)
        #~ d[self.field.name] = self.slave_report.()

class OneToOneStoreField(StoreField):
        
    def unused_form2obj(self,instance,post_data,is_new):
        #v = values.get(self.field.name,None)
        v = post_data.get(self.field.name,None)
        logger.info("OneToOneStoreField %s = %r",self.field.name,v)
        if v == '' and self.field.null:
            v = None
        if v is not None:
            v = self.field.rel.to.objects.get(pk=v)
        setattr(instance,self.field.name,v)
        #~ return instance
        
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
          
        #~ fields = []
        
        self.df2sf = {}
        self.all_fields = []
        self.list_fields = []
        self.detail_fields = []
        
        self.collect_fields(self.list_fields,rh.get_list_layout())
        dtl = rh.report.get_detail()
        if dtl:
            dh = dtl.get_handle(rh.ui)
            dh.lh_list
            self.collect_fields(self.detail_fields,*dh.lh_list)
        #~ self.collect_fields(self.detail_fields,*rh.get_detail_layouts())
        
        del self.df2sf
        
        #~ for df in list_fields | detail_fields: # set union
        #~ for df in fields: 
            #~ sf = self.create_field(df)
            #~ if sf:
                #~ self.fields.append(sf)
                #~ if df in list_fields:
                    #~ self.list_fields.append(sf)
                #~ if df in detail_fields:
                    #~ self.detail_fields.append(sf)
                    
        #~ fields = list(fields)
        #~ self.pk_index = fields.index(self.pk)
        #~ self.fields = [ self.create_field(fld) for fld in fields ]
        self.pk_index = 0
        for fld in self.list_fields:
            """
            Django's Field.__cmp__() does::
            
              return cmp(self.creation_counter, other.creation_counter) 
              
            which causes an exception when trying to compare a field with an object of other type.
            """
            #~ if type(fld.field) == type(self.pk) and fld.field == self.pk:
            if fld.field.__class__ == self.pk.__class__ and fld.field == self.pk:
                break
            self.pk_index += fld.list_values_count
        #~ if self.report.actor_id == 'contacts.Persons':
            #~ print 'ext_store 20101017:\n', '\n'.join([str(f) for f in self.fields])
            
        def addfield(sf):
            self.all_fields.append(sf)
            self.list_fields.append(sf)
            self.detail_fields.append(sf)
            
        if rh.report.disabled_fields:
            addfield(DisabledFieldsStoreField(self))
            #~ sf = DisabledFieldsStoreField(self)
            #~ self.fields.append(sf)
            #~ self.list_fields.append(sf)
            #~ self.detail_fields.append(sf)
        if rh.report.disable_editing:
            addfield(DisableEditingStoreField(self))
            
        #~ self.fields.append(PropertiesStoreField)
        #~ self.fields_dict = dict([(f.field.name,f) for f in self.fields])
        
        # virtual fields must come last so that Store.form2obj() 
        # processes "real" fields first.
        self.all_fields = [
            f for f in self.all_fields if not isinstance(f,VirtStoreField)
            ] + [
            f for f in self.all_fields if isinstance(f,VirtStoreField)
            ]
        self.all_fields = tuple(self.all_fields)
        self.list_fields = tuple(self.list_fields)
        self.detail_fields = tuple(self.detail_fields)
        
          
    def collect_fields(self,fields,*layouts):
        """
        `fields` is a pointer to either `self.detail_fields`
        or `self.list_fields`.
        The `all_data_fields` set is 
        """
        #~ fields = []
        pk_found = False
        def add(df):
            sf = self.df2sf.get(df,None)
            if sf is None:
                sf = self.create_field(df)
                self.all_fields.append(sf)
                self.df2sf[df] = sf
            fields.append(sf)
            
            if df.primary_key:
                pk_found = True
            #~ if df not in all_data_fields:
                #~ self.all_fields.append(sf)
                #~ all_data_fields.add(df)
                
        for layout in layouts:
            for fld in layout._store_fields:
                assert fld is not None
                add(fld)
                #~ fields.add(fld)
        #~ if not self.pk in fields:
        if not pk_found:
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
        if isinstance(fld,fields.LinkedForeignKey):
            #~ logger.info("Store.create_field(%s)", fld)
            return LinkedForeignKeyField(fld)
        if isinstance(fld,fields.VirtualField):
            delegate = self.create_field(fld.return_type)
            return VirtStoreField(fld,delegate)
        if isinstance(fld,models.FileField):
            return FileFieldStoreField(fld)
        if isinstance(fld,models.ManyToManyField):
            return StoreField(fld)
        if isinstance(fld,fields.PasswordField):
            return PasswordStoreField(fld)
        if isinstance(fld,models.OneToOneField):
            return OneToOneStoreField(fld)
        if isinstance(fld,generic.GenericForeignKey):
            return GenericForeignKeyField(fld)
        if isinstance(fld,fields.GenericForeignKeyIdField):
            return ComboStoreField(fld)
        if isinstance(fld,models.ForeignKey):
            return ForeignKeyStoreField(fld)
        if isinstance(fld,models.TimeField):
            return TimeStoreField(fld)
        if isinstance(fld,models.DateTimeField):
            return DateTimeStoreField(fld)
        if isinstance(fld,fields.IncompleteDateField):
            return IncompleteDateStoreField(fld)
        if isinstance(fld,models.DateField):
            return DateStoreField(fld)
            #~ return DateStoreField(fld,self.report.date_format)
        if isinstance(fld,models.BooleanField):
            return BooleanStoreField(fld)
        #~ if isinstance(fld,models.TextField):
            #~ return TextStoreField(fld)
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

    def form2obj(self,request,form_values,instance,is_new):
        #~ logger.info("Store.form2obj(%s)", form_values)
        if self.report.disabled_fields:
            disabled_fields = set(self.report.disabled_fields(instance,request))
        else:
            disabled_fields = set()
        #~ print 20110406, disabled_fields
        for f in self.all_fields:
            if f.field is None or not f.field.name in disabled_fields:
                #~ logger.info("Store.form2obj %s", f.field.name)
                try:
                    f.form2obj(request,instance,form_values,is_new)
                except exceptions.ValidationError,e:
                    raise exceptions.ValidationError({f.field.name:e})
                except Exception,e:
                    logger.warning("%s : %s", f.field.name,e)
                    logger.exception(e)
                    raise 
                #~ logger.info("20111209 Store.form2obj %s -> %s", f, obj2str(instance))
        #~ return instance
            
    def column_names(self):
        l = []
        for fld in self.list_fields:
            l += fld.column_names()
        return l
        
    def column_index(self,name):
        """Used to write definition of Ext.ensible.cal.CalendarMappings
        and Ext.ensible.cal.EventMappings
        """
        #~ logger.info("20111214 column_names: %s",list(self.column_names()))
        return list(self.column_names()).index(name)
        #~ i = 0
        #~ for fld in self.list_fields:
            #~ for cn in fld.column_names()
            #~ if fld.field and fld.field.name == name:
                #~ return i
            #~ i += 1
        

    def row2list(self,request,row):
        assert isinstance(request,reports.ListActionRequest)
        #~ if not isinstance(request,reports.ListActionRequest):
            #~ raise Exception()
        #~ logger.info("20111209 Store.row2list(%s)", obj2str(row))
        l = []
        for fld in self.list_fields:
            l += fld.obj2list(request,row)
            #~ logger.info("20111209 Store.row2list %s -> %s", fld, l)
        return l
      
    def row2dict(self,request,row):
        assert isinstance(request,reports.ListActionRequest)
        #~ logger.info("20111209 Store.row2dict(%s)", obj2str(row))
        d = {}
        for f in self.detail_fields:
            f.obj2dict(request,row,d)
            #~ logger.info("20111209 Store.row2dict %s -> %s", f, d)
        return d
