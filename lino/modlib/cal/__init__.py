# Copyright 2013-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""This is Lino's Calendar module.


.. autosummary::
   :toctree:

    mixins
    utils
    models
    choicelists
    ui
    workflows
    fixtures.std
    fixtures.demo
    fixtures.demo2




Glossary
========

.. glossary::

  event

    Something that happens at a given date and (optionally) time.
    A planned ("scheduled") lapse of time where something happens.
    Stored in :class:`Event`.

  appointment

    An appointment (french "Rendez-vous", german "Termin") is an
    :term:`event` whose :class:`type <EventType>` has the
    :attr:`EventType.is_appointment` field checked.




There is no "Calendar" field per Event
======================================

Note that the default implementation has no "Calendar" field per
Event. The `Event` model instead has a `get_calendar` method.

You might extend Event in your plugin as follows::

    from lino.modlib.cal.models import *
    class Event(Event):

        calendar = dd.ForeignKey('cal.Calendar')

        def get_calendar(self):
            return self.calendar

But in other cases it would create unnecessary complexity to add such
a field. For example in :ref:`welfare` there is one calendar per User,
and thus the `get_calendar` method is implemented as follows::

    def get_calendar(self):
        if self.user is not None:
            return self.user.calendar

Or in :ref:`voga` there is one calendar per Room. Thus the
`get_calendar` method is implemented as follows::

    def get_calendar(self):
        if self.room is not None:
            return self.room.calendar

"""

from lino.api import ad, _


class Plugin(ad.Plugin):
    "See :doc:`/dev/plugins`."
    verbose_name = _("Calendar")

    needs_plugins = ['lino.modlib.gfks', 'lino.modlib.printing']

    ignore_dates_before = None
    """
    Ignore dates before the given date.  Set this to `None` if you want
    no limit.
    Default value is "7 days before server startup".

    """

    ignore_dates_after = None
    """Ignore dates after the given date.  This should never be `None`.
    Default value is 5 years after :meth:`today
    <lino.core.site.Site.today>`.

    """

    def on_init(self):
        tod = self.site.today()
        self.ignore_dates_after = tod.replace(year=tod.year+5)
        # tod + datetime.timedelta(days=5*365)

    def setup_main_menu(self, site, profile, m):
        m = m.add_menu(self.app_label, self.verbose_name)
        m.add_action('cal.MyEvents')  # string spec to allow overriding
        # m.add_separator('-')
        # m  = m.add_menu("tasks",_("Tasks"))
        m.add_action('cal.MyTasks')
        # m.add_action(MyTasksToDo)
        m.add_action('cal.MyGuests')
        m.add_action('cal.MyPresences')

    def setup_config_menu(self, site, profile, m):
        m = m.add_menu(self.app_label, self.verbose_name)
        m.add_action('cal.Calendars')
        # m.add_action('cal.MySubscriptions')
        m.add_action('cal.Rooms')
        m.add_action('cal.Priorities')
        m.add_action('cal.RecurrentEvents')
        # m.add_action(AccessClasses)
        # m.add_action(EventStatuses)
        # m.add_action(TaskStatuses)
        # m.add_action(EventTypes)
        m.add_action('cal.GuestRoles')
        # m.add_action(GuestStatuses)
        m.add_action('cal.EventTypes')
        m.add_action('cal.RemoteCalendars')

    def setup_explorer_menu(self, site, profile, m):
        m = m.add_menu(self.app_label, self.verbose_name)
        m.add_action('cal.Tasks')
        m.add_action('cal.Guests')
        m.add_action('cal.Subscriptions')
        # m.add_action(Memberships)
        m.add_action('cal.EventStates')
        m.add_action('cal.GuestStates')
        m.add_action('cal.TaskStates')
        # m.add_action(RecurrenceSets)


