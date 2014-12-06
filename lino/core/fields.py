# -*- coding: UTF-8 -*-
# Copyright 2008-2014 Luc Saffre
# License: BSD (see file COPYING for details)

"""Defines extended field classes like :class:`RichTextField` and
:class:`PercentageField`, utility functions like
:func:`dd.fields_list`.

"""

import logging
from lino.utils.choosers import chooser

logger = logging.getLogger(__name__)

import datetime
from decimal import Decimal


from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes import generic
from django.db.models.fields import NOT_PROVIDED


from lino.core.dbutils import full_model_name
from lino.core.dbutils import obj2str

from lino.core.dbutils import resolve_field
from lino.core.dbutils import resolve_model, UnresolvedModel
#~ from lino.core.dbutils import is_installed_model_spec

from lino.utils import IncompleteDate, d2iso
from lino.utils import quantities


class PasswordField(models.CharField):

    """Stored as plain text in database, but not displayed in user
interface.

    """
    pass


class RichTextField(models.TextField):

    """
    Only difference with Django's `models.TextField` is that you can
    specify a keyword argument `format` to
    override the global :attr:`ad.Site.textfield_format`.
    """

    def __init__(self, *args, **kw):
        self.textfield_format = kw.pop('format', None)
        super(RichTextField, self).__init__(*args, **kw)

    def set_format(self, fmt):
        self.textfield_format = fmt


#~ class PercentageField(models.SmallIntegerField):
    #~ """
    #~ Deserves more documentation.
    #~ """
    #~ def __init__(self, *args, **kw):
        #~ defaults = dict(
            #~ max_length=3,
            #~ )
        #~ defaults.update(kw)
        #~ models.SmallIntegerField.__init__(self,*args, **defaults)
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


class DatePickerField(models.DateField):

    """
    A DateField that uses a DatePicker instead of a normal DateWidget.
    Doesn't yet work.
    """


class MonthField(models.DateField):

    """
    A DateField that uses a MonthPicker instead of a normal DateWidget
    """

    def __init__(self, *args, **kw):
        models.DateField.__init__(self, *args, **kw)


class PriceField(models.DecimalField):

    """
    A Decimalfield with default values for decimal_places, max_length and max_digits.

    """

    def __init__(self, *args, **kwargs):
        defaults = dict(
            max_length=10,
            max_digits=10,
            decimal_places=2,
        )
        defaults.update(kwargs)
        super(PriceField, self).__init__(*args, **defaults)

    #~ def formfield(self, **kwargs):
        #~ fld = super(PriceField, self).formfield(**kwargs)
        # ~ # display size is smaller than full size:
        #~ fld.widget.attrs['size'] = "6"
        #~ fld.widget.attrs['style'] = "text-align:right;"
        #~ return fld

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


class NullCharField(models.CharField):  # subclass the CharField
    description = "CharField that stores empty strings as NULL instead of ''."

    def __init__(self, *args, **kwargs):
        defaults = dict(blank=True, null=True)
        defaults.update(kwargs)
        super(NullCharField, self).__init__(*args, **defaults)

    # this is the value right out of the db, or an instance
    def to_python(self, value):
        # ~ if isinstance(value, models.CharField): #if an instance, just return the instance
        if isinstance(value, basestring):  # if a string, just return the value
            return value
        if value is None:  # if the db has a NULL (==None in Python)
            return ''  # convert it into the Django-friendly '' string
        else:
            return value  # otherwise, return just the value

    def get_db_prep_value(self, value, connection, prepared=False):
    # catches value right before sending to db
        # if Django tries to save '' string, send the db None (NULL)
        if value == '':
            return None
        else:
            return value  # otherwise, just pass the value


class FakeField(object):

    """
    Base class for
    :class:`RemoteField`
    :class:`DisplayField`
    """
    model = None
    choices = []
    primary_key = False
    editable = False
    name = None
    #~ verbose_name = None
    help_text = None
    preferred_width = 30
    preferred_height = 3
    max_digits = None
    decimal_places = None
    default = NOT_PROVIDED

    def is_enabled(self, lh):
        """
        Overridden by mti.EnableChild
        """
        #~ return False
        #~ return True
        return self.editable

    def has_default(self):
        return self.default is not NOT_PROVIDED


class RemoteField(FakeField):

    """
    Represents a field on a related object.
    LayoutHandle instantiates a RemoteField for example when
    """
    #~ primary_key = False
    #~ editable = False

    def __init__(self, func, name, fld, **kw):
        self.func = func
        self.name = name
        self.field = fld
        self.rel = self.field.rel
        self.verbose_name = fld.verbose_name
        self.max_length = getattr(fld, 'max_length', None)
        self.max_digits = getattr(fld, 'max_digits', None)
        self.decimal_places = getattr(fld, 'decimal_places', None)
        #~ print 20120424, self.name
        #~ settings.SITE.register_virtual_field(self)

        from lino.ui import store
        store.get_atomizer(self.rel, self, name)

    #~ def lino_resolve_type(self):
        #~ self._lino_atomizer = self.field._lino_atomizer
    def value_from_object(self, obj, ar=None):
        """
        Return the value of this field in the specified model instance `obj`.
        `ar` may be `None`, it's forwarded to the getter method who may
        decide to return values depending on it.
        """
        m = self.func
        return m(obj, ar)

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return self.value_from_object(instance)


class DisplayField(FakeField):
    """
    Deserves more documentation.
    """
    choices = None
    blank = True
    drop_zone = None
    max_length = None
    #~ bbar = None

    def __init__(self, verbose_name=None, **kw):
        self.verbose_name = verbose_name
        for k, v in kw.items():
            assert hasattr(self, k)
            setattr(self, k, v)

    # the following dummy methods are never called but needed when
    # using a DisplayField as return_type of a VirtualField

    def to_python(self, *args, **kw):
        raise NotImplementedError(
            "%s.to_python(%s,%s)", (self.name, args, kw))

    def save_form_data(self, *args, **kw):
        raise NotImplementedError

    def value_to_string(self, *args, **kw):
        raise NotImplementedError

    def value_from_object(self, obj, ar=None):
        return ''

#~ class DynamicForeignKey(DisplayField):
    #~ """
    #~ A pointer to "the" one and only MTI child.
    #~ This assumes that there is always one and only one child instance among the given models.
    #~ """
    #~ def __init__(self,get_child,**kw):
        #~ self.get_child = get_child
        #~ VirtualField.__init__(self,models.ForeignKey(**kw),self.has_child)


class HtmlBox(DisplayField):

    """
    Deserves more documentation.
    """
    pass

#~ class QuickAction(DisplayField):
    #~ pass

#~ from django.db.models.fields import Field


class VirtualGetter(object):

    """
    A wrapper object for getting the content of
    a virtual field programmatically.
    """

    def __init__(self, vf, instance):
        self.vf = vf
        self.instance = instance

    def __call__(self, ar=None):
        return self.vf.value_from_object(self.instance, ar)

    def __getattr__(self, name):
        obj = self.vf.value_from_object(self.instance, None)
        return getattr(obj, name)


class VirtualField(FakeField):
    "See :class:`dd.VirtualField`."

    def __init__(self, return_type, get):
        self.return_type = return_type  # a Django Field instance
        self.get = get

        settings.SITE.register_virtual_field(self)
        """
        Normal VirtualFields are read-only and not editable.
        We don't want to require application developers to explicitly 
        specify `editable=False` in their return_type::
        
          @dd.virtualfield(dd.PriceField(_("Total")))
          def total(self,ar=None):
              return self.total_excl + self.total_vat
        """

    def override_getter(self, get):
        self.get = get

    def attach_to_model(self, model, name):
        self.model = model
        self.name = name
        #~ self.return_type.name = name
        #~ self.return_type.attname = name
        #~ if issubclass(model,models.Model):
        #~ self.lino_resolve_type(model,name)
        model._meta.add_virtual_field(self)
        #~ logger.info('20120831 VirtualField %s.%s',full_model_name(model),name)

    def __repr__(self):
        return "%s %s.%s" % (self.__class__.__name__, self.model, self.name)

    def lino_resolve_type(self):
        """
        Unlike attach_to_model, this is also called on virtual
        fields that are defined on an Actor
        """
        #~ logger.info("20120903 lino_resolve_type %s.%s", actor_or_model, name)
        #~ if self.name is not None:
            #~ if self.name != name:
                #~ raise Exception("Tried to re-use %s.%s" % (actor_or_model,name))
        #~ self.name = name

        if isinstance(self.return_type, basestring):
            self.return_type = resolve_field(self.return_type)

        #~ self.return_type.name = self.name
        if isinstance(self.return_type, models.ForeignKey):
            f = self.return_type
            f.rel.to = resolve_model(f.rel.to)
            if f.verbose_name is None:
                #~ if f.name is None:
                f.verbose_name = f.rel.to._meta.verbose_name
                    #~ from lino.core.kernel import set_default_verbose_name
                    #~ set_default_verbose_name(self.return_type)

        #~ removed 20120919 self.return_type.editable = self.editable
        for k in ('''to_python choices save_form_data
          value_to_string verbose_name max_length rel
          max_digits decimal_places
          help_text
          blank'''.split()):
            setattr(self, k, getattr(self.return_type, k, None))
        #~ logger.info('20120831 VirtualField %s on %s',name,actor_or_model)

        from lino.ui import store
        #~ self._lino_atomizer = store.create_field(self,self.name)
        store.get_atomizer(self.model, self, self.name)

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

    #~ def to_python(self,*args,**kw): return self.return_type.to_python(*args,**kw)
    #~ def save_form_data(self,*args,**kw): return self.return_type.save_form_data(*args,**kw)
    #~ def value_to_string(self,*args,**kw): return self.return_type.value_to_string(*args,**kw)
    #~ def get_choices(self): return self.return_type.choices
    #~ choices = property(get_choices)

    def set_value_in_object(self, request, obj, value):
        """
        Stores the specified `value` in the specified model instance `obj`.
        `request` may be `None`.

        Note that any implementation must also return `obj`,
        and callers must be ready to get another instance.
        This special behaviour is needed to implement
        :class:`lino.utils.mti.EnableChild`.
        """
        raise NotImplementedError("Cannot write %r to field %s" %
                                  (value, self))

    #~ def value_from_object(self,request,obj):
    def value_from_object(self, obj, ar=None):
        """
        Return the value of this field in the specified model instance `obj`.
        `request` may be `None`, it's forwarded to the getter method who may
        decide to return values depending on it.
        """
        m = self.get
        #~ assert m.func_code.co_argcount == 2, (self.name, m.func_code.co_varnames)
        #~ print self.field.name
        return m(obj, ar)

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return VirtualGetter(self, instance)

    def __set__(self, instance, value):
        return self.set_value_in_object(None, instance, value)


def virtualfield(return_type):
    def decorator(fn):
        return VirtualField(return_type, fn)
    return decorator


class Constant(object):

    """
    Deserves more documentation.
    """

    def __init__(self, text_fn):
        self.text_fn = text_fn


def constant():
    """Decorator to turn a function into a :class:`Constant`.  The
    function must accept one positional argument `datasource`.

    """
    def decorator(fn):
        return Constant(fn)
    return decorator


class RequestField(VirtualField):
    "See :class:`dd.RequestField`."
    def __init__(self, get, *args, **kw):
        kw.setdefault('max_length', 8)
        VirtualField.__init__(self, DisplayField(*args, **kw), get)


def displayfield(*args, **kw):
    """
    Decorator shortcut to turn a method into a DisplayField.
    """
    return virtualfield(DisplayField(*args, **kw))


def htmlbox(*args, **kw):
    """
    Decorator shortcut to turn a method into a HtmlBox.
    """
    return virtualfield(HtmlBox(*args, **kw))


def requestfield(*args, **kw):
    """
    Decorator to make a RequestField from a method.
    The method to decorate must return either None or a TableRequest object.
    """
    def decorator(fn):
        #~ def wrapped(*args):
            #~ return fn(*args)
        #~ return RequestField(wrapped,*args,**kw)
        return RequestField(fn, *args, **kw)
    return decorator


class MethodField(VirtualField):

    """
    Not used. See `/blog/2011/1221`.
    Similar to VirtualField, but the `get` argument to `__init__`
    must be a string which is the name of a model method to be called
    without a `request`.
    """

    def __init__(self, return_type, get, *args, **kw):
        self.args = args
        self.kw = kw
        VirtualField.__init__(self, return_type, get)

    def attach_to_model(self, model, name):
        self.get = getattr(model, get)
        VirtualField.attach_to_model(self, model, name)

    #~ def value_from_object(self,request,obj):
    def value_from_object(self, obj, ar=None):
        """
        Return the value of this field in the specified model instance `obj`.
        `request` is ignored.
        """
        m = self.get
        return m(obj, *self.args, **self.kw)


class GenericForeignKeyIdField(models.PositiveIntegerField):

    """
    Use this instead of `models.PositiveIntegerField`
    for fields that part of a :term:`GFK` and you want
    Lino to render them using a Combobox.

    Used by :class:`ml.contenttypes.Controllable`.
    """

    def __init__(self, type_field, *args, **kw):
        self.type_field = type_field
        models.PositiveIntegerField.__init__(self, *args, **kw)

    def deconstruct(self):
        # needed for Django 1.7
        # https://docs.djangoproject.com/en/dev/howto/custom-model-fields/#custom-field-deconstruct-method

        name, path, args, kwargs = super(
            GenericForeignKeyIdField, self).deconstruct()
        args = [self.type_field]
        return name, path, args, kwargs


class GenericForeignKey(generic.GenericForeignKey):

    """Add verbose_name and help_text to Django's GFK.  Used by
    :class:`lino.mixins.Controllable`.

    """

    def __init__(self, ct_field="content_type", fk_field="object_id",
                 verbose_name=None, help_text=None, dont_merge=False):
        self.verbose_name = verbose_name
        self.help_text = help_text
        self.dont_merge = dont_merge
        generic.GenericForeignKey.__init__(self, ct_field, fk_field)

    def contribute_to_class(self, cls, name):
        """Automatically set-up chooser and display field for ID field of
        generic foreign key.

        """

        super(GenericForeignKey, self).contribute_to_class(cls, name)

        # Chooser
        fk_choices_name = "{fk_field}_choices".format(fk_field=self.fk_field)
        if not hasattr(cls, fk_choices_name):
            def fk_choices(obj, **kwargs):
                object_type = kwargs[self.ct_field]
                if object_type:
                    return object_type.model_class().objects.all()
                return []
            field = chooser(instance_values=True)(fk_choices)
            setattr(cls, fk_choices_name, field)

        # Display
        fk_display_name = "get_{fk_field}_display".format(
            fk_field=self.fk_field)
        if not hasattr(cls, fk_display_name):
            def fk_display(obj, value):
                ct = getattr(obj, self.ct_field)
                if ct:
                    try:
                        return unicode(ct.get_object_for_this_type(pk=value))
                    except ct.model_class().DoesNotExist:
                        return "%s with pk %r does not exist" % (
                            full_model_name(ct.model_class()), value)
            setattr(cls, fk_display_name, fk_display)


class CharField(models.CharField):

    """

    An extension around Django's `models.CharField`.

    Adds two keywords `mask_re` and
    `strip_chars_re` which, when using the ExtJS ui,
    will be rendered as the
    `maskRe` and `stripCharsRe` config options
    of
    `TextField`
    as described in the
    `ExtJS documentation
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
    A field that accepts both
    :class:`lino.utils.quantity.Decimal`,
    :class:`lino.utils.quantity.Percentage`
    and
    :class:`lino.utils.quantity.Duration`
    values.

    Implemented as a CharField (sorting or filter ranges may not work)

    QuantityFields are implemented as CharFields and
    therefore should *not* be declared `null=True`.
    But if `blank=True`, empty strings are converted to `None`
    values.

    """
    __metaclass__ = models.SubfieldBase
    description = _("Quantity (Decimal or Duration)")

    def __init__(self, *args, **kw):
        kw.setdefault('max_length', 6)
        models.Field.__init__(self, *args, **kw)
        #~ models.CharField.__init__(self,*args,**kw)

    #~ def get_internal_type(self):
        #~ return "CharField"

    def to_python(self, value):
        """

        Excerpt from `Django doc
        <https://docs.djangoproject.com/en/dev/howto/custom-model-fields/#django.db.models.Field.to_python>`__:

            As a general rule, the method should deal gracefully with any of the following arguments:

            - An instance of the correct type (e.g., Hand in our ongoing example).
            - A string (e.g., from a deserializer).
            - Whatever the database returns for the column type you’re using.

        I'd add "Any value specified for this field when instantiating a model."

        >>> to_python(None)
        >>> to_python(30)
        >>> to_python(30L)
        >>> to_python('')
        >>> to_python(Decimal(0))
        """
        if isinstance(value, Decimal):
            return value
        if value:
            if isinstance(value, basestring):
                return quantities.parse(value)
            return Decimal(value)
        return None

    #~ def get_db_prep_save(self, value, connection):
        #~ if value is None:
            #~ return ''
        #~ return str(value)

    def get_prep_value(self, value):
        if value is None:
            return ''
        return str(value)


class IncompleteDateField(models.CharField):

    """
    A field that behaves like a DateField, but accepts
    incomplete dates represented using
    :class:`lino.utils.IncompleteDate`.
    """
    __metaclass__ = models.SubfieldBase

    def __init__(self, *args, **kw):
        kw.update(max_length=11)
        msgkw = dict()
        msgkw.update(ex1=IncompleteDate(1980, 0, 0)
                     .strftime(settings.SITE.date_format_strftime))
        msgkw.update(ex2=IncompleteDate(1980, 7, 0)
                     .strftime(settings.SITE.date_format_strftime))
        msgkw.update(ex3=IncompleteDate(0, 7, 23)
                     .strftime(settings.SITE.date_format_strftime))
        kw.setdefault('help_text', _("""\
Uncomplete dates are allowed, e.g. 
"%(ex1)s" means "some day in 1980", 
"%(ex2)s" means "in July 1980"
or "%(ex3)s" means "on a 23th of July".""") % msgkw)
        models.CharField.__init__(self, *args, **kw)

    #~ def get_internal_type(self):
        #~ return "CharField"

    def to_python(self, value):
        if isinstance(value, IncompleteDate):
            return value
        if isinstance(value, datetime.date):
            #~ return IncompleteDate(value.strftime("%Y-%m-%d"))
            #~ return IncompleteDate(d2iso(value))
            return IncompleteDate.from_date(value)
        if value:
            return IncompleteDate.parse(value)
        return ''

    def get_prep_value(self, value):
        return str(value)

    #~ def get_prep_value(self, value):
        #~ return '"' + str(value) + '"'
        #~ if value:
            #~ return value.format("%04d%02d%02d")
        #~ return ''

    #~ def value_to_string(self, obj):
        #~ value = self._get_val_from_obj(obj)
        #~ return self.get_prep_value(value)


class Dummy(object):
    pass


class DummyField(FakeField):
    "See :class:`dd.DummyField`."
    # choices = []
    # primary_key = False

    def __init__(self, *args, **kw):
        pass

    # def __getattr__(self, name):
    #     return None

    def get_default(self):
        return None

    def contribute_to_class(self, cls, name):
        self.name = name
        assert not hasattr(cls, name)
        setattr(cls, name, self)

    def set_attributes_from_name(self, k):
        pass


class RecurrenceField(models.CharField):
    """
    Deserves more documentation.
    """
    #~ __metaclass__ = models.SubfieldBase

    def __init__(self, *args, **kw):
        kw.setdefault('max_length', 200)
        models.CharField.__init__(self, *args, **kw)


def fields_list(model, field_names):
    "See :func:`dd.fields_list`."
    lst = set()
    for name in field_names.split():
        e = model.get_data_elem(name)
        if e is None:
            raise models.FieldDoesNotExist(
                "No data element %r in %s" % (name, model))
        if not isinstance(e, DummyField):
            lst.add(e.name)
    return lst


def ForeignKey(othermodel, *args, **kw):
    "See :class:`dd.ForeignKey`."
    if othermodel is None:
        return DummyField(othermodel, *args, **kw)
    if isinstance(othermodel, basestring):
        if not settings.SITE.is_installed_model_spec(othermodel):
            return DummyField(othermodel, *args, **kw)
    return models.ForeignKey(othermodel, *args, **kw)


class CustomField(object):
    "See :class:`dd.CustomField`."
    def create_layout_elem(self, layout_handle, field, **kw):
        return None


class ImportedFields(object):
    """
    Model mixin to easily declare "imported fields"
    """
    _imported_fields = set()

    @classmethod
    def declare_imported_fields(cls, names):
        cls._imported_fields = cls._imported_fields | set(
            fields_list(cls, names))
        #~ logger.info('20120801 %s.declare_imported_fields() --> %s' % (
            #~ cls,cls._imported_fields))

