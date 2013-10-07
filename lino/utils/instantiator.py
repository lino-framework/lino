## Copyright 2009-2013 Luc Saffre
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
Defines the :class:`Instantiator` class and some other utilities 
used mainly for :doc:`/topics/dumpy`.
"""

import logging
logger = logging.getLogger(__name__)

import decimal
import datetime
from dateutil import parser as dateparser

from django.db import models
from django.contrib.contenttypes.models import ContentType

#~ import lino
from lino.core.dbutils import resolve_model, UnresolvedModel

from lino.utils import i2d # for backward compatibility of .py fixtures
#~ from lino.core import fields
#~ from lino.core import signals
from lino.core.dbutils import obj2str

class DataError(Exception):
    pass
    

#~ import django.dispatch

    
    
class Converter(object):
    def __init__(self,field):
        self.field = field
  
    def convert(self,**kw):
        return kw
 
class LookupConverter(Converter):
    """
    A Converter for ForeignKey and ManyToManyField. 
    If the lookup_field is a BabelField, then it tries all available languages.
    """
    def __init__(self,field,lookup_field):
        Converter.__init__(self,field)
        model = field.rel.to
        if lookup_field == 'pk':
            self.lookup_field = model._meta.pk
        else:
            self.lookup_field = model._meta.get_field(lookup_field)
        #~ self.lookup_field = lookup_field
        
        
        
    def lookup(self,value,**kw):
        model = self.field.rel.to
        if isinstance(value,model):
            return value
        return model.lookup_or_create(self.lookup_field,value,**kw)
        
        #~ if isinstance(self.lookup_field,babel.BabelCharField):
            #~ flt  = babel.lookup_filter(self.lookup_field.name,value,**kw)
        #~ else:
            #~ kw[self.lookup_field.name] = value
            #~ flt = models.Q(**kw)
        #~ try:
            #~ return model.objects.get(flt)
        #~ except MultipleObjectsReturned,e:
            #~ raise model.MultipleObjectsReturned("%s.objects lookup(%r) : %s" % (model.__name__,value,e))
        #~ except model.DoesNotExist,e:
            #~ raise model.DoesNotExist("%s.objects lookup(%r) : %s" % (model.__name__,value,e))
              
        

class DateConverter(Converter):
    def convert(self,**kw):
        value = kw.get(self.field.name)
        if value is not None:
            if not isinstance(value,datetime.date):
                #~ print "20111218 DateConverter", value
                if type(value) == int:
                    value = str(value)
                d = dateparser.parse(value)
                d = datetime.date(d.year,d.month,d.day)
                kw[self.field.name] = d
        return kw

class ChoiceConverter(Converter):
    """Converter for :class:`ChoiceListField <lino.core.choicelists.ChoiceListField>`.
    """
    def convert(self,**kw):
        value = kw.get(self.field.name)
        if value is not None:
            if not isinstance(value,self.field.choicelist.item_class):
                kw[self.field.name] = self.field.choicelist.get_by_value(value)
        return kw
        
class DecimalConverter(Converter):
    def convert(self,**kw):
        value = kw.get(self.field.name)
        if value is not None:
            if not isinstance(value,decimal.Decimal):
                kw[self.field.name] = decimal.Decimal(value)
        return kw
        

class ForeignKeyConverter(LookupConverter):
    """Converter for ForeignKey fields."""
        
    def convert(self,**kw):
        value = kw.get(self.field.name)
        if value is not None:
            if value == '':
                value = None
            else:
                value = self.lookup(value)
            kw[self.field.name] = value
            #~ logger.info("20111213 %s %s -> %r", self.field.name,self.__class__,value)
        return kw

  

class ManyToManyConverter(LookupConverter):
    """Converter for ManyToMany fields."""
    splitsep = None
        
    #~ def lookup(self,value):
        #~ model = self.field.rel.to
        #~ try:
            #~ return model.objects.get(
              #~ **{self.lookup_field: value})
        #~ except model.DoesNotExist,e:
            #~ raise DataError("%s.objects.get(%r) : %s" % (
              #~ model.__name__,value,e))

    def convert(self,**kw):
        values = kw.get(self.field.name)
        if values is not None:
            del kw[self.field.name]
            l = [self.lookup(value) 
              for value in values.split(self.splitsep)]
            kw['_m2m'][self.field.name] = l
        return kw

def make_converter(f,lookup_fields={}):
    if isinstance(f,models.ForeignKey):
        return ForeignKeyConverter(f,lookup_fields.get(f.name,"pk"))
    #~ if isinstance(f,fields.LinkedForeignKey):
        #~ return LinkedForeignKeyConverter(f,lookup_fields.get(f.name,"pk"))
    if isinstance(f,models.ManyToManyField):
        return ManyToManyConverter(f,lookup_fields.get(f.name,"pk"))
    if isinstance(f,models.DateField):
        return DateConverter(f)
    if isinstance(f,models.DecimalField):
        return DecimalConverter(f)
    from lino.core import choicelists
    if isinstance(f,choicelists.ChoiceListField):
        return ChoiceConverter(f)
      
class Instantiator:
    def is_active(self):
      
        if isinstance(self.model,UnresolvedModel): return False
        if self.model._meta.pk is None: return False
        return True
          
    def __init__(self,model,fieldnames=None,converter_classes={},**kw):
        #~ self.model = resolve_model(model,strict=True)
        self.model = resolve_model(model)
        #~ if isinstance(self.model,UnresolvedModel):
            #~ logger.warning("20120818 unresolved model %s",model)
            #~ return 
        if not self.is_active():
            def noop(*values,**kw): pass
            self.build = noop
            return
        #~ if self.model._meta.pk is None: 
            #~ raise Exception("Model %r is not installed (_meta.pk is None)." % self.model)
        #~ if type(fieldnames) == str:
        if isinstance(fieldnames,basestring):
            fieldnames = fieldnames.split()
        self.default_values = kw
        #self.fieldnames = fieldnames
        lookup_fields = {}
        self.converters = []
        if fieldnames is None:
            self.fields = self.model._meta.fields
        else:
            self.fields = []
            for name in fieldnames:
                a = name.split(":")
                if len(a) == 2:
                    name = a[0]
                    lookup_fields[name] = a[1]
                field = self.model._meta.get_field(name)
                self.fields.append(field)
        #print " ".join(dir(model_class))
        #print " ".join(model_class._meta.fields)
        #for f in model_class._meta.fields:
        #for f in self.fields:
        for f in self.model._meta.fields + self.model._meta.many_to_many:
            cv = None
            cvc = converter_classes.get(f.name,None)
            if cvc is not None:
                cv = cvc(f)
            else:
                cv = make_converter(f,lookup_fields)
            if cv is not None:
                self.converters.append(cv)
        #~ for f in model_class._meta.many_to_many:
            #~ print "foo", f.name

    def build(self,*values,**kw):
        # logger.debug("Instantiator.build(%s,%r,%r)",self.model_class._meta.db_table,values,kw)
        #~ i = 0
        kw['_m2m'] = {}
        for i,v in enumerate(values):
            if isinstance(v,basestring):
                v = v.strip()
                if len(v) > 0:
                    kw[self.fields[i].name] = v
            else:
                kw[self.fields[i].name] = v
            #~ i += 1
        #~ kw.update(self.default_values)
        for k,v in self.default_values.items():
            kw.setdefault(k,v)
        for c in self.converters:
            kw = c.convert(**kw)
        #~ if self.model.__name__ == 'Company':
            #~ print 20130212, __file__, kw
            #~ logger.info("20130212 field_cache for %s (%s)",self.model,
              #~ ' '.join([f.name for f in self.model._meta._field_name_cache]))
            
        m2m = kw.pop("_m2m")
        instance = self.model(**kw)
        instance.full_clean()
        if m2m:
            instance.save()
            for k,v in m2m.items():
                queryset = getattr(instance,k)
                queryset.add(*v)
        return instance
  

def create_and_get(model,**kw):
    """
    Instantiate, full_clean, save 
    and read back from database (the latter to avoid certain Django side effects)
    """
    model = resolve_model(model)
    o = model(**kw)
    o.full_clean()
    o.save()
    return model.objects.get(pk=o.pk)
        
