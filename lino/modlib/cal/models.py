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

class Place(models.Model):
    name = models.CharField(_("Name"),max_length=200)
  

class Component(mixins.AutoUser,mixins.Owned,mixins.CreatedModified):
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
    
    
    
#~ class Event(Component,contacts.PartnerDocument):
class Event(Component):
  
    #~ class Meta:
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
class Task(Component):
  
    #~ class Meta:
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
            '''due_date due_time summary owner_type owner_id''')

    def summary_row(self,ui,rr,**kw):
        return self.summary

class Places(reports.Report):
    model = Place
    
class Events(reports.Report):
    model = Event
    column_names = 'date time summary status *'
    
class Tasks(reports.Report):
    model = Task
    column_names = 'due_date summary status done *'
    
class EventsByOwner(Events):
    fk_name = 'owner'
    
#~ class EventsByPerson(Events):
    #~ fk_name = 'person'
    
#~ class EventsByCompany(Events):
    #~ fk_name = 'company'
    

class TasksByOwner(Tasks):
    fk_name = 'owner'
    hidden_columns = set('owner_id owner_type'.split())

#~ class TasksByPerson(Tasks):
    #~ fk_name = 'person'
    
#~ class TasksByCompany(Tasks):
    #~ fk_name = 'company'
    
class MyEvents(mixins.ByUser):
    model = Event
    label = _("My Events")
    order_by = ["date","time"]
    column_names = 'date time summary status *'
    
class MyTasks(mixins.ByUser):
    model = Task
    label = _("My Tasks")
    order_by = ["due_date","due_time"]
    column_names = 'summary status done *'
    
    
def check_auto_task(autotype,user,date,summary,owner,**kw):
    if date:
        ot = ContentType.objects.get_for_model(owner.__class__)
        kw.setdefault('user',user)
        obj,created = Task.objects.get_or_create(
          defaults=kw,
          owner_id=owner.pk,
          owner_type=ot,
          auto_type=autotype)
        obj.user = user
        obj.summary = force_unicode(summary)
        obj.due_date = date
        #~ for k,v in kw.items():
            #~ setattr(obj,k,v)
        #~ obj.due_date = date - delta
        #~ print 20110712, date, date-delta, obj2str(obj,force_detailed=True)
        obj.save()
    
