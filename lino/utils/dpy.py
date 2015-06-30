# -*- coding: UTF-8 -*-
# Copyright 2009-2015 by Luc Saffre.
# License: BSD, see file LICENSE for more details.

"""
Documented in :ref:`dpy`.

"""

from __future__ import unicode_literals

import logging
logger = logging.getLogger(__name__)


from StringIO import StringIO
import os
import imp
from decimal import Decimal


from django.conf import settings
from django.db import models

from django.utils.module_loading import import_by_path

from django.db import IntegrityError
from django.db.models.fields import NOT_PROVIDED
from django.core.serializers import base
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.contrib.contenttypes.models import ContentType
from django.contrib.sessions.models import Session
from django.utils.encoding import smart_unicode, is_protected_type, force_unicode
from django.utils import translation

from lino.utils.mldbc.fields import BabelCharField, BabelTextField
from lino.core.utils import obj2str, sorted_models_list, full_model_name

SUFFIX = '.py'


def create_mti_child(parent_model, pk, child_model, **kw):
    """Similar to :func:`lino.utils.mti.insert_child`, but very tricky.
    Used in Python dumps.

    The return value is an "almost normal" model instance, whose
    `save` and `full_clean` methods have been hacked.  These are the
    only methods that will be called by :class:`Deserializer`.  You
    should not use this instance for anything else and throw it away
    when the save() has been called.

    """
    parent_link_field = child_model._meta.parents.get(parent_model, None)
    if parent_link_field is None:
        raise ValidationError("A %s cannot be parent for a %s" % (
            parent_model.__name__, child_model.__name__))
    ignored = {}
    for f in parent_model._meta.fields:
        if f.name in kw:
            ignored[f.name] = kw.pop(f.name)
    kw[parent_link_field.name + "_id"] = pk
    if ignored:
        raise Exception(
            "create_mti_child() %s %s from %s : "
            "ignored non-local fields %s" % (
                child_model.__name__,
                pk,
                parent_model.__name__,
                ignored))
    child_obj = child_model(**kw)

    def full_clean(*args, **kw):
        pass

    def save(*args, **kw):
        kw.update(raw=True, force_insert=True)
        child_obj.save_base(**kw)

    child_obj.save = save
    child_obj.full_clean = full_clean
    return child_obj


class Serializer(base.Serializer):
    """Serializes a QuerySet to a py stream.

    Usage: ``manage.py dumpdata --format py``

    DEPRECATED. The problem with this approach is that a serializer
    creates -by definition- one single file. And Python needs
    -understandably- to load a module completely into memory before it
    can be executed.  Use :manage:`dump2py` instead.

    """

    internal_use_only = False

    write_preamble = True  # may be set to False e.g. by testcases
    models = None

    def serialize(self, queryset, **options):
        self.options = options

        self.stream = options.get("stream", StringIO())
        self.selected_fields = options.get("fields")
        self.use_natural_keys = options.get("use_natural_keys", False)
        if self.write_preamble:
            current_version = settings.SITE.version
            if '+' in current_version:
                logger.warning(
                    "Dumpdata from intermediate version %s" % current_version)

            self.stream.write('# -*- coding: UTF-8 -*-\n')
            self.stream.write('''\
"""
This is a `Python dump created using %s.
''' % settings.SITE.using_text())
            #~ self.stream.write(settings.SITE.welcome_text())
            self.stream.write('''
"""
from __future__ import unicode_literals
''')
            self.stream.write('SOURCE_VERSION = %r\n' % str(current_version))
            self.stream.write('from decimal import Decimal\n')
            self.stream.write('from datetime import datetime as dt\n')
            self.stream.write('from datetime import time,date\n')
            self.stream.write('from lino.utils.dpy import create_mti_child\n')
            self.stream.write('from lino.utils.dbutils import resolve_model\n')
            self.stream.write(
                'from lino.modlib.contenttypes.models import ContentType\n')
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
            #~ s = ','.join([
              #~ '%s=values[%d]' % (k,i)
                #~ for i,k in enumerate(settings.SITE.AVAILABLE_LANGUAGES)])
            s = ','.join([
                '%s=values[%d]' % (lng.name, lng.index)
                for lng in settings.SITE.languages])
            self.stream.write('''
def bv2kw(fieldname,values):
    """
    Needed if `Site.languages` changed between dumpdata and loaddata
    """
    return settings.SITE.babelkw(fieldname,%s)
    
''' % s)
        #~ model = queryset.model
        if self.models is None:
            self.models = sorted_models_list()  # models.get_models()
        if self.write_preamble:
            for model in self.models:
                self.stream.write('%s = resolve_model("%s")\n' % (
                    full_model_name(model, '_'), full_model_name(model)))
        self.stream.write('\n')
        for model in self.models:
            fields = [f for f,
                      m in model._meta.get_fields_with_model() if m is None]
            for f in fields:
                if getattr(f, 'auto_now_add', False):
                    raise Exception("%s.%s.auto_now_add is True : values will be lost!" % (
                        full_model_name(model), f.name))
            field_names = [f.attname for f in fields
                           if not getattr(f, '_lino_babel_field', False)]
            self.stream.write('def create_%s(%s):\n' % (
                model._meta.db_table, ', '.join(field_names)))
            if model._meta.parents:
                if len(model._meta.parents) != 1:
                    msg = "%s : model._meta.parents is %r" % (
                        model, model._meta.parents)
                    raise Exception(msg)
                pm, pf = model._meta.parents.items()[0]
                child_fields = [f for f in fields if f != pf]
                if child_fields:
                    attrs = ',' + ','.join([
                        '%s=%s' % (f.attname, f.attname)
                        for f in child_fields])
                else:
                    attrs = ''
                tpl = '    return create_mti_child(%s, %s, %s%s)\n'
                self.stream.write(tpl % (
                    full_model_name(pm, '_'),
                    pf.attname, full_model_name(model, '_'), attrs))
            else:
                self.stream.write("    kw = dict()\n")
                for f in fields:
                    if getattr(f, '_lino_babel_field', False):
                        continue
                    elif isinstance(f, (BabelCharField, BabelTextField)):
                        tpl = '    if %s is not None:'
                        tpl += ' kw.update(bv2kw(%r, %s))\n'
                        self.stream.write(
                            tpl % (f.attname, f.attname, f.attname))
                    else:
                        if isinstance(f, models.DecimalField):
                            self.stream.write(
                                '    if %s is not None: %s = Decimal(%s)\n' % (
                                    f.attname, f.attname, f.attname))
                        elif isinstance(f, models.ForeignKey) and f.rel.to is ContentType:
                            #~ self.stream.write(
                                #~ '    %s = ContentType.objects.get_for_model(%s).pk\n' % (
                                #~ f.attname,f.attname))
                            self.stream.write(
                                '    %s = new_content_type_id(%s)\n' % (
                                    f.attname, f.attname))
                        self.stream.write(
                            '    kw.update(%s=%s)\n' % (f.attname, f.attname))

                self.stream.write('    return %s(**kw)\n\n' %
                                  full_model_name(model, '_'))
        #~ self.start_serialization()
        self.stream.write('\n')
        model = None
        all_models = []
        for obj in queryset:
            if isinstance(obj, ContentType):
                continue
            if isinstance(obj, Session):
                continue
            #~ if isinstance(obj,Permission): continue
            if obj.__class__ != model:
                model = obj.__class__
                if model in all_models:
                    raise Exception("%s instances weren't grouped!" % model)
                all_models.append(model)
                self.stream.write('\ndef %s_objects():\n' %
                                  model._meta.db_table)
            fields = [f for f,
                      m in model._meta.get_fields_with_model() if m is None]
            fields = [
                f for f in fields if not getattr(f, '_lino_babel_field', False)]
            self.stream.write('    yield create_%s(%s)\n' % (
                obj._meta.db_table,
                ','.join([self.value2string(obj, f) for f in fields])))
        self.stream.write('\n\ndef objects():\n')
        all_models = self.sort_models(all_models)
        for model in all_models:
            #~ self.stream.write('    for o in %s_objects(): yield o\n' % model._meta.db_table)
            self.stream.write('    yield %s_objects()\n' %
                              model._meta.db_table)
        # self.stream.write('\nsettings.SITE.install_migrations(globals())\n')

    def sort_models(self, unsorted):
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
            msg = "There are %d models with circular dependencies :\n" % len(
                unsorted)
            msg += "- " + '\n- '.join([
                full_model_name(m) + ' (depends on %s)' % ", ".join([full_model_name(d) for d in deps]) for m, deps in guilty.items()])
            for ln in msg.splitlines():
                self.stream.write('\n    # %s' % ln)
            logger.info(msg)
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
        if isinstance(field, (BabelCharField, BabelTextField)):
            return repr(settings.SITE.field2args(obj, field.name))
        value = field._get_val_from_obj(obj)
        # Protected types (i.e., primitives like None, numbers, dates,
        # and Decimals) are passed through as is. All other values are
        # converted to string first.
        if value is None:
        #~ if value is None or value is NOT_PROVIDED:
            return 'None'
        if isinstance(field, models.DateTimeField):
            d = value
            return 'dt(%d,%d,%d,%d,%d,%d)' % (
                d.year, d.month, d.day, d.hour, d.minute, d.second)
        if isinstance(field, models.TimeField):
            d = value
            return 'time(%d,%d,%d)' % (d.hour, d.minute, d.second)
        if isinstance(field, models.ForeignKey) and field.rel.to is ContentType:
            ct = ContentType.objects.get(pk=value)
            return full_model_name(ct.model_class(), '_')
            #~ return "'"+full_model_name(ct.model_class())+"'"
            #~ return repr(tuple(value.app_label,value.model))
        if isinstance(field, models.DateField):
            d = value
            return 'date(%d,%d,%d)' % (d.year, d.month, d.day)
            #~ return 'i2d(%4d%02d%02d)' % (d.year,d.month,d.day)
        if isinstance(value, (float, Decimal)):
            return repr(str(value))
        if isinstance(value, (int, long)):
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
                    related = smart_unicode(
                        getattr(related, field.rel.field_name), strings_only=True)
        self._current[field.name] = related

    def handle_m2m_field(self, obj, field):
        if field.rel.through._meta.auto_created:
            if self.use_natural_keys and hasattr(field.rel.to, 'natural_key'):
                m2m_value = lambda value: value.natural_key()
            else:
                m2m_value = lambda value: smart_unicode(
                    value._get_pk_val(), strings_only=True)
            self._current[field.name] = [m2m_value(related)
                                         for related in getattr(obj, field.name).iterator()]

    #~ def getvalue(self):
        #~ return self.objects

SUPPORT_EMPTY_FIXTURES = False  # trying, but doesn't yet work

if SUPPORT_EMPTY_FIXTURES:
    from django_site.utils import AttrDict

    class DummyDeserializedObject(base.DeserializedObject):

        class FakeObject:
            _meta = AttrDict(db_table='')
        object = FakeObject()

        def __init__(self):
            pass

        def save(self, *args, **kw):
            pass


class FakeDeserializedObject(base.DeserializedObject):
    """Imitates DeserializedObject required by loaddata.

    Unlike normal DeserializedObject, we *don't want* to bypass
    pre_save and validation methods on the individual objects.

    """

    def __init__(self, deserializer, object):
        self.object = object
        #~ self.name = name
        self.deserializer = deserializer

    def save(self, *args, **kw):
        """
        """
        #~ print 'dpy.py',self.object
        #~ logger.info("Loading %s...",self.name)

        self.try_save(*args, **kw)
        #~ if self.try_save(*args,**kw):
            #~ self.deserializer.saved += 1
        #~ else:
            #~ self.deserializer.save_later.append(self)

    def try_save(self, *args, **kw):
        """Try to save the specified Model instance `obj`. Return `True`
        on success, `False` if this instance wasn't saved and should be
        deferred.
        """
        obj = self.object
        try:
            """
            """
            m = getattr(obj, 'before_dumpy_save', None)
            if m is not None:
                m()
            if not self.deserializer.quick:
                try:
                    obj.full_clean()
                except ValidationError as e:
                    raise  # Exception("{0} : {1}".format(obj2str(obj), e))
            obj.save(*args, **kw)
            logger.debug("%s has been saved" % obj2str(obj))
            self.deserializer.register_success()
            return True
        #~ except ValidationError,e:
        #~ except ObjectDoesNotExist,e:
        #~ except (ValidationError,ObjectDoesNotExist), e:
        #~ except (ValidationError,ObjectDoesNotExist,IntegrityError), e:
        except Exception, e:
            if True:
                if not settings.SITE.loading_from_dump:
                    # hand-written fixtures are expected to yield in savable
                    # order
                    logger.warning("Failed to save %s:" % obj2str(obj))
                    raise
            deps = [f.rel.to for f in obj._meta.fields if f.rel is not None]
            if not deps:
                logger.exception(e)
                raise Exception(
                    "Failed to save independent %s." % obj2str(obj))
            self.deserializer.register_failure(self, e)
            return False
        #~ except Exception,e:
            #~ logger.exception(e)
            #~ raise Exception("Failed to save %s. Abandoned." % obj2str(obj))


class FlushDeferredObjects:

    """
    Indicator class object.
    Fixture may yield a `FlushDeferredObjects`
    to indicate that all deferred objects should get saved before going on.
    """
    pass


class LoaderBase(object):

    quick = False

    def __init__(self):
        #~ logger.info("20120225 DpyLoader.__init__()")
        self.save_later = {}
        self.saved = 0
        self.count_objects = 0
        self.AFTER_LOAD_HANDLERS = []
        # populated by Migrator.after_load(), but remains empty in a DpyDeserializer
        self.before_load_handlers = []

    def flush_deferred_objects(self):
        """
        Flush the list of deferred objects.
        """
        while self.saved and self.save_later:
            try_again = []
            for msg_objlist in self.save_later.values():
                for objlist in msg_objlist.values():
                    try_again += objlist
            logger.info("Trying to save %d deferred objects.",
                        len(try_again))
            self.save_later = {}
            self.saved = 0
            for obj in try_again:
                obj.try_save()  # ,*args,**kw):
            logger.info("Saved %d objects.", self.saved)

    def expand(self, obj):
        if obj is None:
            pass  # ignore None values
        elif obj is FlushDeferredObjects:
            self.flush_deferred_objects()
        elif isinstance(obj, models.Model):
            yield FakeDeserializedObject(self, obj)
        elif hasattr(obj, '__iter__'):
        #~ if type(obj) is GeneratorType:
            #~ logger.info("20120225 expand iterable %r",obj)
            for o in obj:
                for so in self.expand(o):
                    yield so
        #~ elif isinstance(obj,MtiChildWrapper):
            # the return value of create_mti_child()
            #~ yield FakeDeserializedObject(self,obj)
            #~ obj.deserializer = self
            #~ yield obj
        else:
            logger.warning("Ignored unknown object %r", obj)

    def register_success(self):
        self.saved += 1
        self.count_objects += 1

    def register_failure(self, obj, e):
        msg = force_unicode(e)
        d = self.save_later.setdefault(obj.object.__class__, {})
        l = d.setdefault(msg, [])
        if len(l) == 0:
            logger.info("Deferred %s : %s", obj2str(obj.object), msg)
        l.append(obj)

    def initialize(self):
        """To be called after initdb and before starting to load the dumped
data."""
        for h in self.before_load_handlers:
            logger.info("Running before_load handler %s", h.__doc__)
            h(self)

    def finalize(self):
        """
        """
        self.flush_deferred_objects()

        if len(self.AFTER_LOAD_HANDLERS):
            logger.info(
                "Finalize %d after_load handlers",
                len(self.AFTER_LOAD_HANDLERS))

        for h in self.AFTER_LOAD_HANDLERS:
            logger.info("Running after_load handler %s", h.__doc__)
            h(self)

        logger.info("Loaded %d objects", self.count_objects)
    
        if self.save_later:
            count = 0
            s = ''
            for model, msg_objects in self.save_later.items():
                for msg, objects in msg_objects.items():
                    if False:  # detailed content of the first object
                        s += "\n- %s %s (%d object(s), e.g. %s)" % (
                            full_model_name(model), msg, len(objects),
                            obj2str(objects[0].object, force_detailed=True))
                    else:  # pk of all objects
                        s += "\n- %s %s (%d object(s) with primary key %s)" % (
                            full_model_name(model), msg, len(objects),
                            ', '.join([unicode(o.object.pk) for o in objects]))
                    count += len(objects)

            msg = "Abandoning with %d unsaved instances:%s" % (count, s)
            logger.warning(msg)

            # Don't raise an exception. The unsaved instances got lost and
            # the loaddata should be done again, but meanwhile the database
            # is not necessarily invalid and may be used for further testing.
            # And anyway, loaddata would catch it and still continue.
            # raise Exception(msg)


class DpyLoader(LoaderBase):
    """Instantiated by `restore.py`.

    """
    def __init__(self, globals_dict):
        self.globals_dict = globals_dict
        super(DpyLoader, self).__init__()
        site = globals_dict['settings'].SITE
        site.startup()
        site.install_migrations(self)

    def save(self, obj):
        for o in self.expand(obj):
            o.try_save()


class DpyDeserializer(LoaderBase):
    """The Django deserializer for :ref:`dpy`.

    """

    def deserialize(self, fp, **options):
        #~ logger.info("20120225 DpyLoader.deserialize()")
        if isinstance(fp, basestring):
            raise NotImplementedError

        translation.activate(settings.SITE.get_default_language())

        #~ self.count += 1
        fqname = 'lino.dpy_tmp_%s' % hash(self)

        if False:
            parts = fp.name.split(os.sep)
            #~ parts = os.path.split(fp.name)
            print parts
            #~ fqname = parts[-1]
            fqname = '.'.join([p for p in parts if not ':' in p])
            assert fqname.endswith(SUFFIX)
            fqname = fqname[:-len(SUFFIX)]
            print fqname
        desc = (SUFFIX, 'r', imp.PY_SOURCE)
        logger.info("Loading %s...", fp.name)

        module = imp.load_module(fqname, fp, fp.name, desc)
        #~ module = __import__(filename)

        for o in self.deserialize_module(module, **options):
            yield o

    def deserialize_module(self, module, **options):

        self.initialize()

        empty_fixture = True
        objects = getattr(module, 'objects', None)
        if objects is None:
            logger.info("Fixture %s has no attribute 'objects'" %
                        module.__name__)
        else:

            for obj in objects():
                for o in self.expand(obj):
                    empty_fixture = False
                    yield o

        if empty_fixture:
            if SUPPORT_EMPTY_FIXTURES:
                # avoid Django interpreting empty fixtures as an error
                yield DummyDeserializedObject()
            else:
                # To avoid Django interpreting empty fixtures as an
                # error, we yield one object which always exists: the
                # SiteConfig instance.

                # Oops, that will fail in lino_welfare if the company
                # pointed to by SiteConfig.job_office had been
                # deferred.
                if settings.SITE.site_config:
                    yield FakeDeserializedObject(
                        self, settings.SITE.site_config)
                else:
                    raise Exception("""\
Fixture %s decided to not create any object.
We're sorry, but Django doesn't like that.
See <https://code.djangoproject.com/ticket/18213>.
""" % module.__name__)

        #~ logger.info("Saved %d instances from %s.",self.saved,fp.name)

        self.finalize()


def Deserializer(fp, **options):
    """The Deserializer used when ``manage.py loaddata`` encounters a
    `.py` fixture.

    """
    d = DpyDeserializer()
    return d.deserialize(fp, **options)


class Migrator(object):
    """The SITE's Migrator class is instantiated by `install_migrations`.

    If :setting:`migration_class` is None (the default), then this
    class will be instantiated. Applications may define their own
    Migrator class which should be a subclasss of this.

    """
    def __init__(self, site, loader):
        self.site = site
        self.loader = loader

    def after_load(self, todo):
        """Declare a function to be called after all data has been loaded."""
        assert callable(todo)
        # al = self.globals_dict['AFTER_LOAD_HANDLERS']
        self.loader.AFTER_LOAD_HANDLERS.append(todo)

    def before_load(self, todo):
        """Declare a function to be called before loading dumped data."""
        assert callable(todo)
        self.loader.before_load_handlers.append(todo)


def install_migrations(self, loader):
    """Python dumps are generated with one line near the end of their
    `restore.py` file which calls this method, passing it their global
    namespace::

      settings.SITE.install_migrations(globals())

    A dumped fixture should always call this, even if there is no
    version change and no data migration, because this also does
    certain other things:

    - set :setting:`loading_from_dump` to `True`
    - remove any Permission and Site objects that might have been
      generated by `post_syncdb` signal if these apps are installed.

    """
    globals_dict = loader.globals_dict

    self.loading_from_dump = True

    if self.is_installed('auth'):
        from django.contrib.auth.models import Permission
        Permission.objects.all().delete()
    if self.is_installed('sites'):
        from django.contrib.sites.models import Site
        Site.objects.all().delete()

    current_version = self.version

    if current_version is None:
        logger.info("Unversioned Site instance : no database migration")
        return

    if globals_dict['SOURCE_VERSION'] == current_version:
        logger.info("Source version is %s : no migration needed",
                    current_version)
        return

    if self.migration_class is not None:
        mc = import_by_path(self.migration_class)
        migrator = mc(self, loader)
    else:
        migrator = self

    while True:
        from_version = globals_dict['SOURCE_VERSION']
        funcname = 'migrate_from_' + from_version.replace('.', '_')

        m = getattr(migrator, funcname, None)

        if m is not None:
            #~ logger.info("Found %s()", funcname)
            to_version = m(globals_dict)
            if not isinstance(to_version, basestring):
                raise Exception("Oops, %s didn't return a string!" % m)
            if to_version <= from_version:
                raise Exception(
                    "Oops, %s tries to migrate from version %s to %s ?!" %
                    (m, from_version, to_version))
            msg = "Migrating from version %s to %s" % (
                from_version, to_version)
            if m.__doc__:
                msg += ":\n" + m.__doc__
            logger.info(msg)
            globals_dict['SOURCE_VERSION'] = to_version
        else:
            if from_version != current_version:
                logger.warning(
                    "No method for migrating from version %s to %s",
                    from_version, current_version)
            break


def load_fixture_from_module(m, **options):
    """
    Used in unit tests to manually load a given fixture module.
    E.g. in Lino `/tutorials/tables/index`.
    """
    #~ filename = m.__file__[:-1]
    #~ print filename
    #~ assert filename.endswith('.py')
    #~ fp = open(filename)
    d = DpyDeserializer()
    for o in d.deserialize_module(m, **options):
        o.save()

    # 20140506 Don't remember why the following was. But it disturbed
    # in Lino `/tutorials/tables/index`.

    # if d.saved != 1:
    #     logger.info("20140506 Loaded %d objects", d.saved)
    #     raise Exception("Failed to load Python fixture from module %s" %
    #                     m.__name__)
    # return d
