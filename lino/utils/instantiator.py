# Copyright 2009-2018 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""Defines the :class:`Instantiator` class and some other utilities
used for generating database objects in :ref:`python fixtures <dpy>`.

Example values:

>>> import json
>>> s = '<a href="javascript:Lino.pcsw.Clients.detail.run(\
null,{ &quot;record_id&quot;: 116 })">BASTIAENSEN Laurent (116)</a>'
>>> print(json.dumps(GFK_HACK.match(s).groups()))
["pcsw.Clients", "116"]

>>> s = '<a href="javascript:Lino.cal.Guests.detail.run(\
null,{ &quot;record_id&quot;: 6 })">Gast #6 ("Termin #51")</a>'
>>> print(json.dumps(GFK_HACK.match(s).groups()))
["cal.Guests", "6"]

"""

from __future__ import unicode_literals
from __future__ import print_function
from builtins import str
import six
from builtins import object


import re
GFK_HACK = re.compile(r'^<a href="javascript:Lino\.(\w+\.\w+)\.detail\.run\(.*,\{ &quot;record_id&quot;: (\w+) \}\)">.*</a>$')

import logging
logger = logging.getLogger(__name__)


import decimal
import datetime
from dateutil import parser as dateparser

from django.db import models
from django.conf import settings

from lino.core.utils import resolve_model, UnresolvedModel

from lino.utils import i2d  # for backward compatibility of .py fixtures
from lino.core.utils import obj2str
from lino.core.fields import make_remote_field, RemoteField

class DataError(Exception):
    pass


class Converter(object):

    def __init__(self, field):
        self.field = field

    def convert(self, **kw):
        return kw


class LookupConverter(Converter):

    """
    A Converter for ForeignKey and ManyToManyField. 
    If the lookup_field is a BabelField, then it tries all available languages.
    """

    def __init__(self, field, lookup_field):
        Converter.__init__(self, field)
        model = field.remote_field.model
        if lookup_field == 'pk':
            self.lookup_field = model._meta.pk
        else:
            self.lookup_field = model._meta.get_field(lookup_field)
        # self.lookup_field = lookup_field

    def lookup(self, value, **kw):
        model = self.field.remote_field.model
        if isinstance(value, model):
            return value
        return model.lookup_or_create(self.lookup_field, value, **kw)

        # if isinstance(self.lookup_field,babel.BabelCharField):
            # flt  = babel.lookup_filter(self.lookup_field.name,value,**kw)
        # else:
            # kw[self.lookup_field.name] = value
            # flt = models.Q(**kw)
        # try:
            # return model.objects.get(flt)
        # except MultipleObjectsReturned,e:
            # raise model.MultipleObjectsReturned("%s.objects lookup(%r) : %s" % (model.__name__,value,e))
        # except model.DoesNotExist,e:
            # raise model.DoesNotExist("%s.objects lookup(%r) : %s" % (model.__name__,value,e))


class DateConverter(Converter):

    def convert(self, **kw):
        value = kw.get(self.field.name)
        if not isinstance(value, datetime.date):
            if value:  # keep out empty strings
                if type(value) == int:
                    value = str(value)
                d = dateparser.parse(value)
                d = datetime.date(d.year, d.month, d.day)
                kw[self.field.name] = d
        return kw


class ChoiceConverter(Converter):

    """Converter for :class:`ChoiceListField
    <lino.core.choicelists.ChoiceListField>`.

    """

    def convert(self, **kw):
        value = kw.get(self.field.name)

        if value is not None:
            if not isinstance(value, self.field.choicelist.item_class):
                kw[self.field.name] = self.field.choicelist.get_by_value(value)
        return kw


class DecimalConverter(Converter):

    def convert(self, **kw):
        value = kw.get(self.field.name)
        if value is not None:
            if not isinstance(value, decimal.Decimal):
                kw[self.field.name] = decimal.Decimal(value)
        return kw


class ForeignKeyConverter(LookupConverter):

    """Converter for ForeignKey fields."""

    def convert(self, **kw):
        value = kw.get(self.field.name)
        if value is not None:
            if value == '':
                value = None
            else:
                value = self.lookup(value)
            kw[self.field.name] = value
            # logger.info("20111213 %s %s -> %r", self.field.name,self.__class__,value)
        return kw


class GenericForeignKeyConverter(Converter):

    """Converter for GenericForeignKey fields."""

    def convert(self, **kw):
        value = kw.get(self.field.name)
        if value is not None:
            if value == '':
                value = None
            else:
                mo = GFK_HACK.match(value)
                if mo is not None:
                    actor = settings.SITE.models.resolve(mo.group(1))
                    pk = mo.group(2)
                    value = actor.get_row_by_pk(None, pk)
                    # ct = ContentType.objects.get_for_model(actor.model)
                    # value = self.lookup(value)
                else:
                    raise Exception("Could not parse %r" % value)
            kw[self.field.name] = value
        return kw


class ManyToManyConverter(LookupConverter):

    """Converter for ManyToMany fields."""
    splitsep = None

    # def lookup(self,value):
        # model = self.field.remote_field.model
        # try:
            # return model.objects.get(
              # **{self.lookup_field: value})
        # except model.DoesNotExist,e:
            # raise DataError("%s.objects.get(%r) : %s" % (
              # model.__name__,value,e))

    def convert(self, **kw):
        values = kw.get(self.field.name)
        if values is not None:
            del kw[self.field.name]
            l = [self.lookup(value)
                 for value in values.split(self.splitsep)]
            kw['_m2m'][self.field.name] = l
        return kw


def make_converter(f, lookup_fields={}):
    from lino.core.gfks import GenericForeignKey
    
    if isinstance(f, models.ForeignKey):
        return ForeignKeyConverter(f, lookup_fields.get(f.name, "pk"))
    if isinstance(f, GenericForeignKey):
        return GenericForeignKeyConverter(f)
    # if isinstance(f,fields.LinkedForeignKey):
        # return LinkedForeignKeyConverter(f,lookup_fields.get(f.name,"pk"))
    if isinstance(f, models.ManyToManyField):
        return ManyToManyConverter(f, lookup_fields.get(f.name, "pk"))
    if isinstance(f, models.DateField):
        return DateConverter(f)
    if isinstance(f, models.DecimalField):
        return DecimalConverter(f)
    from lino.core import choicelists
    if isinstance(f, choicelists.ChoiceListField):
        # if f.name == 'p_book':
            # print "20131012 b", f
        return ChoiceConverter(f)


class Instantiator(object):
    """A utility class to make python fixtures more compact. See
    :ref:`tutorial.instantiator`.

    An instantiator is a

    """

    def __init__(self, model, fieldnames=None, converter_classes={}, **kw):
        # self.model = resolve_model(model,strict=True)
        self.model = resolve_model(model)
        if isinstance(self.model, UnresolvedModel):
            raise Exception("Instantiator on unresolved model %s", model)
        if not self.is_active():
            def noop(*values, **kw):
                pass
            self.build = noop
            return
        # if self.model._meta.pk is None:
            # raise Exception("Model %r is not installed (_meta.pk is None)." % self.model)
        # if type(fieldnames) == str:
        if isinstance(fieldnames, six.string_types):
            fieldnames = fieldnames.split()
        self.default_values = kw
        #self.fieldnames = fieldnames
        lookup_fields = {}
        self.converters = []
        if fieldnames is None:
            self.fields = self.model._meta.fields
        else:
            self.fields = []
            for name in fieldnames:
                a = name.split(":")
                if len(a) == 2:
                    name = a[0]
                    lookup_fields[name] = a[1]

                rf = make_remote_field(model, name)
                if rf:
                    self.fields.append(rf)
                else:
                    field = self.model._meta.get_field(name)
                    self.fields.append(field)
        # print " ".join(dir(model_class))
        # print " ".join(model_class._meta.fields)
        # for f in model_class._meta.fields:
        # for f in self.fields:
        for f in self.model._meta.fields + self.model._meta.many_to_many:
            cv = None
            cvc = converter_classes.get(f.name, None)
            if cvc is not None:
                cv = cvc(f)
            else:
                cv = make_converter(f, lookup_fields)
            if cv is not None:
                self.converters.append(cv)
        # for f in model_class._meta.many_to_many:
            # print "foo", f.name

    def is_active(self):

        if isinstance(self.model, UnresolvedModel):
            return False
        if self.model._meta.pk is None:
            return False
        return True

    def __call__(self, *values, **kw):
        """Calling an instantiator is the same as callig its :meth:`build`
        method.

        """
        return self.build(*values, **kw)

    def build(self, *values, **kw):
        """Instantiate an object using the default values of this
        instantiator, overridden by the given specified values. The
        number of positional arguments may not exceed the number of
        fieldnames specified when creating this :class:`Instantiator`.

        """
        # logger.debug("Instantiator.build(%s,%r,%r)",self.model_class._meta.db_table,values,kw)
        # i = 0
        kw['_m2m'] = {}
        setters = []
        for i, v in enumerate(values):
            fld = self.fields[i]
            if isinstance(v, six.string_types):
                v = v.strip()
                if len(v) == 0:
                    continue
            if isinstance(fld, RemoteField):
                setters.append((fld, v))
            else:
                kw[fld.name] = v

        for name, v in list(kw.items()):
            if "__" in name:
                del kw[name]
                fld = make_remote_field(self.model, name)
                setters.append((fld, v))
            
        # kw.update(self.default_values)
        for k, v in self.default_values.items():
            kw.setdefault(k, v)
        for c in self.converters:
            kw = c.convert(**kw)
        # if self.model.__name__ == 'Company':
            # print 20130212, __file__, kw
            # logger.info("20130212 field_cache for %s (%s)",self.model,
              # ' '.join([f.name for f in self.model._meta._field_name_cache]))

        m2m = kw.pop("_m2m")
        instance = self.model(**kw)
        instance.full_clean()
        if m2m or len(setters):
            instance.save()
            
        for fld, v in setters:
            fld.setter(instance, v)
        
        if m2m:
            for k, v in list(m2m.items()):
                queryset = getattr(instance, k)
                queryset.add(*v)
        return instance


class InstanceGenerator(object):
    """
    Usage example see :mod:`lino_xl.lib.humanlinks.fixtures`.
    """
    def __init__(self):
        self._objects = []
        self._instantiators = dict()

    def add_instantiator(self, name, *args, **kw):
        i = Instantiator(*args, **kw)
        # self._instantiators[i.model] = i

        def f(*args, **kw):
            o = i.build(*args, **kw)
            return self.on_new(o)
        setattr(self, name, f)

    def on_new(self, o):
        self._objects.append(o)
        return o

    def flush(self):
        rv = self._objects
        self._objects = []
        return rv


def create_row(model, **kw):
    """Instantiate, full_clean, save and return a database object.

    """
    # model = resolve_model(model)
    o = model(**kw)
    o.full_clean()
    o.save()
    return o

def create_or_update_row(model, lookup_values, new_values):
    """
    Update a single existing row that can be found using param: lookup values, with new_values.
    If one doesn't exist, instantiates, full_cleans, saves and returns a database object
    """
    try:
        o = model.objects.get(**lookup_values)
        for attr, value in new_values.items():
            setattr(o, attr, value)
    except model.DoesNotExist: # If get receives more than one item will raise MultipleObjectsReturned:
        o = model(**new_values)
    o.full_clean()
    o.save()
    return o


create = create_row  # backwards-compat

def create_and_get(model, **kw):
    """Create and then read back from database (the latter to avoid
    certain Django side effects)

    """
    o = create(model, **kw)
    return model.objects.get(pk=o.pk)

def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()
