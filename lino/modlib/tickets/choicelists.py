# -*- coding: UTF-8 -*-
# Copyright 2014-2015 Luc Saffre
# License: BSD (see file COPYING for details)
"""
Database models for `lino.modlib.humanlinks`.

.. autosummary::

"""


from __future__ import unicode_literals
from __future__ import print_function

from django.utils.translation import string_concat

from lino.mixins.periods import ObservedEvent

from lino.api import dd, _


from datetime import datetime, time
combine = datetime.combine
T00 = time(0, 0, 0)
T24 = time(23, 59, 59)


class TicketEvents(dd.ChoiceList):
    verbose_name = _("Observed event")
    verbose_name_plural = _("Observed events")


class TicketEventCreated(ObservedEvent):
    text = _("Created")

    def add_filter(self, qs, pv):
        if pv.start_date:
            qs = qs.filter(created__gte=combine(pv.start_date, T00))
        if pv.end_date:
            qs = qs.filter(created__lte=combine(pv.end_date, T24))
        return qs

TicketEvents.add_item_instance(TicketEventCreated('created'))


class TicketEventModified(ObservedEvent):
    text = _("Modified")

    def add_filter(self, qs, pv):
        if pv.start_date:
            qs = qs.filter(modified__gte=combine(pv.start_date, T00))
        if pv.end_date:
            qs = qs.filter(modified__lte=combine(pv.end_date, T24))
        return qs


TicketEvents.add_item_instance(TicketEventModified('modified'))


class ProjectEvents(dd.ChoiceList):
    verbose_name = _("Observed event")
    verbose_name_plural = _("Observed events")
    
ProjectEvents.add_item_instance(TicketEventModified('modified'))


class TicketStates(dd.Workflow):

    """The state of a ticket (new, open, closed, ...)

    Default choices are:

    .. attribute:: new

        Somebody reported this ticket, but there was no response so
        far.
        The ticket needs to be triaged.

    .. attribute:: talk

        The ticket needs discussion with the reporter.
        We don't yet know exactly
        what to do with it.

    .. attribute:: todo

        The ticket is confirmed and we are working on it.
        It appears in the todo list of somebody (either the assigned
        worker, or our general todo list)

    .. attribute:: sticky

        Special state for permanent tickets which have no lifecycle.

    .. attribute:: done

        The ticket is basically done. If it is not also marked as
        closed, then something else still needs to be done
        (e.g. testing, confirmation, documentation,..)

    .. attribute:: refused

        It has been decided that we won't fix this ticket.

    """
    #~ label = _("Ticket State")

    # @classmethod
    # def allow_state_active(cls, self, user):
    #     if not self.reported:
    #         return False
    #     return True

    # @classmethod
    # def allow_state_assigned(cls, self, user):
    #     if not self.user:
    #         return False
    #     return True

    # @classmethod
    # def allow_state_fixed(cls, self, user):
    #     if not self.fixed:
    #         return False
    #     return True


add = TicketStates.add_item

# add('10', _("Assigned"), 'assigned',
#     required=dict(states=['', 'active']),
#     action_name=_("Start"),
#     help_text=_("Ticket has been assigned to somebody who is assigned on it."))
add('10', _("New"), 'new')
add('15', _("Talk"), 'talk')
add('20', _("To do"), 'todo')
add('21', _("Sticky"), 'sticky')
# add('30', _("Callback"), 'callback',
    # required=dict(states=['new']),
    # action_name=_("Wait for feedback"),
    # help_text=_("Waiting for feedback from partner."))
# add('40', _("Fixed"), 'fixed',
#     # required=dict(states=['todo']),
#     help_text=_("Has been fixed. Waiting to be tested."))
add('50', _("Done"), 'done')
# add('50', _("Tested"), 'tested',
#     # required=dict(states=['fixed']),
#     help_text=_("Has been fixed and tested."))
add('60', _("Refused"), 'refused',
    # required=dict(states="tested new todo callback"),
    help_text=_("It has been decided that we won't fix this ticket."))
# add('70', _("Sleeping"), 'sleeping',
#     help_text=_("Waiting for better times."))
# add('90', _("Cancelled"), 'cancelled',
#     # required=dict(states=['new todo waiting']),
#     help_text=_("Has been cancelled for some reason."))

"""Difference between Cancelled and Refused was that: Canceled means
that we don't want to talk about this ticket anymore.  Refused makes
sense for tickets which had been asked by a partner. In that case we
still may want to report it.

"""

# class TicketStateGroups(dd.Choice):
#     def __init__(self, 
# class TicketStateGroups(dd.ChoiceList):
#     verbose_name = _("Dependency type")
# add = DependencyTypes.add_item
# add('10', _("Duplicate"), 'duplicate')


@dd.receiver(dd.pre_analyze)
def tickets_workflows(sender=None, **kw):
    """
    """
    TicketStates.talk.add_transition(required_states="new todo")
    TicketStates.todo.add_transition(required_states="new talk")
    TicketStates.done.add_transition(required_states="todo new talk")
    TicketStates.refused.add_transition(required_states="todo new talk")
    # TicketStates.cancelled.add_transition(states="todo new callback")
    # TicketStates.new.add_transition(states="todo callback fixed tested")
    # TicketStates.sleeping.add_transition(required_states="todo new callback")

    TicketStates.favorite_states = (TicketStates.sticky, )
    TicketStates.work_states = (TicketStates.todo, TicketStates.new)
    TicketStates.waiting_states = (TicketStates.done, )

    # not used:
    # TicketStates.idle_states = (
    #     TicketStates.fixed, TicketStates.tested,
    #     TicketStates.callback, TicketStates.refused)


class LinkType(dd.Choice):

    symmetric = False

    def __init__(self, value, name, ptext, ctext, **kw):
        self.ptext = ptext  # parent
        self.ctext = ctext
        text = string_concat(ctext, ' (', ptext, ')')
        super(LinkType, self).__init__(value, text, name, **kw)

    def as_parent(self):
        return self.ptext

    def as_child(self):
        return self.ctext


class LinkTypes(dd.ChoiceList):
    """The possible values of a :class:`lino.modlib.tickets.models.Link`.

    .. attribute:: requires

        The parent ticket requires the child ticket.
    
    .. attribute:: triggers

        The parent ticket triggers the child ticket.
    
    .. attribute:: deploys

        The parent ticket is a deployment which deploys the child ticket.

        Release notes are a printout of a deployment ticket which
        lists the deployed tickets.

    """
    required_roles = dd.required(dd.SiteStaff)
    verbose_name = _("Dependency type")
    verbose_name_plural = _("Dependency types")
    item_class = LinkType

add = LinkTypes.add_item
add('10', 'requires', _("Requires"), _("Required by"))
add('20', 'triggers', _("Triggers"), _("Triggered by"))
# add('30', 'seealso', _("See also"), _("Referred by"))
add('40', 'deploys', _("Deploys"), _("Deployed by"))
# add('20', 'duplicates', _("Duplicates"), _("Duplicate of"))

# LinkTypes.addable_types = [LinkTypes.requires, LinkTypes.duplicates]
