# -*- coding: UTF-8 -*-
## Copyright 2011-2013 Luc Saffre
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
The :xfile:`models.py` module for the :mod:`lino.modlib.cal` app.
"""

from __future__ import unicode_literals

import logging
logger = logging.getLogger(__name__)

import cgi
import datetime
import dateutil

from django.conf import settings
from django.db import models
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import pgettext_lazy as pgettext
#~ from django.utils.translation import string_concat
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import force_unicode
from django.db.models import loading
from django.core import exceptions
from django.utils.importlib import import_module

from north import dbutils
from north.dbutils import dtosl


from lino import mixins
from lino import dd
#~ from lino.core import reports
from lino.core import actions
from lino.utils import AttrDict
from lino.utils import ONE_DAY
from lino.core import constants

from lino.utils.xmlgen.html import E

from lino.modlib.cal.utils import (
    DurationUnits, Recurrencies, 
    setkw, dt2kw, 
    when_text, 
    Weekdays, AccessClasses, CalendarAction)


from lino.modlib.cal.workflows import (
    TaskStates, EventStates, GuestStates)
    
from lino.modlib.cal.workflows import take    


class CalendarType(object):
    
    def validate_calendar(self,cal):
        pass
        
class LocalCalendar(CalendarType):
    label = "Local Calendar"
  
class GoogleCalendar(CalendarType):
    label = "Google Calendar"
    def validate_calendar(self,cal):
        if not cal.url_template:
            cal.url_template = \
            "https://%(username)s:%(password)s@www.google.com/calendar/dav/%(username)s/"
  
CALENDAR_CHOICES = []
CALENDAR_DICT = {}

def register_calendartype(name,instance):
    CALENDAR_DICT[name] = instance
    CALENDAR_CHOICES.append((name,instance.label))
    
register_calendartype('local',LocalCalendar())
register_calendartype('google',GoogleCalendar())
    

class RemoteCalendar(dd.Sequenced):
    """
    Remote calendars will be synchronized by
    :mod:`lino.modlib.cal.management.commands.watch_calendars`,
    and local modifications will be sent back to the remote calendar.
    """
    class Meta:
        abstract = settings.SITE.is_abstract_model('cal.RemoteCalendar')
        verbose_name = _("Remote Calendar")
        verbose_name_plural = _("Remote Calendars")
        ordering = ['seqno']
        
    type = models.CharField(_("Type"),max_length=20,
        default='local',
        choices=CALENDAR_CHOICES)
    url_template = models.CharField(_("URL template"),
        max_length=200,blank=True) # ,null=True)
    username = models.CharField(_("Username"),
        max_length=200,blank=True) # ,null=True)
    password = dd.PasswordField(_("Password"),
        max_length=200,blank=True) # ,null=True)
    readonly = models.BooleanField(_("read-only"),default=False)
    
    def get_url(self):
        if self.url_template:
            return self.url_template % dict(
              username=self.username,
              password=self.password)
        return ''
                    
    def save(self,*args,**kw):
        ct = CALENDAR_DICT.get(self.type)
        ct.validate_calendar(self)
        super(RemoteCalendar,self).save(*args,**kw)



class Room(dd.BabelNamed):
    """
    A location where Events can happen.
    For a given Room you can see the :class:`EventsByRoom` 
    that happened (or will happen) there.
    A Room is BabelNamed (has a multilingual name).
    """
    class Meta:
        abstract = settings.SITE.is_abstract_model('cal.Room')
        verbose_name = _("Room")
        verbose_name_plural = _("Rooms")
        
    #~ def __unicode__(self):
        #~ s = dd.BabelNamed.__unicode__(self)
        #~ if self.company and self.company.city: 
            #~ s = '%s (%s)' % (self.company.city,s)
        #~ return s
        

        
  
class Rooms(dd.Table):
    help_text = _("List of rooms where calendar events can happen.")
    required = dd.required(user_groups='office',user_level='manager')
    model = 'cal.Room'
    detail_layout = """
    id name 
    cal.EventsByRoom
    """
    
class Priority(dd.BabelNamed):
    "The priority of a Task or Event."
    class Meta:
        verbose_name = _("Priority")
        verbose_name_plural = _('Priorities')
    ref = models.CharField(max_length='1')

class Priorities(dd.Table):
    help_text = _("List of possible priorities of calendar events.")
    required = dd.required(user_groups='office',user_level='manager')
    model = Priority
    column_names = 'name *'


class Started(dd.Model):
    class Meta:
        abstract = True
        
    start_date = models.DateField(
        blank=True,null=True,
        verbose_name=_("Start date")) # iCal:DTSTART
    start_time = models.TimeField(
        blank=True,null=True,
        verbose_name=_("Start time"))# iCal:DTSTART
    #~ start = dd.FieldSet(_("Start"),'start_date start_time')

    def save(self,*args,**kw):
        """
        Fills default value "today" to start_date
        """
        if not self.start_date:
            self.start_date = datetime.date.today()
        super(Started,self).save(*args,**kw)
        
    def set_datetime(self,name,value):
        """
        Given a datetime `value`, update the two corresponding 
        fields `FOO_date` and `FOO_time` 
        (where FOO is specified in `name` which must be 
        either "start" or "end").
        """
        #~ logger.info("20120119 set_datetime(%r)",value)
        setattr(self,name+'_date',value.date())
        t = value.time()
        if not t:
            t = None
        setattr(self,name+'_time',t)
        
    def get_datetime(self,name,altname=None):
        """
        Return a `datetime` value from the two corresponding 
        date and time fields.
        `name` can be 'start' or 'end'.
        """
        d = getattr(self,name+'_date')
        t = getattr(self,name+'_time')
        if not d and altname is not None: 
            d = getattr(self,altname+'_date')
            if not t and altname is not None: 
                t = getattr(self,altname+'_time')
        if not d: return None
        if t:
            return datetime.datetime.combine(d,t)
        else:
            return datetime.datetime(d.year,d.month,d.day)
        
class Ended(dd.Model):
    class Meta:
        abstract = True
    end_date = models.DateField(
        blank=True,null=True,
        verbose_name=_("End Date"))
    end_time = models.TimeField(
        blank=True,null=True,
        verbose_name=_("End Time"))
    #~ end = dd.FieldSet(_("End"),'end_date end_time')
    
  
    
  
class StartedSummaryDescription(Started):
    """
    """

    class Meta:
        abstract = True
        
    summary = models.CharField(_("Summary"),max_length=200,blank=True) # iCal:SUMMARY
    description = dd.RichTextField(_("Description"),blank=True,format='html')
    
    def __unicode__(self):
        return self._meta.verbose_name + " #" + str(self.pk)

    def summary_row(self,ar,**kw):
        elems = list(super(StartedSummaryDescription,self).summary_row(ar,**kw))
        
        #~ html = super(StartedSummaryDescription,self).summary_row(ar,**kw)
        if self.summary:
            elems.append(': %s' % self.summary)
            #~ html += '&nbsp;: %s' % cgi.escape(force_unicode(self.summary))
            #~ html += ui.href_to(self,force_unicode(self.summary))
        elems += [_(" on "), dbutils.dtos(self.start_date)]
        return elems
        
        


class Component(StartedSummaryDescription,
                 mixins.ProjectRelated,
                 mixins.UserAuthored,
                 mixins.Controllable,
                 mixins.CreatedModified):
    """
    Abstract base class for :class:`Event` and :class:`Task`.
    
    """
    workflow_state_field = 'state'
    
    manager_level_field = 'office_level'
    
    class Meta:
        abstract = True
        
    access_class = AccessClasses.field(blank=True,help_text=_("""\
Whether this is private, public or between.""")) # iCal:CLASS
    #~ access_class = models.ForeignKey(AccessClass,
        #~ blank=True,null=True,
        #~ help_text=_("""\
#~ Indicates whether this is private or public (or somewhere between)."""))
    sequence = models.IntegerField(_("Revision"),default=0)
    #~ alarm_value = models.IntegerField(_("Value"),null=True,blank=True,default=1)
    #~ alarm_unit = DurationUnit.field(_("Unit"),blank=True,
        #~ default=DurationUnit.days.value) # ,null=True) # note: it's a char field!
    #~ alarm = dd.FieldSet(_("Alarm"),'alarm_value alarm_unit')
    #~ dt_alarm = models.DateTimeField(_("Alarm time"),
        #~ blank=True,null=True,editable=False)
        
    auto_type = models.IntegerField(null=True,blank=True,editable=False) 
    
    #~ user_modified = models.BooleanField(_("modified by user"),
        #~ default=False,editable=False) 
    
    #~ rset = models.ForeignKey(RecurrenceSet,
        #~ verbose_name=_("Recurrence Set"),
        #~ blank=True,null=True)
    #~ rparent = models.ForeignKey('self',verbose_name=_("Recurrence parent"),blank=True,null=True)
    #~ rdate = models.TextField(_("Recurrence date"),blank=True)
    #~ exdate = models.TextField(_("Excluded date(s)"),blank=True)
    #~ rrules = models.TextField(_("Recurrence Rules"),blank=True)
    #~ exrules = models.TextField(_("Exclusion Rules"),blank=True)
    
    #~ def get_mailable_contacts(self):
        #~ yield ('to',self.project)
    
        
        
    def save(self,*args,**kw):
        #~ if not self.calendar:
            #~ self.calendar = self.user.calendar or settings.SITE.site_config.default_calendar
        if self.user is not None and self.access_class is None:
            self.access_class = self.user.access_class
            #~ self.access_class = AccessClasses.public
        super(Component,self).save(*args,**kw)
        
    def on_duplicate(self,ar,master):
        self.auto_type = None
        
    def disabled_fields(self,ar):
        rv = super(Component,self).disabled_fields(ar)
        if self.auto_type:
            #~ return settings.SITE.TASK_AUTO_FIELDS
            rv |= self.DISABLED_AUTO_FIELDS
        return rv
        
    def get_uid(self):
        """
        This is going to be used when sending 
        locally created components to a remote calendar.
        """
        #~ if self.uid:
            #~ return self.uid
        if not settings.SITE.uid:
            raise Exception('Cannot create local calendar components because settings.SITE.uid is empty.')
        return "%s@%s" % (self.pk,settings.SITE.uid)
            

    #~ def on_user_change(self,request):
        #~ raise NotImplementedError
        #~ self.user_modified = True
        
    def summary_row(self,ar,**kw):
        #~ logger.info("20120217 Component.summary_row() %s", self)
        #~ if self.owner and not self.auto_type:
        #~ html = ui.ext_renderer.href_to(self)
        html = [ar.obj2html(self)]
        if self.start_time:
            #~ html += _(" at ") + unicode(self.start_time)
            html += [_(" at "), self.start_time.strftime(settings.SITE.time_format_strftime) ]
        if self.state:
            html += [' [%s]' % force_unicode(self.state)]
        if self.summary:
            html += [': %s' % force_unicode(self.summary)]
            #~ html += ui.href_to(self,force_unicode(self.summary))
        #~ html += _(" on ") + dbutils.dtos(self.start_date)
        #~ if self.owner and not self.owner.__class__.__name__ in ('Person','Company'):
            #~ html += " (%s)" % reports.summary_row(self.owner,ui,rr)
        if self.project is not None:
            html.append(" (%s)" % self.project.summary_row(ar,**kw))
            #~ print 20120217, self.project.__class__, self
            #~ html += " (%s)" % self.project.summary_row(ui)
        return html
        #~ return super(Event,self).summary_row(ui,rr,**kw)
        
#~ Component.owner.verbose_name = _("Automatically created by")
        
#~ from lino.modlib.workflows import models as workflows # Workflowable

#~ class Components(dd.Table):
#~ # class Components(dd.Table,workflows.Workflowable):
  
    #~ workflow_owner_field = 'user'    
    #~ workflow_state_field = 'state'
    
    #~ def disable_editing(self,request):
    #~ def get_row_permission(cls,row,user,action):
        #~ if row.rset: return False
        
    #~ @classmethod
    #~ def get_row_permission(cls,action,user,row):
        #~ if not action.readonly:
            #~ if row.user != user and user.level < UserLevel.manager: 
                #~ return False
        #~ if not super(Components,cls).get_row_permission(action,user,row):
            #~ return False
        #~ return True



if False: # removed 20130810
    
  def tasks_summary(ui,user,days_back=None,days_forward=None,**kw):
    """
    Return a HTML summary of all open reminders for this user.
    May be called from :xfile:`welcome.html`.
    """
    Task = dd.resolve_model('cal.Task')
    Event = dd.resolve_model('cal.Event')
    today = datetime.date.today()
    
    past = {}
    future = {}
    def add(cmp):
        if cmp.start_date < today:
        #~ if task.dt_alarm < today:
            lookup = past
        else:
            lookup = future
        day = lookup.get(cmp.start_date,None)
        if day is None:
            day = [cmp]
            lookup[cmp.start_date] = day
        else:
            day.append(cmp)
            
    #~ filterkw = { 'due_date__lte' : today }
    filterkw = {}
    if days_back is not None:
        filterkw.update({ 
            'start_date__gte' : today - datetime.timedelta(days=days_back)
            #~ 'dt_alarm__gte' : today - datetime.timedelta(days=days_back)
        })
    if days_forward is not None:
        filterkw.update({ 
            'start_date__lte' : today + datetime.timedelta(days=days_forward)
            #~ 'dt_alarm__lte' : today + datetime.timedelta(days=days_forward)
        })
    #~ filterkw.update(dt_alarm__isnull=False)
    filterkw.update(user=user)
    
    for o in Event.objects.filter(
        #~ models.Q(status=None) | models.Q(status__reminder=True),
        models.Q(state=None) | models.Q(state__lte=EventStates.published),
        **filterkw).order_by('start_date'):
        add(o)
        
    #~ filterkw.update(done=False)
    #~ filterkw.update(state__in=[TaskState.blank_item,TaskState.todo]) 20120829
    filterkw.update(state__in=[None,TaskStates.todo])
            
    for task in Task.objects.filter(**filterkw).order_by('start_date'):
        add(task)
        
    def loop(lookup,reverse):
        sorted_days = lookup.keys()
        sorted_days.sort()
        if reverse: 
            sorted_days.reverse()
        for day in sorted_days:
            yield '<h3>'+dtosl(day) + '</h3>'
            yield dd.summary(ui,lookup[day],**kw)
            
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


def update_auto_event(autotype,user,date,summary,owner,**defaults):
    #~ model = dd.resolve_model('cal.Event')
    return update_auto_component(Event,autotype,user,date,summary,owner,**defaults)
  
def update_auto_task(autotype,user,date,summary,owner,**defaults):
    #~ model = dd.resolve_model('cal.Task')
    return update_auto_component(Task,autotype,user,date,summary,owner,**defaults)
    
def update_auto_component(model,autotype,user,date,summary,owner,**defaults):
    """
    Creates, updates or deletes the 
    automatic :class:`calendar component <Component>`
    of the specified `auto_type` and `owner`.
    
    Specifying `None` for `date` means that 
    the automatic component should be deleted.
    """
    #~ print "20120729 update_auto_component", model,autotype,user, date, settings.SITE.loading_from_dump
    #~ if SKIP_AUTO_TASKS: return 
    if settings.SITE.loading_from_dump: 
        #~ print "20111014 loading_from_dump"
        return None
    ot = ContentType.objects.get_for_model(owner.__class__)
    if date and date >= datetime.date.today() + datetime.timedelta(days=-7):
        #~ defaults = owner.get_auto_task_defaults(**defaults)
        #~ print "20120729 b"
        defaults.setdefault('user',user)
        obj,created = model.objects.get_or_create(
          defaults=defaults,
          owner_id=owner.pk,
          owner_type=ot,
          auto_type=autotype)
        if not obj.is_user_modified():
            original_state = dict(obj.__dict__)
            if obj.user != user:
                obj.user = user
            summary = force_unicode(summary)
            if obj.summary != summary:
                obj.summary = summary
            if obj.start_date != date:
                obj.start_date = date
            if created or obj.__dict__ != original_state:
                #~ obj.full_clean()
                obj.save()
        return obj
    else:
        #~ print "20120729 c"
        # delete task if it exists
        try:
            obj = model.objects.get(owner_id=owner.pk,
                    owner_type=ot,auto_type=autotype)
        except model.DoesNotExist:
            pass
        else:
            if not obj.is_user_modified():
                obj.delete()
                
        
def update_reminder(type,owner,user,orig,msg,num,unit):
    """
    Shortcut for calling :func:`update_auto_task` 
    for automatic "reminder tasks".
    A reminder task is a message about something that will 
    happen in the future.
    """
    update_auto_task(
      type,user,
      unit.add_duration(orig,-num),
      msg,
      owner)
            



def migrate_reminder(obj,reminder_date,reminder_text,
                         delay_value,delay_type,reminder_done):
    """
    This was used only for migrating to 1.2.0, 
    see :mod:`lino.projects.pcsw.migrate`.
    """
    raise NotImplementedError("No longer needed (and no longer supported after 20111026).")
    def delay2alarm(delay_type):
        if delay_type == 'D': return DurationUnits.days
        if delay_type == 'W': return DurationUnits.weeks
        if delay_type == 'M': return DurationUnits.months
        if delay_type == 'Y': return DurationUnits.years
      
    #~ # These constants must be unique for the whole Lino Site.
    #~ # Keep in sync with auto types defined in lino.projects.pcsw.models.Person
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
      


if False:
    
    def reminders_as_html_old(ar,days_back=None,days_forward=None,**kw):
        s = '<div class="htmlText" style="margin:5px">%s</div>' % reminders_as_html(ar,days_back=None,days_forward=None,**kw)
        return s
        
    def reminders_as_html(ar,days_back=None,days_forward=None,**kw):
        """
        Return a HTML summary of all open reminders for this user.
        """
        user = ar.get_user()
        if not user.profile.authenticated: return ''
        today = datetime.date.today()
        
        past = {}
        future = {}
        def add(cmp):
            if cmp.start_date < today:
                lookup = past
            else:
                lookup = future
            day = lookup.get(cmp.start_date,None)
            if day is None:
                day = [cmp]
                lookup[cmp.start_date] = day
            else:
                day.append(cmp)
                
        flt = models.Q()
        if days_back is not None:
            flt = flt & models.Q(start_date__gte = today - datetime.timedelta(days=days_back))
        if days_forward is not None:
            flt = flt & models.Q(start_date__lte=today + datetime.timedelta(days=days_forward))
        
        events = ar.spawn(MyEvents,
            user=user,
            filter=flt & (models.Q(state=None) | models.Q(state__lte=EventStates.published)))
        tasks = ar.spawn(MyTasks,
            user=user,
            filter=flt & models.Q(state__in=[None,TaskStates.todo]))
        
        for o in events:
            o._detail_action = MyEvents.get_url_action('detail_action')
            add(o)
            
        for o in tasks:
            o._detail_action = MyTasks.get_url_action('detail_action')
            add(o)
            
        def loop(lookup,reverse):
            sorted_days = lookup.keys()
            sorted_days.sort()
            if reverse: 
                sorted_days.reverse()
            for day in sorted_days:
                #~ yield E.h3(dtosl(day))
                yield '<h3>'+dtosl(day) + '</h3>'
                yield dd.summary(ar,lookup[day],**kw)
                
        #~ if days_back is not None:
            #~ return loop(past,True)
        #~ else:
            #~ return loop(future,False)
            
        if days_back is not None:
            s = ''.join([chunk for chunk in loop(past,True)])
        else:
            s = ''.join([chunk for chunk in loop(future,False)])
            
        #~ s = '<div class="htmlText" style="margin:5px">%s</div>' % s
        return s
        
        
    settings.SITE.reminders_as_html = reminders_as_html
    
def update_reminders_for_user(user):
    n = 0 
    for model in dd.models_by_base(EventGenerator):
        for obj in model.objects.filter(user=user):
            obj.update_reminders()
            #~ logger.info("--> %s",unicode(obj))
            n += 1
    return n
      
def unused_update_reminders(user):
    n = 0 
    for obj in settings.SITE.get_reminder_generators_by_user(user):
        obj.update_reminders()
        #~ logger.info("--> %s",unicode(obj))
        n += 1
    return n
      

system = dd.resolve_app('system')


def customize_users():
    """
    Injects application-specific fields to users.User.
    """
    
    dd.inject_field(settings.SITE.user_model,
        'access_class',
        AccessClasses.field(
            default=AccessClasses.public,
            verbose_name=_("Default access class"),
            help_text=_("""The default access class for your calendar events and tasks.""")
    ))
    dd.inject_field(settings.SITE.user_model,
        'event_type',
        models.ForeignKey('cal.EventType',
            blank=True,null=True,
            verbose_name=_("Default Event Type"),
            help_text=_("""The default event type for your calendar events.""")
    ))
    
    dd.inject_field('system.SiteConfig',
        'default_event_type',
        models.ForeignKey('cal.EventType',
            blank=True,null=True,
            verbose_name=_("Default Event Type"),
            help_text=_("""The default type of events on this site.""")
    ))
    
    dd.inject_field('system.SiteConfig',
        'holiday_event_type',
        models.ForeignKey('cal.EventType',
            blank=True,null=True,
            related_name="%(app_label)s_%(class)s_set_by_holiday_calender",
            verbose_name=_("Holiday"),
            help_text=_("""The default type for recurring calendar events.""")
    ))
    
    dd.inject_field('system.SiteConfig',
        'max_auto_events',
        models.IntegerField(_("Max automatic events"),default=72,
            blank=True,null=True,
            help_text=_("""Maximum number of automatic events to be generated.""")
    ))
    
    dd.inject_field('system.SiteConfig',
        'farest_future',
        models.DateField(_("Farest future"),
            default=datetime.date.today() + dateutil.relativedelta.relativedelta(years=5),
            help_text=_("""Don't generate automatic events past that date.""")
    ))
    
    #~ users = dd.resolve_app('users')
    #~ users.User.add_model_action(update_reminders=UpdateReminders())
  



def site_setup(site):
    """
    (Called during site setup.)
    
    Adds a "Calendar" tab and the :class:`UpdateReminders` 
    action to `users.User`
    """
    
    #~ site.modules.users.User.update_reminders = UpdateReminders()
    
    site.modules.users.Users.add_detail_panel('cal_left',"""
    event_type access_class 
    cal.SubscriptionsByUser
    # cal.MembershipsByUser
    """)
    site.modules.users.Users.add_detail_tab('cal',"""
    cal_left:30 cal.TasksByUser:60
    """,MODULE_LABEL,required=dict(user_groups='office'))
    #~ site.modules.users.Users.add_detail_tab('cal.TasksByUser')
    
    
MODULE_LABEL = _("Calendar")

def setup_main_menu(site,ui,profile,m): 
    m  = m.add_menu("cal",MODULE_LABEL)
    
    if site.use_extensible:
        m.add_action('cal.CalendarPanel')
    m.add_action('cal.MyEvents') # string spec to allow overriding
    
    #~ m.add_separator('-')
    #~ m  = m.add_menu("tasks",_("Tasks"))
    m.add_action('cal.MyTasks')
    #~ m.add_action(MyTasksToDo)
    
    m.add_action('cal.MyGuests')
    
    m.add_action('cal.MyPresences')
    
  
#~ def setup_master_menu(site,ui,profile,m): 
    #~ pass
    
    
def setup_config_menu(site,ui,profile,m): 
    m  = m.add_menu("cal",MODULE_LABEL)
    m.add_action('cal.MySubscriptions')
    m.add_action('cal.Rooms')
    m.add_action('cal.Priorities')
    m.add_action('cal.RecurrentEvents')
    #~ m.add_action(AccessClasses)
    #~ m.add_action(EventStatuses)
    #~ m.add_action(TaskStatuses)
    #~ m.add_action(EventTypes)
    m.add_action('cal.GuestRoles')
    #~ m.add_action(GuestStatuses)
    m.add_action('cal.EventTypes')
  
def setup_explorer_menu(site,ui,profile,m):
    m  = m.add_menu("cal",MODULE_LABEL)
    m.add_action('cal.Tasks')
    m.add_action('cal.Guests')
    m.add_action('cal.Subscriptions')
    #~ m.add_action(Memberships)
    m.add_action('cal.EventStates')
    m.add_action('cal.GuestStates')
    m.add_action('cal.TaskStates')
    #~ m.add_action(RecurrenceSets)

def setup_quicklinks(site,ar,m):
    #~ print 20120706
    if site.use_extensible:
        #~ m.add_action(self.modules.cal.Panel)
        m.add_action('cal.CalendarPanel')
        #~ m.add_action(MyEventsAssigned)
        #~ m.add_action(MyEventsNotified)
        #~ m.add_action(MyTasksToDo)
        
#~ def whats_up(site,ui,user):
    #~ MyEventsReserved
    #~ MyEventsAssigned
    #~ MyEventsNotified
    

#~ dd.add_user_group('office',MODULE_LABEL)

customize_users()


from .models_calendar import *
from .models_task import *
from .models_guest import *
from .models_event import *

def get_todo_tables(ar):
    yield ('cal.MyAssignedEvents', _("%d events assigned.")) 
    #~ yield (MyUnclearEvents, _("%d unclear events approaching.")) # "%d unklare Termine kommen näher"
    yield ('cal.MyPendingPresences', _("%d invitations are waiting for your answer."))
    #~ yield (MyGuests, _("%d invitations are waiting for your answer."))
    #~ yield (MyTasksToDo,_("%d tasks to do"))
    #~ yield (MyEventsNotified,_("%d notified events"))
    #~ yield (EventsAssignedToMe,_("%d events assigned to you"))
    
