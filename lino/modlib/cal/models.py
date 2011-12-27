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
This module turns Lino into a basic calendar client. 
Supports remote calendars.
Events and Tasks can get attributed to a :attr:`Project <lino.Lino.project_model>`.

"""
import cgi
import datetime

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import force_unicode

from lino import mixins
from lino import dd
#~ from lino.core import reports
from lino.core import actions
from lino.utils import perms
from lino.utils import babel
from lino.utils import dblogger
from lino.tools import resolve_model

from lino.modlib.contacts import models as contacts

from lino.modlib.mails import models as mails # import Mailable

from lino.modlib.cal.utils import \
    DurationUnit, setkw, dt2kw
#~ from lino.modlib.cal.utils import EventStatus, \
    #~ TaskStatus, DurationUnit, Priority, AccessClass, \
    #~ GuestStatus, setkw, dt2kw

from lino.utils.babel import dtosl
#~ from lino.utils.dpy import is_deserializing



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
    
COLOR_CHOICES = [i + 1 for i in range(32)]
  
from django.core.validators import MaxValueValidator
from django.core.validators import MinValueValidator

class Calendar(mixins.AutoUser):
    """
    A Calendar is a collection of events and tasks.
    There are local calendars and remote calendars.
    Remote calendars will be synchronized by
    :mod:`lino.modlib.cal.management.commands.watch_calendars`,
    and local modifications will be sent back to the remote calendar.
    """
    class Meta:
        verbose_name = _("Calendar")
        verbose_name_plural = _("Calendars")
        
    type = models.CharField(_("Type"),max_length=20,
        default='local',
        choices=CALENDAR_CHOICES)
    name = models.CharField(_("Name"),max_length=200)
    description = dd.RichTextField(_("Description"),blank=True,format='html')
    url_template = models.CharField(_("URL template"),
        max_length=200,blank=True) # ,null=True)
    username = models.CharField(_("Username"),
        max_length=200,blank=True) # ,null=True)
    password = dd.PasswordField(_("Password"),
        max_length=200,blank=True) # ,null=True)
    readonly = models.BooleanField(_("read-only"),default=False)
    is_default = models.BooleanField(
        _("is default"),default=False)
    is_hidden = models.BooleanField(
        _("is hidden"),default=False)
    start_date = models.DateField(
        verbose_name=_("Start date"),
        blank=True,null=True)
    color = models.IntegerField(
        _("color"),default=1,
        validators=[MinValueValidator(1), MaxValueValidator(32)]
        )
        #~ choices=COLOR_CHOICES)
    
    def full_clean(self,*args,**kw):
        if not self.name:
            if self.username:
                self.name = self.username
            elif self.user is None:
                self.name = "Anonymous"
            else:
                self.name = self.user.get_full_name()
                if not self.name:
                    self.name = self.user.username
        super(Calendar,self).full_clean(*args,**kw)
        
    def save(self,*args,**kw):
        ct = CALENDAR_DICT.get(self.type)
        ct.validate_calendar(self)
        super(Calendar,self).save(*args,**kw)
        if self.is_default: # and self.user is not None:
            for cal in Calendar.objects.filter(user=self.user):
            #~ for cal in self.user.cal_calendar_set_by_user.all():
            #~ for cal in self.user.calendar_set.all():
                if cal.pk != self.pk and cal.is_default:
                    cal.is_default = False
                    cal.save()

    def get_url(self):
        if self.url_template:
            return self.url_template % dict(
              username=self.username,
              password=self.password)
        return ''
                    
    def __unicode__(self):
        return self.name
        
    #~ def color(self,request):
        #~ return settings.LINO.get_calendar_color(self,request)
    #~ color.return_type = models.IntegerField(_("Color"))
        
        
    
class Calendars(dd.Table):
    model = 'cal.Calendar'
    column_names = "user type name color readonly is_hidden is_default *"

def default_calendar(user):
    """
    Returns or creates the default calendar for the given user.
    """
    #~ if user is None:
    try:
        return Calendar.objects.get(user=user,is_default=True)
        #~ return user.cal_calendar_set_by_user.get(is_default=True)
        #~ return user.calendar_set.get(is_default=True)
    except Calendar.DoesNotExist,e:
        color = Calendar.objects.all().count() + 1
        while color > 32:
            color -= 32
        cal = Calendar(user=user,is_default=True,color=color)
        cal.full_clean()
        cal.save()
        dblogger.debug("Created default_calendar %s for %s.",cal,user)
        return cal




class Place(babel.BabelNamed):
    """
    A location where Events can happen.
    For a given Place you can see the :class:`EventsByPlace` 
    that happened (or will happen) there.
    """
    class Meta:
        verbose_name = _("Place")
        verbose_name_plural = _("Places")
        
    #~ name = models.CharField(_("Name"),max_length=200)
    #~ def __unicode__(self):
        #~ return self.name 
  
class Places(dd.Table):
    model = Place
    

class EventStatus(babel.BabelNamed):
    "The status of an Event."
    class Meta:
        verbose_name = _("Event Status")
        verbose_name_plural = _('Event Statuses')
    ref = models.CharField(max_length='1')
    reminder = models.BooleanField(_("Reminder"),default=True)
    
class EventStatuses(dd.Table):
    model = EventStatus
    column_names = 'name *'

class TaskStatus(babel.BabelNamed):
    "The status of a Task."
    class Meta:
        verbose_name = _("Task Status")
        verbose_name_plural = _('Task Statuses')
    ref = models.CharField(max_length='1')
class TaskStatuses(dd.Table):
    model = TaskStatus
    column_names = 'name *'

class GuestStatus(babel.BabelNamed):
    "The status of a Guest."
    class Meta:
        verbose_name = _("Guest Status")
        verbose_name_plural = _('Guest Statuses')
    ref = models.CharField(max_length='1')
class GuestStatuses(dd.Table):
    model = GuestStatus
    column_names = 'name *'

class Priority(babel.BabelNamed):
    "The priority of a Task or Event."
    class Meta:
        verbose_name = _("Priority")
        verbose_name_plural = _('Priorities')
    ref = models.CharField(max_length='1')
class Priorities(dd.Table):
    model = Priority
    column_names = 'name *'

class AccessClass(babel.BabelNamed):
    "The access class of a Task or Event."
    class Meta:
        verbose_name = _("Access Class")
        verbose_name_plural = _('Access Classes')
    ref = models.CharField(max_length='1')
class AccessClasses(dd.Table):
    model = AccessClass
    column_names = 'name *'



class EventType(mixins.PrintableType,babel.BabelNamed):
    """The type of an Event.
    Determines which build method and template to be used for printing the event.
    """
  
    templates_group = 'cal/Event'
    
    class Meta:
        verbose_name = _("Event Type")
        verbose_name_plural = _('Event Types')

class EventTypes(dd.Table):
    model = EventType
    column_names = 'name build_method template *'



class CalendarRelated(models.Model):
    "Deserves more documentation."
    class Meta:
        abstract = True
        
    calendar = models.ForeignKey(Calendar,verbose_name=_("Calendar"),blank=True)
    
    def full_clean(self,*args,**kw):
        self.before_clean()
        super(CalendarRelated,self).full_clean(*args,**kw)
        
    def save(self,*args,**kw):
        self.before_clean()
        super(CalendarRelated,self).save(*args,**kw)
        
    def before_clean(self):
        """
        Called also from `save()` because `get_or_create()` 
        doesn't call full_clean().
        We cannot do this only in `save()` because otherwise 
        `full_clean()` (when called) will complain 
        about the empty fields.
        """
        if not self.calendar_id:
            self.calendar = default_calendar(self.user)
            #~ print "20111217 calendar_id was empty. set to", self.calendar, "because", self.user
            

  
    
class ComponentBase(CalendarRelated,mixins.ProjectRelated):
    class Meta:
        abstract = True
        
    uid = models.CharField(_("UID"),
        max_length=200,
        blank=True) # ,null=True)

    start_date = models.DateField(
        verbose_name=_("Start date")) # iCal:DTSTART
    start_time = models.TimeField(
        blank=True,null=True,
        verbose_name=_("Start time"))# iCal:DTSTART
    start = dd.FieldSet(_("Start"),'start_date start_time')
    summary = models.CharField(_("Summary"),max_length=200,blank=True) # iCal:SUMMARY
    description = dd.RichTextField(_("Description"),blank=True,format='html')
    
    def save(self,*args,**kw):
        """
        Fills default value "today" to start_date
        """
        if not self.start_date:
            self.start_date = datetime.date.today()
        super(ComponentBase,self).save(*args,**kw)
        
    def __unicode__(self):
        return self._meta.verbose_name + " #" + str(self.pk)

    def summary_row(self,ui,rr,**kw):
        html = mixins.ProjectRelated.summary_row(self,ui,rr,**kw)
        if self.summary:
            html += '&nbsp;: %s' % cgi.escape(force_unicode(self.summary))
            #~ html += ui.href_to(self,force_unicode(self.summary))
        html += _(" on ") + babel.dtos(self.start_date)
        return html
        
    def get_datetime(self,name):
        "`name` can be 'start' or 'end'."
        d = getattr(self,name+'_date')
        if not d: return None
        t = getattr(self,name+'_time')
        if t:
            return datetime.datetime.combine(d,t)
        else:
            return datetime.datetime(d.year,d.month,d.day)
        
    def start_dt(self,request):
        return self.get_datetime('start')
    start_dt.return_type = dd.DisplayField(_("Start"))
    
    def end_dt(self,request):
        return self.get_datetime('end') or self.get_datetime('start')
        #~ et = self.get_datetime('end')
        #~ if et is None:
            #~ et = self.get_datetime('start')
        #~ return et
    end_dt.return_type = dd.DisplayField(_("End"))
        

class RecurrenceSet(ComponentBase):
    """
    Groups together all instances of a set of recurring calendar components.
    
    Thanks to http://www.kanzaki.com/docs/ical/rdate.html
    
    """
    class Meta:
        verbose_name = _("Recurrence Set")
        verbose_name_plural = _("Recurrence Sets")
    
    rdates = models.TextField(_("Recurrence dates"),blank=True)
    exdates = models.TextField(_("Excluded dates"),blank=True)
    rrules = models.TextField(_("Recurrence Rules"),blank=True)
    exrules = models.TextField(_("Exclusion Rules"),blank=True)
    
class RecurrenceSets(dd.Table):
    """
    The list of all :class:`Recurrence Sets <RecurrenceSet>`.
    """
    model = RecurrenceSet
    
    
    
class Component(ComponentBase,
                mixins.Owned,
                mixins.AutoUser,
                mixins.CreatedModified):
    """
    Abstract base class for :class:`Event` and :class:`Task`.
    
    The `owner` of a Task or Event 
    is some other database object that caused the task's or event's 
    creation.
    
    For example, an invoice may cause one or several Tasks 
    to be automatically generated when a certain payment mode 
    is specified.
    
    Automatic Calendar components are "governed" or "controlled"
    by their owner:
    If the owner gets modified, it may decide to delete or 
    modify all its automatic tasks or events.
    
    Non-automatic tasks always have an empty `owner` field.
    Some fields are read-only on an automatic Task because 
    it makes no sense to modify them.
    
    """
    class Meta:
        abstract = True
        
    #~ access_class = AccessClass.field() # iCal:CLASS
    access_class = models.ForeignKey(AccessClass,blank=True,null=True)
    sequence = models.IntegerField(_("Revision"),default=0)
    #~ alarm_value = models.IntegerField(_("Value"),null=True,blank=True,default=1)
    #~ alarm_unit = DurationUnit.field(_("Unit"),blank=True,
        #~ default=DurationUnit.days.value) # ,null=True) # note: it's a char field!
    #~ alarm = dd.FieldSet(_("Alarm"),'alarm_value alarm_unit')
    #~ dt_alarm = models.DateTimeField(_("Alarm time"),
        #~ blank=True,null=True,editable=False)
        
    auto_type = models.IntegerField(null=True,blank=True,editable=False) 
    
    user_modified = models.BooleanField(_("modified by user"),
        default=False,editable=False) 
    
    rset = models.ForeignKey(RecurrenceSet,
        verbose_name=_("Recurrence Set"),
        blank=True,null=True)
    #~ rparent = models.ForeignKey('self',verbose_name=_("Recurrence parent"),blank=True,null=True)
    #~ rdate = models.TextField(_("Recurrence date"),blank=True)
    #~ exdate = models.TextField(_("Excluded date(s)"),blank=True)
    #~ rrules = models.TextField(_("Recurrence Rules"),blank=True)
    #~ exrules = models.TextField(_("Exclusion Rules"),blank=True)
        
        
    def disabled_fields(self,request):
        if self.auto_type:
            #~ return settings.LINO.TASK_AUTO_FIELDS
            return self.DISABLED_AUTO_FIELDS
        return []
        
    def disable_editing(self,request):
        if self.rset: return True

    def get_uid(self):
        """
        This is going to be used when sending 
        locally created components to a remote calendar.
        """
        if self.uid:
            return self.uid
        if not settings.LINO.uid:
            raise Exception('Cannot create local calendar components because settings.LINO.uid is empty.')
        return "%s@%s" % (self.pk,settings.LINO.uid)
            
    def save(self,*args,**kw):
        if self.owner:
            #~ if self.owner.__class__.__name__ == 'Person':
                #~ self.person = self.owner
            #~ elif self.owner.__class__.__name__ == 'Company':
                #~ self.company = self.owner
            m = getattr(self.owner,'update_owned_instance',None)
            #~ m = getattr(self.owner,'update_owned_task',None)
            if m:
                #~ print "20111014 call update_owned_task() on", self.owner
                m(self)
            #~ else:
                #~ print "20111014 no update_owned_task on", self
              
        super(Component,self).save(*args,**kw)
        if self.owner:
            m = getattr(self.owner,'after_update_owned_instance',None)
            if m:
                m(self)


    def on_user_change(self,request):
        self.user_modified = True
        #~ if change_type == 'POST': 
            #~ self.isdirty=True
        
    #~ def summary_row(self,ui,rr,**kw):
        #~ html = contacts.PartnerDocument.summary_row(self,ui,rr,**kw)
        #~ if self.summary:
            #~ html += '&nbsp;: %s' % cgi.escape(force_unicode(self.summary))
        #~ html += _(" on ") + babel.dtos(self.start_date)
        #~ return html
        
    def summary_row(self,ui,rr,**kw):
        #~ if self.owner and not self.auto_type:
        html = ui.href_to(self)
        if self.start_time:
            html += _(" at ") + babel.dtos(self.start_time)
        if self.status_id:
            html += ' [%s]' % cgi.escape(force_unicode(self.status))
        if self.summary:
            html += '&nbsp;: %s' % cgi.escape(force_unicode(self.summary))
            #~ html += ui.href_to(self,force_unicode(self.summary))
        #~ html += _(" on ") + babel.dtos(self.start_date)
        #~ if self.owner and not self.owner.__class__.__name__ in ('Person','Company'):
            #~ html += " (%s)" % reports.summary_row(self.owner,ui,rr)
        if self.project:
            html += " (%s)" % dd.summary_row(self.project,ui,rr)
        return html
        #~ return super(Event,self).summary_row(ui,rr,**kw)
        
#~ Component.owner.verbose_name = _("Automatically created by")

class Event(Component,mixins.TypedPrintable,mails.Mailable):
    """
    A Calendar Event (french "Rendez-vous", german "Termin") 
    is a scheduled lapse of time where something happens.
    """
  
    class Meta:
        verbose_name = _("Event")
        verbose_name_plural = _("Events")
        #~ abstract = True
        
    end_date = models.DateField(
        blank=True,null=True,
        verbose_name=_("End Date"))
    end_time = models.TimeField(
        blank=True,null=True,
        verbose_name=_("End Time"))
    end = dd.FieldSet(_("End"),'end_date end_time')
    transparent = models.BooleanField(_("Transparent"),default=False)
    type = models.ForeignKey(EventType,verbose_name=_("Event Type"),null=True,blank=True)
    place = models.ForeignKey(Place,verbose_name=_("Place"),null=True,blank=True) # iCal:LOCATION
    priority = models.ForeignKey(Priority,null=True,blank=True)
    #~ priority = Priority.field(_("Priority"),blank=True) # iCal:PRIORITY
    #~ status = EventStatus.field(_("Status"),blank=True) # iCal:STATUS
    status = models.ForeignKey(EventStatus,verbose_name=_("Status"),blank=True,null=True) # iCal:STATUS
    duration = dd.FieldSet(_("Duration"),'duration_value duration_unit')
    duration_value = models.IntegerField(_("Duration value"),null=True,blank=True) # iCal:DURATION
    duration_unit = DurationUnit.field(_("Duration unit"),blank=True) # iCal:DURATION
    #~ repeat_value = models.IntegerField(_("Repeat every"),null=True,blank=True) # iCal:DURATION
    #~ repeat_unit = DurationUnit.field(verbose_name=_("Repeat every"),null=True,blank=True) # iCal:DURATION
    
    #~ def duration_changed(self):
    def compute_times(self):
        if self.duration_value is None or not self.duration_unit:
            return
        if self.start_time:
            dt = self.get_datetime('start')
            end_time = self.duration_unit.add_duration(dt,self.duration_value)
            #~ end_time = add_duration(dt,self.duration_value,self.duration_unit)
            setkw(self,**dt2kw(end_time,'end'))
        elif self.end_time:
            dt = self.get_datetime('end')
            end_time = self.duration_unit.add_duration(dt,-self.duration_value)
            setkw(self,**dt2kw(end_time,'start'))
        
    def duration_value_changed(self,oldvalue): self.compute_times()
    def duration_unit_changed(self,oldvalue): self.compute_times()
    def start_date_changed(self,oldvalue): self.compute_times()
    def start_time_changed(self,oldvalue): self.compute_times()
    def end_date_changed(self,oldvalue): self.compute_times()
    def end_time_changed(self,oldvalue): self.compute_times()
        
    def get_mailable_contacts(self):
        for g in self.guest_set.all():
            yield ('to',g)
        yield ('cc',self.user)
        
    @classmethod
    def setup_report(cls,rpt):
        mixins.TypedPrintable.setup_report(rpt)
        mails.Mailable.setup_report(rpt)
        
    @classmethod
    def site_setup(cls,lino):
        cls.DISABLED_AUTO_FIELDS = dd.fields_list(cls,
            '''summary''')
            
    def url(self,request): return 'foo'
    url.return_type = dd.DisplayField(_("Link URL"))
    
    def all_day(self,request): 
        return not self.start_time
    all_day.return_type = models.BooleanField(_("all day"))
    def reminder(self,request): return 'foo'
    reminder.return_type = dd.DisplayField(_("Reminder"))

        

#~ class Task(Component,contacts.PartnerDocument):
class Task(Component):
    """
    A Task is when a user plans to to something and wants to 
    get reminded about it.
    
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
    #~ status = TaskStatus.field(blank=True) # iCal:STATUS
    status = models.ForeignKey(TaskStatus,verbose_name=_("Status"),blank=True,null=True) # iCal:STATUS
    

    @classmethod
    def site_setup(cls,lino):
        #~ lino.TASK_AUTO_FIELDS = dd.fields_list(cls,
        cls.DISABLED_AUTO_FIELDS = dd.fields_list(cls,
            '''start_date start_time summary''')

    #~ def __unicode__(self):
        #~ return "#" + str(self.pk)
        

class Events(dd.Table):
    model = 'cal.Event'
    column_names = 'start_date start_time summary status *'
    
    #~ def setup_actions(self):
        #~ super(dd.Table,self).setup_actions()
        #~ self.add_action(mails.CreateMailAction())
    
class EventsBySet(Events):
    master_key = 'rset'
    
class EventsByCalendar(Events):
    master_key = 'calendar'
    
class EventsByPlace(Events):
    """
    Displays the :class:`Events <Event>` at a given :class:`Place`.
    """
    master_key = 'place'
    
class Tasks(dd.Table):
    model = 'cal.Task'
    column_names = 'start_date summary done status *'
    #~ hidden_columns = set('owner_id owner_type'.split())
    
#~ class EventsByOwner(Events):
    #~ master_key = 'owner'
    
class TasksByOwner(Tasks):
    master_key = 'owner'
    #~ hidden_columns = set('owner_id owner_type'.split())

class EventsByOwner(Events):
    master_key = 'owner'

if settings.LINO.project_model:    
    class EventsByProject(Events):
        master_key = 'project'
    
    class TasksByProject(Tasks):
        master_key = 'project'
    
if settings.LINO.user_model:    
    class MyEvents(mixins.ByUser):
        model = 'cal.Event'
        #~ label = _("My Events")
        order_by = ["start_date","start_time"]
        column_names = 'start_date start_time summary status *'
        
    class MyEventsToday(MyEvents):
        column_names = 'start_time summary status *'
        label = u"Meine Termine heute"
        
        def setup_request(self,rr):
            rr.known_values = dict(start_date=datetime.date.today())
            super(MyEventsToday,self).setup_request(rr)
        
        
    class MyTasks(mixins.ByUser):
        model = 'cal.Task'
        #~ label = _("My Tasks")
        order_by = ["start_date","start_time"]
        column_names = 'start_date summary done status *'
    

class GuestRole(babel.BabelNamed):
    """
    A possible value for the `role` field of an :class:`Guest`.
    
    """
    class Meta:
        verbose_name = _("Guest Role")
        verbose_name_plural = _("Guest Roles")


class GuestRoles(dd.Table):
    model = GuestRole
    

class Guest(contacts.ContactDocument,
            mixins.CachedPrintable,
            mails.Mailable):
    """
    A Guest is a Contact who is invited to an :class:`Event`.
    """
    class Meta:
        verbose_name = _("Guest")
        verbose_name_plural = _("Guests")
        
    event = models.ForeignKey('cal.Event',
        verbose_name=_("Event")) 
        
    role = models.ForeignKey('cal.GuestRole',
        verbose_name=_("Role"),
        blank=True,null=True) 
        
    #~ status = GuestStatus.field(verbose_name=_("Status"),blank=True)
    status = models.ForeignKey(GuestStatus,verbose_name=_("Status"),blank=True,null=True)
    
    #~ confirmed = models.DateField(
        #~ blank=True,null=True,
        #~ verbose_name=_("Confirmed"))

    remark = models.CharField(
        _("Remark"),max_length=200,blank=True)

    #~ def __unicode__(self):
        #~ return self._meta.verbose_name + " #" + str(self.pk)
        
    def __unicode__(self):
        return u'%s #%s ("%s")' % (self._meta.verbose_name,self.pk,self.event)

    @classmethod
    def setup_report(cls,rpt):
        mixins.CachedPrintable.setup_report(rpt)
        mails.Mailable.setup_report(rpt)
        
class Guests(dd.Table):
    model = Guest
    column_names = 'contact role status remark event *'
    
    #~ def setup_actions(self):
        #~ super(dd.Table,self).setup_actions()
        #~ self.add_action(mails.CreateMailAction())
    
class GuestsByEvent(Guests):
    master_key = 'event'

class GuestsByContact(Guests):
    master_key = 'contact'
    column_names = 'event role status remark * contact'


    
def tasks_summary(ui,user,days_back=None,days_forward=None,**kw):
    """
    Return a HTML summary of all open reminders for this user.
    May be called from :xfile:`welcome.html`.
    """
    Task = resolve_model('cal.Task')
    Event = resolve_model('cal.Event')
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
        models.Q(status=None) | models.Q(status__reminder=True),
        **filterkw).order_by('start_date'):
        add(o)
        
    filterkw.update(done=False)
            
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

#~ SKIP_AUTO_TASKS = False 
#~ "See :doc:`/blog/2011/0727`"

def update_auto_event(autotype,user,date,summary,owner,**defaults):
    model = resolve_model('cal.Event')
    return update_auto_component(model,autotype,user,date,summary,owner,**defaults)
  
def update_auto_task(autotype,user,date,summary,owner,**defaults):
    model = resolve_model('cal.Task')
    return update_auto_component(model,autotype,user,date,summary,owner,**defaults)
    
def update_auto_component(model,autotype,user,date,summary,owner,**defaults):
    """
    Creates, updates or deletes the automatic component 
    (either a :class:`Task` or an :class:`Event`)
    related to the specified `owner`.
    
    Specifying `None` for `date` means that 
    the automatic component should be deleted.
    """
    #~ print "20111014 update_auto_task"
    #~ if SKIP_AUTO_TASKS: return 
    if settings.LINO.loading_from_dump: 
        #~ print "20111014 loading_from_dump"
        return None
    #~ if is_deserializing(): return 
    ot = ContentType.objects.get_for_model(owner.__class__)
    if date:
        #~ defaults = owner.get_auto_task_defaults(**defaults)
        defaults.setdefault('user',user)
        obj,created = model.objects.get_or_create(
          defaults=defaults,
          owner_id=owner.pk,
          owner_type=ot,
          auto_type=autotype)
        if not obj.user_modified:
            obj.user = user
            obj.summary = force_unicode(summary)
            #~ obj.summary = summary
            obj.start_date = date
            #~ print "20111014 gonna save() task", task
            #~ for k,v in kw.items():
                #~ setattr(obj,k,v)
            #~ obj.due_date = date - delta
            #~ print 20110712, date, date-delta, obj2str(obj,force_detailed=True)
            #~ owner.update_owned_task(task)
            obj.save()
        return obj
    else:
        # delete task if it exists
        try:
            obj = model.objects.get(owner_id=owner.pk,
                    owner_type=ot,auto_type=autotype)
        except model.DoesNotExist:
            pass
        else:
            if not obj.user_modified:
                obj.delete()
        

def migrate_reminder(obj,reminder_date,reminder_text,
                         delay_value,delay_type,reminder_done):
    """
    This was used only for migrating to 1.2.0, 
    see :mod:`lino.apps.dsbe.migrate`.
    """
    raise NotImplementedError("No longer needed (and no longer supported after 20111026).")
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
      
      
if settings.LINO.use_extensible:
  
    def parsedate(s):
        return datetime.date(*settings.LINO.parse_date(s))
  
    class Panel(dd.Frame):
        default_action_class = dd.Calendar

    class PanelCalendars(Calendars):
        column_names = 'id name description color is_hidden'
        can_add = perms.never
      
    class PanelEvents(Events):
        """
        The report used for Ext.ensible CalendarPanel.
        """
        column_names = 'id start_dt end_dt summary description user place calendar rset url all_day reminder'
        can_add = perms.never
        def parse_req(self,request,**kw):
            filter = kw.get('filter',{})
            endDate = request.REQUEST.get('ed',None)
            if endDate:
                filter.update(start_date__lte=parsedate(endDate))
            startDate = request.REQUEST.get('sd',None)
            if startDate:
                filter.update(start_date__gte=parsedate(startDate))
            kw.update(filter=filter)
            return kw
        

def setup_main_menu(site,ui,user,m): pass

def setup_my_menu(site,ui,user,m): 
    m  = m.add_menu("cal",_("~Calendar"))
    m.add_action('cal.MyTasks')
    #~ m.add_action('cal.MyEventsToday')
    m.add_action('cal.MyEvents')
    if settings.LINO.use_extensible:
        m.add_action('cal.Panel')
    #~ m.add_action_(actions.Calendar())
  
def setup_config_menu(site,ui,user,m): 
    m  = m.add_menu("cal",_("~Calendar"))
    m.add_action('cal.Places')
    m.add_action('cal.Priorities')
    m.add_action('cal.AccessClasses')
    m.add_action('cal.EventStatuses')
    m.add_action('cal.TaskStatuses')
    m.add_action('cal.EventTypes')
    m.add_action('cal.GuestRoles')
    m.add_action('cal.GuestStatuses')
    m.add_action('cal.Calendars')
  
def setup_explorer_menu(site,ui,user,m):
    m  = m.add_menu("cal",_("~Calendar"))
    m.add_action('cal.Events')
    m.add_action('cal.Tasks')
    m.add_action('cal.Guests')
    m.add_action('cal.RecurrenceSets')
  