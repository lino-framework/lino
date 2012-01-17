#coding: utf-8
## Copyright 2008-2012 Luc Saffre
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


from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.contrib.contenttypes import generic

import datetime


#~ from south.modelsinspector import add_introspection_rules
#~ add_introspection_rules([], ["^lino\.fields\.LanguageField"])
#~ add_introspection_rules([], ["^lino\.fields\.PriceField"])
#~ add_introspection_rules([], ["^lino\.fields\.KnowledgeField"])
#~ add_introspection_rules([], ["^lino\.fields\.StrengthField"])
#~ add_introspection_rules([], ["^lino\.fields\.PercentageField"])
#~ add_introspection_rules([], ["^lino\.fields\.MyDateField"])
#~ add_introspection_rules([], ["^lino\.fields\.MonthField"])
#~ add_introspection_rules([], ["^lino\.fields\.QuantityField"])
#~ add_introspection_rules([], ["^lino\.fields\.HtmlTextField"])


import logging
logger = logging.getLogger(__name__)

from lino.tools import full_model_name
from lino.tools import obj2str
from lino.tools import resolve_field

#~ from lino.utils import choosers
from lino.utils import choicelists
from lino.utils import IncompleteDate, d2iso

class PasswordField(models.CharField):
    """Stored as plain text in database, but not displayed in user interface."""
    pass
    
    
#~ TEXT_FORMAT_PLAIN = 'plain'
#~ TEXT_FORMAT_HTML = 'html'
#~ TEXT_FORMAT_TINYMCE = 'tinymce'
#~ TEXT_FORMAT_VINYLFOX = 'vinylfox'
    

class RichTextField(models.TextField):
    """
    Only difference with Django's `models.TextField` is that you can 
    specify a keyword argument `format` to 
    override the global :attr:`lino.Lino.textfield_format`.
    """
    def __init__(self,*args,**kw):
        self.textfield_format = kw.pop('format',None)
        super(RichTextField,self).__init__(*args,**kw)
        
    def set_format(self,fmt):
        self.textfield_format = fmt
    
  
class PercentageField(models.SmallIntegerField):
    def __init__(self, *args, **kw):
        defaults = dict(
            max_length=3,
            )
        defaults.update(kw)
        models.SmallIntegerField.__init__(self,*args, **defaults)
  
#~ class MonthField(models.CharField):
class MonthField(models.DateField):
    def __init__(self, *args, **kw):
        #~ defaults = dict(
            #~ max_length=10,
            #~ )
        #~ defaults.update(kw)
        #~ models.CharField.__init__(self,*args, **defaults)
        models.DateField.__init__(self,*args, **kw)
  
class PriceField(models.DecimalField):
    def __init__(self, *args, **kwargs):
        defaults = dict(
            max_length=10,
            max_digits=10,
            decimal_places=2,
            )
        defaults.update(kwargs)
        super(PriceField, self).__init__(*args, **defaults)
        
    #~ def formfield(self, **kwargs):
        #~ fld = super(PriceField, self).formfield(**kwargs)
        #~ # display size is smaller than full size:
        #~ fld.widget.attrs['size'] = "6"
        #~ fld.widget.attrs['style'] = "text-align:right;"
        #~ return fld
        
class MyDateField(models.DateField):
        
    def formfield(self, **kwargs):
        fld = super(MyDateField, self).formfield(**kwargs)
        # display size is smaller than full size:
        fld.widget.attrs['size'] = "8"
        return fld
        
        
        
class QuantityField(models.DecimalField):
    def __init__(self, *args, **kwargs):
        defaults = dict(
            max_length=5,
            max_digits=5,
            decimal_places=0,
            )
        defaults.update(kwargs)
        super(QuantityField, self).__init__(*args, **defaults)
        
    def formfield(self, **kwargs):
        fld = super(QuantityField, self).formfield(**kwargs)
        fld.widget.attrs['size'] = "3"
        fld.widget.attrs['style'] = "text-align:right;"
        return fld
        
class FakeField: 
    primary_key = False
    editable = False
    name = None
    
    def is_enabled(self,lh):
        return True
        
    def has_default(self):
        return False
        

class DisplayField(FakeField):
    
    choices = None
    blank = True
    drop_zone = None
    max_length = None
    #~ bbar = None
    def __init__(self,verbose_name=None,**kw):
        self.verbose_name = verbose_name
        for k,v in kw.items():
            assert hasattr(self,k)
            setattr(self,k,v)
    # the following dummy methods are never called but needed when using a DisplayField 
    # as return_type of a VirtualField
    def to_python(self,*args,**kw): raise NotImplementedError
    def save_form_data(self,*args,**kw): raise NotImplementedError
    def value_to_string(self,*args,**kw): raise NotImplementedError
        

        
class HtmlBox(DisplayField):
    pass
    
#~ class QuickAction(DisplayField):
    #~ pass
    
#~ from django.db.models.fields import Field

class VirtualField(FakeField): # (Field):
    """
    Currently subclassed only by :class:`lino.utils.mti.EnableChild`.    
    """
    
    def __init__(self,return_type,get):
        if isinstance(return_type,basestring):
            return_type = resolve_field(return_type)
        self.return_type = return_type # a Django Field instance
        self.get = get
        #~ self.set = set
        #~ self.name = None
        #~ Field.__init__(self)
        for k in ('''to_python choices save_form_data 
          value_to_string verbose_name max_length rel
          blank'''.split()):
            setattr(self,k,getattr(return_type,k,None))
            
    def unused_contribute_to_class(self, cls, name):
        ## if defined in abstract base class, called once on each submodel
        if self.name:
            if self.name != name:
                raise Exception("Attempt to re-use %s as %s in %s" % (
                    self.__class__.__name__,name,cls))
        else:
            self.name = name
            if self.verbose_name is None and self.name:
                self.verbose_name = self.name.replace('_', ' ')
        self.model = cls
        cls._meta.add_virtual_field(self)
        #~ cls._meta.add_field(self)
        
    #~ def to_python(self,*args,**kw): return self.return_type.to_python(*args,**kw)
    #~ def save_form_data(self,*args,**kw): return self.return_type.save_form_data(*args,**kw)
    #~ def value_to_string(self,*args,**kw): return self.return_type.value_to_string(*args,**kw)
    #~ def get_choices(self): return self.return_type.choices
    #~ choices = property(get_choices)
            
    def set_value_in_object(self,request,obj,value):
        """
        Stores the specified `value` in the specified model instance `obj`.
        `request` may be `None`.
        
        Note that any implementation must also return `obj`,
        and callers must be ready to get another instance.
        This special behaviour is needed to implement 
        :class:`lino.utils.mti.EnableChild`.
        """
        #~ raise NotImplementedError
        pass
        
    def lino_kernel_setup(self,model,name):
        self.model = model
        self.name = name
        #~ self.return_type.name = name
        #~ self.return_type.attname = name
        #~ if issubclass(model,models.Model):
        model._meta.add_virtual_field(self)
        logger.debug('Found VirtualField %s.%s',full_model_name(model),name)
        
    def value_from_object(self,request,obj):
        """
        Return the value of this field in the specified model instance `obj`.
        `request` may be `None`, it's forwarded to the getter method who may 
        decide to return values depending on it.
        """
        m = self.get
        #~ assert m.func_code.co_argcount == 2, (self.name, m.func_code.co_varnames)
        #~ print self.field.name
        return m(obj,request)
        
class RequestField(VirtualField):
    def __init__(self,get,*args,**kw):
        kw.setdefault('max_length',8)
        VirtualField.__init__(self,DisplayField(*args,**kw),get)
        

def virtualfield(return_type):
    """
    Decorator to make a VirtualField from a method.
    """
    def decorator(fn):
        def wrapped(*args):
            return fn(*args)
        return VirtualField(return_type,wrapped)
    return decorator
    
def displayfield(*args,**kw):
    """
    Decorator shortcut to make a virtual DisplayField from a method.
    """
    return virtualfield(DisplayField(*args,**kw))
    
def requestfield(*args,**kw):
    """
    Decorator to make a RequestField from a method.
    The method to decorate must return either None or a TableRequest object.
    """
    def decorator(fn):
        def wrapped(*args):
            return fn(*args)
        return RequestField(wrapped,*args,**kw)
    return decorator
    
        

class MethodField(VirtualField):
    """
    Not used. See :doc:`/blog/2011/1221`.
    Similar to VirtualField, but the `get` argument to `__init__` 
    must be a string which is the name of a model method to be called 
    without a `request`.
    """
    def __init__(self,return_type,get,*args,**kw):
        self.args = args
        self.kw = kw
        VirtualField.__init__(self,return_type,get)
        
    def lino_kernel_setup(self,model,name):
        self.get = getattr(model,get)
        VirtualField.lino_kernel_setup(self,model,name)
      
    def value_from_object(self,request,obj):
        """
        Return the value of this field in the specified model instance `obj`.
        `request` is ignored.
        """
        m = self.get
        return m(obj,*self.args,**self.kw)
        

#~ class DynamicForeignKey(models.PositiveIntegerField):
    #~ """
    
    #~ """
    #~ def __init__(self, link_field, *args, **kw):
        #~ self.link_field = link_field
        #~ models.PositiveIntegerField.__init__(self,*args, **kw)
        


class LinkedForeignKey(generic.GenericForeignKey):
    """
    Like a GenericForeignKey, but the content type 
    is not stored in another model.
    Code partly copied from django.contrib.contenttypes GenericForeignKey.
    Used by :mod:`lino.modlib.links`.
    
    """
    editable = True
    verbose_name = None
    primary_key = False
    choices = None
    blank = True
    drop_zone = None
    
    
    def __init__(self,type_fk,name,*args,**kw):
        """
        type_fk is a regular ForeignKey field that points to a model whose 
        instances hold the ContentType.
        `name` is the prefix for both fields names.
        """
        self.type_fk = type_fk
        self.type_fieldname = name + '_type' 
        self.fk_field = name + '_id' 
        for k,v in kw.items():
            assert hasattr(self,k)
            setattr(self,k,v)
        
    # the following dummy methods are needed when using a DisplayField 
    # as return_type of a VirtualField
    #~ def to_python(self,*args,**kw): raise NotImplementedError
    #~ def save_form_data(self,*args,**kw): raise NotImplementedError
    #~ def value_to_string(self,*args,**kw): raise NotImplementedError
    
    def instance_pre_init(self, signal, sender, args, kwargs, **_kwargs):
        """
        Handles initializing an object with the generic FK insteed of
        content-type/object-id fields.
        """
        if self.name in kwargs:
            value = kwargs.pop(self.name)
            #~ kwargs[self.ct_field] = self.get_content_type(obj=value)
            kwargs[self.fk_field] = value._get_pk_val()

    def get_content_type(self,obj):
        if not getattr(obj,self.type_fk.name+'_id'):
            #~ logger.info("20111209 get_contenttype() no type_id in %s", obj2str(obj))
            return None
        link_type = getattr(obj,self.type_fk.name)
        #~ link_type = obj.type
        return getattr(link_type,self.type_fieldname)
        


    def __get__(self, instance, instance_type=None):
        if instance is None: # accessed as a class attribute
            return self
        try:
            return getattr(instance, self.cache_attr)
        except AttributeError:
            rel_obj = None
            ct = self.get_content_type(instance)
            if ct is not None: 
                pk = getattr(instance, self.fk_field)
                if pk:
                    model = ct.model_class()
                    rel_obj = ct.get_object_for_this_type(pk=pk)
            setattr(instance, self.cache_attr, rel_obj)
            return rel_obj

    def __set__(self, instance, value):
        ct = None
        fk = None
        if value is not None:
            ct = self.get_content_type(instance) 
            fk = value._get_pk_val()

        ct = self.get_content_type(instance)
        if ct is None:
            raise ValueError("Cannot store value % because content type is undefined" % value)
        if not isinstance(value,ct.model_class()):
            raise ValueError("Expected %s instance but got %r" % (ct.model_class(),value))
        
        #~ setattr(instance, self.ct_field, ct)
        setattr(instance, self.fk_field, fk)
        setattr(instance, self.cache_attr, value)
        
    def value_from_object(self,obj):
        return self.__get__(obj)




#~ class DynamicGeneralForeignKey(models.PositiveIntegerField):
#~ class DynamicForeignKey(models.ForeignKey):
class unused_DynamicForeignKey(object):
    """
    Used to define the two fields 'a' and 'b' on the Link model.
    """
    #~ __metaclass__ = models.SubfieldBase
    
  
    #~ def __init__(self,fk_field,type_field_name,*args,**kw):
    def __init__(self,linkfield,*args,**kw):
        self.fk_field = linkfield.fk_field
        self.type_field_name = type_field_name
        models.PositiveIntegerField.__init__(self,*args,**kw)
    
    
    def to_python(self, value):
        if isinstance(value,models.Model):
            return value
        if not value:
            return value
        raise Exception("Cannot know contenttype for %r" % value)
        #~ ct = self.get_contenttype(obj)
        #~ if ct is None:
            #~ return None
        #~ return ct.get_object_for_this_type(pk=pk)
            
        #~ return value
        
    def get_prep_value(self, value):
        if value:
            return value.pk
        return None
        
    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_prep_value(value)
        #~ return self.get_db_prep_value(value,connection)
        
    #~ def save_form_data(self, instance, data):
        #~ setattr(instance, self.name, data)
        
    #~ def get_text_for_value(self,value):
        #~ return self.choicelist.get_text_for_value(value.value)
        
    def __get__(self,obj):
        return self.get_value(obj)
        
    def get_value(self,obj,request=None):
        """
        The optional 2nd argument `request` (passed from
        `VirtualField.value_from_object`) is ignored.
        """
        pk = getattr(obj,self.name+'_id')
        if pk is None:
            return None
        ct = self.get_contenttype(obj)
        if ct is None:
            return None
        return ct.get_object_for_this_type(pk=pk)
        
        #~ try:
            #~ return ct.get_object_for_this_type(pk=pk)
        #~ except model.DoesNotExist:
            #~ return None

    def set_value_in_object(self,request,obj,v):
        raise Exception("20111208")
        if not v:
            setattr(obj,self.name,None)
            return 
            
        ct = self.get_contenttype(obj)
        if ct is None:
            raise Exception("20111209")
            return None
        
        if not isinstance(v,ct.model_class()):
            raise Exception("20111209")
        setattr(obj,self.name,v.pk)


        
        

class GenericForeignKeyIdField(models.PositiveIntegerField):
    """
    Use this instead of `models.PositiveIntegerField` 
    for fields that part of a :term:`GFK` and you want 
    Lino to render them using a Combobox.
    
    Used by :class:`lino.mixins.Owned`.
    """
    def __init__(self, type_field, *args, **kw):
        self.type_field = type_field
        models.PositiveIntegerField.__init__(self,*args, **kw)
    
class GenericForeignKey(generic.GenericForeignKey):
    """
    Lino's little extension to Django's GFK.
    Used by :class:`lino.mixins.Owned`.
    """
    def __init__(self, ct_field="content_type", fk_field="object_id", 
          verbose_name=None):
        self.verbose_name = verbose_name
        generic.GenericForeignKey.__init__(self,ct_field,fk_field)
        
    
class FieldSet:
    """
    A group of fields that have a common label (`verbose_name`)
    to be displayed and translated.
    """
    def __init__(self,verbose_name,desc=None,**child_labels):
        self.verbose_name = verbose_name
        self.desc = desc
        self.child_labels = child_labels
        
    def get_child_label(self,name):
        s = self.child_labels.get(name,None)
        #~ logger.info('get_child_label(%r)->%s',name,unicode(s))
        return s
        



class ChoiceListField(models.CharField):
    """
    A field that stores values from a 
    :class:`lino.utils.choicelists.ChoiceList`.
    """
    
    __metaclass__ = models.SubfieldBase
    
    #~ choicelist = NotImplementedError
    
    def __init__(self,choicelist,*args,**kw):
        if args:
            verbose_name = args[0]
            args = args[1:]
        else:
            verbose_name = kw.pop('verbose_name',None)
        if verbose_name is None:
            verbose_name = choicelist.label
        self.choicelist = choicelist
        defaults = dict(
            #~ choices=KNOWLEDGE_CHOICES,
            choices=choicelist.get_choices(),
            max_length=choicelist.max_length,
            blank=True,  # null=True,
            #~ validators=[validate_knowledge],
            #~ limit_to_choices=True,
            )
        defaults.update(kw)
        #~ models.SmallIntegerField.__init__(self,*args, **defaults)
        models.CharField.__init__(self,verbose_name,*args, **defaults)
        
    def get_internal_type(self):
        return "CharField"
        
    def to_python(self, value):
        if isinstance(value,choicelists.BabelChoice):
            return value
        value = self.choicelist.to_python(value)
        if value is None: # see 20110907
            value = ''
        return value
        
    def get_prep_value(self, value):
        if value:
            return value.value
        return '' # see 20110907
        #~ return None
        
    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_prep_value(value)
        #~ return self.get_db_prep_value(value,connection)
        
    #~ def save_form_data(self, instance, data):
        #~ setattr(instance, self.name, data)
        
    def get_text_for_value(self,value):
        return self.choicelist.get_text_for_value(value.value)
    
      
class IncompleteDateField(models.CharField):
    """
    A field that behaves like a DateField, but accepts
    incomplete dates represented using 
    :class:`lino.utils.IncompleteDate`.
    """
    __metaclass__ = models.SubfieldBase

    def __init__(self,*args,**kw):
        kw.update(max_length=11)
        models.CharField.__init__(self,*args,**kw)
      
    def get_internal_type(self):
        return "CharField"
        
    def to_python(self, value):
        if isinstance(value,IncompleteDate):
            return value
        if isinstance(value,datetime.date):
            #~ return IncompleteDate(value.strftime("%Y-%m-%d"))
            #~ return IncompleteDate(d2iso(value))
            return IncompleteDate.from_date(value)
        if value:
            return IncompleteDate.parse(value)
        return ''
        
    def get_prep_value(self, value):
        return str(value)
        
    #~ def get_prep_value(self, value):
        #~ return '"' + str(value) + '"'
        #~ if value:
            #~ return value.format("%04d%02d%02d")
        #~ return '' 
        
    #~ def value_to_string(self, obj):
        #~ value = self._get_val_from_obj(obj)
        #~ return self.get_prep_value(value)
        


