# -*- coding: UTF-8 -*-
# Copyright 2010-2020 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)
"""
This defines the :class:`Registable` model mixin.
"""

from django.db import models
from django.utils.translation import ugettext_lazy as _

from lino.core import model
from lino.core.actions import Action
from lino.core.workflows import ChangeStateAction
from lino.core.exceptions import ChangedAPI

from lino.core.workflows import State



class RegistrableState(State):
    """

    Base class for the choices of the choicelist that defines the :attr:`state`
    field of any :class:`Registrable`.

    """
    is_editable = True
    """
    Whether the registrable object having this state should be
    editable or not.
    """



class Registrable(model.Model):

    """

    Base class to anything that may be "registered" and "deregistered", where
    "registered" means "this object has been taken account of".

    For example, when a :term:`ledger voucher` is registered, its associated
    :term:`ledger movements <ledger movement>` have been generated.
    Deregistering a voucher will first delete these movements.

    Registered objects are usually not editable, but this readonlyness is
    usually limited to certain fields.

    :class:`lino_xl.lib.cal.Reservation` is an example of a registrable that is
    not a ledger voucher.

    Subclasses must themselves define a field :attr:`state`.

    .. attribute:: state

        The workflow state field.

        This field must be a choicelist field, and the choices representing
        these states must be subclasses of :class:`RegistrableState`.

        There must be one state named "draft", which will be set e.g. after
        duplicating a registered object.

        There is no need to have a state named "registered". Actually
        "registered" means "in a non editable state".

    """
    class Meta(object):
        abstract = True

    workflow_state_field = 'state'

    _registrable_fields = None

    @classmethod
    def on_analyze(cls, site):
        super(Registrable, cls).on_analyze(site)
        if cls.workflow_state_field is None:
            raise Exception("{} has no workflow_state_field".format(cls))
        chl = cls.workflow_state_field.choicelist
        # for k in ('draft', 'registered'):
        #     if not hasattr(chl, k):
        #         raise Exception("{} has no value '{}'".format(chl, k))
        ic = chl.item_class
        if not issubclass(chl.item_class, RegistrableState):
            raise Exception("Invalid choicelist {} for {} state".format(chl, cls))
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
        Return a list of the fields that are *disabled* when this is
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
        # if isinstance(cls.workflow_state_field, str):
        #     raise Exception("Unresolved workflow state field in {}".format(cls))
        yield "state"
        # yield cls.workflow_state_field.name fails e.g. for vat.VatInvoices
        # because the actor is on an abstract model


    def on_duplicate(self, ar, master):
        self.state = self.workflow_state_field.choicelist.draft
        super(Registrable, self).on_duplicate(ar, master)
