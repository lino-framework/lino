# -*- coding: UTF-8 -*-
# Copyright 2011-2014 Luc Saffre
# This file is part of the Lino project.
# Lino is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
# Lino is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
# You should have received a copy of the GNU Lesser General Public License
# along with Lino; if not, see <http://www.gnu.org/licenses/>.

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
from lino import dd
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
            self.start_date = datetime.date.today()
        super(Started, self).save(*args, **kw)

    def set_datetime(self, name, value):
        """
        Given a datetime `value`, update the two corresponding
        fields `FOO_date` and `FOO_time`
        (where FOO is specified in `name` which must be
        either "start" or "end").
        """
        #~ logger.info("20120119 set_datetime(%r)",value)
        setattr(self, name + '_date', value.date())
        t = value.time()
        if not t:
            t = None
        setattr(self, name + '_time', t)

    def get_datetime(self, name, altname=None):
        """
        Return a `datetime` value from the two corresponding
        date and time fields.
        `name` can be 'start' or 'end'.
        """
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
    description = dd.RichTextField(_("Description"), blank=True, format='html')

    def __unicode__(self):
        return self._meta.verbose_name + " #" + str(self.pk)

    def summary_row(self, ar, **kw):
        elems = list(super(StartedSummaryDescription, self)
                     .summary_row(ar, **kw))

        if self.summary:
            elems.append(': %s' % self.summary)
        elems += [_(" on "), dd.dtos(self.start_date)]
        return elems


class MultipleRowAction(actions.Action):

    callable_from = (actions.GridEdit, actions.ShowDetailAction)

    def run_on_row(self, obj, ar):
        raise NotImplemented()

    def run_from_ui(self, ar, **kw):
        ar.success(**kw)
        n = 0
        for obj in ar.selected_rows:
            if not ar.response.get('success'):
                ar.info("Aborting remaining rows")
                break
            ar.info("%s for %s...", self.label, unicode(obj))
            n += self.run_on_row(obj, ar)
            ar.response.update(refresh_all=True)

        msg = _("%d event(s) have been updated.") % n
        ar.info(msg)
        #~ ar.success(msg,**kw)


class UpdateEvents(MultipleRowAction):
    label = _('Update Events')
    show_in_row_actions = True
    icon_name = 'lightning'

    def run_on_row(self, obj, ar):
        return obj.update_reminders(ar)


class MoveEventNext(MultipleRowAction):
    label = _('Move down')
    show_in_row_actions = True
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

    """Base class for things that generate a suite of events.

    The generated events are "controlled" by their generator (their
    `owner` field points to the generator) and have a non-empty
    `auto_type` field.

    Examples:

    - :class:`Reservation` (subclassed by
      :class:`lino.modlib.courses.Course`)

    - :class:`lino_welfare.modlib.isip.Contract` and
      :class:`lino_welfare.modlib.jobs.Contract` are event generators
      with a separate

    """

    class Meta:
        abstract = True

    do_update_events = UpdateEvents()

    @classmethod
    def get_registrable_fields(cls, site):
        for f in super(EventGenerator, cls).get_registrable_fields(site):
            yield f
        yield "user"

    def delete(self):
        """
        Delete all events generated by me before deleting myself.
        """
        self.get_existing_auto_events().delete()
        super(EventGenerator, self).delete()

    def update_cal_rset(self):
        raise NotImplementedError()

    def update_cal_from(self, ar):
        """
        Return the date of the first Event to be generated.
        Return None if no Events should be generated.
        """
        raise NotImplementedError()
        #~ return self.applies_from

    def update_cal_until(self):
        """Return the limit date until which to generate events.  None means
        "no limit" (which de facto becomes `SiteConfig.farest_future`)

        """
        return None

    def update_cal_calendar(self):
        """Return the event_type for the events to generate.  Returning None
        means: don't generate any events.

        """
        return None

    def get_events_language(self):
        """Return the language to activate while events are being generated.

        """
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
        """Generate automatic calendar events owned by this contract.

        If one event has been manually rescheduled, all following
        events adapt to the new rythm.

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

    def before_auto_event_save(self, obj):
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

    def get_wanted_auto_events(self, ar):
        """
        Return a dict which maps sequence number
        to AttrDict instances which hold the wanted event.
        """
        wanted = dict()
        event_type = self.update_cal_calendar()
        if event_type is None:
            ar.debug("No event_type")
            return wanted
        rset = self.update_cal_rset()
        #~ ar.info("20131020 rset %s",rset)
        #~ if rset and rset.every > 0 and rset.every_unit:
        if rset is not None:
            if rset.every_unit:
                date = self.update_cal_from(ar)
                if not date:
                    ar.info("no start date")
                    return wanted
                date = rset.find_start_date(date)
                if date is None:
                    ar.debug("No available weekday.")
    
            else:
                ar.info("20131020 no every_unit")
                return wanted
        else:
            ar.info("20131020 no rset")
            return wanted
        until = self.update_cal_until() \
            or settings.SITE.site_config.farest_future
        i = 0
        max_events = rset.max_events or \
            settings.SITE.site_config.max_auto_events
        Event = settings.SITE.modules.cal.Event
        with translation.override(self.get_events_language()):
            while i < max_events:
                if date > until:
                    ar.info("20131020 reached maximum date %s", until)
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
                    date = self.resolve_conflicts(we, ar, rset, until)
                    if date is None:
                        return wanted

                    wanted[i] = we
                date = rset.get_next_date(ar, date)
                if date is None:
                    ar.info("Could not find next date.")
                    break
        return wanted

    def move_event_next(self, we, ar):
        """Move the specified event to the next date in this series.
        """
        if we.owner is not self:
            raise Exception(
                "%s cannot move event controlled by %s" % (
                    self, we.owner))
        if we.state == EventStates.suggested:
            we.state = EventStates.draft
        rset = self.update_cal_rset()
        date = rset.get_next_date(ar, we.start_date)
        if date is None:
            ar.error("Could not find next date.")
            return
        until = self.update_cal_until() \
            or settings.SITE.site_config.farest_future
        we.start_date = date
        if self.resolve_conflicts(we, ar, rset, until) is None:
            return
        we.save()
        ar.response.update(refresh=True)
        ar.success()

    def resolve_conflicts(self, we, ar, rset, until):
        """Check whether given event conflicts with other events and move it
        to a new date if necessary. Returns the new date, or None if
        no alternative could be found.

        """
        date = we.start_date
        while we.has_conflicting_events():
            # ar.debug("%s conflicts with %s. ", we,
            #          we.get_conflicting_events())
            date = rset.get_next_date(ar, date)
            if date is None or date > until:
                ar.debug("Failed to get next date for %s.", we)
                conflicts = [E.tostring(ar.obj2html(o))
                             for o in we.get_conflicting_events()]
                msg = ', '.join(conflicts)
                ar.warning("%s conflicts with %s. ", we, msg)
                return None
        
            rset.move_event_to(we, date)
        return date

    def get_existing_auto_events(self):
        ot = ContentType.objects.get_for_model(self.__class__)
        return settings.SITE.modules.cal.Event.objects.filter(
            owner_type=ot, owner_id=self.pk,
            auto_type__isnull=False).order_by('auto_type')


class RecurrenceSet(Started, Ended):
    """Abstract base for models that express a set of recurrency
    rules. This might be combined with :class:`EventGenerator` into a
    same model as done by :class:`Reservation`.

    Thanks to http://www.kanzaki.com/docs/ical/rdate.html

    """
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
        cls.WEEKDAY_FIELDS = dd.fields_list(cls,
            '''monday tuesday wednesday
            thursday friday saturday  sunday    
            ''')
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

    def disabled_fields(self, ar):
        rv = super(RecurrenceSet, self).disabled_fields(ar)
        if self.every_unit != Recurrencies.per_weekday:
            #~ return settings.SITE.TASK_AUTO_FIELDS
            rv |= self.WEEKDAY_FIELDS
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
        """Move given event to a new date.
        Also change `end_date` if necessary.
        """
        ev.start_date = newdate
        if self.end_date is None:
            ev.end_date = None
        else:
            duration = self.end_date - newdate
            ev.end_date = newdate + duration
            
    def get_next_date(self, ar, date):
        """Find the next date after the given date, without worrying about
        conflicts.

        """
        if self.every_unit == Recurrencies.once:
            ar.debug("get_next_date() once --> None.")
            return None
        if self.every_unit == Recurrencies.per_weekday:
            date = self.find_start_date(date + ONE_DAY)
            if date is None:
                ar.debug("get_next_date() failed to find available weekday.")
            return date
        return self.every_unit.add_duration(date, self.every)

    def find_start_date(self, date):
        """Find the first available date for the given date (possibly
        including that date)

        """
        if self.every_unit != Recurrencies.per_weekday:
            return date
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

dd.update_field(RecurrenceSet, 'start_date', default=datetime.date.today)


class Reservation(RecurrenceSet, EventGenerator, dd.Registrable):

    "Base class for rooms.Booking and courses.Course"

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
