# -*- coding: UTF-8 -*-
## Copyright 2011 Luc Saffre
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
This module defines tables :class:`Task` and :class:`Event`.

"""
import cgi
import datetime

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import force_unicode

from lino import mixins
from lino import fields
from lino import reports
from lino.utils import babel
from lino.tools import resolve_model

from lino.modlib.contacts import models as contacts

from lino.modlib.cal.utils import EventStatus, \
    TaskStatus, DurationUnit, Priority, AccessClass, add_duration

from lino.utils.babel import dtosl
#~ from lino.utils.dpy import is_deserializing

class Place(models.Model):
    name = models.CharField(_("Name"),max_length=200)
  
class Places(reports.Report):
    model = Place
    

class EventType(mixins.PrintableType):
    "Deserves more documentation."
  
    templates_group = 'events'
    
    class Meta:
        verbose_name = _("Event Type")
        verbose_name_plural = _('Event Types')
        
    name = babel.BabelCharField(_("Event title"),max_length=200)
    
    def __unicode__(self):
        return unicode(babel.babelattr(self,'name'))

class EventTypes(reports.Report):
    model = EventType
    column_names = 'name build_method template *'

    
class Component(mixins.AutoUser,
                mixins.CreatedModified):
    """
    The `user` field is the iCal:ORGANIZER
    """
    class Meta:
        abstract = True
        
    start_date = models.DateField(
        verbose_name=_("Start date")) # iCal:DTSTART
    start_time = models.TimeField(
        blank=True,null=True,
        verbose_name=_("Start time"))# iCal:DTSTART
    summary = models.CharField(_("Summary"),max_length=200,blank=True) # iCal:SUMMARY
    description = fields.RichTextField(_("Description"),blank=True,format='html')
    access_class = AccessClass.field() # iCal:CLASS
    sequence = models.IntegerField(_("Revision"),default=0)
    alarm_value = models.IntegerField(_("Alarm value"),null=True,blank=True)
    alarm_unit = DurationUnit.field(_("Alarm unit"),null=True,blank=True)
    dt_alarm = models.DateTimeField(
        blank=True,null=True,editable=False)
    
    def __unicode__(self):
        return self._meta.verbose_name + " #" + str(self.pk)
        
    def save(self,*args,**kw):
        if self.alarm_unit:
            if not self.start_date:
                self.start_date = datetime.date.today()
            if self.start_time:
                dt = datetime.datetime.combine(self.start_date,self.start_time)
            else:
                d = self.start_date
                dt = datetime.datetime(d.year,d.month,d.day)
            self.dt_alarm = add_duration(dt,-self.alarm_value,self.alarm_unit)
        else:
            self.dt_alarm = None
        super(Component,self).save(*args,**kw)
        
    def summary_row(self,ui,rr,**kw):
        html = contacts.PartnerDocument.summary_row(self,ui,rr,**kw)
        if self.summary:
            html += '&nbsp;: %s' % cgi.escape(force_unicode(self.summary))
            #~ html += ui.href_to(self,force_unicode(self.summary))
        html += _(" on ") + babel.dtos(self.start_date)
        return html
        



#~ class Event(Component,contacts.PartnerDocument):
class Event(Component,mixins.TypedPrintable):
    "Deserves more documentation."
  
    class Meta:
        verbose_name = _("Event")
        verbose_name_plural = _("Events")
        abstract = True
        
    end_date = models.DateField(
        blank=True,null=True,
        verbose_name=_("End date"))
    end_time = models.TimeField(
        blank=True,null=True,
        verbose_name=_("End time"))
    transparent = models.BooleanField(_("Transparent"),default=False)
    type = models.ForeignKey(EventType,verbose_name=_("Event Type"),null=True,blank=True)
    place = models.ForeignKey(Place,verbose_name=_("Place"),null=True,blank=True) # iCal:LOCATION
    priority = Priority.field(_("Priority"),null=True,blank=True) # iCal:PRIORITY
    status = EventStatus.field(_("Status"),null=True,blank=True) # iCal:STATUS
    duration_value = models.IntegerField(_("Duration value"),null=True,blank=True) # iCal:DURATION
    duration_unit = DurationUnit.field(null=True,blank=True) # iCal:DURATION
    repeat_value = models.IntegerField(_("Repeat every"),null=True,blank=True) # iCal:DURATION
    repeat_unit = DurationUnit.field(verbose_name=_("Repeat every"),null=True,blank=True) # iCal:DURATION

#~ class Task(Component,contacts.PartnerDocument):
class Task(mixins.Owned,Component):
    """
    The owner of a Task is the record that caused the automatich creation.
    Non-automatic tasks always have an empty `owner` field.
    The owner and auto_type fields are hidden to the user.
    """
  
    class Meta:
        verbose_name = _("Task")
        verbose_name_plural = _("Tasks")
        abstract = True
        
    due_date = models.DateField(
        blank=True,null=True,
        verbose_name=_("Due date"))
    due_time = models.TimeField(
        blank=True,null=True,
        verbose_name=_("Due time"))
    done = models.BooleanField(_("Done"),default=False) # iCal:COMPLETED
    percent = models.IntegerField(_("Duration value"),null=True,blank=True) # iCal:PERCENT
    status = TaskStatus.field(null=True,blank=True) # iCal:STATUS
    
    auto_type = models.IntegerField(null=True,blank=True,editable=False) 
    
    def disabled_fields(self,request):
        if self.auto_type:
            return settings.LINO.TASK_AUTO_FIELDS
        return []
        

    @classmethod
    def site_setup(cls,lino):
        lino.TASK_AUTO_FIELDS= reports.fields_list(cls,
            '''start_date start_time summary''')

    def save(self,*args,**kw):
        if self.owner:
            #~ if self.owner.__class__.__name__ == 'Person':
                #~ self.person = self.owner
            #~ elif self.owner.__class__.__name__ == 'Company':
                #~ self.company = self.owner
            m = getattr(self.owner,'update_owned_task',None)
            if m:
                m(self)
        super(Task,self).save(*args,**kw)

    def __unicode__(self):
        return "#" + str(self.pk)
        
    def summary_row(self,ui,rr,**kw):
        #~ if self.owner and not self.auto_type:
        if self.owner and not self.owner.__class__.__name__ in ('Person','Company'):
            html = ui.href_to(self)
            html += " (%s)" % reports.summary_row(self.owner,ui,rr)
            if self.summary:
                html += '&nbsp;: %s' % cgi.escape(force_unicode(self.summary))
                #~ html += ui.href_to(self,force_unicode(self.summary))
            html += _(" on ") + babel.dtos(self.start_date)
            return html
        return super(Task,self).summary_row(ui,rr,**kw)
        

class Events(reports.Report):
    model = 'cal.Event'
    column_names = 'start_date start_time summary status *'
    
class Tasks(reports.Report):
    model = 'cal.Task'
    column_names = 'start_date summary done status *'
    #~ hidden_columns = set('owner_id owner_type'.split())
    
#~ class EventsByOwner(Events):
    #~ fk_name = 'owner'
    
class TasksByOwner(Tasks):
    fk_name = 'owner'
    #~ hidden_columns = set('owner_id owner_type'.split())

class MyEvents(mixins.ByUser):
    model = 'cal.Event'
    #~ label = _("My Events")
    order_by = ["start_date","start_time"]
    column_names = 'start_date start_time summary status *'
    
class MyTasks(mixins.ByUser):
    model = 'cal.Task'
    #~ label = _("My Tasks")
    order_by = ["start_date","start_time"]
    column_names = 'start_date summary done status *'


class Attendance(contacts.PartnerDocument,
      mixins.CachedPrintable,
      mixins.Sendable):
    """An Attendance is when somebody possibly attends to an Event.
"Somebody" means a Person, a Company or both.
An unconfirmed attendance is when the partner has been invited.
"""
    class Meta:
        verbose_name = _("Attendance")
        verbose_name_plural = _("Attendances")
        #~ abstract = True
        
    event = models.ForeignKey('cal.Event',
        verbose_name=_("Event")) 
        
    confirmed = models.DateField(
        blank=True,null=True,
        verbose_name=_("Confirmed"))

    remark = models.CharField(
        _("Remark"),max_length=200,blank=True)

    def __unicode__(self):
        return self._meta.verbose_name + " #" + str(self.pk)
        
    @classmethod
    def setup_report(cls,rpt):
        mixins.CachedPrintable.setup_report(rpt)
        mixins.Sendable.setup_report(rpt)
        
class Attendances(reports.Report):
    model = Attendance
    column_names = 'person company confirmed remark event *'
    
class AttendancesByEvent(Attendances):
    fk_name = 'event'

class AttendancesByPerson(Attendances):
    fk_name = 'person'
    column_names = 'event confirmed remark company * person'

class AttendancesByCompany(Attendances):
    fk_name = 'company'
    column_names = 'event confirmed remark person * company'

    
def tasks_summary(ui,user,days_back=None,days_forward=None,**kw):
    """Return a HTML summary of all open reminders for this user.
    """
    Task = resolve_model('cal.Task')
    Event = resolve_model('cal.Event')
    #~ today = datetime.date.today()
    today = datetime.datetime.now()
    #~ if days_back is None:
        #~ back_until = None
    #~ else:
        #~ back_until = today - datetime.timedelta(days=days_back)
    
    past = {}
    future = {}
    def add(task):
        if task.dt_alarm < today:
            lookup = past
        else:
            lookup = future
        day = lookup.get(task.dt_alarm,None)
        if day is None:
            day = [task]
            lookup[task.dt_alarm] = day
        else:
            day.append(task)
            
    #~ filterkw = { 'due_date__lte' : today }
    filterkw = {}
    if days_back is not None:
        filterkw.update({ 
            'dt_alarm__gte' : today - datetime.timedelta(days=days_back)
        })
    if days_forward is not None:
        filterkw.update({ 
            'dt_alarm__lte' : today + datetime.timedelta(days=days_forward)
        })
    filterkw.update(dt_alarm__isnull=False)
    filterkw.update(user=user)
    
    
    
    for o in Event.objects.filter(**filterkw).order_by('dt_alarm'):
        add(o)
        
    filterkw.update(done=False)
            
    for task in Task.objects.filter(**filterkw).order_by('dt_alarm'):
        add(task)
        
    def loop(lookup,reverse):
        sorted_days = lookup.keys()
        sorted_days.sort()
        if reverse: 
            sorted_days.reverse()
        for day in sorted_days:
            yield '<h3>'+dtosl(day) + '</h3>'
            yield reports.summary(ui,lookup[day],**kw)
            
    #~ cells = ['Ausblick'+':<br>',cgi.escape(u'Rückblick')+':<br>']
    cells = [
      cgi.escape(_('Upcoming reminders')) + ':<br>',
      cgi.escape(_('Past reminders')) + ':<br>'
    ]
    for s in loop(future,False):
        cells[0] += s
    for s in loop(past,True):
        cells[1] += s
    s = ''.join(['<td valign="top" bgcolor="#eeeeee" width="30%%">%s</td>' % s for s in cells])
    s = '<table cellspacing="3px" bgcolor="#ffffff"><tr>%s</tr></table>' % s
    s = '<div class="htmlText">%s</div>' % s
    return s

SKIP_AUTO_TASKS = False 
"See :blog:`/blog/2011/0727`"

def update_auto_task(autotype,user,date,summary,owner,**defaults):
    """Creates, updates or deletes the automatic :class:`Task` 
    related to the specified `owner`.
    """
    if SKIP_AUTO_TASKS: return 
    #~ if is_deserializing(): return 
    Task = resolve_model('cal.Task')
    ot = ContentType.objects.get_for_model(owner.__class__)
    if date:
        #~ defaults = owner.get_auto_task_defaults(**defaults)
        defaults.setdefault('user',user)
        task,created = Task.objects.get_or_create(
          defaults=defaults,
          owner_id=owner.pk,
          owner_type=ot,
          auto_type=autotype)
        task.user = user
        if summary:
            task.summary = force_unicode(summary)
        #~ obj.summary = summary
        task.start_date = date
        #~ for k,v in kw.items():
            #~ setattr(obj,k,v)
        #~ obj.due_date = date - delta
        #~ print 20110712, date, date-delta, obj2str(obj,force_detailed=True)
        #~ owner.update_owned_task(task)
        task.save()
    else:
        try:
            obj = Task.objects.get(owner_id=owner.pk,
                    owner_type=ot,auto_type=autotype)
        except Task.DoesNotExist:
            pass
        else:
            obj.delete()
        

def migrate_reminder(obj,reminder_date,reminder_text,
                         delay_value,delay_type,reminder_done):
    """This was used only for migrating to 1.2.0, see :mod:`lino.apps.dsbe.migrate`.
    """
    def delay2alarm(delay_type):
        if delay_type == 'D': return DurationUnit.days
        if delay_type == 'W': return DurationUnit.weeks
        if delay_type == 'M': return DurationUnit.months
        if delay_type == 'Y': return DurationUnit.years
      
    #~ # These constants must be unique for the whole Lino Site.
    #~ # Keep in sync with auto types defined in lino.apps.dsbe.models.Person
    #~ REMINDER = 5
    
    if reminder_text:
        summary = reminder_text
    else:
        summary = _('due date reached')
    
    update_auto_task(
      None, # REMINDER,
      obj.user,
      reminder_date,
      summary,obj,
      done = reminder_done,
      alarm_value = delay_value,
      alarm_unit = delay2alarm(delay_type))
      



def setup_main_menu(site,ui,user,m): pass

def setup_my_menu(site,ui,user,m): 
    m.add_action('cal.MyTasks')
    m.add_action('cal.MyEvents')
  
def setup_config_menu(site,ui,user,m): 
    m  = m.add_menu("cal",_("~Calendar"))
    m.add_action('cal.Places')
    m.add_action('cal.EventTypes')
  
def setup_explorer_menu(site,ui,user,m):
    m.add_action('cal.Events')
    m.add_action('cal.Tasks')
    m.add_action('cal.Attendances')
  