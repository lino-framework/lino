# -*- coding: UTF-8 -*-
# Copyright 2009-2014 Luc Saffre
# License: BSD (see file COPYING for details)

import logging
logger = logging.getLogger(__name__)

from django.conf import settings

from lino.utils import curry
from lino.core import actions


class BoundAction(object):

    """An Action which is bound to an Actor.  If an Actor has subclasses,
    each subclass "inherits" its actions.

    """

    def __init__(self, actor, action):

        if not isinstance(action, actions.Action):
            raise Exception("%s : %r is not an Action" % (actor, action))
        self.action = action
        self.actor = actor

        required = dict()
        if action.readonly:
            required.update(actor.required)
        #~ elif isinstance(action,InsertRow):
            #~ required.update(actor.create_required)
        elif isinstance(action, actions.DeleteSelected):
            required.update(actor.delete_required)
        else:
            required.update(actor.update_required)
        required.update(action.required)
        #~ print 20120628, str(a), required
        #~ def wrap(a,required,fn):
            #~ return fn

        debug_permissions = actor.debug_permissions and \
            action.debug_permissions

        if debug_permissions:
            if settings.DEBUG:
                logger.info("debug_permissions active for %r (required=%s)",
                            self, required)
            else:
                raise Exception(
                    "settings.DEBUG is False, but `debug_permissions` "
                    "for %r (required=%s) is active." % (self, required))

        from lino.modlib.users.mixins import (
            make_permission_handler, make_view_permission_handler)
        self.allow_view = curry(make_view_permission_handler(
            self, action.readonly, debug_permissions, **required), action)
        self._allow = curry(make_permission_handler(
            action, actor, action.readonly,
            debug_permissions, **required), action)
        #~ if debug_permissions:
            #~ logger.info("20130424 _allow is %s",self._allow)
        #~ actor.actions.define(a.action_name,ba)

    def get_window_layout(self):
        return self.action.get_window_layout(self.actor)

    def get_window_size(self):
        return self.action.get_window_size(self.actor)

    def full_name(self):
        return self.action.full_name(self.actor)
        #~ if self.action.action_name is None:
            #~ raise Exception("%r action_name is None" % self.action)
        #~ return str(self.actor) + '.' + self.action.action_name

    def request(self, *args, **kw):
        kw.update(action=self)
        return self.actor.request(*args, **kw)

    def get_button_label(self, *args):
        return self.action.get_button_label(self.actor, *args)

    #~ def get_panel_btn_handler(self,*args):
        #~ return self.action.get_panel_btn_handler(self.actor,*args)

    def setup_action_request(self, *args):
        return self.action.setup_action_request(self.actor, *args)

    def get_row_permission(self, ar, obj, state):
        #~ if self.actor is None: return False
        return self.actor.get_row_permission(obj, ar, state, self)

    def get_bound_action_permission(self, ar, obj, state):
        if not self.action.get_action_permission(ar, obj, state):
            return False
        return self._allow(ar.get_user(), obj, state)

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
        return "<%s(%s,%r)>" % (
            self.__class__.__name__, self.actor, self.action)


