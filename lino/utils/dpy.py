# -*- coding: UTF-8 -*-
# Copyright 2009-2018 Rumma & Ko Ltd
# License: BSD, see file LICENSE for more details.

"""
Defines Lino's **Python serializer and deserializer**.  See
:doc:`Specification </specs/dpy>`.
"""

from __future__ import unicode_literals
from __future__ import print_function
# from future import standard_library
# standard_library.install_aliases()
from builtins import str
from builtins import object
import six

import logging
logger = logging.getLogger(__name__)
from pkg_resources import parse_version as PV


#from io import StringIO
import os
#from os.path import dirname
import imp
#from decimal import Decimal
from unipath import Path
# from lino import AFTER17

from django.conf import settings
from django.db import models

from django.utils import translation
from django.utils.module_loading import import_string
from django.utils.encoding import force_str

#from django.db import IntegrityError
from django.core.serializers import base
from django.core.exceptions import ValidationError
#from django.core.exceptions import ObjectDoesNotExist

#from lino.utils.mldbc.fields import BabelCharField, BabelTextField
#from lino.core.choicelists import ChoiceListField
from lino.core.utils import obj2str, full_model_name

SUFFIX = '.py'


def create_mti_child(parent_model, pk, child_model, **kw):
    """Similar to :func:`lino.utils.mti.insert_child`, but for usage in
    Python dumps (generated by :manage:`dump2py`).

    The difference is very tricky.  The return value here is an
    "almost normal" model instance, whose `save` and `full_clean`
    methods have been hacked.  These are the only methods that will be
    called by :class:`Deserializer`.  You should not use this instance
    for anything else and throw it away when the save() has been
    called.

    """
    parent_link_field = child_model._meta.parents.get(parent_model, None)
    if parent_link_field is None:
        raise ValidationError("A %s cannot be parent for a %s" % (
            parent_model.__name__, child_model.__name__))
    pfields = {}
    for f in parent_model._meta.fields:
        if f.name in kw:
            pfields[f.name] = kw.pop(f.name)
    kw[parent_link_field.name + "_id"] = pk
    # if ignored:
    #     raise Exception(
    #         "create_mti_child() %s %s from %s : "
    #         "ignored non-local fields %s" % (
    #             child_model.__name__,
    #             pk,
    #             parent_model.__name__,
    #             ignored))

    child_obj = child_model(**kw)

    if len(pfields):
        parent_obj = parent_model.objects.get(pk=pk)
        for k, v in pfields.items():
            setattr(parent_obj, k, v)
        parent_obj.full_clean()
        parent_obj.save()

    def full_clean(*args, **kw):
        pass

    def save(*args, **kw):
        kw.update(raw=True, force_insert=True)
        child_obj.save_base(**kw)

    child_obj.save = save
    child_obj.full_clean = full_clean
    return child_obj


SUPPORT_EMPTY_FIXTURES = False  # trying, but doesn't yet work

if SUPPORT_EMPTY_FIXTURES:
    from django_site.utils import AttrDict

    class DummyDeserializedObject(base.DeserializedObject):

        class FakeObject(object):
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

    def __init__(self, deserializer, object, **kw):
        super(FakeDeserializedObject,self).__init__(object, deserializer, **kw)
        self.object = object
        # self.name = name
        self.deserializer = deserializer

    def save(self, *args, **kw):
        """
        """
        # print 'dpy.py',self.object
        # logger.info("Loading %s...",self.name)

        self.try_save(*args, **kw)
        # if self.try_save(*args,**kw):
            # self.deserializer.saved += 1
        # else:
            # self.deserializer.save_later.append(self)

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
                m(self.deserializer)
            if not self.deserializer.quick:
                try:
                    obj.full_clean()
                except ValidationError as e:
                    # raise Exception("{0} : {1}".format(obj2str(obj), e))
                    raise  # Exception("{0} : {1}".format(obj2str(obj), e))
            obj.save(*args, **kw)
            logger.debug("%s has been saved" % obj2str(obj))
            self.deserializer.register_success()
            return True
        # except ValidationError,e:
        # except ObjectDoesNotExist,e:
        # except (ValidationError,ObjectDoesNotExist), e:
        # except (ValidationError,ObjectDoesNotExist,IntegrityError), e:
        except Exception as e:
            if True:
                if not settings.SITE.loading_from_dump:
                    # hand-written fixtures are expected to yield in savable
                    # order
                    logger.warning("Failed to save %s from manual fixture:" % obj2str(obj))
                    raise
            deps = [f.remote_field.model for f in obj._meta.fields
                    if f.remote_field and f.remote_field.model]
            if not deps:
                logger.exception(e)
                raise Exception(
                    "Failed to save independent %s." % obj2str(obj))
            self.deserializer.register_failure(self, e)
            return False
        # except Exception,e:
            # logger.exception(e)
            # raise Exception("Failed to save %s. Abandoned." % obj2str(obj))


class Serializer(base.Serializer):
    """Serializes a QuerySet to a py stream.

    Usage: ``manage.py dumpdata --format py``

    DEPRECATED. The problem with this approach is that a serializer
    creates -by definition- one single file. And Python needs
    -understandably- to load a module completely into memory before it
    can be executed.  Use :manage:`dump2py` instead.

    """

    internal_use_only = False

    def serialize(self, queryset, **options):
        raise NotImplementedError("Don't use dumpdata but `dump2py`")


class FlushDeferredObjects(object):

    """
    Indicator class object.
    Fixture may yield a `FlushDeferredObjects`
    to indicate that all deferred objects should get saved before going on.
    """
    pass


class LoaderBase(object):

    quick = False
    source_version = None
    max_deferred_objects = 1000

    def __init__(self):
        # logger.info("20120225 DpyLoader.__init__()")
        self.save_later = {}
        self.reported_tracebacks = set()
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
            for msg_objlist in list(self.save_later.values()):
                for objlist in list(msg_objlist.values()):
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
        # if type(obj) is GeneratorType:
            # logger.info("20120225 expand iterable %r",obj)
            for o in obj:
                for so in self.expand(o):
                    yield so
        # elif isinstance(obj,MtiChildWrapper):
            # the return value of create_mti_child()
            # yield FakeDeserializedObject(self,obj)
            # obj.deserializer = self
            # yield obj
        else:
            logger.warning("Ignored unknown object %r", obj)

    def register_success(self):
        self.saved += 1
        self.count_objects += 1

    def register_failure(self, obj, e):
        msg = force_str(e)
        d = self.save_later.setdefault(obj.object.__class__, {})
        l = d.setdefault(msg, [])
        count = len(l)
        if count == 0:
            logger.info("Deferred %s : %s", obj2str(obj.object), msg)
        elif count > self.max_deferred_objects:
            self.flush_deferred_objects()
            if count > self.max_deferred_objects + 1:
                raise Exception(
                    "More than {} deferred objects".format(
                        self.max_deferred_objects))
        l.append(obj)
        # report a full traceback, but only once per model and
        # exception type:
        k = (obj.object.__class__, e.__class__)
        if k not in self.reported_tracebacks:
            logger.exception(e)
            self.reported_tracebacks.add(k)

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

        # logger.info("Loaded %d objects", self.count_objects)

        if self.save_later:
            count = 0
            s = ''
            for model, msg_objects in list(self.save_later.items()):
                for msg, objects in list(msg_objects.items()):
                    if False:  # detailed content of the first object
                        s += "\n- %s %s (%d object(s), e.g. %s)" % (
                            full_model_name(model), msg, len(objects),
                            obj2str(objects[0].object, force_detailed=True))
                    else:  # pk of all objects
                        s += "\n- %s %s (%d object(s) with primary key %s)" % (
                            full_model_name(model), msg, len(objects),
                            ', '.join([str(o.object.pk) for o in objects]))
                    count += len(objects)
            msg = "Abandoning with {} unsaved instances:{}"
            logger.warning(msg.format(count, s))

            # Don't raise an exception. The unsaved instances got lost and
            # the loaddata should be done again, but meanwhile the database
            # is not necessarily invalid and may be used for further testing.
            # And anyway, loaddata would catch it and still continue.
            # raise Exception(msg)

        settings.SITE.loading_from_dump = False
        # reset to False because the same SITE might get reused by
        # Django test runner for other test cases.



class DpyLoader(LoaderBase):
    """Instantiated by :xfile:`restore.py`.

    """
    def __init__(self, globals_dict, quick=None):
        if quick is not None:
            self.quick = quick
        self.globals_dict = globals_dict
        super(DpyLoader, self).__init__()
        self.source_version = globals_dict['SOURCE_VERSION']
        site = globals_dict['settings'].SITE
        site.startup()
        site.install_migrations(self)

    def save(self, obj):
        for o in self.expand(obj):
            o.try_save()


class DpyDeserializer(LoaderBase):
    """The Django deserializer for :ref:`dpy`.

    Note that this deserializer explicitly ignores fixtures whose
    source file is located in the current directory because i the case
    of `.py` files this can lead to side effects when importing them.
    See e.g. :ticket:`1029`.  We consider it an odd behaviour of
    Django to search for fixtures also in the current directory (and
    not, as `documented
    <https://docs.djangoproject.com/en/1.11/howto/initial-data/#where-django-finds-fixture-files>`__,
    in the `fixtures` subdirs of plugins and the optional
    :setting:`FIXTURE_DIRS`).

    """

    def deserialize(self, fp, **options):
        # logger.info("20120225 DpyLoader.deserialize()")
        if isinstance(fp, six.string_types):
            raise NotImplementedError

        # ignore fixtures in current directory.
        p1 = Path(fp.name).parent.absolute().resolve()
        p2 = Path(os.getcwd()).absolute().resolve()
        if p1 == p2:
            return

        translation.activate(settings.SITE.get_default_language())

        # self.count += 1
        fqname = 'lino.dpy_tmp_%s' % abs(hash(fp.name))

        if False:
            parts = fp.name.split(os.sep)
            # parts = os.path.split(fp.name)
            print(parts)
            # fqname = parts[-1]
            fqname = '.'.join([p for p in parts if ':' not in p])
            assert fqname.endswith(SUFFIX)
            fqname = fqname[:-len(SUFFIX)]
            print(fqname)

        desc = (SUFFIX, 'r', imp.PY_SOURCE)
        # logger.info("20160817 %s...", options)
        logger.info("Loading data from %s", fp.name)

        module = imp.load_module(fqname, fp, fp.name, desc)
        # module = __import__(filename)

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

#         # Since Django 1.7 no longer considers empty fixtures as an
#         # error, we don't need to use our trick of yielding the
#         # SiteConfig instance. That trick sometimes could cause side
#         # effects.
#         if empty_fixture and not AFTER17:
#             if SUPPORT_EMPTY_FIXTURES:
#                 # avoid Django interpreting empty fixtures as an error
#                 yield DummyDeserializedObject()
#             else:
#                 # To avoid Django interpreting empty fixtures as an
#                 # error, we yield one object which always exists: the
#                 # SiteConfig instance.

#                 # Oops, that will fail in lino_welfare if the company
#                 # pointed to by SiteConfig.job_office had been
#                 # deferred.
#                 if settings.SITE.site_config:
#                     yield FakeDeserializedObject(
#                         self, settings.SITE.site_config)
#                 else:
#                     raise Exception("""\
# Fixture %s decided to not create any object.
# We're sorry, but Django doesn't like that.
# See <https://code.djangoproject.com/ticket/18213>.
# """ % module.__name__)

        # logger.info("Saved %d instances from %s.",self.saved,fp.name)

        self.finalize()


def Deserializer(fp, **options):
    """The Deserializer used when ``manage.py loaddata`` encounters a
    `.py` fixture.

    """
    d = DpyDeserializer()
    return d.deserialize(fp, **options)


class Migrator(object):
    """The SITE's Migrator class is instantiated by `install_migrations`.

    If :attr:`migration_class<lino.core.site.Site.migration_class>` is
    `None` (the default), then this class will be
    instantiated. Applications may define their own Migrator class
    which should be a subclasss of this.

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
    """
    Install "migrators" into the given global namespace.

    Python dumps are generated with one line near the end of their
    :xfile:`restore.py` file which calls this method, passing it their
    global namespace::

      settings.SITE.install_migrations(globals())

    A dumped fixture should always call this, even if there is no
    version change and no data migration, because this also does
    certain other things:

    - set :attr:`loading_from_dump
      <lino.core.site.Site.loading_from_dump>` to `True`

    - remove any Permission and Site objects that might have been
      generated by `post_syncdb` signal if these apps are installed.
    """
    globals_dict = loader.globals_dict

    self.loading_from_dump = True

    # if self.is_installed('auth'):
    #     from django.contrib.auth.models import Permission
    #     Permission.objects.all().delete()
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
        mc = import_string(self.migration_class)
        migrator = mc(self, loader)
    else:
        migrator = self

    while True:
        from_version = globals_dict['SOURCE_VERSION']
        funcname = 'migrate_from_' + from_version.replace('.', '_')

        m = getattr(migrator, funcname, None)

        if m is not None:
            # logger.info("Found %s()", funcname)
            to_version = m(globals_dict)
            if not isinstance(to_version, six.string_types):
                raise Exception("Oops, %s didn't return a string!" % m)
            if PV(to_version) <= PV(from_version):
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


def unused_load_fixture_from_module(m, **options):
    """No longer used in unit tests to manually load a given fixture
module.

    """
    # filename = m.__file__[:-1]
    # print filename
    # assert filename.endswith('.py')
    # fp = open(filename)
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


# from functools import wraps

def override(globals_dict):
    """A decorator to be applied when redefining, in a
    :meth:`migrate_from_VERSION` method, one of the
    :func:`create_APP_MODEL` functions defined in the
    :xfile:`restore.py` file of a dump.

    """
    def override_decorator(func):
        if func.__name__ not in globals_dict:
            raise Exception("Cannot override {}".format(func))
        globals_dict[func.__name__] = func
        # @wraps(func)
        # def wrapper(name):
        #     if func.__name__ not in globals_dict:
        #         raise Exception("Cannot override {}".format(func))
        #     globals_dict[func.__name__] = func
        # return wrapper
    return override_decorator
