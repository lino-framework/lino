# -*- coding: UTF-8 -*-
# Copyright 2011-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""Database models for `lino.modlib.cal`.

"""

from __future__ import unicode_literals

import logging
logger = logging.getLogger(__name__)

import datetime

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import force_unicode

from lino import mixins
from lino.api import dd
from lino.utils import ONE_DAY

from lino.modlib.contenttypes.mixins import Controllable
from lino.modlib.users.mixins import UserAuthored
from lino.modlib.office.roles import OfficeUser, OfficeStaff

from .utils import (
    DurationUnits, Recurrencies,
    setkw, dt2kw,
    when_text,
    Weekdays, AccessClasses)

from .workflows import (TaskStates, EventStates, GuestStates)

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
    required_roles = dd.required(OfficeStaff)


class Room(mixins.BabelNamed):
    """A location where calendar events can happen.  For a given Room you
    can see the :class:`EventsByRoom` that happened (or will happen)
    there.  A Room is BabelNamed (has a multilingual name).

    """
    class Meta:
        abstract = dd.is_abstract_model(__name__, 'Room')
        verbose_name = _("Room")
        verbose_name_plural = _("Rooms")


class Rooms(dd.Table):
    help_text = _("List of rooms where calendar events can happen.")
    required_roles = dd.required(OfficeStaff)
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
    required_roles = dd.required(OfficeStaff)
    model = Priority
    column_names = 'name *'


class Component(StartedSummaryDescription,
                mixins.ProjectRelated,
                UserAuthored,
                Controllable,
                mixins.CreatedModified):

    """
    Abstract base class for :class:`Event` and :class:`Task`.

    """
    workflow_state_field = 'state'

    manager_roles_required = OfficeStaff
    # manager_level_field = 'office_level'

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


MODULE_LABEL = dd.plugins.cal.verbose_name


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
        required_roles=dd.required(OfficeUser))

    
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
        required_roles=dd.required(OfficeUser))


customize_users()

from .models_calendar import *
from .models_task import *
from .models_guest import *
from .models_event import *

from .mixins import EventGenerator, RecurrenceSet, Reservation

Reservation.show_today = ShowEventsByDay('start_date')
Event.show_today = ShowEventsByDay('start_date')
