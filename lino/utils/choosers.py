# Copyright 2009-2020 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""Extends the possibilities for defining choices for fields of a
Django model.

- Context-sensitive choices (see :ref:`lino.dev.combo`)
- Non-limiting choices (`force_selection` False) :
  specify a pick list of suggestions but leave the possibility
  to store manually entered values
- :ref:`learning_combos`

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

import decimal
import datetime
from dateutil import parser as dateparser

import re
GFK_HACK = re.compile(r'^<a href="javascript:Lino\.(\w+\.\w+)\.detail\.run\(.*,\{ &quot;record_id&quot;: (\w+) \}\)">.*</a>$')

from django.db import models
from django.conf import settings

# from lino.api import rt
from lino.core import constants
from lino.core import fields
from lino.core.utils import getrqdata




# class DataError(Exception):
#     pass


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

    If you specify a string, then it can be a *value* or a *name*.

    """

    def convert(self, **kw):
        value = kw.get(self.field.name)

        if value is not None:
            if not isinstance(value, self.field.choicelist.item_class):
                # kw[self.field.name] = self.field.choicelist.get_by_value(value)
                kw[self.field.name] = self.field.choicelist.to_python(value)
                # if self.field.name == "vat_class":
                #     print("20191210 convert {} from {} --> {}".format(
                #         value, self.field.choicelist.items_dict, kw[self.field.name]))
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




class BaseChooser(object):
    pass


class FieldChooser(BaseChooser):

    def __init__(self, field):
        self.field = field


class ChoicesChooser(FieldChooser):

    def __init__(self, field):
        FieldChooser.__init__(self, field)
        self.simple_values = type(field.choices[0])


class Chooser(FieldChooser):
    """Holds information about the possible choices of a field.

    """
    #~ stored_name = None
    simple_values = False
    instance_values = True
    force_selection = True
    choice_display_method = None  # not yet used.
    can_create_choice = False

    def __init__(self, model, field, meth):
        FieldChooser.__init__(self, field)
        self.model = model
        #~ self.field = model._meta.get_field(fldname)
        self.meth = meth
        from lino.core.gfks import is_foreignkey
        from lino.core.choicelists import ChoiceListField
        if isinstance(field, ChoiceListField):
            self.simple_values = getattr(meth, 'simple_values', False)
            self.instance_values = getattr(meth, 'instance_values', True)
            self.force_selection = getattr(
                meth, 'force_selection', self.force_selection)
        elif is_foreignkey(field):
            pass
        elif isinstance(field, fields.VirtualField) and isinstance(field.return_type, models.ForeignKey):
            pass
        else:
            self.simple_values = getattr(meth, 'simple_values', False)
            self.instance_values = getattr(meth, 'instance_values', False)
            self.force_selection = getattr(
                meth, 'force_selection', self.force_selection)
        #~ self.context_params = meth.func_code.co_varnames[1:meth.func_code.co_argcount]
        self.context_params = meth.context_params
        #~ self.multiple = meth.multiple
        #~ self.context_params = meth.func_code.co_varnames[:meth.func_code.co_argcount]
        #~ print '20100724', meth, self.context_params
        #~ logger.warning("20100527 %s %s",self.context_params,meth)
        self.context_values = []
        self.context_fields = []
        for name in self.context_params:
            if name == "ar":
                continue
            f = self.get_data_elem(name)

            if f is None:
                raise Exception(
                    "No data element '%s' in %s "
                    "(method %s_choices)" % (
                        name, self.model, field.name))
            #~ if name == 'p_book':
                #~ print 20131012, f
            self.context_fields.append(f)
            self.context_values.append(name + "Hidden")
            #~ if isinstance(f,models.ForeignKey):
                #~ self.context_values.append(name+"Hidden")
            #~ else:
                #~ self.context_values.append(name)
        self.converters = []
        #~ try:
        for f in self.context_fields:
            cv = make_converter(f)
            if cv is not None:
                self.converters.append(cv)
        #~ except models.FieldDoesNotExist,e:
            #~ print e

        if hasattr(model, "create_%s_choice" % field.name):
            self.can_create_choice = True

        m = getattr(model, "%s_choice_display" % field.name, None)
        if m is not None:
            self.choice_display_method = m

    def __str__(self):
        return "Chooser(%s.%s,%s)" % (
            self.model.__name__, self.field.name,
            self.context_params)

    def create_choice(self, obj, text):
        m = getattr(obj, "create_%s_choice" % self.field.name)
        return m(text)

    def get_data_elem(self, name):
        """Calls :meth:`dd.Actor.get_data_elem` or
        :meth:`dd.Model.get_data_elem` or
        :meth:`dd.Action.get_data_elem`.

        """
        de = self.model.get_data_elem(name)
        if de is None:
            return self.model.get_param_elem(name)
        return de

    def __call__(self, *args, **kw):
        for i, v in enumerate(args):
            kw[self.context_fields[i]] = v
        return self.get_choices(**kw)

    def get_choices(self, **context):
        """Return a list of choices for this chooser, using keyword parameters
        as context.

        """
        args = []
        for varname in self.context_params:
            args.append(context.get(varname, None))
        return self.meth(*args)

    def get_request_choices(self, ar, tbl):
        """
        Return a list of choices for this chooser,
        using a HttpRequest to build the context.
        """
        kw = {
            "ar": ar,
        }
        # kw = {}

        # ba = tbl.get_url_action(tbl.default_elem_action_name)
        # 20120202
        if tbl.master_field is not None:
            from django.contrib.contenttypes.models import ContentType
            rqdata = getrqdata(ar.request)
            if tbl.master is not None:
                master = tbl.master
            else:
                mt = rqdata.get(constants.URL_PARAM_MASTER_TYPE)
                # ContentType = rt.models.contenttypes.ContentType
                try:
                    master = ContentType.objects.get(pk=mt).model_class()
                except ContentType.DoesNotExist:
                    master = None

            pk = rqdata.get(constants.URL_PARAM_MASTER_PK, None)
            if pk and master:
                try:
                    kw[tbl.master_field.name] = master.objects.get(pk=pk)
                except ValueError:
                    raise Exception(
                        "Invalid primary key %r for %s", pk, master.__name__)
                except master.DoesNotExist:
                    raise Exception("There's no %s with primary key %r" %
                                    (master.__name__, pk))

        for k, v in list(ar.request.GET.items()):
            kw[str(k)] = v

        # logger.info(
        #     "20130513 get_request_choices(%r) -> %r",
        #     tbl, kw)

        for cv in self.converters:
            kw = cv.convert(**kw)

        if tbl.known_values:
            kw.update(tbl.known_values)

        if False:  # removed 20120815 #1114
            #~ ar = tbl.request(ui,request,tbl.default_action)
            if ar.create_kw:
                kw.update(ar.create_kw)
            if ar.known_values:
                kw.update(ar.known_values)
            if tbl.master_key:
                kw[tbl.master_key] = ar.master_instance
            #~ if tbl.known_values:
                #~ kw.update(tbl.known_values)
        return self.get_choices(**kw)  # 20120918b

    def get_text_for_value(self, value, obj):
        m = getattr(self.field, 'get_text_for_value', None)
        if m is not None:  # e.g. lino.utils.choicelist.ChoiceListField
            return m(value)
        #~ raise NotImplementedError
        #~ assert not self.simple_values
        m = getattr(obj, "get_" + self.field.name + "_display", str)
        #~ if m is None:
            #~ raise Exception("")
        return m(value)
        #~ raise NotImplementedError("%s : Cannot get text for value %r" % (self.meth,value))


def uses_simple_values(holder, fld):
    "used by :class:`lino.core.store`"
    from lino.core.gfks import is_foreignkey
    if is_foreignkey(fld):
        return False
    # if isinstance(fld, models.OneToOneRel):
    #     return False
    if holder is not None and fld.name is not None:
        ch = holder.get_chooser_for_field(fld.name)
        if ch is not None:
            return ch.simple_values
    if fld.choices is None:
        return True
    choices = list(fld.choices)
    if len(choices) == 0:
        return True
    if type(choices[0]) in (list, tuple):
        return False
    return True


def _chooser(make, **options):
    #~ options.setdefault('quick_insert_field',None)
    def chooser_decorator(fn):
        def wrapped(*args):
            return fn(*args)
        cp = options.pop(
            'context_params',
            fn.__code__.co_varnames[1:fn.__code__.co_argcount])
        wrapped.context_params = cp
        for k, v in options.items():
            setattr(wrapped, k, v)
        return make(wrapped)
        # return classmethod(wrapped)
        # A chooser on an action must not turn it into a classmethod
    return chooser_decorator


def chooser(**options):
    "Decorator which turns the method into a chooser."
    return _chooser(classmethod, **options)


def noop(x):
    return x


def action_chooser(**options):
    return _chooser(noop, **options)

def get_choosers_dict(holder):
    d = holder.__dict__.get('_choosers_dict', None)
    if d is None:
        d = dict()
        setattr(holder, '_choosers_dict', d)
    return d

def check_for_chooser(holder, field):
    # holder is either a Model, an Actor or an Action.
    if isinstance(field, fields.DummyField):
        return
    d = get_choosers_dict(holder)
    ch = d.get(field.name, None)
    if ch is not None:
        # if ch.model is not holder:
        #     raise Exception("20200425 {} is not {}".format(holder, ch.model))
        return ch

    methname = field.name + "_choices"
    m = getattr(holder, methname, None)
    if m is not None:
        # if field.name.endswith('municipality'):
        #     print("20200524 check_for_chooser() found {} on {}", field.name, holder)
        # 20200425 fix theoretical bug
        # if field.name
        # if ch in d:
            # raise Exception(
            #     "Duplicate of chooser for {} in {}".format(field, holder))
        ch = Chooser(holder, field, m)
        d[field.name] = ch
        return ch
    # if field.name == 'city':
    #     logger.info("20140822 chooser for %s.%s", holder, field.name)
