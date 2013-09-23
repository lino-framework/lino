# -*- coding: UTF-8 -*-
## Copyright 2008-2013 Luc Saffre
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
Defines classes :class:`Frame` and :class:`FrameHandle`
"""

import logging
logger = logging.getLogger(__name__)

import datetime
from decimal import Decimal


from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.contrib.contenttypes import generic
from django.db.models.fields import NOT_PROVIDED



from djangosite.dbutils import full_model_name
from djangosite.dbutils import obj2str

from north.dbutils import contribute_to_class

from lino.core.dbutils import resolve_field
from lino.core.dbutils import resolve_model, UnresolvedModel
#~ from lino.core.dbutils import is_installed_model_spec

#~ from lino.utils import choosers
from lino.utils import IncompleteDate, d2iso
#~ from lino.utils.quantities import Duration
from lino.utils import quantities 

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




class BabelTextField(RichTextField):
    """
    Define a variable number of clones of the "master" field, 
    one for each language .
    """
    def contribute_to_class(self, cls, name):
        super(BabelTextField,self).contribute_to_class(cls, name)
        contribute_to_class(self,cls,RichTextField,
            format=self.textfield_format)


  
#~ class PercentageField(models.SmallIntegerField):
    #~ """
    #~ Deserves more documentation.
    #~ """
    #~ def __init__(self, *args, **kw):
        #~ defaults = dict(
            #~ max_length=3,
            #~ )
        #~ defaults.update(kw)
        #~ models.SmallIntegerField.__init__(self,*args, **defaults)

class PercentageField(models.DecimalField):
    """
    A field to express a percentage. 
    The database stores this like a DecimalField.
    Plain HTML adds a "%".
    """
    def __init__(self, *args, **kwargs):
        defaults = dict(
            max_length=5,
            max_digits=5,
            decimal_places=2,
            )
        defaults.update(kwargs)
        super(PercentageField, self).__init__(*args, **defaults)
  
class DatePickerField(models.DateField):
    """
    A DateField that uses a DatePicker instead of a normal DateWidget.
    Doesn't yet work.
    """

class MonthField(models.DateField):
    """
    A DateField that uses a MonthPicker instead of a normal DateWidget
    """
    def __init__(self, *args, **kw):
        models.DateField.__init__(self,*args, **kw)
  
class PriceField(models.DecimalField):
    """
    A Decimalfield with default values for decimal_places, max_length and max_digits.
    
    """
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
        
#~ class MyDateField(models.DateField):
        
    #~ def formfield(self, **kwargs):
        #~ fld = super(MyDateField, self).formfield(**kwargs)
        #~ # display size is smaller than full size:
        #~ fld.widget.attrs['size'] = "8"
        #~ return fld
        
        
"""
http://stackoverflow.com/questions/454436/unique-fields-that-allow-nulls-in-django
answer Dec 20 '09 at 3:40 by mightyhal
http://stackoverflow.com/a/1934764
"""
class NullCharField(models.CharField): #subclass the CharField
    description = "CharField that stores empty strings as NULL instead of ''."
    def __init__(self, *args, **kwargs):
        defaults = dict(blank=True,null=True)
        defaults.update(kwargs)
        super(NullCharField, self).__init__(*args, **defaults)
        
    def to_python(self, value):  #this is the value right out of the db, or an instance
       #~ if isinstance(value, models.CharField): #if an instance, just return the instance
       if isinstance(value, basestring): #if a string, just return the value
            return value 
       if value is None:   #if the db has a NULL (==None in Python)
            return ''  # convert it into the Django-friendly '' string
       else:
            return value # otherwise, return just the value
            
    def get_db_prep_value(self, value, connection, prepared=False):
    #catches value right before sending to db
       if value == '':     # if Django tries to save '' string, send the db None (NULL)
            return None
       else:
            return value # otherwise, just pass the value        


class FakeField(object):
    """
    Base class for 
    :class:`RemoteField`
    :class:`DisplayField`
    """
    model = None
    choices = None
    primary_key = False
    editable = False
    name = None
    #~ verbose_name = None
    help_text = None
    preferred_width = 30
    preferred_height = 3
    max_digits = None
    decimal_places = None
    default = NOT_PROVIDED
    
    def is_enabled(self,lh):
        """
        Overridden by mti.EnableChild
        """
        #~ return False
        #~ return True
        return self.editable
        
    def has_default(self):
        return self.default is not NOT_PROVIDED
        
        

#~ class NullField(FakeField):
    #~ def __init__(self,name):
        #~ self.name = name
    
class RemoteField(FakeField):
    """
    Represents a field on a related object.
    LayoutHandle instantiates a RemoteField for example when 
    """
    #~ primary_key = False
    #~ editable = False
    def __init__(self,func,name,fld,**kw):
        self.func = func
        self.name = name
        self.field = fld
        self.rel = self.field.rel
        self.verbose_name = fld.verbose_name
        self.max_length = getattr(fld,'max_length',None)
        self.max_digits = getattr(fld,'max_digits',None)
        self.decimal_places = getattr(fld,'decimal_places',None)
        #~ print 20120424, self.name
        #~ settings.SITE.register_virtual_field(self)
        
        #~ store = top_model.get_default_table().get_handle().store
        #~ store = self.field.model.get_default_table().get_handle().store
        from lino.ui import store
        #~ self._lino_atomizer = store.create_field(self,name)
        store.get_atomizer(self,name)
        
        
    #~ def lino_resolve_type(self):
        #~ self._lino_atomizer = self.field._lino_atomizer

    def value_from_object(self,obj,ar=None):
        """
        Return the value of this field in the specified model instance `obj`.
        `ar` may be `None`, it's forwarded to the getter method who may 
        decide to return values depending on it.
        """
        m = self.func
        return m(obj,ar)
        
    def __get__(self,instance,owner):
        if instance is None: return self
        return self.value_from_object(instance)

        

class DisplayField(FakeField):
    """
    Deserves more documentation.
    """
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
    def to_python(self,*args,**kw): 
        raise NotImplementedError("%s.to_python(%s,%s)",(self.name,args,kw))
    def save_form_data(self,*args,**kw): raise NotImplementedError
    def value_to_string(self,*args,**kw): raise NotImplementedError
        
    def value_from_object(self,obj,ar=None):
        return ''

#~ class DynamicForeignKey(DisplayField):
    #~ """
    #~ A pointer to "the" one and only MTI child.
    #~ This assumes that there is always one and only one child instance among the given models.
    #~ """
    #~ def __init__(self,get_child,**kw):
        #~ self.get_child = get_child
        #~ VirtualField.__init__(self,models.ForeignKey(**kw),self.has_child)
        
        
class HtmlBox(DisplayField):
    """
    Deserves more documentation.
    """
    pass
    
#~ class QuickAction(DisplayField):
    #~ pass
    
#~ from django.db.models.fields import Field

class VirtualGetter(object):
    """
    A wrapper object for getting the content of 
    a virtual field programmatically. 
    """
    def __init__(self,vf,instance):
        self.vf  = vf
        self.instance = instance
        
    def __call__(self,ar=None):
        return self.vf.value_from_object(self.instance,ar)
        

class VirtualField(FakeField): # (Field):
    """
    Currently subclassed only by :class:`lino.utils.mti.EnableChild`.    
    """
    
    def __init__(self,return_type,get):
        self.return_type = return_type # a Django Field instance
        self.get = get
        
        settings.SITE.register_virtual_field(self)
        """
        Normal VirtualFields are read-only and not editable.
        We don't want to require application developers to explicitly 
        specify `editable=False` in their return_type::
        
          @dd.virtualfield(dd.PriceField(_("Total")))
          def total(self,ar=None):
              return self.total_excl + self.total_vat
        """
            
    def override_getter(self,get):
        self.get = get
        
    def attach_to_model(self,model,name):
        self.model = model
        self.name = name
        #~ self.return_type.name = name
        #~ self.return_type.attname = name
        #~ if issubclass(model,models.Model):
        #~ self.lino_resolve_type(model,name)
        model._meta.add_virtual_field(self)
        #~ logger.info('20120831 VirtualField %s.%s',full_model_name(model),name)
        
    def __repr__(self):
        return "%s %s.%s" % (self.__class__.__name__,self.model,self.name)
        
    def lino_resolve_type(self):
        """
        Unlike attach_to_model, this is also called on virtual 
        fields that are defined on an Actor
        """
        #~ logger.info("20120903 lino_resolve_type %s.%s", actor_or_model, name)
        #~ if self.name is not None:
            #~ if self.name != name:
                #~ raise Exception("Tried to re-use %s.%s" % (actor_or_model,name))
        #~ self.name = name
            
        if isinstance(self.return_type,basestring):
            self.return_type = resolve_field(self.return_type)
            
        #~ self.return_type.name = self.name
        if isinstance(self.return_type,models.ForeignKey):
            f = self.return_type
            f.rel.to = resolve_model(f.rel.to)
            if f.verbose_name is None:
                #~ if f.name is None:
                f.verbose_name = f.rel.to._meta.verbose_name
                    #~ from lino.core.kernel import set_default_verbose_name
                    #~ set_default_verbose_name(self.return_type)
            

        #~ removed 20120919 self.return_type.editable = self.editable
        for k in ('''to_python choices save_form_data 
          value_to_string verbose_name max_length rel
          max_digits decimal_places
          help_text
          blank'''.split()):
            setattr(self,k,getattr(self.return_type,k,None))
        #~ logger.info('20120831 VirtualField %s on %s',name,actor_or_model)
        
        #~ store = self.model.get_default_table().get_handle().store
        #~ self._lino_atomizer = store.create_field(self,self.name)
        #~ self._lino_atomizer = self.return_type._lino_atomizer
        from lino.ui import store
        #~ self._lino_atomizer = store.create_field(self,self.name)
        store.get_atomizer(self,self.name)
        
    def get_default(self):
        return self.return_type.get_default()
        #~ 
    def has_default(self):
        return self.return_type.has_default()
        
      
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
        raise NotImplementedError("Cannot write %r to field %s" % (value,self))
        
    #~ def value_from_object(self,request,obj):
    def value_from_object(self,obj,ar=None):
        """
        Return the value of this field in the specified model instance `obj`.
        `request` may be `None`, it's forwarded to the getter method who may 
        decide to return values depending on it.
        """
        m = self.get
        #~ assert m.func_code.co_argcount == 2, (self.name, m.func_code.co_varnames)
        #~ print self.field.name
        return m(obj,ar)
        
    def __get__(self,instance,owner):
        if instance is None: return self
        return VirtualGetter(self,instance)
        
    def __set__(self,instance,value):
        return self.set_value_in_object(None,instance,value)
        

def virtualfield(return_type):
    """
    Decorator to turn a method into a VirtualField.
    """
    def decorator(fn):
        return VirtualField(return_type,fn)
    return decorator
    


class Constant(object):
    """
    Deserves more documentation.
    """
    #~ get = None
    def __init__(self,text_fn):
        self.text_fn = text_fn
        
#~ def constant(verbose_name=None):
def constant():
    """
    Decorator to turn a method into a :class:`Constant`.
    """
    def decorator(fn):
        #~ def wrapped(*args):
            #~ return fn(*args)
        #~ return Constant(wrapped)
        return Constant(fn)
    return decorator


class RequestField(VirtualField):
    """
    Deserves more documentation.
    """
    def __init__(self,get,*args,**kw):
        kw.setdefault('max_length',8)
        VirtualField.__init__(self,DisplayField(*args,**kw),get)
        

def displayfield(*args,**kw):
    """
    Decorator shortcut to turn a method into a virtual DisplayField.
    """
    return virtualfield(DisplayField(*args,**kw))
    
def requestfield(*args,**kw):
    """
    Decorator to make a RequestField from a method.
    The method to decorate must return either None or a TableRequest object.
    """
    def decorator(fn):
        #~ def wrapped(*args):
            #~ return fn(*args)
        #~ return RequestField(wrapped,*args,**kw)
        return RequestField(fn,*args,**kw)
    return decorator
    
        

class MethodField(VirtualField):
    """
    Not used. See `/blog/2011/1221`.
    Similar to VirtualField, but the `get` argument to `__init__` 
    must be a string which is the name of a model method to be called 
    without a `request`.
    """
    def __init__(self,return_type,get,*args,**kw):
        self.args = args
        self.kw = kw
        VirtualField.__init__(self,return_type,get)
        
    def attach_to_model(self,model,name):
        self.get = getattr(model,get)
        VirtualField.attach_to_model(self,model,name)
      
    #~ def value_from_object(self,request,obj):
    def value_from_object(self,obj,ar=None):
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
        


class unused_LinkedForeignKey(generic.GenericForeignKey):
    """
    Like a GenericForeignKey, but the content type is not stored in another model.
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
    
    Used by :class:`lino.mixins.Controllable`.
    """
    def __init__(self, type_field, *args, **kw):
        self.type_field = type_field
        models.PositiveIntegerField.__init__(self,*args, **kw)
    
class GenericForeignKey(generic.GenericForeignKey):
    """
    Add verbose_name and help_text to Django's GFK.
    Used by :class:`lino.mixins.Controllable`.
    """
    def __init__(self, ct_field="content_type", fk_field="object_id", 
          verbose_name=None,help_text=None,dont_merge=False):
        self.verbose_name = verbose_name
        self.help_text = help_text
        self.dont_merge = dont_merge
        generic.GenericForeignKey.__init__(self,ct_field,fk_field)
        
    #~ def contribute_to_class(self, cls, name):
        #~ """
        #~ @chooser(instance_values=True)
        #~ def object_id_choices(cls,object_type):
            #~ if object_type:
                #~ return object_type.model_class().objects.all()
            #~ return []
        #~ def get_object_id_display(self,value):
            #~ if self.object_type:
                #~ try:
                    #~ return unicode(self.object_type.get_object_for_this_type(pk=value))
                #~ except self.object_type.model_class().DoesNotExist,e:
                    #~ return "%s with pk %r does not exist" % (
                        #~ full_model_name(self.object_type.model_class()),value)
        #~ """
        #~ generic.GenericForeignKey.contribute_to_class(self, cls, name)
        #~ if not hasattr(cls,
        
    
#~ class FieldSet:
    #~ """
    #~ A group of fields that have a common label (`verbose_name`)
    #~ to be displayed and translated.
    #~ """
    #~ def __init__(self,verbose_name,desc=None,**child_labels):
        #~ self.verbose_name = verbose_name
        #~ self.desc = desc
        #~ self.child_labels = child_labels
        
    #~ def get_child_label(self,name):
        #~ s = self.child_labels.get(name,None)
        #~ return s
        



class CharField(models.CharField):
    """
    
    An extension around Django's `models.CharField`.
    
    Adds two keywords `mask_re` and
    `strip_chars_re` which, when using the ExtJS ui, 
    will be rendered as the 
    `maskRe` and `stripCharsRe` config options 
    of 
    `TextField` 
    as described in the 
    `ExtJS documentation 
    <http://docs.sencha.com/extjs/3.4.0/#!/api/Ext.form.TextField>`__,
    converting naming conventions as follows:
    
    =============== ============ ==========================
    regex           regex        A JavaScript RegExp object to be tested against the field value during validation (defaults to null). If the test fails, the field will be marked invalid using regexText.
    mask_re         maskRe       An input mask regular expression that will be used to filter keystrokes that do not match (defaults to null). The maskRe will not operate on any paste events.
    strip_chars_re  stripCharsRe A JavaScript RegExp object used to strip unwanted content from the value before validation (defaults to null).
    =============== ============ ==========================
    
    
    Example usage:
    
      belgian_phone_no = dd.CharField(max_length=15,strip_chars_re='')
    
    
    """
    
    def __init__(self,*args,**kw):
        self.strip_chars_re = kw.pop('strip_chars_re',None)
        self.mask_re = kw.pop('mask_re',None)
        self.regex = kw.pop('regex',None)
        models.CharField.__init__(self,*args,**kw)
       
  
class QuantityField(CharField):
#~ class QuantityField(models.CharField):
#~ class QuantityField(models.DecimalField):
#~ class QuantityField(models.Field):
    """
    A field that accepts both 
    :class:`lino.utils.quantity.Decimal`,
    :class:`lino.utils.quantity.Percentage` 
    and 
    :class:`lino.utils.quantity.Duration` 
    values.
    
    Implemented as a CharField (sorting or filter ranges may not work)
    
    QuantityFields are implemented as CharFields and 
    therefore should *not* be declared `null=True`. 
    But if `blank=True`, empty strings are converted to `None` 
    values.    
  
    """
    __metaclass__ = models.SubfieldBase
    description = _("Quantity (Decimal or Duration)")

    def __init__(self,*args,**kw):
        kw.setdefault('max_length',6)
        models.Field.__init__(self,*args,**kw)
        #~ models.CharField.__init__(self,*args,**kw)
      
    #~ def get_internal_type(self):
        #~ return "CharField"
        
    def to_python(self, value):
        """
        
        Excerpt from `Django doc 
        <https://docs.djangoproject.com/en/dev/howto/custom-model-fields/#django.db.models.Field.to_python>`__:
        
            As a general rule, the method should deal gracefully with any of the following arguments:

            - An instance of the correct type (e.g., Hand in our ongoing example).
            - A string (e.g., from a deserializer).
            - Whatever the database returns for the column type you’re using.
            
        I'd add "Any value specified for this field when instantiating a model."
       
        >>> to_python(None)
        >>> to_python(30)
        >>> to_python(30L)
        >>> to_python('')
        >>> to_python(Decimal(0))
        """
        if isinstance(value,Decimal):
            return value
        if value:
            if isinstance(value,basestring):
                return quantities.parse(value)
            return Decimal(value)
        return None
        
    #~ def get_db_prep_save(self, value, connection):
        #~ if value is None:
            #~ return ''
        #~ return str(value)
        
    def get_prep_value(self,value):
        if value is None:
            return ''
        return str(value)
        
class IncompleteDateField(models.CharField):
    """
    A field that behaves like a DateField, but accepts
    incomplete dates represented using 
    :class:`lino.utils.IncompleteDate`.
    """
    __metaclass__ = models.SubfieldBase

    def __init__(self,*args,**kw):
        kw.update(max_length=11)
        msgkw = dict()
        msgkw.update(ex1=IncompleteDate(1980,0,0).strftime(settings.SITE.date_format_strftime))
        msgkw.update(ex2=IncompleteDate(1980,7,0).strftime(settings.SITE.date_format_strftime))
        msgkw.update(ex3=IncompleteDate(0,7,23).strftime(settings.SITE.date_format_strftime))
        kw.setdefault('help_text',_("""\
Uncomplete dates are allowed, e.g. 
"%(ex1)s" means "some day in 1980", 
"%(ex2)s" means "in July 1980"
or "%(ex3)s" means "on a 23th of July".""") % msgkw)
        models.CharField.__init__(self,*args,**kw)
      
    #~ def get_internal_type(self):
        #~ return "CharField"
        
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
        
class DummyField(object):
    """
    Deserves more documentation.
    """
    def __init__(self,*args,**kw):
        pass
    def set_attributes_from_name(self,k):
        pass

      
    
class RecurrenceField(models.CharField):
    """
    Deserves more documentation.
    """
    #~ __metaclass__ = models.SubfieldBase

    def __init__(self,*args,**kw):
        kw.setdefault('max_length',200)
        models.CharField.__init__(self,*args,**kw)
      


def fields_list(model,field_names):
    """
    Return a list with the names of the specified fields, 
    checking whether each of them exists.
    
    Arguments: 
    `model` is any subclass of `django.db.models.Model`.
    `field_names` is a single string with a space-separated list of field names.
    
    For example if you have a model `MyModel` 
    with two fields `foo` and `bar`,
    then ``dd.fields_list(MyModel,"foo bar")`` 
    will return ``['foo','bar']``
    and ``dd.fields_list(MyModel,"foo baz")`` will raise an exception.
    """
    #~ return tuple([get_field(model,n) for n in field_names.split()])
    #~ if model.__name__ == 'Company':
        #~ print 20110929, [get_field(model,n) for n in field_names.split()]
    #~ return [get_field(model,n).name for n in field_names.split()]
    lst = []
    for name in field_names.split():
        e = model.get_data_elem(name)
        if e is None:
            raise models.FieldDoesNotExist("No data element %r in %s" % (name,model))
        lst.append(e.name)
    return lst


def ForeignKey(othermodel,*args,**kw):
    """
    This is almost as 
    `django.db.models.ForeignKey <https://docs.djangoproject.com/en/dev/ref/models/fields/#foreignkey>`, 
    except for a subtle difference: 
    it supports `othermodel` being `None` or the name of some non-installed model
    and returns a :class:`DummyField <lino.core.fields.DummyField>` 
    in that case.
    This difference is useful when designing reusable models.
    """
    if othermodel is None: 
        return DummyField(othermodel,*args,**kw)
    if isinstance(othermodel,basestring):
        if not settings.SITE.is_installed_model_spec(othermodel):
            return DummyField(othermodel,*args,**kw)
    return models.ForeignKey(othermodel,*args,**kw)
    

class ImportedFields(object):
    """
    Utility mixin to easily declare "imported fields"
    """
    _imported_fields = set()
    
    @classmethod
    def declare_imported_fields(cls,names):
        cls._imported_fields = cls._imported_fields | set(fields_list(cls,names))
        #~ logger.info('20120801 %s.declare_imported_fields() --> %s' % (
            #~ cls,cls._imported_fields))
        
