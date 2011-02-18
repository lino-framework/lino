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

from django.db import models
from django.utils.translation import ugettext_lazy as _

from lino.utils import babel

CHOICELISTS = {}

def register_choicelist(ch):
    if not isinstance(ch.stored_name,basestring):
        raise Exception("Invalid stored_name %r" % ch.stored_name)
    if CHOICELISTS.has_key(ch.stored_name):
        raise Exception("Duplicate Chooser.stored_name %s" % ch.stored_name)
    CHOICELISTS[ch.stored_name] = ch
    
def get_choicelist(i):
    return CHOICELISTS[i]

class ChoiceList(object):
    #~ def __init__(self,stored_name,choices,**names):
    def __init__(self,stored_name,value_class,items):
        self.stored_name = stored_name
        self.value_class = value_class
        #~ self.choices = [ (i.pk,i) for i in items]
        self.choices = [ (i,unicode(i)) for i in items]
        #~ self.names = names
        self.max_length = max([len(i.pk) for i in items])
        self.items = {}
        for i in items:
            self.items[i.pk] = i
        register_choicelist(self)
        
    def to_python(self, value):
        if isinstance(value, self.value_class):
            return value        
        return self.items.get(value)
        
        
    def get_choices(self):
        return self.choices
      
    def __unicode__(self):
        return unicode(self.stored_name) # babel_get(self.names)
        
def choicelist_choices():
    return [ (k,unicode(v)) for k,v in CHOICELISTS.items()]


class Strength(babel.BabelValue):
    pass
    
#~ STRENGTH_CHOICES = [
  #~ ('0' , _("certainly not")),     # bloß nicht
  #~ ('1' , _("rather not")),        # eher nicht
  #~ ('2' , _("normally")),          # 
  #~ ('3' , _("quite much")),        # gerne
  #~ ('4' , _("very much")),         # sehr gerne
#~ ]

STRENGTH_LIST = ChoiceList("HowMuchDoYouLike", Strength, [
  Strength('0' , en="certainly not",de=u"bloß nicht"),     
  Strength('1' , en="rather not"   ),        # eher nicht
  Strength('2' , en="normally"     ),          # 
  Strength('3' , en="quite much"   ),        # gerne
  Strength('4' , en="very much"    ),         # sehr gerne
])


class Knowledge(babel.BabelValue):
    pass
    

#~ KNOWLEDGE_LIST = 

#~ KNOWLEDGE_DICT = {}
#~ for k in KNOWLEDGE_LIST:
    #~ KNOWLEDGE_DICT[k.pk] = k

#~ KNOWLEDGE_CHOICES = [ (k,unicode(k)) for k in KNOWLEDGE_LIST]

KNOWLEDGE_LIST = ChoiceList("HowWellDoYouKnow", Knowledge, [
  Knowledge('0',en=u"not at all",de=u"gar nicht",   fr=u"pas du tout"),
  Knowledge('1',en=u"a bit",     de=u"ein bisschen",fr=u"un peu"),
  Knowledge('2',en=u"moderate",  de=u"mittelmäßig", fr=u"moyennement"),
  Knowledge('3',en=u"quite well",de=u"gut",         fr=u"bien"),
  Knowledge('4',en=u"very well", de=u"sehr gut",    fr=u"très bien"),
])



class ChoiceListField(models.CharField):
    """
    
    """
    
    __metaclass__ = models.SubfieldBase
    
    choicelist = NotImplementedError
    
    def __init__(self,*args,**kw):
        defaults = dict(
            #~ choices=KNOWLEDGE_CHOICES,
            choices=self.choicelist.get_choices(),
            max_length=self.choicelist.max_length,
            blank=True,null=True,
            #~ validators=[validate_knowledge],
            #~ limit_to_choices=True,
            )
        defaults.update(kw)
        #~ models.SmallIntegerField.__init__(self,*args, **defaults)
        models.CharField.__init__(self,*args, **defaults)
        
    def get_internal_type(self):
        return "CharField"
        
    def to_python(self, value):
        return self.choicelist.to_python(value)
        
    def get_prep_value(self, value):
        if value:
            return value.pk
        return None
        
    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)
        
    #~ def save_form_data(self, instance, data):
        #~ setattr(instance, self.name, data)
    
class KnowledgeField(ChoiceListField):
    choicelist = KNOWLEDGE_LIST
    
    """
    A char field that can take one of the 
    :class:`lino.utils.babel.BabelValue` values 
    "not at all", "a bit", "moderate", "quite well" and "very well" 
    which are stored in the database as '0' to '4',
    and whose `__unicode__()` returns their translated text.
    
    `lino.modlib.dsbe.models.Languageknowledge.spoken` 
    `lino.modlib.dsbe.models.Languageknowledge.written` 
    """
  
        
class StrengthField(ChoiceListField):
    choicelist = STRENGTH_LIST

if False:
    class StrengthField(models.CharField):
        def __init__(self, *args, **kw):
            defaults = dict(
                #~ choices=STRENGTH_CHOICES,
                choices=HowMuchDoYouLike.get_choices(),
                max_length=1,
                blank=True,null=True,
                #~ validators=[validate_knowledge],
                #~ limit_to_choices=True,
                )
            defaults.update(kw)
            #~ models.SmallIntegerField.__init__(self,*args, **defaults)
            models.CharField.__init__(self,*args, **defaults)
            #~ models.IntegerField.__init__(self,*args, **defaults)
        
            
