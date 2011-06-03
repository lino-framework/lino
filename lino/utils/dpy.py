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


from django.db import models
from django.db.models.fields import NOT_PROVIDED
from django.core.serializers import base
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.contrib.contenttypes.models import ContentType
#~ from django.contrib.auth.models import Permission
from django.contrib.sessions.models import Session
from django.utils.encoding import smart_unicode, is_protected_type, force_unicode

import lino
from lino.tools import obj2str, sorted_models_list
from lino.utils import dblogger

SUFFIX = '.py'
#~ SUFFIX = '.dpy'

class Serializer(base.Serializer):
    """
    Serializes a QuerySet to a dpy stream.
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
            self.stream.write('# Created using Lino version %s\n' % lino.__version__)
            self.stream.write('from lino.utils import i2d\n')
            self.stream.write('from lino.utils.mti import insert_child\n')
            self.stream.write('from lino.tools import resolve_model\n')
        #~ model = queryset.model
        if self.models is None:
            self.models = sorted_models_list() # models.get_models()
        if self.write_preamble:
            for model in self.models:
                self.stream.write('%s = resolve_model("%s.%s")\n' % (model.__name__, model._meta.app_label,model.__name__))
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
                    pm.__name__,pf.attname,model.__name__,attrs))
            else:
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
        if value is None:
        #~ if value is None or value is NOT_PROVIDED:
            return 'None'
        if isinstance(field,models.DateField):
            d = value
            return 'i2d(%4d%02d%02d)' % (d.year,d.month,d.day)
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
    
    Unlike normal DeserializedObject this stores just the generator 
    function `objects` and will start to run it only when the 
    Serializer asks it to :meth:`save`. 
    Django thinks that there is only 
    one object per fixture. That's why the loaddata of a 
    python dump ends with the irritating message 
    "Installed 1 object(s) from 1 fixture(s)". 
    
    The reason for this is that we perform our own algorithm 
    for resolving dependencies (by trying to save them, and if 
    an exception occurs we defer this instance, trying to save 
    the other instances first. Then we do another round of 
    :meth:`try_save` (as long as there is hope) 
    until everything has been saved. This sophisticated and 
    suboptimal method is necessary as long as we don't have an 
    algorithm for deserializing in the right order.
    """
    
    object = None # required by loaddata
    
    def __init__(self, name, objects):
        self.objects = objects
        self.name = name
        #~ self.save_later = []

    def save(self, *args,**kw):
        """This will execute the `objects` function and save all instances.
        """
        #~ print 'dpy.py',self.object
        save_later = []
        saved = 0
        for obj in self.objects():
            if self.try_save(obj,*args,**kw):
                saved += 1
            else:
                save_later.append(obj)
        dblogger.info("Saved %d instances from %s.",saved,self.name)
                
        while saved and save_later:
            dblogger.info("Trying again with %d unsaved instances.",
                len(save_later))
            try_again = save_later
            save_later = []
            saved = 0
            for obj in try_again:
                if self.try_save(obj,*args,**kw):
                    saved += 1
                else:
                    save_later.append(obj)
            dblogger.info("Saved %d instances.",saved)
            
        if save_later:
            dblogger.warning("Abandoning with %d unsaved instances from %s.",
                len(save_later),self.name)
            raise Exception("Abandoned with %d unsaved instances. "
              "See dblog for details." % len(save_later))
                
    def try_save(self,obj,*args,**kw):
        """Try to save the specified Model instance `obj`. Return `True` 
        on success, `False` if this instance wasn't saved and should be 
        deferred.
        """
        if obj is None:
            return True
        #~ try:
            #~ obj.full_clean()
        #~ except (ObjectDoesNotExist,ValidationError),e:
            #~ if obj.pk is None:
                #~ dblogger.exception(e)
                #~ raise Exception("Failed to validate %s. Abandoned." % obj2str(obj))
            #~ dblogger.debug("Deferred %s : %s",obj2str(obj),e)
            #~ return False
        #~ try:
            #~ obj.save(*args,**kw)
            #~ dblogger.debug("Deserialized %s has been saved" % obj2str(obj))
            #~ return True
        #~ except Exception,e:
            #~ if obj.pk is None:
                #~ dblogger.exception(e)
                #~ raise Exception("Failed to save %s. Abandoned." % obj2str(obj))
            #~ dblogger.debug("Deferred %s : %s",obj2str(obj),e)
            #~ return False
        try:
            obj.full_clean()
            obj.save(*args,**kw)
            dblogger.debug("%s has been saved" % obj2str(obj))
            return True
        #~ except Exception,e:
        #~ except ValidationError,e:
        #~ except ObjectDoesNotExist,e:
        except (ValidationError,ObjectDoesNotExist), e:
            if obj.pk is None:
                dblogger.exception(e)
                raise Exception("Failed to save %s. Abandoned." % obj2str(obj))
            deps = [f.rel.to for f in obj._meta.fields if f.rel is not None]
            if not deps:
                dblogger.exception(e)
                raise Exception("Failed to save independent %s. Abandoned." % obj2str(obj))
            dblogger.info("Deferred %s : %s",obj2str(obj),force_unicode(e))
            return False
      
        
              


def Deserializer(fp, **options):
    """
    Used when ``manage.py loaddata`` encounters a `.py` fixture.
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
    yield FakeDeserializedObject(fp.name,module.objects)


