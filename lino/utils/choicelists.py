# -*- coding: UTF-8 -*-
## Copyright 2008-2011 Luc Saffre
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

Usage example :

(choicelists requires :setting:`DJANGO_SETTINGS_MODULE` to be set)

>>> import os
>>> os.environ['DJANGO_SETTINGS_MODULE'] = 'lino.apps.std.settings'


>>> from django.utils import translation
>>> from lino.utils.choicelists import Gender
>>> translation.activate('en')
>>> print unicode(Gender.male)
Male
>>> translation.activate('de')
>>> print unicode(Gender.male)
Männlich


:class:`Gender`, 
:class:`DoYouLike` and :class:`HowWell` 
are "batteries included" usage examples.

Example on how to use them in your model::

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
from django.utils.functional import lazy

from lino.utils import curry

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
        cls = type.__new__(meta, classname, bases, classDict)
        cls.choices = []
        cls.max_length = 1
        cls.items_dict = {}
        for i in cls.items:
            cls.add_item(i)
        if classname not in ('ChoiceList',):
            register_choicelist(cls)
        return cls
  

class ChoiceList(object):
    """
    Every subclass of ChoiceList will be automatically registered.
    Define this if your class's name clashes with the name of an exiting ChoiceList.
    """
    __metaclass__ = ChoiceListMeta
    items = []
    stored_name = None
    label = None
    """
    """
    def __init__(self,items=[],max_length=1):
        raise Exception("ChoiceList may not be instantiated")
        
    @classmethod
    def field(cls,*args,**kw):
        from lino.fields import ChoiceListField
        return ChoiceListField(cls,*args,**kw)
        
    @classmethod
    def add_item(cls,value,text,alias=None):
    #~ def add_item(cls,value,ref=None,**kw):
        if cls is ChoiceList:
            raise Exception("Cannot define items on the base class")
        i = BabelChoice(cls,value,text)
        cls.choices.append((i,cls.display_text(i)))
        assert not cls.items_dict.has_key(value)
        cls.items_dict[value] = i
        #~ cls.items_dict[i] = i
        cls.max_length = max(len(value),cls.max_length)
        if alias:
            if hasattr(cls,alias):
                raise Exception("Item %r already defined in %s" % (
                    alias,cls.__name__))
            setattr(cls,alias,i)
        return i
        
    @classmethod
    def to_python(cls, value):
        #~ if isinstance(value, babel.BabelChoice):
            #~ return value        
        return cls.items_dict.get(value)
        
        
    #~ @classmethod
    #~ def get_label(cls):
        #~ if cls.label is None:
            #~ return cls.__name__ 
        #~ return _(cls.label)
        
    @classmethod
    def get_choices(cls):
        return cls.choices
      
    @classmethod
    def display_text(cls,bc):
        """Override this to customize the display text of choices.
        Example: :class:`lino.apps.dsbe.models.CefLevel`
        """
        return lazy(unicode,unicode)(bc)
        #~ return bc
        #~ return unicode(bc)
        #~ return _(bc)
        
    @classmethod
    def get_text_for_value(self,value):
        """
        Return the text corresponding to the specified value.
        """
        if not isinstance(value,basestring):
            raise Exception("%r is not a string" % value)
        #~ print "get_text_for_value"
        bc = self.items_dict.get(value,None)
        if bc is None:
            return _("%(value)r (invalid choice for %(list)s)") % dict(
                list=self.__name__,value=value)
        return self.display_text(bc)
    #~ def __unicode__(self):
        #~ return unicode(self.stored_name) # babel_get(self.names)
        
#~ class BabelChoice(babel.BabelText):
class BabelChoice(object):
    """
    A constant value whose unicode representation 
    depends on the current babel language at runtime.
    Used by :class:`lino.utils.choicelists`.

    """
    def __init__(self,choicelist,value,text):
        self.choicelist = choicelist
        self.value = value
        self.text = text
        #~ babel.BabelText.__init__(self,**kw)
        
    def __len__(self):
        return len(self.value)
        
    def __getattr__(self,name):
        return curry(getattr(self.choicelist,name),self)
        
    def __str__(self):
        #~ return "%s (%s:%s)" % (self.texts[babel.DEFAULT_LANGUAGE],
          #~ self.__class__.__name__,self.value)
        return "%s (%s:%s)" % (self.text,
            self.choicelist.__name__,self.value)
        
    def __unicode__(self):
        return unicode(self.text)
                
                



class DoYouLike(ChoiceList):
    """
    A list of possible answers to questions of type "How much do you like ...?".
    """
    label = _("certainly not...very much")
    
add = DoYouLike.add_item
#~ add('0', en="certainly not",de=u"bloß nicht", fr=u"certainement pas")
#~ add('1', en="rather not"   ,de="eher nicht" , fr=u"plutôt pas")       
#~ add('2', en="normally"     ,de="normal"     , fr=u"moyennement", ref="default")    
#~ add('3', en="quite much"   ,de="gerne"      , fr=u"assez bien")
#~ add('4', en="very much"    ,de="sehr gerne" , fr=u"très bien")
add('0',_("certainly not"))
add('1',_("rather not"))
add('2',_("normally"),alias="default")
add('3',_("quite much"))
add('4',_("very much"))

class HowWell(ChoiceList):
    """
    A list of possible answers to questions of type "How well ...?":
    "not at all", "a bit", "moderate", "quite well" and "very well" 
    
    which are stored in the database as '0' to '4',
    and whose `__unicode__()` returns their translated text.

    `lino.apps.dsbe.models.Languageknowledge.spoken` 
    `lino.apps.dsbe.models.Languageknowledge.written` 
    """
    label = _("not at all...very well")
    
add = HowWell.add_item
#~ add('0',en=u"not at all",de=u"gar nicht",   fr=u"pas du tout")
#~ add('1',en=u"a bit",     de=u"ein bisschen",fr=u"un peu")
#~ add('2',en=u"moderate",  de=u"mittelmäßig", fr=u"moyennement", ref="default")
#~ add('3',en=u"quite well",de=u"gut",         fr=u"bien")
#~ add('4',en=u"very well", de=u"sehr gut",    fr=u"très bien")
add('0',_("not at all"))
add('1',_("a bit"))
add('2',_("moderate"),alias="default")
add('3',_("quite well"))
add('4',_("very well"))


class Gender(ChoiceList):
    """
    Defines choices for the "Gender" of a person.

    """
add = Gender.add_item
add('M',_("Male"),alias='male')
add('F',_("Female"),alias='female')
    


def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()

