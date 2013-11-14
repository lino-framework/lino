## Copyright 2013 Luc Saffre
## This file is part of the Lino project.

from lino import dd
from django.utils.translation import ugettext_lazy as _

class EntryStates(dd.Workflow):
    pass
    
add = EntryStates.add_item
add('10', _("To do"),'todo')
add('20', _("Started"),'started')
add('30', _("Done"),'done')
add('40', _("Sleeping"),'sleeping')
add('50', _("Cancelled"),'cancelled')


@dd.receiver(dd.pre_analyze)
def my_entry_workflow(sender=None,**kw):
    EntryStates.todo.add_transition(_("Reopen"),states='done cancelled')
    EntryStates.todo.add_transition(WakeupEntry)
    EntryStates.started.add_transition(StartEntry)
    EntryStates.sleeping.add_transition(states="todo")
    EntryStates.done.add_transition(FinishEntry)
    EntryStates.cancelled.add_transition(states='sleeping started',
        help_text=_("""This is a rather verbose help text for the action 
        which triggers transition from 'sleeping' or 'started' to 'cancelled'."""),
        icon_name='cancel')


class StartEntry(dd.ChangeStateAction):
    label = _("Start")
    help_text = _("This action is not allowed when company, body or subject is empty.")
    required = dict(states='todo cancelled')
    def get_action_permission(self,ar,obj,state):
        # cannot start entries with empty company, subject or body fields
        if not obj.company or not obj.subject or not obj.body:
            return False
        return super(StartEntry,self).get_action_permission(ar,obj,state)

class FinishEntry(StartEntry):
    icon_name='accept'
    label = _("Finish")
    required = dict(states='todo started')
    help_text = _("Inherts from StartEntry and thus is not allowed when company, body or subject is empty.")
        
class WakeupEntry(dd.ChangeStateAction,dd.NotifyingAction):
    label = _("Wake up")
    required = dict(states='sleeping')
    # in our example waking up an antry will send a notification
    def get_notify_subject(self,ar,obj):
        return _("Entry %s has been reactivated!") % obj
            
