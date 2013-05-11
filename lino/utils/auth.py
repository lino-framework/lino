# -*- coding: UTF-8 -*-
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

"""

Overview
--------

Lino's authentification utilities

Notes
-----

Notes about marked code locations:

[C1] Before logging the error we must create a `request.user` 
     attribute, otherwise Django might say 
     "AssertionError: The XView middleware requires authentication 
     middleware to be installed."
     
Documented classes and functions
--------------------------------

"""

import os
import logging
logger = logging.getLogger(__name__)


from django.utils.translation import ugettext_lazy as _

from django.core import exceptions
from django.utils import translation
from django.conf import settings
from django import http

from lino.core.choicelists import ChoiceList, Choice
from lino.core.actors import get_default_required as required

from lino.core.dbutils import obj2str
from lino.core import constants # as ext_requests


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
    required = required(user_level='admin')
    
    
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


class UserProfile(Choice):
    
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
            
        for k,v in self.kw.items():
            setattr(self,k,v)
            
        for k in cls.default_memberships:
            setattr(self,k,self.level)
            
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

    #~ @classmethod
    #~ def clear(cls):
        #~ cls.groups_list = [g.value for g in UserGroups.items()]
        #~ super(UserProfiles,cls).clear()
          

    #~ @classmethod
    #~ def clear(cls,groups='*'):
    @classmethod
    def reset(cls,groups=None):
        """
        Deserves a docstring.
        """
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

#~ UserProfiles choicelist is going to be filled in `lino.Site.setup_choicelists` 
#~ because the attributes of each item depend on UserGroups


#~ def default_required(): return dict(auth=True)

def make_permission_handler(*args,**kw):
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
    #~ try:
    return make_permission_handler_(*args,**kw)
    #~ except Exception,e:
        #~ raise Exception("Exception while making permissions for %s: %s" % (actor,e))

def make_view_permission_handler(*args,**kw):
    """
    Similar to :func:`make_permission_handler`, but for static view permissions 
    which don't have an object nor states.
    """
    return make_view_permission_handler_(*args,**kw)
    
def make_view_permission_handler_(
    actor,readonly,debug_permissions,
    user_level=None,user_groups=None,allow=None,auth=False,
    owner=None,states=None):
    #~ if states is not None:
        #~ logger.info("20121121 ignoring required states %s for %s",states,actor)
    #~ if owner is not None:
        #~ logger.info("20121121 ignoring required owner %s for %s",owner,actor)
    if allow is None:
        def allow(action,profile):
            return True
    #~ if settings.SITE.user_model is not None:
    if True: # e.g. e.g. public readonly site
        if auth:
            allow_before_auth = allow
            def allow(action,profile):
                if not profile.authenticated:
                    return False
                return allow_before_auth(action,profile)
            
        if user_level is not None:
            user_level = getattr(UserLevels,user_level)
            allow_user_level = allow
            def allow(action,profile):
                if profile.level < user_level:
                    return False
                return allow_user_level(action,profile)
                
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
            def allow(action,profile):
                if not allow1(action,profile): return False
                for g in user_groups:
                    level = getattr(profile,g+'_level')
                    if level >= user_level:
                        return True
                return False
    
    if not readonly:
        allow3 = allow
        def allow(action,profile):
            if not allow3(action,profile): return False
            if profile.readonly:
                return False
            return True
    
    if debug_permissions: # False:
        #~ logger.info("20130424 install debug_permissions for %s",
            #~ [actor,readonly,debug_permissions,
            #~ user_level,user_groups,allow,auth,owner,states])
        allow4 = allow
        def allow(action,profile):
            v = allow4(action,profile)
            if True: # not v:
                logger.info(u"debug_permissions (view) %r required(%s,%s), allow(%s)--> %s",
                  action,user_level,user_groups,profile,v)
            return v
    return allow
        

def make_permission_handler_(
    elem,actor,readonly,debug_permissions,
    user_level=None,user_groups=None,states=None,allow=None,owner=None,auth=False):
        
    #~ if str(actor) == 'courses.PendingCourseRequests':
        #~ if allow is None: raise Exception("20130424")
    
    #~ if debug_permissions: # False:
        #~ logger.info("20130424 install debug_permissions for %s",
            #~ [elem,actor,readonly,debug_permissions,
            #~ user_level,user_groups,states,allow,owner,auth])
    
    if allow is None:
        def allow(action,user,obj,state):
            return True
    #~ if settings.SITE.user_model is not None:
    if True: # e.g. e.g. public readonly site
        if auth:
            allow_before_auth = allow
            def allow(action,user,obj,state):
                if not user.profile.authenticated:
                    #~ if action.action_name == 'wf7':
                        #~ logger.info("20130424 allow_before_auth returned False")
                    return False
                return allow_before_auth(action,user,obj,state)
            
        if user_level is not None:
            user_level = getattr(UserLevels,user_level)
            allow_user_level = allow
            def allow(action,user,obj,state):
                #~ if user.profile.level is None or user.profile.level < user_level:
                if user.profile.level < user_level:
                    #~ print 20120715, user.profile.level
                    #~ if action.action_name == 'wf7':
                        #~ logger.info("20130424 allow_user_level returned False")
                    return False
                return allow_user_level(action,user,obj,state)
                
        if owner is not None:
            allow_owner = allow
            def allow(action,user,obj,state):
                if obj is not None and (user == obj.user) != owner:
                    #~ if action.action_name == 'wf7':
                        #~ logger.info("20130424 allow_owner returned False")
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
                if not allow1(action,user,obj,state): 
                    #~ if action.action_name == 'wf7':
                        #~ logger.info("20130424 allow1 returned False")
                    return False
                for g in user_groups:
                    level = getattr(user.profile,g+'_level')
                    if level >= user_level:
                        return True
                return False
            
    if states is not None and actor.workflow_state_field is not None:
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
        #~ if debug_permissions:
            #~ logger.info("20121009 %s required states: %s",actor,states)
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
                return False
            return True
    
    if debug_permissions: # False:
        allow4 = allow
        def allow(action,user,obj,state):
            v = allow4(action,user,obj,state)
            logger.info(u"debug_permissions %r required(%s,%s,%s), allow(%s,%s,%s)--> %s",
              action,user_level,user_groups,states,user.username,obj2str(obj),state,v)
            return v
    return allow
        



class AnonymousUser(object):
    """
    Similar to Django's approach to represent anonymous visitors 
    as a special kind of user.
    """
    #~ authenticated = False
    email = None
    username = 'anonymous'
    modified = None
    partner = None
    language = None
    
    _instance = None
    
    @classmethod
    def instance(cls):
        if cls._instance is None:
            #~ cls._instance = super(AnonymousUser, cls).__new__(cls, *args, **kwargs)
            cls._instance = AnonymousUser()
            try:
                cls._instance.profile = UserProfiles.get_by_value(settings.SITE.anonymous_user_profile)
                if cls._instance.profile.authenticated:
                    raise Exception("20121121 profile specified by `anonymous_user_profile` is `authenticated`")
            except KeyError:
                raise Exception(
                    "Invalid value %r for `SITE.anonymous_user_profile`. Must be one of %s" % (
                        settings.SITE.anonymous_user_profile,
                        [i.value for i in UserProfiles.items()]))
        return cls._instance
        
    def __str__(self):
        return self.username
    


class NOT_NEEDED:
    pass
    
    
def authenticate(username,password=NOT_NEEDED):

    if not username:
        return AnonymousUser.instance()
        
    """
    20120110 : alicia hatte es geschafft, 
    beim Anmelden ein Leerzeichen vor ihren Namen zu setzen. 
    Apache ließ sie als " alicia" durch.
    Und Lino legte brav einen neuen User " alicia" an.
    """
    username = username.strip()
    
    try:
        user = settings.SITE.user_model.objects.get(username=username)
        if user.profile is None:
            #~ logger.info("20121127 user has no profile")
            return None
        if password != NOT_NEEDED:
            if not user.check_password(password):
                #~ logger.info("20121104 password mismatch")
                return None
        return user
    except settings.SITE.user_model.DoesNotExist,e:
        #~ logger.info("20121104 no username %r",username)
        return None  
    
    
class AuthMiddleWareBase(object):
    """
    Common base class for 
    :class:`RemoteUserMiddleware`,
    :class:`SessionsUserMiddleware`
    and
    :class:`NoUserMiddleware`.
    """
    def get_user_from_request(self, request):
        raise NotImplementedError
        
    def process_request(self, request):
      
        #~ print 20130313, request.session.get('username')
        
        settings.SITE.startup() 
        """
        first request will trigger site startup to load UserProfiles
        """
        
        user = self.get_user_from_request(request)
        
        self.on_login(request,user)
        
        
            
            
    def on_login(self,request,user):
        """
        The method which is applied when the user has been determined.
        On multilingual sites, 
        if URL_PARAM_USER_LANGUAGE is present it overrides user.language.
        """
        #~ logger.info("20130313 on_login(%s)" % user)
        request.user = user
        
        if len(settings.SITE.languages) > 1:
        #~ if settings.SITE.languages != None and len(settings.SITE.languages) > 1:
            
            #~ lang = settings.SITE.override_user_language() or request.user.language
            lang = user.language
            if lang:
                translation.activate(lang)
                request.LANGUAGE_CODE = translation.get_language()
                #~ logger.info("20121205 on_login %r",lang)
                
            #~ logger.info("20121205 on_login %r",translation.get_language())
            
              
        if request.method == 'GET':
            rqdata = request.GET
        elif request.method in ('PUT','DELETE'):
            rqdata = http.QueryDict(request.body) # raw_post_data before Django 1.4
        elif request.method == 'POST':
            rqdata = request.POST
        else: 
            # e.g. OPTIONS, HEAD
            request.requesting_panel = None
            request.subst_user = None
            return
        #~ else: # DELETE
            #~ request.subst_user = None
            #~ request.requesting_panel = None
            #~ return
            
        if len(settings.SITE.languages) > 1:
        #~ if settings.SITE.languages != None and len(settings.SITE.languages) > 1:
          
            ul = rqdata.get(constants.URL_PARAM_USER_LANGUAGE,None)
            if ul:
                translation.activate(ul)
                request.LANGUAGE_CODE = translation.get_language()
          
        su = rqdata.get(constants.URL_PARAM_SUBST_USER,None)
        if su is not None:
            if su:
                try:
                    su = settings.SITE.user_model.objects.get(id=int(su))
                    #~ logger.info("20120714 su is %s",su.username)
                except settings.SITE.user_model.DoesNotExist, e:
                    su = None
            else:
                su = None # e.g. when it was an empty string "su="
        request.subst_user = su
        request.requesting_panel = rqdata.get(constants.URL_PARAM_REQUESTING_PANEL,None)
        #~ logger.info("20121228 subst_user is %r",request.subst_user)
        #~ if request.subst_user is not None and not isinstance(request.subst_user,settings.SITE.user_model):
            #~ raise Exception("20121228")
        
        
            
            

            
class RemoteUserMiddleware(AuthMiddleWareBase):
    """
    Middleware which Lino automatically uses when bith
    :attr:`remote_user_header <lino.Site.remote_user_header>` 
    and :attr:`user_model <lino.Site.user_model>` are not empty.
    
    This does the same as
    `django.contrib.auth.middleware.RemoteUserMiddleware`, 
    but in a simplified manner and without using Sessions.
    
    It also activates the User's language, if that field is not empty.
    Since it will run *after*
    `django.contrib.auth.middleware.RemoteUserMiddleware`
    (at least if you didn't change :meth:`lino.Lino.get_middleware_classes`),
    it will override any browser setting.
    
    """
    
    def get_user_from_request(self, request):
        username = request.META.get(
            settings.SITE.remote_user_header,settings.SITE.default_user)
            
        if not username:
            #~ msg = "Using remote authentication, but no user credentials found."
            #~ raise exceptions.PermissionDenied(msg)
            raise Exception("Using remote authentication, but no user credentials found.")
            
        user = authenticate(username)
        
        if user is None:
            #~ logger.exception("Unknown username %s from request %s",username, request)
            #~ raise Exception(
            #~ raise exceptions.PermissionDenied("Unknown or inactive username %r. Please contact your system administrator." 
            logger.info("Unknown or inactive username %r.",username)
            raise exceptions.PermissionDenied()
              
        return user
    

class SessionUserMiddleware(AuthMiddleWareBase):
    """
    Middleware which Lino automatically uses when 
    :attr:`remote_user_header <lino.Site.remote_user_header>` is None
    and :attr:`user_model <lino.Site.user_model>` not.
    """

    def get_user_from_request(self, request):
      
        user = authenticate(request.session.get('username'),
            request.session.get('password'))
        
        if user is None:
            logger.debug("Login failed from session %s", request.session)
            user = AnonymousUser.instance()
        
        return user
        
        
class NoUserMiddleware(AuthMiddleWareBase):
    """
    Middleware which Lino automatically uses when 
    :attr:`lino.Site.user_model` is None.
    """
    def get_user_from_request(self, request):
        
        return AnonymousUser.instance()
        
        
        
