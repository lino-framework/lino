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
from django.utils import translation
#~ from django.utils.translation import string_concat
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import force_unicode
from django.db.models import loading
from django.core import exceptions
from django.utils.importlib import import_module

from north import dbutils
from north.dbutils import dtosl
from babel.dates import format_datetime, format_date
from north import to_locale


from lino import mixins
from lino import dd
#~ from lino.core import reports
from lino.core import actions
from lino.utils import AttrDict
from lino.utils import ONE_DAY
#~ from lino.ui import requests as ext_requests
from lino.core import constants


from lino.utils.xmlgen.html import E

from lino.modlib.cal.utils import \
    DurationUnits, Recurrencies, setkw, dt2kw, \
    Weekdays, AccessClasses, CalendarAction
    
def format_time(t):
    return t.strftime(settings.SITE.time_format_strftime)
    
def when_text(d,t):
    if d is None: return ''
    if t is None: return format_date(d,'yyyy MMM dd',locale=to_locale(translation.get_language()))
    #~ if d.year == datetime.date.today().year:
        #~ fmt = "%a" + settings.SITE.time_format_strftime
    #~ else:
        #~ fmt = "%a %y %b %d" + settings.SITE.time_format_strftime
    #~ fmt = "%a %Y %b %d " + settings.SITE.time_format_strftime
    #~ return datetime.datetime.combine(d,t).strftime(fmt)
    fmt = "yyyy MMM dd (EE) HH:mm"
    return format_datetime(datetime.datetime.combine(d,t),fmt,locale=to_locale(translation.get_language()))

    
    
contacts = dd.resolve_app('contacts')
postings = dd.resolve_app('postings')
outbox = dd.resolve_app('outbox')

workflow = import_module('lino.modlib.cal.workflows.welfare')
#~ workflow = import_module('lino.modlib.cal.workflows.faggio')

for n in ('TaskStates','EventStates','GuestStates'):
    globals()[n] = getattr(workflow,n)



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



#~ class Calendar(mixins.UserAuthored):
class Calendar(mixins.PrintableType,outbox.MailableType,dd.BabelNamed):
    """
    A Calendar is a collection of events and tasks.
    There are local calendars and remote calendars.
    Remote calendars will be synchronized by
    :mod:`lino.modlib.cal.management.commands.watch_calendars`,
    and local modifications will be sent back to the remote calendar.
    """
    
    templates_group = 'cal/Event'
    
    class Meta:
        verbose_name = _("Calendar")
        verbose_name_plural = _("Calendars")
        
    type = models.CharField(_("Type"),max_length=20,
        default='local',
        choices=CALENDAR_CHOICES)
    #~ name = models.CharField(_("Name"),max_length=200)
    description = dd.RichTextField(_("Description"),blank=True,format='html')
    url_template = models.CharField(_("URL template"),
        max_length=200,blank=True) # ,null=True)
    username = models.CharField(_("Username"),
        max_length=200,blank=True) # ,null=True)
    password = dd.PasswordField(_("Password"),
        max_length=200,blank=True) # ,null=True)
    readonly = models.BooleanField(_("read-only"),default=False)
    #~ invite_team_members = models.BooleanField(
        #~ _("Invite team members"),default=False)
    invite_team_members = dd.ForeignKey('users.Team',blank=True,null=True)
    #~ is_default = models.BooleanField(
        #~ _("is default"),default=False)
    #~ is_private = models.BooleanField(
        #~ _("private"),default=False,help_text=_("""\
#~ Whether other users may subscribe to this Calendar."""))
    start_date = models.DateField(
        verbose_name=_("Start date"),
        blank=True,null=True)
    color = models.IntegerField(
        _("color"),default=1,
        validators=[MinValueValidator(1), MaxValueValidator(32)]
        )
        #~ choices=COLOR_CHOICES)
    
    #~ def full_clean(self,*args,**kw):
        #~ if not self.name:
            #~ if self.username:
                #~ self.name = self.username
            #~ elif self.user is None:
                #~ self.name = "Anonymous"
            #~ else:
                #~ self.name = self.user.get_full_name()
        #~ super(Calendar,self).full_clean(*args,**kw)
        
    def save(self,*args,**kw):
        ct = CALENDAR_DICT.get(self.type)
        ct.validate_calendar(self)
        super(Calendar,self).save(*args,**kw)
        #~ if self.is_default: # and self.user is not None:
            #~ for cal in Calendar.objects.filter(user=self.user):
                #~ if cal.pk != self.pk and cal.is_default:
                    #~ cal.is_default = False
                    #~ cal.save()

    def get_url(self):
        if self.url_template:
            return self.url_template % dict(
              username=self.username,
              password=self.password)
        return ''
                    
    #~ def __unicode__(self):
        #~ return self.name
        
    #~ def color(self,request):
        #~ return settings.SITE.get_calendar_color(self,request)
    #~ color.return_type = models.IntegerField(_("Color"))
        
        
    
class Calendars(dd.Table):
    help_text = _("""The list of calendars defined on this system.
    A calendar is a list of events which have certain things in common,
    especially they are displayed in the same colour in the calendar panel""")
    required = dd.required(user_groups='office',user_level='manager')
    model = 'cal.Calendar'
    column_names = "name type color readonly build_method template *"
    
    detail_layout = """
    type name id 
    # description
    url_template username password
    readonly invite_team_members color start_date
    build_method template email_template attach_to_email
    EventsByCalendar SubscriptionsByCalendar
    """

    insert_layout = dd.FormLayout("""
    name 
    type invite_team_members color 
    """,window_size=(60,'auto'))

#~ def default_calendar(user):
    #~ """
    #~ Returns or creates the default calendar for the given user.
    #~ """
    #~ try:
        #~ return Calendar.objects.get(user=user,is_default=True)
    #~ except Calendar.DoesNotExist,e:
        #~ color = Calendar.objects.all().count() + 1
        #~ while color > 32:
            #~ color -= 32
        #~ cal = Calendar(user=user,is_default=True,color=color)
        #~ cal.full_clean()
        #~ cal.save()
        #~ logger.debug(u"Created default calendar for %s.",user)
        #~ return cal





class Subscription(mixins.UserAuthored):
    """
    A Suscription is when a User subscribes to some Calendar.
    
    :user: points to the author (recipient) of this subscription
    :calendar: points to the Calendar to subscribe
    
    """
    
    manager_level_field = 'office_level'
    
    class Meta:
        verbose_name = _("Subscription")
        verbose_name_plural = _("Subscriptions")
        
    #~ quick_search_fields = ('user__username','user__first_name','user__last_name')
    

    calendar = models.ForeignKey(Calendar,help_text=_("""\
The calendar you want to subscribe to.
You can subscribe to *non-private* calendars of *other* users."""))
    is_hidden = models.BooleanField(
        _("hidden"),default=False,help_text=_("""\
Whether this subscription should initially be hidden in your calendar panel."""))
    


class Subscriptions(dd.Table):
    required = dd.required(user_groups='office',user_level='manager')
    model = Subscription

class SubscriptionsByCalendar(Subscriptions):
    master_key = 'calendar'

class SubscriptionsByUser(Subscriptions):
    required = dd.required(user_groups='office')
    master_key = 'user'

#~ class MySubscriptions(Subscriptions,mixins.ByUser):
    #~ pass
    
from lino.modlib.users.models import Membership    

if False: # 20130320
  
  if settings.SITE.user_model:

    class Membership(mixins.UserAuthored):
        """
        A Membership is when a User decides that subscribes to somebody else's Calendar.
        
        :user: points to the author (recipient) of this membership
        :watched_user: points to the watched user
        
        """
        
        manager_level_field = 'office_level'
        
        class Meta:
            verbose_name = _("Membership")
            verbose_name_plural = _("Memberships")
            
        #~ quick_search_fields = ('user__username','user__first_name','user__last_name')
        
        watched_user = models.ForeignKey(settings.SITE.user_model,
            help_text=_("""\
    The user whose calendar events you want to see in team view."""))



        @dd.chooser()
        def watched_user_choices(cls,user):
            return settings.SITE.user_model.objects.exclude(
                #~ profile=dd.UserProfiles.blank_item).exclude(id=user.id) 20120829
                profile=None).exclude(id=user.id)
        
            
    class Memberships(dd.Table):
        required = dd.required(user_groups='office',user_level='manager')
        model = Membership


    class MembershipsByUser(Memberships):
        required = dd.required(user_groups='office')
        master_key = 'user'
        label = _("Team Members")



class Room(dd.BabelNamed,contacts.ContactRelated):
    """
    A location where Events can happen.
    For a given Room you can see the :class:`EventsByRoom` 
    that happened (or will happen) there.
    """
    class Meta:
        verbose_name = _("Room")
        verbose_name_plural = _("Rooms")
        
    def __unicode__(self):
        s = dd.BabelNamed.__unicode__(self)
        if self.company and self.company.city: 
            s = '%s (%s)' % (self.company.city,s)
        return s
        

        
  
class Rooms(dd.Table):
    help_text = _("List of rooms where calendar events can happen.")
    required = dd.required(user_groups='office',user_level='manager')
    model = Room
    detail_layout = """
    id name company contact_person contact_role
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


#~ class EventType(mixins.PrintableType,outbox.MailableType,dd.BabelNamed):
    #~ """The type of an Event.
    #~ Determines which build method and template to be used for printing the event.
    #~ """
  
    #~ templates_group = 'cal/Event'
    
    #~ class Meta:
        #~ verbose_name = pgettext(u"cal",u"Event Type")
        #~ verbose_name_plural = pgettext(u"cal",u'Event Types')

#~ class EventTypes(dd.Table):
    #~ model = EventType
    #~ required = dict(user_groups='office')
    #~ column_names = 'name build_method template *'
    #~ detail_layout = """
    #~ id name
    #~ build_method template email_template attach_to_email
    #~ cal.EventsByType
    #~ """



    
    
#~ class AutoEvent(object):
    #~ def __init__(self,auto_id,user,date,subject,owner,start_time,end_time):
        #~ self.auto_id = auto_id
        #~ self.user = user
        #~ self.date = date
        #~ self.subject = subject
        #~ self.owner = owner
        #~ self.start_time = start_time
        #~ self.end_time = end_time
    
    
class EventGenerator(mixins.UserAuthored):
    """
    Base class for things that generate a suite of events.
    Examples
    :class:`isip.Contract`,     :class:`jobs.Contract`, 
    :class:`schools.Course`
    """
    
    class Meta:
        abstract = True
        
    def save(self,*args,**kw):
        super(EventGenerator,self).save(*args,**kw)
        if self.user is not None:
            dbutils.run_with_language(self.user.language,self.update_reminders)
  
    def update_cal_rset(self):
        return self.exam_policy
        
    def update_cal_from(self):
        """
        Return the date of the first Event to be generated.
        Return None if no Events should be generated.
        """
        return self.applies_from
        
    def update_cal_until(self):
        return self.date_ended or self.applies_until
        
    def update_cal_calendar(self,i):
        return None
        
    def update_cal_subject(self,i):
        raise NotImplementedError()
        #~ return _("Evaluation %d") % i

    def update_reminders(self):
        """
        Generate automatic calendar events owned by this contract.
        
        [NOTE1] if one event has been manually rescheduled, all following events
        adapt to the new rythm.
        
        """
        return self.update_auto_events()
            
    def update_auto_events(self):
        if settings.SITE.loading_from_dump: 
            #~ print "20111014 loading_from_dump"
            return 
        qs = self.get_existing_auto_events()
        wanted = self.get_wanted_auto_events()
        current = 0
        
        #~ msg = dd.obj2str(self)
        #~ msg += ", qs=" + str([e.auto_type for e in qs])
        #~ msg += ", wanted=" + str([dbutils.dtos(e.start_date) for e in wanted.values()])
        #~ logger.info('20130528 ' + msg)
        
        for e in qs:
            ae = wanted.pop(e.auto_type,None)
            if ae is None:
                # there is an unwanted event in the database
                if not e.is_user_modified():
                    e.delete()
                #~ else:
                    #~ e.auto_type = None
                    #~ e.save()
            elif e.is_user_modified():
                if e.start_date != ae.start_date:
                    # modify subsequent dates
                    delta = e.start_date - ae.start_date
                    for se in wanted.values():
                        se.start_date += delta
            else:
                self.compare_auto_event(e,ae)
        # create new Events for remaining wanted
        for ae in wanted.values():
            Event(**ae).save()
        #~ logger.info("20130528 update_auto_events done")
            
    def compare_auto_event(self,obj,ae):
        original_state = dict(obj.__dict__)
        if obj.user != ae.user:
            obj.user = ae.user
        summary = force_unicode(ae.summary)
        if obj.summary != summary:
            obj.summary = summary
        if obj.start_date != ae.start_date:
            obj.start_date = ae.start_date
        if obj.start_time != ae.start_time:
            obj.start_time = ae.start_time
        if obj.end_time != ae.end_time:
            obj.end_time = ae.end_time
        if obj.calendar != ae.calendar:
            obj.calendar = ae.calendar
        if obj.__dict__ != original_state:
            obj.save()
      
    def get_wanted_auto_events(self):
        """
        Return a dict which maps sequence number 
        to AttrDict instances which hold the wanted event.
        """
        wanted = dict()
        rset = self.update_cal_rset()
        if rset and rset.every > 0 and rset.every_unit:
            date = self.update_cal_from()
            if not date:
                return wanted
        else:
            return wanted
        until = self.update_cal_until()
        #~ if until < wanted:
            #~ raise Warning("Series ends before it was started!")
        i = 0
        max_occurences = rset.max_occurences or settings.SITE.max_auto_events
        while i < max_occurences:
            i += 1
            if until is not None and date > until:
                return wanted
            if settings.SITE.ignore_dates_before is None or date >= settings.SITE.ignore_dates_before:
                wanted[i] = AttrDict(
                    auto_type=i,
                    user=self.user,
                    start_date=date,
                    summary=self.update_cal_subject(i),
                    owner=self,
                    calendar=self.update_cal_calendar(i),
                    start_time=rset.start_time,
                    end_time=rset.end_time)
            date = rset.get_next_date(date)
        return wanted
                    
        
    def get_existing_auto_events(self):
        ot = ContentType.objects.get_for_model(self.__class__)
        return Event.objects.filter(
            owner_type=ot,owner_id=self.pk,
            auto_type__isnull=False).order_by('auto_type')
        



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
        html = super(StartedSummaryDescription,self).summary_row(ar,**kw)
        if self.summary:
            html += '&nbsp;: %s' % cgi.escape(force_unicode(self.summary))
            #~ html += ui.href_to(self,force_unicode(self.summary))
        html += _(" on ") + dbutils.dtos(self.start_date)
        return html
        
    
#~ class RecurrenceSet(StartedSummaryDescription,Ended):
class RecurrenceSet(Started,Ended):
    """
    Abstract base for models that group together all instances 
    of a set of recurring calendar components.
    
    Thanks to http://www.kanzaki.com/docs/ical/rdate.html
    
    """
    class Meta:
        abstract = True
        verbose_name = _("Recurrence Set")
        verbose_name_plural = _("Recurrence Sets")
    
    every = models.IntegerField(_("Repeat every (value)"),
        default=0)
    #~ every_unit = DurationUnits.field(_("Repeat every (unit)"),
    every_unit = Recurrencies.field(_("Repeat every (unit)"),
        default=Recurrencies.monthly,
        blank=True) # iCal:DURATION
        
    monday    = models.BooleanField(Weekdays.monday.text)
    tuesday   = models.BooleanField(Weekdays.tuesday.text)
    wednesday = models.BooleanField(Weekdays.wednesday.text)
    thursday  = models.BooleanField(Weekdays.thursday.text)
    friday    = models.BooleanField(Weekdays.friday.text)
    saturday  = models.BooleanField(Weekdays.saturday.text)
    sunday    = models.BooleanField(Weekdays.sunday.text)
    
    max_occurences = models.PositiveIntegerField(
        _("Number of occurences"),
        blank=True,null=True)
        
        
    @dd.displayfield(_("Where"))
    def where_text(self,ar):
        return unicode(self.company.city or self.company)
        
    @dd.displayfield(_("Description"))
    def what_text(self,ar):
        return unicode(self)
        
    @dd.displayfield(_("Times"))
    def times_text(self,ar):

        return "%s-%s" % (format_time(self.start_time),format_time(self.end_time))
        
    @dd.displayfield(_("When"))
    def weekdays_text(self,ar):
        weekdays = []
        for wd in Weekdays.objects():
            if getattr(self,wd.name):
                weekdays.append(unicode(wd.text))
        weekdays = ', '.join(weekdays)
        if self.every == 1:
            return _("Every %s") % weekdays
        return _("Every %snd %s") % (self.every,weekdays)
        
        
    calendar = models.ForeignKey(Calendar,null=True,blank=True,
        help_text=_("""\
The calendar to which events will be generated."""))
    #~ event_type = models.ForeignKey(EventType,null=True,blank=True)
    
    #~ rdates = models.TextField(_("Recurrence dates"),blank=True)
    #~ exdates = models.TextField(_("Excluded dates"),blank=True)
    #~ rrules = models.TextField(_("Recurrence Rules"),blank=True)
    #~ exrules = models.TextField(_("Exclusion Rules"),blank=True)
    
    def get_next_date(self,date):
        if self.every_unit == Recurrencies.per_weekday:
            for i in range(7):
                date += ONE_DAY
                if self.is_available_on(date):
                    return date
            raise Exception("Failed to find available weekday.")
        return self.every_unit.add_duration(date,self.every)
    
    def is_available_on(self,date):
        wd = date.isoweekday() # Monday:1, Tuesday:2 ... Sunday:7
        wd = Weekdays.get_by_value(str(wd))
        rv = getattr(self,wd.name)
        #~ logger.info('20130529 is_available_on(%s) -> %s -> %s',date,wd,rv)
        return rv 
        
        
class RecurrenceSets(dd.Table):
    """
    The list of all :class:`Recurrence Sets <RecurrenceSet>`.
    """
    model = RecurrenceSet
    required = dd.required(user_groups='office')
    
    detail_layout = """
    id calendar uid summary start_date start_time
    description
    """
    #~ """
    #~ ## rdates exdates rrules exrules
    #~ ## EventsBySet    
    #~ """
    
    
class ComponentBase(mixins.ProjectRelated,StartedSummaryDescription):
    """
    Abstract model used as base class for 
    both :class:`Event` and :class:`Task`.
    """
    class Meta:
        abstract = True
        
    uid = models.CharField(_("UID"),
        max_length=200,
        blank=True) # ,null=True)




class Component(ComponentBase,
                #~ CalendarRelated,
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
        
    calendar = models.ForeignKey(Calendar,verbose_name=_("Calendar"),blank=True,null=True)
        
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
        if not self.calendar:
            self.calendar = self.user.calendar
        if not self.access_class:
            self.access_class = self.user.access_class
            #~ self.access_class = AccessClasses.public
        super(Component,self).save(*args,**kw)
        
    def on_duplicate(self,ar,master):
        self.auto_type = None
        
    def disabled_fields(self,ar):
        if self.auto_type:
            #~ return settings.SITE.TASK_AUTO_FIELDS
            return self.DISABLED_AUTO_FIELDS
        return []
        
    def get_uid(self):
        """
        This is going to be used when sending 
        locally created components to a remote calendar.
        """
        if self.uid:
            return self.uid
        if not settings.SITE.uid:
            raise Exception('Cannot create local calendar components because settings.SITE.uid is empty.')
        return "%s@%s" % (self.pk,settings.SITE.uid)
            

    #~ def on_user_change(self,request):
        #~ raise NotImplementedError
        #~ self.user_modified = True
        
    #~ def summary_row(self,ui,rr,**kw):
        #~ html = contacts.PartnerDocument.summary_row(self,ui,rr,**kw)
        #~ if self.summary:
            #~ html += '&nbsp;: %s' % cgi.escape(force_unicode(self.summary))
        #~ html += _(" on ") + dbutils.dtos(self.start_date)
        #~ return html
        
    def summary_row(self,ar,**kw):
        #~ logger.info("20120217 Component.summary_row() %s", self)
        #~ if self.owner and not self.auto_type:
        #~ html = ui.ext_renderer.href_to(self)
        html = ar.href_to(self)
        if self.start_time:
            #~ html += _(" at ") + unicode(self.start_time)
            html += _(" at ") + self.start_time.strftime(settings.SITE.time_format_strftime)
        if self.state:
            html += ' [%s]' % cgi.escape(force_unicode(self.state))
        if self.summary:
            html += '&nbsp;: %s' % cgi.escape(force_unicode(self.summary))
            #~ html += ui.href_to(self,force_unicode(self.summary))
        #~ html += _(" on ") + dbutils.dtos(self.start_date)
        #~ if self.owner and not self.owner.__class__.__name__ in ('Person','Company'):
            #~ html += " (%s)" % reports.summary_row(self.owner,ui,rr)
        if self.project:
            html += " (%s)" % dd.summary_row(self.project,ar)
            #~ print 20120217, self.project.__class__, self
            #~ html += " (%s)" % self.project.summary_row(ui)
        return html
        #~ return super(Event,self).summary_row(ui,rr,**kw)
        
#~ Component.owner.verbose_name = _("Automatically created by")

class ExtAllDayField(dd.VirtualField):
    """
    An editable virtual field needed for 
    communication with the Ext.ensible CalendarPanel
    because we consider the "all day" checkbox 
    equivalent to "empty start and end time fields".
    """
    
    editable = True
    
    def __init__(self,*args,**kw):
        dd.VirtualField.__init__(self,models.BooleanField(*args,**kw),None)
        
    def set_value_in_object(self,request,obj,value):
        if value:
            obj.end_time = None
            obj.start_time = None
        else:
            if not obj.start_time:
                obj.start_time = datetime.time(9,0,0)
            if not obj.end_time:
                obj.end_time = datetime.time(10,0,0)
        #~ obj.save()
        
    def value_from_object(self,obj,ar):
        #~ logger.info("20120118 value_from_object() %s",dd.obj2str(obj))
        return (obj.start_time is None)
        
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




#~ bases = (Component,Ended,mixins.TypedPrintable,outbox.Mailable, postings.Postable)
#~ class Event(*bases):
class Event(Component,Ended,
    mixins.TypedPrintable,
    outbox.Mailable, 
    postings.Postable):
    """
    A Calendar Event (french "Rendez-vous", german "Termin") 
    is a planned ("scheduled") lapse of time where something happens.
    """
    
    class Meta:
        #~ abstract = True
        verbose_name = pgettext(u"cal",u"Event")
        verbose_name_plural = pgettext(u"cal",u"Events")
        
    transparent = models.BooleanField(_("Transparent"),default=False,help_text=_("""\
Indicates that this Event shouldn't prevent other Events at the same time."""))
    #~ type = models.ForeignKey(EventType,null=True,blank=True)
    room = models.ForeignKey(Room,null=True,blank=True) # iCal:LOCATION
    priority = models.ForeignKey(Priority,null=True,blank=True)
    #~ priority = Priority.field(_("Priority"),blank=True) # iCal:PRIORITY
    state = EventStates.field(default=EventStates.suggested) # iCal:STATUS
    #~ status = models.ForeignKey(EventStatus,verbose_name=_("Status"),blank=True,null=True) # iCal:STATUS
    #~ duration = dd.FieldSet(_("Duration"),'duration_value duration_unit')
    #~ duration_value = models.IntegerField(_("Duration value"),null=True,blank=True) # iCal:DURATION
    #~ duration_unit = DurationUnit.field(_("Duration unit"),blank=True) # iCal:DURATION
    #~ repeat_value = models.IntegerField(_("Repeat every"),null=True,blank=True) # iCal:DURATION
    #~ repeat_unit = DurationUnit.field(verbose_name=_("Repeat every"),null=True,blank=True) # iCal:DURATION
    all_day = ExtAllDayField(_("all day"))
    #~ all_day = models.BooleanField(_("all day"),default=False)
    
    if settings.SITE.user_model:
        assigned_to = models.ForeignKey(settings.SITE.user_model,
            verbose_name=_("Assigned to"),
            related_name="cal_events_assigned",
            blank=True,null=True
            )
    else:
        assigned_to = dd.DummyField()
        
        
    def is_editable_state(self):
        return self.state in (EventStates.suggested, EventStates.draft)
        
    def is_user_modified(self):
        return self.state != EventStates.suggested
        
    def after_send_mail(self,mail,ar,kw):
        if self.state == EventStates.assigned:
            self.state = EventStates.notified
            kw['message'] += '\n('  +_("Event %s has been marked *notified*.") % self + ')'
            self.save()
            
    def before_ui_save(self,ar,**kw):
        """
        Mark the event as "user modified" by setting a default state.
        This is important because EventGenerators may not modify any user-modified Events.
        """
        #~ logger.info("20130528 before_ui_save")
        if self.state is EventStates.suggested:
            self.state = EventStates.draft
        return super(Event,self).before_ui_save(ar,**kw)
        
    def on_create(self,ar):
        self.start_date = datetime.date.today()
        self.start_time = datetime.datetime.now().time()
        #~ if ar.subst_user is not None:
        self.assigned_to = ar.subst_user
        super(Event,self).on_create(ar)
        
    #~ def on_create(self,ar):
        #~ self.start_date = datetime.date.today()
        #~ self.start_time = datetime.datetime.now().time()
        #~ # default user is almost the same as for UserAuthored
        #~ # but we take the *real* user, not the "working as"
        #~ if self.user_id is None:
            #~ u = ar.user
            #~ if u is not None:
                #~ self.user = u
        #~ super(Event,self).on_create(ar)
        
        
        
    def get_postable_recipients(self):
        """return or yield a list of Partners"""
        if settings.SITE.is_installed('contacts') and issubclass(settings.SITE.project_model,contacts.Partner):
            if self.project:
                yield self.project
        for g in self.guest_set.all():
            yield g.partner
        #~ if self.user.partner:
            #~ yield self.user.partner
        
    def get_mailable_type(self):  
        return self.calendar
        
    def get_mailable_recipients(self):
        if settings.SITE.is_installed('contacts') and issubclass(settings.SITE.project_model,contacts.Partner):
            if self.project:
                yield ('to',self.project)
        for g in self.guest_set.all():
            yield ('to',g.partner)
        if self.user.partner:
            yield ('cc',self.user.partner)
            
    #~ def get_mailable_body(self,ar):
        #~ return self.description
        
    def get_system_note_recipients(self,ar,silent):
        if self.user != ar.user:
            yield "%s <%s>" % (unicode(self.user),self.user.email)
        if silent:
            return
        for g in self.guest_set.all():
            if g.partner.email:
                yield "%s <%s>" % (unicode(g.partner),g.partner.email)
      
        
    @dd.displayfield(_("When"))
    def when_text(self,ar):
        return when_text(self.start_date,self.start_time)
        
            
    @dd.displayfield(_("Link URL"))
    def url(self,ar): return 'foo'
    
    @dd.virtualfield(dd.DisplayField(_("Reminder")))
    def reminder(self,request): return False
    #~ reminder.return_type = dd.DisplayField(_("Reminder"))

    def get_print_language(self,bm):
        if settings.SITE.project_model is not None and self.project:
            return self.project.get_print_language(bm)
        return self.user.language
        
    @classmethod
    def on_analyze(cls,lino):
        cls.DISABLED_AUTO_FIELDS = dd.fields_list(cls,
            '''summary''')

dd.update_field(Event,'user',verbose_name=_("Responsible user"))


class EventDetail(dd.FormLayout):
    start = "start_date start_time"
    end = "end_date end_time"
    main = """
    calendar summary user assigned_to
    start end #all_day #duration state
    room priority access_class transparent #rset 
    owner created:20 modified:20  
    description
    GuestsByEvent outbox.MailsByController
    """
class EventInsert(EventDetail):
    main = """
    calendar summary 
    start end 
    room priority access_class transparent 
    """
    
#~ class NextDateAction(dd.ListAction):
    #~ label = _("Next")
    #~ # action_name = 'next'
    #~ default_format = ext_requests.URL_FORMAT_JSON
    
    #~ def setup_action_request(self,actor,ar):
        #~ # print "coucou"
        #~ # assert row is None
        #~ dates_from = ar.param_values.dates_from or datetime.date.today()
        #~ dates_to = ar.param_values.dates_to or dates_from
        #~ ar.param_values.define('dates_from',dates_from + ONE_DAY)
        #~ ar.param_values.define('dates_to',dates_to + ONE_DAY)
        #~ # ar.param_values.dates_to += ONE_DAY
        #~ # logger.info("20121203 cal.NextDateAction.setup_action_request() %s",ar.param_values)
        #~ # return ar.success_response(refresh=True)
    
    
unclear_event_states = (EventStates.suggested,EventStates.draft,EventStates.notified)

class Events(dd.Table):
    help_text = _("A List of calendar entries. Each entry is called an event.")
    #~ debug_permissions = True
    model = 'cal.Event'
    required = dd.required(user_groups='office',user_level='manager')
    #~ column_names = 'start_date start_time user summary workflow_buttons calendar *'
    column_names = 'when_text:20 user summary calendar *'
    #~ column_names = 'start_date start_time user summary calendar *'
    
    hidden_columns = """
    priority access_class transparent
    owner created modified
    description
    uid sequence auto_type build_time owner owner_id owner_type 
    end_date end_time
    """
    
    #~ active_fields = ['all_day']
    order_by = ["start_date","start_time"]
    
    detail_layout = EventDetail()
    insert_layout = EventInsert()
    
    params_panel_hidden = True
    
    parameters = dict(
        #~ dates_from = dd.DatePickerField(_("Date from"),
        dates_from = models.DateField(_("Date from"),
            blank=True,null=True,help_text=u"""\
Nur Termine ab diesem Datum."""),
        #~ dates_to = dd.DatePickerField(_("until"),
        dates_to = models.DateField(_("until"),
            blank=True,null=True,help_text=u"""\
Nur Termine bis zu diesem Datum."""),
        user = models.ForeignKey(settings.SITE.user_model,
            verbose_name=_("Responsible user"),
            blank=True,null=True,
            help_text=u"""\
Nur Termine dieses Benutzers."""),
        assigned_to = models.ForeignKey(settings.SITE.user_model,
            verbose_name=_("Assigned to"),
            blank=True,null=True,
            help_text=u"""\
Nur Termine, die diesem Benutzer zugewiesen sind."""),
        state = EventStates.field(blank=True,help_text=u"""\
Nur Termine in diesem Bearbeitungszustand."""),
        unclear = models.BooleanField(_("Unclear events"))
    )
    
    params_layout = """
    dates_from dates_to user assigned_to state unclear
    """
    #~ params_layout = dd.Panel("""
    #~ dates_from dates_to other
    #~ """,other="""
    #~ user 
    #~ assigned_to 
    #~ state
    #~ """)
    
    #~ next = NextDateAction() # doesn't yet work. 20121203
    
    
    @classmethod
    def get_request_queryset(self,ar):
        #~ logger.info("20121010 Clients.get_request_queryset %s",ar.param_values)
        qs = super(Events,self).get_request_queryset(ar)
            
        if ar.param_values.user:
            qs = qs.filter(user=ar.param_values.user)
        if ar.param_values.assigned_to:
            qs = qs.filter(assigned_to=ar.param_values.assigned_to)

        if ar.param_values.state:
            qs = qs.filter(state=ar.param_values.state)
            
        if ar.param_values.unclear:
            qs = qs.filter(state__in=unclear_event_states)
            
        if ar.param_values.dates_from:
            if ar.param_values.dates_to:
                qs = qs.filter(start_date__gte=ar.param_values.dates_from)
            else:
                qs = qs.filter(start_date=ar.param_values.dates_from)
        if ar.param_values.dates_to:
            qs = qs.filter(start_date__lte=ar.param_values.dates_to)
        return qs
        
    @classmethod
    def get_title_tags(self,ar):
        for t in super(Events,self).get_title_tags(ar):
            yield t
        if ar.param_values.dates_from or ar.param_values.dates_to:
            yield unicode(_("Dates %(min)s to %(max)s") % dict(
              min=ar.param_values.dates_from or'...',
              max=ar.param_values.dates_to or '...'))
              
        if ar.param_values.state:
            yield unicode(ar.param_values.state)
            
        if ar.param_values.user:
            yield unicode(ar.param_values.user)
            
        if ar.param_values.assigned_to:
            yield unicode(self.parameters['assigned_to'].verbose_name) + ' ' + unicode(ar.param_values.assigned_to)

    
class EventsByCalendar(Events):
    master_key = 'calendar'
    
#~ class EventsByType(Events):
    #~ master_key = 'type'
    
#~ class EventsByPartner(Events):
    #~ required = dd.required(user_groups='office')
    #~ master_key = 'user'
    
class EventsByRoom(Events):
    """
    Displays the :class:`Events <Event>` at a given :class:`Room`.
    """
    master_key = 'room'

class EventsByController(Events):
    required = dd.required(user_groups='office')
    master_key = 'owner'
    column_names = 'when_text:20 summary workflow_buttons id'

if settings.SITE.project_model:    
  
    class EventsByProject(Events):
        required = dd.required(user_groups='office')
        master_key = 'project'
    
if settings.SITE.user_model:    
  
    #~ class MyEvents(Events,mixins.ByUser):
    class MyEvents(Events):
        #~ label = _("My events")
        help_text = _("Table of all my calendar events.")
        required = dd.required(user_groups='office')
        #~ column_names = 'start_date start_time calendar project summary workflow_buttons *'
        column_names = 'when_text:20 calendar project summary *'
        
        @classmethod
        def param_defaults(self,ar,**kw):
            kw = super(MyEvents,self).param_defaults(ar,**kw)
            kw.update(user=ar.get_user())
            return kw
        
        
    class MyUnclearEvents(MyEvents):
        label = _("My unclear events")
        help_text = _("Events which probably need your attention.")
        #~ required = dd.required(user_groups='office')
        column_names = 'when_text:20 project summary workflow_buttons *'
        #~ known_values = dict(assigned_to=EventStates.assigned)
        #~ master_key = 'assigned_to'
        
        @classmethod
        def param_defaults(self,ar,**kw):
            kw = super(MyUnclearEvents,self).param_defaults(ar,**kw)
            kw.update(unclear=True)
            kw.update(dates_from=datetime.date.today())
            kw.update(dates_to=datetime.date.today()+ONE_DAY)
            return kw
        
    class EventsAssignedToMe(Events):
        #~ label = _("Events assigned to me")
        help_text = _("Table of events assigned to me.")
        #~ master_key = 'assigned_to'
        required = dd.required(user_groups='office')
        column_names = 'when_text:20 project summary workflow_buttons *'
        #~ known_values = dict(assigned_to=EventStates.assigned)
        
        @classmethod
        def param_defaults(self,ar,**kw):
            kw = super(EventsAssignedToMe,self).param_defaults(ar,**kw)
            kw.update(assigned_to=ar.get_user())
            return kw
        
        
    #~ class EventsAssigned(Events):
        #~ label = _("Assigned Events")
        #~ help_text = _("Table of all events assigned to somebody.")
        #~ required = dd.required(user_groups='office',user_level='manager')
        #~ column_names = 'start_date start_time user project summary workflow_buttons *'
        #~ # known_values = dict(state=EventStates.assigned)
        #~ filter = models.Q(assigned_to__isnull=False)
        
        
    #~ class EventsNotified(Events):
        #~ help_text = _("Table of all notified events (waiting to become scheduled).")
        #~ label = _("Notified Events")
        #~ required = dd.required(user_groups='office',user_level='manager')
        #~ column_names = 'start_date start_time user project summary workflow_buttons *'
        #~ known_values = dict(state=EventStates.notified)
        
    #~ class MyEventsNotified(EventsNotified,MyEvents):
        #~ help_text = _("Table of my notified events (waiting to become scheduled).")
        #~ required = dd.required(user_groups='office')
        #~ column_names = 'start_date start_time project summary workflow_buttons *'
        #~ label = _("My notified Events")
        
    #~ class EventsToNotify(Events):
        #~ """
        #~ A list of events that need to be notified (i.e. communicated to the guests). 
        #~ Clicking on :attr:`Event.mark_notified` 
        #~ will remove this Event from this 
        #~ table and make it appear 
        #~ in :class:`MyEventsToConfirm`.
        #~ or :class:`MyEventsConfirmed`.
        #~ """
        #~ help_text = _("Table of all events that need to be communicated to guests.")
        #~ required = dict(user_level='manager',user_groups='office')
        #~ column_names = 'start_date start_time user project summary workflow_buttons *'
        #~ label = _("Events to notify")
        #~ order_by = ["start_date","start_time"]
        #~ filter = models.Q(state=EventStates.scheduled)
        
    #~ class MyEventsToNotify(EventsToNotify,MyEvents):
        #~ help_text = _("Table of all my events that need to be communicated to guests.")
        #~ required = dict(user_groups='office')
        #~ column_names = 'start_date start_time project summary workflow_buttons *'
        #~ label = _("My events to notify")
        
    #~ class EventsToSchedule(Events):
        #~ """
        #~ A list of events that aren't yet scheduled. 
        #~ The user is supposed to fill at least a start_date and start_time.
        #~ Clicking on "mark scheduled" 
        #~ means "I made up my mind on when this event should happen"
        #~ and will remove this Event from this 
        #~ table and make it appear in 
        #~ :class:`EventsToNotify` and 
        #~ :class:`MyEventsToNotify`.
        #~ """
        #~ help_text = _("Table of all events that need to be scheduled.")
        #~ label = _("Events to schedule")
        #~ required = dict(user_groups='office',user_level='manager')
        #~ column_names = 'start_date start_time user project summary workflow_buttons *'
        #~ filter = models.Q(state__in=(EventStates.blank_item,EventStates.draft))
        
    #~ class MyEventsToSchedule(EventsToSchedule,MyEvents):
        #~ help_text = _("Table of all my events that need to be scheduled.")
        #~ required = dict(user_groups='office')
        #~ column_names = 'start_date start_time project summary workflow_buttons *'
        #~ label = _("My events to schedule")
        
    #~ class EventsToConfirm(MyEvents):
        #~ """
        #~ A list of events that need to be confirmed
        #~ (i.e. the user made sure that the guests received 
        #~ their notification and plan to attend to the event). 
        #~ """
        #~ help_text = _("Table of all events that are waiting for confirmation from guests.")
        #~ required = dict(user_level='manager',user_groups='office')
        #~ column_names = 'start_date start_time project user summary workflow_buttons *'
        #~ label = _("Events to confirm")
        #~ order_by = ["start_date","start_time"]
        #~ filter = models.Q(state=EventStates.scheduled)
        
    #~ class MyEventsToConfirm(EventsToConfirm):
        #~ help_text = _("Table of all my events that are waiting for confirmation from guests.")
        #~ required = dict(user_groups='office')
        #~ label = _("My events to confirm")
        #~ column_names = 'start_date start_time project summary workflow_buttons *'
        
    class MyEventsToday(MyEvents):
        required = dd.required(user_groups='office')
        help_text = _("Table of my events per day.")
        column_names = 'start_time summary workflow_buttons *'
        label = _("My events today")
        order_by = ['start_time']
        
        parameters = dict(
          date = models.DateField(_("Date"),
          blank=True,default=datetime.date.today),
        )
        @classmethod
        def get_request_queryset(self,ar):
            qs = super(MyEventsToday,self).get_request_queryset(ar)
            #~ if ar.param_values.date:
            return qs.filter(start_date=ar.param_values.date)
            #~ return qs
            
        @classmethod
        def create_instance(self,ar,**kw):
            kw.update(start_date=ar.param_values.date)
            return super(MyEventsToday,self).create_instance(ar,**kw)

        #~ @classmethod
        #~ def setup_request(self,rr):
            #~ rr.known_values = dict(start_date=datetime.date.today())
            #~ super(MyEventsToday,self).setup_request(rr)
            

#~ class Task(Component,contacts.PartnerDocument):
class Task(Component):
    """
    A Task is when a user plans to to something 
    (and optionally wants to get reminded about it).
    """
    #~ workflow_state_field = 'state'
    
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
    #~ done = models.BooleanField(_("Done"),default=False) # iCal:COMPLETED
    percent = models.IntegerField(_("Duration value"),null=True,blank=True) # iCal:PERCENT
    state = TaskStates.field(default=TaskStates.todo) # iCal:STATUS
    #~ status = models.ForeignKey(TaskStatus,verbose_name=_("Status"),blank=True,null=True) # iCal:STATUS
    
    #~ @dd.action(_("Done"),required=dict(states=['','todo','started']))
    #~ @dd.action(TaskState.todo.text,required=dict(states=['']))
    #~ def mark_todo(self,ar):
        #~ self.state = TaskState.todo
        #~ self.save()
        #~ return ar.success_response(refresh=True)
    
    #~ @dd.action(TaskState.done.text,required=dict(states=['','todo','started']))
    #~ def mark_done(self,ar):
        #~ self.state = TaskState.done
        #~ self.save()
        #~ return ar.success_response(refresh=True)
    
    #~ @dd.action(TaskState.started.text,required=dict(states=['','todo']))
    #~ def mark_started(self,ar):
        #~ self.state = TaskState.started
        #~ self.save()
        #~ return ar.success_response(refresh=True)
    
    #~ @dd.action(TaskState.sleeping.text,required=dict(states=['','todo']))
    #~ def mark_sleeping(self,ar):
        #~ self.state = TaskState.sleeping
        #~ self.save()
        #~ return ar.success_response(refresh=True)
    

    def before_ui_save(self,ar,**kw):
        if self.state == TaskStates.todo:
            self.state = TaskStates.started
        return super(Task,self).before_ui_save(ar,**kw)
        
    #~ def on_user_change(self,request):
        #~ if not self.state:
            #~ self.state = TaskState.todo
        #~ self.user_modified = True
        
    def is_user_modified(self):
        return self.state != TaskStates.todo
        
    @classmethod
    def on_analyze(cls,lino):
        #~ lino.TASK_AUTO_FIELDS = dd.fields_list(cls,
        cls.DISABLED_AUTO_FIELDS = dd.fields_list(cls,
            '''start_date start_time summary''')
        super(Task,cls).on_analyze(lino)

    #~ def __unicode__(self):
        #~ return "#" + str(self.pk)
        

class Tasks(dd.Table):
    help_text = _("""A calendar task is something you need to do.
    """)
    #~ debug_permissions = True
    model = 'cal.Task'
    required = dd.required(user_groups='office',user_level='manager')
    column_names = 'start_date summary workflow_buttons *'
    order_by = ["-start_date","-start_time"]
    #~ hidden_columns = set('owner_id owner_type'.split())
    
    #~ detail_layout = """
    #~ start_date status due_date user  
    #~ summary 
    #~ created:20 modified:20 owner #owner_type #owner_id
    #~ description #notes.NotesByTask    
    #~ """
    detail_layout = """
    start_date due_date id workflow_buttons 
    summary 
    user project 
    calendar owner created:20 modified:20   
    description #notes.NotesByTask
    """
    insert_layout = dd.FormLayout("""
    summary
    user project
    """,window_size=(50,'auto'))
    
class TasksByController(Tasks):
    master_key = 'owner'
    required = dd.required(user_groups='office')
    column_names = 'start_date summary workflow_buttons id'
    #~ hidden_columns = set('owner_id owner_type'.split())

if settings.SITE.user_model:    
  
    #~ class RemindersByUser(dd.Table):
    class TasksByUser(Tasks):
        """
        Shows the list of automatically generated tasks for this user.
        """
        #~ model = Task
        #~ label = _("Reminders")
        master_key = 'user'
        required = dd.required(user_groups='office')
        #~ column_names = "start_date summary *"
        #~ order_by = ["start_date"]
        #~ filter = Q(auto_type__isnull=False)
        
    class MyTasks(Tasks,mixins.ByUser):
        required = dd.required(user_groups='office')
        #~ required = dict()
        help_text = _("Table of all my tasks.")
        column_names = 'start_date summary workflow_buttons *'
    
    class MyTasksToDo(MyTasks):
        help_text = _("Table of my tasks marked 'to do'.")
        column_names = 'start_date summary workflow_buttons *'
        label = _("To-do list")
        #~ filter = models.Q(state__in=(TaskState.blank_item,TaskState.todo,TaskState.started))
        filter = models.Q(
            start_date__lte=datetime.date.today()+dateutil.relativedelta.relativedelta(days=1),
            state__in=(TaskStates.todo,TaskStates.started))
    
if settings.SITE.project_model:    
  
    class TasksByProject(Tasks):
        required = dd.required(user_groups='office')
        master_key = 'project'
        column_names = 'start_date user summary workflow_buttons *'
    

class GuestRole(mixins.PrintableType,outbox.MailableType,dd.BabelNamed):
    templates_group = 'cal/Guest'
    
    class Meta:
        verbose_name = _("Guest Role")
        verbose_name_plural = _("Guest Roles")


class GuestRoles(dd.Table):
    help_text = _("""The role of a guest expresses what the 
    partner is going to do there.""")
    model = GuestRole
    required = dd.required(user_groups='office',user_level='admin')
    detail_layout = """
    id name
    build_method template email_template attach_to_email
    cal.GuestsByRole
    """
    

class Guest(mixins.TypedPrintable,outbox.Mailable):
    
    workflow_state_field = 'state'
    
    class Meta:
        verbose_name = _("Guest")
        verbose_name_plural = _("Guests")
        
        
    event = models.ForeignKey('cal.Event',
        verbose_name=_("Event")) 
        
    partner = dd.ForeignKey('contacts.Partner')

    role = models.ForeignKey('cal.GuestRole',
        verbose_name=_("Role"),
        blank=True,null=True) 
        
    #~ state = GuestStates.field(blank=True)
    state = GuestStates.field(default=GuestStates.invited)
    #~ status = models.ForeignKey(GuestStatus,verbose_name=_("Status"),blank=True,null=True)
    
    #~ confirmed = models.DateField(
        #~ blank=True,null=True,
        #~ verbose_name=_("Confirmed"))

    remark = models.CharField(
        _("Remark"),max_length=200,blank=True)
        
    def get_user(self):
        # used to apply `owner` requirement in GuestState
        return self.event.user
    user = property(get_user)

    #~ def __unicode__(self):
        #~ return self._meta.verbose_name + " #" + str(self.pk)
        
    def __unicode__(self):
        return u'%s #%s ("%s")' % (self._meta.verbose_name,self.pk,self.event)

    def get_printable_type(self):
        return self.role
        
    def get_mailable_type(self):  
        return self.role

    def get_mailable_recipients(self):
        yield ('to',self.partner)
        
    @dd.displayfield(_("Event"))
    def event_summary(self,ar):
        return ar.href_to(self.event,event_summary(self.event,ar.get_user()))
        #~ return event_summary(self.event,ar.get_user())
        
    #~ def before_ui_save(self,ar,**kw):
        #~ if not self.state:
            #~ self.state = GuestStates.invited
        #~ return super(Guest,self).before_ui_save(ar,**kw)
        
    #~ def on_user_change(self,request):
        #~ if not self.state:
            #~ self.state = GuestState.invited
        

    #~ def get_recipient(self):
        #~ return self.partner
    #~ recipient = property(get_recipient)
        
    #~ @classmethod
    #~ def setup_report(cls,rpt):
        #~ mixins.CachedPrintable.setup_report(rpt)
        #~ outbox.Mailable.setup_report(rpt)
        
    #~ @dd.action(_("Invite"),required=dict(states=['']))
    #~ def invite(self,ar):
        #~ self.state = GuestState.invited
        
    #~ @dd.action(_("Confirm"),required=dict(states=['invited']))
    #~ def confirm(self,ar):
        #~ self.state = GuestState.confirmed
    
#~ class Guests(dd.Table,workflows.Workflowable):
class Guests(dd.Table):
    help_text = _("""A guest is a partner invited to an event.
    """)
    model = Guest
    required = dd.required(user_groups='office',user_level='admin')
    column_names = 'partner role workflow_buttons remark event *'
    #~ workflow_state_field = 'state'
    #~ column_names = 'contact role state remark event *'
    #~ workflow_actions = ['invite','notify']
    #~ workflow_owner_field = 'event__user'
    
    #~ def setup_actions(self):
        #~ super(dd.Table,self).setup_actions()
        #~ self.add_action(mails.CreateMailAction())
        
class GuestsByEvent(Guests):
    master_key = 'event'
    required = dd.required(user_groups='office')

class GuestsByRole(Guests):
    master_key = 'role'
    required = dd.required(user_groups='office')

if settings.SITE.is_installed('contacts'):
  
  class GuestsByPartner(Guests):
      master_key = 'partner'
      required = dd.required(user_groups='office')
      column_names = 'event role workflow_buttons remark *'

  class MyPresences(GuestsByPartner):
      required = dd.required(user_groups='office')
      order_by = ['event__start_date','event__start_time']
      label = _("My presences")
      help_text = _("""Shows all my presences in calendar events, independently of their state.""")
      column_names = 'event__start_date event__start_time event_summary role workflow_buttons remark *'
      
      @classmethod
      def get_request_queryset(self,ar):
          ar.master_instance = ar.get_user().partner
          return super(MyPresences,self).get_request_queryset(ar)
          
      
  class MyPendingInvitations(MyPresences):
      help_text = _("""Shows received invitations which I must accept or reject.""")
      label = _("My received invitations")
      filter = models.Q(state=GuestStates.invited)
    
#~ class MySentInvitations(Guests):
    #~ help_text = _("""Shows invitations which I sent accept or reject.""")
  
    #~ label = _("My Sent Invitations")
    
    #~ order_by = ['event__start_date','event__start_time']
    #~ column_names = 'event__start_date event__start_time event_summary role workflow_buttons remark *'
    
    #~ @classmethod
    #~ def get_request_queryset(self,ar):
        #~ datelimit = datetime.date.today() + dateutil.relativedelta.relativedelta(days=-7)
        #~ ar.filter = models.Q(event__user=ar.get_user(),event__start_date__gte=datelimit)
        #~ return super(MySentInvitations,self).get_request_queryset(ar)
    
#~ class MyPendingSentInvitations(MySentInvitations):
    #~ help_text = _("""Shows invitations which I sent, and for which I accept or reject.""")
    #~ label = _("My Pending Sent Invitations")
    #~ @classmethod
    #~ def get_request_queryset(self,ar):
        #~ ar.filter = models.Q(state=GuestStates.invited,event__user=ar.get_user())
        #~ # ! note that we skip one mro parent:
        #~ return super(MySentInvitations,self).get_request_queryset(ar)
    

    
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
        models.Q(state=None) | models.Q(state__lte=EventStates.scheduled),
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
    of the specified `type` and `owner`.
    
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
      

class ExtDateTimeField(dd.VirtualField):
    """
    An editable virtual field needed for 
    communication with the Ext.ensible CalendarPanel
    because Lino uses two separate fields 
    `start_date` and `start_time`
    or `end_date` and `end_time` while CalendarPanel expects 
    and sends single DateTime values.
    """
    editable = True
    def __init__(self,name_prefix,alt_prefix,label):
        self.name_prefix = name_prefix
        self.alt_prefix = alt_prefix
        rt = models.DateTimeField(label)
        dd.VirtualField.__init__(self,rt,None)
    
    def set_value_in_object(self,request,obj,value):
        obj.set_datetime(self.name_prefix,value)
        
    def value_from_object(self,obj,ar):
        #~ logger.info("20120118 value_from_object() %s",dd.obj2str(obj))
        return obj.get_datetime(self.name_prefix,self.alt_prefix)

class ExtSummaryField(dd.VirtualField):
    """
    An editable virtual field needed for 
    communication with the Ext.ensible CalendarPanel
    because we want a customized "virtual summary" 
    that includes the project name.
    """
    editable = True
    def __init__(self,label):
        rt = models.CharField(label)
        dd.VirtualField.__init__(self,rt,None)
        
    def set_value_in_object(self,request,obj,value):
        if obj.project:
            s = unicode(obj.project)
            if value.startswith(s):
                value = value[len(s):]
        obj.summary = value
        
    def value_from_object(self,obj,ar):
        #~ logger.info("20120118 value_from_object() %s",dd.obj2str(obj))
        return settings.SITE.get_event_summary(obj,ar.get_user())


def user_calendars(qs,user):
    #~ Q = models.Q
    subs = Subscription.objects.filter(user=user).values_list('calendar__id',flat=True)
    #~ print 20120710, subs
    return qs.filter(id__in=subs)


if settings.SITE.use_extensible:
  
    def parsedate(s):
        return datetime.date(*settings.SITE.parse_date(s))
  
    class CalendarPanel(dd.Frame):
        """
        Opens the "Calendar View" (a special window with the Ext.ensible CalendarAppPanel).
        """
        required = dd.required(user_groups='office')
        label = _("Calendar")
        
        @classmethod
        def get_default_action(self):
            return CalendarAction()

    class PanelCalendars(Calendars):
        use_as_default_table = False
        required = dd.required(user_groups='office')
        #~ column_names = 'id name description color is_hidden'
        column_names = 'id babel_name description color is_hidden'
        
        @classmethod
        def get_request_queryset(self,ar):
            qs = super(PanelCalendars,self).get_request_queryset(ar)
            return user_calendars(qs,ar.get_user())
            
        @dd.displayfield()
        def babel_name(cls,self,ar):
            return dbutils.babelattr(self,'name')
            
        @dd.virtualfield(models.BooleanField(_('Hidden')))
        def is_hidden(cls,self,ar):
            return False
            #~ if self.user == ar.get_user():
                #~ return False
            #~ sub = Subscription.objects.get(user=ar.get_user(),calendar=self)
            #~ return sub.is_hidden

            
    class PanelEvents(Events):
        """
        The table used for Ext.ensible CalendarPanel.
        """
        required = dd.required(user_groups='office')
        use_as_default_table = False
        #~ parameters = dict(team_view=models.BooleanField(_("Team View")))
        
        column_names = 'id start_dt end_dt summary description user room calendar #rset url all_day reminder'
        
        start_dt = ExtDateTimeField('start',None,_("Start"))
        end_dt = ExtDateTimeField('end','start',_("End"))
        
        summary = ExtSummaryField(_("Summary"))
        #~ overrides the database field of same name
        
      
        @classmethod
        def parse_req(self,request,rqdata,**kw):
            #~ logger.info('20120710 %s', request.GET[requests.URL_PARAM_TEAM_VIEW])
          
            #~ filter = kw.get('filter',{})
            assert not kw.has_key('filter')
            fkw = {}
            #~ logger.info("20120118 filter is %r", filter)
            endDate = rqdata.get('ed',None)
            if endDate:
                d = parsedate(endDate)
                fkw.update(start_date__lte=d)
            startDate = rqdata.get('sd',None)
            if startDate:
                d = parsedate(startDate)
                #~ logger.info("startDate is %r", d)
                fkw.update(start_date__gte=d)
            #~ logger.info("20120118 filter is %r", filter)
            
            #~ subs = Subscription.objects.filter(user=request.user).values_list('calendar__id',flat=True)
            #~ filter.update(calendar__id__in=subs)
            
            filter = models.Q(**fkw)
            
            # who am i ?
            me = request.subst_user or request.user
            
            """
            If you override `parse_req`, then keep in mind that it will
            be called *before* Lino checks the requirements. 
            For example the user may be AnonymousUser even if 
            the requirements won't let it be executed.
            """
            
            if not me.profile.authenticated: 
                raise exceptions.PermissionDenied(
                    _("As %s you have no permission to run this action.") % me.profile)
                
                
            # show al my events
            for_me = models.Q(user=me)
            
            # also show events to which i am invited
            if me.partner:
                #~ me_as_guest = Guest.objects.filter(partner=request.user.partner)
                #~ for_me = for_me | models.Q(guest_set__count__gt=0)
                #~ for_me = for_me | models.Q(guest_count__gt=0)
                for_me = for_me | models.Q(guest__partner=me.partner)
            
            # in team view, show also events of all my team members
            tv = rqdata.get(constants.URL_PARAM_TEAM_VIEW,False)
            if tv and constants.parse_boolean(tv):
                # positive list of ACLs for events of team members
                team_classes = (None,AccessClasses.public,AccessClasses.show_busy)
                my_teams = Membership.objects.filter(user=me)
                we = settings.SITE.user_model.objects.filter(users_membership_set_by_user__team__in=my_teams)
                #~ team_ids = Membership.objects.filter(user=me).values_list('watched_user__id',flat=True)
                #~ for_me = for_me | models.Q(user__id__in=team_ids,access_class__in=team_classes)
                for_me = for_me | models.Q(user__in=we,access_class__in=team_classes)
            filter = filter & for_me
            #~ logger.info('20120710 %s', filter)
            kw.update(filter=filter)
            return kw
            
        #~ @classmethod
        #~ def get_request_queryset(self,ar):
            #~ qs = super(PanelEvents,self).get_request_queryset(ar)
            #~ return qs
            
            


    
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
        filter=flt & (models.Q(state=None) | models.Q(state__lte=EventStates.scheduled)))
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
    
def update_reminders(user):
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
      

class UpdateReminders(actions.RowAction):
    """
    Users can invoke this to re-generate their automatic tasks.
    """
    url_action_name = 'UpdateReminders'
    label = _('Update Reminders')
    
    callable_from = (actions.GridEdit, actions.ShowDetailAction)
        
    def run_from_ui(self,user,ar,**kw):
        logger.info("Updating reminders for %s",unicode(user))
        n = update_reminders(user)
        kw.update(success=True)
        msg = _("%(num)d reminders for %(user)s have been updated."
          ) % dict(user=user,num=n)
        logger.info(msg)
        return ar.ui.success(msg,**kw)
        

from lino.ui import models as ui

class Home(ui.Home):
    """
    Deserves better documentation.
    """
    #~ debug_permissions = True 

    label = ui.Home.label
    app_label = 'lino'
    detail_layout = """
    quick_links:80x1
    welcome
    coming_reminders:40x16 missed_reminders:40x16
    """
    
    @dd.virtualfield(dd.HtmlBox(_('Upcoming reminders')))
    def coming_reminders(cls,self,ar):
        return reminders_as_html(ar,days_forward=30,
            max_items=10,before='<ul><li>',separator='</li><li>',after="</li></ul>")

    @dd.virtualfield(dd.HtmlBox(_('Missed reminders')))
    def missed_reminders(cls,self,ar):
        return reminders_as_html(ar,days_back=90,
          max_items=10,before='<ul><li>',separator='</li><li>',after="</li></ul>")
          
          


#~ class MissedReminders(dd.Frame):
    #~ label = _('Missed reminders')
    
    #~ @classmethod
    #~ def value(cls,ar):
        #~ return reminders(ar.ui,ar.get_user(),days_back=90,
          #~ max_items=10,before='<ul><li>',separator='</li><li>',after="</li></ul>")
          
#~ class ComingReminders(dd.Frame):
    #~ label = _('Coming reminders')
    
    #~ @classmethod
    #~ def value(cls,ar):
        #~ return reminders(ar.ui,ar.get_user(),days_forward=30,
            #~ max_items=10,before='<ul><li>',separator='</li><li>',after="</li></ul>")



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
        'calendar',
        models.ForeignKey(Calendar,
            blank=True,null=True,
            verbose_name=_("Default calendar"),
            help_text=_("""The default calendar for your events and tasks.""")
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
    calendar access_class 
    cal.SubscriptionsByUser
    # cal.MembershipsByUser
    """)
    site.modules.users.Users.add_detail_tab('cal',"""
    cal_left:30 cal.TasksByUser:60
    """,MODULE_LABEL,required=dict(user_groups='office'))
    #~ site.modules.users.Users.add_detail_tab('cal.TasksByUser')
    
@dd.receiver(dd.pre_analyze)
def pre_analyze(sender,**kw):
    #~ logger.info("%s.set_merge_actions()",__name__)
    #~ modules = sender.modules
    sender.user_model.add_model_action(update_reminders=UpdateReminders())
    
    
MODULE_LABEL = _("Calendar")

def setup_main_menu(site,ui,profile,m): 
    m  = m.add_menu("cal",MODULE_LABEL)
    
    if site.use_extensible:
        m.add_action(CalendarPanel)
    m.add_action(MyEvents)
    #~ m.add_action(MyEventsToday)
    #~ m.add_action(MyEventsAssigned)
    #~ m.add_action(MyEventsNotified)
    
    #~ m.add_separator('-')
    #~ m.add_action(Events)
    #~ m.add_action(EventsReserved)
    #~ m.add_action(EventsAssigned)
    #~ m.add_action(EventsNotified)
    #~ m.add_action(EventsToSchedule)
    #~ m.add_action(EventsToNotify)
    #~ m.add_action(EventsToConfirm)
    
    m.add_separator('-')
    #~ m  = m.add_menu("tasks",_("Tasks"))
    m.add_action(MyTasks)
    m.add_action(MyTasksToDo)
    
    
    if True: # user.partner:
        m.add_separator('-')
        m.add_action(MyPresences)
        m.add_action(MyPendingInvitations)
    #~ m.add_action(MySentInvitations)
    #~ m.add_action(MyPendingSentInvitations)
    
  
#~ def setup_master_menu(site,ui,profile,m): 
    #~ pass
    
#~ def setup_my_menu(site,ui,profile,m): 
    #~ pass
    #~ m  = m.add_menu("cal",MODULE_LABEL)
    #~ m.add_action(MySubscriptions)
    
def setup_config_menu(site,ui,profile,m): 
    m  = m.add_menu("cal",MODULE_LABEL)
    m.add_action(Rooms)
    m.add_action(Priorities)
    #~ m.add_action(AccessClasses)
    #~ m.add_action(EventStatuses)
    #~ m.add_action(TaskStatuses)
    #~ m.add_action(EventTypes)
    m.add_action(GuestRoles)
    #~ m.add_action(GuestStatuses)
    m.add_action(Calendars)
  
def setup_explorer_menu(site,ui,profile,m):
    m  = m.add_menu("cal",MODULE_LABEL)
    m.add_action(Tasks)
    m.add_action(Guests)
    m.add_action(Subscriptions)
    #~ m.add_action(Memberships)
    m.add_action(EventStates)
    m.add_action(GuestStates)
    m.add_action(TaskStates)
    #~ m.add_action(RecurrenceSets)

def setup_quicklinks(site,ar,m):
    #~ print 20120706
    if site.use_extensible:
        #~ m.add_action(self.modules.cal.Panel)
        m.add_action(CalendarPanel)
        #~ m.add_action(MyEventsAssigned)
        #~ m.add_action(MyEventsNotified)
        #~ m.add_action(MyTasksToDo)
        
#~ def whats_up(site,ui,user):
    #~ MyEventsReserved
    #~ MyEventsAssigned
    #~ MyEventsNotified
    
def get_todo_tables(ar):
    yield (MyUnclearEvents, _("%d unclear events approaching.")) # "%d unklare Termine kommen näher"
    yield (MyPendingInvitations, _("%d invitations are waiting for your answer."))
    yield (MyTasksToDo,_("%d tasks to do"))
    #~ yield (MyEventsNotified,_("%d notified events"))
    yield (EventsAssignedToMe,_("%d events assigned to you"))
    

#~ dd.add_user_group('office',MODULE_LABEL)

customize_users()



