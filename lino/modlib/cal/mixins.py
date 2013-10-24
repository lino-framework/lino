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
Part of the :mod:`lino.modlib.cal` app.

Defines the mixins
:class:`Started` ,
:class:`Ended`,
:class:`EventGenerator` 
and :class:`RecurrenceSet` 
.

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
from django.utils import translation
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import pgettext_lazy as pgettext
#~ from django.utils.translation import string_concat
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import force_unicode


from lino import mixins
from lino import dd
from lino.utils import ONE_DAY

from lino.core import actions

from .utils import Recurrencies
from .utils import Weekdays


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
        
        



class UpdateReminders(actions.Action):
    url_action_name = 'update_reminders'
    label = _('Update Events')
    #~ label = _('Update Reminders')
    show_in_row_actions = True
    icon_name = 'lightning'
    
    callable_from = (actions.GridEdit, actions.ShowDetailAction)
        
    def run_from_ui(self,ar,**kw):
        ar.success(**kw)
        n = 0
        for obj in ar.selected_rows:
            if not ar.response.get('success'):
                ar.info("Aborting remaining rows")
                break
            ar.info("Updating reminders for %s...",unicode(obj))
            n += obj.update_reminders(ar)
            ar.response.update(refresh_all=True)

        msg = _("%d reminder(s) have been updated.") % n
        ar.info(msg)
        #~ ar.success(msg,**kw)

class EventGenerator(mixins.UserAuthored):
    """
    Base class for things that generate a suite of events.
    Examples
    :class:`isip.Contract`,     :class:`jobs.Contract`, 
    :class:`schools.Course`.
    
    """
    
    class Meta:
        abstract = True
        
    do_update_reminders = UpdateReminders()
    #~ holiday_calendar = dd.ForeignKey('cal.Calendar',
        #~ verbose_name=_("Holiday calendar"),
        #~ related_name="%(app_label)s_%(class)s_set_by_event_generator",
        #~ null=True,blank=True,
        #~ help_text=_("""Holiday calendar to which events will be generated."""))
    
        
    #~ def save(self,*args,**kw):
        #~ super(EventGenerator,self).save(*args,**kw)
        #~ if self.user is None:
            #~ self.update_reminders()
        #~ else:
            #~ dbutils.run_with_language(self.user.language,self.update_reminders)

    def update_cal_rset(self):
        raise NotImplementedError()
        #~ return self.exam_policy
        
    def update_cal_from(self,ar):
        """
        Return the date of the first Event to be generated.
        Return None if no Events should be generated.
        """
        raise NotImplementedError()
        #~ return self.applies_from
        
    #~ def get_conflict_calendars(self):
        #~ yield settings.SITE.site_config.site_calendar
        
        #~ sc = settings.SITE.site_config
        #~ if sc.holiday_event_type is not None and sc.holiday_event_type != self:
            #~ yield sc.holiday_event_type
        
    def update_cal_until(self):
        """Return the limit date until which to generate events.
        None means "no limit" (which de facto becomes `SiteConfig.farest_future`)
        """
        return None
        #~ raise NotImplementedError()
        #~ return self.date_ended or self.applies_until
        
    def update_cal_calendar(self):
        """
        Return the event_type for the events to generate.
        Returning None means: don't generate any events.
        """
        return None
        
    def get_events_language(self):
        if self.user is None: 
            return settings.SITE.get_default_language()
        return self.user.language
        
    def update_cal_summary(self,i):
        raise NotImplementedError()
        #~ return _("Evaluation %d") % i

    def update_reminders(self,ar):
        return self.update_auto_events(ar)
            
    def update_auto_events(self,ar):
        """
        Generate automatic calendar events owned by this contract.
        
        [NOTE1] if one event has been manually rescheduled, all following events
        adapt to the new rythm.
        
        """
        if settings.SITE.loading_from_dump: 
            #~ print "20111014 loading_from_dump"
            return 0
        qs = self.get_existing_auto_events()
        wanted = self.get_wanted_auto_events(ar)
        #~ logger.info("20131020 get_wanted_auto_events() returned %s",wanted)
        count = len(wanted)
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
                    subsequent = ', '.join([str(x.auto_type) for x in wanted.values()])
                    logger.info("""\
%d has been rescheduled from %s to %s, adapt subsequent dates (%s)""" % (e.auto_type,ae.start_date,e.start_date,subsequent))
                    delta = e.start_date - ae.start_date
                    for se in wanted.values():
                        se.start_date += delta
            else:
                self.compare_auto_event(e,ae)
        # create new Events for remaining wanted
        for ae in wanted.values():
            #~ e = settings.SITE.modules.cal.Event(**ae)
            self.before_auto_event_save(ae)
            ae.save()
        #~ logger.info("20130528 update_auto_events done")
        return count
            
    def compare_auto_event(self,obj,ae):
        original_state = dict(obj.__dict__)
        if obj.user != ae.user:
            obj.user = ae.user
        summary = force_unicode(ae.summary)
        if obj.summary != summary:
            obj.summary = summary
        if obj.start_date != ae.start_date:
            obj.start_date = ae.start_date
        if obj.end_date != ae.end_date:
            obj.end_date = ae.end_date
        if obj.start_time != ae.start_time:
            obj.start_time = ae.start_time
        if obj.end_time != ae.end_time:
            obj.end_time = ae.end_time
        if obj.event_type != ae.event_type:
            obj.event_type = ae.event_type
        self.before_auto_event_save(obj)
        if obj.__dict__ != original_state:
            obj.save()
            
    def before_auto_event_save(self,obj):
        """
        Called for automatically generated events after their automatic
        fields have been set and before the event is saved.
        This allows for application-specific "additional-automatic" fields. 
        E.g. the room field in `lino.modlib.courses`
        
        **Automatic event fields**:
        :class:`EventGenerator` 
        by default manages the following fields:
        
        - auto_type
        - user
        - summary
        - start_date, start_time
        - end_date, end_time
    
        
        """
        pass
            
      
    def get_wanted_auto_events(self,ar):
        """
        Return a dict which maps sequence number 
        to AttrDict instances which hold the wanted event.
        """
        wanted = dict()
        event_type = self.update_cal_calendar()
        if event_type is None:
            return wanted
        rset = self.update_cal_rset()
        #~ ar.info("20131020 rset %s",rset)
        #~ if rset and rset.every > 0 and rset.every_unit:
        if rset and rset.every_unit:
            date = self.update_cal_from(ar)
            if not date:
                #~ ar.info("20131020 no start date")
                return wanted
        else:
            ar.info("20131020 no recurrency")
            return wanted
        until = self.update_cal_until() \
            or settings.SITE.site_config.farest_future
            #~ or datetime.date.today().replace(year=2018)
        #~ if until < wanted:
            #~ raise Warning("Series ends before it was started!")
        i = 0
        max_events = rset.max_events or settings.SITE.site_config.max_auto_events
        Event = settings.SITE.modules.cal.Event
        with translation.override(self.get_events_language()):
          while i < max_events:
            if date > until: 
                ar.info("20131020 reached maximum date")
                break
            i += 1
            if settings.SITE.ignore_dates_before is None or date >= settings.SITE.ignore_dates_before:
                #~ we = AttrDict(
                we = settings.SITE.modules.cal.Event(
                    auto_type=i,
                    user=self.user,
                    start_date=date,
                    summary=self.update_cal_summary(i),
                    owner=self,
                    event_type=event_type,
                    start_time=rset.start_time,
                    end_time=rset.end_time)
                    
                #~ for cal in self.get_conflict_calendars():
                    #~ if cal is not None:
                        #~ while cal.conflicts_with_event(we):
                            #~ date = rset.get_next_date(date)
                            #~ if date is None or date > until: 
                                #~ return wanted
                            #~ we.start_date = date
                while we.has_conflicting_events():
                    ar.info("%s conflicts with %s. ",self,we.get_conflicting_events())
                    date = rset.get_next_date(date)
                    if date is None or date > until: 
                        ar.info("Failed to find another date for %s.",self)
                        return wanted
                    we.start_date = date
                    
                if rset.end_date is None:
                    #~ we.update(end_date=None)
                    we.end_date = None
                else:
                    duration = rset.end_date - rset.start_date
                    #~ we.update(end_date=we.start_date + duration)
                    we.end_date = we.start_date + duration
                wanted[i] = we
            date = rset.get_next_date(date)
            if date is None: 
                ar.info("20131020 no date left")
                break
        return wanted
                    
        
    def get_existing_auto_events(self):
        ot = ContentType.objects.get_for_model(self.__class__)
        return settings.SITE.modules.cal.Event.objects.filter(
            owner_type=ot,owner_id=self.pk,
            auto_type__isnull=False).order_by('auto_type')
        


  
    
  
    
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
    
    #~ every_unit = DurationUnits.field(_("Repeat every (unit)"),
    every_unit = Recurrencies.field(_("Recurrency"),
        default=Recurrencies.monthly,
        blank=True) # iCal:DURATION
    every = models.IntegerField(_("Repeat every"), default=0)
        
    monday    = models.BooleanField(Weekdays.monday.text)
    tuesday   = models.BooleanField(Weekdays.tuesday.text)
    wednesday = models.BooleanField(Weekdays.wednesday.text)
    thursday  = models.BooleanField(Weekdays.thursday.text)
    friday    = models.BooleanField(Weekdays.friday.text)
    saturday  = models.BooleanField(Weekdays.saturday.text)
    sunday    = models.BooleanField(Weekdays.sunday.text)
    
    max_events = models.PositiveIntegerField(
        _("Number of events"),
        blank=True,null=True)
        
    @classmethod
    def on_analyze(cls,lino):
        cls.WEEKDAY_FIELDS = dd.fields_list(cls,
            '''monday tuesday wednesday 
            thursday friday saturday  sunday    
            ''')
        super(RecurrenceSet,cls).on_analyze(lino)
            
    def disabled_fields(self,ar):
        rv = super(RecurrenceSet,self).disabled_fields(ar)
        if self.every_unit != Recurrencies.per_weekday:
            #~ return settings.SITE.TASK_AUTO_FIELDS
            rv |= self.WEEKDAY_FIELDS
        return rv
        
        
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
        
        
    #~ calendar = models.ForeignKey('cal.Calendar',null=True,blank=True,
        #~ help_text=_("""\
#~ The calendar to which events will be generated."""))

    #~ event_type = models.ForeignKey(EventType,null=True,blank=True)
    
    #~ rdates = models.TextField(_("Recurrence dates"),blank=True)
    #~ exdates = models.TextField(_("Excluded dates"),blank=True)
    #~ rrules = models.TextField(_("Recurrence Rules"),blank=True)
    #~ exrules = models.TextField(_("Exclusion Rules"),blank=True)
    
    def get_next_date(self,date):
        if self.every_unit == Recurrencies.once:
            return None
        if self.every_unit == Recurrencies.per_weekday:
            for i in range(7):
                date += ONE_DAY
                if self.is_available_on(date):
                    return date
            #~ raise Exception("Failed to find available weekday.")
            logger.info("%s : get_next_date() failed to find available weekday.",self)
            return None
        return self.every_unit.add_duration(date,self.every)
    
    def is_available_on(self,date):
        wd = date.isoweekday() # Monday:1, Tuesday:2 ... Sunday:7
        wd = Weekdays.get_by_value(str(wd))
        rv = getattr(self,wd.name)
        #~ logger.info('20130529 is_available_on(%s) -> %s -> %s',date,wd,rv)
        return rv 
        
dd.update_field(RecurrenceSet,'start_date',default = datetime.date.today)

class Reservation(RecurrenceSet,EventGenerator):
    "Base class for rooms.Booking and courses.Course"
    class Meta:
        abstract = True
    room = dd.ForeignKey('cal.Room',blank=True,null=True)
    max_date = models.DateField(
        blank=True,null=True,
        verbose_name=_("Generate events until"))
        
    def update_cal_until(self):
        return self.max_date
    
    def update_cal_rset(self):
        return self
        

