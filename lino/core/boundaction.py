# -*- coding: UTF-8 -*-
# Copyright 2009-2018 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)
"""
.. autosummary::

"""
from builtins import object

import logging
logger = logging.getLogger(__name__)

import os

from django.conf import settings

from lino.utils import curry
# from .actions import Action

from lino.core.permissions import (
    make_permission_handler, make_view_permission_handler)


class BoundAction(object):

    """An Action which is bound to an Actor.  If an Actor has subclasses,
    each subclass "inherits" its actions.

    """

    def __init__(self, actor, action):
        # the following test would require us to import Action, which
        # would trigger a circular import Action -> BoundAction ->
        # BaseRequest -> InstanceAction -> Action
        # if not isinstance(action, Action):
        #     raise Exception("%s : %r is not an Action" % (actor, action))
        self.action = action
        self.actor = actor

        # take care of not accidentally modifying ther actor's
        # requirements!
        required = set(action.get_required_roles(actor))
        # required = set(actor.required_roles)
        # if action.defining_actor is None:
        #     required = set(actor.required_roles)
        # else:
        #     required = set(action.defining_actor.required_roles)
        # required = set()
        # required |= actor.required_roles
        required |= action.required_roles
        
        if True:  # 20170902 useful when debugging permission problems
            self.required = required  

        debug_permissions = actor.debug_permissions and \
            action.debug_permissions

        if debug_permissions:
            if settings.DEBUG:
                logger.info("debug_permissions active for %r (required=%s)",
                            self, required)
            else:
                raise Exception(
                    "settings.DEBUG is False, but `debug_permissions` "
                    "for %r (required=%s) is active (settings=%s)." % (
                        self, required, os.environ['DJANGO_SETTINGS_MODULE']))

        self.allow_view = curry(make_view_permission_handler(
            self, action.readonly, debug_permissions, required), action)
        self._allow = curry(make_permission_handler(
            action, actor, action.readonly,
            debug_permissions, required), action)
            # allowed_states=action.required_states), action)
        #~ if debug_permissions:
            #~ logger.info("20130424 _allow is %s",self._allow)
        #~ actor.actions.define(a.action_name,ba)

    def get_window_layout(self):
        return self.action.get_window_layout(self.actor)

    def get_layout_handel(self):
        layout = self.get_window_layout()
        return layout.get_layout_handle() if layout is not None else None

    def get_window_size(self):
        return self.action.get_window_size(self.actor)

    def full_name(self):
        return self.action.full_name(self.actor)

    def request(self, *args, **kw):
        # print("20170116 BoundAction.request()", args, kw)
        kw.update(action=self)
        return self.actor.request(*args, **kw)

    def request_from(self, ar, *args, **kw):
        """Create a request of this action from parent request `ar`.

        """
        kw.update(parent=ar)
        return self.request(*args, **kw)

    def run_from_session(self, ses, **kw):
        ar = self.request_from(ses, **kw)
        self.action.run_from_code(ar)
        return ar.response

    def get_button_label(self, *args):
        return self.action.get_button_label(self.actor, *args)

    #~ def get_panel_btn_handler(self,*args):
        #~ return self.action.get_panel_btn_handler(self.actor,*args)

    def setup_action_request(self, *args):
        return self.action.setup_action_request(self.actor, *args)

    def get_row_permission(self, ar, obj, state):
        """Checks whether this bound action has permission to run on the given
        database object.
        
        This will check requirements specified on the *actor*, which
        by default checks those defined on the *model*, which in turn
        checks those defined on the *action* by calling
        :meth:`get_bound_action_permission`.

        """
        #~ if self.actor is None: return False
        return self.actor.get_row_permission(obj, ar, state, self)

    def get_bound_action_permission(self, ar, obj, state):
        """Checks whether the bound action gives permission to run.

        If this is a list action, `obj` is None.  If this is a row
        action, then `obj` is the current row.  Note that this method
        does not (again) call any custom permission handler defined on
        the model.

        This is done in two steps: first we check the requirements
        specified in `required_roles` and `required_states`, then (if
        these pass) we check any custom permissions defined on the
        action via :meth:`get_action_permission
        <lino.core.actions.Action.get_action_permission>`.

        The order of these is important since a custom permission
        handler of an action with default `required_roles` can make
        database queries based on `ar.get_user()`, which would cause
        errors like :message:`Cannot assign
        "<lino.core.auth.utils.AnonymousUser object at
        0x7f562512f210>": "Upload.user" must be a "User" instance`
        when called by anonymous.

        """
        u = ar.get_user()
        if not self.action.get_view_permission(u.user_type):
            return False
        if not self._allow(u, obj, state):
            return False
        if not self.action.get_action_permission(ar, obj, state):
            return False
        return True
        # return self._allow(ar.get_user(), obj, state)

    def get_view_permission(self, user_type):
        """
        Return True if this bound action is visible for users of this
        user_type.
        """
        if not self.actor.get_view_permission(user_type):
            return False
        # # 20170902
        # if self.action.defining_actor is None:
        #     if not self.actor.get_view_permission(user_type):
        #         return False
        # elif not self.action.defining_actor.get_view_permission(user_type):
        #     return False
        if not self.action.get_view_permission(user_type):
            return False
        return self.allow_view(user_type)

    def __repr__(self):
        return "<%s(%s, %r)>" % (
            self.__class__.__name__, self.actor, self.action)


