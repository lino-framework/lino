## Copyright 2012 Luc Saffre
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

import logging
logger = logging.getLogger(__name__)

from django.utils.translation import ugettext_lazy as _


#~ from django.conf import settings
#~ from django.utils.translation import ugettext_lazy as _
from lino.utils.choicelists import ChoiceList, Choice
#~ from lino.utils import curry
#~ from lino.core.modeltools import obj2str





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
    verbose_name = _("User Level")
    verbose_name_plural = _("User Levels")
    app_label = 'lino'
    
    
    @classmethod
    def field(cls,module_name=None,**kw):
        """
        Shortcut to create a :class:`lino.core.fields.ChoiceListField` in a Model.
        """
        kw.setdefault('blank',True)
        if module_name is not None:
            kw.update(verbose_name=string_concat(cls.verbose_name,' (',module_name,')'))
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
    verbose_name = _("User Group")
    verbose_name_plural = _("User Groups")
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
        #~ s = self.__class__.__name__ 
        s = str(self.choicelist)
        if self.name:
            s += "." + self.name
        s += ":" + self.value + "("
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
    verbose_name = _("User Profile")
    verbose_name_plural = _("User Profiles")
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
    def reset(cls,groups=None):
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
        if len(expected_names) > 0:
            raise Exception("Missing name(s) %s in %r" % (expected_names,groups))
        cls.membership_keys = tuple(s)
        cls.clear()

    @classmethod
    def add_item(cls,value,text,memberships=None,name=None,**kw):
        return cls.add_item_instance(UserProfile(cls,value,text,name,memberships,**kw))

#~ UserProfiles choicelist is going to be filled in `lino.Lino.setup_choicelists` 
#~ because attributes of Choice depend on UserGroups
    
#~ add = UserProfiles.add_item
#~ add('100', _("User"), name='user', level='user')
#~ add('900', _("Administrator"), name='admin', level='admin')




