# -*- coding: UTF-8 -*-
## Copyright 2011-2012 Luc Saffre
## This file is part of the Lino project.
## Lino is free software; you can redistribute it and/or modify 
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 3 of the License, or
## (at your option) any later version.
## Lino is distributed in the hope that it will be useful, 
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
## GNU General Public License for more details.
## You should have received a copy of the GNU General Public License
## along with Lino; if not, see <http://www.gnu.org/licenses/>.

from django.utils.translation import ugettext_lazy as _
#~ from lino.utils.workflows import Workflow
from lino import dd


class TicketStates(dd.Workflow):
    """
    The state of a ticket (new, open, closed, ...)
    """
    #~ label = _("Ticket State")
    
    @classmethod
    def allow_state_accepted(cls,self,user):
        if not self.reported:
            return False
        return True
        
    @classmethod
    def allow_state_working(cls,self,user):
        if not self.user:
            return False
        return True
        
    @classmethod
    def allow_state_fixed(cls,self,user):
        if not self.fixed:
            return False
        return True
    

add = TicketStates.add_item

add('10',_("Accepted"),'accepted')
add('20',_("Working"),'working',
    required=dict(states=['','accepted']),
    action_name=_("Start"),
    help_text=_("Ticket has been assigned to somebody who is working on it."))
add('30',_("Waiting"),'waiting',
    required=dict(states=['working']),
    action_name=_("Wait for feedback"),
    help_text=_("Waiting for feedback from partner."))
#~ add('20',_("Assigned"),'assigned')
add('40',_("Fixed"),'fixed',
    required=dict(states=['working']),
    help_text=_("Has been fixed. Waiting for test results."))
add('50',_("Tested"),'tested',
    required=dict(states=['fixed']),
    help_text=_("Has been tested. Waiting to be closed."))
add('60',_("Closed"),'closed',
    required=dict(states=['tested']),
    help_text=_("Definitively closed. Cannot be undone."))
add('90',_("Cancelled"),'cancelled',
    required=dict(states=['working']),
    help_text=_("Has been cancelled for some reason."))

