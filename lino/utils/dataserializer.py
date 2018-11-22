# Copyright 2009 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)


"""
YAML serializer.

Requires PyYaml (http://pyyaml.org/), but that's checked for in __init__.
"""
# from future import standard_library
# standard_library.install_aliases()
from builtins import str
import six

from io import StringIO
import yaml

try:
    import decimal
except ImportError:
    from django.utils import _decimal as decimal  # Python 2.3 fallback

from django.core.serializers import base

from django.db import models
from django.core.serializers.python import Serializer as PythonSerializer
from django.core.serializers.python import Deserializer as PythonDeserializer


class DjangoSafeDumper(yaml.SafeDumper):

    def represent_decimal(self, data):
        return self.represent_scalar('tag:yaml.org,2002:str', str(data))

DjangoSafeDumper.add_representer(
    decimal.Decimal, DjangoSafeDumper.represent_decimal)


class FakeDeserializedObject(base.DeserializedObject):

    """loaddata requires DeserializedObject instances, 
    but this Deserializer does *not* bypass pre_save/save methods.
    """

    def __init__(self, obj):
        self.object = obj

    def save(self, save_m2m=True):
        self.object.save()

# my code

from lino.utils.instantiator import Instantiator


class Serializer(PythonSerializer):
    internal_use_only = False

    #~ """
    #~ Convert a queryset to YAML.
    #~ """


    #~ def handle_field(self, obj, field):
        # ~ # A nasty special case: base YAML doesn't support serialization of time
        # ~ # types (as opposed to dates or datetimes, which it does support). Since
        # ~ # we want to use the "safe" serializer for better interoperability, we
        # ~ # need to do something with those pesky times. Converting 'em to strings
        # ~ # isn't perfect, but it's better than a "!!python/time" type which would
        # ~ # halt deserialization under any other language.
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
    if isinstance(stream_or_string, six.string_types):
        stream = StringIO(stream_or_string)
    else:
        stream = stream_or_string

    model_builder = None
    for values in yaml.load_all(stream):
        if 'model' in values:
            modelspec = values.pop('model')
            #model_class = eval(modelspec)
            app, model = modelspec.split(".")
            # print app,model
            model_class = models.get_model(app, model)
            if not model_class:
                raise Exception("invalid model:" + modelspec)
            model_builder = Instantiator(model_class)
        if model_builder is None:
            raise DataError("No model specified")
        # print model_class
        instance = model_builder.build(**values)
        # yield instance
        #~ if model_class == User:
            #~ instance.set_password(yamldict.get('password'))
        # data files are required to use "!!python/object:", so the
        # yamldict is a Python object
        # self.add_node(yamldict)
        # print instance.pk, instance
        #~ instance.save()
        #~ m2m_data = {}
        yield FakeDeserializedObject(instance)


        #~ instance.save()
        #~ print "Saved:", instance
        #self.modelspec = modelspec
