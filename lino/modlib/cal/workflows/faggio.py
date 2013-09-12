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

from __future__ import unicode_literals

from lino.modlib.cal.workflows import *
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import pgettext_lazy as pgettext

#~ @dd.receiver(dd.pre_analyze)
#~ def my(sender,**kw):
if True:
    add = GuestStates.add_item
    #add('20', _("Accepted"),'accepted') 
    add('30', _("Excused"),'excused')
    add('40', _("Present"),'present',afterwards=True)
    add('50', _("Absent"),'absent',afterwards=True)
    #~ add('60', _("Visit"),'visit')


@dd.receiver(dd.pre_analyze)
def my_event_workflows(sender=None,**kw):
    
    EventStates.took_place.add_transition(
        states='suggested draft cancelled',
        #~ owner=True,
        help_text=_("Event took place."),
        icon_name='emoticon_smile')
    #~ EventStates.absent.add_transition(states='published',icon_file='emoticon_unhappy.png')
    #~ EventStates.rescheduled.add_transition(_("Reschedule"),
        #~ states='published',icon_file='date_edit.png')
    EventStates.cancelled.add_transition(pgettext("calendar event action","Cancel"),
        #~ owner=True,
        states='suggested draft took_place',
        icon_name='cross')
