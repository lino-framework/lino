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

from django.utils.translation import ugettext_lazy as _
from django.utils.translation import pgettext_lazy 

from lino.utils.choicelists import ChoiceList, Choice

from dateutil.tz import tzlocal

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
                              


class Weekday(ChoiceList):
    label = _("Weekday")
add = Weekday.add_item
add('1', _('Monday'),'monday')
add('2', _('Tuesday'),'tuesday')
add('3', _('Wednesday'),'wednesday')
add('4', _('Thursday'),'thursday')
add('5', _('Friday'),'friday')
add('6', _('Saturday'),'saturday')
add('7', _('Sunday'),'sunday')

class DurationUnit(Choice):
  
    def add_duration(unit,orig,value):
        """
        Return a date or datetime obtained by adding `value` 
        times the specified `unit` to the specified 
        value `orig`.
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
    
  
    
class DurationUnits(ChoiceList):
    """A list of possible values for the `duration_unit` field of an :class:`Event`.
    """
    label = _("Duration Unit")
    item_class = DurationUnit
        
    
    
add = DurationUnits.add_item
add('s', _('seconds'),'seconds')
add('m', _('minutes'),'minutes')
add('h', _('hours')  ,'hours'  )
add('D', _('days')   ,'days'   )
add('W', _('weeks')  ,'weeks'  )
add('M', _('months') ,'months' )
add('Y', _('years')  ,'years'  )



class TaskState(ChoiceList):
    """
    State of a Calendar Task. Used as Workflow selector.
    """
    label = _("State")
    @classmethod
    def migrate(cls,status_id):
        """
        Used by :meth:`lino.apps.pcsw.migrate.migrate_from_1_4_4`.
        """
        #~ if status_id is None: return None
        cv = {
          None: '',
          1:TaskState.todo,
          2:TaskState.started,
          3:TaskState.done,
          4:TaskState.cancelled,
          }
        return cv[status_id]
    
add = TaskState.add_item
add('10', _("To do"),'todo',required=dict(states=['']))
add('20', pgettext_lazy(u"cal",u"Started"),'started',required=dict(states=['','todo']))
add('30', _("Done"),'done',required=dict(states=['','todo','started']))
add('40', _("Sleeping"),'sleeping',required=dict(states=['','todo']))
add('50', _("Cancelled"),'cancelled',required=dict(states=['todo','sleeping']))

class EventState(ChoiceList):
    """
    State of a Calendar Event. Used as Workflow selector.
    """
    label = _("State")
    
    @classmethod
    def migrate(cls,status_id):
        """
        Used by :meth:`lino.apps.pcsw.migrate.migrate_from_1_4_4`.
        """
        #~ if status_id is None: return cls.blank_item
        cv = {
          None: '',
          1:EventState.scheduled,
          2:EventState.confirmed,
          3:EventState.cancelled,
          4:EventState.rescheduled,
          5:EventState.absent,
        }
        return cv[status_id]
        
#~ def allow_scheduled(action,user,obj,state):
    #~ if not obj.start_time: return False
    #~ return True
    
add = EventState.add_item
add('10', _("Draft"), 'draft',
  #~ required=dict(states=['','scheduled']),
  help_text=_("Will automatically be set if user saves some changes.")
  ) # is_user_modified
add('20', _("Scheduled"), 'scheduled',
  #~ required=dict(allow=allow_scheduled,states=['','draft']),
  required=dict(states=['','draft']),
  help_text=_("Author is aware of this event and guests should get notified. Requires a start_time.")
  )
add('30', _("Notified"),'notified',required=dict(states=['scheduled']))
#~ add('20', _("Suggested"),'suggested')
#~ add('30', _("Published"),'published')
add('40', _("Confirmed"),'confirmed',required=dict(states=['scheduled','notified']))
add('50', _("Took place"),'took_place',required=dict(states=['scheduled','notified','confirmed']))
add('60', _("Rescheduled"),'rescheduled',required=dict(states=['scheduled','notified','confirmed']))
add('70', _("Cancelled"),'cancelled',required=dict(states=['scheduled','notified','confirmed']))
add('80', _("Absent"),'absent',required=dict(states=['scheduled','notified','confirmed']))
add('90', _("Obsolete"),'obsolete',required=dict(states=[]))


    
class GuestState(ChoiceList):
    """
    State of a Calendar Event Guest. Used as Workflow selector.
    """
    #~ label = _("Guest State")
    label = _("State")
add = GuestState.add_item
add('10', _("Invited"),'invited',required=dict(states=[''],owner=True),action_label=_("Invite"))
add('20', _("Confirmed"),'confirmed',required=dict(states=['','invited'],owner=False),action_label=_("Confirm"))
add('30', _("Rejected"),'rejected',required=dict(states=['','invited'],owner=False),action_label=_("Reject"))
add('40', _("Present"),'present',required=dict(states=['invited','confirmed'],owner=True))
add('50', _("Absent"),'absent',required=dict(states=['invited','confirmed'],owner=True))


class AccessClasses(ChoiceList):
    label = _("Access Class")
add = AccessClasses.add_item
add('10', _('Private'),'private')
add('20', _('Show busy'),'show_busy')
add('30', _('Public'),'public')
