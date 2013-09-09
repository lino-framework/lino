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

from __future__ import unicode_literals


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

class EventState(dd.State):
    fixed = False
    
class EventStates(dd.Workflow):
    required = dd.required(user_level='admin')
    help_text = _("""The possible states of a calendar event.""")
    app_label = 'cal'
    item_class = EventState
    #~ editable_states = set()
        
add = EventStates.add_item
add('10', _("Suggested"), 'suggested',
    help_text=_("Automatically suggested. Default state of an automatic event."))
add('20', _("Draft"), 'draft')
add('40', _("Published"), 'published')
if False:
    #~ add('30', _("Notified"),'notified')
    add('30', _("Visit"), 'visit')
    add('60', _("Rescheduled"),'rescheduled',fixed=True)
add('50', _("Took place"),'took_place',fixed=True)
add('70', _("Cancelled"),'cancelled',fixed=True)
#~ add('80', _("Absent"),'absent')



#~ EventStates.editable_states.add(EventStates.suggested)
#~ EventStates.editable_states.add(EventStates.draft)

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

# will be filled by importing either feedback or faggio


class ResetEvent(dd.ChangeStateAction):
    label = _("Reset")
    icon_file = 'cancel.png'
    #~ required = dict(states='assigned',owner=True)
    #~ required = dict(states='published rescheduled took_place')#,owner=True)
    required = dict(states='published took_place')#,owner=True)
    #~ help_text=_("Return to Draft state and restart workflow for this event.")
  
    def unused_run_from_ui(self,ar,**kw):
        obj = ar.selected_rows[0]
        if obj.guest_set.exclude(state=GuestStates.invited).count() > 0:
            def ok():
                for g in obj.guest_set.all():
                    g.state = GuestStates.invited
                    g.save()
            return ar.confirm(ok,_("This will reset all invitations"),_("Are you sure?"))
        else:
            ar.confirm(self.help_text,_("Are you sure?"))
        kw = super(ResetEvent,self).run_from_ui(ar,**kw)
        return kw
    



@dd.receiver(dd.pre_analyze)
def my_setup_workflows(sender=None,**kw):
    
    
    TaskStates.todo.add_transition(_("Reopen"),states='done cancelled')
    TaskStates.done.add_transition(states='todo started',icon_file='accept.png')
    TaskStates.cancelled.add_transition(states='todo started',icon_file='cancel.png')

    
    #~ EventStates.draft.add_transition(_("Accept"),
        #~ states='suggested',
        #~ owner=True,
        #~ icon_file='book.png',
        #~ help_text=_("User takes responsibility for this event. Planning continues."))
    #~ EventStates.draft.add_transition(TakeAssignedEvent)
    EventStates.published.add_transition(#_("Confirm"), 
        #~ states='new draft assigned',
        states='suggested draft',
        #~ owner=True,
        icon_file='accept.png',
        help_text=_("Mark this as published. All participants have been informed."))
    EventStates.took_place.add_transition(
        states='published draft',
        #~ owner=True,
        help_text=_("Event took place."),
        icon_file='emoticon_smile.png')
    #~ EventStates.absent.add_transition(states='published',icon_file='emoticon_unhappy.png')
    #~ EventStates.rescheduled.add_transition(_("Reschedule"),
        #~ states='published',icon_file='date_edit.png')
    EventStates.cancelled.add_transition(pgettext("calendar event action","Cancel"),
        #~ owner=True,
        states='published draft',
        icon_file='cross.png')
    EventStates.draft.add_transition(ResetEvent)
