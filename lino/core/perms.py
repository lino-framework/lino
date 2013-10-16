## Copyright 2010-2013 Luc Saffre
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

from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils import translation

from lino.core.choicelists import ChoiceList, Choice
from lino.core.actors import get_default_required as required


class UserLevel(Choice):
    short_name = None
    
class UserLevels(ChoiceList):
    """
    The level of a user is one way of differenciating users when 
    defining access permissions and workflows. 
    
    See :ref:`UserLevels`
    
    """
    verbose_name = _("User Level")
    verbose_name_plural = _("User Levels")
    app_label = 'lino'
    required = required(user_level='admin')
    short_name = models.CharField(_("Short name"),max_length=2,
        help_text=_("Used when defining UserProfiles"))
        
    
    @classmethod
    def get_column_names(self,ar):
        return 'value name short_name text remark'
        #~ return 'value name short_name *'
    
    @classmethod
    def field(cls,module_name=None,**kw):
        """
        Extends :meth:`lino.core.fields.ChoiceListField.field` .
        """
        kw.setdefault('blank',True)
        if module_name is not None:
            kw.update(verbose_name=translation.string_concat(cls.verbose_name,' (',module_name,')'))
        return super(UserLevels,cls).field(**kw)
        
    #~ @fields.virtualfield(models.CharField(_("Short name"),max_length=2,
        #~ help_text="used to fill UserProfiles"))
    #~ def short_name(cls,choice,ar):
        #~ return choice.short_name
        
        
        
add = UserLevels.add_item
add('10', _("Guest"),'guest',short_name='G')
#~ add('20', _("Restricted"),'restricted')
#~ add('20', _("Secretary"),'secretary')
add('30', _("User"), "user",short_name='U')
add('40', _("Manager"), "manager",short_name='M')
add('50', _("Administrator"), "admin",short_name='A')
#~ add('90', _("Expert"), "expert",short_name='E')
#~ UserLevels.SHORT_NAMES = dict(A='admin',U='user',_=None,M='manager',G='guest',S='secretary')
#~ UserLevels.SHORT_NAMES = dict(A='admin',U='user',_=None,M='manager',G='guest',R='restricted')
UserLevels.SHORT_NAMES = dict(A='admin',U='user',_=None,M='manager',G='guest')

"""

"""

class UserGroups(ChoiceList):
    """
    TODO: Rename this to "FunctionalGroups" or sth similar.
    
    Functional Groups are another way of differenciating users when 
    defining access permissions and workflows. 
    
    Applications can define their functional groups
    
    """
    required = required(user_level='admin')
    verbose_name = _("User Group")
    verbose_name_plural = _("User Groups")
    app_label = 'lino'
    show_values = True
    max_length = 20 
    """
    """
        
#~ add = UserGroups.add_item
#~ add('system', _("System"))

# filled using add_user_group()





class UserProfile(Choice):
    
    hidden_languages = None
    """
    A subset of :attr:`languages <north.Site.languages>` 
    which should be hidden in this user profile.
    Default value is :attr:`hidden_languages <UserProfiles.hidden_languages>`.
    This is used on multilingual sites with more than 4 or 5 languages.
    See the source code of :meth:`lino_welfare.settings.Site.setup_choicelists`
    for a usage example.
    """
    
    def __init__(self,cls,value,text,
            name=None,memberships=None,authenticated=True,
            readonly=False,
            #~ expert=False,
            **kw):
      
        super(UserProfile,self).__init__(value,text,name)
        #~ keys = ['level'] + [g+'_level' for g in choicelist.groups_list]
        #~ keys = ['level'] + [g+'_level' for g in choicelist.membership_keys]
        self.readonly = readonly
        #~ self.expert = expert
        self.authenticated = authenticated
        self.memberships = memberships
        self.kw = kw
        
    def attach(self,cls):
        super(UserProfile,self).attach(cls)
        self.kw.setdefault('hidden_languages',cls.hidden_languages)
        if self.memberships is None:
            for k in cls.membership_keys:
                #~ kw[k] = UserLevels.blank_item
                #~ kw.setdefault(k,UserLevels.blank_item) 20120829
                self.kw.setdefault(k,None)
        else:
        #~ if memberships is not None:
            if len(self.memberships.split()) != len(cls.membership_keys):
                raise Exception(
                    "Invalid memberships specification %r : must contain %d letters" 
                    % (self.memberships,len(cls.membership_keys)))
            for i,k in enumerate(self.memberships.split()):
                self.kw[cls.membership_keys[i]] = UserLevels.get_by_name(UserLevels.SHORT_NAMES[k])
                
        #~ print 20120705, value, kw
        
        assert self.kw.has_key('level')
        
        
        for k,vf in cls.virtual_fields.items():
            if vf.has_default():
                self.kw.setdefault(k,vf.get_default())
            elif vf.return_type.blank:
                self.kw.setdefault(k,None)
            #~ if k == 'accounting_level':
            #~ if k == 'hidden_languages':
                #~ print 20130920, k, vf, vf.has_default(), vf.get_default()
        #~ self.kw.setdefault('hidden_languages',cls.hidden_languages.default)
        
            
        for k,v in self.kw.items():
            setattr(self,k,v)
            
        for k in cls.default_memberships:
            setattr(self,k,self.level)
            
        if self.hidden_languages is not None:
            self.hidden_languages = set(settings.SITE.resolve_languages(self.hidden_languages))
            
        del self.kw
        del self.memberships
        
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
        #~ s = self.__class__.__name__ 
        s = str(self.choicelist)
        if self.name:
            s += "." + self.name
        s += ":" + self.value + "("
        #~ s += "level=%s" % self.level.name
        s += "level=%s" % self.level
        for g in UserGroups.items():
            if g.value: # no level for UserGroups.blank_item
                v = getattr(self,g.value+'_level',None)
                if v is not None:
                    s += ",%s=%s" % (g.value,v.name)
        s += ")"
        return s
        
    #~ def hide_languages(self,languages):
        #~ self.hidden_languages = set(settings.SITE.resolve_languages(languages))
            
        
        

        
class UserProfiles(ChoiceList):
    """
    Deserves a docstring.
    """
    required = required(user_level='admin')
    #~ item_class = UserProfile
    verbose_name = _("User Profile")
    verbose_name_plural = _("User Profiles")
    app_label = 'lino'
    show_values = True
    max_length = 20
    membership_keys = ('level',)
    
    preferred_foreignkey_width = 20 
    
    #~ 20130920 
    hidden_languages = settings.SITE.hidden_languages 
    #~ hidden_languages = fields.NullCharField(_("Hidden languages"),
        #~ max_length=200,null=True,default=settings.SITE.hidden_languages)
    """
    Default value for the :attr:`hidden_languages <UserProfile.hidden_languages>`
    of newly attached choice item
    """
    
    level = UserLevels.field(_("System"))
    
    
    #~ @classmethod
    #~ def clear(cls):
        #~ cls.groups_list = [g.value for g in UserGroups.items()]
        #~ super(UserProfiles,cls).clear()
          

    #~ @classmethod
    #~ def clear(cls,groups='*'):
    @classmethod
    def reset(cls,groups=None,hidden_languages=None):
        """
        Deserves a docstring.
        """
        if hidden_languages is not None:
            cls.hidden_languages = hidden_languages
        #~ cls.groups_list = [g.value for g in UserGroups.items()]
        expected_names = set(['*']+[g.value for g in UserGroups.items() if g.value])
        if groups is None:
            groups = ' '.join(expected_names)
            #~ cls.membership_keys = tuple(expected_names)
        s = []
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
        #~ if len(expected_names) > 0:
            #~ raise Exception("Missing name(s) %s in %r" % (expected_names,groups))
        cls.default_memberships = expected_names
        cls.membership_keys = tuple(s)
        cls.clear()

    @classmethod
    def add_item(cls,value,text,memberships=None,name=None,**kw):
        return cls.add_item_instance(UserProfile(cls,value,text,name,memberships,**kw))

#~ UserProfiles choicelist is going to be filled in `lino.site.Site.setup_choicelists` 
#~ because the attributes of each item depend on UserGroups



def add_user_group(name,label):
    """
    Add a user group to the :class:`UserGroups <lino.core.perms.UserGroups>` 
    choicelist. If a group with that name already exists, add `label` to the 
    existing group.
    """
    #~ logging.info("add_user_group(%s,%s)",name,label)
    #~ print "20120705 add_user_group(%s,%s)" % (name,unicode(label))
    g = UserGroups.items_dict.get(name)
    if g is None:
        g = UserGroups.add_item(name,label)
    else:
        if g.text != label:
            g.text += " & " + unicode(label)
    #~ if False: 
        # TODO: 'UserProfile' object has no attribute 'accounting_level'
    k = name+'_level'
    UserProfiles.inject_field(k,UserLevels.field(g.text,blank=True))
    UserProfiles.virtual_fields[k].lino_resolve_type()

    


