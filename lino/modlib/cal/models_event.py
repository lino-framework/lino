# -*- coding: UTF-8 -*-
# Copyright 2011-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""
Part of the :xfile:`models.py` module for the :mod:`lino.modlib.cal` app.

Defines the :class:`EventType` and :class:`Event` models and their tables.

"""

from __future__ import unicode_literals

import logging
logger = logging.getLogger(__name__)

import datetime

from django.conf import settings
from django.db import models
from django.db.models import Q

from lino.api import dd, rt, _, pgettext
from lino import mixins

from lino.modlib.postings.mixins import Postable
from lino.modlib.outbox.mixins import MailableType, Mailable
from lino.modlib.office.roles import OfficeUser, OfficeStaff, OfficeOperator

from .utils import (
    Recurrencies,
    when_text,
    AccessClasses)


from .mixins import Ended
from .mixins import RecurrenceSet, EventGenerator
from .mixins import UpdateEvents
from .mixins import MoveEventNext
from .mixins import daterange_text
from .models import Component
from .models import Priority
from .workflows import EventStates

outbox = dd.resolve_app('outbox')


class EventType(mixins.BabelNamed, mixins.Sequenced,
                MailableType):
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
        max_length=200, blank=True)
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


class EventTypes(dd.Table):
    help_text = _("""The list of Event Types defined on this system.
    An EventType is a list of events which have certain things in common,
    especially they are displayed in the same colour in the calendar panel.
    """)
    required_roles = dd.required(OfficeStaff)
    model = 'cal.EventType'
    column_names = "name *"

    detail_layout = """
    name
    event_label
    # description
    start_date id
    # type url_template username password
    #build_method #template email_template attach_to_email
    is_appointment all_rooms locks_user max_conflicting
    EventsByType
    """

    insert_layout = dd.FormLayout("""
    name
    event_label
    """, window_size=(60, 'auto'))


class RecurrentEvent(mixins.BabelNamed, RecurrenceSet, EventGenerator):
    """An event that recurs at intervals.
    """
    class Meta:
        verbose_name = _("Recurrent Event")
        verbose_name_plural = _("Recurrent Events")

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

dd.update_field(
    RecurrentEvent, 'every_unit',
    default=Recurrencies.yearly, blank=False, null=False)


class RecurrentEvents(dd.Table):
    """The list of all recurrent events (:class:`RecurrentEvent`).

    """
    model = 'cal.RecurrentEvent'
    required_roles = dd.required(OfficeStaff)
    column_names = "start_date end_date name every_unit event_type *"
    auto_fit_column_widths = True
    order_by = ['start_date']

    insert_layout = """
    name
    start_date end_date every_unit event_type
    """
    insert_layout_width = 80

    detail_layout = """
    name
    id user event_type
    start_date start_time  end_date end_time
    every_unit every max_events
    monday tuesday wednesday thursday friday saturday sunday
    description cal.EventsByController
    """


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
                obj.end_time = datetime.time(10, 0, 0)
        #~ obj.save()

    def value_from_object(self, obj, ar):
        #~ logger.info("20120118 value_from_object() %s",dd.obj2str(obj))
        return (obj.start_time is None)

# ~ from lino.modlib.workflows import models as workflows # Workflowable

#~ class Components(dd.Table):
# ~ # class Components(dd.Table,workflows.Workflowable):

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


class Event(Component, Ended,
            mixins.TypedPrintable,
            Mailable,
            Postable):
    """
    A calendar event is a lapse of time to be visualized in a calendar.

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

    """
    class Meta:
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
    state = EventStates.field(default=EventStates.suggested)  # iCal:STATUS
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
        """
        Mark the event as "user modified" by setting a default state.
        This is important because EventGenerators may not modify any user-modified Events.
        """
        #~ logger.info("20130528 before_ui_save")
        if self.state is EventStates.suggested:
            self.state = EventStates.draft
        return super(Event, self).before_ui_save(ar, **kw)

    def on_create(self, ar):
        self.event_type = ar.user.event_type or \
            settings.SITE.site_config.default_event_type
        self.start_date = settings.SITE.today()
        self.start_time = datetime.datetime.now().time()
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
        assert ar is not None
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
        if settings.SITE.project_model is not None and self.project:
            return self.project.get_print_language()
        return self.user.language

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


class EventDetail(dd.FormLayout):
    start = "start_date start_time"
    end = "end_date end_time"
    main = """
    event_type summary user assigned_to
    start end #all_day #duration state
    room priority access_class transparent #rset
    owner created:20 modified:20
    description
    GuestsByEvent #outbox.MailsByController
    """


class EventInsert(EventDetail):
    main = """
    event_type summary
    start end
    room priority access_class transparent
    """


class EventEvents(dd.ChoiceList):
    verbose_name = _("Observed event")
    verbose_name_plural = _("Observed events")
add = EventEvents.add_item
add('10', _("Okay"), 'okay')
add('20', _("Pending"), 'pending')


class Events(dd.Table):
    """Table which shows all calendar events. """

    help_text = _("A List of calendar entries. Each entry is called an event.")
    model = 'cal.Event'
    required_roles = dd.required(OfficeStaff)
    column_names = 'when_text:20 user summary event_type *'

    # hidden_columns = """
    # priority access_class transparent
    # owner created modified
    # description
    # sequence auto_type build_time owner owner_id owner_type
    # end_date end_time
    # """

    order_by = ["start_date", "start_time"]

    detail_layout = EventDetail()
    insert_layout = EventInsert()

    params_panel_hidden = True

    parameters = mixins.ObservedPeriod(
        user=dd.ForeignKey(settings.SITE.user_model,
                           verbose_name=_("Managed by"),
                           blank=True, null=True,
                           help_text=_("Only rows managed by this user.")),
        project=dd.ForeignKey(settings.SITE.project_model,
                              blank=True, null=True),
        event_type=dd.ForeignKey('cal.EventType', blank=True, null=True),
        room=dd.ForeignKey('cal.Room', blank=True, null=True),
        assigned_to=dd.ForeignKey(settings.SITE.user_model,
                                  verbose_name=_("Assigned to"),
                                  blank=True, null=True,
                                  help_text=_(
                                      "Only events assigned to this user.")),
        state=EventStates.field(blank=True,
                                help_text=_("Only rows having this state.")),
        #~ unclear = models.BooleanField(_("Unclear events"))
        observed_event=EventEvents.field(blank=True),
        show_appointments=dd.YesNo.field(_("Appointments"), blank=True),
    )

    params_layout = """
    start_date end_date observed_event state
    user assigned_to project event_type room show_appointments
    """
    # ~ next = NextDateAction() # doesn't yet work. 20121203

    fixed_states = set(EventStates.filter(fixed=True))
    #~ pending_states = set([es for es in EventStates if not es.fixed])
    pending_states = set(EventStates.filter(fixed=False))

    @classmethod
    def get_request_queryset(self, ar):
        #~ logger.info("20121010 Clients.get_request_queryset %s",ar.param_values)
        qs = super(Events, self).get_request_queryset(ar)
        pv = ar.param_values

        if pv.user:
            qs = qs.filter(user=pv.user)
        if pv.assigned_to:
            qs = qs.filter(assigned_to=pv.assigned_to)

        if settings.SITE.project_model is not None and pv.project:
            qs = qs.filter(project=pv.project)

        if pv.event_type:
            qs = qs.filter(event_type=pv.event_type)
        else:
            if pv.show_appointments == dd.YesNo.yes:
                qs = qs.filter(event_type__is_appointment=True)
            elif pv.show_appointments == dd.YesNo.no:
                qs = qs.filter(event_type__is_appointment=False)

        if pv.state:
            qs = qs.filter(state=pv.state)

        if pv.room:
            qs = qs.filter(room=pv.room)

        if pv.observed_event == EventEvents.okay:
            qs = qs.filter(state__in=self.fixed_states)
        elif pv.observed_event == EventEvents.pending:
            qs = qs.filter(state__in=self.pending_states)

        if pv.start_date:
            qs = qs.filter(start_date__gte=pv.start_date)
        if pv.end_date:
            qs = qs.filter(start_date__lte=pv.end_date)
        return qs

    @classmethod
    def get_title_tags(self, ar):
        for t in super(Events, self).get_title_tags(ar):
            yield t
        pv = ar.param_values
        if pv.start_date or pv.end_date:
            yield daterange_text(
                pv.start_date,
                pv.end_date)

        if pv.state:
            yield unicode(pv.state)

        if pv.event_type:
            yield unicode(pv.event_type)

        if pv.user:
            yield unicode(pv.user)

        if pv.room:
            yield unicode(pv.room)

        if settings.SITE.project_model is not None and pv.project:
            yield unicode(pv.project)

        if pv.assigned_to:
            yield unicode(self.parameters['assigned_to'].verbose_name) \
                + ' ' + unicode(pv.assigned_to)

    @classmethod
    def apply_cell_format(self, ar, row, col, recno, td):
        """
        Enhance today by making background color a bit darker.
        """
        if row.start_date == settings.SITE.today():
            td.attrib.update(bgcolor="#bbbbbb")


class EventsByType(Events):
    master_key = 'event_type'


class EventsByDay(Events):
    """
    This table is usually labelled "Appointments today". It has no
    "date" column because it shows events of a given date.

    The default filter parameters are set to show only
    :term:`appointments <appointment>`.

    """
    required_roles = dd.required((OfficeUser, OfficeOperator))
    label = _("Appointments today")
    column_names = 'room event_type summary owner workflow_buttons *'
    auto_fit_column_widths = True
    params_panel_hidden = False

    @classmethod
    def param_defaults(self, ar, **kw):
        kw = super(EventsByDay, self).param_defaults(ar, **kw)
        kw.update(show_appointments=dd.YesNo.yes)
        kw.update(start_date=settings.SITE.today())
        kw.update(end_date=settings.SITE.today())
        return kw

    @classmethod
    def create_instance(self, ar, **kw):
        kw.update(start_date=ar.param_values.start_date)
        return super(EventsByDay, self).create_instance(ar, **kw)

    @classmethod
    def get_title_base(self, ar):
        return when_text(ar.param_values.start_date)

    @classmethod
    def as_link(cls, ar, today, txt=None):
        if today is None:
            today = settings.SITE.today()
        if txt is None:
            txt = when_text(today)
        pv = dict(start_date=today)
        # TODO: what to do with events that span multiple days?
        pv.update(end_date=today)
        target = ar.spawn(cls, param_values=pv)
        return ar.href_to_request(target, txt)


class ShowEventsByDay(dd.Action):
    label = _("Today")
    help_text = _("Show all calendar events of the same day.")
    show_in_bbar = True
    sort_index = 60
    icon_name = 'calendar'

    def __init__(self, date_field, **kw):
        self.date_field = date_field
        super(ShowEventsByDay, self).__init__(**kw)

    def run_from_ui(self, ar, **kw):
        obj = ar.selected_rows[0]
        today = getattr(obj, self.date_field)
        pv = dict(start_date=today)
        pv.update(end_date=today)
        sar = ar.spawn(EventsByDay, param_values=pv)
        js = ar.renderer.request_handler(sar)
        ar.set_response(eval_js=js)


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
    required_roles = dd.required(OfficeUser)
    master_key = 'owner'
    column_names = 'when_text summary workflow_buttons *'
    # column_names = 'when_text:20 linked_date summary workflow_buttons *'
    auto_fit_column_widths = True

if settings.SITE.project_model:

    class EventsByProject(Events):
        required_roles = dd.required(OfficeUser)
        master_key = 'project'
        auto_fit_column_widths = True
        column_names = 'linked_date user summary workflow_buttons'
        # column_names = 'when_text user summary workflow_buttons'


class OneEvent(Events):
    show_detail_navigator = False
    use_as_default_table = False
    required_roles = dd.required(OfficeUser)


class MyEvents(Events):
    """Table which shows today's and future appointments of the
    requesting user.  The default filter parameters are set to show
    only :term:`appointments <appointment>`.

    """
    label = _("My appointments")
    help_text = _("Table of my appointments.")
    required_roles = dd.required(OfficeUser)
    column_names = 'when_text project event_type summary workflow_buttons *'
    auto_fit_column_widths = True

    @classmethod
    def param_defaults(self, ar, **kw):
        kw = super(MyEvents, self).param_defaults(ar, **kw)
        kw.update(user=ar.get_user())
        kw.update(show_appointments=dd.YesNo.yes)
        #~ kw.update(assigned_to=ar.get_user())
        #~ logger.info("20130807 %s %s",self,kw)
        kw.update(start_date=settings.SITE.today())
        # kw.update(end_date=settings.SITE.today(14))
        return kw

    @classmethod
    def create_instance(self, ar, **kw):
        kw.update(start_date=ar.param_values.start_date)
        return super(MyEvents, self).create_instance(ar, **kw)


class MyAssignedEvents(MyEvents):
    """
    The table of events which are *assigned* to me. That is, whose
    :attr:`Event.assigned_to` field refers to the requesting user.

    This table also causes a :term:`welcome message` "X events have been
    assigned to you" in case it is not empty.

    """
    label = _("Events assigned to me")
    help_text = _("Table of events assigned to me.")
    #~ master_key = 'assigned_to'
    required_roles = dd.required(OfficeUser)
    #~ column_names = 'when_text:20 project summary workflow_buttons *'
    #~ known_values = dict(assigned_to=EventStates.assigned)

    @classmethod
    def param_defaults(self, ar, **kw):
        kw = super(MyAssignedEvents, self).param_defaults(ar, **kw)
        kw.update(user=None)
        kw.update(assigned_to=ar.get_user())
        return kw

    @classmethod
    def get_welcome_messages(cls, ar, **kw):
        sar = ar.spawn(cls)
        count = sar.get_total_count()
        if count > 0:
            txt = _("%d events have been assigned to you.") % count
            yield ar.href_to_request(sar, txt)


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


