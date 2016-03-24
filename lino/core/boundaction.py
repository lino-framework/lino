# -*- coding: UTF-8 -*-
# Copyright 2009-2016 Luc Saffre
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
from lino.core import actions

from lino.core.permissions import (
    make_permission_handler, make_view_permission_handler)


class BoundAction(object):

    """An Action which is bound to an Actor.  If an Actor has subclasses,
    each subclass "inherits" its actions.

    """

    def __init__(self, actor, action):

        if not isinstance(action, actions.Action):
            raise Exception("%s : %r is not an Action" % (actor, action))
        self.action = action
        self.actor = actor

        required = set(actor.required_roles)
        # required = set()
        # required |= actor.required_roles
        required |= action.required_roles

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
            debug_permissions, required,
            allowed_states=action.required_states), action)
        #~ if debug_permissions:
            #~ logger.info("20130424 _allow is %s",self._allow)
        #~ actor.actions.define(a.action_name,ba)

    def get_window_layout(self):
        return self.action.get_window_layout(self.actor)

    def get_window_size(self):
        return self.action.get_window_size(self.actor)

    def full_name(self):
        return self.action.full_name(self.actor)

    def request(self, *args, **kw):
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
        "<lino.modlib.users.utils.AnonymousUser object at
        0x7f562512f210>": "Upload.user" must be a "User" instance`
        when called by anonymous.

        """
        if not self._allow(ar.get_user(), obj, state):
            return False
        return self.action.get_action_permission(ar, obj, state)
        # if not self.action.get_action_permission(ar, obj, state):
        #     return False
        # return self._allow(ar.get_user(), obj, state)

    def get_view_permission(self, profile):
        """
        Return True if this bound action is visible for users of this
        profile.
        """
        if not self.actor.get_view_permission(profile):
            return False
        if not self.action.get_view_permission(profile):
            return False
        return self.allow_view(profile)

    def __repr__(self):
        return "<%s(%s, %r)>" % (
            self.__class__.__name__, self.actor, self.action)


