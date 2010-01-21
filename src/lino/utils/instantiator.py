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

from django.db import models
import datetime
from dateutil import parser as dateparser
import decimal

import lino

def i2d(i):
    d = dateparser.parse(str(i))
    d = datetime.date(d.year,d.month,d.day)
    #print i, "->", v
    return d

class DataError(Exception):
    pass

class Converter:
    def __init__(self,field,lookup_field=None):
        self.field = field
        self.lookup_field = lookup_field
  
    def convert(self,**kw):
        return kw
      

#~ def parse_date(value):
    #~ if len(value) == 8:
        #~ year = int(value[:4])
        #~ month = int(value[4:6])
        #~ day = int(value[6:8])
    #~ elif len(value) == 10:
        #~ year,month,day = map(int,value.split('-'))
    #~ else:
        #~ raise ValueError("Invalid value %r for date." % value)
    #~ return datetime.date(year,month,day)


class DateConverter(Converter):
    def convert(self,**kw):
        value = kw.get(self.field.name)
        if value is not None:
            if not isinstance(value,datetime.date):
                if type(value) == int:
                    value = str(value)
                d = dateparser.parse(value)
                d = datetime.date(d.year,d.month,d.day)
                kw[self.field.name] = d
        return kw

class DecimalConverter(Converter):
    def convert(self,**kw):
        value = kw.get(self.field.name)
        if value is not None:
            if not isinstance(value,decimal.Decimal):
                kw[self.field.name] = decimal.Decimal(value)
        return kw

class ForeignKeyConverter(Converter):
    def convert(self,**kw):
        value = kw.get(self.field.name)
        if value is not None:
            model = self.field.rel.to
            if not isinstance(value,model):
                lookup_kw = {self.lookup_field: value}
                try:
                    p = model.objects.get(**lookup_kw)
                except model.DoesNotExist,e:
                    raise DataError("%s.objects.get(**%r) : %s" % (
                          model.__name__,lookup_kw,e))
                kw[self.field.name] = p
        return kw

class ManyToManyConverter(Converter):
    splitsep = None
        
    def lookup(self,value):
        model = self.field.rel.to
        try:
            return model.objects.get(
              **{self.lookup_field: value})
        except model.DoesNotExist,e:
            raise DataError("%s.objects.get(%r) : %s" % (
              model.__name__,value,e))

    def convert(self,**kw):
        values = kw.get(self.field.name)
        if values is not None:
            del kw[self.field.name]
            l = [self.lookup(value) 
              for value in values.split(self.splitsep)]
            kw['_m2m'][self.field.name] = l
        return kw

      
from lino.modlib.tools import resolve_model

class Instantiator:
    def __init__(self,model,fieldnames=None,
          converter_classes={},**kw):
        self.model = resolve_model(model)
        if self.model._meta.pk is None: 
            raise Exception("Model %r is not installed (_meta.pk is None)." % self.model)
        if type(fieldnames) == str:
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
            #f = getattr(model_class,name)
            #print repr(f)
            #print f.name
            cvc = converter_classes.get(f.name,None)
            if cvc is not None:
                cv = cvc(f)
            else:
                if isinstance(f,models.ForeignKey):
                    cv = ForeignKeyConverter(f,
                      lookup_fields.get(f.name,"pk"))
                elif isinstance(f,models.ManyToManyField):
                    cv = ManyToManyConverter(f,
                      lookup_fields.get(f.name,"pk"))
                elif isinstance(f,models.DateField):
                    cv = DateConverter(f)
                elif isinstance(f,models.DecimalField):
                    cv = DecimalConverter(f)
            if cv is not None:
                self.converters.append(cv)
        #~ for f in model_class._meta.many_to_many:
            #~ print "foo", f.name

    def build(self,*values,**kw):
        # lino.log.debug("Instantiator.build(%s,%r,%r)",self.model_class._meta.db_table,values,kw)
        i = 0
        kw['_m2m'] = {}
        for v in values:
            if isinstance(v,basestring):
                v = v.strip()
                if len(v) > 0:
                    kw[self.fields[i].name] = v
            else:
                kw[self.fields[i].name] = v
            i += 1
        kw.update(self.default_values)
        for c in self.converters:
            kw = c.convert(**kw)
        m2m = kw.pop("_m2m")
        instance = self.model(**kw)
        instance.save()
        for k,v in m2m.items():
            queryset = getattr(instance,k)
            queryset.add(*v)
        return instance
  
