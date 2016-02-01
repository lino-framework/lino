# -*- coding: UTF-8 -*-
# Copyright 2011-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""
Model mixins for `lino.modlib.cal`.

.. autosummary::


"""

from __future__ import unicode_literals

import datetime
try:
    import pytz
except ImportError:
    pytz = None

from django.conf import settings
from django.db import models
from django.utils import translation
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import is_aware
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import force_unicode

from lino import mixins
from lino.api import dd, rt
from lino.utils import ONE_DAY
from lino.utils.quantities import Duration
from lino.utils.xmlgen.html import E

from .choicelists import Recurrencies, Weekdays, AccessClasses

from .workflows import EventStates
from lino.modlib.office.roles import OfficeStaff

from lino.modlib.users.mixins import UserAuthored
from lino.modlib.gfks.mixins import Controllable


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
    """Mixin for models with two fields :attr:`start_date` and
    :attr:`start_time`

    .. attribute:: start_date
    .. attribute:: start_time

    """
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

    def get_timezone(self):
        """May get overridden to return the author's timezone."""
        return settings.TIME_ZONE

    def set_datetime(self, name, value):
        """
        Given a datetime `value`, update the two corresponding fields
        `FOO_date` and `FOO_time` (where FOO is specified in `name` which
        must be either "start" or "end").
        """
        if settings.USE_TZ and is_aware(value):
            tz = pytz.timezone(self.get_timezone())
            # dd.logger.info("20151128 set_datetime(%r, %r)", value, tz)
            value = value.astimezone(tz)
            # value = tz.localize(value)
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
            dt = datetime.datetime.combine(d, t)
        else:
            dt = datetime.datetime(d.year, d.month, d.day)
        if settings.USE_TZ:
            tz = pytz.timezone(self.get_timezone())
            # dd.logger.info("20151128 get_datetime() %r %r", dt, tz)
            dt = tz.localize(dt)
        return dt


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


class StartedEnded(Started, Ended):
    """Model mixin for things that have both a start_time and an end_time.

    """
    class Meta:
        abstract = True

    def save(self, *args, **kw):
        """
        Fills default value end_date
        """
        if self.end_time and not self.end_date:
            self.end_date = self.start_date
        super(Ended, self).save(*args, **kw)

    def get_duration(self):
        st = self.get_datetime('start')
        et = self.get_datetime('end')
        if st is None or et is None:
            return None
        if et < st:
            return None  # negative duration not supported
        # print 20151127, repr(et), repr(st)
        return Duration(et - st)

    @dd.virtualfield(dd.QuantityField(_("Duration")))
    def duration(self, ar):
        return self.get_duration()

    # @dd.virtualfield(models.TimeField(_("Duration")))
    # def duration(self, ar):
    #     return datetime.time(self.get_duration())


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


class UpdateEvents(dd.MultipleRowAction):
    label = _('Update Events')
    icon_name = 'lightning'

    def run_on_row(self, obj, ar):
        return obj.update_reminders(ar)


class EventGenerator(UserAuthored):
    """
    Base class for things that generate a suite of events.

    The generated events are "controlled" by their generator (their
    `owner` field points to the generator) and have a non-empty
    `auto_type` field.

    Examples:

    - :class:`Reservation` (subclassed by
      :class:`lino.modlib.courses.Course`)

    - :class:`lino_welfare.modlib.isip.models.Contract` and
      :class:`lino_welfare.modlib.jobs.models.Contract` are event generators
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
        """Delete all events generated by me before deleting myself."""

        self.get_existing_auto_events().delete()
        super(EventGenerator, self).delete()

    def update_cal_rset(self):
        raise NotImplementedError()

    def update_cal_from(self, ar):
        """Return the date of the first Event to be generated.
        Return None if no Events should be generated.

        """
        raise NotImplementedError()
        #~ return self.applies_from

    def update_cal_until(self):
        """Return the limit date until which to generate events.  None means
        "no limit" (which de facto becomes
        :attr:`lino.modlib.cal.Plugin.ignore_dates_after`)

        """

        return None

    def update_cal_calendar(self):
        """Return the event_type for the events to generate.  Returning None
    means: don't generate any events.

        """
        return None

    def get_events_language(self):
        """Return the language to activate while events are being
        generated.

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
        """
        Generate automatic calendar events owned by this contract.

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
            ae.after_ui_create(ar)
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
        """
        Called for automatically generated events after their automatic
        fields have been set and before the event is saved.
        This allows for application-specific "additional-automatic" fields.
        E.g. the room field in `lino.modlib.courses`.

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
        """Return a dict which maps sequence number to AttrDict instances
        which hold the wanted event.

        """
        wanted = dict()
        event_type = self.update_cal_calendar()
        if event_type is None:
            ar.info("No event_type")
            return wanted
        rset = self.update_cal_rset()
        #~ ar.info("20131020 rset %s",rset)
        #~ if rset and rset.every > 0 and rset.every_unit:
        if rset is None:
            ar.info("No recurrency set")
            return wanted
        if not rset.every_unit:
            ar.info("No every_unit")
            return wanted
        date = self.update_cal_from(ar)
        if not date:
            ar.info("No start date")
            return wanted
        # ar.debug("20140310a %s", date)
        date = rset.find_start_date(date)
        # ar.debug("20140310b %s", date)
        if date is None:
            ar.info("No available start date.")
            return wanted
        until = self.update_cal_until() \
            or dd.plugins.cal.ignore_dates_after
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
                if dd.plugins.cal.ignore_dates_before is None or \
                   date >= dd.plugins.cal.ignore_dates_before:
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
        """Move the specified event to the next date in this series."""

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
            or dd.plugins.cal.ignore_dates_after
        we.start_date = date
        if self.resolve_conflicts(we, ar, rset, until) is None:
            return
        we.save()
        ar.set_response(refresh=True)
        ar.success()

    def care_about_conflicts(self, we):
        """Whether this event generator should try to resolve cnoflicts (in
        :meth:`resolve_conflicts`)

        """
        return True

    def resolve_conflicts(self, we, ar, rset, until):
        """
        Check whether given event conflicts with other events and move it
        to a new date if necessary. Returns the new date, or None if
        no alternative could be found.
        """
    
        date = we.start_date
        if not self.care_about_conflicts(we):
            return date
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
        """Yield or return a list of (unsaved) :class:`Guest
        <lino.modlib.cal.models.Guest>` objects representing the
        participants to invite to every the given event. Called on
        every event generated by this generator.

        """

        return []


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
        default=Recurrencies.monthly.as_callable,
        blank=True)  # iCal:DURATION
    every = models.IntegerField(_("Repeat every"), default=1)

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
    def on_analyze(cls, site):
        cls.WEEKDAY_FIELDS = dd.fields_list(
            cls, 'monday tuesday wednesday thursday friday saturday  sunday')
        super(RecurrenceSet, cls).on_analyze(site)

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
        """A textual formulation of "when" the recurrence occurs. This is a
        virtual field labelled "When".

        """
        weekdays = []
        for wd in Weekdays.objects():
            if getattr(self, wd.name):
                weekdays.append(unicode(wd.text))
        weekdays = ', '.join(weekdays)
        if self.every == 1:
            return _("Every %s") % weekdays
        return _("Every %snd %s") % (self.every, weekdays)

    def move_event_to(self, ev, newdate):
        """Move given event to a new date.  Also change `end_date` if
        necessary.

        """
        ev.start_date = newdate
        if self.end_date is None:
            ev.end_date = None
        else:
            duration = self.end_date - newdate
            ev.end_date = newdate + duration
            
    def get_next_alt_date(self, ar, date):
        """Currently always returns date + 1.

        """
        return self.find_start_date(date + ONE_DAY)

    def get_next_suggested_date(self, ar, date):
        """Find the next date after the given date, without worrying about
        conflicts.

        """
        if self.every_unit == Recurrencies.once:
            ar.debug("get_next_suggested_date() once --> None.")
            return None
        if self.every_unit == Recurrencies.per_weekday:
            date = date + ONE_DAY
        else:
            date = self.every_unit.add_duration(date, self.every)
        return self.find_start_date(date)

    def find_start_date(self, date):
        """Find the first available date for the given date (possibly
        including that date)

        """

        if date is not None:
            for i in range(7):
                if self.is_available_on(date):
                    return date
                date += ONE_DAY
        return None

    def is_available_on(self, date):
        """Whether the given date `date` is allowed according to the weekdays
        of this recurrence set.

        """
        if self.monday or self.tuesday or self.wednesday or self.thursday \
           or self.friday or self.saturday or self.sunday:
            wd = date.isoweekday()  # Monday:1, Tuesday:2 ... Sunday:7
            wd = Weekdays.get_by_value(str(wd))
            rv = getattr(self, wd.name)
            #~ logger.info('20130529 is_available_on(%s) -> %s -> %s',date,wd,rv)
            return rv
        return True

dd.update_field(RecurrenceSet, 'start_date', default=dd.today)


class Reservation(RecurrenceSet, EventGenerator, mixins.Registrable):
    """Base class for :class:`lino.modlib.rooms.models.Booking` and
    :class:`lino.modlib.courses.models.Course`.

    Inherits from both :class:`EventGenerator` and :class:`RecurrenceSet`.

    .. attribute:: room
    .. attribute:: max_date

    """

    class Meta:
        abstract = True

    room = dd.ForeignKey('cal.Room', blank=True, null=True)
    max_date = models.DateField(
        blank=True, null=True,
        verbose_name=_("Generate events until"))

    def update_cal_until(self):
        return self.max_date

    def update_cal_rset(self):
        """Return the *reccurrency set* to be used when generating events for
        this reservation.

        """
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


class Component(StartedSummaryDescription,
                mixins.ProjectRelated,
                UserAuthored,
                Controllable,
                mixins.CreatedModified):

    """
    Abstract base class for :class:`Event` and :class:`Task`.

    """
    workflow_state_field = 'state'
    manager_roles_required = dd.login_required(OfficeStaff)

    class Meta:
        abstract = True

    access_class = AccessClasses.field(blank=True, help_text=_("""\
Whether this is private, public or between."""))  # iCal:CLASS
    sequence = models.IntegerField(_("Revision"), default=0)
    auto_type = models.IntegerField(null=True, blank=True, editable=False)

    def save(self, *args, **kw):
        if self.user is not None and self.access_class is None:
            self.access_class = self.user.access_class
        super(Component, self).save(*args, **kw)

    def on_duplicate(self, ar, master):
        self.auto_type = None

    def disabled_fields(self, ar):
        rv = super(Component, self).disabled_fields(ar)
        if self.auto_type:
            rv |= self.DISABLED_AUTO_FIELDS
        return rv

    def get_uid(self):
        """
        This is going to be used when sending
        locally created components to a remote calendar.
        """
        if not settings.SITE.uid:
            raise Exception(
                'Cannot create local calendar components because settings.SITE.uid is empty.')
        return "%s@%s" % (self.pk, settings.SITE.uid)

    #~ def on_user_change(self,request):
        #~ raise NotImplementedError
        #~ self.user_modified = True
    def summary_row(self, ar, **kw):
        #~ logger.info("20120217 Component.summary_row() %s", self)
        #~ if self.owner and not self.auto_type:
        html = [ar.obj2html(self)]
        if self.start_time:
            html += [_(" at "),
                     dd.strftime(self.start_time)]
        if self.state:
            html += [' [%s]' % force_unicode(self.state)]
        if self.summary:
            html += [': %s' % force_unicode(self.summary)]
            #~ html += ui.href_to(self,force_unicode(self.summary))
        #~ html += _(" on ") + dbutils.dtos(self.start_date)
        #~ if self.owner and not self.owner.__class__.__name__ in ('Person','Company'):
            #~ html += " (%s)" % reports.summary_row(self.owner,ui,rr)
        if self.project is not None:
            html.append(" (%s)" % self.project.summary_row(ar, **kw))
            #~ print 20120217, self.project.__class__, self
            #~ html += " (%s)" % self.project.summary_row(ui)
        return html
        #~ return super(Event,self).summary_row(ui,rr,**kw)

#~ Component.owner.verbose_name = _("Automatically created by")

