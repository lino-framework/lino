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


#~ from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from lino.utils import choicelists
from lino.utils import curry


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
    
        
#~ add = UserGroups.add_item
#~ add('system', _("System"))


class UserProfile(choicelists.Choice):
    def __init__(self,level='',**kw):
    #~ def __init__(self,**kw):
        self.level = level
        for g in UserGroups.items():
            #~ if g.value == 'system':
                #~ attname = 'level'
            #~ else:
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
add('10', _("User"),'user', level=UserLevels.user)
add('20', _("Administrator"),'admin', level=UserLevels.admin)


class Permittable(object): 
    """
    Base class for Components that have permissions control.
    """
    required = {}
    """
    Conditions required to read (view) this component.
    """
    workflow_state_field = None # internally needed for make_permission_handler
    workflow_owner_field = None # internally needed for make_permission_handler
    
    
    #~ def allow_read(self,user,obj,state):
        #~ return True
    
    def __init__(self):
        #~ super(PermissionComponent,self).__init__(self,*args,**kw)
        self.allow_read = curry(make_permission_handler(self,self,**self.required),self)

        
    def get_view_permission(self,user):
        #~ logger.info("20120622 %s.get_view_permission",self)
        return self.allow_read(user,None,None)
        
        



#~ BLANK_STATE = ''


def make_permission_handler(elem,actor,
    user_level=None,user_groups=None,states=None):
    """
    Return a function that will test whether permission is given or not.
    
    The generated function will always expect three arguments user, obj and state.
    The latter two may be None depending on the context
    (for example a read_required is expected to not test on obj or 
    state because these values are not known when generating the 
    :xfile:`lino*.js` files.).
    
    `user_level`
        A string (e.g. ``'manager'``, ``'user'``,...) 
        The minimum :class:`user level <lino.utils.choicelists.UserLevels>` 
        required to get the permission.
        The default value `None` means that no special user level is required.
        
    `user_groups`
        List of strings naming the user groups for which membership is required 
        to get permission to view this Actor.
        The default value `None` means
        
    `states`
        List of strings naming the user groups for which membership is required 
    
    
    """
    try:
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
                raise Exception(
                    """\
Cannot specify `states` on %s.required (`workflow_state_field` is %r).
                    """ % (elem,actor.workflow_state_field))
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
            allow2 = allow
            def allow(self,user,obj,state):
                if not allow2(self,user,obj,state): return False
                if obj is None: return True
                return state in states
        #~ return perms.Permission(allow)
        return allow
    except Exception,e:
        raise Exception("Exception while making permissions for %s: %s" % (actor,e))

        
