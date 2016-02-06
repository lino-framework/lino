# -*- coding: UTF-8 -*-
# Copyright 2011-2016 Luc Saffre
# License: BSD (see file COPYING for details)

"""Database models for `lino.modlib.cal`.

"""

from __future__ import unicode_literals

import logging
logger = logging.getLogger(__name__)

import datetime

from django.db import models
from django.db.models import Q
from django.conf import settings
from django.core.validators import MaxValueValidator
from django.core.validators import MinValueValidator
from django.utils import timezone

from lino import mixins
from lino.api import dd, rt, _, pgettext

from .choicelists import (
    DurationUnits, Recurrencies, Weekdays, AccessClasses)
from .utils import setkw, dt2kw, when_text

from lino.modlib.users.mixins import UserAuthored
from lino.modlib.postings.mixins import Postable
from lino.modlib.outbox.mixins import MailableType, Mailable
from lino.modlib.office.roles import OfficeStaff
from .workflows import (TaskStates, EventStates, GuestStates)

from .workflows import take
from .mixins import Component
from .mixins import EventGenerator, RecurrenceSet, Reservation
from .mixins import Ended
from .mixins import MoveEventNext, UpdateEvents
from .ui import *

DEMO_START_YEAR = 2013


class CalendarType(object):

    def validate_calendar(self, cal):
        pass


class LocalCalendar(CalendarType):
    label = "Local Calendar"


class GoogleCalendar(CalendarType):
    label = "Google Calendar"

    def validate_calendar(self, cal):
        if not cal.url_template:
            cal.url_template = \
                "https://%(username)s:%(password)s@www.google.com/calendar/dav/%(username)s/"

CALENDAR_CHOICES = []
CALENDAR_DICT = {}


def register_calendartype(name, instance):
    CALENDAR_DICT[name] = instance
    CALENDAR_CHOICES.append((name, instance.label))

register_calendartype('local', LocalCalendar())
register_calendartype('google', GoogleCalendar())


class RemoteCalendar(mixins.Sequenced):

    """
    Remote calendars will be synchronized by
    :mod:`lino.modlib.cal.management.commands.watch_calendars`,
    and local modifications will be sent back to the remote calendar.
    """
    class Meta:
        app_label = 'cal'
        abstract = dd.is_abstract_model(__name__, 'RemoteCalendar')
        verbose_name = _("Remote Calendar")
        verbose_name_plural = _("Remote Calendars")
        ordering = ['seqno']

    type = models.CharField(_("Type"), max_length=20,
                            default='local',
                            choices=CALENDAR_CHOICES)
    url_template = models.CharField(_("URL template"),
                                    max_length=200, blank=True)  # ,null=True)
    username = models.CharField(_("Username"),
                                max_length=200, blank=True)  # ,null=True)
    password = dd.PasswordField(_("Password"),
                                max_length=200, blank=True)  # ,null=True)
    readonly = models.BooleanField(_("read-only"), default=False)

    def get_url(self):
        if self.url_template:
            return self.url_template % dict(
                username=self.username,
                password=self.password)
        return ''

    def save(self, *args, **kw):
        ct = CALENDAR_DICT.get(self.type)
        ct.validate_calendar(self)
        super(RemoteCalendar, self).save(*args, **kw)


class Room(mixins.BabelNamed):
    """A location where calendar events can happen.  For a given Room you
    can see the :class:`EventsByRoom` that happened (or will happen)
    there.  A Room is BabelNamed (has a multilingual name).

    """
    class Meta:
        app_label = 'cal'
        abstract = dd.is_abstract_model(__name__, 'Room')
        verbose_name = _("Room")
        verbose_name_plural = _("Rooms")


class Priority(mixins.BabelNamed):

    "The priority of a Task or Event."
    class Meta:
        app_label = 'cal'
        verbose_name = _("Priority")
        verbose_name_plural = _('Priorities')
    ref = models.CharField(max_length=1)


class EventType(mixins.BabelNamed, mixins.Sequenced, MailableType):
    """The possible value of the :attr:`Event.type` field.
    Example content:

    .. lino2rst::

       rt.show(cal.EventTypes, limit=5)

    .. attribute:: is_appointment

        Whether events of this type should be considered
        "appointments" (i.e. whose time and place have been agreed
        upon with other users or external parties).

        The table (:class:`EventsByDay` and
        :class:`MyEvents`) show only events whose type has the
        `is_appointment` field checked.

    """
    templates_group = 'cal/Event'

    class Meta:
        app_label = 'cal'
        abstract = dd.is_abstract_model(__name__, 'EventType')
        verbose_name = _("Calendar Event Type")
        verbose_name_plural = _("Calendar Event Types")
        ordering = ['seqno']

    description = dd.RichTextField(
        _("Description"), blank=True, format='html')
    is_appointment = models.BooleanField(
        _("Event is an appointment"), default=True)
    all_rooms = models.BooleanField(_("Locks all rooms"), default=False)
    locks_user = models.BooleanField(
        _("Locks the user"),
        help_text=_(
            "Whether events of this type make the user unavailable "
            "for other locking events at the same time."),
        default=False)

    start_date = models.DateField(
        verbose_name=_("Start date"),
        blank=True, null=True)
    event_label = dd.BabelCharField(
        _("Event label"),
        max_length=200, blank=True,
        help_text=_("Default text for summary of new events."))
    # , default=_("Calendar entry"))
    # default values for a Babelfield don't work as expected

    max_conflicting = models.PositiveIntegerField(
        _("Simultaneous events"),
        help_text=_("How many conflicting events should be tolerated."),
        default=1)

    def __unicode__(self):
        # when selecting an Event.event_type it is more natural to
        # have the event_label. It seems that the current `name` field
        # is actually never used.
        return settings.SITE.babelattr(self, 'event_label') \
            or settings.SITE.babelattr(self, 'name')


class GuestRole(mixins.BabelNamed):
    templates_group = 'cal/Guest'

    class Meta:
        app_label = 'cal'
        verbose_name = _("Guest Role")
        verbose_name_plural = _("Guest Roles")


def default_color():
    d = Calendar.objects.all().aggregate(models.Max('color'))
    n = d['color__max'] or 0
    return n + 1


class Calendar(mixins.BabelNamed):

    COLOR_CHOICES = [i + 1 for i in range(32)]

    class Meta:
        app_label = 'cal'
        abstract = dd.is_abstract_model(__name__, 'Calendar')
        verbose_name = _("Calendar")
        verbose_name_plural = _("Calendars")

    description = dd.RichTextField(_("Description"), blank=True, format='html')

    color = models.IntegerField(
        _("color"), default=default_color,
        validators=[MinValueValidator(1), MaxValueValidator(32)]
    )
        #~ choices=COLOR_CHOICES)


class Subscription(UserAuthored):

    """
    A Suscription is when a User subscribes to a Calendar.
    It corresponds to what the extensible CalendarPanel calls "Calendars"
    
    :user: points to the author (recipient) of this subscription
    :other_user:
    
    """

    class Meta:
        app_label = 'cal'
        abstract = dd.is_abstract_model(__name__, 'Subscription')
        verbose_name = _("Subscription")
        verbose_name_plural = _("Subscriptions")
        unique_together = ['user', 'calendar']

    manager_roles_required = dd.login_required(OfficeStaff)

    calendar = dd.ForeignKey(
        'cal.Calendar', help_text=_("The calendar you want to subscribe to."))

    is_hidden = models.BooleanField(
        _("hidden"), default=False,
        help_text=_("""Whether this subscription should "
        "initially be displayed as a hidden calendar."""))


class Task(Component):
    """A Task is when a user plans to to something
    (and optionally wants to get reminded about it).

    .. attribute:: state
     
        The state of this Task. one of :class:`TaskStates`


    """
    class Meta:
        app_label = 'cal'
        verbose_name = _("Task")
        verbose_name_plural = _("Tasks")
        abstract = dd.is_abstract_model(__name__, 'Task')

    due_date = models.DateField(
        blank=True, null=True,
        verbose_name=_("Due date"))
    due_time = models.TimeField(
        blank=True, null=True,
        verbose_name=_("Due time"))
    # ~ done = models.BooleanField(_("Done"),default=False) # iCal:COMPLETED
    # iCal:PERCENT
    percent = models.IntegerField(_("Duration value"), null=True, blank=True)
    state = TaskStates.field(default=TaskStates.todo.as_callable)  # iCal:STATUS

    def before_ui_save(self, ar, **kw):
        if self.state == TaskStates.todo:
            self.state = TaskStates.started
        return super(Task, self).before_ui_save(ar, **kw)

    #~ def on_user_change(self,request):
        #~ if not self.state:
            #~ self.state = TaskState.todo
        #~ self.user_modified = True

    def is_user_modified(self):
        return self.state != TaskStates.todo

    @classmethod
    def on_analyze(cls, lino):
        #~ lino.TASK_AUTO_FIELDS = dd.fields_list(cls,
        cls.DISABLED_AUTO_FIELDS = dd.fields_list(
            cls, """start_date start_time summary""")
        super(Task, cls).on_analyze(lino)

    #~ def __unicode__(self):
        # ~ return "#" + str(self.pk)


class RecurrentEvent(mixins.BabelNamed, RecurrenceSet, EventGenerator):
    """A rule designed to generate a series of recurrent events.
    
    .. attribute:: name

        See :attr:`lino.utils.mldbc.mixins.BabelNamed.name`.
    
    .. attribute:: every_unit

        Inherited from :attr:`RecurrentSet.every_unit
        <lino.modlib.cal.models.RecurrentSet.every_unit>`

    .. attribute:: event_type



    .. attribute:: description

    """
    class Meta:
        app_label = 'cal'
        verbose_name = _("Recurrent event rule")
        verbose_name_plural = _("Recurrent event rules")

    event_type = models.ForeignKey('cal.EventType', blank=True, null=True)
    description = dd.RichTextField(
        _("Description"), blank=True, format='html')

    def before_auto_event_save(self, obj):
        if self.end_date and self.end_date != self.start_date:
            duration = self.end_date - self.start_date
            obj.end_date = obj.start_date + duration
        super(RecurrentEvent, self).before_auto_event_save(obj)

    #~ def on_create(self,ar):
        #~ super(RecurrentEvent,self).on_create(ar)
        #~ self.event_type = settings.SITE.site_config.holiday_event_type

    #~ def __unicode__(self):
        #~ return self.summary

    def update_cal_rset(self):
        return self

    def update_cal_from(self, ar):
        return self.start_date

    def update_cal_calendar(self):
        return self.event_type

    def update_cal_summary(self, i):
        return unicode(self)

    def care_about_conflicts(self, we):
        """Recurrent events don't care about conflicts. A holiday won't move
        just because some other event has been created before on that date.

        """
        return False

dd.update_field(
    RecurrentEvent, 'every_unit',
    default=Recurrencies.yearly.as_callable, blank=False, null=False)


class UpdateGuests(dd.MultipleRowAction):
    """Decide whether it is time to add Guest instances for this event,
    and if yes, call :meth:`suggest_guests` to instantiate them.

    - No guests must be added when loading from dump
    - The Event must be in a state which allows editing the guests
    - If there are already at least one guest, no guests will be added

    """

    label = _('Update Guests')
    icon_name = 'lightning'

    def run_on_row(self, obj, ar):
        if settings.SITE.loading_from_dump:
            return 0
        if not obj.state.edit_guests:
            ar.info("not state.edit_guests")
            return 0
        existing = set([g.partner.pk for g in obj.guest_set.all()])
        n = 0
        for g in obj.suggest_guests():
            if g.partner.pk not in existing:
                g.save()
                n += 1
        return n


class ExtAllDayField(dd.VirtualField):

    """
    An editable virtual field needed for
    communication with the Ext.ensible CalendarPanel
    because we consider the "all day" checkbox
    equivalent to "empty start and end time fields".
    """

    editable = True

    def __init__(self, *args, **kw):
        dd.VirtualField.__init__(self, models.BooleanField(*args, **kw), None)

    def set_value_in_object(self, request, obj, value):
        if value:
            obj.end_time = None
            obj.start_time = None
        else:
            if not obj.start_time:
                obj.start_time = datetime.time(9, 0, 0)
            if not obj.end_time:
                pass
                # obj.end_time = datetime.time(10, 0, 0)
        #~ obj.save()

    def value_from_object(self, obj, ar):
        #~ logger.info("20120118 value_from_object() %s",dd.obj2str(obj))
        return (obj.start_time is None)


class Event(Component, Ended,
            mixins.TypedPrintable,
            Mailable, Postable):
    """A calendar event is a lapse of time to be visualized in a calendar.

    .. attribute:: user

         The responsible user.

    .. attribute:: assigned_to

        This field is usually empty.  Setting it to another user means "I
        am not fully responsible for this event".  This will cause the
        other user to see this event in his :class:`MyAssignedEvents`
        table.

        This field is cleared when somebody calls :class:`TakeEvent` on
        the event.

    .. attribute:: event_type

         The type of this event. Every calendar event should have this
         field pointing to a given :class:`EventType`, which holds
         extended configurable information about this event.

    .. attribute:: linked_date

         Shows the date and time of the event with a link that opens
         all events on that day (cal.EventsByDay)

    """
    class Meta:
        app_label = 'cal'
        abstract = dd.is_abstract_model(__name__, 'Event')
        #~ abstract = True
        verbose_name = pgettext("cal", "Event")
        verbose_name_plural = pgettext("cal", "Events")

    update_guests = UpdateGuests()

    event_type = models.ForeignKey('cal.EventType', blank=True, null=True)

    transparent = models.BooleanField(
        _("Transparent"), default=False, help_text=_("""\
Indicates that this Event shouldn't prevent other Events at the same time."""))
    room = dd.ForeignKey('cal.Room', null=True, blank=True)  # iCal:LOCATION
    priority = models.ForeignKey(Priority, null=True, blank=True)
    state = EventStates.field(
        default=EventStates.suggested.as_callable)  # iCal:STATUS
    all_day = ExtAllDayField(_("all day"))

    assigned_to = dd.ForeignKey(
        settings.SITE.user_model,
        verbose_name=_("Assigned to"),
        related_name="cal_events_assigned",
        blank=True, null=True)

    move_next = MoveEventNext()

    def strftime(self):
        if not self.start_date:
            return ''
        d = self.start_date.strftime(settings.SITE.date_format_strftime)
        if self.start_time:
            t = self.start_time.strftime(
                settings.SITE.time_format_strftime)
            return "%s %s" % (d, t)
        else:
            return d

    def __unicode__(self):
        if self.pk:
            s = self._meta.verbose_name + " #" + str(self.pk)
        else:
            s = _("Unsaved %s") % self._meta.verbose_name
        if self.summary:
            s += " " + self.summary
        when = self.strftime()
        if when:
            s += " (%s)" % when
        return s

    def has_conflicting_events(self):
        qs = self.get_conflicting_events()
        if qs is None:
            return False
        if self.event_type is not None:
            n = self.event_type.max_conflicting - 1
        else:
            n = 0
        return qs.count() > n

    def get_conflicting_events(self):
        """
        Return a QuerySet of Events that conflict with this one.
        Must work also when called on an unsaved instance.
        May return None to indicate an empty queryset.
        Applications may override this to add specific conditions.
        """
        if self.transparent:
            return
        #~ return False
        #~ Event = dd.resolve_model('cal.Event')
        #~ ot = ContentType.objects.get_for_model(RecurrentEvent)
        qs = self.__class__.objects.filter(transparent=False)
        end_date = self.end_date or self.start_date
        flt = Q(start_date=self.start_date, end_date__isnull=True)
        flt |= Q(end_date__isnull=False,
                 start_date__lte=self.start_date, end_date__gte=end_date)
        if end_date == self.start_date:
            if self.start_time and self.end_time:
                # the other starts before me and ends after i started
                c1 = Q(start_time__lte=self.start_time,
                       end_time__gt=self.start_time)
                # the other ends after me and started before i ended
                c2 = Q(end_time__gte=self.end_time,
                       start_time__lt=self.end_time)
                # the other is full day
                c3 = Q(end_time__isnull=True, start_time__isnull=True)
                flt &= (c1 | c2 | c3)
        qs = qs.filter(flt)
        if self.id is not None:  # don't conflict with myself
            qs = qs.exclude(id=self.id)
        # generated events never conflict with other generated events
        # of same owner. Rule needed for update_events.
        if self.auto_type is not None:
            qs = qs.exclude(
                # auto_type=self.auto_type,
                owner_id=self.owner_id, owner_type=self.owner_type)
        if self.room is not None:
            # other event in the same room
            c1 = Q(room=self.room)
            # other event locks all rooms (e.h. holidays)
            c2 = Q(event_type__all_rooms=True)
            qs = qs.filter(c1 | c2)
        if self.user is not None:
            if self.event_type is not None:
                if self.event_type.locks_user:
                    #~ c1 = Q(event_type__locks_user=False)
                    #~ c2 = Q(user=self.user)
                    #~ qs = qs.filter(c1|c2)
                    qs = qs.filter(user=self.user, event_type__locks_user=True)
        #~ qs = Event.objects.filter(flt,owner_type=ot)
        #~ if we.start_date.month == 7:
            #~ print 20131011, self, we.start_date, qs.count()
        #~ print 20131025, qs.query
        return qs

    def is_fixed_state(self):
        return self.state.fixed
        #~ return self.state in EventStates.editable_states

    def is_user_modified(self):
        return self.state != EventStates.suggested

    def after_ui_create(self, ar):
        super(Event, self).after_ui_create(ar)
        self.update_guests.run_from_code(ar)

    def after_ui_save(self, ar, cw):
        super(Event, self).after_ui_save(ar, cw)
        self.update_guests.run_from_code(ar)

    def suggest_guests(self):
        """Yield the list of Guest instances to be added to this Event.  This
        method is called from :meth:`update_guests`.

        """
        if self.owner:
            for obj in self.owner.suggest_cal_guests(self):
                yield obj

    def get_event_summary(event, ar):
        """How this event should be summarized in contexts where possibly
        another user is looking (i.e. currently in invitations of
        guests, or in the extensible calendar panel).

        """
        #~ from django.utils.translation import ugettext as _
        s = event.summary
        # if event.owner_id:
        #     s += " ({0})".format(event.owner)
        if event.user is not None and event.user != ar.get_user():
            if event.access_class == AccessClasses.show_busy:
                s = _("Busy")
            s = event.user.username + ': ' + unicode(s)
        elif settings.SITE.project_model is not None \
                and event.project is not None:
            s += " " + unicode(_("with")) + " " + unicode(event.project)
        if event.state:
            s = ("(%s) " % unicode(event.state)) + s
        n = event.guest_set.all().count()
        if n:
            s = ("[%d] " % n) + s
        return s

    def before_ui_save(self, ar, **kw):
        """Mark the event as "user modified" by setting a default state.
        This is important because EventGenerators may not modify any
        user-modified Events.

        """
        #~ logger.info("20130528 before_ui_save")
        if self.state is EventStates.suggested:
            self.state = EventStates.draft
        return super(Event, self).before_ui_save(ar, **kw)

    def on_create(self, ar):
        self.event_type = ar.user.event_type or \
            settings.SITE.site_config.default_event_type
        self.start_date = settings.SITE.today()
        self.start_time = timezone.now().time()
        # 20130722 e.g. CreateClientEvent sets it explicitly
        if self.assigned_to is None:
            self.assigned_to = ar.subst_user
        super(Event, self).on_create(ar)

    #~ def on_create(self,ar):
        #~ self.start_date = settings.SITE.today()
        #~ self.start_time = datetime.datetime.now().time()
        # ~ # default user is almost the same as for UserAuthored
        # ~ # but we take the *real* user, not the "working as"
        #~ if self.user_id is None:
            #~ u = ar.user
            #~ if u is not None:
                #~ self.user = u
        #~ super(Event,self).on_create(ar)

    def get_postable_recipients(self):
        """return or yield a list of Partners"""
        if self.project:
            if isinstance(self.project, rt.modules.contacts.Partner):
                yield self.project
        for g in self.guest_set.all():
            yield g.partner
        #~ if self.user.partner:
            #~ yield self.user.partner

    def get_mailable_type(self):
        return self.event_type

    def get_mailable_recipients(self):
        if self.project:
            if isinstance(self.project, rt.modules.contacts.Partner):
                yield ('to', self.project)
        for g in self.guest_set.all():
            yield ('to', g.partner)
        if self.user.partner:
            yield ('cc', self.user.partner)

    #~ def get_mailable_body(self,ar):
        #~ return self.description

    def get_system_note_recipients(self, request, silent):
        if self.user != request.user:
            yield "%s <%s>" % (unicode(self.user), self.user.email)
        if silent:
            return
        for g in self.guest_set.all():
            if g.partner.email:
                yield "%s <%s>" % (unicode(g.partner), g.partner.email)

    @dd.displayfield(_("When"))
    def when_text(self, ar):
        if ar is None:
            return ''
        txt = when_text(self.start_date, self.start_time)
        if self.end_date and self.end_date != self.start_date:
            txt += "-" + when_text(self.end_date, self.end_time)
        return txt
        # return ar.obj2html(self, txt)

    @dd.displayfield(_("Link URL"))
    def url(self, ar):
        return 'foo'

    @dd.displayfield(_("When"))
    def linked_date(self, ar):
        EventsByDay = settings.SITE.modules.cal.EventsByDay
        txt = when_text(self.start_date, self.start_time)
        return EventsByDay.as_link(ar, self.start_date, txt)

    @dd.virtualfield(dd.DisplayField(_("Reminder")))
    def reminder(self, request):
        return False
    #~ reminder.return_type = dd.DisplayField(_("Reminder"))

    def get_calendar(self):
        """
        Returns the Calendar which contains this event,
        or None if no subscription is found.
        Needed for ext.ensible calendar panel.

        The default implementation returns None.
        Override this if your app uses Calendars.
        """
        #~ for sub in Subscription.objects.filter(user=ar.get_user()):
            #~ if sub.contains_event(self):
                #~ return sub
        return None

    @dd.virtualfield(models.ForeignKey('cal.Calendar'))
    def calendar(self, ar):
        return self.get_calendar()

    def get_print_language(self):
        # if settings.SITE.project_model is not None and self.project:
        if self.project:
            return self.project.get_print_language()
        if self.user:
            return self.user.language
        return settings.SITE.get_default_language()

    @classmethod
    def get_default_table(cls):
        return OneEvent

    @classmethod
    def on_analyze(cls, lino):
        cls.DISABLED_AUTO_FIELDS = dd.fields_list(cls, "summary")
        super(Event, cls).on_analyze(lino)


dd.update_field(Event, 'user', verbose_name=_("Responsible user"))

from lino.modlib.plausibility.choicelists import Checker


class EventChecker(Checker):
    """Check whether this event has :message:`No participants although NNN
    suggestions exist.` -- This is probably due to some bug, so we
    repair this by adding the suggested guests.

    """
    verbose_name = _("Check for missing participants")
    model = Event

    def get_plausibility_problems(self, obj, fix=False):
        if not obj.state.edit_guests:
            return
        existing = set([g.partner.pk for g in obj.guest_set.all()])
        if len(existing) == 0:
            suggested = list(obj.suggest_guests())
            if len(suggested) > 0:
                msg = _("No participants although {0} suggestions exist.")
                yield (True, msg.format(len(suggested)))
                if fix:
                    for g in suggested:
                        g.save()

EventChecker.activate()


class Guest(dd.Model):
    """Represents the fact that a given person is expected to attend to a
   given event.

   TODO: Rename this to "Presence".

    """
    workflow_state_field = 'state'

    allow_cascaded_delete = ['event']

    class Meta:
        app_label = 'cal'
        abstract = dd.is_abstract_model(__name__, 'Guest')
        verbose_name = _("Participant")
        verbose_name_plural = _("Participants")

    event = models.ForeignKey('cal.Event')

    partner = dd.ForeignKey('contacts.Partner')

    role = models.ForeignKey('cal.GuestRole',
                             verbose_name=_("Role"),
                             blank=True, null=True)

    state = GuestStates.field(default=GuestStates.invited.as_callable)

    remark = models.CharField(
        _("Remark"), max_length=200, blank=True)

    def get_user(self):
        # used to apply `owner` requirement in GuestState
        return self.event.user
    user = property(get_user)

    def __unicode__(self):
        return u'%s #%s (%s)' % (
            self._meta.verbose_name, self.pk, self.event.strftime())

    # def get_printable_type(self):
    #     return self.role

    def get_mailable_type(self):
        return self.role

    def get_mailable_recipients(self):
        yield ('to', self.partner)

    @dd.displayfield(_("Event"))
    def event_summary(self, ar):
        if ar is None:
            return ''
        return ar.obj2html(self.event, self.event.get_event_summary(ar))


def migrate_reminder(obj, reminder_date, reminder_text,
                     delay_value, delay_type, reminder_done):
    """
    This was used only for migrating to 1.2.0,
    see :mod:`lino.projects.pcsw.migrate`.
    """
    raise NotImplementedError(
        "No longer needed (and no longer supported after 20111026).")

    def delay2alarm(delay_type):
        if delay_type == 'D':
            return DurationUnits.days
        if delay_type == 'W':
            return DurationUnits.weeks
        if delay_type == 'M':
            return DurationUnits.months
        if delay_type == 'Y':
            return DurationUnits.years

    # ~ # These constants must be unique for the whole Lino Site.
    # ~ # Keep in sync with auto types defined in lino.projects.pcsw.models.Person
    #~ REMINDER = 5

    if reminder_text:
        summary = reminder_text
    else:
        summary = _('due date reached')

    update_auto_task(
        None,  # REMINDER,
        obj.user,
        reminder_date,
        summary, obj,
        done=reminder_done,
        alarm_value=delay_value,
        alarm_unit=delay2alarm(delay_type))


# Inject application-specific fields to users.User.
dd.inject_field(settings.SITE.user_model,
                'access_class',
                AccessClasses.field(
                    default=AccessClasses.public.as_callable,
                    verbose_name=_("Default access class"),
                    help_text=_(
            """The default access class for your calendar events and tasks.""")
                ))
dd.inject_field(settings.SITE.user_model,
                'event_type',
                models.ForeignKey('cal.EventType',
                                  blank=True, null=True,
                                  verbose_name=_("Default Event Type"),
        help_text=_("""The default event type for your calendar events.""")
                ))

dd.inject_field('system.SiteConfig',
                'default_event_type',
                models.ForeignKey('cal.EventType',
                                  blank=True, null=True,
                                  verbose_name=_("Default Event Type"),
        help_text=_("""The default type of events on this site.""")
                ))

dd.inject_field(
    'system.SiteConfig',
    'site_calendar',
    models.ForeignKey(
        'cal.Calendar',
        blank=True, null=True,
        related_name="%(app_label)s_%(class)s_set_by_site_calender",
        verbose_name=_("Site Calendar"),
        help_text=_("""The default calendar of this site.""")))

dd.inject_field(
    'system.SiteConfig',
    'max_auto_events',
    models.IntegerField(
        _("Max automatic events"), default=72,
        blank=True, null=True,
        help_text=_(
            """Maximum number of automatic events to be generated.""")
    ))


Reservation.show_today = ShowEventsByDay('start_date')
Event.show_today = ShowEventsByDay('start_date')


def update_reminders_for_user(user, ar):
    n = 0
    for model in rt.models_by_base(EventGenerator):
        for obj in model.objects.filter(user=user):
            obj.update_reminders(ar)
            #~ logger.info("--> %s",unicode(obj))
            n += 1
    return n


class UpdateUserReminders(UpdateEvents):

    """
    Users can invoke this to re-generate their automatic tasks.
    """

    def run_from_ui(self, ar, **kw):
        user = ar.selected_rows[0]
        logger.info("Updating reminders for %s", unicode(user))
        n = update_reminders_for_user(user, ar)
        msg = _("%(num)d reminders for %(user)s have been updated."
                ) % dict(user=user, num=n)
        logger.info(msg)
        ar.success(msg, **kw)


@dd.receiver(dd.pre_analyze, dispatch_uid="add_update_reminders")
def pre_analyze(sender, **kw):
    sender.user_model.define_action(update_reminders=UpdateUserReminders())


