# Copyright 2010-2014 Luc Saffre
# License: BSD (see file COPYING for details)
"""This defines some helper classes like 

- :class:`Parametrizable` and :class:`Permittable` ("mixins" with
  common functionality for both actors and actions),
- the volatile :class:`InstanceAction` object
- the :class:`ParameterPanel` class (used
  e.g. by :class:`lino.mixins.periods.ObservedPeriod`)

TODO: Merge this module and :mod:`lino.core.dbutils`.

"""

from __future__ import unicode_literals

from django.conf import settings
from lino.utils.xmlgen.html import E


class Parametrizable(object):
    """Base class for both Actors and Actions.


    .. method:: FOO_choices

        For every parameter field named "FOO", if the action has a method
        called "FOO_choices" (which must be decorated by
        :func:`dd.chooser`), then this method will be installed as a
        chooser for this parameter field.


    """

    active_fields = None  # 20121006
    master_field = None

    parameters = None
    """
    User-definable parameter fields for this actor or action.
    Set this to a `dict` of `name = models.XyzField()` pairs.

    TODO: write documentation.
    """

    params_layout = None
    """
    The layout to be used for the parameter panel.
    If this table or action has parameters, specify here how they
    should be laid out in the parameters panel.
    """

    params_panel_hidden = False
    """
    If this table has parameters, set this to True if the parameters
    panel should be initially hidden when this table is being
    displayed.

    """

    _layout_class = NotImplementedError

    def get_window_layout(self, actor):
        return self.params_layout

    def get_window_size(self, actor):
        wl = self.get_window_layout(actor)
        if wl is not None:
            return wl.window_size


class Permittable(object):

    """Base class for objects that have view permissions control.

    :class:`lino.core.actors.Actor` would be a subclass, but is a
    special case since actors never get instantiated.

    """

    required = {}
    """
    The permissions required to view this actor.
    A dict with permission requirements.
    See :func:`lino.core.perms.make_permission_handler`.
    """

    # internally needed for make_permission_handler
    workflow_state_field = None
    # internally needed for make_permission_handler
    workflow_owner_field = None
    #~ readonly = True

    debug_permissions = False
    """
    Whether to log :ref:`debug_permissions` for this action.
    
    """

    def add_requirements(self, **kw):
        return add_requirements(self, **kw)

    def get_view_permission(self, profile):
        raise NotImplementedError()


def add_requirements(obj, **kw):
    """
    Add the specified requirements to `obj`.
    `obj` can be an 
    :class:`lino.core.actors.Actor` or any 
    :class:`lino.core.actions.Permittable`.
    Application code uses this indirectly through the shortcut methods
    :meth:`lino.core.actors.Actor.add_view_requirements` or a 
    :meth:`lino.core.actions.Permittable.add_requirements`.
    
    """
    #~ logger.info("20120927 perms.set_required %r",kw)
    new = dict()
    #~ new.update(getattr(obj,'required',{}))
    new.update(obj.required)
    new.update(kw)
    obj.required = new


class InstanceAction(object):
    """Volatile object which wraps a given action to be run on a given
    model instance.

    """

    def __init__(self, action, actor, instance, owner):
        #~ print "Bar"
        #~ self.action = action
        self.bound_action = actor.get_action_by_name(action.action_name)
        if self.bound_action is None:
            raise Exception("%s has not action %r" % (actor, action))
            # Happened 20131020 from lino.modlib.beid.eid_info() :
            # When `use_eid_jslib` was False, then
            # `Action.attach_to_actor` returned False.
        self.instance = instance
        self.owner = owner

    def run_from_code(self, ar, **kw):
        ar.selected_rows = [self.instance]
        return self.bound_action.action.run_from_code(ar)

    def run_from_ui(self, ar, **kw):
        ar.selected_rows = [self.instance]
        self.bound_action.action.run_from_ui(ar)

    def run_from_session(self, ses, **kw):
        #~ print self,args, kw
        ar = self.bound_action.request(**kw)
        ar.setup_from(ses)
        ar.selected_rows = [self.instance]
        self.bound_action.action.run_from_code(ar)
        return ar.response

    def __call__(self, *args, **kwargs):
        return self.run_from_session(*args, **kwargs)

    def as_button_elem(self, ar, label=None, **kwargs):
        return settings.SITE.ui.row_action_button(
            self.instance, ar, self.bound_action, label, **kwargs)

    def as_button(self, *args, **kwargs):
        """Return a HTML chunk with a "button" which, when clicked, will
        execute this action on this instance.  This is being used in
        the :ref:`lino.tutorial.polls`.

        """
        return E.tostring(self.as_button_elem(*args, **kwargs))


class ParameterPanel(object):
    """A utility class for defining reusable definitions for
    :attr:`parameters <lino.core.actors.Actor.parameters>`.

    """
    def __init__(self, **kw):
        self.fields = kw

    def values(self, *args, **kw):
        return self.fields.values(*args, **kw)

    def keys(self, *args, **kw):
        return self.fields.keys(*args, **kw)

    def __iter__(self, *args, **kw):
        return self.fields.__iter__(*args, **kw)

    def __len__(self, *args, **kw):
        return self.fields.__len__(*args, **kw)

    def __getitem__(self, *args, **kw):
        return self.fields.__getitem__(*args, **kw)

    def get(self, *args, **kw):
        return self.fields.get(*args, **kw)

    def items(self, *args, **kw):
        return self.fields.items(*args, **kw)


class Requirements(object):

    """Not yet used. TODO: implement requirements as a class.

    - handle conversions (like accepting both list and string for
      `user_groups` )
    - implement loosen_requirements as __or__()
    - implement add_requirements as __and__()

    """
    user_level = None
    user_groups = None
    states = None
    allow = None
    auth = True
    owner = None


