# -*- coding: UTF-8 -*-
# Copyright 2008-2020 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""
Defines extended database field classes and utility functions
related to fields.
"""

import logging ; logger = logging.getLogger(__name__)
import datetime
from decimal import Decimal

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.db.models.fields import NOT_PROVIDED
from django.utils.functional import cached_property

from lino.core.utils import resolve_field, full_model_name, resolve_model
from lino.core.exceptions import ChangedAPI
from lino.core.diff import ChangeWatcher

from lino.utils import get_class_attr
from lino.utils import IncompleteDate
from lino.utils import quantities
from lino.utils import choosers
from lino.utils.quantities import Duration


def validate_incomplete_date(value):
    """Raise ValidationError if user enters e.g. a date 30.02.2009.
    """
    try:
        value.as_date()
    except ValueError:
        raise ValidationError(_("Invalid date"))


def set_default_verbose_name(f):
    """

    If the verbose_name of a ForeignKey was not set by user code, Lino sets it
    to the verbose_name of the model pointed to.  This rule holds also for
    virtual FK fields.

    For every FK field defined on a model (including virtual FK fields) this is
    called during kernel startup.  Django sets the `verbose_name` of every
    field to ``field.name.replace('_', ' ')``.

    For virtual FK fields defined on an actor or an action it is called a bit
    later. These fields don't have a name.

    """
    if f.name is None:
        if f.verbose_name is None:
            f.verbose_name = f.remote_field.model._meta.verbose_name
    elif f.verbose_name == f.name.replace('_', ' '):
        f.verbose_name = f.remote_field.model._meta.verbose_name



class PasswordField(models.CharField):

    """Stored as plain text in database, but not displayed in user
    interface.

    """
    pass


class RichTextField(models.TextField):
    # See :doc:`/dev/textfield`.

    def __init__(self, *args, **kw):
        self.textfield_format = kw.pop(
            'format', kw.pop('textfield_format', None))
        self.bleached = kw.pop('bleached', None)
        super(RichTextField, self).__init__(*args, **kw)

    def set_format(self, fmt):
        self.textfield_format = fmt


class PercentageField(models.DecimalField):

    """
    A field to express a percentage.
    The database stores this like a DecimalField.
    Plain HTML adds a "%".
    """

    def __init__(self, *args, **kwargs):
        defaults = dict(
            max_length=5,
            max_digits=5,
            decimal_places=2,
        )
        defaults.update(kwargs)
        super(PercentageField, self).__init__(*args, **defaults)


class TimeField(models.TimeField):
    """
    Like a TimeField, but allowed values are between
    :attr:`calendar_start_hour
    <lino.core.site.Site.calendar_start_hour>` and
    :attr:`calendar_end_hour <lino.core.site.Site.calendar_end_hour>`.
    """
    pass

class DatePickerField(models.DateField):

    """
    A DateField that uses a DatePicker instead of a normal DateWidget.
    Doesn't yet work.
    """
    pass


class MonthField(models.DateField):

    """
    A DateField that uses a MonthPicker instead of a normal DateWidget
    """

    def __init__(self, *args, **kw):
        models.DateField.__init__(self, *args, **kw)


# def PriceField(*args, **kwargs):
#     defaults = dict(
#         max_length=10,
#         max_digits=10,
#         decimal_places=2,
#     )
#     defaults.update(kwargs)
#     return models.DecimalField(*args, **defaults)


class PriceField(models.DecimalField):
    """
    A thin wrapper around Django's `DecimalField
    <https://docs.djangoproject.com/en/1.11/ref/models/fields/#decimalfield>`_
    which adds default values for `decimal_places`, `max_length` and
    `max_digits`.
    """

    def __init__(self, verbose_name=None, max_digits=10, **kwargs):
        defaults = dict(
            max_length=max_digits,
            max_digits=max_digits,
            decimal_places=2,
        )
        defaults.update(kwargs)
        super(PriceField, self).__init__(verbose_name, **defaults)


#~ class MyDateField(models.DateField):

    #~ def formfield(self, **kwargs):
        #~ fld = super(MyDateField, self).formfield(**kwargs)
        # ~ # display size is smaller than full size:
        #~ fld.widget.attrs['size'] = "8"
        #~ return fld


"""
http://stackoverflow.com/questions/454436/unique-fields-that-allow-nulls-in-django
answer Dec 20 '09 at 3:40 by mightyhal
http://stackoverflow.com/a/1934764
"""


# class NullCharField(models.CharField):  # subclass the CharField
#     description = "CharField that stores empty strings as NULL instead of ''."

#     def __init__(self, *args, **kwargs):
#         defaults = dict(blank=True, null=True)
#         defaults.update(kwargs)
#         super(NullCharField, self).__init__(*args, **defaults)

#     # this is the value right out of the db, or an instance
#     def to_python(self, value):
#         # ~ if isinstance(value, models.CharField): #if an instance, just return the instance
#         if isinstance(value, six.string_types):  # if a string, just return the value
#             return value
#         if value is None:  # if the db has a NULL (==None in Python)
#             return ''  # convert it into the Django-friendly '' string
#         else:
#             return value  # otherwise, return just the value

#     def get_db_prep_value(self, value, connection, prepared=False):
#         # catches value right before sending to db
#         # if Django tries to save '' string, send the db None (NULL)
#         if value == '':
#             return None
#         else:
#             return value  # otherwise, just pass the value


class FakeField(object):
    """
    Base class for :class:`RemoteField` and :class:`DisplayField`.
    """
    model = None
    db_column = None
    choices = []
    primary_key = False
    editable = False
    name = None
    null = True
    serialize = False
    verbose_name = None
    help_text = None
    preferred_width = 30
    preferred_height = 3
    max_digits = None
    decimal_places = None
    default = NOT_PROVIDED
    generate_reverse_relation = False  # needed when AFTER17
    remote_field = None
    blank = True  # 20200425

    wildcard_data_elem = False
    """Whether to consider this field as wildcard data element.
    """
    sortable_by = None
    """
    A list of names of real fields to be used for sorting when this
    fake field is selected.  For remote fields this is set
    automatically, on virtual fields you can set it yourself.
    """

    # required by Django 1.8+:
    is_relation = False
    concrete = False
    auto_created = False
    column = None
    empty_values = set([None, ''])

    # required by Django 1.10+:
    one_to_many = False
    one_to_one = False

    # required since 20171003
    rel = None

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            if not hasattr(self, k):
                raise Exception("{} has no attribute {}".format(self, k))
            setattr(self, k, v)

    def is_enabled(self, lh):
        """
        Overridden by mti.EnableChild
        """
        return self.editable

    def clean(self, raw_value, obj):
        # needed for Django 1.8
        return raw_value

    def has_default(self):
        return self.default is not NOT_PROVIDED

    def get_default(self):
        return self.default

    def set_attributes_from_name(self, name):
        if not self.name:
            self.name = name
        self.attname = name
        self.column = None
        self.concrete = False
        # if self.verbose_name is None and self.name:
        #     self.verbose_name = self.name.replace('_', ' ')

class RemoteField(FakeField):
    """
    A field on a related object.

    Remote fields are created by
    :meth:`lino.core.model.Model.get_data_elem` when needed.

    .. attribute:: field

        The bottom-level (leaf) field object.

    """
    #~ primary_key = False
    #~ editable = False

    def __init__(self, getter, name, fld, setter=None, **kwargs):
        self.func = getter
        self.name = name
        self.attname = name
        # self.db_column = name  # 20200423
        self.field = fld
        # for k in ('verbose_name', 'help_text', 'blank', 'default', 'null'):
        #     kwargs.setdefault(k, getattr(fld, k))
        self.verbose_name = fld.verbose_name
        self.help_text = fld.help_text
        # self.blank = fld.blank
        self.blank = True
        self.default = None
        # self.null = fld.null
        # self.null = getattr(fld, 'null', None)
        self.max_length = getattr(fld, 'max_length', None)
        self.max_digits = getattr(fld, 'max_digits', None)
        self.decimal_places = getattr(fld, 'decimal_places', None)
        self.sortable_by = [ name ]

        self.setter = setter
        if setter is not None:
            self.editable = True
            self.choices = getattr(fld, 'choices', None)
        super(RemoteField, self).__init__(**kwargs)
        #~ print 20120424, self.name
        #~ settings.SITE.register_virtual_field(self)

        # The remote_field of a FK field has nothing to do with our RemoteField,
        # it is set by Django on each FK field and points to

        if isinstance(fld, VirtualField) and isinstance(fld.return_type, models.ForeignKey):
            fld.lino_resolve_type()  # 20200425
            fk = fld.return_type
        elif isinstance(fld, models.ForeignKey):
            fk = fld
        else:
            fk = None
        if fk is not None:
            # if not fk.remote_field:
            #     raise Exception("20200425 {} has no remote_field".format(fk))
            self.remote_field = fk.remote_field
            from lino.core import store
            store.get_atomizer(self.remote_field, self, name)

    def value_from_object(self, obj, ar=None):
        """
        Return the value of this field in the specified model instance
        `obj`.  `ar` may be `None`, it's forwarded to the getter
        method who may decide to return values depending on it.
        """
        m = self.func
        return m(obj, ar)

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return self.value_from_object(instance)


class DisplayField(FakeField):
    """
    A field to be rendered like a normal read-only form field, but with
    plain HTML instead of an ``<input>`` tag.

    This is to be used as
    the `return_type` of a :class:`VirtualField`.

    The value to be represented is either some unicode text, a
    translatable text or a :mod:`HTML element <etgen.html>`.
    """
    choices = None
    blank = True  # 20200425
    drop_zone = None
    max_length = None

    def __init__(self, verbose_name=None, **kwargs):
        self.verbose_name = verbose_name
        super(DisplayField, self).__init__(**kwargs)

    # the following dummy methods are never called but needed when
    # using a DisplayField as return_type of a VirtualField

    def to_python(self, *args, **kw):
        return None
        # raise NotImplementedError(
        #     "{}.to_python({},{})".format(self.name, args, kw))

    def save_form_data(self, *args, **kw):
        raise NotImplementedError

    def value_to_string(self, *args, **kw):
        raise NotImplementedError

    def value_from_object(self, obj, ar=None):
        return self.default


class HtmlBox(DisplayField):
    """
    Like :class:`DisplayField`, but to be rendered as a panel rather
    than as a form field.
    """
    pass


# class VirtualGetter(object):
#     """A wrapper object for getting the content of a virtual field
#     programmatically.

#     """

#     def __init__(self, vf, instance):
#         self.vf = vf
#         self.instance = instance

#     def __call__(self, ar=None):
#         return self.vf.value_from_object(self.instance, ar)

#     # def __get__(self, instance, owner):
#     #     return self.vf.value_from_object(instance, None)

#     def __getattr__(self, name):
#         obj = self.vf.value_from_object(self.instance, None)
#         return getattr(obj, name)

#     def __repr__(self):
#         return "<{0}>.{1}".format(repr(self.instance), self.vf.name)

class VirtualModel:
    def __init__(self, model):
        self.wrapped_model = model
        self._meta = model._meta

VFIELD_ATTRIBS = frozenset('''to_python choices save_form_data
  value_to_string max_length remote_field
  max_digits verbose_name decimal_places
  help_text blank'''.split())

class VirtualField(FakeField):
    """
    Represents a virtual field. Values of virtual fields are not stored
    in the database, but computed on the fly each time they get
    read. Django doesn't see them.

    A virtual field must have a `return_type`, which can be either a
    Django field type (CharField, TextField, IntegerField,
    BooleanField, ...) or one of Lino's custom fields
    :class:`DisplayField`, :class:`HtmlBox` or :class:`RequestField`.

    The `get` must be a callable which takes two arguments: `obj` the
    database object and `ar` an action request.

    The :attr:`model` of a VirtualField is the class where the field
    was *defined*. This can be an abstract model. The VirtualField
    instance does not have a list of the concrete models which use it
    (because they inherit from that class).
    """

    def __init__(self, return_type, get, **kwargs):
        """
        Normal VirtualFields are read-only and not editable.
        We don't want to require application developers to explicitly
        specify `editable=False` in their return_type::

          @dd.virtualfield(dd.PriceField(_("Total")))
          def total(self, ar=None):
              return self.total_excl + self.total_vat
        """
        self.return_type = return_type  # a Django Field instance
        self.get = get

        # if isinstance(return_type, FakeField):
        #     sortable_by = return_type.sortable_by
        #     self.sortable_by = sortable_by
        #     if sortable_by and isinstance(sortable_by, list):
        #             sortable_by = sortable_by[0]
        #     self.column = sortable_by
        # for k in VFIELD_ATTRIBS:
        #     setattr(self, k, getattr(return_type, k, None))

        settings.SITE.register_virtual_field(self)
        super(VirtualField, self).__init__(**kwargs)

    def lino_resolve_type(self):
        """
        Called on every virtual field when all models are loaded.
        """

        f = self.return_type

        if isinstance(f, str):
            try:
                f = self.return_type = resolve_field(f)
            except Exception as e:
                raise Exception(
                    "Invalid return type spec {} for {} : {}".format(f, self, e))

        if isinstance(f, FakeField):
            sortable_by = f.sortable_by
            self.sortable_by = sortable_by
            if sortable_by and isinstance(sortable_by, list):
                sortable_by = sortable_by[0]
            self.column = sortable_by

        if isinstance(f, models.ForeignKey):
            f.remote_field.model = resolve_model(f.remote_field.model)
            set_default_verbose_name(f)
            self.get_lookup = f.remote_field.get_lookup  # 20200425
            self.get_path_info = f.remote_field.get_path_info  # 20200425
            self.remote_field = f.remote_field

        for k in VFIELD_ATTRIBS:
            setattr(self, k, getattr(f, k, None))

        # if self.name == 'detail_pointer':
        #     logger.info('20170905 resolve_type 1 %s on %s',
        #                 self.name, self.verbose_name)

        #~ removed 20120919 self.return_type.editable = self.editable
        # if self.name == 'detail_pointer':
        #     logger.info('20170905 resolve_type done %s %s',
        #                 self.name, self.verbose_name)

        from lino.core import store
        store.get_atomizer(self.model, self, self.name)

        # print("20181023 Done: lino_resolve_type() for {}".format(self))


    def override_getter(self, get):
        self.get = get

    def attach_to_model(self, model, name):
        self.model = model
        self.name = name
        self.attname = name
        if hasattr(self.return_type, 'model'):
            # logger.info("20200425 return_type for virtual field %s has a model", self)
            return
        self.return_type.model = VirtualModel(model)
        self.return_type.column = None

        # if name == "overview":
        #     print("20181022", self, self.verbose_name)

        #~ self.return_type.name = name
        #~ self.return_type.attname = name
        #~ if issubclass(model,models.Model):
        #~ self.lino_resolve_type(model,name)

        # must now be done by caller code:
        # if AFTER17:
        #     model._meta.add_field(self, virtual=True)
        # else:
        #     model._meta.add_virtual_field(self)

        # if self.get is None:
        #     return
        # if self.get.func_code.co_argcount != 2:
        #     if self.get.func_code.co_argcount == 2:
        #         getter = self.get
        #         def w(fld, obj, ar=None):
        #             return getter(obj, ar)
        #         self.get = w
        #         logger.warning("DeprecationWarning")
        #     else:
        #         msg = "Invalid getter for VirtualField {}".format(self)
        #         raise ChangedAPI(msg)

        #~ logger.info('20120831 VirtualField %s.%s',full_model_name(model),name)

    def __repr__(self):
        if self.model is None:
            return "{} {} ({})".format(
                self.__class__.__name__, self.name, self.verbose_name)
            # return super(VirtualField, self).__repr__()
        return "%s.%s.%s" % (self.model.__module__,
                             self.model.__name__, self.name)

    def get_default(self):
        return self.return_type.get_default()
        #~

    def has_default(self):
        return self.return_type.has_default()

    def unused_contribute_to_class(self, cls, name):
        # if defined in abstract base class, called once on each submodel
        if self.name:
            if self.name != name:
                raise Exception("Attempt to re-use %s as %s in %s" % (
                    self.__class__.__name__, name, cls))
        else:
            self.name = name
            if self.verbose_name is None and self.name:
                self.verbose_name = self.name.replace('_', ' ')
        self.model = cls
        cls._meta.add_virtual_field(self)
        #~ cls._meta.add_field(self)

    def to_python(self, *args, **kwargs):
        return self.return_type.to_python(*args, **kwargs)

    #~ def save_form_data(self,*args,**kw): return self.return_type.save_form_data(*args,**kw)
    #~ def value_to_string(self,*args,**kw): return self.return_type.value_to_string(*args,**kw)
    #~ def get_choices(self): return self.return_type.choices
    #~ choices = property(get_choices)

    def set_value_in_object(self, request, obj, value):
        """
        Stores the specified `value` in the specified model instance
        `obj`.  `request` may be `None`.

        Note that any implementation must also return `obj`, and
        callers must be ready to get another instance.  This special
        behaviour is needed to implement
        :class:`lino.utils.mti.EnableChild`.
        """
        pass
        # if value is not None:
        #     raise NotImplementedError("Cannot write %s to field %s" %
        #                               (value, self))

    #~ def value_from_object(self,request,obj):
    def value_from_object(self, obj, ar=None):
        """
        Return the value of this field in the specified model instance
        `obj`.  `ar` may be `None`, it's forwarded to the getter
        method who may decide to return values depending on it.
        """
        m = self.get
        #~ print self.field.name
        # return m(self, obj, ar)
        return m(obj, ar)
        # try:
        #     return m(obj, ar)
        # except TypeError as e:
        #     return "{} : {}".format(self, e)

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return self.value_from_object(instance, None)
        # return VirtualGetter(self, instance)

    def __set__(self, instance, value):
        return self.set_value_in_object(None, instance, value)

    def get_col(self, alias, output_field=None):
        if output_field is None:
            output_field = self
        if alias != self.model._meta.db_table or output_field != self:
            from django.db.models.expressions import Col
            return Col(alias, self, output_field)
        else:
            return self.cached_col

    @cached_property
    def cached_col(self):
        from django.db.models.expressions import Col
        return Col(self.model._meta.db_table, self)

    def select_format(self, compiler, sql, params):
        """
        Custom format for select clauses. For example, GIS columns need to be
        selected as AsText(table.col) on MySQL as the table.col data can't be
        used by Django.
        """
        return sql, params


def virtualfield(return_type, **kwargs):
    """
    Decorator to turn a method into a :class:`VirtualField`.
    """
    def decorator(fn):
        if isinstance(return_type, DummyField):
            return DummyField(fn)
        return VirtualField(return_type, fn, **kwargs)
    return decorator


class Constant(object):
    """
    Deserves more documentation.
    """

    def __init__(self, text_fn):
        self.text_fn = text_fn

def constant():
    """
    Decorator to turn a function into a :class:`Constant`.  The
    function must accept one positional argument `datasource`.
    """
    def decorator(fn):
        return Constant(fn)
    return decorator


class RequestField(VirtualField):
    """
    A :class:`VirtualField` whose values are table action requests to
    be rendered as a clickable integer containing the number of rows.
    Clicking on it will open a window with the table.
    """
    def __init__(self, get, *args, **kw):
        kw.setdefault('max_length', 8)
        VirtualField.__init__(self, DisplayField(*args, **kw), get)


def displayfield(*args, **kw):
    """
    Decorator to turn a method into a :class:`VirtualField` of type
    :class:`DisplayField`.
    """
    return virtualfield(DisplayField(*args, **kw))


def htmlbox(*args, **kwargs):
    """
    Decorator shortcut to turn a method into a a :class:`VirtualField`
    of type :class:`HtmlBox`.
    """
    return virtualfield(HtmlBox(*args, **kwargs))


def requestfield(*args, **kw):
    """
    Decorator shortcut to turn a method into a a :class:`VirtualField`
    of type :class:`RequestField`.
    """
    def decorator(fn):
        #~ def wrapped(*args):
            #~ return fn(*args)
        #~ return RequestField(wrapped,*args,**kw)
        return RequestField(fn, *args, **kw)
    return decorator


class CharField(models.CharField):
    """
    An extension around Django's `models.CharField`.

    Adds two keywords `mask_re` and `strip_chars_re` which, when using
    the ExtJS ui, will be rendered as the `maskRe` and `stripCharsRe`
    config options of `TextField` as described in the `ExtJS
    documentation
    <http://docs.sencha.com/extjs/3.4.0/#!/api/Ext.form.TextField>`__,
    converting naming conventions as follows:

    =============== ============ ==========================
    regex           regex        A JavaScript RegExp object to be tested against the field value during validation (defaults to null). If the test fails, the field will be marked invalid using regexText.
    mask_re         maskRe       An input mask regular expression that will be used to filter keystrokes that do not match (defaults to null). The maskRe will not operate on any paste events.
    strip_chars_re  stripCharsRe A JavaScript RegExp object used to strip unwanted content from the value before validation (defaults to null).
    =============== ============ ==========================


    Example usage:

      belgian_phone_no = dd.CharField(max_length=15,strip_chars_re='')
    """

    def __init__(self, *args, **kw):
        self.strip_chars_re = kw.pop('strip_chars_re', None)
        self.mask_re = kw.pop('mask_re', None)
        self.regex = kw.pop('regex', None)
        models.CharField.__init__(self, *args, **kw)


class QuantityField(CharField):
    """
    A field that accepts :class:`Quantity
    <lino.utils.quantities.Quantity>`, :class:`Percentage
    <lino.utils.quantities.Percentage>` and :class:`Duration
    <lino.utils.quantities.Duration>` values.

    Implemented as a CharField (sorting or filter ranges may not work
    as expected).

    When you set `blank=True`, then you should also declare `null=True`.

    """
    description = _("Quantity (Decimal or Duration)")

    def __init__(self, *args, **kw):
        kw.setdefault('max_length', 6)
        models.Field.__init__(self, *args, **kw)
        if self.blank and not self.null:
            raise ChangedAPI(
                "When `blank` is True, `null` must be True as well.")

        #~ models.CharField.__init__(self,*args,**kw)

    #~ def get_internal_type(self):
        #~ return "CharField"

    def to_python(self, value):
        """
        Excerpt from `Django docs
        <https://docs.djangoproject.com/en/1.11/howto/custom-model-fields/#converting-values-to-python-objects>`__:

            As a general rule, the method should deal gracefully with
            any of the following arguments:

            - An instance of the correct type (e.g., Hand in our ongoing example).
            - A string (e.g., from a deserializer).
            - Whatever the database returns for the column type you’re using.

        I'd add "Any value potentially specified for this field when instantiating
        a model."

        >>> to_python(None)
        >>> to_python(30)
        >>> to_python(30L)
        >>> to_python('')
        >>> to_python(Decimal(0))
        """
        if isinstance(value, Decimal):
            return value
        if value:
            # try:
            if isinstance(value, str):
                return quantities.parse(value)
            return Decimal(value)
            # except Exception as e:
            #     raise ValidationError(
            #         "Invalid value {} for {} : {}".format(value, self, e))
        return None

    def from_db_value(self, value, expression, connection, context=None):
        return quantities.parse(value) if value else self.get_default()

    # def get_db_prep_value(self, value, connection, prepared=False):
    #     return str(value) if value else ''

    def get_prep_value(self, value):
        # if value is None:
        #     return ''
        return str(value) if value else ''


class DurationField(QuantityField):
    """
    A field that stores :class:`Duration
    <lino.utils.quantities.Duration>` values as CHAR.

    Note that you cannot use SUM or AVG agregators on these fields
    since the database does not know how to calculate sums from them.


    """
    def from_db_value(self, value, expression, connection, context=None):
        return Duration(value) if value else self.get_default()

    def to_python(self, value):
        if isinstance(value, Duration):
            return value
        if value:
            # if isinstance(value, six.string_types):
            #     return Duration(value)
            return Duration(value)
        return None


class IncompleteDateField(models.CharField):
    """
    A field that behaves like a DateField, but accepts incomplete
    dates represented using
    :class:`lino.utils.format_date.IncompleteDate`.
    """

    default_validators = [validate_incomplete_date]

    def __init__(self, *args, **kw):
        kw.update(max_length=11)
        # msgkw = dict()
        # msgkw.update(ex1=IncompleteDate(1980, 0, 0)
        #              .strftime(settings.SITE.date_format_strftime))
        # msgkw.update(ex2=IncompleteDate(1980, 7, 0)
        #              .strftime(settings.SITE.date_format_strftime))
        # msgkw.update(ex3=IncompleteDate(0, 7, 23)
        #              .strftime(settings.SITE.date_format_strftime))
        kw.setdefault('help_text', _("""\
Uncomplete dates are allowed, e.g.
"00.00.1980" means "some day in 1980",
"00.07.1980" means "in July 1980"
or "23.07.0000" means "on a 23th of July"."""))
        models.CharField.__init__(self, *args, **kw)

    def deconstruct(self):
        name, path, args, kwargs = super(IncompleteDateField, self).deconstruct()
        del kwargs["max_length"]
        return name, path, args, kwargs

    # def get_internal_type(self):
    #     return "CharField"

    def from_db_value(self, value, expression, connection, context=None):
        return IncompleteDate.parse(value) if value else self.get_default()
        # if value:
        #     return IncompleteDate.parse(value)
        # return ''

    def to_python(self, value):
        if isinstance(value, IncompleteDate):
            return value
        if isinstance(value, datetime.date):
            #~ return IncompleteDate(value.strftime("%Y-%m-%d"))
            #~ return IncompleteDate(d2iso(value))
            return IncompleteDate.from_date(value)
        # if value:
        #     return IncompleteDate.parse(value)
        # return ''
        return IncompleteDate.parse(value) if value else ''

    # def get_prep_value(self, value):
    #     return str(value)

    def get_prep_value(self, value):
        return str(value) if value else ''
        # if value:
        #     return str(value)
        #     # return '"' + str(value) + '"'
        #     #~ return value.format("%04d%02d%02d")
        # return ''

    #~ def value_to_string(self, obj):
        #~ value = self._get_val_from_obj(obj)
        #~ return self.get_prep_value(value)


class Dummy(object):
    pass


class DummyField(FakeField):
    """
    Represents a field that doesn't exist in the current configuration
    but might exist in other configurations. The "value" of a
    DummyField is always `None`.

    See e.g. :func:`ForeignKey` and :func:`fields_list`.
    """
    # choices = []
    # primary_key = False

    def __init__(self, *args, **kw):
        pass

    # def __init__(self, name, *args, **kw):
    #     self.name = name

    def __str__(self):
        return self.name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return None

    def get_default(self):
        return None

    def contribute_to_class(self, cls, name):
        self.name = name
        v = getattr(cls, name, NOT_PROVIDED)
        if v is not NOT_PROVIDED:
            msg = ("{0} cannot contribute to {1} because it has already "
                   "an attribute '{2}'.")
            msg = msg.format(self, cls, name)
            if settings.SITE.ignore_model_errors:
                logger.warning(msg)
            else:
                raise Exception(msg)
        setattr(cls, name, self)

    def set_attributes_from_name(self, k):
        pass

class RecurrenceField(models.CharField):
    """
    Deserves more documentation.
    """

    def __init__(self, *args, **kw):
        kw.setdefault('max_length', 200)
        models.CharField.__init__(self, *args, **kw)


def OneToOneField(*args, **kwargs):
    """
    Instantiate a :class:`django.db.models.OneToOneField` using :func:`pointer_factory`.
    """
    return pointer_factory(models.OneToOneField, *args, **kwargs)

def ForeignKey(*args, **kwargs):
    """
    Instantiate a :class:`django.db.models.ForeignKey` using
    :func:`pointer_factory`.
    """
    return pointer_factory(models.ForeignKey, *args, **kwargs)


class CustomField(object):
    """
    Mixin to create a custom field.

    It defines a single method :meth:`create_layout_elem`.
    """
    def create_layout_elem(self, base_class, layout_handle, field, **kw):
        """Return the widget to represent this field in the specified
        `layout_handle`.

        The widget must be an instance of the given `base_class`.

        `self` and `field` are identical unless `self` is a
        :class`RemoteField` or a :class:`VirtualField`.

        """
        return None


class ImportedFields(object):
    """
    Mixin for models which have "imported fields".
    """
    _imported_fields = set()

    @classmethod
    def declare_imported_fields(cls, names):
        cls._imported_fields = cls._imported_fields | set(
            fields_list(cls, names))
        #~ logger.info('20120801 %s.declare_imported_fields() --> %s' % (
            #~ cls,cls._imported_fields))



class TableRow(object):

    """Base class for everything that can be used as a table row. """

    _lino_default_table = None

    hidden_columns = frozenset()
    """If specified, this is the default value for
    :attr:`hidden_columns<lino.core.tables.AbstractTable.hidden_columns>`
    of every `Table` on this model.

    """

    @classmethod
    def setup_parameters(cls, params):
        """Inheritable hook for defining parameters for every actor on this model.

        Called at site startup once for each actor using this model.

        Toes not return anything. Receives a `dict` object `params` and is
        expected to update that `dict`, which will be used to fill the actor's
        :attr:`parameters`.

        See also :meth:`get_simple_parameters`.

        """
        pass

    @classmethod
    def get_simple_parameters(cls):
        """
        Return or yield a list of names of simple parameter fields of every
        actor that uses this model.

        When the list contains names for which no parameter field is
        defined, then Lino creates that parameter field as a copy of
        the database field of the same name.

        This is also called by :meth:`get_title_tags`, you don't need to
        manually define title tags for simple parameters.

        """
        return []



    @classmethod
    def get_default_table(self):
        """Used internally. Lino chooses during the kernel startup, for each
        model, one of the discovered Table subclasses as the "default
        table".

        """
        return self._lino_default_table  # set in dbtables.py

    @classmethod
    def get_data_elem(cls, name):
        return None

        # v = getattr(cls, name, None)
        # if isinstance(v, VirtualField):
        #     return v

        # return getattr(cls, name, None)


        # return get_class_attr(cls, name)

        # v = get_class_attr(cls, name)
        # if v is not None:
        #     if isinstance(v, fields.DummyField):
        #         return v
        #     raise Exception("Oops, {} on {} is {}".format(name, cls, v))

    def obj2href(self, ar, *args, **kwargs):
        """Return a html representation of a pointer to the given database
        object.

        Examples see :ref:`obj2href`.

        """
        if ar is None:
            if len(args):
                return args[0]
            return str(self)
        return ar.obj2html(self, *args, **kwargs)

    def get_detail_action(self, ar):
        """Return the (bound) detail action to use for showing this object in
        a detail window.  Return `None` when no detail form exists or
        the requesting user has no permission to see it.

        `ar` is the action request who asks to see a detail.
        If the action requests's actor can be used for this model,
        then use its `detail_action`. Otherwise use the
        `detail_action` of this model's default table.

        When `ar` is `None`, the permission check is bypassed.

        If `self` has a special attribute `_detail_action` defined,
        return this.  This magic is used by
        :meth:`Menu.add_instance_action
        <lino.core.menus.Menu.add_instance_action>`.

        Usage example: :class:`courses.Course
        <lino_xl.lib.courses.models.Course>` overrides this to return
        the detail_action depending on the CourseArea.

        """
        a = getattr(self, '_detail_action', None)
        if a is None:
            if ar and ar.actor and ar.actor.model \
               and self.__class__ is ar.actor.model:
                a = ar.actor.detail_action
            else:
                # if ar and ar.actor and ar.actor.model:
                #     print("20170902 {} : {} is not {}".format(
                #         ar.actor, self.__class__, ar.actor.model))
                dt = self.__class__.get_default_table()
                if dt is not None:
                    a = dt.detail_action
        if a is None or ar is None:
            return a
        if a.get_view_permission(ar.get_user().user_type):
            return a

    def get_choices_text(self, request, actor, field):
        """
        Return the text to be displayed when an instance of this model
        is being used as a choice in a combobox of a ForeignKey field
        pointing to this model.
        `request` is the web request,
        `actor` is the requesting actor.

        The default behaviour is to simply return `str(self)`.

        A usage example
        is :class:`lino_xl.lib.countries.Place`.

        """
        return str(self)

    def get_overview_elems(self, ar):
        """This is expected to return a list of HTML elements to be wrapped
        into a `<DIV>`.

        """
        # return [ar.obj2html(self)]
        return [self.obj2href(ar)]

    def save_existing_instance(self, ar):
        watcher = ChangeWatcher(self)
        ar.ah.store.form2obj(ar, ar.rqdata, self, False)
        self.full_clean()
        self.save_watched_instance(ar, watcher)


def wildcard_data_elems(model):
    """
    Yield names to be used as wildcard in the :attr:`column_names` of a
    table or when :func:`fields_list` finds a ``*``.
    """
    meta = model._meta
    for f in meta.fields:
        # if not isinstance(f, fields.RichTextField):
        if isinstance(f, VirtualField):
            if f.wildcard_data_elem:
                yield f
        else:
            if not getattr(f, '_lino_babel_field', False):
                yield f
    for f in meta.many_to_many:
        yield f
    for f in meta.private_fields:
        #if not isinstance(f, VirtualField):
        yield f
    # todo: for slave in self.report.slaves


def use_as_wildcard(de):
    if de.name.endswith('_ptr'):
        return False
    return True


def fields_list(model, field_names):
    """
    Return a set with the names of the specified fields, checking
    whether each of them exists.

    Arguments: `model` is any subclass of `django.db.models.Model`. It
    may be a string with the full name of a model
    (e.g. ``"myapp.MyModel"``).  `field_names` is a single string with
    a space-separated list of field names.

    If one of the names refers to a dummy field, this name will be ignored
    silently.

    For example if you have a model `MyModel` with two fields `foo` and
    `bar`, then ``dd.fields_list(MyModel,"foo bar")`` will return
    ``['foo','bar']`` and ``dd.fields_list(MyModel,"foo baz")`` will raise
    an exception.

    TODO: either rename this to `fields_set` or change it to return an
    iterable on the fields.
    """
    lst = set()
    names_list = field_names.split()

    for name in names_list:
        if name == '*':
            explicit_names = set()
            for name in names_list:
                if name != '*':
                    explicit_names.add(name)
            for de in wildcard_data_elems(model):
                if not isinstance(de, DummyField):
                    if de.name not in explicit_names:
                        if use_as_wildcard(de):
                            lst.add(de.name)
        else:
            e = model.get_data_elem(name)
            if e is None:
                raise models.FieldDoesNotExist(
                    "No data element %r in %s" % (name, model))
            if not hasattr(e, 'name'):
                raise models.FieldDoesNotExist(
                    "%s %r in %s has no name" % (e.__class__, name, model))
            if isinstance(e, DummyField):
                pass
            else:
                lst.add(e.name)
    return lst


def pointer_factory(cls, othermodel, *args, **kw):
    """
    Instantiate a `ForeignKey` or `OneToOneField` with some subtle
    differences:

    - It supports `othermodel` being `None` or the name of some
      non-installed model and returns a :class:`DummyField` in that
      case.  This difference is useful when designing reusable models.

    - Explicitly sets the default value for `on_delete
      <https://docs.djangoproject.com/en/1.11/ref/models/fields/#django.db.models.ForeignKey.on_delete>`__
      to ``CASCADE`` (as required by Django 2).
    """
    if othermodel is None:
        return DummyField(othermodel, *args, **kw)
    if isinstance(othermodel, str):
        if not settings.SITE.is_installed_model_spec(othermodel):
            return DummyField(othermodel, *args, **kw)

    kw.setdefault('on_delete', models.CASCADE)
    return cls(othermodel, *args, **kw)


def make_remote_field(model, name):
    parts = name.split('__')
    if len(parts) == 1:
        return
    # It's going to be a RemoteField
    # logger.warning("20151203 RemoteField %s in %s", name, cls)

    from lino.core import store
    cls = model
    field_chain = []
    editable = False
    leaf_chooser = None
    for n in parts:
        if model is None:
            return
            # raise Exception(
            #     "Invalid remote field {0} for {1}".format(name, cls))

        if isinstance(model, str):
            # Django 1.9 no longer resolves the
            # rel.model of ForeignKeys on abstract
            # models, so we do it here.
            model = resolve_model(model)
            # logger.warning("20151203 %s", model)

        fld = model.get_data_elem(n)
        if fld is None:
            return
            # raise Exception(
            #     "Invalid RemoteField %s.%s (no field %s in %s)" %
            #     (full_model_name(model), name, n, full_model_name(model)))

        # make sure that the atomizer gets created.
        store.get_atomizer(model, fld, fld.name)

        if isinstance(fld, VirtualField):
            fld.lino_resolve_type()
        leaf_chooser = choosers.check_for_chooser(model, fld)

        field_chain.append(fld)
        if isinstance(fld, models.OneToOneRel):
            editable = True
        if getattr(fld, 'remote_field', None):
            model = fld.remote_field.model
        else:
            model = None

    if leaf_chooser is not None:
        d = choosers.get_choosers_dict(cls)
        d[name] = leaf_chooser

    def getter(obj, ar=None):
        try:
            for fld in field_chain:
                if obj is None:
                    return None
                obj = fld._lino_atomizer.full_value_from_object(
                    obj, ar)
            return obj
        except Exception as e:
            # raise
            msg = "Error while computing {}: {} ({} in {})"
            raise Exception(msg.format(
                name, e, fld, field_chain))
            # ~ if False: # only for debugging
            if True:  # see 20130802
                logger.exception(e)
                return str(e)
            return None

    if not editable:
        rf = RemoteField(getter, name, fld)
        # choosers.check_for_chooser(model, rf)
        return rf

    def setter(obj, value):
        # logger.info("20180712 %s setter() %s", name, value)
        # all intermediate fields are OneToOneRel
        target = obj
        try:
            for fld in field_chain:
                # print("20180712a %s" % fld)
                if isinstance(fld, models.OneToOneRel):
                    reltarget = getattr(target, fld.name, None)
                    if reltarget is None:
                        rkw = { fld.field.name: target}
                        # print(
                        #     "20180712 create {}({})".format(
                        #         fld.related_model, rkw))
                        reltarget = fld.related_model(**rkw)
                        reltarget.full_clean()
                        reltarget.save()

                    setattr(target, fld.name, reltarget)
                    target.full_clean()
                    target.save()
                    # print("20180712b {}.{} = {}".format(
                    #     target, fld.name, reltarget))
                    target = reltarget
                else:
                    setattr(target, fld.name, value)
                    target.full_clean()
                    target.save()
                    # print(
                    #     "20180712c setattr({},{},{}".format(
                    #         target, fld.name, value))
                    return True
        except Exception as e:
            raise e.__class__(
                "Error while setting %s: %s" % (name, e))
            # ~ if False: # only for debugging
            if True:  # see 20130802
                logger.exception(e)
                return str(e)
            return False

    rf = RemoteField(getter, name, fld, setter)
    # choosers.check_for_chooser(model, rf)
    return rf

# # would be nice for lino_xl.lib.vat.VatItemBase.item_total
# class FieldAlias(VirtualField):
#     def __init__(self, orig_name):
#         ...
#
#
