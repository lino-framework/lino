# -*- coding: UTF-8 -*-
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
from lino.utils.babel import dtosl

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
    def get_reminders(model,ui,user,today,back_until):
        """
        yield a list of reminders for this model and user for the specified date `today`.
        `back_until` is a date *before* `today` and may be None.
        """
        #~ print "get_reminders()"
        #~ for obj in model.objects.filter(
            #~ user__exact=user,reminder_date__lte=pivot).order_by('reminder_date'):
        for obj in model.objects.filter(user__exact=user,
              reminder_date__isnull=False, 
              reminder_done__exact=False).order_by('reminder_date'):
            pivot = today + time_delta(obj.delay_type,obj.delay_value)
            #~ print obj, pivot
            if obj.reminder_date <= pivot:
                if back_until is None or obj.reminder_date > back_until:
                    yield ReminderEntry(obj.reminder_date,obj.get_reminder_html(ui,user))
                        #~ target=obj,
                        #~ fmt='detail')
                        
    def get_reminder_html(self,ui,user):
        url = ui.get_detail_url(self,fmt='detail')
        if self.reminder_text:
            s = self.reminder_text
        else:
            s = _('due date reached')
        return '<a href="%s">%s</a>&nbsp;: %s' % (url,unicode(self),cgi.escape(s))

    @chooser(simple_values=True)
    def reminder_text_choices(self):
        return REMINDER_TEXT_CHOICES
    #~ reminder_text_choices.simple_values = True
    #~ reminder_text_choices = classmethod(reminder_text_choices)
    
    #~ def create_reminder_text_choice(self,text):
        #~ dblogger.warning("Would create reminder_text %r",text)
        #~ print text
        #~ return text
    
class ReminderEntry:
    """
    The class of volatile objects that `get_reminders`is expected to yield.
    """
    #~ def __init__(self,target,date,text,**target_kw):
    #~ def __init__(self,date,text,target=None,target_text=None,**target_kw):
    def __init__(self,date,text):
        """
        date: due date of this reminder
        text: the 
        target: the object this reminder links to
        """
        self.date = date
        #~ self.target = target
        #~ self.target_kw = target_kw
        #~ if target is not None:
            #~ if target_text is None:
                #~ target_text = target.get_reminder_target_text()
        #~ self.target_text = target_text 
        self.text = text
        #~ self._lino_model_report = target._lino_model_report
        #~ self.pk = target.pk
        #~ self.__unicode__ = target.__unicode__
        
    def summary_row(self,ui,rr,**kw):
        return self.text
        #~ url = ui.get_detail_url(self.target,**self.target_kw)
        #~ s = '<a href="%s">%s</a>' % (url,cgi.escape(self.target_text))
        #~ a = self.target.__class__._lino_model_report.detail_action
        #~ params = dict(record_id=self.target.pk)
        #~ s = ui.action_href(a,unicode(self.target),**params)
        #~ if self.text:
            #~ s += ' <b>' + cgi.escape(self.text) + '</b> '
            #~ s += ' (' + cgi.escape(self.text) + ')'
            #~ s += '&nbsp;: ' + cgi.escape(self.text)
        #~ return s

def reminders_summary(ui,user,days_back=None,**kw):
    """
    Return a HTML summary of all open reminders for this user
    """
    date_from = datetime.date.today()
    if days_back is None:
        back_until = None
    else:
        back_until = date_from - datetime.timedelta(days=days_back)
    
    past = {}
    future = {}
    #~ days = {}
    objects = []
    def add(rem):
        if rem.date < date_from:
            lookup = past
        else:
            lookup = future
        day = lookup.get(rem.date,None)
        if day is None:
            day = [rem]
            lookup[rem.date] = day
        else:
            day.append(rem)
        
    for model in models.get_models():
        #~ if issubclass(model,Reminder):
            #~ for obj in model.objects.filter(
                #~ user__exact=user,reminder_date__lte=date).order_by('reminder_date'):
                #~ ReminderEntry(obj,obj,
                #~ add(obj)
        if hasattr(model,'get_reminders'):
            for rem in model.get_reminders(ui,user,date_from,back_until):
                add(rem)

    def loop(lookup,reverse):
        sorted_days = lookup.keys()
        sorted_days.sort()
        if reverse: 
            sorted_days.reverse()
        for day in sorted_days:
            yield '<h3>'+dtosl(day) + '</h3>'
            yield reports.summary(ui,lookup[day],**kw)
            
    cells = ['Ausblick'+':<br>',cgi.escape(u'Rückblick')+':<br>']
    for s in loop(future,False):
        cells[0] += s
    for s in loop(past,True):
        cells[1] += s
    s = ''.join(['<td valign="top" bgcolor="#eeeeee" width="30%%">%s</td>' % s for s in cells])
    s = '<table cellspacing="3px" bgcolor="#ffffff"><tr>%s</tr></table>' % s
    s = '<div class="htmlText">%s</div>' % s
    return s
    #~ objects.sort(lambda a,b:cmp(a.reminder_date,b.reminder_date))
    #~ return objects
    
#~ class RemindersByUser(reports.Report):
    #~ fk_name = 'user'
    #~ model = Reminder
    
    #~ def get_request_queryset(self,rr):
        #~ return reminders(rr.user)
    
  
  
