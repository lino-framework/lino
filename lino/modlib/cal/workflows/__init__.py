# -*- coding: UTF-8 -*-
## Copyright 2011-2013 Luc Saffre
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

"""

Minimal workflow definition for lino.modlib.cal.

"""

from django.utils.translation import ugettext_lazy as _
from django.utils.translation import pgettext_lazy as pgettext

from lino import dd

class TaskStates(dd.Workflow):
    """
    State of a Calendar Task. Used as Workflow selector.
    """
    required = dd.required(user_level='admin')
    app_label = 'cal'
    
    
add = TaskStates.add_item
#~ add('10', _("To do"),'todo',required=dict(states=['']))
#~ add('20', pgettext_lazy(u"cal",u"Started"),'started',required=dict(states=['','todo']))
#~ add('30', _("Done"),'done',required=dict(states=['','todo','started']))
#~ add('40', _("Sleeping"),'sleeping',required=dict(states=['','todo']))
#~ add('50', _("Cancelled"),'cancelled',required=dict(states=['todo','sleeping']))

#~ add('00', _("Virgin"),'todo')
add('10', _("To do"),'todo')
add('20', pgettext(u"cal",u"Started"),'started')
add('30', _("Done"),'done')
#~ add('40', _("Sleeping"),'sleeping')
add('50', _("Cancelled"),'cancelled')

    
class EventStates(dd.Workflow):
    required = dd.required(user_level='admin')
    help_text = _("""List of the possible states of a calendar event.""")
    app_label = 'cal'
        
add = EventStates.add_item
add('10', _("Suggested"), 'suggested',help_text=_("Automatically suggested. Default state of an automatic event."))
add('20', _("Draft"), 'draft')
#~ add('30', _("Notified"),'notified')
add('40', _("Scheduled"), 'scheduled')
add('50', _("Took place"),'took_place')
add('60', _("Rescheduled"),'rescheduled')
add('70', _("Cancelled"),'cancelled')
#~ add('80', _("Absent"),'absent')

class GuestState(dd.State):
    afterwards = False
    
class GuestStates(dd.Workflow):
    """
    State of a Calendar Event Guest. Used as Workflow selector.
    """
    required = dd.required(user_level='admin')
    app_label = 'cal'
    item_class = GuestState

add = GuestStates.add_item
add('10', _("Invited"),'invited')
add('20', _("Accepted"),'accepted') 
add('30', _("Rejected"),'rejected')
add('40', _("Present"),'present',afterwards=True)
add('50', _("Absent"),'absent',afterwards=True)
    
