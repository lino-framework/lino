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
This module deserves more documentation.

It defines tables like :class:`Task` and :class:`Event` 

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

from lino.modlib.contacts import models as contacts

from lino.modlib.cal.utils import EventStatus, \
    TaskStatus, DurationUnit, Priority, AccessClass

from lino.utils.babel import dtosl

class Place(models.Model):
    name = models.CharField(_("Name"),max_length=200)
  

class Component(mixins.AutoUser,
                mixins.CreatedModified,
                contacts.PartnerDocument):
    """
    The `user` field is the iCal:ORGANIZER
    """
    class Meta:
        abstract = True
        
    summary = models.CharField(_("Summary"),max_length=200,blank=True) # iCal:SUMMARY
    description = fields.RichTextField(_("Description"),blank=True,format='html')
    access_class = AccessClass.field() # iCal:CLASS
    sequence = models.IntegerField(_("Revision"),default=0)
    alarm_value = models.IntegerField(_("Alarm value"),null=True,blank=True)
    alarm_unit = DurationUnit.field(null=True,blank=True)
    
    def __unicode__(self):
        return self._meta.verbose_name + " #" + str(self.pk)
        
    def summary_row(self,ui,rr,**kw):
        #~ linkkw = {}
        #~ linkkw.update(fmt='detail')
        #~ url = ui.get_detail_url(self,**linkkw)
        #~ html = '<a href="%s">#%s</a>&nbsp;: %s' % (url,self.pk,
            #~ cgi.escape(force_unicode(self.summary)))
        if self.owner:
            html = ui.href_to(self)
            html += " (%s)" % reports.summary_row(self.owner,ui,rr)
        else:
            html = contacts.PartnerDocument.summary_row(self,ui,rr,**kw)
        if self.summary:
            html += '&nbsp;: %s' % cgi.escape(force_unicode(self.summary))
            #~ html += ui.href_to(self,force_unicode(self.summary))
        return html
        
    
    
#~ class Event(Component,contacts.PartnerDocument):
class Event(Component):
  
    class Meta:
        verbose_name = _("Event")
        verbose_name_plural = _("Events")
        #~ abstract = True
        
    date = models.DateField(
        verbose_name=_("Start date")) # iCal:DTSTART
    time = models.TimeField(
        blank=True,null=True,
        verbose_name=_("Start time"))# iCal:DTSTART
    end_date = models.DateField(
        blank=True,null=True,
        verbose_name=_("End date"))
    end_time = models.TimeField(
        blank=True,null=True,
        verbose_name=_("End time"))
    transparent = models.BooleanField(_("Transparent"),default=False)
    place = models.ForeignKey(Place,verbose_name=_("Place"),null=True,blank=True) # iCal:LOCATION
    priority = Priority.field(null=True,blank=True) # iCal:PRIORITY
    status = EventStatus.field(null=True,blank=True) # iCal:STATUS
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
        #~ abstract = True
        
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
            '''due_date due_time summary''')

    def save(self,*args,**kw):
        m = getattr(self.owner,'update_owned_task',None)
        if m:
            m(self)
        super(Task,self).save(*args,**kw)

    def __unicode__(self):
        return "#" + str(self.pk)
        
class Places(reports.Report):
    model = Place
    
class Events(reports.Report):
    model = Event
    column_names = 'date time summary status *'
    
class Tasks(reports.Report):
    model = Task
    column_names = 'due_date summary done status *'
    #~ hidden_columns = set('owner_id owner_type'.split())
    
#~ class EventsByOwner(Events):
    #~ fk_name = 'owner'
    
class EventsByPerson(Events):
    fk_name = 'person'
    
class EventsByCompany(Events):
    fk_name = 'company'
    

class TasksByOwner(Tasks):
    fk_name = 'owner'
    #~ hidden_columns = set('owner_id owner_type'.split())

class TasksByPerson(Tasks):
    fk_name = 'person'
    
class TasksByCompany(Tasks):
    fk_name = 'company'
    
class MyEvents(mixins.ByUser):
    model = Event
    label = _("My Events")
    order_by = ["date","time"]
    column_names = 'date time summary status *'
    
class MyTasks(mixins.ByUser):
    model = Task
    label = _("My Tasks")
    order_by = ["due_date","due_time"]
    column_names = 'due_date summary done status *'
    
    
def tasks_summary(ui,user,days_back=None,days_forward=None,**kw):
    """
    Return a HTML summary of all open reminders for this user
    """
    today = datetime.date.today()
    #~ if days_back is None:
        #~ back_until = None
    #~ else:
        #~ back_until = today - datetime.timedelta(days=days_back)
    
    past = {}
    future = {}
    def add(task):
        if task.due_date < today:
            lookup = past
        else:
            lookup = future
        day = lookup.get(task.due_date,None)
        if day is None:
            day = [task]
            lookup[task.due_date] = day
        else:
            day.append(task)
            
    #~ filterkw = { 'due_date__lte' : today }
    filterkw = {}
    if days_back is not None:
        filterkw.update({ 
            'due_date__gte' : today - datetime.timedelta(days=days_back)
        })
    if days_forward is not None:
        filterkw.update({ 
            'due_date__lte' : today + datetime.timedelta(days=days_forward)
        })
    filterkw.update(user=user)
    filterkw.update(done=False)
            
    for task in Task.objects.filter(**filterkw).order_by('due_date'):
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



def update_auto_task(autotype,user,date,summary,owner,**defaults):
    """Creates, updates or deletes the automatic :class:`Task` 
    related to the specified `owner`.
    """
    ot = ContentType.objects.get_for_model(owner.__class__)
    if date:
        #~ defaults = owner.get_auto_task_defaults(**defaults)
        defaults.setdefault('user',user)
        obj,created = Task.objects.get_or_create(
          defaults=defaults,
          owner_id=owner.pk,
          owner_type=ot,
          auto_type=autotype)
        obj.user = user
        if summary:
            obj.summary = force_unicode(summary)
        #~ obj.summary = summary
        obj.due_date = date
        #~ for k,v in kw.items():
            #~ setattr(obj,k,v)
        #~ obj.due_date = date - delta
        #~ print 20110712, date, date-delta, obj2str(obj,force_detailed=True)
        owner.update_owned_task(obj)
        obj.save()
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
  
    def delay2alarm(delay_type):
        if delay_type == 'D': return DurationUnit.days
        if delay_type == 'W': return DurationUnit.weeks
        if delay_type == 'M': return DurationUnit.months
        if delay_type == 'Y': return DurationUnit.years
      
    # These constants must be unique for the whole Lino Site.
    # Keep in sync with auto types defined in lino.apps.dsbe.models.Person
    REMINDER = 5
    
    if reminder_text:
        summary = reminder_text
    else:
        summary = _('due date reached')
    
    
    update_auto_task(
      REMINDER,
      obj.user,
      reminder_date,
      summary,self,defaults=dict(
        done = reminder_done,
        alarm_value = delay_value,
        alarm_unit = delay2alarm(delay_type)))
      
