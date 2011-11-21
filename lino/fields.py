#coding: utf-8
## Copyright 2008-2011 Luc Saffre
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

from lino.utils import choosers
from lino.utils import choicelists
from lino.tools import full_model_name
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
        
    def formfield(self, **kwargs):
        fld = super(PriceField, self).formfield(**kwargs)
        # display size is smaller than full size:
        fld.widget.attrs['size'] = "6"
        fld.widget.attrs['style'] = "text-align:right;"
        return fld
        
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
        
class DisplayField:
    editable = False
    choices = None
    blank = True
    drop_zone = None
    #~ bbar = None
    def __init__(self,verbose_name=None,**kw):
        self.verbose_name = verbose_name
        for k,v in kw.items():
            assert hasattr(self,k)
            setattr(self,k,v)
    # the following dummy methods are needed when using a DisplayField 
    # as return_type of a VirtualField
    def to_python(self,*args,**kw): raise NotImplementedError
    def save_form_data(self,*args,**kw): raise NotImplementedError
    def value_to_string(self,*args,**kw): raise NotImplementedError
    #~ def value_from_object(self,*args,**kw): raise NotImplementedError
        
class HtmlBox(DisplayField):
    pass
    
#~ class QuickAction(DisplayField):
    #~ pass
    
#~ from django.db.models.fields import Field

class VirtualField: # (Field):
    """
    Currently subclassed only by :class:`lino.utils.mti.EnableChild`.    
    """
    editable = False
    name = None
    
    def __init__(self,return_type,get):
        self.return_type = return_type # a Django Field instance
        self.get = get
        #~ self.set = set
        #~ self.name = None
        #~ Field.__init__(self)
        for k in ('''to_python choices save_form_data 
          value_to_string verbose_name
          blank'''.split()):
            setattr(self,k,getattr(return_type,k))
            
    def is_enabled(self,lh):
        return True
        
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
        self.return_type.name = name
        self.return_type.attname = name
        model._meta.add_virtual_field(self)
        logger.debug('Found VirtualField %s.%s',full_model_name(model),name)
        
    #~ def contribute_to_class(self, cls, name):
        #~ "Called from lino.core.kernel.setup"
        #~ self.name = name
        #~ self.model = cls
        
    #~ def get_db_prep_save(self, value, connection):
        #~ raise NotImplementedError
    #~ def pre_save(self, model_instance, add):
        #~ raise NotImplementedError
        
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
        
    
class GenericForeignKeyIdField(models.PositiveIntegerField):
    """
    """
    def __init__(self, type_field, *args, **kw):
        self.type_field = type_field
        models.PositiveIntegerField.__init__(self,*args, **kw)
    
    
    
class FieldSet:
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
        #~ if value:
            #~ return value.format("%04d%02d%02d")
        #~ return '' 
        
    #~ def value_to_string(self, obj):
        #~ value = self._get_val_from_obj(obj)
        #~ return self.get_prep_value(value)
        


        