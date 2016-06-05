# -*- coding: UTF-8 -*-
# Copyright 2008-2016 Luc Saffre
# License: BSD (see file COPYING for details)

"""
Defines the classes :class:`Choice` and :class:`ChoiceList`.  See
:doc:`/dev/choicelists`.


Defining your own ChoiceLists
-----------------------------

>>> class MyColors(Choicelist):
...     verbose_name_plural = "My colors"
>>> MyColors.add_item('01', ("Red"), 'red')
>>> MyColors.add_item('02', ("Green"), 'green')

`add_item` takes at least 2 and optionally a third positional argument:

- The `value` is used to store this Choice in the database and for
  sorting the choices.
- The `text` is what the user sees. It should be translatable.
- The optional `name` is used to install this choice as a class
  attribute on the ChoiceList.

  
The `value` must be a string.
  
>>> MyColors.add_item(1, _("Green"), 'green')
>>> MyColors.add_item(1, _("Green"), 'verbose_name_plural')
  

ChoiceListField
---------------

Example on how to use a ChoiceList in your model::

  from django.db import models
  from lino.modlib.properties.models import HowWell
  
  class KnownLanguage(models.Model):
      spoken = HowWell.field(verbose_name=_("spoken"))
      written = HowWell.field(verbose_name=_("written"))

Every user-defined subclass of ChoiceList is also
automatically available as a property value in
:mod:`lino.modlib.properties`.
"""
from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from past.builtins import cmp
from past.builtins import basestring
from builtins import object
from builtins import str
from future.utils import with_metaclass
import six

import logging
logger = logging.getLogger(__name__)

import warnings

from django.utils.translation import ugettext_lazy as _
from django.utils.functional import lazy
from django.db import models
from django.conf import settings

from atelier.utils import assert_pure
from lino.core import actions
from lino.core import actors
from lino.core import tables
from lino.core import fields
from lino.core.exceptions import UnresolvedChoice


STRICT = True
VALUE_FIELD = models.CharField(_("value"), max_length=20)
VALUE_FIELD.attname = 'value'


@python_2_unicode_compatible
class Choice(object):
    """A constant value whose unicode representation depends on the
    current language at runtime.  Every item of a :class:`ChoiceList`
    must be an instance of :class:`Choice` or a subclass thereof.

    """
    choicelist = None
    remark = None
    pk = None
    value = None
    """(a string) The value to use e.g. when this choice is being
                stored in a database."""
    text = None
    """A translatable string containing the text to show to the user.

    """

    name = None
    """A string to be used as attribute name on the choicelist for
    referring to this choice from application code.

    If this is `None` or not specified, the choice is a nameless
    choice, which is a full-fledged choice object but is not
    accessible as a class attribute on its choicelists

    """

    def __init__(self, value, text=None, name=None, **kwargs):
        """Create a new :class:`Choice` instance.
    
        Parameters: see :attr:`value`, :attr:`text` and :attr:`name`.
        Any keyword arguments will become attributes on the instance.

        This is also being called from :meth:`Choicelist.add_item`.
    
        """
        if not isinstance(value, basestring):
            raise Exception("value must be a string")
        self.pk = self.value = value
        self.name = name
        # if name is not None:
        #     if self.name is None:
        #         self.name = value
        # else:
        #     self.name = name
        if text is None:
            if self.text is None:
                self.text = self.__class__.__name__
        else:
            # assert_pure(text)
            self.text = text
        for k, v in list(kwargs.items()):
            setattr(self, k, v)

    def update(self, **kwargs):
        for k, v in list(kwargs.items()):
            if not hasattr(self, k):
                raise Exception("%s has no attribute `%s`" % (self, k))
            setattr(self, k, v)

    def attach(self, choicelist):
        self.choicelist = choicelist

    def __len__(self):
        return len(self.value)

    def __cmp__(self, other):
        if other.__class__ is self.__class__:
            return cmp(self.value, other.value)
        return cmp(self.value, other)

    #~ 20120620: removed to see where it was used
    #~ def __getattr__(self,name):
        #~ return curry(getattr(self.choicelist, name),self)

    def __repr__(self):
        if self.name is None:
            return "<%s:%s>" % (self.choicelist.__name__, self.value)
        else:
            return "<%s.%s:%s>" % (
                self.choicelist.__name__, self.name, self.value)

    # def __str__(self):
    #     if self.name:
    #         return str(self.name)
    #     return str(self.text)

    def __str__(self):
        # return force_text(self.text, errors="replace")
        # return self.text
        return str(self.text)

    def as_callable(self):
        """Return this as a callable so it can be used as `default` of a
        field. A Choice object may not be callable itself because
        Django 1.9 would misunderstand it.

        """
        return self
        # def f():
        #     return self
        # return f

    # def __call__(self):
    #     """Make it callable so it can be used as `default` of a field."""
    #     return self

    @classmethod
    def get_chooser_for_field(cls, fieldname):
        return None

    def get_typed_instance(self, model):
        """
        Used when implementing :ref:`polymorphism`.
        """
        return self


class UnresolvedValue(Choice):
    def __init__(self, choicelist, value):
        self.choicelist = choicelist
        self.value = value
        self.text = "Unresolved value %r for %s" % (
            value, choicelist.__name__)
        self.name = None


CHOICELISTS = {}


def register_choicelist(cl):
    #~ print '20121209 register_choicelist', cl
    #~ k = cl.stored_name or cl.__name__
    k = cl.stored_name or cl.actor_id
    if k in CHOICELISTS:
        raise Exception(
            "Cannot register %r : actor name '%s' "
            "already defined by %r" % (cl, k, CHOICELISTS[k]))
        # logger.warning("ChoiceList name '%s' already defined by %s",
        #                k, CHOICELISTS[k])
    CHOICELISTS[k] = cl


def get_choicelist(i):
    return CHOICELISTS[i]


def choicelist_choices():
    """Return a list of all choicelists defined for this application."""
    l = []
    for k, v in list(CHOICELISTS.items()):
        if v.verbose_name_plural is None:
            text = v.__name__
        else:
            text = v.verbose_name_plural
        l.append((k, text))
    l.sort(lambda a, b: cmp(a[0], b[0]))
    return l


class ChoiceListMeta(actors.ActorMetaClass):

    def __new__(meta, classname, bases, classDict):
        #~ if not classDict.has_key('app_label'):
            #~ classDict['app_label'] = cls.__module__.split('.')[-2]
        """
        UserGroups manually sets `max_length` because the
        default list has only one group with value "system",
        but applications may want to add longer group names
        """
        if 'label' in classDict:
            raise Exception("label replaced by verbose_name_plural")
        classDict.setdefault('max_length', 1)
        cls = actors.ActorMetaClass.__new__(meta, classname, bases, classDict)

        cls.items_dict = {}
        cls.clear()
        cls._fields = []
        #~ cls.max_length = 1
        #~ assert not hasattr(cls,'items') 20120620
        #~ for i in cls.items:
            #~ cls.add_item(i)
        if classname not in ('ChoiceList', 'Workflow'):
            #~ if settings.SITE.is_installed(cls.app_label):
            register_choicelist(cls)
        return cls


#~ choicelist_column_fields = dict()
#~ choicelist_column_fields['value'] = fields.VirtualField(models.CharField())
#~ choicelist_column_fields['text'] = fields.VirtualField(models.CharField())
#~ choicelist_column_fields['name'] = fields.VirtualField(models.CharField())


class ChoiceList(with_metaclass(ChoiceListMeta, tables.AbstractTable)):

    """
    User-defined choice lists must inherit from this base class.
    """

    workflow_actions = []

    item_class = Choice
    """
    The class of items of this list.
    """

    auto_fit_column_widths = True

    preferred_foreignkey_width = 20
    """
    Default preferred with for ChoiceList fields to this list.
    """

    stored_name = None
    """Every subclass of ChoiceList will be automatically registered.
    Define this if your class's name clashes with the name of an
    existing ChoiceList.

    """

    verbose_name = None
    verbose_name_plural = None

    show_values = False
    """Set this to `True` if the user interface should include the `value`
    attribute of each choice.

    """

    preferred_width = None
    """Preferred width (in characters) used by
    :class:`fields<lino.core.fields.ChoiceListField>` that refer to
    this list.

    If this is `None`, then Lino calculates the value at startup,
    taking the length of the longest choice text.  The hard-coded
    absolute minimum in that case is 4.  Note that it calculates the
    value using the :attr:`default site language
    <lino.site.Site.languages>` and thus might guess wrong if the user
    language is not the default site language.

    Note that by this we mean the width of the bare text field,
    excluding any UI-specific control like the trigger button of a
    combobox.  That's why e.g. :mod:`lino.modlib.extjs.ext_elems` adds
    another value for the trigger button.

    """

    pk = True  # added 20150218.

    @classmethod
    def get_default_action(cls):
        return actions.GridEdit()

    hidden_columns = frozenset(['workflow_buttons'])

    column_names = 'value name text *'

    @classmethod
    def get_column_names(self, ar):
        return self.column_names

    @classmethod
    def get_data_elem(self, name):
        de = super(ChoiceList, self).get_data_elem(name)
        if de:
            return de
        return getattr(self, name)
        #~ return _choicelist_column_fields.get(name)

    @fields.virtualfield(VALUE_FIELD)
    def value(cls, choice, ar):
        return choice.value

    @fields.virtualfield(models.CharField(_("text"), max_length=50))
    def text(cls, choice, ar):
        return choice.text

    @fields.virtualfield(models.CharField(_("name"), max_length=20))
    def name(cls, choice, ar):
        return choice.name or ''

    @fields.displayfield(_("Remark"))
    def remark(cls, choice, ar):
        return choice.remark

    @classmethod
    def get_data_rows(self, ar=None):
        return list(self.items())

    @classmethod
    def get_actor_label(self):
        """
        Compute the label of this actor.
        Called only if `label` is not set, and only once during site startup.
        """
        return self._label or self.verbose_name_plural or self.__name__

    @classmethod
    def clear(cls):
        """
        """
        # remove previously defined choices from class dict:
        for ci in list(cls.items_dict.values()):
            if ci.name:
                delattr(cls, ci.name)
        cls.items_dict = {}
        cls.choices = []
        cls.choices = []  # remove blank_item from choices

    @classmethod
    def setup_field(cls, fld):
        pass

    @classmethod
    def field(cls, *args, **kw):
        """Create a database field (a :class:`ChoiceListField`) that holds
        one value of this choicelist.

        """
        fld = ChoiceListField(cls, *args, **kw)
        cls.setup_field(fld)
        cls._fields.append(fld)
        return fld

    @classmethod
    def multifield(cls, *args, **kw):
        """
        Not yet implemented.
        Create a database field (a :class:`ChoiceListField`)
        that holds a set of multiple values of this choicelist.
        """
        fld = MultiChoiceListField(cls, *args, **kw)
        cls._fields.append(fld)
        return fld

    @classmethod
    def add_item(cls, *args, **kw):
        """Instantiates a new choice and adds it to this list. Signature is
        that of the :meth:`Choice.__init__` method (which might have
        been overridden if you defined a customized
        :attr:`item_class`.

        """
        return cls.add_item_instance(
            cls.item_class(*args, **kw))

    @classmethod
    def class_init(cls):
        super(ChoiceList, cls).class_init()
        if cls.preferred_width is None:
            pw = 4
            for i in cls.get_list_items():
                dt = cls.display_text(i)
                pw = max(pw, len(dt))
            cls.preferred_width = pw

    @classmethod
    def add_item_instance(cls, i):
        #~ if cls is ChoiceList:
            #~ raise Exception("Cannot define items on the base class")
        is_duplicate = False
        if i.value in cls.items_dict:
            raise Exception("Duplicate value %r in %s." % (i.value, cls))
            warnings.warn("Duplicate value %r in %s." % (i.value, cls))
            is_duplicate = True
        i.attach(cls)
        dt = cls.display_text(i)
        cls.choices.append((i, dt))
        # cls.preferred_width = max(cls.preferred_width, len(unicode(dt)))
        cls.items_dict[i.value] = i
        #~ cls.items_dict[i] = i
        if len(i.value) > cls.max_length:
            if len(cls._fields) > 0:
                raise Exception(
                    "%s cannot add value %r because fields exist "
                    "and max_length is %d."
                    % (cls, i.value, cls.max_length) + """\
When fields have been created, we cannot simply change their max_length because
Django creates copies of them when inheriting models.
""")
            cls.max_length = len(i.value)
            #~ for fld in cls._fields:
                #~ fld.set_max_length(cls.max_length)
        if i.name:
            if not is_duplicate:
                if i.name in cls.__dict__:
                    raise Exception(
                        "An item named %r is already defined in %s" % (
                            i.name, cls.__name__))
            setattr(cls, i.name, i)
            #~ i.name = name
        return i

    @classmethod
    def get_pk_field(self):
        """See :meth:`lino.core.actors.Actor.get_pk_field`.
        """
        return VALUE_FIELD

    @classmethod
    def get_row_by_pk(cls, ar, pk):
        return cls.get_by_value(pk)

    @classmethod
    def to_python(cls, value):
        # if isinstance(value, Choice):
        #     return value
        if not value:
            return None
        v = cls.items_dict.get(value)
        if v is None:
            if settings.SITE.strict_choicelist_values:
                raise UnresolvedChoice(
                    "Unresolved value %r (%s) for %s (set "
                    "Site.strict_choicelist_values to False "
                    "to ignore this)" % (
                        value, value.__class__, cls))
            else:
                return UnresolvedValue(cls, value)
        return v
        # Hamza, why did you replace above line by the following ones?
        # if hasattr(v,'value'):
        #     return v.value
        # else:
        #     return v
        #~ return cls.items_dict.get(value) or UnresolvedValue(cls,value)
        #~ return cls.items_dict[value]

    #~ @classmethod
    #~ def get_label(cls):
        #~ if cls.label is None:
            #~ return cls.__name__
        #~ return _(cls.label)

    @classmethod
    def get_choices(cls):
        return cls.choices

    #~ @classmethod
    #~ def get_choices(cls):
        #~ """
        #~ We must make it dynamic since e.g. UserProfiles can change after
        #~ the fields have been created.

        #~ https://docs.djangoproject.com/en/dev/ref/models/fields/
        #~ note that choices can be any iterable object -- not necessarily
        #~ a list or tuple. This lets you construct choices dynamically.
        #~ But if you find yourself hacking choices to be dynamic, you're
        #~ probably better off using a proper database table with a
        #~ ForeignKey. choices is meant for static data that doesn't
        #~ change much, if ever.
        #~ """
        #~ for c in cls.choices:
            #~ yield c

    @classmethod
    def display_text(cls, bc):
        """Return the text to be used for representing the given choice
        instance `bc` to the user.

        Override this to customize the display text of choices.
        :class:`lino.modlib.users.choicelists.UserGroups` and
        :class:`lino.modlib.cv.models.CefLevel` used to do this before
        we had the :attr:`ChoiceList.show_values` option.

        This must be lazyly translatable because the result are also
        used to build the `choices` attribute of ChoiceListFields on
        this choicelist.

        Note that Django's `lazy` function has a list of
        "resultclasses" which are used "so that the automatic forcing
        of the lazy evaluation code is triggered".

        """
        if cls.show_values:
            # if unicodeerror:
            # assert_pure(str(bc))
            # str(bc)

            def fn(bc):
                # return "%s (%s)" % (bc.value, str(bc))
                return "{0} ({1})".format(bc.value, bc)
            return lazy(fn, str, six.text_type)(bc)
        return lazy(str, str, six.text_type)(bc)

    @classmethod
    def get_by_name(self, name, *args):
        """
        Supports the case that `name` is `None` (returns `None` then).
        """
        if name:
            return getattr(self, name, *args)
        else:
            return None

    @classmethod
    def get_by_value(self, value, *args):
        """Return the item (a :class:`Choice` instance) corresponding to the
        specified `value`.

        """
        if not isinstance(value, basestring):
            raise Exception("%r is not a string" % value)
        #~ print "get_text_for_value"
        #~ return self.items_dict.get(value, None)
        #~ return self.items_dict.get(value)
        return self.items_dict.get(value, *args)

    #~ @classmethod
    #~ def items(self):
        #~ return [choice[0] for choice in self.choices]

    @classmethod
    def filter(self, **fkw):
        def f(item):
            for k, v in list(fkw.items()):
                if getattr(item, k) != v:
                    return False
            return True
        return [choice[0] for choice in self.choices if f(choice[0])]

    @classmethod
    def get_list_items(self):
        return [choice[0] for choice in self.choices]
    objects = get_list_items
    items = get_list_items

    @classmethod
    def get_text_for_value(self, value):
        """
        Return the text corresponding to the specified value.
        """
        bc = self.get_by_value(value)
        if bc is None:
            return _("%(value)r (invalid choice for %(list)s)") % dict(
                list=self.__name__, value=value)
        return self.display_text(bc)


class ChoiceListField(models.CharField):

    """A field that stores a value to be selected from a
    :class:`ChoiceList`.
    
    ChoiceListField cannot be nullable since they are implemented as
    CharFields.  Therefore when filtering on empty values in a
    database query you cannot use ``__isnull``.  The following query
    won't work as expected::
    
      for u in users.User.objects.filter(profile__isnull=False):
      
    You must either check for an empty string::
      
      for u in users.User.objects.exclude(profile='')

    or use the ``__gte`` operator::
      
      for u in users.User.objects.filter(profile__gte=dd.UserLevels.guest):

    """

    empty_strings_allowed = False

    def __init__(self, choicelist, verbose_name=None,
                 force_selection=True, **kw):
        if verbose_name is None:
            verbose_name = choicelist.verbose_name
        self.choicelist = choicelist
        self.force_selection = force_selection
        defaults = dict(
            #~ choices=KNOWLEDGE_CHOICES,
            #~ choices=choicelist.get_choices(),
            max_length=choicelist.max_length,
            # ~ blank=choicelist.blank,  # null=True,
            #~ validators=[validate_knowledge],
            #~ limit_to_choices=True,
        )
        defaults.update(kw)
        kw.update(kw)
        #~ models.SmallIntegerField.__init__(self,*args, **defaults)
        models.CharField.__init__(self, verbose_name, **defaults)

    # def contribute_to_class(self, cls, name):
    #     super(ChoiceListField, self).contribute_to_class(cls, name)
    #     # add workflow actions to the model so that we can access them
    #     # as InstanceActions
    #     logger.info("20150122 %s %s", cls, name)
    #     for a in self.choicelist.workflow_actions:
    #         logger.info("20150122 %s %s", a.action_name, a)
    #         setattr(cls, a.action_name, a)
    
    def deconstruct(self):
        """Needed for Django 1.7+, see
        https://docs.djangoproject.com/en/dev/howto/custom-model-fields/#custom-field-deconstruct-method

        """

        name, path, args, kwargs = super(ChoiceListField, self).deconstruct()
        args = [self.choicelist]

        # kwargs.pop('default', None)
        # TODO: above line is cheating in order to get makemigrations
        # to pass. we remove the default attribute because it is not
        # serializable. This means that our migrations are probably
        # invalid and not usable.

        return name, path, args, kwargs

    def get_internal_type(self):
        return "CharField"

    #~ def set_max_length(self,ml):
        #~ self.max_length = ml

    def from_db_value(self, value, expression, connection, context):
        if value is None:
            return None
        return self.choicelist.to_python(value)

    def to_python(self, value):
        """See Django's docs about `to_python()
        <https://docs.djangoproject.com/en/1.9/ref/models/fields/#django.db.models.Field.to_python>`__.

        """
        #~ if self.attname == 'query_register':
            #~ print '20120527 to_python', repr(value), '\n'
        if isinstance(value, Choice):
            return value
        return self.choicelist.to_python(value)

    def _get_choices(self):
        """HACK: Django by default stores a copy of our list when the
        `choices` of a field are evaluated for the first time. We
        don't want that because ChoiceLists may change afterwards.

        """
        return self.choicelist.choices

    def _set_choices(self, value):
        # if value != []:
        #     logger.warning("Ignoring set choices {0}".format(value))
        return

    choices = property(_get_choices, _set_choices)

    def get_prep_value(self, value):
        """Excerpt from `Django docs
        <https://docs.djangoproject.com/en/1.9/howto/custom-model-fields/#converting-python-objects-to-query-values>`__:
        "If you override `to_python()
        <https://docs.djangoproject.com/en/1.9/ref/models/fields/#django.db.models.Field.to_python>`__ you also have to override
        `get_prep_value()
        <https://docs.djangoproject.com/en/1.9/ref/models/fields/#django.db.models.Field.get_prep_value>`__ to
        convert Python objects back to query values."

        """
        #~ if self.attname == 'query_register':
            #~ print '20120527 get_prep_value()', repr(value)
        #~ return value.value
        # Hamza, why did you add the following 2 lines?
        # if isinstance(value,unicode):
        #     return str(value)
        if value:
            if callable(value):  # Django 1.9
                value = value()
            value = self.to_python(value)  # see Luc's blog 20160204
            return value.value
        return ''
        #~ return None

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        #~ if self.attname == 'query_register':
            #~ print '20120527 value_to_string', repr(value)
        return self.get_prep_value(value)
        #~ return self.get_db_prep_value(value,connection)

    #~ def save_form_data(self, instance, data):
        #~ setattr(instance, self.name, data)

    def get_text_for_value(self, value):
        return self.choicelist.get_text_for_value(value.value)


class MultiChoiceListField(ChoiceListField):
    """
    A field whose value is a `list` of `Choice` instances.
    Stored in the database as a CharField using a delimiter character.
    """
    delimiter_char = ','
    max_values = 1

    def __init__(self, choicelist, verbose_name=None, max_values=10, **kw):
        if verbose_name is None:
            verbose_name = choicelist.verbose_name_plural
        self.max_values = max_values
        defaults = dict(
            max_length=(choicelist.max_length + 1) * max_values
        )
        defaults.update(kw)
        ChoiceListField.__init__(self, verbose_name, **defaults)

    #~ def set_max_length(self,ml):
        #~ self.max_length = (ml+1) * self.max_values

    def from_db_value(self, value, expression, connection, context):
        return [self.choicelist.to_python(v) for v in value.split(self.delimiter_char)]

    def to_python(self, value):
        if value is None:
            return []
        if isinstance(value, list):
            return value
        value = [self.choicelist.to_python(v)
                 for v in value.split(self.delimiter_char)]
        return value

    def get_prep_value(self, value):
        """
        This must convert the given Python value (always a list)
        into the value to be stored to database.
        """
        return self.delimiter_char.join([bc.value for bc in value])

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_prep_value(value)

    def get_text_for_value(self, value):
        return ', '.join([
            self.choicelist.get_text_for_value(bc.value) for bc in value])


def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()
