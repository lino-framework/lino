# -*- coding: UTF-8 -*-
# Copyright 2008-2014 Luc Saffre
# License: BSD (see file COPYING for details)

ur"""
Utility for defining hard-coded internationalized choice lists
whose value is rendered according to the current language.

Usage:


>>> import os
>>> os.environ['DJANGO_SETTINGS_MODULE'] = 'lino.projects.docs.settings.demo'
>>> from lino.runtime import *
>>> from django.utils import translation

>>> for value,text in choicelist_choices():
...     print "%s : %s" % (value, unicode(text))
cal.AccessClasses : AccessClasses
cal.DurationUnits : DurationUnits
cal.Weekdays : Weekdays
lino.Genders : Genders
users.UserGroups : User Groups
users.UserLevels : User Levels
users.UserProfiles : User Profiles

>>> Genders = dd.Genders
>>> for bc,text in Genders.choices:
...     print "%s : %s" % (bc.value, unicode(text))
M : Male
F : Female

>>> print unicode(Genders.male)
Male

>>> with translation.override('de'):
...    print unicode(Genders.male)
Männlich

>>> print str(Genders.male)
male

>>> print repr(Genders.male)
Genders.male:M

Comparing Choices uses their *value* (not the alias or text):

>>> UserLevels = dd.UserLevels

>>> UserLevels.manager > UserLevels.user
True
>>> UserLevels.manager == '40'
True
>>> UserLevels.manager == 'manager'
False
>>> UserLevels.manager == ''
False


Defining your own ChoiceLists
-----------------------------

>>> class MyColors(Choicelist):
...     verbose_name_plural = "My colors"
>>> MyColors.add_item('01',("Red"),'red')
>>> MyColors.add_item('02',("Green"),'green')

`add_item` takes at least 2 and optionally a third positional argument:

- The `value` is used to store this Choice in the database and for
  sorting the choices.
- The `text` is what the user sees. It should be translatable.
- The optional `name` is used to install this choice as a class
  attribute on the ChoiceList.

  
The `value` must be a string.
  
>>> MyColors.add_item(1,("Green"), 'green')
>>> MyColors.add_item(1,("Green"), 'verbose_name_plural')
  

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

import logging
logger = logging.getLogger(__name__)

import warnings

from django.utils.translation import ugettext_lazy as _
from django.utils.functional import lazy
from django.db import models

from lino.utils import unicode_string

from lino.core import actions
from lino.core import actors
from lino.core import tables
from lino.core import fields


STRICT = True


class Choice(object):

    """
    A constant (hard-coded) value whose unicode representation
    depends on the current babel language at runtime.
    Used by :class:`ChoiceList`.

    """
    choicelist = None
    remark = None

    def __init__(self, value, text=None, name=None, **kw):
        #~ self.choicelist = choicelist
        if not isinstance(value, basestring):
            raise Exception("value must be a string")
        self.value = value
        self.name = name or value
        self.text = text or self.__class__.__name__
        for k, v in kw.items():
            setattr(self, k, v)

    def update(self, **kw):
        for k, v in kw.items():
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
        #~ return curry(getattr(self.choicelist,name),self)

    def __repr__(self):
        if self.name is None:
            return "<%s:%s>" % (self.choicelist.__name__, self.value)
            #~ s = "%s:%s" % (self.choicelist.__name__,self.value)
        else:
            return "<%s.%s:%s>" % (self.choicelist.__name__, self.name, self.value)
            #~ s = "%s.%s:%s" % (self.choicelist.__name__,self.name,self.value)
        #~ return "<%s(%s)>" % (self.__class__.__name__,s)

    def __str__(self):
        if self.name:
            return self.name
        return unicode_string(self.text)
        #~ return unicode(self.text).encode(sys.getdefaultencoding(),'backslashreplace')

    def __unicode__(self):
        return unicode(self.text)

    def __call__(self):
        # make it callable so it can be used as `default` of a field.
        # see blog/2012/0527
        return self

    @classmethod
    def get_chooser_for_field(cls, fieldname):
        return None


class UnresolvedValue(Choice):
    def __init__(self, choicelist, value):
        self.choicelist = choicelist
        self.value = value
        self.text = "Unresolved value %r for %s" % (value, choicelist.__name__)
        self.name = ''


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
    #~ print '20121209 choicelist_choices()', CHOICELISTS
    l = [(k, v.verbose_name_plural or v.__name__)
         for k, v in CHOICELISTS.items()]
    #~ l = [ (k,v.label or v.__name__) for k,v in CHOICELISTS.items()]
    l.sort(lambda a, b: cmp(a[0], b[0]))
    return l


class ChoiceListMeta(actors.ActorMetaClass):

    def __new__(meta, classname, bases, classDict):
        #~ if not classDict.has_key('app_label'):
            #~ classDict['app_label'] = cls.__module__.split('.')[-2]
        """
        UserGroups manually sets max_length because the
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


#~ class ChoiceList(object):
#~ class ChoiceList(actors.Actor):
class ChoiceList(tables.AbstractTable):

    """
    User-defined choice lists must inherit from this base class.
    """
    __metaclass__ = ChoiceListMeta

    #~ _handle_class = tables.TableHandle

    item_class = Choice
    """
    The class of items of this list.
    """

    auto_fit_column_widths = True

    #~ blank = True
    #~ """
    #~ Set this to False if you don't want to accept
    #~ any blank value for your ChoiceList.
    #~ """

    preferred_foreignkey_width = 20
    """
    Default preferred with for ChoiceList fields to this list.
    """

    stored_name = None
    """
    Every subclass of ChoiceList will be automatically registered.
    Define this if your class's name clashes with the name of an 
    existing ChoiceList.
    """

    verbose_name = None
    verbose_name_plural = None

    #~ label = None
    #~ "The label or title for this list"

    show_values = False
    """
    Set this to True if the user interface should include the `value`
    attribute of each choice.
    """

    preferred_width = 4
    """Preferred width (in characters) used by :class:`fields
    <lino.core.fields.ChoiceListField>` that refer to this list.

    This is automatically set to length of the longest choice text
    (using the :attr:`default site language <lino.Lino.languages>`).
    It might guess wrong if the user language is not the default site
    language.

    The hard-coded absolute minimum is 4.  Currently you cannot
    manually force it to a lower value than that.

    Note that by this we mean the width of the bare text field,
    excluding any UI-specific control like the trigger button of a
    combobox.  That's why e.g. `lino.ui.extjs3.ext_elems` adds a
    another value for the trigger button.

    """

    @classmethod
    def get_default_action(cls):
        return actions.GridEdit()

    #~ hidden_columns = frozenset()
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

    @fields.virtualfield(models.CharField(_("value"), max_length=20))
    def value(cls, choice, ar):
        return choice.value

    @fields.displayfield(_("Remark"))
    def remark(cls, choice, ar):
        return choice.remark
        #~ txt = unicode(getattr(choice,'remark',''))
        #~ print repr(txt)
        #~ txt = ""
        #~ return txt

    @fields.virtualfield(models.CharField(_("text"), max_length=50))
    def text(cls, choice, ar):
        return choice.text

    @fields.virtualfield(models.CharField(_("name"), max_length=20))
    def name(cls, choice, ar):
        return choice.name

    @classmethod
    def get_data_rows(self, ar=None):
        return self.items()

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
        for ci in cls.items_dict.values():
            if ci.name:
                delattr(cls, ci.name)
        cls.items_dict = {}
        cls.choices = []
        #~ if cls.blank:
            #~ cls.add_item('','',name='blank_item')
        cls.choices = []  # remove blank_item from choices

        #~ cls.items_dict = {'' : cls.blank_item }

        #~ cls.max_length = 1
        #~ cls.items = []

    @classmethod
    def setup_field(cls, fld):
        pass

    @classmethod
    def field(cls, *args, **kw):
        """
        Create a database field (a :class:`ChoiceListField`)
        that holds one value of this choicelist. 
        """
        fld = ChoiceListField(cls, *args, **kw)
        cls.setup_field(fld)
        cls._fields.append(fld)
        return fld

    @classmethod
    def multifield(cls, *args, **kw):
        """
        Not yet imlpemented.
        Create a database field (a :class:`ChoiceListField`)
        that holds a set of multiple values of this choicelist. 
        """
        fld = MultiChoiceListField(cls, *args, **kw)
        cls._fields.append(fld)
        return fld

    @classmethod
    def add_item(cls, value, text, name=None, *args, **kw):
        return cls.add_item_instance(
            cls.item_class(value, text, name, *args, **kw))

    @classmethod
    def add_item_instance(cls, i):
        #~ if cls is ChoiceList:
            #~ raise Exception("Cannot define items on the base class")
        is_duplicate = False
        if cls.items_dict.has_key(i.value):
            #~ raise Exception("Duplicate value %r in %s." % (i.value,cls))
            warnings.warn("Duplicate value %r in %s." % (i.value, cls))
            is_duplicate = True
        i.attach(cls)
        dt = cls.display_text(i)
        cls.choices.append((i, dt))
        cls.preferred_width = max(cls.preferred_width, len(unicode(dt)))
        cls.items_dict[i.value] = i
        #~ cls.items_dict[i] = i
        if len(i.value) > cls.max_length:
            if len(cls._fields) > 0:
                raise Exception(
                    "%s cannot add value %r because fields exist and max_length is %d."
                    % (cls, i.value, cls.max_length) + """\
When fields have been created, we cannot simply change their max_length because 
Django creates copies of them when inheriting models.
""")
            cls.max_length = len(i.value)
            #~ for fld in cls._fields:
                #~ fld.set_max_length(cls.max_length)
        if i.name:
            #~ if hasattr(cls,i.name):
            if not is_duplicate:
                if cls.__dict__.has_key(i.name):
                    raise Exception("An item named %r is already defined in %s" % (
                        i.name, cls.__name__))
            setattr(cls, i.name, i)
            #~ i.name = name
        return i

    @classmethod
    def to_python(cls, value):
        #~ if isinstance(value, babel.BabelChoice):
            #~ return value
        if not value:
            return None
        v = cls.items_dict.get(value)
        if v is None:
            if STRICT:
                raise Exception("Unresolved value %r for %s" % (value, cls))
            else:
                return UnresolvedValue(cls, value)
        return v
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
        """
        Override this to customize the display text of choices.
        :class:`lino.core.perms.UserGroups` and :class:`lino.modlib.cv.models.CefLevel`
        used to do this before we had the 
        :attr:`ChoiceList.show_values` option.
        """
        if cls.show_values:
            def fn(bc):
                return u"%s (%s)" % (bc.value, unicode(bc))
            return lazy(fn, unicode)(bc)
        return lazy(unicode, unicode)(bc)
        #~ return bc
        #~ return unicode(bc)
        #~ return _(bc)

    @classmethod
    def get_by_name(self, name, *args):
        """
        Accepts the case that `name` is `None` (returns None then).
        """
        #~ return getattr(self,name,*args)
        if name:
            return getattr(self, name, *args)
        else:
            return None

    @classmethod
    def get_by_value(self, value, *args):
        """
        Return the item (a :class:`Choice` instance) 
        corresponding to the specified `value`.
        """
        if not isinstance(value, basestring):
            raise Exception("%r is not a string" % value)
        #~ print "get_text_for_value"
        #~ return self.items_dict.get(value,None)
        #~ return self.items_dict.get(value)
        return self.items_dict.get(value, *args)

    #~ @classmethod
    #~ def items(self):
        #~ return [choice[0] for choice in self.choices]

    @classmethod
    def filter(self, **fkw):
        def f(item):
            for k, v in fkw.items():
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
    #~ def __unicode__(self):
        # ~ return unicode(self.stored_name) # babel_get(self.names)


class ChoiceListField(models.CharField):

    """A field that stores a value to be selected from a
    :class:`ChoiceList`.
    
    ChoiceListField cannot be nullable since they are implemented as
    CharFields.  Therefore when filtering on empty values in a
    database query you cannot use ``__isnull``::
    
      for u in users.User.objects.filter(profile__isnull=False):
      
    You must either check for an empty string::
      
      for u in users.User.objects.exclude(profile='')

    or use the ``__gte`` operator::
      
      for u in users.User.objects.filter(profile__gte=dd.UserLevels.guest):

    """

    __metaclass__ = models.SubfieldBase

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

    def deconstruct(self):
        # needed for Django 1.7
        # https://docs.djangoproject.com/en/dev/howto/custom-model-fields/#custom-field-deconstruct-method

        name, path, args, kwargs = super(ChoiceListField, self).deconstruct()
        args = [self.choicelist]
        return name, path, args, kwargs

    def get_internal_type(self):
        return "CharField"

    #~ def set_max_length(self,ml):
        #~ self.max_length = ml

    def to_python(self, value):
        #~ if self.attname == 'query_register':
            #~ print '20120527 to_python', repr(value), '\n'
        if isinstance(value, Choice):
            return value
        return self.choicelist.to_python(value)
        #~ value = self.choicelist.to_python(value)
        # ~ if value is None: # see 20110907
            #~ value = ''
        #~ return value

    def _get_choices(self):
        """
        HACK: Django by default stores a copy of our list 
        when the `choices` of a field are evaluated for the 
        first time. We don't want that because ChoiceLists may 
        change afterwards.
        """
        return self.choicelist.choices
        #~ if hasattr(self._choices, 'next'):
            #~ choices, self._choices = tee(self._choices)
            #~ return choices
        #~ else:
            #~ return self._choices
    choices = property(_get_choices)

    def get_prep_value(self, value):
        #~ if self.attname == 'query_register':
            #~ print '20120527 get_prep_value()', repr(value)
        #~ return value.value
        if value:
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
    __metaclass__ = models.SubfieldBase
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

    def to_python(self, value):
        if value is None:
            return []
        if isinstance(value, list):
            return value

        value = self.choicelist.to_python(value)
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
        return ', '.join([self.choicelist.get_text_for_value(bc.value) for bc in value])



def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()
