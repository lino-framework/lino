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

"""
Utility for defining hard-coded multi-lingual choice lists 
whose value is rendered according to the current babel language.

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

from django.db import models
from django.utils.translation import ugettext_lazy as _

from lino.utils import babel

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
        return ChoiceListField(cls,*args,**kw)
        
    @classmethod
    def add_item(cls,value,ref=None,**kw):
        if cls is ChoiceList:
            raise Exception("Cannot define items on the base class")
        i = babel.BabelChoice(value,**kw)
        cls.choices.append((i,cls.display_text(i)))
        assert not cls.items_dict.has_key(value)
        cls.items_dict[value] = i
        #~ cls.items_dict[i] = i
        cls.max_length = max(len(value),cls.max_length)
        if ref is not None:
            if hasattr(cls,ref):
                raise Exception("Attribute %r already defined in %s" % (
                    ref,cls.__name__))
            setattr(cls,ref,i)
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
        return unicode(bc)
        
    @classmethod
    def get_text_for_value(self,value):
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
        

class ChoiceListField(models.CharField):
    """
    
    """
    
    __metaclass__ = models.SubfieldBase
    
    #~ choicelist = NotImplementedError
    
    def __init__(self,choicelist,*args,**kw):
        if args:
            verbose_name = args[0]
            args = args[1:]
        else:
            verbose_name = kw.pop('verbose_name',None)
        if verbose_name is None:
            verbose_name = choicelist.label
        self.choicelist = choicelist
        defaults = dict(
            #~ choices=KNOWLEDGE_CHOICES,
            choices=choicelist.get_choices(),
            max_length=choicelist.max_length,
            blank=True,  # null=True,
            #~ validators=[validate_knowledge],
            #~ limit_to_choices=True,
            )
        defaults.update(kw)
        #~ models.SmallIntegerField.__init__(self,*args, **defaults)
        models.CharField.__init__(self,verbose_name,*args, **defaults)
        
    def get_internal_type(self):
        return "CharField"
        
    def to_python(self, value):
        if isinstance(value,babel.BabelChoice):
            return value
        value = self.choicelist.to_python(value)
        if value is None: # see 20110907
            value = ''
        return value
        
    def get_prep_value(self, value):
        if value:
            return value.value
        return '' # see 20110907
        #~ return None
        
    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_prep_value(value)
        #~ return self.get_db_prep_value(value,connection)
        
    #~ def save_form_data(self, instance, data):
        #~ setattr(instance, self.name, data)
        
    def get_text_for_value(self,value):
        return self.choicelist.get_text_for_value(value.value)
    
      



class DoYouLike(ChoiceList):
    """
    A list of possible answers to questions of type "How much do you like ...?".
    """
    label = _("certainly not...very much")
    
add = DoYouLike.add_item
add('0', en="certainly not",de=u"bloß nicht", fr=u"certainement pas")
add('1', en="rather not"   ,de="eher nicht" , fr=u"plutôt pas")       
add('2', en="normally"     ,de="normal"     , fr=u"moyennement", ref="default")    
add('3', en="quite much"   ,de="gerne"      , fr=u"assez bien")
add('4', en="very much"    ,de="sehr gerne" , fr=u"très bien")


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
add('0',en=u"not at all",de=u"gar nicht",   fr=u"pas du tout")
add('1',en=u"a bit",     de=u"ein bisschen",fr=u"un peu")
add('2',en=u"moderate",  de=u"mittelmäßig", fr=u"moyennement", ref="default")
add('3',en=u"quite well",de=u"gut",         fr=u"bien")
add('4',en=u"very well", de=u"sehr gut",    fr=u"très bien")

