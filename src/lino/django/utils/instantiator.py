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
        pkvalue = kw.get(self.field.name)
        if pkvalue is not None:
            try:
                p = self.field.rel.to.objects.get(pk=pkvalue)
            except self.field.rel.to.DoesNotExist,e:
                e = DataError(
                  "%s.objects.get(%s) : %s" % (
                      self.field.rel.to.__name__,pkvalue,e))
                #print e
                raise e
            else:
                kw[self.field.name] = p
        return kw
    
      
class Instantiator:
    def __init__(self,model_class,fieldnames=None):
        if type(fieldnames) == str:
            fieldnames = fieldnames.split()
        self.model_class = model_class
        self.fieldnames = fieldnames
        self.converters = []
        #print " ".join(dir(model_class))
        #print " ".join(model_class._meta.fields)
        for f in model_class._meta.fields:
            #f = getattr(model_class,name)
            #print repr(f)
            if isinstance(f,models.ForeignKey):
                self.converters.append(ForeignKeyConverter(f))
            
    def build(self,*values,**kw):
        #print "build",kw
        i = 0
        for v in values:
            if (not isinstance(v,basestring)) or len(v) > 0:
                kw[self.fieldnames[i]] = v
            i += 1
        for c in self.converters:
            kw = c.convert(**kw)
        instance = self.model_class(**kw)
        instance.save()
        return instance
  
