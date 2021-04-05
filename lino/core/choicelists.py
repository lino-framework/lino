# -*- coding: UTF-8 -*-
# Copyright 2008-2020 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

"""
Defines the classes :class:`Choice` and :class:`ChoiceList`.  See
:doc:`/dev/choicelists`.
"""

from future.utils import with_metaclass
from past.builtins import cmp

import warnings

from django.utils.translation import gettext_lazy as _
from django.utils.functional import lazy
from django.utils.deconstruct import deconstructible
from django.db import models
from django.conf import settings
from django.db.models import NOT_PROVIDED
from django.db.migrations.serializer import BaseSerializer
from django.db.migrations.writer import MigrationWriter


from lino.utils import is_string
from lino.core import actions
from lino.core import actors
from lino.core import tables
from lino.core import fields
from .exceptions import UnresolvedChoice
from .signals import receiver, pre_analyze


STRICT = True
VALUE_FIELD = models.CharField(_("value"), max_length=20)
VALUE_FIELD.attname = 'value'

@deconstructible
class Choice(fields.TableRow):
    """A constant value whose unicode representation depends on the
    current language at runtime.  Every item of a :class:`ChoiceList`
    must be an instance of :class:`Choice` or a subclass thereof.

    .. attribute:: choicelist

        The choice list that owns this choice.

    .. attribute:: value

        (a string) The value to use e.g. when this choice is being stored in a
        database.

    .. attribute:: text

        A translatable string containing the text to show to the user.

    .. attribute:: names

        A list of names to be used as attribute name on the choicelist for referring
        to this choice from application code.

        If this is `None` or not specified, the choice is a nameless
        choice, which is a full-fledged choice object but is not
        accessible as a class attribute on its choicelist.

    .. attribute:: button_text

        The text to appear on buttons representing this state.

    """
    choicelist = None
    remark = None
    pk = None
    value = None
    text = None
    names = ''
    button_text = None

    def __init__(self, value=None, text=None, names=None, **kwargs):
        """Create a new :class:`Choice` instance.

        Parameters: see :attr:`value`, :attr:`text` and :attr:`name`.
        Any keyword arguments will become attributes on the instance.

        This is also being called from :meth:`Choicelist.add_item`.

        If `names` is given, it should be either an iterable of strings or a
        string of space-separated names.  Each name will be installed as an
        attribute of the choicelist that contains this choice and must be a
        valid Python identifier.  Lino will refuse to add duplicate names.

        """
        if value is not None:
            if not isinstance(value, str):
                raise Exception("value must be a string")
            self.value = self.pk = value
        if names is None:
            names = self.names
        if isinstance(names, str):
            names = tuple(names.split())
        self.names = names

        # if name is not None:
        #     if self.name is None:
        #         self.name = value
        # else:
        #     self.name = name
        if text is None:
            if self.text is None:
                # self.text = self.__class__.__name__
                self.text = self.value
        else:
            # assert_pure(text)
            self.text = text
        for k, v in kwargs.items():
            setattr(self, k, v)


    @property
    def name(self):
       if len(self.names) == 0:
           return None
       # elif len(self.names) == 1:
       else:
           return self.names[0]
       # raise Exception("{} has multiple names".format(self))
       # return ' '.join(self.names[0])

    # def deconstruct(self):
    #     return ('str', self.value, {})
    #     # path = self.choicelist.__module__ + "." + self.choicelist.__name__
    #     # args = (self.value, self.text, self.name)
    #     # kwargs = {}
    #     # return (path, args, kwargs)
    #     # return ('lino.api.rt.resolve', (str(self.choicelist), self.value), {})

    def update(self, **kwargs):
        for k, v in kwargs.items():
            if not hasattr(self, k):
                raise Exception("%s has no attribute `%s`" % (self, k))
            setattr(self, k, v)

    def attach(i, cls):
        i.choicelist = cls
        if i.value is None:
            i.pk = i.value = str(len(cls.choices)+1)
        elif len(i.value) > cls.max_length:
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

        dt = cls.display_text(i)
        cls.choices.append((i, dt))
        # cls.preferred_width = max(cls.preferred_width, len(unicode(dt)))
        cls.items_dict[i.value] = i
        #~ cls.items_dict[i] = i

    def remove(self):
        """Remove this choice from its list.

        Usage example see
        """
        self.choicelist.remove_item(self)

    def __len__(self):
        # if self.value is None:
        #     return 1
        return len(self.value)

    def __cmp__(self, other):
        if other.__class__ is self.__class__:
            return cmp(self.value, other.value)
        return cmp(self.value, other)

    def __eq__(self, other):
        # if self.value is None:
        #     return super(Choice, self).__eq__(other)
        if other.__class__ is self.__class__:
            return (self.value == other.value)
        return self.value == other

    def __ne__(self, other):
        # if self.value is None:
        #     return super(Choice, self).__neq__(other)
        if other.__class__ is self.__class__:
            return (self.value != other.value)
        return (self.value != other)

    def __lt__(self, other):
        # if self.value is None:
        #     return super(Choice, self).__lt__(other)
        if other.__class__ is self.__class__:
            return (self.value < other.value)
        return (self.value < other)

    def __le__(self, other):
        # if self.value is None:
        #     return super(Choice, self).__le__(other)
        if other.__class__ is self.__class__:
            return (self.value <= other.value)
        return (self.value <= other)

    def __gt__(self, other):
        # if self.value is None:
        #     return super(Choice, self).__gt__(other)
        if other.__class__ is self.__class__:
            return (self.value > other.value)
        return (self.value > other)

    def __ge__(self, other):
        # if self.value is None:
        #     return super(Choice, self).__ge__(other)
        if other.__class__ is self.__class__:
            return (self.value >= other.value)
        return (self.value >= other)

    __hash__ = object.__hash__
    #~ 20120620: removed to see where it was used
    #~ def __getattr__(self,name):
        #~ return curry(getattr(self.choicelist, name),self)

    def __repr__(self):
        # when there several names, we use the first one
        if len(self.names) > 0:
            return "<%s.%s:%s>" % (
                self.choicelist, self.names[0], self.value)
        else:
            return "<%s:%s>" % (self.choicelist, self.value)

    # def __str__(self):
    #     if self.name:
    #         return str(self.name)
    #     return str(self.text)

    def __str__(self):
        # return force_str(self.text, errors="replace")
        # return self.text
        if self.choicelist.show_values:
            return "{0} ({1})".format(self.value, self.text)
        return str(self.text)

    @classmethod
    def get_chooser_for_field(cls, fieldname):
        return None

    def get_typed_instance(self, model):
        """
        Used when implementing :ref:`polymorphism`.
        """
        return self

    def obj2href(self, ar):
        # needed by `detail_pointer`
        return str(self)


class UnresolvedValue(Choice):
    def __init__(self, choicelist, value):
        self.choicelist = choicelist
        self.value = value
        self.text = "Unresolved value %r for %s" % (
            value, choicelist.__name__)
        self.names = {}


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
        classDict.setdefault('max_length', 10)
        cls = actors.ActorMetaClass.__new__(meta, classname, bases, classDict)

        cls.items_dict = {}
        cls.clear()
        cls._fields = []
        # cls._lazy_items = []
        return cls


#~ choicelist_column_fields = dict()
#~ choicelist_column_fields['value'] = fields.VirtualField(models.CharField())
#~ choicelist_column_fields['text'] = fields.VirtualField(models.CharField())
#~ choicelist_column_fields['name'] = fields.VirtualField(models.CharField())

class CallableChoice(object):
    def __repr__(self):
        return "{}.as_callable('{}')".format(repr(self.ChoiceList), self.name)
    # def __eq__(self, other):
    #     return self.ChoiceList == other.ChoiceList and self.name == other.name
    def __init__(self, ChoiceList, name):
        self.ChoiceList = ChoiceList
        self.name = name
    def __call__(self, *args, **kwargs):
        return self.ChoiceList.get_by_name(self.name)
        # return self.callfn(*args, **kwargs)

class ChoiceList(with_metaclass(ChoiceListMeta, tables.AbstractTable)):

    """
    User-defined choice lists must inherit from this base class.

    .. attribute:: max_length

        The default `max_length` for fields using this choicelist.

    """
    abstract = True
    workflow_actions = []

    item_class = Choice
    """
    The class of items of this list.
    """

    auto_fit_column_widths = True

    default_value = None
    """A string with the name of a choice to be used as default value for
    fields using this list.

    Note that this specifies the *default* default value for *all*
    :class:`ChoiceListField <lino.core.choicelists.ChoiceListField>`
    of this choicelist, including parameter fields.

    You can remove that "default default value" for all tables by
    specifying `default=''`. There are two places where you can
    specify this: (a) on the parameter field itself (which then
    applies to all subtables) or (b) just on one table. For example
    (excerpt from :mod:`lino_avanti.lib.avanti`)::

        from lino_xl.lib.clients.choicelists import ClientStates
        ClientStates.default_value = 'coached'

        parameters = ObservedDateRange(
            ...
            client_state=ClientStates.field(blank=True, default=''))

    Note that the default values of parameter fields of a table which
    is used as the *models default table* will apply for the choices
    of pointers to that model. Concrete use case is the choicelist of
    `cal.Guest.partner` in :ref:`avanti` which should show only
    coached clients.  So instead of above code we actually now do::

        class MyClients(My, Clients):
            @classmethod
            def param_defaults(self, ar, **kw):
                kw = super(MyClients, self).param_defaults(ar, **kw)
                kw.update(client_state='')
                return kw



    The disadvantage
    is that when somebody *does not* want your default value, then
    they must explicitly specify `default=''` when defining a field on
    your choicelist.

    """

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

    removed_names = frozenset()

    @classmethod
    def get_default_action(cls):
        return actions.ShowTable()

    hidden_columns = frozenset(['workflow_buttons'])

    column_names = 'value name text *'

    button_text = models.CharField(_("Button text"), blank=True)

    old2new = {}
    """
    A dict which maps old values to their new values.

    This dict is consulted when an unknown value is read from database
    (e.g. during a migration).  If if contains a replacement for the
    old value, Lino will return the choice with the new value.
    """

    @classmethod
    def get_column_names(self, ar):
        return self.column_names

    @classmethod
    def get_data_elem(self, name):
        de = super(ChoiceList, self).get_data_elem(name)
        if de:
            return de
        return getattr(self, name, None)
        #~ return _choicelist_column_fields.get(name)

    @fields.virtualfield(VALUE_FIELD)
    def value(cls, choice, ar):
        return choice.value

    @fields.virtualfield(models.CharField(_("text"), max_length=50))
    def text(cls, choice, ar):
        return choice.text

    @fields.virtualfield(models.CharField(_("name"), max_length=20))
    def name(cls, choice, ar):
        return ' '.join(choice.names)

    @fields.displayfield(_("Remark"))
    def remark(cls, choice, ar):
        return choice.remark

    @fields.displayfield(_("Type"))
    def type(cls, choice, ar):
        return choice.__class__.__name__

    # @fields.displayfield(_("Description"))
    # def description(cls, choice, ar):
    #     return choice.help_text

    @classmethod
    def get_data_rows(self, ar=None):
        """

        """
        # return sorted(self.items())
        return self.get_list_items()

    @classmethod
    def get_actor_label(self):
        """
        Compute the label of this actor.
        Called only if `label` is not set, and only once during site startup.
        """
        return self._label or self.verbose_name_plural or self.__name__

    @classmethod
    def clear(cls):
        """Clear the list, i.e. remove all items.

        This is used when you want to restart from scratch for building a
        choicelist.

        """
        # remove previously defined named choices from class dict:
        for ci in cls.items_dict.values():
            for name in ci.names:
                delattr(cls, name)
                # if cls.__name__ == "UserTypes":
                #     print("20200504 clear {} {} {}".format(cls, ci.name, ci))
        cls.removed_names = frozenset()
        cls.items_dict = {}
        cls.choices = []  # remove blank_item from choices
        cls.workflow_actions = []

    @classmethod
    def remove_item(cls, i):
        """Remove the specified item from this list. Called by
        :meth:`Choice.remove`.
        """
        del cls.items_dict[i.value]
        for name in i.names:
            cls.removed_names.add(name)
            # print(20161215, cls.removed_names)
            delattr(cls, name)
        for n, el in enumerate(cls.choices):
            if el[0] == i:
                del cls.choices[n]
        for n, a in enumerate(cls.workflow_actions):
            if a.target_state == i:
                del cls.workflow_actions[n]

    # @classmethod  # was not used
    # def setup_field(cls, fld):
    #     pass

    @classmethod
    def sort(cls):
        """
        Sort the items by their value.

        Used for example by :mod:`lino_xl.lib.orders` where we add a journal
        group to :class:`lino_xl.lib.ledger.JournalGroups` and want it to come
        before the other groups.

        """
        cls.choices.sort(key=lambda x: x[0].value)

    @classmethod
    def field(cls, *args, **kw):
        """
        Create and return a database field that points to one value of this
        choicelist.

        The returned field is an instance of :class:`ChoiceListField`.
        Returns a `DummyField` if the plugin which defines this
        choicelist is not installed.
        """
        if settings.SITE.is_installed(cls.app_label):
            fld = ChoiceListField(cls, *args, **kw)
            # cls.setup_field(fld)
            cls._fields.append(fld)
            return fld
        return fields.DummyField()

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
    def add_item_lazy(cls, *args, **kwargs):
        """Run :meth:`add_item` with these arguments when all plugins have
        been loaded.

        This is used e.g. when declaring :mod:`lino_xl.lib.ledger.VoucherTypes`
        : a voucher type is defined using its ByJournal table, but the model of
        that table is not necessarily resolvable at that moment.

        """
        @receiver(pre_analyze, weak=False)
        def func(sender, **ignored):
            cls.add_item(*args, **kwargs)
            # logger.info("20190506 added item %s to %s %s %s", i, cls, args, kwargs)

        # cls._lazy_items.append(func)
        # we must store the func somewhere because receiver only connects it to
        # the signal, which is a weak reference.

    @classmethod
    def add_item(cls, *args, **kwargs):
        """Instantiates a new choice and adds it to this list. Signature is
        that of the :meth:`Choice.__init__` method (which might have
        been overridden if you defined a customized
        :attr:`item_class`.

        """
        return cls.add_item_instance(cls.item_class(*args, **kwargs))

    @classmethod
    def class_init(cls):
        super(ChoiceList, cls).class_init()
        if cls.abstract:
            return
        if cls.preferred_width is None:
            pw = 4
            for i in cls.get_list_items():
                dt = cls.display_text(i)
                pw = max(pw, len(dt))
            cls.preferred_width = pw
            # print("20200122b setting preferred_width for {} to {}".format(cls, cls.preferred_width))

    @classmethod
    def add_item_instance(cls, i):
        #~ if cls is ChoiceList:
            #~ raise Exception("Cannot define items on the base class")
        is_duplicate = False
        if i.value is not None and i.value in cls.items_dict:
            raise Exception("Duplicate value %r in %s." % (i.value, cls))
            warnings.warn("Duplicate value %r in %s." % (i.value, cls))
            is_duplicate = True
        for name in i.names:
            if not is_duplicate:
                if name in cls.__dict__:
                    raise Exception(
                        "An attribute named %r is already defined in %s" % (
                            name, cls.__name__))
            # if cls.__name__ == "UserTypes":
            #     print("20200504 add {} {} {}".format(cls, i.name, i))
            setattr(cls, name, i)
            #~ i.name = name
        i.attach(cls)
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
        nv = cls.old2new.get(value)
        if nv is not None:
            value = nv
        v = cls.items_dict.get(value) or cls.get_by_name(value, None)
        if v is not None:
            return v
        if settings.SITE.strict_choicelist_values:
            raise UnresolvedChoice(
                "Unresolved value %r (%s) for %s (set "
                "Site.strict_choicelist_values to False "
                "to ignore this)" % (
                    value, value.__class__, cls))
        return UnresolvedValue(cls, value)

    @classmethod
    def get_choices(cls):
        return cls.choices

    #~ @classmethod
    #~ def get_choices(cls):
        #~ """
        #~ We must make it dynamic since e.g. UserTypes can change after
        #~ the fields have been created.

        #~ https://docs.djangoproject.com/en/3.1/ref/models/fields/
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
        :class:`lino.modlib.users.UserGroups` and
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
            return lazy(fn, str, str)(bc)
        return lazy(str, str, str)(bc)

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
    def get_by_value(cls, value, *args):
        """
        Return the item (a :class:`Choice` instance) corresponding to the
        specified `value`.
        """
        if not isinstance(value, str):
            raise Exception("%r is not a string" % value)
        #~ print "get_text_for_value"
        #~ return self.items_dict.get(value, None)
        #~ return self.items_dict.get(value)
        return cls.items_dict.get(value, *args)

    @classmethod
    def as_callable(self, name):
        """
        Use this when you want to specify some named default choice of this
        list as a default value *without* removing the possibility to
        clear and re-populate the list after the field definition.

        Usage example::

            foo_state = MyStates.as_callable('foo')

        This is used internally when you specify a string as default value of a
        choicelist field.

        """
        return CallableChoice(self, name)

    @classmethod
    def get_default_value(self):
        """Return the *default* default value for fields using this
        choicelist.

        """
        return self.get_by_name(self.default_value)

    #~ @classmethod
    #~ def items(self):
        #~ return [choice[0] for choice in self.choices]

    @classmethod
    def find(cls, **fkw):
        """Find and return the choice that satisfies the given search
        criteria.  Return `None` if no choice is found or if more than
        one choice is found.

        """
        lst = cls.filter(**fkw)
        if len(lst) == 1:
            return lst[0]
        return None

    @classmethod
    def filter(self, **fkw):
        def f(item):
            for k, v in list(fkw.items()):
                if getattr(item, k) != v:
                    return False
            return True
        return [choice[0] for choice in self.choices if f(choice[0])]

    # @classmethod
    # def filter_choice(self, **fkw):
    #     """
    #     Apply the fkw filter and return the list of filtered choices.
    #     :param fkw:
    #     :return:
    #     """
    #     def f(item):
    #         for k, v in list(fkw.items()):
    #             if getattr(item, k) != v:
    #                 return False
    #         return True
    #
    #     return [choice for choice in self.choices if f(choice[0])]

    @classmethod
    def get_list_items(self):
        return [choice[0] for choice in self.choices]
    objects = get_list_items  # deprecated alias for backwards compat
    items = get_list_items   # deprecated alias for backwards compat

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

      for u in users.User.objects.filter(user_type__isnull=False):

    You must either check for an empty string::

      for u in users.User.objects.exclude(user_type='')

    or use the ``__gte`` operator::

      for u in users.User.objects.filter(user_type__gte=dd.UserLevels.guest):

    """

    empty_strings_allowed = False

    def __init__(self, choicelist=None, verbose_name=None,
                 force_selection=True, default=None, **kw):
        if verbose_name is None:
            verbose_name = choicelist.verbose_name
        self.choicelist = choicelist
        self.force_selection = force_selection
        if default is not None:
            if is_string(default):
                default = choicelist.as_callable(default)
            kw.update(default=default)
        defaults = dict(
            max_length=choicelist.max_length)
        # if choicelist.default_value:
        #     defaults.update(
        #         default=choicelist.as_callable(choicelist.default_value))
        if choicelist.default_value:
            defaults.update(default=choicelist.get_default_value)
        # if not 'help_text' in kw:
        #     # inherited docstrings won't be helpful here.
        #     doc = choicelist.__dict__['__doc__']
        #     if doc:
        #         kw['help_text'] = choicelist.__doc__.split('\n\n')[0]
        defaults.update(kw)
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
        """
        Needed for Django 1.7+, see
        https://docs.djangoproject.com/en/3.1/howto/custom-model-fields/#custom-field-deconstruct-method
        """

        name, path, args, kwargs = super(ChoiceListField, self).deconstruct()
        # args = [self.choicelist]

        kwargs['choicelist'] = self.choicelist
        # kwargs.pop('default', None)
        # TODO: above line is cheating in order to get makemigrations
        # to pass. we remove the `default` attribute because it is not
        # serializable. This means that our migrations are probably
        # invalid and not usable.

        return name, path, args, kwargs

    def get_internal_type(self):
        return "CharField"

    #~ def set_max_length(self,ml):
        #~ self.max_length = ml

    def from_db_value(self, value, expression, connection, context=None):
        if value is None:
            return None
        return self.choicelist.to_python(value)

    def to_python(self, value):
        """See Django's docs about `to_python()
        <https://docs.djangoproject.com/en/1.11/ref/models/fields/#django.db.models.Field.to_python>`__.

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
        """
        Excerpt from `Django docs
        <https://docs.djangoproject.com/en/3.0/howto/custom-model-fields/#converting-python-objects-to-query-values>`__:
        "If you override `to_python()
        <https://docs.djangoproject.com/en/3.0/ref/models/fields/#django.db.models.Field.to_python>`__
        you also have to override `get_prep_value()
        <https://docs.djangoproject.com/en/3.0/ref/models/fields/#django.db.models.Field.get_prep_value>`__
        to convert Python objects back to query values."
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
        value = self.value_from_object(obj)
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

    def from_db_value(self, value, expression, connection, context=None):
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



# from lino.core.choicelists import Choice, ChoiceList, CallableChoice


class ChoiceSerializer(BaseSerializer):
    def serialize(self):
        return ("rt.models.{}.{}.get_by_value('{}')".format(
            self.value.choicelist.app_label, self.value.choicelist.__name__,
                self.value.value),
            {'from lino.api.shell import rt'})

MigrationWriter.register_serializer(Choice, ChoiceSerializer)

class ChoiceListSerializer(BaseSerializer):
    def serialize(self):
        return ("rt.models.{}.{}".format(
            self.value.choicelist.app_label, self.value.choicelist.__name__),
            {'from lino.api.shell import rt'})
MigrationWriter.register_serializer(ChoiceList, ChoiceListSerializer)


class CallableChoiceSerializer(BaseSerializer):
    def serialize(self):
        choice = self.value()
        return ("rt.models.{}.{}.as_callable('{}')".format(
            choice.choicelist.app_label, choice.choicelist.__name__, choice.name),
            {'from lino.api.shell import rt'})

MigrationWriter.register_serializer(CallableChoice, CallableChoiceSerializer)
