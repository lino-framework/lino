# -*- coding: UTF-8 -*-
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

"Documented in :doc:`/topics/dumpy`."


import logging
logger = logging.getLogger(__name__)


from StringIO import StringIO
import os
import imp
from decimal import Decimal
#~ from types import GeneratorType


from django.conf import settings
from django.db import models
from django.db import IntegrityError
from django.db.models.fields import NOT_PROVIDED
from django.core.serializers import base
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.contrib.contenttypes.models import ContentType
#~ from django.contrib.auth.models import Permission
from django.contrib.sessions.models import Session
from django.utils.encoding import smart_unicode, is_protected_type, force_unicode

import lino
from lino.core.modeltools import obj2str, sorted_models_list, full_model_name
from lino.utils import dblogger
from lino.utils import babel
from lino import dd
#~ from lino.utils.mti import MtiChildWrapper

SUFFIX = '.py'

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
            self.stream.write('# -*- coding: UTF-8 -*-\n')
            #~ self.stream.write('# Created using Lino version %s\n' % lino.__version__)
            name,current_version,url = settings.LINO.using().next()
            if '+' in current_version:
                raise Exception(
                    "Cannot dumpdata from intermediate version %s" % current_version)
            
            self.stream.write('''\
"""
This is a `Python dump <http://lino-framework.org/topics/dumpy.html>`_.
"""
from __future__ import unicode_literals
''')
            self.stream.write('SOURCE_VERSION = %r\n' % current_version)
            #~ self.stream.write('SOURCE_VERSION = %r\n' % lino.__version__)
            self.stream.write('from decimal import Decimal\n')
            self.stream.write('from datetime import datetime as dt\n')
            self.stream.write('from datetime import time,date\n')
            #~ self.stream.write('from lino.utils import i2d\n')
            #~ self.stream.write('from lino.utils.mti import insert_child\n')
            self.stream.write('from lino.utils import babel\n')
            self.stream.write('from lino.utils.mti import create_child\n')
            self.stream.write('from lino.dd import resolve_model\n')
            self.stream.write('from django.contrib.contenttypes.models import ContentType\n')
            self.stream.write('from django.conf import settings\n')
            self.stream.write('''
            
def new_content_type_id(m):
    if m is None: return m
    # if not fmn: return None
    # m = resolve_model(fmn)
    ct = ContentType.objects.get_for_model(m)
    if ct is None: return None
    return ct.pk
    
''')
            s = ','.join([
              '%s=values[%d]' % (k,i) 
                for i,k in enumerate(babel.AVAILABLE_LANGUAGES)])
            self.stream.write('''
def bv2kw(fieldname,values):
    """
    Needed if `lino.Lino.languages` changed between dumpdata and loaddata
    """
    return babel.babel_values(fieldname,%s)
    
''' % s)
        #~ model = queryset.model
        if self.models is None:
            self.models = sorted_models_list() # models.get_models()
        if self.write_preamble:
            for model in self.models:
                self.stream.write('%s = resolve_model("%s")\n' % (
                  full_model_name(model,'_'), full_model_name(model)))
        self.stream.write('\n')
        for model in self.models:
            fields = [f for f,m in model._meta.get_fields_with_model() if m is None]
            #~ fields = model._meta.local_fields
            #~ fields = [f for f in model._meta.fields if f.serialize]
            #~ fields = [f for f in model._meta.local_fields if f.serialize]
            self.stream.write('def create_%s(%s):\n' % (
                model._meta.db_table,', '.join([f.attname for f in fields if not getattr(f,'_lino_babel_field',False)])))
            if model._meta.parents:
                if len(model._meta.parents) != 1:
                    msg = "%s : model._meta.parents is %r" % (model,model._meta.parents)
                    raise Exception(msg)
                pm,pf = model._meta.parents.items()[0]
                child_fields = [f for f in fields if f != pf]
                if child_fields:
                    attrs = ','+','.join([
                      '%s=%s' % (f.attname,f.attname) 
                          for f in child_fields])
                else: attrs = ''
                #~ self.stream.write('    return insert_child(%s.objects.get(pk=%s),%s%s)\n' % (
                    #~ full_model_name(pm,'_'),pf.attname,full_model_name(model,'_'),attrs))
                self.stream.write('    return create_child(%s,%s,%s%s)\n' % (
                    full_model_name(pm,'_'),pf.attname,full_model_name(model,'_'),attrs))
            else:
                self.stream.write("    kw = dict()\n")
                for f in fields:
                    if getattr(f,'_lino_babel_field',False):
                        continue
                    elif isinstance(f,(babel.BabelCharField,babel.BabelTextField)):
                        self.stream.write(
                            '    if %s is not None: kw.update(bv2kw(%r,%s))\n' % (
                            f.attname,f.attname,f.attname))
                    else:
                        if isinstance(f,models.DecimalField):
                            self.stream.write(
                                '    if %s is not None: %s = Decimal(%s)\n' % (
                                f.attname,f.attname,f.attname))
                        elif isinstance(f,models.ForeignKey) and f.rel.to is ContentType:
                            #~ self.stream.write(
                                #~ '    %s = ContentType.objects.get_for_model(%s).pk\n' % (
                                #~ f.attname,f.attname))
                            self.stream.write(
                                '    %s = new_content_type_id(%s)\n' % (
                                f.attname,f.attname))
                        self.stream.write(
                            '    kw.update(%s=%s)\n' % (f.attname,f.attname))
                            
                self.stream.write('    return %s(**kw)\n\n' % full_model_name(model,'_'))
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
            fields = [f for f,m in model._meta.get_fields_with_model() if m is None]
            fields = [f for f in fields if not getattr(f,'_lino_babel_field',False)]
            self.stream.write('    yield create_%s(%s)\n' % (
                obj._meta.db_table,
                ','.join([self.value2string(obj,f) for f in fields])))
        self.stream.write('\n\ndef objects():\n')
        all_models = self.sort_models(all_models)
        for model in all_models:
            #~ self.stream.write('    for o in %s_objects(): yield o\n' % model._meta.db_table)
            self.stream.write('    yield %s_objects()\n' % model._meta.db_table)
        self.stream.write('\nsettings.LINO.loading_from_dump = True\n')
        self.stream.write('\nsettings.LINO.install_migrations(globals())\n')
        #~ if settings.LINO.migration_module:
            #~ self.stream.write('\n')
            #~ self.stream.write('from %s import install\n' \
                #~ % settings.LINO.migration_module)
            #~ self.stream.write('install(globals())\n')
            
    def sort_models(self,unsorted):
        sorted = []
        hope = True
        """
        20121120 if we convert the list to a set, we gain some performance 
        for the ``in`` tests, but we obtain a random sorting order for all 
        independent models, making the double dump test less evident.
        """
        #~ 20121120 unsorted = set(unsorted)
        while len(unsorted) and hope:
            hope = False
            guilty = dict()
            #~ print "hope for", [m.__name__ for m in unsorted]
            for model in unsorted:
                deps = set([f.rel.to 
                  for f in model._meta.fields 
                      if f.rel is not None and f.rel.to is not model and f.rel.to in unsorted])
                #~ deps += [m for m in model._meta.parents.keys()]
                for m in sorted:
                    if m in deps:
                        deps.remove(m)
                if len(deps):
                    guilty[model] = deps
                else:
                    sorted.append(model)
                    unsorted.remove(model)
                    hope = True
                    break
                    
                #~ ok = True
                #~ for d in deps:
                    #~ if d in unsorted:
                        #~ ok = False
                #~ if ok:
                    #~ sorted.append(model)
                    #~ unsorted.remove(model)
                    #~ hope = True
                    #~ break
                #~ else:
                    #~ guilty[model] = deps
                #~ print model.__name__, "depends on", [m.__name__ for m in deps]
        if unsorted:
            assert len(unsorted) == len(guilty)
            msg = "There are %d models with circular dependencies :\n" % len(unsorted)
            msg += "- " + '\n- '.join([
                full_model_name(m)+' (depends on %s)' % ", ".join([full_model_name(d) for d in deps]) for m,deps in guilty.items()])
            for ln in msg.splitlines():
                self.stream.write('\n    # %s' % ln)
            dblogger.info(msg)
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
        if isinstance(field,(babel.BabelCharField,babel.BabelTextField)):
            #~ return repr([repr(x) for x in babel.field2args(obj,field.name)])
            return repr(babel.field2args(obj,field.name))
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
            #~ return "'"+full_model_name(ct.model_class())+"'"
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

SUPPORT_EMPTY_FIXTURES = False # trying, but doesn't yet work

if SUPPORT_EMPTY_FIXTURES:
    from lino.utils import AttrDict
    class DummyDeserializedObject(base.DeserializedObject):
        class FakeObject:
            _meta = AttrDict(db_table='')
        object = FakeObject()
        def __init__(self): pass
        def save(self, *args,**kw): pass

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
            """
            """
            m = getattr(obj,'before_dumpy_save',None)
            if m is not None:
                m()
            obj.full_clean()
            obj.save(*args,**kw)
            dblogger.debug("%s has been saved" % obj2str(obj))
            self.deserializer.register_success()
            return True
        #~ except ValidationError,e:
        #~ except ObjectDoesNotExist,e:
        #~ except (ValidationError,ObjectDoesNotExist), e:
        #~ except (ValidationError,ObjectDoesNotExist,IntegrityError), e:
        except Exception, e:
            if not settings.LINO.loading_from_dump:
                # hand-written fixtures are expected to not raise any exception
                dblogger.warning("Failed to save %s:" % obj2str(obj))
                raise
            if False:
              """
              20120906 deactivated this test. also fixtures from dump may yield instances without pk.
              example migrate_from_1_4_10 adds pcsw.Third instances without pk, and which need to 
              get a second chance.
              """
              if obj.pk is None: 
                """
                (no longer true:) 
                presto.tim2lino creates invoices without pk which possibly fail to save 
                on first attempt because their project
                """
                if True:
                    msg = "Failed to save %s without %s: %s." % (
                        obj.__class__,obj._meta.pk.attname,obj2str(obj))
                    dblogger.warning(msg)
                    raise
                else:
                    dblogger.exception(e)
                    raise Exception(msg)
            deps = [f.rel.to for f in obj._meta.fields if f.rel is not None]
            if not deps:
                dblogger.exception(e)
                raise Exception("Failed to save independent %s." % obj2str(obj))
            self.deserializer.register_failure(self,e)
            return False
        #~ except Exception,e:
            #~ dblogger.exception(e)
            #~ raise Exception("Failed to save %s. Abandoned." % obj2str(obj))




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
    
class FlushDeferredObjects: 
    """
    Indicator class object. 
    Fixture may yield a ``dumpy.FlushDeferredObjects`` 
    to indicate that all deferred objects should get saved before going on.
    """
    pass

class DpyDeserializer:
    
    def __init__(self):
        #~ dblogger.info("20120225 DpyDeserializer.__init__()")
        self.save_later = {}
        self.saved = 0
        #~ self.count = 0

  
    def flush_deferred_objects(self):
        """
        Flush the list of deferred objects.
        """
        while self.saved and self.save_later:
            try_again = []
            for msg_objlist in self.save_later.values():
                for objlist in msg_objlist.values():
                    try_again += objlist
            logger.info("Trying again with %d unsaved instances.",
                len(try_again))
            self.save_later = {}
            self.saved = 0
            for obj in try_again:
                obj.try_save() # ,*args,**kw):
                #~ if obj.try_save(): # ,*args,**kw):
                    #~ self.saved += 1
                #~ else:
                    #~ self.save_later.append(obj)
            dblogger.info("Saved %d instances.",self.saved)
            
    def deserialize(self,fp, **options):
        #~ dblogger.info("20120225 DpyDeserializer.deserialize()")
        if isinstance(fp, basestring):
            raise NotImplementedError
        babel.set_language(babel.DEFAULT_LANGUAGE)
        
        #~ self.count += 1
        fqname = 'lino.utils.dumpy_tmp_%s' % hash(self)
        
        if False:
            parts = fp.name.split(os.sep)
            #~ parts = os.path.split(fp.name)
            print parts
            #~ fqname = parts[-1]
            fqname = '.'.join([p for p in parts if not ':' in p])
            assert fqname.endswith(SUFFIX)
            fqname = fqname[:-len(SUFFIX)]
            print fqname
        desc = (SUFFIX,'r',imp.PY_SOURCE)
        module = imp.load_module(fqname, fp, fp.name, desc)
        #~ module = __import__(filename)
        
        def expand(obj):
            if obj is None:
                pass # ignore None values
            elif obj is FlushDeferredObjects:
                self.flush_deferred_objects()
            elif isinstance(obj,models.Model):
                yield FakeDeserializedObject(self,obj)
            elif hasattr(obj,'__iter__'):
            #~ if type(obj) is GeneratorType:
                #~ dblogger.info("20120225 expand iterable %r",obj)
                for o in obj: 
                    for so in expand(o): 
                        yield so
            #~ elif isinstance(obj,MtiChildWrapper):
                # the return value of create_child()
                #~ yield FakeDeserializedObject(self,obj)
                #~ obj.deserializer = self
                #~ yield obj
            else:
                dblogger.warning("Ignored unknown object %r",obj)
                
        dblogger.info("Loading %s...",fp.name)
        if not hasattr(module,'objects'):
            raise Exception("%s has no attribute 'objects'" % fp.name)
        empty_fixture = True
        for obj in module.objects():
            for o in expand(obj): 
                empty_fixture = False
                yield o
        if empty_fixture:
            if SUPPORT_EMPTY_FIXTURES:
                yield DummyDeserializedObject() # avoid Django interpreting empty fixtures as an error
            else:
                """
                To avoid Django interpreting empty fixtures as an error, 
                we yield one object which always exists: the SiteConfig instance
                """
                yield FakeDeserializedObject(self,settings.LINO.site_config)
                #~ raise Exception("""\
#~ Fixture %s decided to not create any object.
#~ We're sorry, but Django doesn't like that. 
#~ See <https://code.djangoproject.com/ticket/18213>.
#~ """ % fp.name)
          
        #~ dblogger.info("Saved %d instances from %s.",self.saved,fp.name)
        
        self.flush_deferred_objects()
        
        if self.save_later:
            count = 0
            s = ''
            for model,msg_objects in self.save_later.items():
                for msg,objects in msg_objects.items():
                    if False: # detailed content of the first object
                        s += "\n- %s %s (%d object(s), e.g. %s)" % (
                          full_model_name(model),msg,len(objects),
                          obj2str(objects[0].object,force_detailed=True))
                    else: # pk of all objects
                        s += "\n- %s %s (%d object(s) with primary key %s)" % (
                          full_model_name(model),msg,len(objects),
                          ', '.join([unicode(o.object.pk) for o in objects]))
                    count += len(objects)
            
            msg = "Abandoning with %d unsaved instances from %s:%s" % (
                count,fp.name,s)
            dblogger.warning(msg)
            """
            Don't raise an exception. The unsaved instances got lost and 
            the loaddata should be done again, but meanwhile the database
            is not necessarily invalid and may be used for further testing.
            """
            #~ raise Exception(msg)
            
        if hasattr(module,'after_load'):
            module.after_load()
        #~ IS_DESERIALIZING = False

    def register_success(self):
        self.saved += 1
        
    def register_failure(self,obj,e):
        msg = force_unicode(e)
        d = self.save_later.setdefault(obj.object.__class__,{})
        l = d.setdefault(msg,[])
        if len(l) == 0:
            dblogger.info("Deferred %s : %s",obj2str(obj.object),msg)
        l.append(obj)

def Deserializer(fp, **options):
    """
    The Deserializer used when ``manage.py loaddata`` encounters a `.py` fixture.
    """
    d = DpyDeserializer()
    return d.deserialize(fp, **options)

