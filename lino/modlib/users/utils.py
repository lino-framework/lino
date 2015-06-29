# Copyright 2011-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""Utilities for :mod:`lino.modlib.users`.

.. autosummary::

"""
from __future__ import unicode_literals

import logging
logger = logging.getLogger(__name__)

from django.conf import settings

from lino.core import workflows
from lino.core.utils import obj2str

from .choicelists import UserProfiles


def make_permission_handler(*args, **kw):
    """Return a function that will test whether permission is given or not.
    
    `elem` is not used (either an Action or a Permittable.)
    
    `actor` is who contains the workflow state field
    
    `readonly`
    
    `debug_permissions`
    
    The generated function will always expect three arguments user,
    obj and state.  The latter two may be None depending on the
    context (for example a read_required is expected to not test on
    obj or state because these values are not known when generating
    the :xfile:`lino*.js` files.).
    
    The remaining keyword arguments are aka "requirements":
    
    `user_level`

        A string (e.g. ``'manager'``, ``'user'``,...)

        The minimum user level required to get the permission.  The
        default value `None` means that no special user level is
        required.
        
        When `user_groups` is not specified, then the profile's
        default level (`UserProfile.level`) is being tested, otherwise
        the userlevel for the group membership.
        E.g. `dd.required(user_level='manager', user_groups='integ')`
        will pass when `profile.level` is "user" and
        `profile.integ_level` is "manager"
        
        
    `user_groups`

        List of strings naming the user groups for which membership is
        required to get permission to view this Actor.  The default
        value `None` means that no special group membership is
        required.  Alternatively, if this is a string, it will be
        converted to a list of strings.  Specifying more than one user
        groups means that only one of them is required.
        
    `states`

        List of strings naming the user groups for which membership is
        required.
    
    `allow`
        An additional custom permission handler
        
    `auth`

        If True, permission is given only to authenticated users.  The
        default value of this is `True` when
        :attr:`lino.core.Site.user_model` is not None, or otherwise
        `False`.
        
    `owner`

        If True, permission is given only to the author of the object.
        If False, permission is given only to users who are not the
        author of the object.  This requirement is allowed only on
        models that have a field `user` which is supposed to contain
        the author.  Usually a subclass of
        :class:`lino.modlib.users.mixins.UserAuthored`, but
        e.g. :class:`lino.modlib.cal.models.Guest` defines a property
        `user` because it has no own `user` field).

    """
    # try:
    return make_permission_handler_(*args, **kw)
    # except Exception,e:
        # raise Exception("Exception while making permission handler "
        # "for %s: %s" % (actor,e))


def make_view_permission_handler(*args, **kw):
    """Similar to :func:`make_permission_handler`, but for static view
    permissions which don't have an object nor states.

    """
    # try:
    return make_view_permission_handler_(*args, **kw)
    # except Exception,e:
        # raise Exception("Exception while making view permission handler "
        # "for %s: %s" % (actor,e))


def make_view_permission_handler_(
        actor, readonly, debug_permissions, required_roles):

        # user_level=None, user_groups=None,
        # allow=None, auth=False, owner=None, states=None):

    if settings.SITE.disable_user_roles or settings.SITE.user_model is None:
        def allow(action, profile):
            return True
    else:
        def allow(action, profile):
            return profile.has_required_role(required_roles)

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
                    u"debug_permissions (view) %r "
                    "required(%s), allow(%s)--> %s",
                    action, action.required_roles, profile, v)
            return v
    return allow


def make_permission_handler_(
    elem, actor, readonly, debug_permissions, required_roles,
        allow=None, auth=False, owner=None, allowed_states=None):

    #~ if str(actor) == 'courses.PendingCourseRequests':
        #~ if allow is None: raise Exception("20130424")

    # ~ if debug_permissions: # False:
        #~ logger.info("20130424 install debug_permissions for %s",
            #~ [elem,actor,readonly,debug_permissions,
            #~ user_level,user_groups,states,allow,owner,auth])

    if allow is None:
        if settings.SITE.disable_user_roles or \
           settings.SITE.user_model is None:
            def allow(action, user, obj, state):
                return True
        else:
            def allow(action, user, obj, state):
                return user.profile.has_required_role(required_roles)

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

    if allowed_states:
        #~ if not isinstance(actor.workflow_state_field,choicelists.ChoiceListField):
        if actor.workflow_state_field is None:
            raise Exception(
                """\
%s cannot specify `allowed_states` when %s.workflow_state_field is %r.
                """ % (elem, actor, actor.workflow_state_field))
        #~ else:
            #~ print 20120621, "ok", actor
        lst = actor.workflow_state_field.choicelist
        #~ states = frozenset([getattr(lst,n) for n in states])
        #~ possible_states = [st.name for st in lst.items()] + [BLANK_STATE]
        ns = []
        if isinstance(allowed_states, basestring):
            allowed_states = allowed_states.split()
        for n in allowed_states:
            if n is not None:
                if n == '_':
                    n = None
                else:
                    n = lst.get_by_name(n)
            ns.append(n)
        allowed_states = frozenset(ns)
        allow2 = allow

        def allow(action, user, obj, state):
            if not allow2(action, user, obj, state):
                return False
            if obj is None:
                return True
            return state in allowed_states

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
                u"debug_permissions %r required(%s, %s), "
                "allow(%s, %s, %s) --> %s",
                action, required_roles,
                allowed_states, user.username, obj2str(obj), state, v)
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
            # Call startup() to fill UserProfiles also in a
            # multi-threaded environment:
            settings.SITE.startup()
            cls._instance = AnonymousUser()
            cls._instance.profile = UserProfiles.get_by_value(
                settings.SITE.anonymous_user_profile, None)
            if cls._instance.profile is None:
                raise Exception(
                    "Invalid value %r for `SITE.anonymous_user_profile`. "
                    "Must be one of %s" % (
                        settings.SITE.anonymous_user_profile,
                        [i.value for i in UserProfiles.items()]))
        return cls._instance

    def __str__(self):
        return self.username

    def get_typed_instance(self, model):
        # 20131022 AttributeError at /api/outbox/MyOutbox : 'AnonymousUser'
        # object has no attribute 'get_typed_instance'
        return self

