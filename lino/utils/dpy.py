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


"""
exec serializer.

"""

from StringIO import StringIO
import os
import imp


from django.db import models
from django.db.models.fields import NOT_PROVIDED
from django.core.serializers import base
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission
from django.contrib.sessions.models import Session
from django.utils.encoding import smart_unicode, is_protected_type

from lino.tools import obj2str
from lino.utils import dblogger

#~ from lino.utils.instantiator import d2i

SUFFIX = '.dpy'



class Serializer(base.Serializer):
    """
    Serializes a QuerySet to a dpy stream.
    """

    internal_use_only = False
    
    def serialize(self, queryset, **options):
        self.options = options

        self.stream = options.get("stream", StringIO())
        self.selected_fields = options.get("fields")
        self.use_natural_keys = options.get("use_natural_keys", False)

        self.stream.write('# -*- coding: UTF-8 -*-\n\n')
        self.stream.write('from lino.utils import i2d\n')
        self.stream.write('from lino.tools import resolve_model\n')
        #~ model = queryset.model
        for model in models.get_models():
            self.stream.write('%s = resolve_model("%s.%s")\n' % (model.__name__, model._meta.app_label,model.__name__))
        self.stream.write('\n')
        for model in models.get_models():
            fields = model._meta.fields
            #~ fields = [f for f in model._meta.fields if f.serialize]
            #~ fields = [f for f in model._meta.local_fields if f.serialize]
            self.stream.write('def create_%s(%s):\n' % (model._meta.db_table,','.join([f.attname for f in fields])))
            #~ for f in fields:
                #~ if isinstance(f,models.ForeignKey):
                    #~ self.stream.write('    if %s is not None:\n' % f.name)
                    #~ self.stream.write('         %s = %s.objects.get(pk=%s)\n' % (f.name,f.rel.to.__name__,f.name))
            #~ self.stream.write('    %s(%s).save(force_insert=True)\n' % (
            self.stream.write('    return %s(%s)\n' % (
                model.__name__,
                ','.join([
                    '%s=%s' % (f.attname,f.attname) for f in fields])))
        #~ self.start_serialization()
        self.stream.write('\n')
        model = None
        all_models = []
        for obj in queryset:
            if isinstance(obj,ContentType): continue
            if isinstance(obj,Session): continue
            if isinstance(obj,Permission): continue
            if obj.__class__ != model:
                model = obj.__class__
                all_models.append(model)
                self.stream.write('\ndef %s_objects():\n' % model._meta.db_table)
            fields = obj._meta.fields
            #~ fields = [f for f in obj._meta.local_fields if f.serialize]
            self.stream.write('    yield create_%s(%s)\n' % (
                obj._meta.db_table,
                ','.join([self.value2string(obj,f) for f in fields])))
            #~ self.start_object(obj)
            #~ for field in obj._meta.local_fields:
                #~ if field.serialize:
                    #~ if field.rel is None:
                        #~ if self.selected_fields is None or field.attname in self.selected_fields:
                            #~ self.handle_field(obj, field)
                    #~ else:
                        #~ if self.selected_fields is None or field.attname[:-3] in self.selected_fields:
                            #~ self.handle_fk_field(obj, field)
            #~ for field in obj._meta.many_to_many:
                #~ if field.serialize:
                    #~ if self.selected_fields is None or field.attname in self.selected_fields:
                        #~ self.handle_m2m_field(obj, field)
            #~ self.end_object(obj)
        #~ self.end_serialization()
        #~ return self.getvalue()
        self.stream.write('\n\ndef objects():\n')
        all_models = self.sort_models(all_models)
        for model in all_models:
            self.stream.write('    for o in %s_objects(): yield o\n' % model._meta.db_table)          
            
    def sort_models(self,unsorted):
        sorted = []
        hope = True
        while unsorted and hope:
            hope = False
            #~ print "hope for", [m.__name__ for m in unsorted]
            for model in unsorted:
                deps = [f.rel.to for f in model._meta.fields if f.rel is not None]
                ok = True
                for d in deps:
                    if d in unsorted:
                    #~ if not d in sorted:
                        ok = False
                if ok:
                    #~ print "ok:", model.__name__
                    sorted.append(model)
                    unsorted.remove(model)
                    hope = True
                    break
                #~ print model.__name__, "depends on", [m.__name__ for m in deps]
        if unsorted:
            dblogger.warning("models with circular dependencies : %s",[m.__name__ for m in unsorted])
            sorted.extend(unsorted)              
        return sorted      
    

    #~ def start_serialization(self):
        #~ self._current = None
        #~ self.objects = []

    #~ def end_serialization(self):
        #~ pass

    #~ def start_object(self, obj):
        #~ self._current = {}

    #~ def end_object(self, obj):
        #~ self.objects.append({
            #~ "model"  : smart_unicode(obj._meta),
            #~ "pk"     : smart_unicode(obj._get_pk_val(), strings_only=True),
            #~ "fields" : self._current
        #~ })
        #~ self._current = None

    def value2string(self, obj, field):
        value = field._get_val_from_obj(obj)
        # Protected types (i.e., primitives like None, numbers, dates,
        # and Decimals) are passed through as is. All other values are
        # converted to string first.
        if value is None or value is NOT_PROVIDED:
            return 'None'
        if isinstance(field,models.DateField):
            #~ return 'i2d(%d)' % d2i(value)
            d = value
            return 'i2d(%4d%02d%02d)' % (d.year,d.month,d.day)
        if is_protected_type(value):
            return unicode(value)
        else:
            return repr(field.value_to_string(obj))

    def handle_fk_field(self, obj, field):
        related = getattr(obj, field.name)
        if related is not None:
            if self.use_natural_keys and hasattr(related, 'natural_key'):
                related = related.natural_key()
            else:
                if field.rel.field_name == related._meta.pk.name:
                    # Related to remote object via primary key
                    related = related._get_pk_val()
                else:
                    # Related to remote object via other field
                    related = smart_unicode(getattr(related, field.rel.field_name), strings_only=True)
        self._current[field.name] = related

    def handle_m2m_field(self, obj, field):
        if field.rel.through._meta.auto_created:
            if self.use_natural_keys and hasattr(field.rel.to, 'natural_key'):
                m2m_value = lambda value: value.natural_key()
            else:
                m2m_value = lambda value: smart_unicode(value._get_pk_val(), strings_only=True)
            self._current[field.name] = [m2m_value(related)
                               for related in getattr(obj, field.name).iterator()]

    #~ def getvalue(self):
        #~ return self.objects









class FakeDeserializedObject(base.DeserializedObject):
    """
    Imitates DeserializedObject required by loaddata,
    but this time we *don't want* to bypass pre_save/save methods.
    """
    def __init__(self, obj):
        self.object = obj

    def save(self, *args,**kw):
        #~ print 'dpyserializer',self.object
        if True:
            try:
                self.object.full_clean()
            except ValidationError,e:
                raise Exception("Cannot save %s : %s" % (obj2str(self.object),e))
        self.object.save(*args,**kw)
        dblogger.info("Deserialized %s has been saved" % obj2str(self.object))


#~ class Serializer:
    #~ internal_use_only = False
    
def Deserializer(fp, **options):
    """
    """
    if isinstance(fp, basestring):
        raise NotImplementedError
    parts = os.path.split(fp.name)
    fqname = parts[-1]
    assert fqname.endswith(SUFFIX)
    fqname = fqname[:-4]
    #print fqname
    desc = (SUFFIX,'r',imp.PY_SOURCE)
    module = imp.load_module(fqname, fp, fp.name, desc)
    #m = __import__(filename)
    for instance in module.objects():
        if instance is not None:
            yield FakeDeserializedObject(instance)


