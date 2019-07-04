# -*- coding: UTF-8 -*-
# Copyright 2010-2018 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)
"""
This defines the :class:`Registable` model mixin.
"""

from __future__ import unicode_literals

from django.db import models

from lino.core import model
from lino.core.workflows import ChangeStateAction
from lino.core.exceptions import ChangedAPI



from lino.core.workflows import State

class RegistrableState(State):
    """
    Base class 
    """
    is_editable = True
    """
    Whether the registrable object having this state should be
    editable or not.
    """



class Registrable(model.Model):

    """
    Base class to anything that may be "registered" and "deregistered"
    (e.g. Invoices, Vouchers, Declarations, Reservations,...).
    "Registered" means "this object has been taken account of".
    Registered objects are not editable.

    .. attribute:: state

        The ChoiceList of this  field must have at least two items
        named "draft" and "registered".
        There may be additional states.
        Every state must have an extra attribute "is_editable".

    """
    class Meta(object):
        abstract = True

    workflow_state_field = 'state'

    _registrable_fields = None

    @classmethod
    def on_analyze(cls, site):
        super(Registrable, cls).on_analyze(site)
        chl = cls.workflow_state_field.choicelist
        ic = chl.item_class
        k = 'is_editable'
        if not hasattr(ic, k):
            fld = getattr(chl, k, None)
            if not isinstance(fld, models.BooleanField):
                raise ChangedAPI(
                    "The workflow state field for {} uses {} which "
                    "has no attribute {}".format(cls, ic, k))
        cls._registrable_fields = set(cls.get_registrable_fields(site))


    @classmethod
    def get_registrable_fields(cls, site):
        """
        Return a list of the fields which are *disabled* when this is
        *registered* (i.e. `state` is not `editable`).

        Usage example::

            class MyModel(dd.Registrable):

                @classmethod
                def get_registrable_fields(self, site):
                    for f in super(MyModel, self).get_registrable_fields(site):
                        yield f
                    yield 'user'
                    yield 'date'
        """
        return []
        # yield 'date'

    def disabled_fields(self, ar):
        if not self.state.is_editable:
            return self._registrable_fields
        return super(Registrable, self).disabled_fields(ar)

    def get_row_permission(self, ar, state, ba):
        """Only rows in an editable state may be edited.

        Note that `ba` is the action being requested while
        `ar.bound_action` is the action from which the request was
        started.

        """
        if state and not state.is_editable and not isinstance(
                ba.action, ChangeStateAction):
            # if not ar.bound_action.action.readonly:
            if not ba.action.readonly:
                return False
        return super(Registrable, self).get_row_permission(ar, state, ba)

    def register(self, ar):
        """
        Register this object.  The base implementation just sets the state
        to "registered".

        Subclasses may override this to add custom behaviour.  Instead
        of subclassing you can also override :meth:`set_workflow_state
        <lino.core.model.Model.set_workflow_state>`,
        :meth:`before_state_change
        <lino.core.model.Model.before_state_change>` or
        :meth:`after_state_change
        <lino.core.model.Model.after_state_change>`.
        """

        # state_field = self._meta.get_field(self.workflow_state_field)
        state_field = self.workflow_state_field
        target_state = state_field.choicelist.registered
        self.set_workflow_state(ar, state_field, target_state)

    def deregister(self, ar):
        """
        Deregister this object.  The base implementation just sets the
        state to "draft".

        Subclasses may override this to add custom behaviour.  Instead
        of subclassing you can also override :meth:`set_workflow_state
        <lino.core.model.Model.set_workflow_state>`,
        :meth:`before_state_change
        <lino.core.model.Model.before_state_change>` or
        :meth:`after_state_change
        <lino.core.model.Model.after_state_change>`.
        """

        # state_field = self._meta.get_field(self.workflow_state_field)
        state_field = self.workflow_state_field
        target_state = state_field.choicelist.draft
        self.set_workflow_state(ar, state_field, target_state)

    # no longer needed after 20170826
    # @classmethod
    # def setup_parameters(cls, **fields):
    #     wsf = cls.workflow_state_field
    #     fields[wsf.name] = wsf.choicelist.field(blank=True, null=True)
    #     return super(Registrable, cls).setup_parameters(**fields)

    @classmethod
    def get_simple_parameters(cls):
        for p in super(Registrable, cls).get_simple_parameters():
            yield p
        yield cls.workflow_state_field.name


    def on_duplicate(self, ar, master):
        self.state = self.workflow_state_field.choicelist.draft
        super(Registrable, self).on_duplicate(ar, master)

