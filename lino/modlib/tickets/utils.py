# -*- coding: UTF-8 -*-
# Copyright 2011-2012 Luc Saffre
# License: BSD (see file COPYING for details)

from django.utils.translation import ugettext_lazy as _
#~ from lino.utils.workflows import Workflow
from lino.api import dd, rt


class DependencyTypes(dd.ChoiceList):
    verbose_name = _("Dependency type")
add = DependencyTypes.add_item
add('10', _("Duplicate"), 'duplicate')
add('20', _("Callback"), 'callback')
add('30', _("Requires"), 'requires')

    
class TicketStates(dd.Workflow):

    """
    The state of a ticket (new, open, closed, ...)
    """
    #~ label = _("Ticket State")

    @classmethod
    def allow_state_active(cls, self, user):
        if not self.reported:
            return False
        return True

    @classmethod
    def allow_state_assigned(cls, self, user):
        if not self.user:
            return False
        return True

    @classmethod
    def allow_state_fixed(cls, self, user):
        if not self.fixed:
            return False
        return True


add = TicketStates.add_item

add('10', _("Assigned"), 'assigned',
    required=dict(states=['', 'active']),
    action_name=_("Start"),
    help_text=_("Ticket has been assigned to somebody who is assigned on it."))
add('20', _("Active"), 'active')
add('30', _("Waiting"), 'waiting',
    required=dict(states=['assigned']),
    action_name=_("Wait for feedback"),
    help_text=_("Waiting for feedback from partner."))
add('40', _("Fixed"), 'fixed',
    required=dict(states=['assigned']),
    help_text=_("Has been fixed. Waiting for test results."))
add('50', _("Tested"), 'tested',
    required=dict(states=['fixed']),
    help_text=_("Has been tested. Waiting to be closed."))
add('60', _("Closed"), 'closed',
    required=dict(states=['tested']),
    help_text=_("Definitively closed. Cannot be undone."))
add('90', _("Cancelled"), 'cancelled',
    required=dict(states=['assigned']),
    help_text=_("Has been cancelled for some reason."))
