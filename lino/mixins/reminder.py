## Copyright 2010-2011 Luc Saffre
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

import cgi
import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _
from lino.mixins import AutoUser
from lino.utils.choosers import chooser

from lino import reports

REMINDER_TEXT_CHOICES = [
  _("test"),
  _("must check"),
]

DELAY_TYPE_CHOICES = [
  ('D', _("days")),
  ('W', _("weeks")),
  ('M', _("months")),
  ('Y', _("years")),
]

def time_delta(delay_type,delay_value):
    if delay_type == 'D':
        return datetime.timedelta(days=delay_value)
    if delay_type == 'W':
        return datetime.timedelta(days=delay_value*7)
    if delay_type == 'M':
        return datetime.timedelta(days=delay_value*30)
        #~ return datetime.timedelta(months=delay_value)
    if delay_type == 'Y':
        return datetime.timedelta(days=delay_value*365)
        #~ return datetime.timedelta(years=delay_value)

  


class Reminder(AutoUser):
  
    class Meta:
        abstract = True
        
    reminder_date = models.DateField(_("Due date"),
      blank=True,null=True)
    reminder_text = models.CharField(_("Reminder text"),
      max_length=200,blank=True,null=True)
    delay_value = models.IntegerField(_("Delay (value)"),
      default=0)
    delay_type = models.CharField(_("Delay (unit)"),
        max_length=1,default='D',
        choices=DELAY_TYPE_CHOICES)
    reminder_done = models.BooleanField(
        verbose_name=_("Done"),
        default=False)
      
      
    @classmethod
    def get_reminders(model,today,user):
        #~ print "get_reminders()"
        #~ for obj in model.objects.filter(
            #~ user__exact=user,reminder_date__lte=pivot).order_by('reminder_date'):
        for obj in model.objects.filter(user__exact=user,
              reminder_date__isnull=False, 
              reminder_done__exact=False).order_by('reminder_date'):
            pivot = today + time_delta(obj.delay_type,obj.delay_value)
            #~ print obj, pivot
            if obj.reminder_date <= pivot:
                msg = obj.reminder_text
                if not msg:
                    msg = _('due date reached')
                yield ReminderEntry(obj,obj.reminder_date,msg,fmt='detail')

    @chooser(simple_values=True)
    def reminder_text_choices(self):
        return REMINDER_TEXT_CHOICES
    #~ reminder_text_choices.simple_values = True
    #~ reminder_text_choices = classmethod(reminder_text_choices)
    
class ReminderEntry:
    def __init__(self,target,date,text,**target_kw):
        self.date = date
        self.target = target
        self.target_kw = target_kw
        self.text = text
        self._lino_model_report = target._lino_model_report
        self.pk = target.pk
        self.__unicode__ = target.__unicode__
        
    def summary_row(self,ui,rr,**kw):
        a = self.target.__class__._lino_model_report.detail_action
        params = dict(record_id=self.target.pk)
        s = ui.action_href(a,unicode(self.target),**params)
        if self.text:
            #~ s += ' <b>' + cgi.escape(self.text) + '</b> '
            s += ' (' + cgi.escape(self.text) + ')'
        return s

        #~ s += '<a href="%s" target="_blank">%s</a>' % (
          #~ ui.get_detail_url(self,**self.target_kw),
          #~ unicode(self.target))
        #~ return s

def reminders_summary(ui,user,*args,**kw):
    s= ''
    date = datetime.date.today()
    days = {}
    objects = []
    def add(rem):
        day = days.get(rem.date,None)
        if day is None:
            day = [rem]
            days[rem.date] = day
        else:
            day.append(rem)
        
    for model in models.get_models():
        #~ if issubclass(model,Reminder):
            #~ for obj in model.objects.filter(
                #~ user__exact=user,reminder_date__lte=date).order_by('reminder_date'):
                #~ ReminderEntry(obj,obj,
                #~ add(obj)
        if hasattr(model,'get_reminders'):
            for rem in model.get_reminders(date,user):
                add(rem)

    sorted_days = days.keys()
    sorted_days.sort()
    for day in sorted_days:
        s += '<h3>'+day.isoformat() + '</h3>'
        s += reports.summary(ui,days[day],'<br/>')
    return s
    #~ objects.sort(lambda a,b:cmp(a.reminder_date,b.reminder_date))
    #~ return objects
    
#~ class RemindersByUser(reports.Report):
    #~ fk_name = 'user'
    #~ model = Reminder
    
    #~ def get_request_queryset(self,rr):
        #~ return reminders(rr.user)
    
  
  
