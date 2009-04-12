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


"""
YAML serializer.

Requires PyYaml (http://pyyaml.org/), but that's checked for in __init__.
"""

from StringIO import StringIO
import yaml

try:
    import decimal
except ImportError:
    from django.utils import _decimal as decimal # Python 2.3 fallback

from django.core.serializers import base

from django.db import models
from django.core.serializers.python import Serializer as PythonSerializer
from django.core.serializers.python import Deserializer as PythonDeserializer

class DjangoSafeDumper(yaml.SafeDumper):
    def represent_decimal(self, data):
        return self.represent_scalar('tag:yaml.org,2002:str', str(data))

DjangoSafeDumper.add_representer(decimal.Decimal, DjangoSafeDumper.represent_decimal)



# my code

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
                raise DataError(
                  "%s.objects.get(%s) : %s" % (
                      self.field.rel.to.__name__,pkvalue,e))
            else:
                kw[self.field.name] = p
        return kw
    
      
class ModelBuilder:
    def __init__(self,model_class):
        self.model_class = model_class
        self.converters = []
        #print " ".join(dir(model_class))
        #print " ".join(model_class._meta.fields)
        for f in model_class._meta.fields:
            #f = getattr(model_class,name)
            #print repr(f)
            if isinstance(f,models.ForeignKey):
                self.converters.append(ForeignKeyConverter(f))
            
    def build(self,**kw):
        #print "build",kw
        for c in self.converters:
            kw = c.convert(**kw)
        instance = self.model_class(**kw)
        instance.save()
        return instance
  


class Serializer(PythonSerializer):
    internal_use_only = False
    
    #~ """
    #~ Convert a queryset to YAML.
    #~ """
    
    
    #~ def handle_field(self, obj, field):
        #~ # A nasty special case: base YAML doesn't support serialization of time
        #~ # types (as opposed to dates or datetimes, which it does support). Since
        #~ # we want to use the "safe" serializer for better interoperability, we
        #~ # need to do something with those pesky times. Converting 'em to strings
        #~ # isn't perfect, but it's better than a "!!python/time" type which would
        #~ # halt deserialization under any other language.
        #~ if isinstance(field, models.TimeField) and getattr(obj, field.name) is not None:
            #~ self._current[field.name] = str(getattr(obj, field.name))
        #~ else:
            #~ super(Serializer, self).handle_field(obj, field)
    
    #~ def end_serialization(self):
        #~ self.options.pop('stream', None)
        #~ self.options.pop('fields', None)
        #~ yaml.dump(self.objects, self.stream, Dumper=DjangoSafeDumper, **self.options)

    #~ def getvalue(self):
        #~ return self.stream.getvalue()

def Deserializer(stream_or_string, **options):
    """
    Deserialize a stream or string of YAML data.
    """
    if isinstance(stream_or_string, basestring):
        stream = StringIO(stream_or_string)
    else:
        stream = stream_or_string
        
    model_builder = None
    for values in yaml.load_all(stream):
        if values.has_key('model'):
            modelspec = values.pop('model')
            #model_class = eval(modelspec)
            app,model = modelspec.split(".")
            #print app,model
            model_class = models.get_model(app,model)
            if not model_class:
                raise Exception("invalid model:" + modelspec)
            model_builder = ModelBuilder(model_class)
        if model_builder is None:
            raise DataError("No model specified")
        #print model_class
        instance = model_builder.build(**values)
        #~ if model_class == User:
            #~ instance.set_password(yamldict.get('password'))
        # data files are required to use "!!python/object:", so the
        # yamldict is a Python object
        #self.add_node(yamldict)
        #print instance.pk, instance
        m2m_data = {}
        yield base.DeserializedObject(instance, m2m_data)


        #~ instance.save()
        #~ print "Saved:", instance
        #self.modelspec = modelspec
        

