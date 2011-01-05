## Copyright 2010 Luc Saffre
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

class Reminder(AutoUser):
  
    class Meta:
        abstract = True
        
    reminder_date = models.DateField(_("Reminder date"),
      blank=True,null=True)
    reminder_text = models.CharField(_("Reminder text"),
      max_length=200,blank=True,null=True)
      
    @classmethod
    def get_reminders(model,date,user):
        for obj in model.objects.filter(
            user__exact=user,reminder_date__lte=date).order_by('reminder_date'):
            yield ReminderEntry(obj,obj.reminder_date,obj.reminder_text,fmt='detail')
    
    def unused_summary_row(self,ui,rr,**kw):
        #~ s = u'<b>%s</b> :'
        #~ s = cgi.escape(self.reminder_date.isoformat()) + ": "
        s = ''
        if self.reminder_text:
            s += '<b>' + cgi.escape(self.reminder_text) + '</b> '
        s += '<a href="%s" target="_blank">%s</a>' % (
          ui.get_detail_url(self,fmt='detail'),
          #~ rr.get_request_url(str(obj.pk),fmt='detail'),
          unicode(self))
        return s
        
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
        s = ''
        if self.text:
            s += '<b>' + cgi.escape(self.text) + '</b> '
        s += '<a href="%s" target="_blank">%s</a>' % (
          ui.get_detail_url(self,**self.target_kw),
          unicode(self.target))
        return s

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
    
  
  
def unused_reminders_summary(ui,user,*args,**kw):
    #~ m = RemindersByUser().slave_as_summary_meth(ui,row_separator)
    return reports.summary(ui,reminders(user),*args,**kw)
    #~ return m(user)
