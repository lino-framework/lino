# -*- coding: UTF-8 -*-
# Copyright 2011-2014 Luc Saffre
# License: BSD (see file COPYING for details)

"""
The :xfile:`models.py` module for the :mod:`lino.modlib.cal` app.
"""

from __future__ import unicode_literals

import logging
logger = logging.getLogger(__name__)

import datetime

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import force_unicode

from lino import mixins
from lino import dd
from lino.utils import ONE_DAY

from lino.modlib.contenttypes.mixins import Controllable

from .utils import (
    DurationUnits, Recurrencies,
    setkw, dt2kw,
    when_text,
    Weekdays, AccessClasses)


from .workflows import (
    TaskStates, EventStates, GuestStates)

from .workflows import take

from .mixins import StartedSummaryDescription

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
        super(RemoteCalendar, self).save(*args, **k)


class RemoteCalendars(dd.Table):
    model = 'cal.RemoteCalendar'
    required = dd.required(user_groups='office', user_level='manager')


class Room(mixins.BabelNamed):

    """
    A location where Events can happen.
    For a given Room you can see the :class:`EventsByRoom`
    that happened (or will happen) there.
    A Room is BabelNamed (has a multilingual name).
    """
    class Meta:
        abstract = dd.is_abstract_model(__name__, 'Room')
        verbose_name = _("Room")
        verbose_name_plural = _("Rooms")

    #~ def __unicode__(self):
        #~ s = mixins.BabelNamed.__unicode__(self)
        #~ if self.company and self.company.city:
            #~ s = '%s (%s)' % (self.company.city,s)
        #~ return s


class Rooms(dd.Table):
    help_text = _("List of rooms where calendar events can happen.")
    required = dd.required(user_groups='office', user_level='manager')
    model = 'cal.Room'
    detail_layout = """
    id name
    cal.EventsByRoom
    """


class Priority(mixins.BabelNamed):

    "The priority of a Task or Event."
    class Meta:
        verbose_name = _("Priority")
        verbose_name_plural = _('Priorities')
    ref = models.CharField(max_length='1')


class Priorities(dd.Table):
    help_text = _("List of possible priorities of calendar events.")
    required = dd.required(user_groups='office', user_level='manager')
    model = Priority
    column_names = 'name *'


class Component(StartedSummaryDescription,
                mixins.ProjectRelated,
                mixins.UserAuthored,
                Controllable,
                mixins.CreatedModified):

    """
    Abstract base class for :class:`Event` and :class:`Task`.

    """
    workflow_state_field = 'state'

    manager_level_field = 'office_level'

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


def update_auto_event(
        autotype, user, date, summary, owner, **defaults):
        #~ model = dd.resolve_model('cal.Event')
    return update_auto_component(Event, autotype, user, date, summary, owner, **defaults)


def update_auto_task(
        autotype, user, date, summary, owner, **defaults):
    Task = dd.resolve_model('cal.Task')
    return update_auto_component(
        Task, autotype, user, date, summary, owner, **defaults)


def update_auto_component(
        model, autotype, user, date, summary, owner, **defaults):
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
    if date and date >= settings.SITE.today() + datetime.timedelta(days=-7):
        #~ defaults = owner.get_auto_task_defaults(**defaults)
        #~ print "20120729 b"
        defaults.setdefault('user', user)
        obj, created = model.objects.get_or_create(
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
                                    owner_type=ot, auto_type=autotype)
        except model.DoesNotExist:
            pass
        else:
            if not obj.is_user_modified():
                obj.delete()


def update_reminder(type, owner, user, orig, msg, num, unit):
    """
    Shortcut for calling :func:`update_auto_task`
    for automatic "reminder tasks".
    A reminder task is a message about something that will
    happen in the future.
    """
    update_auto_task(
        type, user,
        unit.add_duration(orig, -num),
        msg,
        owner)


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


MODULE_LABEL = settings.SITE.plugins.cal.verbose_name


class UserDetailMixin(dd.Panel):

    cal_left = """
    event_type access_class
    calendar
    cal.SubscriptionsByUser
    # cal.MembershipsByUser
    """

    cal = dd.Panel(
        """
        cal_left:30 cal.TasksByUser:60
        """,
        label=MODULE_LABEL,
        required=dict(user_groups='office'))

    
def unused_site_setup(site):
    """
    (Called during site setup.)

    Adds a "Calendar" tab and the :class:`UpdateEvents`
    action to `users.User`
    """

    site.modules.users.Users.add_detail_panel(
        'cal_left', """
        event_type access_class
        cal.SubscriptionsByUser
        # cal.MembershipsByUser
        """)
    site.modules.users.Users.add_detail_tab(
        'cal', """
        cal_left:30 cal.TasksByUser:60
        """,
        MODULE_LABEL,
        required=dict(user_groups='office'))


def setup_main_menu(site, ui, profile, m):
    m = m.add_menu("cal", MODULE_LABEL)

    m.add_action('cal.MyEvents')  # string spec to allow overriding

    #~ m.add_separator('-')
    #~ m  = m.add_menu("tasks",_("Tasks"))
    m.add_action('cal.MyTasks')
    #~ m.add_action(MyTasksToDo)

    m.add_action('cal.MyGuests')

    m.add_action('cal.MyPresences')


def setup_config_menu(site, ui, profile, m):
    m = m.add_menu("cal", MODULE_LABEL)
    m.add_action('cal.Calendars')
    #~ m.add_action('cal.MySubscriptions')
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
    m.add_action('cal.RemoteCalendars')


def setup_explorer_menu(site, ui, profile, m):
    m = m.add_menu("cal", MODULE_LABEL)
    m.add_action('cal.Tasks')
    m.add_action('cal.Guests')
    m.add_action('cal.Subscriptions')
    #~ m.add_action(Memberships)
    m.add_action('cal.EventStates')
    m.add_action('cal.GuestStates')
    m.add_action('cal.TaskStates')
    #~ m.add_action(RecurrenceSets)


customize_users()

from .models_calendar import *
from .models_task import *
from .models_guest import *
from .models_event import *

from .mixins import EventGenerator, RecurrenceSet, Reservation

Reservation.show_today = ShowEventsByDay('start_date')
Event.show_today = ShowEventsByDay('start_date')
