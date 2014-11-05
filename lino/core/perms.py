# Copyright 2010-2014 Luc Saffre
# License: BSD (see file COPYING for details)

from __future__ import unicode_literals

import logging
logger = logging.getLogger(__name__)

from django.conf import settings
from django.db.models.fields import NOT_PROVIDED

from lino.core import workflows
from lino.core.dbutils import obj2str

from lino.modlib.users.mixins import UserLevels, UserGroups, UserProfiles

class Requirements(object):

    """
    Not yet used. TODO: implement requirements as a class. 
    - handle conversions (like accepting both list and string for `user_groups` ),
    - implement loosen_requirements as __or__() 
    - implement add_requirements as __and__() 
    """
    user_level = None
    user_groups = None
    states = None
    allow = None
    auth = True
    owner = None


def make_permission_handler(*args, **kw):
    """Return a function that will test whether permission is given or not.
    
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

        The minimum user level required to get the permission.  The
        default value `None` means that no special user level is
        required.
        
        When `user_groups` is not specified, then the profile's
        default level (`UserProfile.level`) is being tested, otherwise
        the userlevel for the group membership.
        E.g. `dd.required(user_level='manager',user_groups='integ')`
        will pass when `profile.level` is "user" and
        `profile.integ_level` is "manager"
        
        
    `user_groups`

        List of strings naming the user groups for which membership is
        required to get permission to view this Actor.  The default
        value `None` means that no special group membership is
        required.  Alternatively, if this is a string, it will be
        converted to a list of strings.
        
    `states`
        List of strings naming the user groups for which membership is required 
    
    `allow`
        An additional custom permission handler
        
    `auth`
        If True, permission is given for any authenticated user 
        (and not for :class:`AnonymousUser`).
        
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
    return make_permission_handler_(*args, **kw)
    #~ except Exception,e:
        #~ raise Exception("Exception while making permissions for %s: %s" % (actor,e))


def make_view_permission_handler(*args, **kw):
    """
    Similar to :func:`make_permission_handler`, but for static view permissions 
    which don't have an object nor states.
    """
    return make_view_permission_handler_(*args, **kw)


def make_view_permission_handler_(
        actor, readonly, debug_permissions,
        user_level=None, user_groups=None,
        allow=None, auth=False, owner=None, states=None):
    #~ if states is not None:
        #~ logger.info("20121121 ignoring required states %s for %s",states,actor)
    #~ if owner is not None:
        #~ logger.info("20121121 ignoring required owner %s for %s",owner,actor)
    #~ if allow is None:
    if allow is not None:
        if not isinstance(actor.action, workflows.ChangeStateAction):
            raise Exception("20130724 %s" % actor)
    if True:
        # ignore `allow` requirement for view_permission because
        # workflows.Choice.add_transition
        def allow(action, profile):
            return True
    # if settings.SITE.user_model is not None:
    if True:  # e.g. public readonly site
        if auth:
            allow_before_auth = allow

            def allow(action, profile):
                if not profile.authenticated:
                    return False
                return allow_before_auth(action, profile)

        if user_groups is not None:
            if isinstance(user_groups, basestring):
                user_groups = user_groups.split()
            if user_level is None:
                user_level = UserLevels.user
            else:
                user_level = getattr(UserLevels, user_level, None)
                if user_level is None:
                    raise Exception("Invalid user_level %r for %s" %
                                    (user_level, actor))
            for g in user_groups:
                # raise Exception if no such group exists
                UserGroups.get_by_value(g)
                #~ if not UserGroups.get_by_name(g):
                    #~ raise Exception("Invalid UserGroup %r" % g)
            allow1 = allow

            def allow(action, profile):
                if not allow1(action, profile):
                    return False
                for g in user_groups:
                    level = getattr(profile, g + '_level', NOT_PROVIDED)
                    if level is NOT_PROVIDED:
                        # We need to report the guilty actor,
                        # otherwise it is difficult to locate the error.
                        raise Exception(
                            "user_group '%s' required by %s does not exist" %
                            (g, actor))
                        return False
                    if level >= user_level:
                        return True
                    #~ elif debug_permissions:
                        #~ logger.info("20130704 level %r < %r",level,user_level)
                return False

        elif user_level is not None:
            user_level = getattr(UserLevels, user_level)
            allow_user_level = allow

            def allow(action, profile):
                if profile.level < user_level:
                    return False
                return allow_user_level(action, profile)

    if not readonly:
        allow3 = allow

        def allow(action, profile):
            if not allow3(action, profile):
                return False
            if profile.readonly:
                return False
            return True

    if debug_permissions:  # False:
        #~ logger.info("20130424 install debug_permissions for %s",
            #~ [actor,readonly,debug_permissions,
            #~ user_level,user_groups,allow,auth,owner,states])
        allow4 = allow

        def allow(action, profile):
            v = allow4(action, profile)
            if True:  # not v:
                logger.info(
                    u"debug_permissions (view) %r required(%s,%s), allow(%s)--> %s",
                    action, user_level, user_groups, profile, v)
            return v
    return allow


def make_permission_handler_(
    elem, actor, readonly, debug_permissions,
        user_level=None, user_groups=None,
        allow=None, auth=False, owner=None, states=None):

    #~ if str(actor) == 'courses.PendingCourseRequests':
        #~ if allow is None: raise Exception("20130424")

    # ~ if debug_permissions: # False:
        #~ logger.info("20130424 install debug_permissions for %s",
            #~ [elem,actor,readonly,debug_permissions,
            #~ user_level,user_groups,states,allow,owner,auth])

    if allow is None:
        def allow(action, user, obj, state):
            return True
    # if settings.SITE.user_model is not None:
    if True:  # e.g. public readonly site
        if auth:
            allow_before_auth = allow

            def allow(action, user, obj, state):
                if not user.profile.authenticated:
                    #~ if action.action_name == 'wf7':
                        #~ logger.info("20130424 allow_before_auth returned False")
                    return False
                return allow_before_auth(action, user, obj, state)

        if owner is not None:
            allow_owner = allow

            def allow(action, user, obj, state):
                if obj is not None and (user == obj.user) != owner:
                    #~ if action.action_name == 'wf7':
                        #~ logger.info("20130424 allow_owner returned False")
                    return False
                return allow_owner(action, user, obj, state)

        if user_groups is not None:
            if isinstance(user_groups, basestring):
                user_groups = user_groups.split()
            if user_level is None:
                user_level = UserLevels.user
            else:
                user_level = getattr(UserLevels, user_level)
            for g in user_groups:
                # raise Exception if no such group exists
                UserGroups.get_by_value(g)
                #~ if not UserGroups.get_by_name(g):
                    #~ raise Exception("Invalid UserGroup %r" % g)
            allow1 = allow

            def allow(action, user, obj, state):
                if not allow1(action, user, obj, state):
                    #~ if action.action_name == 'wf7':
                        #~ logger.info("20130424 allow1 returned False")
                    return False
                for g in user_groups:
                    level = getattr(user.profile, g + '_level')
                    if level >= user_level:
                        return True
                return False

        elif user_level is not None:
            user_level = getattr(UserLevels, user_level)
            allow_user_level = allow

            def allow(action, user, obj, state):
                #~ if user.profile.level is None or user.profile.level < user_level:
                if user.profile.level < user_level:
                    #~ print 20120715, user.profile.level
                    #~ if action.action_name == 'wf7':
                        #~ logger.info("20130424 allow_user_level returned False")
                    return False
                return allow_user_level(action, user, obj, state)

    if states is not None:
        #~ if not isinstance(actor.workflow_state_field,choicelists.ChoiceListField):
        if actor.workflow_state_field is None:
            raise Exception(
                """\
%s cannot specify `states` when %s.workflow_state_field is %r.
                """ % (elem, actor, actor.workflow_state_field))
        #~ else:
            #~ print 20120621, "ok", actor
        lst = actor.workflow_state_field.choicelist
        #~ states = frozenset([getattr(lst,n) for n in states])
        #~ possible_states = [st.name for st in lst.items()] + [BLANK_STATE]
        ns = []
        if isinstance(states, basestring):
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

        def allow(action, user, obj, state):
            if not allow2(action, user, obj, state):
                return False
            if obj is None:
                return True
            return state in states
    #~ return perms.Permission(allow)

    if not readonly:
        allow3 = allow

        def allow(action, user, obj, state):
            if not allow3(action, user, obj, state):
                return False
            if user.profile.readonly:
                return False
            return True

    if debug_permissions:  # False:
        allow4 = allow

        def allow(action, user, obj, state):
            v = allow4(action, user, obj, state)
            logger.info(
                u"debug_permissions %r required(%s,%s,%s), allow(%s,%s,%s)--> %s",
                action, user_level, user_groups, states, user.username, obj2str(obj), state, v)
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
    #~ id = None
    pk = None

    _instance = None

    @classmethod
    def instance(cls):
        if cls._instance is None:
            #~ cls._instance = super(AnonymousUser, cls).__new__(cls, *args, **kwargs)
            cls._instance = AnonymousUser()
            try:
                cls._instance.profile = UserProfiles.get_by_value(
                    settings.SITE.anonymous_user_profile)
                
                # if cls._instance.profile.authenticated:
                #     logger.warning(
                #         "20121121 profile specified by \
                #         `anonymous_user_profile` is `authenticated`")
            except KeyError:
                raise Exception(
                    "Invalid value %r for `SITE.anonymous_user_profile`. Must be one of %s" % (
                        settings.SITE.anonymous_user_profile,
                        [i.value for i in UserProfiles.items()]))
        return cls._instance

    def __str__(self):
        return self.username

    def get_typed_instance(self, model):
        # 20131022 AttributeError at /api/outbox/MyOutbox : 'AnonymousUser'
        # object has no attribute 'get_typed_instance'
        return self
