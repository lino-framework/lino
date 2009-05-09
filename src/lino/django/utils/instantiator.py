## Copyright 2009 Luc Saffre

## This file is part of the Lino project.

## Lino is free software; you can redistribute it and/or modify it
## under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.

## Lino is distributed in the hope that it will be useful, but WITHOUT
## ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
## or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public
## License for more details.

## You should have received a copy of the GNU General Public License
## along with Lino; if not, write to the Free Software Foundation,
## Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

from django.db import models

class DataError(Exception):
    pass

class Converter:
    def __init__(self,field):
        self.field = field
  
    def convert(self,**kw):
        return kw
      
class ForeignKeyConverter(Converter):
    def convert(self,**kw):
        value = kw.get(self.field.name)
        if value is not None:
            try:
                p = self.field.rel.to.objects.get(pk=value)
            except self.field.rel.to.DoesNotExist,e:
                e = DataError(
                  "%s.objects.get(%s) : %s" % (
                      self.field.rel.to.__name__,value,e))
                #print e
                raise e
            else:
                kw[self.field.name] = p
        return kw

class ManyToManyConverter(Converter):
    def __init__(self,field,lookup_field):
        Converter.__init__(self,field)
        self.lookup_field = lookup_field
        
    def convert(self,**kw):
        values = kw.get(self.field.name)
        if values is not None:
            del kw[self.field.name]
            l = []
            for lookup_value in values.split():
                obj = self.field.rel.to.objects.get(**{self.lookup_field: lookup_value})
                l.append(obj)
            kw['m2m'][self.field.name] = l
        return kw

      
class Instantiator:
    def __init__(self,model_class,fieldnames=None):
        if type(fieldnames) == str:
            fieldnames = fieldnames.split()
        self.model_class = model_class
        #self.fieldnames = fieldnames
        lookup_fields = {}
        self.converters = []
        if fieldnames is None:
            self.fields = model_class._meta.fields
        else:
            self.fields = []
            for name in fieldnames:
                a = name.split(":")
                if len(a) == 2:
                    name = a[0]
                    lookup_fields[name] = a[1]
                field = model_class._meta.get_field(name)
                self.fields.append(field)
        #print " ".join(dir(model_class))
        #print " ".join(model_class._meta.fields)
        #for f in model_class._meta.fields:
        for f in self.fields:
            #f = getattr(model_class,name)
            #print repr(f)
            #print f.name
            if isinstance(f,models.ForeignKey):
                self.converters.append(ForeignKeyConverter(f))
            elif isinstance(f,models.ManyToManyField):
                self.converters.append(ManyToManyConverter(f,lookup_fields.get(f.name,"pk")))
        #~ for f in model_class._meta.many_to_many:
            #~ print "foo", f.name

    def build(self,*values,**kw):
        #print "build",kw
        i = 0
        kw['m2m'] = {}
        for v in values:
            if (not isinstance(v,basestring)) or len(v) > 0:
                kw[self.fields[i].name] = v
            i += 1
        for c in self.converters:
            kw = c.convert(**kw)
        m2m = kw.pop("m2m")
        instance = self.model_class(**kw)
        instance.save()
        for k,v in m2m.items():
            queryset = getattr(instance,k)
            queryset.add(*v)
            #~ lookup_field = self.lookup_fields.get(k,"pk")
            #~ for pk in v:
                #~ obj = queryset.get(**{lookup_field: pk})
                #~ queryset.add(obj)
        return instance
  
