# -*- coding: UTF-8 -*-
# Copyright 2011-2015 Luc Saffre.
# License: BSD, see LICENSE for more details.
"""Core tools of Lino's permission system.

"""
from past.builtins import basestring
from builtins import object

import logging
logger = logging.getLogger(__name__)

from django.conf import settings

from lino.core.utils import obj2str

from .roles import check_required_roles
from .exceptions import ChangedAPI


class Permittable(object):
    """Base class for objects that have view permissions control.
    Inherited by :class:`lino.core.actions.Action`,
    :class:`lino.utils.jsgen.VisibleComponent` and
    :class:`lino.core.actors.Actor` (though the latter is a special
    case since actors never get instantiated).

    """

    required_roles = set()
    """A set of user roles required to view this actor or action.

    Each element of the set must be either a subclass of
    :class:`lino.core.roles.UserRole` or a tuple thereof.  An empty
    set means that the actor is visible to everybody, including
    anonymous users.

    The default value on *actors* is a set with a single element
    :class:`SiteUser <lino.core.roles.SiteUser>`, which means that the
    actor is available only for authenticated users.

    Note that this is being ignored when
    :attr:`user_profiles_module
    <lino.core.site.Site.user_profiles_module>` is empty.

    Examples of recommended ways for specifying this attribute::

       # for everybody
       required_roles = set()

       # only for office users:
       required_roles = dd.login_required(OfficeUser)

       # only for users who are BOTH OfficeUser AND SiteStaff:
       required_roles = dd.login_required(OfficeUser, SiteStaff)

       # only for users who are EITHER OfficeUser OR SiteStaff:
       required_roles = dd.login_required((OfficeUser, SiteStaff))

    """

    workflow_state_field = None
    """The name of the field that contains the workflow state of an
    object.  Subclasses may override this.

    """

    workflow_owner_field = None
    """The name of the field that contains the user who is considered to
    own an object when `Rule.owned_only` is checked.

    """

    debug_permissions = False
    """
    Whether to log :ref:`debug_permissions` for this action.
    
    """

    def add_requirements(self, *args):
        return add_requirements(self, *args)

    def get_view_permission(self, profile):
        raise NotImplementedError()


def add_requirements(obj, *args):
    """Add the specified requirements to `obj`.  `obj` can be an
    :class:`lino.core.actors.Actor` or any :class:`Permittable`.
    Application code uses this indirectly through the shortcut methods
    :meth:`lino.core.actors.Actor.add_view_requirements` or a
    :meth:`Permittable.add_requirements`.

    """
    obj.required_roles |= set(args)


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
    
    `states`

        List of strings naming the user groups for which membership is
        required.
    
    `allow`
        An additional custom permission handler
        
    `auth`
        No longer supported.
        If True, permission is given only to authenticated users.  The
        default value of this is `True` when
        :attr:`lino.core.Site.user_model` is not None, or otherwise
        `False`.
        
    `owner`
        No longer supported.
        If True, permission is given only to the author of the object.
        If False, permission is given only to users who are not the
        author of the object.  This requirement is allowed only on
        models that have a field `user` which is supposed to contain
        the author.  Usually a subclass of
        :class:`lino.modlib.users.mixins.UserAuthored`, but
        e.g. :class:`lino_xl.lib.cal.models.Guest` defines a property
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

    check_required_roles(required_roles, actor)

    if settings.SITE.user_profiles_module:
        def allow(action, profile):
            # print str(actor)
            # if str(actor.actor) == "tickets.PublicTickets":
            #     print 20150831, profile.role, required_roles
            # if action.action_name == "export_excel":
            #     print 20150828, profile.role, required_roles
            return profile.has_required_roles(required_roles)
    else:
        def allow(action, profile):
            return True

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

    check_required_roles(required_roles, actor)

    #~ if str(actor) == 'courses.PendingCourseRequests':
        #~ if allow is None: raise Exception("20130424")

    # ~ if debug_permissions: # False:
        #~ logger.info("20130424 install debug_permissions for %s",
            #~ [elem,actor,readonly,debug_permissions,
            #~ user_level,user_groups,states,allow,owner,auth])

    if allow is None:
        if settings.SITE.user_profiles_module:
            def allow(action, user, obj, state):
                # print 20150828, action, required_roles
                return user.profile.has_required_roles(required_roles)
        else:
            def allow(action, user, obj, state):
                return True

    if auth:
        raise ChangedAPI("20150718 auth no longer supported")

    if owner is not None:
        raise ChangedAPI("20150718 owner no longer supported")

    if allowed_states:
        if actor.workflow_state_field is None:
            raise Exception(
                """\
%s cannot specify `allowed_states` when %s.workflow_state_field is %r.
                """ % (elem, actor, actor.workflow_state_field))
        #~ else:
            #~ print 20120621, "ok", actor
        lst = actor.workflow_state_field.choicelist
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


