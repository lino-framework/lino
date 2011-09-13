## Copyright 2009-2011 Luc Saffre
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
See :doc:`/topics/dpy`

"""

from StringIO import StringIO
import os
import imp
from decimal import Decimal
#~ from types import GeneratorType


from django.conf import settings
from django.db import models
from django.db.models.fields import NOT_PROVIDED
from django.core.serializers import base
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.contrib.contenttypes.models import ContentType
#~ from django.contrib.auth.models import Permission
from django.contrib.sessions.models import Session
from django.utils.encoding import smart_unicode, is_protected_type, force_unicode

import lino
from lino.tools import obj2str, sorted_models_list, full_model_name
from lino.utils import dblogger
from lino.utils import babel

SUFFIX = '.py'
#~ SUFFIX = '.dpy'

class Serializer(base.Serializer):
    """
    Serializes a QuerySet to a py stream.
    Usage: ``manage.py dumpdata --format py``
    """

    internal_use_only = False
    
    write_preamble = True # may be set to False e.g. by testcases
    models = None
    
    def serialize(self, queryset, **options):
        self.options = options

        self.stream = options.get("stream", StringIO())
        self.selected_fields = options.get("fields")
        self.use_natural_keys = options.get("use_natural_keys", False)
        if self.write_preamble:
            self.stream.write('# -*- coding: UTF-8 -*-\n\n')
            #~ self.stream.write('# Created using Lino version %s\n' % lino.__version__)
            self.stream.write('SOURCE_VERSION = %r\n' % lino.__version__)
            self.stream.write('from datetime import datetime as dt\n')
            self.stream.write('from datetime import time,date\n')
            #~ self.stream.write('from lino.utils import i2d\n')
            self.stream.write('from lino.utils.mti import insert_child\n')
            self.stream.write('from lino.tools import resolve_model\n')
            self.stream.write('from django.contrib.contenttypes.models import ContentType\n')
            self.stream.write('from django.conf import settings\n')
        #~ model = queryset.model
        if self.models is None:
            self.models = sorted_models_list() # models.get_models()
        if self.write_preamble:
            for model in self.models:
                self.stream.write('%s = resolve_model("%s")\n' % (
                  full_model_name(model,'_'), full_model_name(model)))
        self.stream.write('\n')
        for model in self.models:
            fields = model._meta.local_fields
            #~ fields = [f for f in model._meta.fields if f.serialize]
            #~ fields = [f for f in model._meta.local_fields if f.serialize]
            self.stream.write('def create_%s(%s):\n' % (
                model._meta.db_table,', '.join([f.attname for f in fields])))
            if model._meta.parents:
                assert len(model._meta.parents) == 1
                pm,pf = model._meta.parents.items()[0]
                child_fields = [f for f in fields if f != pf]
                if child_fields:
                    attrs = ','+','.join([
                      '%s=%s' % (f.attname,f.attname) 
                          for f in child_fields])
                else: attrs = ''
                self.stream.write('    return insert_child(%s.objects.get(pk=%s),%s%s)\n' % (
                    full_model_name(pm,'_'),pf.attname,full_model_name(model,'_'),attrs))
            else:
                for f in fields:
                    if isinstance(f,models.ForeignKey) and f.rel.to is ContentType:
                        self.stream.write(
                            '    %s = ContentType.objects.get_for_model(%s).pk\n' % (
                            f.attname,f.attname))
                self.stream.write('    return %s(%s)\n' % (
                    full_model_name(model,'_'),
                    ','.join([
                        '%s=%s' % (f.attname,f.attname) for f in fields])))
        #~ self.start_serialization()
        self.stream.write('\n')
        model = None
        all_models = []
        for obj in queryset:
            if isinstance(obj,ContentType): continue
            #~ if isinstance(obj,Session): continue
            #~ if isinstance(obj,Permission): continue
            if obj.__class__ != model:
                model = obj.__class__
                if model in all_models:
                    raise Exception("%s instances weren't grouped!" % model)
                all_models.append(model)
                self.stream.write('\ndef %s_objects():\n' % model._meta.db_table)
            fields = obj._meta.local_fields
            #~ fields = [f for f in obj._meta.local_fields if f.serialize]
            self.stream.write('    yield create_%s(%s)\n' % (
                obj._meta.db_table,
                ','.join([self.value2string(obj,f) for f in fields])))
        self.stream.write('\n\ndef objects():\n')
        all_models = self.sort_models(all_models)
        for model in all_models:
            #~ self.stream.write('    for o in %s_objects(): yield o\n' % model._meta.db_table)
            self.stream.write('    yield %s_objects()\n' % model._meta.db_table)
        self.stream.write('\nsettings.LINO.loading_from_dump = True\n')
        if settings.LINO.migration_module:
            self.stream.write('\n')
            self.stream.write('from %s import install\n' \
                % settings.LINO.migration_module)
            self.stream.write('install(globals())\n')
            
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
        if value is None:
        #~ if value is None or value is NOT_PROVIDED:
            return 'None'
        if isinstance(field,models.DateTimeField):
            d = value
            return 'dt(%d,%d,%d,%d,%d,%d)' % (
              d.year,d.month,d.day,d.hour,d.minute,d.second)
        if isinstance(field,models.TimeField):
            d = value
            return 'time(%d,%d,%d)' % (d.hour,d.minute,d.second)
        if isinstance(field,models.ForeignKey) and field.rel.to is ContentType:
            ct = ContentType.objects.get(pk=value)
            return full_model_name(ct.model_class(),'_')
            #~ return repr(tuple(value.app_label,value.model))
        if isinstance(field,models.DateField):
            d = value
            return 'date(%d,%d,%d)' % (d.year,d.month,d.day)
            #~ return 'i2d(%4d%02d%02d)' % (d.year,d.month,d.day)
        if isinstance(value,(float,Decimal)):
            return repr(str(value))
        if isinstance(value,(int,long)):
            return str(value)
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
    Imitates DeserializedObject required by loaddata.
    
    Unlike normal DeserializedObject, we *don't want* to bypass 
    pre_save and validation methods on the individual objects.
    
    """
    
    
    def __init__(self, deserializer, object):
        self.object = object
        #~ self.name = name
        self.deserializer = deserializer

    def save(self, *args,**kw):
        """
        """
        #~ print 'dpy.py',self.object
        #~ dblogger.info("Loading %s...",self.name) 
        
        self.try_save(*args,**kw)
        #~ if self.try_save(*args,**kw):
            #~ self.deserializer.saved += 1
        #~ else:
            #~ self.deserializer.save_later.append(self)
        
    def try_save(self,*args,**kw):
        """Try to save the specified Model instance `obj`. Return `True` 
        on success, `False` if this instance wasn't saved and should be 
        deferred.
        """
        obj = self.object
        try:
            obj.full_clean()
            obj.save(*args,**kw)
            dblogger.debug("%s has been saved" % obj2str(obj))
            self.deserializer.register_success()
            return True
        #~ except ValidationError,e:
        #~ except ObjectDoesNotExist,e:
        #~ except (ValidationError,ObjectDoesNotExist,IntegrityError), e:
        except Exception, e:
            if obj.pk is None:
                dblogger.exception(e)
                raise Exception(
                    "Failed to save %s (and %s is None). Abandoned." 
                    % (obj2str(obj),obj._meta.pk.attname))
            deps = [f.rel.to for f in obj._meta.fields if f.rel is not None]
            if not deps:
                dblogger.exception(e)
                raise Exception("Failed to save independent %s. Abandoned." % obj2str(obj))
            self.deserializer.register_failure(obj,e)
            return False
        except Exception,e:
            dblogger.exception(e)
            raise Exception("Failed to save %s. Abandoned." % obj2str(obj))
        
           
#~ IS_DESERIALIZING = False

#~ def is_deserializing():
    #~ """
    #~ Some special features may want to know out whether they are happening 
    #~ during a deserialization or not.
    #~ The only one known so far is :func:`lino.modlib.cal.models.update_auto_task`, 
    #~ which should not do anything during deserialization.    
    #~ See :doc:`/blog/2011/0727`.
    #~ """
    #~ return IS_DESERIALIZING

class DpyDeserializer:
    """
    Used when ``manage.py loaddata`` encounters a `.py` fixture.
    # new after blog/2011/0831
    """
    
    def __init__(self):
        self.save_later = {}
        self.saved = 0
  
    def deserialize(self,fp, **options):
        if isinstance(fp, basestring):
            raise NotImplementedError
        #~ global IS_DESERIALIZING
        #~ IS_DESERIALIZING = True
        babel.set_language(babel.DEFAULT_LANGUAGE)
        parts = os.path.split(fp.name)
        fqname = parts[-1]
        assert fqname.endswith(SUFFIX)
        fqname = fqname[:-4]
        #print fqname
        desc = (SUFFIX,'r',imp.PY_SOURCE)
        module = imp.load_module(fqname, fp, fp.name, desc)
        #m = __import__(filename)
        
        def expand(obj):
            if obj is None:
                pass # silently ignore None values
            elif isinstance(obj,models.Model):    
                yield FakeDeserializedObject(self,obj)
            elif hasattr(obj,'__iter__'):
            #~ if type(obj) is GeneratorType:
                for o in obj: 
                    for so in expand(o): 
                        yield so
            else:
                dblogger.warning("Ignored unknown object %r",obj)
                
        for obj in module.objects():
            for o in expand(obj): yield o
              
        dblogger.info("Saved %d instances from %s.",self.saved,fp.name)
                    
        while self.saved and self.save_later:
            try_again = []
            for msg_objlist in self.save_later.values():
                for obj in msg_objlist.values():
                    try_again.append(obj)
            dblogger.info("Trying again with %d unsaved instances.",
                len(self.save_later))
            self.save_later = {}
            self.saved = 0
            for obj in try_again:
                obj.try_save() # ,*args,**kw):
                #~ if obj.try_save(): # ,*args,**kw):
                    #~ self.saved += 1
                #~ else:
                    #~ self.save_later.append(obj)
            dblogger.info("Saved %d instances.",self.saved)
            
        if self.save_later:
            count = 0
            s = ''
            for model,msg_objects in save_later.items():
                for msg,objects in msg_objects.items():
                    s += "\n- %s %s (%d object(s), e.g. %s)" % (
                      full_model_name(model),msg,len(objects),obj2str(objects[0]))
                    count += len(objects)
            
            msg = "Abandoning with %d unsaved instances from %s:%s" % (
                count,fp.name,s)
            #~ dblogger.warning(msg)
            raise Exception(msg)
            
        if hasattr(module,'after_load'):
            module.after_load()
        #~ IS_DESERIALIZING = False

    def register_success(self):
        self.saved += 1
        
    def register_failure(self,obj,e):
        msg = force_unicode(e)
        d = self.save_later.setdefault(obj.__class__,{})
        l = d.setdefault(msg,[])
        l.append(obj)
        dblogger.info("Deferred %s : %s",obj2str(obj),msg)

def Deserializer(fp, **options):
    d = DpyDeserializer()
    return d.deserialize(fp, **options)

