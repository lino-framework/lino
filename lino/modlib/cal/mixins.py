# -*- coding: UTF-8 -*-
# Copyright 2011-2014 Luc Saffre
# License: BSD (see file COPYING for details)

"""
Part of the :mod:`lino.modlib.cal` app.

Defines the mixins
:class:`Started` ,
:class:`Ended`,
:class:`EventGenerator`
and :class:`RecurrenceSet`.

"""

from __future__ import unicode_literals

import datetime

from django.conf import settings
from django.db import models
from django.utils import translation
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import force_unicode


from lino import mixins
from lino import dd, rt
from lino.utils import ONE_DAY
from lino.utils.xmlgen.html import E

from lino.core import actions

from .utils import Recurrencies
from .utils import Weekdays

from .workflows import EventStates


def format_time(t):
    if t is None:
        return ''
    return t.strftime(settings.SITE.time_format_strftime)


def daterange_text(a, b):
    if a == b:
        return a.strftime(settings.SITE.date_format_strftime)
    d = dict(min="...", max="...")
    if a:
        d.update(min=a.strftime(settings.SITE.date_format_strftime))
    if b:
        d.update(max=b.strftime(settings.SITE.date_format_strftime))
    return _("Dates %(min)s to %(max)s") % d


class Started(dd.Model):

    class Meta:
        abstract = True

    start_date = models.DateField(
        blank=True, null=True,
        verbose_name=_("Start date"))  # iCal:DTSTART
    start_time = models.TimeField(
        blank=True, null=True,
        verbose_name=_("Start time"))  # iCal:DTSTART
    #~ start = dd.FieldSet(_("Start"),'start_date start_time')

    def save(self, *args, **kw):
        """
        Fills default value "today" to start_date
        """
        if not self.start_date:
            self.start_date = settings.SITE.today()
        super(Started, self).save(*args, **kw)

    def set_datetime(self, name, value):
        #~ logger.info("20120119 set_datetime(%r)",value)
        setattr(self, name + '_date', value.date())
        t = value.time()
        if not t:
            t = None
        setattr(self, name + '_time', t)

    def get_datetime(self, name, altname=None):
        d = getattr(self, name + '_date')
        t = getattr(self, name + '_time')
        if not d and altname is not None:
            d = getattr(self, altname + '_date')
            if not t and altname is not None:
                t = getattr(self, altname + '_time')
        if not d:
            return None
        if t:
            return datetime.datetime.combine(d, t)
        else:
            return datetime.datetime(d.year, d.month, d.day)


class Ended(dd.Model):

    class Meta:
        abstract = True
    end_date = models.DateField(
        blank=True, null=True,
        verbose_name=_("End Date"))
    end_time = models.TimeField(
        blank=True, null=True,
        verbose_name=_("End Time"))
    #~ end = dd.FieldSet(_("End"),'end_date end_time')


class StartedSummaryDescription(Started):

    """
    """

    class Meta:
        abstract = True

    # iCal:SUMMARY
    summary = models.CharField(_("Summary"), max_length=200, blank=True)
    description = dd.RichTextField(
        _("Description"),
        blank=True,
        format='plain')
        # format='html')

    def __unicode__(self):
        return self._meta.verbose_name + " #" + str(self.pk)

    def summary_row(self, ar, **kw):
        elems = list(super(StartedSummaryDescription, self)
                     .summary_row(ar, **kw))

        if self.summary:
            elems.append(': %s' % self.summary)
        elems += [_(" on "), dd.dtos(self.start_date)]
        return elems


class UpdateEvents(dd.MultipleRowAction):
    label = _('Update Events')
    icon_name = 'lightning'

    def run_on_row(self, obj, ar):
        return obj.update_reminders(ar)


class MoveEventNext(dd.MultipleRowAction):
    label = _('Move down')
    custom_handler = True
    icon_name = 'date_next'

    def get_action_permission(self, ar, obj, state):
        if obj.auto_type is None:
            return False
        return super(MoveEventNext, self).get_action_permission(
            ar, obj, state)

    def run_on_row(self, obj, ar):
        obj.owner.move_event_next(obj, ar)
        return 1


class EventGenerator(mixins.UserAuthored):

    class Meta:
        abstract = True

    do_update_events = UpdateEvents()

    @classmethod
    def get_registrable_fields(cls, site):
        for f in super(EventGenerator, cls).get_registrable_fields(site):
            yield f
        yield "user"

    def delete(self):
        self.get_existing_auto_events().delete()
        super(EventGenerator, self).delete()

    def update_cal_rset(self):
        raise NotImplementedError()

    def update_cal_from(self, ar):
        """
        """
        raise NotImplementedError()
        #~ return self.applies_from

    def update_cal_until(self):
        return None

    def update_cal_calendar(self):
        return None

    def get_events_language(self):
        if self.user is None:
            return settings.SITE.get_default_language()
        return self.user.language

    def update_cal_room(self, i):
        return None

    def update_cal_summary(self, i):
        raise NotImplementedError()
        #~ return _("Evaluation %d") % i

    def update_reminders(self, ar):
        return self.update_auto_events(ar)

    def update_auto_events(self, ar):
        if settings.SITE.loading_from_dump:
            #~ print "20111014 loading_from_dump"
            return 0
        qs = self.get_existing_auto_events()
        wanted = self.get_wanted_auto_events(ar)
        #~ logger.info("20131020 get_wanted_auto_events() returned %s",wanted)
        count = len(wanted)
        # current = 0

        #~ msg = dd.obj2str(self)
        #~ msg += ", qs=" + str([e.auto_type for e in qs])
        #~ msg += ", wanted=" + str([dbutils.dtos(e.start_date) for e in wanted.values()])
        #~ logger.info('20130528 ' + msg)

        for e in qs:
            ae = wanted.pop(e.auto_type, None)
            if ae is None:
                # there is an unwanted event in the database
                if not e.is_user_modified():
                    e.delete()
                #~ else:
                    #~ e.auto_type = None
                    #~ e.save()
            elif e.is_user_modified():
                if e.start_date != ae.start_date:
                    subsequent = ', '.join([str(x.auto_type)
                                           for x in wanted.values()])
                    delta = e.start_date - ae.start_date
                    ar.debug(
                        "%d has been moved from %s to %s: "
                        "move subsequent dates (%s) by %s"
                        % (
                            e.auto_type, ae.start_date,
                            e.start_date, subsequent, delta))
                    for se in wanted.values():
                        ov = se.start_date
                        se.start_date += delta
                        ar.debug("%d : %s -> %s" % (
                            se.auto_type, ov, se.start_date))
            else:
                self.compare_auto_event(e, ae)
        # create new Events for remaining wanted
        for ae in wanted.values():
            self.before_auto_event_save(ae)
            ae.save()
            ae.update_guests(ar)
        #~ logger.info("20130528 update_auto_events done")
        return count

    def compare_auto_event(self, obj, ae):
        original_state = dict(obj.__dict__)
        summary = force_unicode(ae.summary)
        if obj.summary != summary:
            obj.summary = summary
        if obj.user != ae.user:
            obj.user = ae.user
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
        if obj.room != ae.room:
            obj.room = ae.room
        self.before_auto_event_save(obj)
        if obj.__dict__ != original_state:
            obj.save()

    def setup_auto_event(self, obj):
        pass

    def before_auto_event_save(self, obj):
        pass

    def get_wanted_auto_events(self, ar):
        wanted = dict()
        event_type = self.update_cal_calendar()
        if event_type is None:
            ar.debug("No event_type")
            return wanted
        rset = self.update_cal_rset()
        #~ ar.info("20131020 rset %s",rset)
        #~ if rset and rset.every > 0 and rset.every_unit:
        if rset is None:
            ar.info("20131020 no rset")
            return wanted
        if not rset.every_unit:
            ar.info("20131020 no every_unit")
            return wanted
        date = self.update_cal_from(ar)
        if not date:
            ar.info("no start date")
            return wanted
        # ar.debug("20140310a %s", date)
        date = rset.find_start_date(date)
        # ar.debug("20140310b %s", date)
        if date is None:
            ar.info("No available weekday.")
            return wanted
        until = self.update_cal_until() \
            or settings.SITE.ignore_dates_after
        if until is None:
            raise Exception("ignore_dates_after may not be None")
        i = 0
        max_events = rset.max_events or \
            settings.SITE.site_config.max_auto_events
        Event = settings.SITE.modules.cal.Event
        ar.info("Generating events between %s and %s.", date, until)
        with translation.override(self.get_events_language()):
            while i < max_events:
                if date > until:
                    ar.info("Reached upper date limit %s", until)
                    break
                i += 1
                if settings.SITE.ignore_dates_before is None or \
                   date >= settings.SITE.ignore_dates_before:
                    we = Event(
                        auto_type=i,
                        user=self.user,
                        start_date=date,
                        summary=self.update_cal_summary(i),
                        room=self.update_cal_room(i),
                        owner=self,
                        event_type=event_type,
                        start_time=rset.start_time,
                        end_time=rset.end_time)
                    self.setup_auto_event(we)
                    date = self.resolve_conflicts(we, ar, rset, until)
                    if date is None:
                        return wanted
                    wanted[i] = we
                date = rset.get_next_suggested_date(ar, date)
                date = rset.find_start_date(date)
                if date is None:
                    ar.info("Could not find next date.")
                    break
        return wanted

    def move_event_next(self, we, ar):
        if we.owner is not self:
            raise Exception(
                "%s cannot move event controlled by %s" % (
                    self, we.owner))
        if we.state == EventStates.suggested:
            we.state = EventStates.draft
        rset = self.update_cal_rset()
        date = rset.get_next_alt_date(ar, we.start_date)
        if date is None:
            return
        until = self.update_cal_until() \
            or settings.SITE.ignore_dates_after
        we.start_date = date
        if self.resolve_conflicts(we, ar, rset, until) is None:
            return
        we.save()
        ar.set_response(refresh=True)
        ar.success()

    def resolve_conflicts(self, we, ar, rset, until):
        date = we.start_date
        # ar.debug("20140310 resolve_conflicts %s", we.start_date)
        while we.has_conflicting_events():
            qs = we.get_conflicting_events()
            # ar.debug("20140310 %s conflicts with %s. ", we,
            #          we.get_conflicting_events())
            date = rset.get_next_alt_date(ar, date)
            if date is None or date > until:
                ar.debug(
                    "Failed to get next date for %s (%s > %s).",
                    we, date, until)
                conflicts = [E.tostring(ar.obj2html(o)) for o in qs]
                msg = ', '.join(conflicts)
                ar.warning("%s conflicts with %s. ", we, msg)
                return None
        
            rset.move_event_to(we, date)
        return date

    def get_existing_auto_events(self):
        ot = ContentType.objects.get_for_model(self.__class__)
        return rt.modules.cal.Event.objects.filter(
            owner_type=ot, owner_id=self.pk,
            auto_type__isnull=False).order_by('auto_type')

    def suggest_cal_guests(self, event):
        return []


class RecurrenceSet(Started, Ended):
    class Meta:
        abstract = True
        verbose_name = _("Recurrence Set")
        verbose_name_plural = _("Recurrence Sets")

    #~ every_unit = DurationUnits.field(_("Repeat every (unit)"),
    every_unit = Recurrencies.field(
        _("Recurrency"),
        default=Recurrencies.monthly,
        blank=True)  # iCal:DURATION
    every = models.IntegerField(_("Repeat every"), default=0)

    monday = models.BooleanField(Weekdays.monday.text, default=False)
    tuesday = models.BooleanField(Weekdays.tuesday.text, default=False)
    wednesday = models.BooleanField(Weekdays.wednesday.text, default=False)
    thursday = models.BooleanField(Weekdays.thursday.text, default=False)
    friday = models.BooleanField(Weekdays.friday.text, default=False)
    saturday = models.BooleanField(Weekdays.saturday.text, default=False)
    sunday = models.BooleanField(Weekdays.sunday.text, default=False)

    max_events = models.PositiveIntegerField(
        _("Number of events"),
        blank=True, null=True)

    @classmethod
    def on_analyze(cls, lino):
        cls.WEEKDAY_FIELDS = dd.fields_list(
            cls, 'monday tuesday wednesday thursday friday saturday  sunday')
        super(RecurrenceSet, cls).on_analyze(lino)

    @classmethod
    def get_registrable_fields(cls, site):
        for f in super(RecurrenceSet, cls).get_registrable_fields(site):
            yield f
        for f in cls.WEEKDAY_FIELDS:
            yield f
        yield 'every'
        yield 'every_unit'
        yield 'max_events'
        #~ yield 'event_type'
        yield 'start_date'
        yield 'end_date'
        yield 'start_time'
        yield 'end_time'

    def save(self, *args, **kw):
        if self.every_unit == Recurrencies.per_weekday:
            self.every_unit = Recurrencies.weekly
        elif self.every_unit == Recurrencies.once:
            self.max_events = 1
            self.every = 0
        super(RecurrenceSet, self).save(*args, **kw)

    def disabled_fields(self, ar):
        rv = super(RecurrenceSet, self).disabled_fields(ar)
        if self.every_unit == Recurrencies.once:
            rv.add('max_events')
            rv.add('every')
        # if self.every_unit != Recurrencies.per_weekday:
            # rv |= self.WEEKDAY_FIELDS
        return rv

    @dd.displayfield(_("Description"))
    def what_text(self, ar):
        return unicode(self)

    @dd.displayfield(_("Times"))
    def times_text(self, ar):
        return "%s-%s" % (format_time(self.start_time),
                          format_time(self.end_time))

    @dd.displayfield(_("When"))
    def weekdays_text(self, ar):
        weekdays = []
        for wd in Weekdays.objects():
            if getattr(self, wd.name):
                weekdays.append(unicode(wd.text))
        weekdays = ', '.join(weekdays)
        if self.every == 1:
            return _("Every %s") % weekdays
        return _("Every %snd %s") % (self.every, weekdays)

    def move_event_to(self, ev, newdate):
        ev.start_date = newdate
        if self.end_date is None:
            ev.end_date = None
        else:
            duration = self.end_date - newdate
            ev.end_date = newdate + duration
            
    def get_next_alt_date(self, ar, date):
        return self.find_start_date(date + ONE_DAY)

    def get_next_suggested_date(self, ar, date):
        if self.every_unit == Recurrencies.once:
            ar.debug("get_next_suggested_date() once --> None.")
            return None
        if self.every_unit == Recurrencies.per_weekday:
            date = date + ONE_DAY
        else:
            date = self.every_unit.add_duration(date, self.every)
        return self.find_start_date(date)

    def find_start_date(self, date):
        if date is not None:
            for i in range(7):
                if self.is_available_on(date):
                    return date
                date += ONE_DAY
        return None

    def is_available_on(self, date):
        wd = date.isoweekday()  # Monday:1, Tuesday:2 ... Sunday:7
        wd = Weekdays.get_by_value(str(wd))
        rv = getattr(self, wd.name)
        #~ logger.info('20130529 is_available_on(%s) -> %s -> %s',date,wd,rv)
        return rv

dd.update_field(RecurrenceSet, 'start_date', default=settings.SITE.today)


class Reservation(RecurrenceSet, EventGenerator, mixins.Registrable):

    class Meta:
        abstract = True

    room = dd.ForeignKey('cal.Room', blank=True, null=True)
    max_date = models.DateField(
        blank=True, null=True,
        verbose_name=_("Generate events until"))

    def update_cal_until(self):
        return self.max_date

    def update_cal_rset(self):
        if self.room:
            return self

    def update_cal_room(self, i):
        return self.room

    @classmethod
    def get_registrable_fields(cls, site):
        for f in super(Reservation, cls).get_registrable_fields(site):
            yield f
        yield 'room'
        yield 'max_date'

    def after_state_change(self, ar, old, target_state):
        super(Reservation, self).after_state_change(ar, old, target_state)
        self.update_reminders(ar)

    #~ def after_ui_save(self,ar):
        #~ super(Reservation,self).after_ui_save(ar)
        #~ if self.state.editable:
            #~ self.update_reminders(ar)
