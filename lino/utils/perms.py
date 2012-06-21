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

#~ Note: doctesting this module requires the Django translation machine, 
#~ so you must set :setting:`DJANGO_SETTINGS_MODULE` using something like::
#~   set DJANGO_SETTINGS_MODULE=lino.apps.std.settings
#~ >>> import os
#~ >>> os.environ['DJANGO_SETTINGS_MODULE'] = 'lino.apps.std.settings'



#~ from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from lino.utils import choicelists

class UserLevels(choicelists.ChoiceList):
    """
    The level of a user is one way of differenciating users when 
    giving access permissions. User levels are a graduation: 
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
add('20', _("Restricted"),'restricted')
add('30', _("User"), "user")
add('40', _("Manager"), "manager")
add('50', _("Administrator"), "admin")
add('90', _("Expert"), "expert")

class UserGroups(choicelists.ChoiceList):
    """
    This list is cleared and re-filled in lino.apps.pcsw.models. 
    applications may want to clear() this list and add longer 
    names than the only default "system".
    Since this redefinitions happens at a moment where database 
    fields have already been instantiated, 
    it is too late to change their max_length.
    """
    label = _("User Group")
    show_values = True
    max_length = 20 
    """
    """
    
        
add = UserGroups.add_item
add('system', _("System"))


class UserProfile(choicelists.Choice):
    #~ def __init__(self,level='',**kw):
    def __init__(self,**kw):
        #~ self.level = level
        for g in UserGroups.items():
            if g.value == 'system':
                attname = 'level'
            else:
                attname = g.value + '_level'
            setattr(self,attname,kw.pop(attname,''))
        if kw:
            raise Exception("UserProfile got unexpected arguments %s" % kw)
        
class UserProfiles(choicelists.ChoiceList):
    """
    
    """
    item_class = UserProfile
    label = _("User Profile")
    show_values = False
    max_length = 20
    
add = UserProfiles.add_item
add('1', _("User"),level=UserLevels.user)
add('2', _("Administrator"),level=UserLevels.admin)


BLANK_STATE = ''


#~ def make_permission(actor,required_user_level=None,required_user_groups=None,required_states=None):
def make_permission(actor,user_level=None,user_groups=None,states=None):
    """
    Return a function that will test whether permission is given or not.
    The function will always expect three arguments user, obj and state.
    The latter two may be None depending on the context. 
    For example a read_required is expected to not test on obj or state.
    """
    #~ user = _for_user
    if user_level is None:
        def allow(self,user,obj,state):
            return True
    else:
        user_level = getattr(UserLevels,user_level)
        def allow(self,user,obj,state):
            if user.profile.level is None or user.profile.level < user_level:
                return False
            return True
    if user_groups is not None:
        if user_level is None:
            user_level = UserLevels.user
            #~ raise Exception("20120621")
        else:
            user_level = getattr(UserLevels,user_level)
        allow1 = allow
        def allow(self,user,obj,state):
            if not allow1(self,user,obj,state): return False
            for g in user_groups:
                level = getattr(user.profile,g+'_level')
                if level >= user_level:
                    return True
            return False
            
    if states is not None:
        if not isinstance(actor.workflow_state_field,choicelists.ChoiceListField):
            raise Exception("%r.workflow_state_field is not a ChoiceListField" % actor)
        #~ else:
            #~ print 20120621, "ok", actor
        lst = actor.workflow_state_field.choicelist
        #~ states = frozenset([getattr(lst,n) for n in states])
        #~ possible_states = [st.name for st in lst.items()] + [BLANK_STATE]
        ns = []
        for n in states:
            if n:
                ns.append(getattr(lst,n))
            else:
                ns.append(lst.blank_item)
                
            #~ if not st in possible_states:
                #~ raise Exception("Invalid state %r, must be one of %r" % (st,possible_states))
        states = frozenset(ns)
        allow1 = allow
        def allow(self,user,obj,state):
            if not allow1(self,user,obj,state): return False
            if obj is None: return True
            return state in states
    #~ return perms.Permission(allow)
    return allow

        



#~ class Permittable(object):
    #~ create_required = dict()
    #~ read_required = dict()
    #~ update_required = dict()
    #~ delete_required = dict()
    
    #~ allow_create = lambda u,o,s : True
    #~ allow_read = lambda u,o,s : True
    #~ allow_update = lambda u,o,s : True
    #~ allow_delete = lambda u,o,s : True
    
    #~ def setup_permissions(self,state_field):
        #~ self.allow_create = make_permission(state_field,**self.create_required)
        #~ self.allow_read = make_permission(state_field,**self.read_required)
        #~ self.allow_update = make_permission(state_field,**self.update_required)
        #~ self.allow_delete = make_permission(state_field,**self.delete_required)
    
    #~ @classmethod
    #~ def read_required(self):
        #~ return dict()

    #~ @classmethod
    #~ def create_required(self):
        #~ return self.update_required()

    #~ @classmethod
    #~ def update_required(self):
        #~ return kw

    #~ @classmethod
    #~ def delete_required(self):
        #~ return self.update_required()



#~ class Required(object):
    #~ """
    #~ """
    #~ states = None
    #~ user_level = None
    #~ """
    #~ The minimum :class:`lino.utils.choicelists.UserLevels` 
    #~ required to get permission to view this Actor.
    #~ The default value `None` means that no special UserLevel is required.
    #~ """
    
    #~ user_groups = None
    #~ """
    #~ List of strings naming the user groups for which membership is required 
    #~ to get permission to view this Actor.
    #~ The default value `None` means
    #~ """
    #~ def __init__(self,**kw):
        #~ for k,v in kw.items():
            #~ if not self.__dict__.haskey(k):
                #~ raise Exception("Invalid keyword %s" % k)
            #~ setattr(self,k,v)
            
    
  
#~ class Permission(object):
  
    #~ def __init__(self,allow):
        #~ self.allow = allow
  
    #~ def allow(self,obj,user):
        #~ raise NotImplementedError()
  
#~ class Always(Permission):
    #~ def allow(self,obj,user):
        #~ return True
        
#~ ALWAYS = Always()

#~ ALWAYS = Permission(lambda obj,user: True)
#~ NEVER = Permission(lambda obj,user: False)

#~ class Never(Permission):
  
    #~ def allow(self,obj,user):
        #~ return False
  
#~ NEVER = Never()



#~ class OwnedOnlyPermission(Permission):
    #~ def allow(self,obj,user):
        #~ if obj.user != user:
            #~ return False
        #~ return Permission.allow(self,obj,user)






if False:
    class ViewPermissionBase(object):
        """
        Inherited by 
        :class:`lino.core.actors.Actor`,
        :class:`lino.utils.jsgen.Component`,
        but also instantiated 
        :meth:`lino.models.Workflow.get_permission`.
        """
        
        required_user_level = None
        """
        The minimum :class:`lino.utils.choicelists.UserLevels` 
        required to get permission to view this Actor.
        The default value `None` means that no special UserLevel is required.
        See also :attr:`required_user_groups`
        """
        
        required_user_groups = None
        """
        List of strings naming the user groups for which membership is required 
        to get permission to view this Actor.
        The default value `None` means
        """
        
    class ViewPermissionClass(ViewPermissionBase):
        @classmethod    
        def get_view_permission(cls,user):
            return _get_view_permission(cls,user)
            
    class ViewPermissionInstance(ViewPermissionBase):
        def __init__(self,**kw):
            for k,v in kw.items(): 
                setattr(self,k,v)
                
        def get_view_permission(self,user):
            #~ if self.required_user_groups is not None or self.required_user_level is not None:
                #~ print 20120616, user, self.required_user_groups, self.required_user_level
            return _get_view_permission(self,user)
            
    def _get_view_permission(self,user):
        """
        Return `True` if the specified `user` has permission 
        to see this.
        """
        #~ if hasattr(self,'value') and self.value.get("title") == "CBSS":
            #~ print "20120525 jsgen.get_view_permission()", self
        #~ user = _for_user
        if self.required_user_level is None:
            if self.required_user_groups is None:
                return True
            for g in self.required_user_groups:
                if getattr(user.profile,g+'_level'):
                #~ if getattr(user,g+'_level',None) is not None:
                    return True
            return False
        else:
            if user.profile.level is None or user.profile.level < self.required_user_level:
                return False
            if self.required_user_groups is None:
                return True
            for g in self.required_user_groups:
                level = getattr(user.profile,g+'_level')
                #~ if level is not None and level >= self.required_user_level:
                if level >= self.required_user_level:
                    return True
        return False
    
    



#~ def _test():
    #~ import doctest
    #~ doctest.testmod()

#~ if __name__ == "__main__":
    #~ _test()

