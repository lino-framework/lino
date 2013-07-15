# -*- coding: UTF-8 -*-
## Copyright 2013 Luc Saffre
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
Not used.
"""
import logging
logger = logging.getLogger(__name__)

import cgi
import datetime
import dateutil

from django.conf import settings
from django.db import models
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import pgettext_lazy as pgettext
#~ from django.utils.translation import string_concat
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import force_unicode
from django.db.models import loading
from django.core import exceptions

from north import dbutils
from north.dbutils import dtosl


from lino import mixins
from lino import dd
#~ from lino.core import reports
from lino.core import actions
from lino.utils import AttrDict
from lino.utils import ONE_DAY
#~ from lino.ui import requests as ext_requests
from lino.core import constants


from lino.utils.xmlgen.html import E

from .base import TaskStates, GuestStates, EventStates


add = TaskStates.add_item
add('10', _("To do"),'todo')
add('20', pgettext(u"cal",u"Started"),'started')
add('30', _("Done"),'done')
add('50', _("Cancelled"),'cancelled')

    
add = GuestStates.add_item
add('10', _("Invited"),'invited')
add('20', _("Accepted"),'accepted') 
add('30', _("Rejected"),'rejected')
add('40', _("Present"),'present')
add('50', _("Absent"),'absent')
    

add = EventStates.add_item
add('10', _("Suggested"), 'suggested',help_text=_("Automatically suggested. Default state of an automatic event."))
add('20', _("Draft"), 'draft')
add('30', _("Notified"),'notified')
add('40', _("Scheduled"), 'scheduled')
add('50', _("Took place"),'took_place')
add('60', _("Rescheduled"),'rescheduled')
add('70', _("Cancelled"),'cancelled')
add('80', _("Absent"),'absent')
#~ add('90', _("Obsolete"),'obsolete')


@dd.receiver(dd.pre_analyze)
def setup_workflows(sender=None,**kw):
    
    site = sender
    
    TaskStates.todo.add_transition(_("Reopen"),states='done cancelled')
    TaskStates.done.add_transition(states='todo started',icon_file='accept.png')
    TaskStates.cancelled.add_transition(states='todo started',icon_file='cancel.png')

    EventStates.draft.add_transition(_("Accept"),
        #~ states='new assigned',
        states='suggested',
        owner=True,
        icon_file='book.png',
        help_text=_("User takes responsibility for this event. Planning continues."))
    #~ EventStates.draft.add_transition(TakeAssignedEvent)
    EventStates.notified.add_transition( #_("Notify guests"), 
        #~ icon_file='eye.png',
        #~ icon_file='telephone.png',
        icon_file='hourglass.png',
        states='suggested draft',
        help_text=_("Invitations have been sent. Waiting for feedback from invited guests."))
    EventStates.scheduled.add_transition(_("Confirm"), 
        #~ states='new draft assigned',
        states='suggested draft notified',
        owner=True,
        icon_file='accept.png',
        help_text=_("Mark this as Scheduled. All participants have been informed."))
    EventStates.took_place.add_transition(
        states='scheduled notified',
        owner=True,
        help_text=_("Event took place."),
        icon_file='emoticon_smile.png')
    EventStates.absent.add_transition(states='scheduled notified',icon_file='emoticon_unhappy.png')
    EventStates.rescheduled.add_transition(_("Reschedule"),
        owner=True,
        states='scheduled notified',icon_file='date_edit.png')
    EventStates.cancelled.add_transition(pgettext(u"calendar event action",u"Cancel"),
        owner=True,
        states='scheduled notified',
        icon_file='cross.png')
    #~ EventStates.assigned.add_transition(AssignEvent)
    EventStates.draft.add_transition(ResetEvent)
    


    """
    A Guest can be marked absent or present only for events that took place
    """
    #~ def allow_transition(obj,user,new_state):
    def event_took_place(action,user,obj,state):
        #~ if new_state.name in ('present','absent'):
        return obj.event.state == EventStates.took_place

    #~ kw = dict(allow=allow_transition)
    #~ GuestStates.invited.add_transition(_("Invite"),states='_',owner=True)
    GuestStates.accepted.add_transition(_("Accept"),states='_ invited',owner=False)
    #~ GuestStates.rejected.add_transition(_("Reject"),states='_ invited',owner=False)
    GuestStates.rejected.add_transition(RejectInvitation)
    GuestStates.present.add_transition(states='invited accepted',owner=True,allow=event_took_place)
    GuestStates.absent.add_transition(states='invited accepted',owner=True,allow=event_took_place)
    
    
    @dd.receiver(dd.post_save, sender=site.modules.cal.Event)
    def fill_event_guests_from_team_members(sender=None,instance=None,**kw):
        """
        If this is a team event, fill the team members as guests.
        """
        if site.loading_from_dump: return
        self = instance
        #~ logger.info("20130528 fill_event_guests_from_team_members")
        #~ if not self.state in (EventStates.blank_item, EventStates.draft): 20120829
        if not self.is_user_modified(): return
        if not self.is_editable_state(): return 
        if self.calendar and self.calendar.invite_team_members:
            if self.guest_set.all().count() == 0:
                #~ print 20120711
                ug = self.calendar.invite_team_members
                for obj in site.modules.cal.Membership.objects.filter(group=ug).exclude(user=self.user):
                    #~ if obj.watched_user.partner:
                    if obj.user.partner:
                        #~ Guest(event=self,partner=obj.watched_user.partner).save()
                        site.modules.cal.Guest(event=self,partner=obj.user.partner).save()
