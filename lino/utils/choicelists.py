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

ur"""
Utility for defining hard-coded multi-lingual choice lists 
whose value is rendered according to the current language.

:class:`Gender`, :class:`DoYouLike` and :class:`HowWell` 
are "batteries included" usage examples.

Usage:

(Doctesting this module requires the Django translation machine, 
so we must set :envvar:`DJANGO_SETTINGS_MODULE`)

>>> import os
>>> os.environ['DJANGO_SETTINGS_MODULE'] = 'lino.apps.std.settings'


>>> from django.utils import translation
>>> translation.activate('en')
>>> for value,text in choicelist_choices():
...     print "%s : %s" % (value, unicode(text))
DoYouLike : certainly not...very much
Gender : Gender
HowWell : not at all...very well

>>> for bc,text in Gender.choices:
...     print "%s : %s" % (bc.value, unicode(text))
M : Male
F : Female

>>> print unicode(Gender.male)
Male

>>> translation.activate('de')
>>> print unicode(Gender.male)
Männlich

>>> print str(Gender.male)
M\xe4nnlich

>>> print repr(Gender.male)
M\xe4nnlich (Gender.male:M)

Comparing Choices uses their *value* (not the alias or text):

>>> from lino.core.perms import UserLevels

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

import sys

from django.utils.functional import Promise
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import string_concat
from django.utils.functional import lazy
from django.db import models

from lino.utils import curry, unicode_string

from lino.core import actions
from lino.core import actors


class Choice(object):
    """
    A constant (hard-coded) value whose unicode representation 
    depends on the current babel language at runtime.
    Used by :class:`lino.utils.choicelists`.

    """
    def __init__(self,choicelist,value,text,name,**kw):
        self.choicelist = choicelist
        self.value = value
        self.text = text
        self.name = name
        for k,v in kw.items():
            setattr(self,k,v)
        
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
        if self.name is None:
            return "%s (%s:%s)" % (self,self.choicelist.__name__,self.value)
        return "%s (%s.%s:%s)" % (self,self.choicelist.__name__,self.name,self.value)
        
        
    def __str__(self):
        return unicode_string(self.text)
        #~ return unicode(self.text).encode(sys.getdefaultencoding(),'backslashreplace')
        
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
    #~ k = cl.stored_name or cl.__name__
    k = cl.stored_name or cl.actor_id
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
      
    
class ChoiceListMeta(actors.ActorMetaClass):
    def __new__(meta, classname, bases, classDict):
        #~ if not classDict.has_key('app_label'):
            #~ classDict['app_label'] = cls.__module__.split('.')[-2]
        """
        UserGroups manually sets max_length because the 
        default list has only one group with value "system", 
        but applications may want to add longer group names
        """
        classDict.setdefault('max_length',1)
        cls = actors.ActorMetaClass.__new__(meta, classname, bases, classDict)
        
        cls.items_dict = {}
        cls.clear()
        cls._fields = []
        #~ cls.max_length = 1
        #~ assert not hasattr(cls,'items') 20120620
        #~ for i in cls.items:
            #~ cls.add_item(i)
        if classname not in ('ChoiceList','Workflow'):
            register_choicelist(cls)
        return cls
  

#~ class ChoiceList(object):
class ChoiceList(actors.Actor):
    """
    Used-defined choice lists must inherit from this base class.
    """
    __metaclass__ = ChoiceListMeta
    
    item_class = Choice
    """
    The class of items of this list.
    """
    
    #~ blank = True
    #~ """
    #~ Set this to False if you don't want to accept 
    #~ any blank value for your ChoiceList.
    #~ """
    
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
    
    #~ def __init__(self,*args,**kw):
        #~ raise Exception("ChoiceList may not be instantiated")
        
    #~ grid = actions.GridEdit()
    
    @classmethod
    def get_default_action(cls):
        #~ return actions.BoundAction(cls,cls.grid)
        #~ return 'grid'
        return actions.GridEdit()
        
        
        
    @classmethod
    def clear(cls):
        """
        """
        
        # remove previously defined choices from class dict:
        for ci in cls.items_dict.values():
            if ci.name:
                delattr(cls,ci.name)
        cls.items_dict = {}
        cls.choices = []
        #~ if cls.blank:
            #~ cls.add_item('','',name='blank_item')
        cls.choices = [] # remove blank_item from choices
        
        #~ cls.items_dict = {'' : cls.blank_item }
        
        #~ cls.max_length = 1
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
    def add_item(cls,value,text,name=None,*args,**kw):
        return cls.add_item_instance(cls.item_class(cls,value,text,name,*args,**kw))
        
    @classmethod
    def add_item_instance(cls,i):
        #~ if cls is ChoiceList:
            #~ raise Exception("Cannot define items on the base class")
        if cls.items_dict.has_key(i.value):
            raise Exception("Duplicate value %r in %s." % (i.value,cls))
        dt = cls.display_text(i)
        cls.choices.append((i,dt))
        cls.preferred_width = max(cls.preferred_width,len(unicode(dt)))
        cls.items_dict[i.value] = i
        #~ cls.items_dict[i] = i
        if len(i.value) > cls.max_length:
            if len(cls._fields) > 0:
                raise Exception(
                    "%s cannot add value %r because fields exist and max_length is %d."
                    % (cls,i.value,cls.max_length)+"""\
When fields have been created, we cannot simply change their max_length because 
Django creates copies of them when inheriting models.
""")
            cls.max_length = len(i.value)
            #~ for fld in cls._fields:
                #~ fld.set_max_length(cls.max_length)
        if i.name:
            #~ if hasattr(cls,i.name):
            if cls.__dict__.has_key(i.name):
                raise Exception("An item named %r is already defined in %s" % (
                    i.name,cls.__name__))
            setattr(cls,i.name,i)
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
    def display_text(cls,bc):
        """
        Override this to customize the display text of choices.
        :class:`lino.core.perms.UserGroups` and :class:`lino.modlib.cv.models.CefLevel`
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
            #~ return getattr(self,name,None)
            return getattr(self,name)
        else:
            #~ return self.blank_item
            return None
            
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

    @classmethod
    def before_state_change(cls,obj,ar,kw,oldstate,newstate):
        pass

    @classmethod
    def after_state_change(cls,obj,ar,kw,oldstate,newstate):
        pass
    
class ChoiceListField(models.CharField):
    """
    A field that stores a value to be selected from a 
    :class:`lino.utils.choicelists.ChoiceList`.
    
    ChoiceListField cannot be nullable since they are implemented as CharFields.
    Therefore when filtering on empty values in a database query
    you cannot use ``__isnull``::
    
      for u in users.User.objects.filter(profile__isnull=False):
      
    You must either check for an empty string::
      
      for u in users.User.objects.exclude(profile='')

    or use the ``__gte`` operator::
      
      for u in users.User.objects.filter(profile__gte=dd.UserLevels.guest):
      
    
    
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
            #~ choices=choicelist.get_choices(),
            max_length=choicelist.max_length,
            #~ blank=choicelist.blank,  # null=True,
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
        
    def _get_choices(self):
        """
        HACK: Django by default stores a copy of our list 
        when the `choices` of a field are evaluated for the 
        first time.
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










class State(Choice):
        
    def add_workflow(self,label=None,help_text=None,**required):
        """
        `label` can be either a string or a subclass of ChangeStateAction
        """
        i = len(self.choicelist.workflow_actions)
        #~ if label and issubclass(label,actions.Action):
        kw = dict()
        if help_text is not None:
            kw.update(help_text=help_text)
        kw.update(sort_index=10+i)
        if label and not isinstance(label,(basestring,Promise)):#issubclass(label,ChangeStateAction):
            a = label(self,required,**kw)
        else:
            a = actions.ChangeStateAction(self,required,label=label or self.text,**kw)
        #~ name = 'mark_' + self.value
        name = 'wf' + str(i+1)
        a.attach_to_workflow(self.choicelist,name)
        #~ print 20120709, self, name, a
        self.choicelist.workflow_actions = self.choicelist.workflow_actions + [ a ]
        #~ self.choicelist.workflow_actions.append(a) 
        #~ yield name,a
        
        #~ if action_label is not None:
            #~ self.action_label = action_label
        #~ if help_text is not None:
            #~ self.help_text = help_text
        #~ self.required = required
        
    #~ def set_required(self,**kw):
        #~ from lino.core import perms
        #~ perms.set_required(self,**kw)
        


class Workflow(ChoiceList):
  
    workflow_actions = []
    
    item_class = State
  
    #~ @classmethod
    #~ def add_statechange(self,newstate,action_label=None,states=None,**kw):
        #~ old = self.get_by_name()
    
    @classmethod
    def before_state_change(cls,obj,ar,kw,oldstate,newstate):
        pass

    @classmethod
    def after_state_change(cls,obj,ar,kw,oldstate,newstate):
        pass

        
 #~ def set_required(self,**kw):
        #~ from lino.core import perms
        #~ perms.set_required(self,**kw)


class UserLevels(ChoiceList):
    """
    The level of a user is one way of differenciating users when 
    defining access permissions and workflows. 
    Lino speaks about user *level* where Plone speaks about user *role*.
    Unlike user roles in Plone, user levels are hierarchic:
    a "Manager" is higher than a simple "User" and thus 
    can do everything for which a simple "User" level has permission.
    
    About the difference between "Administrator" and "Manager":
    
    - "Management is closer to the employees. 
      Admin is over the management and more over the money 
      of the organization and lilscencing of an organization. 
      Mananagement manages employees. 
      Admin manages the outside contacts and the 
      facitlity as a whole." (`answerbag.com <http://www.answerbag.com/q_view/295182>`__)
    
    - See also a more detailed overview at
      http://www.differencebetween.com/difference-between-manager-and-vs-administrator/
    
    """
    label = _("User Level")
    app_label = 'lino'
    
    
    @classmethod
    def field(cls,module_name=None,**kw):
        """
        Shortcut to create a :class:`lino.core.fields.ChoiceListField` in a Model.
        """
        kw.setdefault('blank',True)
        if module_name is not None:
            kw.update(verbose_name=string_concat(cls.label,' (',module_name,')'))
        return super(UserLevels,cls).field(**kw)
        
add = UserLevels.add_item
add('10', _("Guest"),'guest')
#~ add('20', _("Restricted"),'restricted')
add('20', _("Secretary"),'secretary')
add('30', _("User"), "user")
add('40', _("Manager"), "manager")
add('50', _("Administrator"), "admin")
add('90', _("Expert"), "expert")
UserLevels.SHORT_NAMES = dict(A='admin',U='user',_=None,M='manager',G='guest',S='secretary')

class UserGroups(ChoiceList):
    """
    User Groups are another way of differenciating users when 
    defining access permissions and workflows. 
    
    Applications will 
    
    """
    label = _("User Group")
    app_label = 'lino'
    show_values = True
    max_length = 20 
    """
    """
        
#~ add = UserGroups.add_item
#~ add('system', _("System"))


class UserProfile(Choice):
  
    def __init__(self,cls,value,text,name=None,memberships=None,readonly=False,**kw):
      
        super(UserProfile,self).__init__(cls,value,text,name)
        
        #~ keys = ['level'] + [g+'_level' for g in choicelist.groups_list]
        #~ keys = ['level'] + [g+'_level' for g in choicelist.membership_keys]
        self.readonly = readonly

        if memberships is None:
            for k in cls.membership_keys:
                #~ kw[k] = UserLevels.blank_item
                #~ kw.setdefault(k,UserLevels.blank_item) 20120829
                kw.setdefault(k,None)
        else:
        #~ if memberships is not None:
            if len(memberships.split()) != len(cls.membership_keys):
                raise Exception(
                    "Invalid memberships specification %r : must contain %d letters" 
                    % (memberships,len(cls.membership_keys)))
            for i,k in enumerate(memberships.split()):
                kw[cls.membership_keys[i]] = UserLevels.get_by_name(UserLevels.SHORT_NAMES[k])
                
        #~ print 20120705, value, kw
        
        assert kw.has_key('level')
            
        for k,v in kw.items():
            setattr(self,k,v)
            
        
        #~ for grp in enumerate(UserGroups.items()):
            #~ attname = grp.value + '_level'
            #~ setattr(self,attname,kw.pop(attname,''))
        #~ if kw:
            #~ raise Exception("UserProfile got unexpected arguments %s" % kw)
            
        #~ dd.UserProfiles.add_item(value,label,None,**kw)
      
    #~ def __init__(self,level='',*args,**kw):
    #~ def __init__(self,level='',*args):
    #~ def __init__(self,**kw):
        #~ if level:
            #~ self.level = getattr(UserLevels,level)
        #~ else:
            #~ self.level = UserLevels.blank_item
        #~ self.level = UserLevels.get_by_name(level)
        #~ groups = UserGroups.items()
        #~ if len(args) > len(groups):
            #~ raise Exception("More arguments than user groups.")
        #~ for i,levelname in enumerate(args):
            #~ attname = groups[i].value + '_level'
            #~ v = UserLevels.get_by_name(levelname)
            #~ setattr(self,attname,v)
        #~ kw.setdefault('readonly',False)
        #~ for k,v in kw.items():
            #~ setattr(self,k,v)
            
    def __repr__(self):
        s = self.__class__.__name__ + ":" + self.value + "("
        s += "level=%s" % self.level.name
        for g in UserGroups.items():
            if g.value: # no level for UserGroups.blank_item
                v = getattr(self,g.value+'_level',None)
                if v is not None:
                    s += ",%s=%s" % (g.value,v.name)
        s += ")"
        return s
        

        
class UserProfiles(ChoiceList):
    """
    
    """
    #~ item_class = UserProfile
    label = _("User Profile")
    app_label = 'lino'
    show_values = True
    max_length = 20
    membership_keys = ('level',)
    
    #~ @classmethod
    #~ def clear(cls):
        #~ cls.groups_list = [g.value for g in UserGroups.items()]
        #~ super(UserProfiles,cls).clear()
          

    #~ @classmethod
    #~ def clear(cls,groups='*'):
    @classmethod
    def reset(cls,groups):
        #~ cls.groups_list = [g.value for g in UserGroups.items()]
        s = []
        expected_names = set(['*']+[g.value for g in UserGroups.items() if g.value])
        for g in groups.split():
            if not g in expected_names:
                raise Exception("Unexpected name %r (UserGroups are: %s)" % (
                    g,[g.value for g in UserGroups.items() if g.value]))
            else:
                expected_names.remove(g)
                if g == '*':
                    s.append('level')
                else:
                    if not UserGroups.get_by_value(g):
                        raise Exception("Unknown group %r" % g)
                    s.append(g+'_level')
        if len(expected_names) > 0:
            raise Exception("Missing name(s) %s in %r" % (expected_names,groups))
        cls.membership_keys = tuple(s)
        cls.clear()

    @classmethod
    def add_item(cls,value,text,memberships=None,name=None,**kw):
        return cls.add_item_instance(UserProfile(cls,value,text,name,memberships,**kw))
          
    
add = UserProfiles.add_item
add('100', _("User"), name='user', level='user')
add('900', _("Administrator"), name='admin', level='admin')






def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()

