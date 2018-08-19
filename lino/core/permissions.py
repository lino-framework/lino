# -*- coding: UTF-8 -*-
# Copyright 2011-2018 Rumma & Ko Ltd
# License: BSD, see LICENSE for more details.
"""Core tools of Lino's permission system.

"""
import six
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
    :attr:`user_types_module
    <lino.core.site.Site.user_types_module>` is empty.

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

    def get_view_permission(self, user_type):
        return True


def add_requirements(obj, *args):
    """
    Add the specified requirements to `obj`.  `obj` can be an
    :class:`lino.core.actors.Actor` or any :class:`Permittable`.
    Application code uses this indirectly through the shortcut methods
    :meth:`lino.core.actors.Actor.add_view_requirements` or a
    :meth:`Permittable.add_requirements`.
    """
    obj.required_roles |= set(args)


def make_permission_handler(*args, **kw):
    """
    Return a function that will test whether permission is given or
    not.
    
    `elem` is not used (either an Action or a Permittable.)
    
    `actor` is who contains the workflow state field
    
    `readonly`
    
    `debug_permissions`
    
    The generated function will always expect three arguments user,
    obj and state.  The latter two may be None depending on the
    context (for example a read_required is expected to not test on
    obj or state because these values are not known when generating
    the :xfile:`linoweb.js` files.).
    
    The remaining keyword arguments are aka "requirements":
    
    `states`

        List of strings naming the user groups for which membership is
        required.
    
    `allow`

        An additional custom permission handler
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

    if settings.SITE.user_types_module:
        def allow(action, user_type):
            v = user_type.has_required_roles(required_roles)
            return v
        
        if not readonly:
            allow3 = allow

            def allow(action, user_type):
                if not allow3(action, user_type):
                    return False
                if user_type.readonly:
                    return False
                return True

    else:
        def allow(action, user_type):
            return True

    if debug_permissions:  # False:
        allow4 = allow

        def allow(action, user_type):
            v = allow4(action, user_type)
            if True:  # not v:
                logger.info(
                    u"debug_permissions (view) %r "
                    "required(%s), allow(%s)--> %s",
                    action, action.required_roles, user_type, v)
            return v
    return allow


def make_permission_handler_(
    elem, actor, readonly, debug_permissions, required_roles,
        allow=None, auth=False, owner=None):

    check_required_roles(required_roles, actor)

    if allow is None:
        if settings.SITE.user_types_module:
            def allow(action, user, obj, state):
                # print 20150828, action, required_roles
                return user.user_type.has_required_roles(required_roles)
        else:
            def allow(action, user, obj, state):
                return True

    if auth:
        raise ChangedAPI("20150718 auth no longer supported")

    if owner is not None:
        raise ChangedAPI("20150718 owner no longer supported")

    if settings.SITE.user_types_module and not readonly:
        allow3 = allow

        def allow(action, user, obj, state):
            if not allow3(action, user, obj, state):
                return False
            if user.user_type.readonly:
                return False
            return True

    if debug_permissions:
        allow4 = allow

        def allow(action, user, obj, state):
            v = allow4(action, user, obj, state)
            logger.info(
                u"debug_permissions %r required(%s), "
                "allow(%s, %s, %s) --> %s",
                action, required_roles,
                user.username, obj2str(obj), state, v)
            return v
    return allow

