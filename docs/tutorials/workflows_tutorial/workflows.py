## Copyright 2013 Luc Saffre
## This file is part of the Lino project.

from lino import dd
from django.utils.translation import ugettext_lazy as _

class EntryStates(dd.Workflow):
    pass
    
add = EntryStates.add_item
add('10', _("Draft"),'draft')
add('20', _("To do"),'todo')
add('30', _("Started"),'started')
add('40', _("Done"),'done')
add('50', _("Sleeping"),'sleeping')
add('60', _("Cancelled"),'cancelled')


@dd.receiver(dd.pre_analyze)
def setup_task_workflows(sender=None,**kw):
    EntryStates.draft.add_transition(_("Reset"),states='todo done cancelled')
    EntryStates.todo.add_transition(_("Reopen"),states='draft done cancelled')
    EntryStates.started.add_transition(StartEntry)
    EntryStates.sleeping.add_transition(WakeupEntry)
    EntryStates.done.add_transition(states='draft todo started',icon_name='accept')
    EntryStates.cancelled.add_transition(states='draft todo started',icon_name='cancel')




class StartEntry(dd.ChangeStateAction):
    required = dict(states='draft todo cancelled')
    def get_action_permission(self,ar,obj,state):
        # cannot start entries with empty company, subject or body fields
        if not obj.company or not obj.subject or not obj.body:
            return False
        return super(StartEntry,self).get_action_permission(ar,obj,state)
        
class WakeupEntry(dd.ChangeStateAction,dd.NotifyingAction):
    required = dict(states='sleeping')
    # in our example waking up an antry will send a notification
    def get_notify_subject(self,ar,obj):
        return _("Entry %s has been reactivated!") % obj
            
