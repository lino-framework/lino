## Copyright 2009-2010 Luc Saffre
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
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext_lazy as _

from lino import reports
from lino.utils.printable import Printable, PrintableType, TypedPrintable

class AutoUser(models.Model):
  
    class Meta:
        abstract = True
        
    user = models.ForeignKey("auth.User",verbose_name=_("user")) # ,blank=True,null=True)
    
    def on_create(self,req):
        u = req.get_user()
        if u is not None:
            self.user = u
        

class Reminder(AutoUser):
  
    class Meta:
        abstract = True
        
    reminder_date = models.DateField(_("Reminder date"),
      blank=True,null=True)
    reminder_text = models.CharField(_("Reminder text"),
      max_length=200,blank=True,null=True)
    
    def summary_row(self,ui,rr,**kw):
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

def reminders_summary(ui,user,*args,**kw):
    s= ''
    date = datetime.date.today()
    days = {}
    objects = []
    def add(obj):
        day = days.get(obj.reminder_date,None)
        if day is None:
            day = [obj]
            days[obj.reminder_date] = day
        else:
            day.append(obj)
        
    for model in models.get_models():
        if issubclass(model,Reminder):
            for obj in model.objects.filter(
                user__exact=user,reminder_date__lte=date).order_by('reminder_date'):
                add(obj)
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
    
class MultiTableBase(models.Model):
  
    """
    Mixin for Models that use `Multi-table inheritance 
    <http://docs.djangoproject.com/en/dev/topics/db/models/#multi-table-inheritance>`__.
    Subclassed by :class:`lino.modlib.journals.models.Journaled`.
    """
    class Meta:
        abstract = True
    
    def get_child_model(self):
        return self.__class__
        
    def get_child_instance(self):
        model = self.get_child_model()
        if model is self.__class__:
            return self
        related_name = model.__name__.lower()
        return getattr(self,related_name)
        
class Owned(models.Model):
  
    owner_type = models.ForeignKey(ContentType,verbose_name=_('Owner type'))
    owner_id = models.PositiveIntegerField(verbose_name=_('Owner'))
    owner = generic.GenericForeignKey('owner_type', 'owner_id')
    
    def owner_id_choices(self,owner_type):
      #~ ct = ContentType.objects.get(pk=owner_type)
      return owner_type.model_class().objects.all()
    owner_id_choices.instance_values = True
    owner_id_choices = classmethod(owner_id_choices)
        
    def get_owner_id_display(self,value):
        return unicode(self.owner_type.get_object_for_this_type(pk=value))
            

class PartnerDocument(models.Model):
    class Meta:
        abstract = True
    person = models.ForeignKey("contacts.Person",blank=True,null=True,verbose_name=_("Person"))
    company = models.ForeignKey("contacts.Company",blank=True,null=True,verbose_name=_("Company"))

