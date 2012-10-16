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

#~ from django.conf import settings
from django.utils.translation import ugettext_lazy as _
#~ from lino.utils.choicelists import ChoiceList, Choice
from lino.utils import curry
from lino.core.modeltools import obj2str



class Permittable(object):  
    """
    Base class for Components that have view permissions control.
    """
    
    required = None # not {}, see blog/2012/0923
    """
    Conditions required to read (view) this component.
    """
    
    workflow_state_field = None # internally needed for make_permission_handler
    workflow_owner_field = None # internally needed for make_permission_handler
    #~ readonly = True
    
    
    #~ def allow_read(self,user,obj,state):
        #~ return True
    
    def __init__(self,debug_permissions):
        #~ if type(debug_permissions) != bool:
            #~ raise Exception("20120925 %s %r",self,self)
        if self.required is None:
            self.allow_read = curry(make_permission_handler(
                self,self,True,
                debug_permissions),self)
        else:
            self.allow_read = curry(make_permission_handler(
                self,self,True,
                debug_permissions,
                **self.required),self)

        
    def get_view_permission(self,user):
        #~ if str(self.layout_handle.layout) == 'ClientDetail on pcsw.Clients':
            #~ if self.name == 'cbss':
                #~ logger.info("20120925 %s Permittable.get_view_permission(%s)", self,self.required)
        #~ logger.info("20120622 %s.get_view_permission",self)
        return self.allow_read(user,None,None)
        
        



#~ BLANK_STATE = ''


def make_permission_handler(
    elem,actor,
    readonly,debug_permissions,
    user_level=None,user_groups=None,states=None,allow=None,owner=None,auth=False):
    """
    Return a function that will test whether permission is given or not.
    
    `elem` is not used (either an Action or a Permittable.)
    
    `actor` is who contains the workflow state field
    
    `readonly`
    
    `debug_permissions`
    
    The generated function will always expect three arguments user, obj and state.
    The latter two may be None depending on the context
    (for example a read_required is expected to not test on obj or 
    state because these values are not known when generating the 
    :xfile:`lino*.js` files.).
    
    The remaining keyword arguments are aka "requirements":
    
    `user_level`
        A string (e.g. ``'manager'``, ``'user'``,...) 
        The minimum :class:`user level <lino.base.utils.UserLevels>` 
        required to get the permission.
        The default value `None` means that no special user level is required.
        
    `user_groups`
        List of strings naming the user groups for which membership is required 
        to get permission to view this Actor.
        The default value `None` means that no special group membership is required.
        Alternatively, if this is a string, it will be converted to a list of strings.
        
    `states`
        List of strings naming the user groups for which membership is required 
    
    `allow`
        An additional custom permission handler
        
    `auth`
        If True, permission is given for any authenticated user 
        (and not for :class:`lino.utils.auth.AnonymousUser`).
        
    `owner`
        If True, permission is given only to the author of the object. 
        If False, permission is given only to users who are not the author of the object. 
        This requirement is allowed only on models that have a field `user` 
        which is supposed to contain the author.
        Usually a subclass of :class:`lino.mixins.UserAuthored`,
        but e.g. :class:`lino.modlib.cal.models.Guest` 
        defines a property `user` because it has no own `user` field).
    
    
    """
    from lino.utils.choicelists import UserLevels, UserGroups
    try:
        if allow is None:
            def allow(action,user,obj,state):
                return True
        if auth:
            allow_before_auth = allow
            def allow(action,user,obj,state):
                if not user.authenticated:
                    return False
                return allow_before_auth(action,user,obj,state)
                
        if user_level is not None:
            user_level = getattr(UserLevels,user_level)
            allow_user_level = allow
            def allow(action,user,obj,state):
                #~ if user.profile.level is None or user.profile.level < user_level:
                if user.profile.level < user_level:
                    #~ print 20120715, user.profile.level
                    return False
                return allow_user_level(action,user,obj,state)
                
        if owner is not None:
            allow_owner = allow
            def allow(action,user,obj,state):
                if obj is not None and (user == obj.user) != owner:
                    return False
                return allow_owner(action,user,obj,state)
                
        if user_groups is not None:
            if isinstance(user_groups,basestring):
                user_groups = user_groups.split()
            if user_level is None:
                user_level = UserLevels.user
                #~ raise Exception("20120621")
            for g in user_groups:
                UserGroups.get_by_value(g) # raise Exception if no such group exists
                #~ if not UserGroups.get_by_name(g):
                    #~ raise Exception("Invalid UserGroup %r" % g)
            allow1 = allow
            def allow(action,user,obj,state):
                if not allow1(action,user,obj,state): return False
                for g in user_groups:
                    level = getattr(user.profile,g+'_level')
                    if level >= user_level:
                        return True
                #~ if isinstance(elem,Permittable):
                    #~ print '20120630 not for you:', elem
                return False
                
        if states is not None:
            #~ if not isinstance(actor.workflow_state_field,choicelists.ChoiceListField):
                #~ raise Exception(
                    #~ """\
#~ Cannot specify `states` when `workflow_state_field` is %r.
                    #~ """ % actor.workflow_state_field)
            #~ else:
                #~ print 20120621, "ok", actor
            lst = actor.workflow_state_field.choicelist
            #~ states = frozenset([getattr(lst,n) for n in states])
            #~ possible_states = [st.name for st in lst.items()] + [BLANK_STATE]
            ns = []
            if isinstance(states,basestring):
                states = states.split()
            for n in states:
                if n is not None:
                    if n == '_':
                        n = None
                    else:
                        n = lst.get_by_name(n)
                ns.append(n)
                #~ if n:
                    #~ ns.append(getattr(lst,n))
                #~ else:
                    #~ ns.append(lst.blank_item)
                    
                #~ if not st in possible_states:
                    #~ raise Exception("Invalid state %r, must be one of %r" % (st,possible_states))
            states = frozenset(ns)
            allow2 = allow
            if debug_permissions:
                logger.info("20121009 %s %s required states: %s",actor,elem,states)
            def allow(action,user,obj,state):
                if not allow2(action,user,obj,state): return False
                if obj is None: return True
                return state in states
        #~ return perms.Permission(allow)
        
        if not readonly:
            allow3 = allow
            def allow(action,user,obj,state):
                if not allow3(action,user,obj,state): return False
                if user.profile.readonly:
                    #~ if isinstance(elem,Permittable):
                        #~ print '20120630 not readonly:', elem
                    return False
                return True
        
        if debug_permissions: # False:
            #~ logger.info("20120920 debug_permissions %r",elem)
            allow4 = allow
            def allow(action,user,obj,state):
                v = allow4(action,user,obj,state)
                if True: # not v:
                    #~ logger.info(u"debug_permissions %s %s.required(%s,%s,%s), allow(%s,%s,%s)--> %s",
                      #~ actor,action.action_name,user_level,user_groups,states,user.username,obj2str(obj),state,v)
                    logger.info(u"debug_permissions %r required(%s,%s,%s), allow(%s,%s,%s)--> %s",
                      action,user_level,user_groups,states,user.username,obj2str(obj),state,v)
                return v
        return allow
        
    except Exception,e:
      
        raise Exception("Exception while making permissions for %s: %s" % (actor,e))

        

def set_required(obj,**kw):
    """
    Add the specified requirements to `obj`.
    `obj` can be an 
    :class:`lino.core.actors.Actor` or a 
    :class:`lino.utils.choicelists.Choice`.
    Application code uses this indirectly through the shortcut methods
    :meth:`lino.core.actors.Actor.set_required` or a 
    :meth:`lino.utils.choicelists.Choice.set_required`.
    
    """
    #~ logger.info("20120927 perms.set_required %r",kw)
    new = dict()
    new.update(getattr(obj,'required',{}))
    new.update(kw)
    obj.required = new
    
