# -*- coding: UTF-8 -*-
# Copyright 2011-2014 Luc Saffre
# License: BSD (see file COPYING for details)

"""

Minimal workflow definition for :mod:`lino.modlib.cal`.

"""

from __future__ import unicode_literals


from django.db import models

from django.utils.translation import ugettext_lazy as _
from django.utils.translation import pgettext_lazy as pgettext

from lino import dd


class TaskStates(dd.Workflow):

    """
    State of a Calendar Task. Used as Workflow selector.
    """
    verbose_name_plural = _("Task states")
    required = dd.required(user_level='admin')
    app_label = 'cal'


add = TaskStates.add_item
#~ add('10', _("To do"),'todo',required=dict(states=['']))
#~ add('20', pgettext_lazy(u"cal",u"Started"),'started',required=dict(states=['','todo']))
#~ add('30', _("Done"),'done',required=dict(states=['','todo','started']))
#~ add('40', _("Sleeping"),'sleeping',required=dict(states=['','todo']))
#~ add('50', _("Cancelled"),'cancelled',required=dict(states=['todo','sleeping']))

#~ add('00', _("Virgin"),'todo')
add('10', _("To do"), 'todo')
add('20', pgettext(u"cal", u"Started"), 'started')
add('30', _("Done"), 'done')
#~ add('40', _("Sleeping"),'sleeping')
add('50', _("Cancelled"), 'cancelled')


class EventState(dd.State):
    fixed = False
    edit_guests = False


class EventStates(dd.Workflow):
    verbose_name_plural = _("Event states")
    required = dd.required(user_level='admin')
    help_text = _("""The possible states of a calendar event.""")
    app_label = 'cal'
    item_class = EventState
    edit_guests = models.BooleanField(_("Edit guests list"), default=False)
    fixed = models.BooleanField(_("Fixed"), default=False)
    #~ editable_states = set()
    #~ column_names = "value name text edit_guests"

    #~ @dd.virtualfield(models.BooleanField("edit_guests"))
    #~ def edit_guests(cls,obj,ar):
        #~ return obj.edit_guests

    @classmethod
    def get_column_names(self, ar):
        return 'value name text edit_guests fixed remark'

add = EventStates.add_item
add('10', _("Suggested"), 'suggested',
    edit_guests=True,
    help_text=_("Automatically suggested. \
    Default state of an automatic event."))
add('20', _("Draft"), 'draft', edit_guests=True)
if False:
    add('40', _("Published"), 'published')
    #~ add('30', _("Notified"),'notified')
    add('30', _("Visit"), 'visit')
    add('60', _("Rescheduled"), 'rescheduled', fixed=True)
add('50', _("Took place"), 'took_place', fixed=True, edit_guests=True)
add('70', _("Cancelled"), 'cancelled', fixed=True)
add('75', _("Omitted"), 'omitted', fixed=True)
#~ add('80', _("Absent"), 'absent')


#~ EventStates.editable_states.add(EventStates.suggested)
#~ EventStates.editable_states.add(EventStates.draft)
class GuestState(dd.State):
    afterwards = False


class GuestStates(dd.Workflow):

    """
    State of a Calendar Event Guest. Used as Workflow selector.
    """
    verbose_name_plural = _("Guest states")
    required = dd.required(user_level='admin')
    app_label = 'cal'
    item_class = GuestState
    afterwards = models.BooleanField(_("Afterwards"), default=False)

    @classmethod
    def get_column_names(self, ar):
        return 'value name afterwards text remark'


add = GuestStates.add_item
add('10', _("Invited"), 'invited')

# will be filled by importing either feedback or faggio


@dd.receiver(dd.pre_analyze)
def setup_task_workflows(sender=None, **kw):

    TaskStates.todo.add_transition(_("Reopen"), states='done cancelled')
    TaskStates.done.add_transition(states='todo started', icon_name='accept')
    TaskStates.cancelled.add_transition(
        states='todo started', icon_name='cancel')
