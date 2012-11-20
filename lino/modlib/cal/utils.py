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

"""
This module deserves more documentation.

"""
import datetime

from dateutil.tz import tzlocal

from django.utils.translation import ugettext_lazy as _
from django.utils.translation import pgettext_lazy 

#~ from lino.utils.choicelists import Choice
from lino.core import actions
#~ from lino.core.actors import 
from lino import dd
from lino.utils import babel


def aware(d):
    return datetime.datetime(d.year,d.month,d.day,tzinfo=tzlocal())

def dt2kw(dt,name,**d):
    """
    Store given timestamp `dt` in a field dict. `name` can be 'start' or 'end'. 
    """
    if dt:
        if isinstance(dt,datetime.datetime):
            d[name+'_date'] = dt.date()
            if dt.time():
                d[name+'_time'] = dt.time()
            else:
                d[name+'_time'] = None
        elif isinstance(dt,datetime.date):
            d[name+'_date'] = dt
            d[name+'_time'] = None
        else:
            raise Exception("Invalid datetime value %r" % dt)
    else:
        d[name+'_date'] = None
        d[name+'_time'] = None
    return d
  
def setkw(obj,**kw):
    for k,v in kw.items():
        setattr(obj,k,v)
                              
class CalendarAction(actions.Action):
    """
    The default action for :class:`lino.modlib.cal.models.CalendarPanel`,
    only used there.
    """
    opens_a_window = True
    action_name = 'grid' # because...
    default_format = 'html'
    icon_name = 'x-tbar-calendar'



class Weekday(dd.ChoiceList):
    verbose_name = _("Weekday")
add = Weekday.add_item
add('1', _('Monday'),'monday')
add('2', _('Tuesday'),'tuesday')
add('3', _('Wednesday'),'wednesday')
add('4', _('Thursday'),'thursday')
add('5', _('Friday'),'friday')
add('6', _('Saturday'),'saturday')
add('7', _('Sunday'),'sunday')

class DurationUnit(dd.Choice):
  
    def add_duration(unit,orig,value):
        """
        Return a date or datetime obtained by adding `value` 
        times this `unit` to the specified value `orig`.
        Returns None is `orig` is empty.
        
        This is intended for use as a 
        `curried magic method` of a specified list item:
        
        >>> start_date = datetime.date(2011,10,26)
        >>> DurationUnits.months.add_duration(start_date,2)
        datetime.date(2011,12,26)
        
        See more usage examples in :func:`lino.modlib.cal.tests.cal_test.test01`.
        """
        if orig is None: 
            return None
        if unit.value == 's' : 
            return orig + datetime.timedelta(seconds=value)
        if unit.value == 'm' : 
            return orig + datetime.timedelta(minutes=value)
        if unit.value == 'h' : 
            return orig + datetime.timedelta(hours=value)
        if unit.value == 'D' : 
            return orig + datetime.timedelta(days=value)
        if unit.value == 'W' : 
            return orig + datetime.timedelta(days=value*7)
        day = orig.day
        while True:
            year = orig.year
            try:
                if unit.value == 'M' : 
                    m = orig.month + value
                    while m > 12: 
                        m -= 12
                        year += 1
                    while m < 1: 
                        m += 12
                        year -= 1
                    return orig.replace(month=m,day=day,year=year)
                if unit.value == 'Y' : 
                    return orig.replace(month=dt.year + value,day=day)
                raise Exception("Invalid DurationUnit %s" % unit)
            except ValueError:
                if day > 28:
                    day -= 1
                else:
                    raise
    
  
    
class DurationUnits(dd.ChoiceList):
    """A list of possible values for the `duration_unit` field of an :class:`Event`.
    """
    verbose_name = _("Duration Unit")
    item_class = DurationUnit
        
    
    
add = DurationUnits.add_item
add('s', _('seconds'),'seconds')
add('m', _('minutes'),'minutes')
add('h', _('hours')  ,'hours'  )
add('D', _('days')   ,'days'   )
add('W', _('weeks')  ,'weeks'  )
add('M', _('months') ,'months' )
add('Y', _('years')  ,'years'  )


def amonthago():
    return DurationUnits.months.add_duration(datetime.date.today(),-1)
        

class TaskStates(dd.Workflow):
    """
    State of a Calendar Task. Used as Workflow selector.
    """
    #~ label = _("State")
    
    @classmethod
    def migrate(cls,status_id):
        """
        Used by :meth:`lino.apps.pcsw.migrate.migrate_from_1_4_4`.
        """
        #~ if status_id is None: return None
        cv = {
          None: TaskStates.todo,
          1:TaskStates.todo,
          2:TaskStates.started,
          #~ 2:TaskStates.todo,
          3:TaskStates.done,
          4:TaskStates.cancelled,
          }
        return cv[status_id]
    
add = TaskStates.add_item
#~ add('10', _("To do"),'todo',required=dict(states=['']))
#~ add('20', pgettext_lazy(u"cal",u"Started"),'started',required=dict(states=['','todo']))
#~ add('30', _("Done"),'done',required=dict(states=['','todo','started']))
#~ add('40', _("Sleeping"),'sleeping',required=dict(states=['','todo']))
#~ add('50', _("Cancelled"),'cancelled',required=dict(states=['todo','sleeping']))

#~ add('00', _("Virgin"),'todo')
add('10', _("To do"),'todo')
add('20', pgettext_lazy(u"cal",u"Started"),'started')
add('30', _("Done"),'done')
#~ add('40', _("Sleeping"),'sleeping')
add('50', _("Cancelled"),'cancelled')

TaskStates.todo.add_workflow(_("Reopen"),states='done cancelled')
#~ TaskStates.todo.add_workflow(_("Wake up"),states='sleeping')
#~ TaskStates.started.add_workflow(states='_ todo')
TaskStates.done.add_workflow(states='todo started',icon_file='accept.png')
#~ TaskStates.sleeping.add_workflow(states='_ todo')
TaskStates.cancelled.add_workflow(states='todo started',icon_file='cancel.png')

#~ class EventStates(ChoiceList):
class EventStates(dd.Workflow):
    """
    State of a Calendar Event. Used as Workflow selector.
    """
    #~ label = _("State")
    
    @classmethod
    def allow_state_suggest(cls,self,user):
        if not self.start_time: return False
        return True
        
    @classmethod
    def before_state_change(cls,obj,ar,kw,oldstate,newstate):
      
        if newstate.name == 'draft':
            ar.confirm(_("This will reset all invitations"))
            for g in obj.guest_set.all():
                g.state = GuestStates.invited
                g.save()
        
        
    @classmethod
    def migrate(cls,status_id):
        """
        Used by :meth:`lino.apps.pcsw.migrate.migrate_from_1_4_4`.
        """
        #~ if status_id is None: return cls.blank_item
        cv = {
          #~ None: '',
          None:EventStates.draft,
          1:EventStates.suggested,
          2:EventStates.scheduled,
          3:EventStates.cancelled,
          4:EventStates.rescheduled,
          5:EventStates.absent,
        }
        return cv[status_id]
        
#~ def allow_scheduled(action,user,obj,state):
    #~ if not obj.start_time: return False
    #~ return True
    
    
add = EventStates.add_item
add('10', _("New"), 'new',help_text=_("Default state of an automatic event."))
add('15', _("Suggested"), 'suggested',help_text=_("Suggested by colleague. External guests are notified, but user must confirm."))
add('20', _("Draft"), 'draft')
add('30', _("Notified"),'notified')
add('40', _("Scheduled"), 'scheduled')
add('50', _("Took place"),'took_place')
add('60', _("Rescheduled"),'rescheduled')
add('70', _("Cancelled"),'cancelled')
add('80', _("Absent"),'absent')
#~ add('90', _("Obsolete"),'obsolete')

EventStates.draft.add_workflow(_("Accept"),
    states='new suggested',
    owner=True,
    icon_file='book.png',
    help_text=_("User takes responsibility for this event. Guests are not yet notified."))
EventStates.suggested.add_workflow(_("Suggest"),
    icon_file='flag_blue.png',
    states='new draft',
    owner=False,
    help_text=_("Event was created by colleague for a client. Owner must confirm it."))
EventStates.new.add_workflow(_("Suggest"),
    icon_file='cancel.png',
    states='suggested',
    owner=False,
    help_text=_("Undo suggested event."))
EventStates.notified.add_workflow(_("Notify guests"), 
    icon_file='eye.png',
    states='draft',
    help_text=_("Invitations have been sent. Waiting for feedback from guests."))
EventStates.scheduled.add_workflow(_("Confirm"), 
    states='new draft suggested',
    owner=True,
    icon_file='accept.png',
    help_text=_("Mark this as Scheduled. All participants have been informed."))
EventStates.took_place.add_workflow(
    states='scheduled notified',
    owner=True,
    help_text=_("Event took place."),
    icon_file='emoticon_smile.png')
EventStates.rescheduled.add_workflow(_("Reschedule"),
    owner=True,
    states='suggested scheduled notified',icon_file='date_edit.png')
EventStates.cancelled.add_workflow(_("Cancel"),
    owner=True,
    states='suggested scheduled notified',
    icon_file='cancel.png')
EventStates.absent.add_workflow(states='scheduled notified',icon_file='emoticon_unhappy.png')
#~ EventStates.obsolete.add_workflow()
EventStates.draft.add_workflow(_("Restart"),
    states='notified scheduled rescheduled',
    notify=True,
    icon_file='arrow_undo.png',
    help_text=_("Return to Draft state and restart workflow for this event."))

#~ EventStates.add_statechange('draft',help_text=_("Default state of a new event."))
#~ EventStates.add_statechange('suggested',_("Suggest"),states='_ draft')
#~ EventStates.add_statechange('notified',_("Notify guests"), states='draft')
#~ EventStates.add_statechange('scheduled',_("Confirm"), states='_draft suggested'
    #~ help_text=_("Confirmed. All participants have been informed."))
#~ EventStates.add_statechange('took_place',states='scheduled notified')
#~ EventStates.add_statechange('rescheduled',_("Reschedule"),states='suggested scheduled notified')
#~ EventStates.add_statechange('cancelled',_("Cancel"),states='suggested scheduled notified')
#~ EventStates.add_statechange('absent',states='scheduled notified')
#~ EventStates.add_statechange('obsolete')
    

    
class GuestStates(dd.Workflow):
    """
    State of a Calendar Event Guest. Used as Workflow selector.
    """
    #~ label = _("Guest State")
    #~ label = _("State")
    
    @classmethod
    def allow_state_present(self,obj,user):
        return obj.event.state == EventStates.took_place
        
    @classmethod
    def allow_state_absent(self,obj,user):
        return obj.event.state == EventStates.took_place
        
add = GuestStates.add_item
add('10', _("Invited"),'invited')
add('20', _("Accepted"),'accepted') #,required=dict(states=['','invited'],owner=False),action_label=_("Accept"))
add('30', _("Rejected"),'rejected')# ,required=dict(states=['','invited'],owner=False),action_label=_("Reject"))
add('40', _("Present"),'present')# ,required=dict(states=['invited','accepted'],owner=True))
add('50', _("Absent"),'absent')# ,required=dict(states=['invited','accepted'],owner=True))

class RejectInvitation(dd.ChangeStateAction,dd.NotifyingAction):
    label = _("Reject")
    help_text = _("Reject this invitation.")  
    required = dict(states='invited',owner=False)
    
    def get_notify_subject(self,ar,obj):
        return _("Cannot accept invitation %(day)s at %(time)s") % dict(
           day=babel.dtos(obj.event.start_date),
           time=str(obj.event.start_time))

  
#~ GuestStates.invited.add_workflow(_("Invite"),states='_',owner=True)
GuestStates.accepted.add_workflow(_("Accept"),states='_ invited',owner=False)
#~ GuestStates.rejected.add_workflow(_("Reject"),states='_ invited',owner=False)
GuestStates.rejected.add_workflow(RejectInvitation)
GuestStates.present.add_workflow(states='invited accepted',owner=True)
GuestStates.absent.add_workflow(states='invited accepted',owner=True)


class AccessClasses(dd.ChoiceList):
    verbose_name = _("Access Class")
add = AccessClasses.add_item
add('10', _('Private'),'private')
add('20', _('Show busy'),'show_busy')
add('30', _('Public'),'public')
