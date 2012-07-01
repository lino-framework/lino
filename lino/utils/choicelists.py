# -*- coding: UTF-8 -*-
## Copyright 2008-2012 Luc Saffre
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

u"""
Utility for defining hard-coded multi-lingual choice lists 
whose value is rendered according to the current language.

:class:`Gender`, :class:`DoYouLike` and :class:`HowWell` 
are "batteries included" usage examples.

Usage:

(Doctesting this module requires the Django translation machine, 
so we must set :setting:`DJANGO_SETTINGS_MODULE`)

>>> import os
>>> os.environ['DJANGO_SETTINGS_MODULE'] = 'lino.apps.std.settings'


>>> from django.utils import translation
>>> translation.activate('en')
>>> for value,text in choicelist_choices():
...     print "%s : %s" % (value, unicode(text))
DoYouLike : certainly not...very much
Gender : Gender
HowWell : not at all...very well

>>> for bc,text in Gender.get_choices():
...     print "%s : %s" % (bc.value, unicode(text))
M : Male
F : Female

>>> print unicode(Gender.male)
Male

>>> translation.activate('de')
>>> print unicode(Gender.male)
Männlich

Comparing Choices uses their *value* (not the alias or text):

>>> from lino.utils.perms import UserLevels

>>> UserLevels.manager > UserLevels.user
True
>>> UserLevels.manager == '40'
True
>>> UserLevels.manager == 'manager'
False
>>> UserLevels.manager == ''
False



Example on how to use a ChoiceList in your model::

  from django.db.models import Model
  from lino.utils.choicelists import HowWell
  
  class KnownLanguage(Model):
      spoken = HowWell.field(verbose_name=_("spoken"))
      written = HowWell.field(verbose_name=_("written"))

Every user-defined subclass of ChoiceList is also 
automatically available as a property value in 
:mod:`lino.modlib.properties`.


"""

from django.utils.translation import ugettext_lazy as _
from django.utils.translation import string_concat
from django.utils.functional import lazy
from django.db import models

from lino.utils import curry




class Choice(object):
    """
    A constant (hard-coded) value whose unicode representation 
    depends on the current babel language at runtime.
    Used by :class:`lino.utils.choicelists`.

    """
    #~ def __init__(self,choicelist,value,text):
        #~ self.choicelist = choicelist
        #~ self.value = value
        #~ self.text = text
        
    def __len__(self):
        return len(self.value)
        
    def __cmp__(self,other):
        if other.__class__ is self.__class__:
            return cmp(self.value,other.value)
        return cmp(self.value,other)
        
    #~ 20120620: removed to see where it was used
    #~ def __getattr__(self,name):
        #~ return curry(getattr(self.choicelist,name),self)
        
    def __repr__(self):
        return str(self)
        
    def __str__(self):
        #~ return "%s (%s:%s)" % (self.texts[babel.DEFAULT_LANGUAGE],
          #~ self.__class__.__name__,self.value)
        name = getattr(self,'name',None)
        if name is None:
            return "%s (%s:%s)" % (unicode(self.text),
                self.choicelist.__name__,self.value)
        return "%s (%s.%s:%s)" % (unicode(self.text),
            self.choicelist.__name__,name,self.value)
        
    def __unicode__(self):
        return unicode(self.text)
                
    def __call__(self):
        # make it callable so it can be used as `default` of a field.
        # see blog/2012/0527
        return self

#~ class UnresolvedValue(Choice):
    #~ def __init__(self,choicelist,value):
        #~ self.choicelist = choicelist
        #~ self.value = value
        #~ self.text = "Unresolved value %r for %s" % (value,choicelist.__name__)
        #~ self.name = ''
        


CHOICELISTS = {}

def register_choicelist(cl):
    k = cl.stored_name or cl.__name__
    if CHOICELISTS.has_key(k):
        raise Exception("ChoiceList name '%s' already defined by %s" % 
            (k,CHOICELISTS[k]))
    CHOICELISTS[k] = cl
    
def get_choicelist(i):
    return CHOICELISTS[i]

def choicelist_choices():
    l = [ (k,v.label or v.__name__) for k,v in CHOICELISTS.items()]
    l.sort(lambda a,b : cmp(a[0],b[0]))
    return l
      
    
class ChoiceListMeta(type):
    def __new__(meta, classname, bases, classDict):
        #~ if not classDict.has_key('app_label'):
            #~ classDict['app_label'] = cls.__module__.split('.')[-2]
        """
        UserGroups manually sets max_length because the 
        default list has only one group with value "system", 
        but applications may want to add longer group names
        """
        classDict.setdefault('max_length',1)
        cls = type.__new__(meta, classname, bases, classDict)
        
        cls.items_dict = {}
        cls.clear()
        cls._fields = []
        #~ cls.max_length = 1
        #~ assert not hasattr(cls,'items') 20120620
        #~ for i in cls.items:
            #~ cls.add_item(i)
        if classname not in ('ChoiceList',):
            register_choicelist(cls)
        return cls
  

class ChoiceList(object):
    """
    Used-defined choice lists must inherit from this base class.
    """
    __metaclass__ = ChoiceListMeta
    
    item_class = Choice
    """
    The class of items of this list.
    """
    
    stored_name = None
    """
    Every subclass of ChoiceList will be automatically registered.
    Define this if your class's name clashes with the name of an 
    existing ChoiceList.
    """
    
    label = None
    "The label or title for this list"
    
    show_values = False
    """
    Set this to True if the user interface should include the `value`
    attribute of each choice.
    """
    
    
    preferred_width = 5
    """
    Preferred width (in characters) used by 
    :class:`fields <lino.core.fields.ChoiceListField>` 
    that refer to this list.
    This is automatically set to length of the longest choice 
    text (using the :attr:`default site language <lino.Lino.languages>`). 
    
    Currently you cannot manually force it to a lower 
    value than that. And it might guess wrong if the user language 
    is not the default site language.
    """
    
    def __init__(self,*args,**kw):
        raise Exception("ChoiceList may not be instantiated")
        
    @classmethod
    def clear(cls):
        """
        """
        for ci in cls.items_dict.values():
            if ci.name is not None:
                delattr(cls,ci.name)
                
        cls.choices = []
        
        blank = cls.item_class()
        blank.choicelist = cls
        blank.value = ''
        blank.text = ''
        blank.name = 'blank_item'
        cls.blank_item = blank
        
        #~ cls.max_length = 1
        cls.items_dict = {'' : cls.blank_item }
        #~ cls.items = []
        
    @classmethod
    def field(cls,*args,**kw):
        """
        Create a database field (a :class:`ChoiceListField`)
        that holds one value of this choicelist. 
        """
        fld = ChoiceListField(cls,*args,**kw)
        cls._fields.append(fld)
        return fld
        
    @classmethod
    def multifield(cls,*args,**kw):
        """
        Not yet imlpemented.
        Create a database field (a :class:`ChoiceListField`)
        that holds a set of multiple values of this choicelist. 
        """
        fld = MultiChoiceListField(cls,*args,**kw)
        cls._fields.append(fld)
        return fld
        
    @classmethod
    #~ def add_item(cls,value,text,alias=None):
    def add_item(cls,value,text,name=None,*args,**kw):
        if cls is ChoiceList:
            raise Exception("Cannot define items on the base class")
        if cls.items_dict.has_key(value):
            raise Exception("Duplicate value %r in choicelist %s.",(value,cls.label))
        i = cls.item_class(*args,**kw)
        # these attributes are always set:
        i.choicelist = cls
        i.value = value
        i.text = text
        
        dt = cls.display_text(i)
        cls.choices.append((i,dt))
        cls.preferred_width = max(cls.preferred_width,len(unicode(dt)))
        cls.items_dict[value] = i
        #~ cls.items_dict[i] = i
        if len(value) > cls.max_length:
            if len(cls._fields) > 0:
                raise Exception(
                    "%s cannot add value %r because fields exist and max_length is %d."
                    % (cls,value,cls.max_length)+"""\
When fields have been created, we cannot simply change their max_length because 
Django creates copies of them when inheriting models.
""")
            cls.max_length = len(value)
            #~ for fld in cls._fields:
                #~ fld.set_max_length(cls.max_length)
        if name:
            if hasattr(cls,name):
                raise Exception("Item %r already defined in %s" % (
                    name,cls.__name__))
            setattr(cls,name,i)
            i.name = name
        return i
        
    @classmethod
    def to_python(cls, value):
        #~ if isinstance(value, babel.BabelChoice):
            #~ return value        
        v = cls.items_dict.get(value) 
        if v is None:
            raise Exception("Unresolved value %r for %s" % (value,cls))
            #~ return UnresolvedValue(cls,value)
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
        """
        make it dynamic
        
        https://docs.djangoproject.com/en/dev/ref/models/fields/
        note that choices can be any iterable object -- not necessarily 
        a list or tuple. This lets you construct choices dynamically. 
        But if you find yourself hacking choices to be dynamic, you're 
        probably better off using a proper database table with a 
        ForeignKey. choices is meant for static data that doesn't 
        change much, if ever.        
        """
        for c in cls.choices:
            yield c
        #~ return cls.choices
      
    @classmethod
    def display_text(cls,bc):
        """
        Override this to customize the display text of choices.
        :class:`lino.utils.perms.UserGroups` and :class:`lino.modlib.cv.models.CefLevel`
        used to do this before we had the 
        :attr:`ChoiceList.show_values` option.
        """
        if cls.show_values:
            def fn(bc):
                return u"%s (%s)" % (bc.value,unicode(bc))
            return lazy(fn,unicode)(bc)
        return lazy(unicode,unicode)(bc)
        #~ return bc
        #~ return unicode(bc)
        #~ return _(bc)
        
    @classmethod
    def get_by_name(self,name):
        if name:
            return getattr(self,name,None)
        else:
            return self.blank_item
            
    @classmethod
    def get_by_value(self,value):
        """
        Return the item (a :class:`Choice` instance) 
        corresponding to the specified `value`.
        """
        if not isinstance(value,basestring):
            raise Exception("%r is not a string" % value)
        #~ print "get_text_for_value"
        #~ return self.items_dict.get(value,None)
        #~ return self.items_dict.get(value)
        return self.items_dict[value]
      
    @classmethod
    def items(self):
        #~ return self.items_dict.values()
        return [choice[0] for choice in self.choices]
        
    @classmethod
    def get_text_for_value(self,value):
        """
        Return the text corresponding to the specified value.
        """
        bc = self.get_by_value(value)
        if bc is None:
            return _("%(value)r (invalid choice for %(list)s)") % dict(
                list=self.__name__,value=value)
        return self.display_text(bc)
    #~ def __unicode__(self):
        #~ return unicode(self.stored_name) # babel_get(self.names)



        
    
class ChoiceListField(models.CharField):
    """
    A field that stores a value to be selected from a 
    :class:`lino.utils.choicelists.ChoiceList`.
    """
    
    __metaclass__ = models.SubfieldBase
    
    #~ force_selection = True
    
    #~ choicelist = NotImplementedError
    
    def __init__(self,choicelist,verbose_name=None,force_selection=True,**kw):
        if verbose_name is None:
            verbose_name = choicelist.label
        self.choicelist = choicelist
        self.force_selection = force_selection
        defaults = dict(
            #~ choices=KNOWLEDGE_CHOICES,
            choices=choicelist.get_choices(),
            max_length=choicelist.max_length,
            blank=True,  # null=True,
            #~ validators=[validate_knowledge],
            #~ limit_to_choices=True,
            )
        defaults.update(kw)
        kw.update(kw)
        #~ models.SmallIntegerField.__init__(self,*args, **defaults)
        models.CharField.__init__(self,verbose_name, **defaults)
        
    def get_internal_type(self):
        return "CharField"
        
    #~ def set_max_length(self,ml):
        #~ self.max_length = ml
        
    def to_python(self, value):
        #~ if self.attname == 'query_register':
            #~ print '20120527 to_python', repr(value), '\n'
        if isinstance(value,Choice):
            return value
        return self.choicelist.to_python(value)
        #~ value = self.choicelist.to_python(value)
        #~ if value is None: # see 20110907
            #~ value = ''
        #~ return value
        
    def get_prep_value(self, value):
        #~ if self.attname == 'query_register':
            #~ print '20120527 get_prep_value()', repr(value)
        return value.value
        #~ if value:
            #~ return value.value
        #~ return '' # see 20110907
        #~ return None
        
    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        #~ if self.attname == 'query_register':
            #~ print '20120527 value_to_string', repr(value)
        return self.get_prep_value(value)
        #~ return self.get_db_prep_value(value,connection)
        
    #~ def save_form_data(self, instance, data):
        #~ setattr(instance, self.name, data)
        
    def get_text_for_value(self,value):
        return self.choicelist.get_text_for_value(value.value)
    
      
class MultiChoiceListField(ChoiceListField):
    """
    A field whose value is a `list` of `Choice` instances.
    Stored in the database as a CharField using a delimiter character.
    """
    __metaclass__ = models.SubfieldBase
    delimiter_char = ','
    max_values = 1
    
    def __init__(self,choicelist,verbose_name=None,max_values=10,**kw):
        if verbose_name is None:
            verbose_name = choicelist.label_plural
        self.max_values = max_values
        defaults = dict(
            max_length=(choicelist.max_length+1) * max_values
            )
        defaults.update(kw)
        ChoiceListField.__init__(self,verbose_name, **defaults)
    
    #~ def set_max_length(self,ml):
        #~ self.max_length = (ml+1) * self.max_values
        
    def to_python(self, value):
        if value is None: 
            return []
        if isinstance(value,list):
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
        
    def get_text_for_value(self,value):
        return ', '.join([self.choicelist.get_text_for_value(bc.value) for bc in value])






class DoYouLike(ChoiceList):
    """
    A list of possible answers to questions of type "How much do you like ...?".
    """
    label = _("certainly not...very much")
    
add = DoYouLike.add_item
add('0',_("certainly not"))
add('1',_("rather not"))
add('2',_("normally"),"default")
add('3',_("quite much"))
add('4',_("very much"))

class HowWell(ChoiceList):
    """
    A list of possible answers to questions of type "How well ...?":
    "not at all", "a bit", "moderate", "quite well" and "very well" 
    
    which are stored in the database as '0' to '4',
    and whose `__unicode__()` returns their translated text.

    `lino.apps.pcsw.models.Languageknowledge.spoken` 
    `lino.apps.pcsw.models.Languageknowledge.written` 
    """
    label = _("not at all...very well")
    
add = HowWell.add_item
add('0',_("not at all"))
add('1',_("a bit"))
add('2',_("moderate"),"default")
add('3',_("quite well"))
add('4',_("very well"))


class Gender(ChoiceList):
    """
    Defines choices for the "Gender" of a person.

    """
    label = _("Gender")
add = Gender.add_item
add('M',_("Male"),'male')
add('F',_("Female"),'female')




def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()

