# -*- coding: UTF-8 -*-
# Copyright 2013-2015 Luc Saffre
# License: BSD (see file COPYING for details)

from __future__ import unicode_literals

from ..workflows import *
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import pgettext_lazy as pgettext

GuestStates.clear()
add = GuestStates.add_item
add('10', _("Invited"), 'invited')
#add('20', _("Accepted"),'accepted')
add('40', _("Present"), 'present', afterwards=True)
add('50', _("Absent"), 'absent', afterwards=True)
add('60', _("Excused"), 'excused')
#~ add('60', _("Visit"),'visit')


# class FindNextDate(dd.Action):
#     label = _("Move event to next")
#     icon_name = 'date_next'

#     def get_action_permission(self, ar, obj, state):
#         if obj.auto_type is None:
#             return False
#         return super(FindNextDate, self).get_action_permission(
#             ar, obj, state)

#     def run_from_ui(self, ar):
#         eg = ar.master_instance
#         if eg is None:
#             return
#         for obj in ar.selected_rows:
#             obj.move_next(ar)
#             obj.save()


@dd.receiver(dd.pre_analyze)
def my_event_workflows(sender=None, **kw):

    # sender.modules.cal.Event.find_next_date = FindNextDate()

    EventStates.took_place.add_transition(
        required_states='suggested draft cancelled',
        help_text=_("Event took place."),
        icon_name='emoticon_smile')
    #~ EventStates.absent.add_transition(states='published',icon_file='emoticon_unhappy.png')
    #~ EventStates.rescheduled.add_transition(_("Reschedule"),
        #~ states='published',icon_file='date_edit.png')
    EventStates.cancelled.add_transition(
        pgettext("calendar event action", "Cancel"),
        #~ owner=True,
        required_states='suggested draft took_place',
        icon_name='cross')
    # EventStates.omitted.add_transition(
    #     pgettext("calendar event action", "Omit"),
    #     states='suggested draft took_place',
    #     icon_name='date_delete')
    EventStates.suggested.add_transition(
        _("Reset"),
        required_states='draft suggested took_place cancelled',
        help_text=_("Reset to initial state."))

    # EventStates.suggested.add_transition(
    #     _("Reset"),
    #     required_states='draft took_place cancelled',
    #     help_text=_("Reset to 'suggested' state."))
