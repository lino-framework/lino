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

"""

from __future__ import unicode_literals

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

from lino.modlib.cal.workflows import (TaskStates,
    EventStates,GuestStates)
    
#~ EventStates.add_item('30', _("Accepted"), 'accepted')


class InvitationFeedback(dd.ChangeStateAction,dd.NotifyingAction):
    def get_action_permission(self,ar,obj,state):
        if obj.event.state != EventStates.published:
            return False
        return super(InvitationFeedback,self).get_action_permission(ar,obj,state)
        
    def get_notify_subject(self,ar,obj):
        return self.notify_subject % dict(
            guest=obj.partner,
            day=dbutils.dtos(obj.event.start_date),
            time=str(obj.event.start_time))
            
class RejectInvitation(InvitationFeedback):
    label = _("Reject")
    help_text = _("Reject this invitation.")  
    required = dict(states='invited accepted') # ,owner=False)
    notify_subject = _("%(guest)s cannot accept invitation %(day)s at %(time)s")
    
class AcceptInvitation(InvitationFeedback):
    label = _("Accept")
    help_text = _("Accept this invitation.")  
    required = dict(states='invited rejected') # ,owner=False)
    notify_subject = _("%(guest)s confirmed invitation %(day)s at %(time)s")
    
    
@dd.receiver(dd.pre_analyze)
def my_setup_workflows(sender=None,**kw):
    
    site = sender
    
    """
    A Guest can be marked absent or present only for events that took place
    """
    #~ def allow_transition(obj,user,new_state):
    def event_took_place(action,user,obj,state):
        #~ if new_state.name in ('present','absent'):
        return obj.event.state == EventStates.took_place

    #~ kw = dict(allow=allow_transition)
    #~ GuestStates.invited.add_transition(_("Invite"),states='_',owner=True)
    #~ GuestStates.accepted.add_transition(_("Accept"),states='_ invited rejected') # ,owner=False)
    #~ GuestStates.rejected.add_transition(_("Reject"),states='_ invited',owner=False)
    GuestStates.rejected.add_transition(AcceptInvitation)
    GuestStates.rejected.add_transition(RejectInvitation)
    GuestStates.present.add_transition(states='invited accepted',#owner=True,
        allow=event_took_place)
    GuestStates.absent.add_transition(states='invited accepted',#owner=True,
        allow=event_took_place)
    
    
    #~ @dd.receiver(dd.post_save, sender=site.modules.cal.Event)
    #~ def fill_event_guests_from_team_members(sender=None,instance=None,**kw):
        #~ """
        #~ If this is a team event, fill the team members as guests.
        #~ """
        #~ if site.loading_from_dump: return
        #~ self = instance
        #~ if not self.is_user_modified(): return
        #~ if self.is_fixed_state(): return 
        #~ if self.calendar and self.calendar.invite_team_members:
            #~ if self.guest_set.all().count() == 0:
                #~ ug = self.calendar.invite_team_members
                #~ for obj in site.modules.cal.Membership.objects.filter(group=ug).exclude(user=self.user):
                    #~ if obj.user.partner:
                        #~ site.modules.cal.Guest(event=self,partner=obj.user.partner).save()
