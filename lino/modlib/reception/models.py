# -*- coding: UTF-8 -*-
# Copyright 2013-2014 Luc Saffre
# License: BSD (see file COPYING for details)

"""
Defines models for :mod:`ml.reception`.

Guest

    state   ---action--> new state

    present ---checkin--> waiting
    waiting ---receive-->  busy
    busy    ---checkout--> gone

"""

import logging
logger = logging.getLogger(__name__)

import datetime


from django.db import models
from django.db.models import Q
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.contrib.humanize.templatetags.humanize import naturaltime

from lino.utils.xmlgen.html import E
from lino.utils import join_elems

from lino import dd, rt

cal = dd.resolve_app('cal')
system = dd.resolve_app('system')

from ..cal.models import GuestStates, EventStates

#~ EventStates.add_item('30', _("Visit"), 'visit',fixed=False)

add = GuestStates.add_item
add('44', _("Waiting"), 'waiting')
add('45', _("Busy"), 'busy')
add('46', _("Gone"), 'gone')


from lino.modlib.reception import Plugin

#~ add = GuestStates.add_item
#~ add('21', _("Waiting"),'waiting')

dd.inject_field(
    'cal.Guest', 'waiting_since',
    models.DateTimeField(
        _("Waiting since"),
        editable=False, blank=True, null=True,
        help_text=_("Time when the visitor arrived (checked in).")))
dd.inject_field(
    'cal.Guest', 'busy_since',
    models.DateTimeField(
        _("Waiting until"),
        editable=False, blank=True, null=True,
        help_text=_("Time when the visitor was received by agent.")))
dd.inject_field(
    'cal.Guest', 'gone_since',
    models.DateTimeField(
        _("Present until"),
        editable=False, blank=True, null=True,
        help_text=_("Time when the visitor left (checked out).")))


dd.inject_field(
    'system.SiteConfig', 'prompt_calendar',
    dd.ForeignKey(
        'cal.EventType',
        verbose_name=_("Default type for prompt events"),
        related_name='prompt_calendars',
        blank=True, null=True))


@dd.receiver(dd.pre_save, sender=system.SiteConfig)
def beware(sender, instance=None, **kw):
    if instance.prompt_calendar is not None:
        if instance.prompt_calendar.invite_client:
            raise Warning("prompt event_type may not invite client!")

#~ dd.inject_field('cal.Event','is_prompt',
    #~ models.BooleanField(_("Prompt event"),default=False))


def create_prompt_event(
        project, partner, user, summary,
        guest_role, now=None):
    """
    Create a "prompt event".
    """
    ekw = dict(project=project)
    #~ ekw.update(state=cal.EventStates.draft)
    #~ ekw.update(state=EventStates.published)
    today = settings.SITE.today()
    ekw.update(start_date=today)
    ekw.update(end_date=today)
    ekw.update(event_type=settings.SITE.site_config.prompt_calendar)
    ekw.update(state=EventStates.published)
    ekw.update(user=user)
    if summary:
        ekw.update(summary=summary)
    event = cal.Event(**ekw)
    event.save()
    if now is None:
        now = datetime.datetime.now()
    rt.modules.cal.Guest(
        event=event,
        partner=partner,
        state=cal.GuestStates.waiting,
        role=guest_role,
        #~ role=settings.SITE.site_config.client_guestrole,
        waiting_since=now
    ).save()
    #~ event.full_clean()
    #~ print 20130722, ekw, ar.action_param_values.user, ar.get_user()
    return event


class CheckinVisitor(dd.NotifyingAction):
    label = _("Checkin")
    help_text = _("Mark this visitor as arrived")
    show_in_workflow = True

    required = dd.Required(
        user_groups='reception',
        states='invited accepted present')

    def get_action_permission(self, ar, obj, state):
        if obj.partner_id is None:
            return False
        return super(CheckinVisitor,
                     self).get_action_permission(ar, obj, state)

    def get_notify_subject(self, ar, obj):
        return _("%(partner)s has started waiting for %(user)s") % dict(
            event=obj,
            user=obj.event.user,
            partner=obj.partner)

    def run_from_ui(self, ar, **kw):
        obj = ar.selected_rows[0]
        # cal.Guest

        def doit(ar2):
            obj.waiting_since = datetime.datetime.now()
            obj.state = GuestStates.busy
            obj.busy_since = None
            obj.save()
            ar2.success()
            super(CheckinVisitor, self).run_from_ui(ar2, **kw)

        if obj.event.assigned_to is not None:

            def ok(ar3):
                obj.event.user = obj.event.assigned_to
                obj.event.assigned_to = None
                obj.event.save()
                doit(ar3)

            return ar.confirm(
                ok,
                _("Checkin in will reassign the event "
                  "from %(old)s to %(new)s.") %
                dict(old=obj.event.user, new=obj.event.assigned_to),
                _("Are you sure?"))

        return doit(ar)


class ReceiveVisitor(dd.Action):
    label = _("Receive")
    help_text = _("Visitor was received by agent")
    show_in_workflow = True

    required = dd.Required(states='waiting')

    def run_from_ui(self, ar, **kw):
        obj = ar.selected_rows[0]

        def ok(ar):
            obj.state = GuestStates.busy
            obj.busy_since = datetime.datetime.now()
            #~ if obj.state in ExpectedGuestsStates:
                #~ obj.state = GuestStates.present

            if not obj.event.start_time:
                ar.info("event.start_time has been set")
                obj.event.start_time = obj.busy_since
                obj.event.save()

            obj.save()
            ar.success(refresh=True)

        ar.confirm(ok,
                   _("%(guest)s begins consultation with %(user)s.") %
                   dict(user=obj.event.user, guest=obj.partner),
                   _("Are you sure?"))


"""

What                       waiting_since   busy_since  gone_since
Visitor checks in          X
Agent receives the visitor X               X
Visitor leaves             X               X              X




"""


class CheckoutVisitor(dd.Action):
    label = _("Checkout")
    help_text = _("Visitor left the centre")
    show_in_workflow = True

    #~ required = dict(states='waiting')
    required = dd.Required(states='busy waiting')

    def run_from_ui(self, ar, **kw):
        obj = ar.selected_rows[0]

        def ok(ar2):
            obj.gone_since = datetime.datetime.now()
            if obj.busy_since is None:
                obj.busy_since = obj.gone_since
            if not obj.event.end_time:
                ar.info("event.end_time has been set")
                obj.event.end_time = obj.gone_since
                obj.event.save()

            obj.state = GuestStates.gone
            obj.save()
            kw.update(refresh=True)
            ar2.success(**kw)

        #~ if obj.busy_since is None:
            #~ msg = _("%(guest)s leaves without being received.") % dict(guest=obj.partner)
        #~ else:
        msg = _("%(guest)s leaves after meeting with %(user)s.") % dict(
            guest=obj.partner, user=obj.user)
        ar.confirm(ok, msg, _("Are you sure?"))


cal.Guest.checkin = CheckinVisitor(sort_index=100)
cal.Guest.receive = ReceiveVisitor(sort_index=101)
cal.Guest.checkout = CheckoutVisitor(sort_index=102)


@dd.receiver(dd.pre_analyze)
def my_guest_workflows(sender=None, **kw):
    GuestStates.excused.add_transition(
        states='invited waiting accepted absent')
    GuestStates.absent.add_transition(
        states='waiting invited accepted excused')


class AppointmentsByPartner(dd.Table):
    label = _("Appointments")
    model = 'cal.Guest'
    #~ detail_layout = cal.Guests.detail_layout
    master_key = 'partner'
    #~ column_names = 'event__start_date event__user workflow_buttons'
    column_names = 'event__when_text event__user workflow_buttons'
    #~ slave_grid_format = 'html'
    editable = False
    auto_fit_column_widths = True
    variable_row_height = True

    @classmethod
    def get_request_queryset(self, ar):
        # logger.info("20121010 Clients.get_request_queryset %s",ar.param_values)
        qs = super(AppointmentsByPartner, self).get_request_queryset(ar)
        if isinstance(qs, list):
            return qs
        start_date = settings.SITE.today() - datetime.timedelta(days=17)
        end_date = settings.SITE.today() + datetime.timedelta(days=17)
        qs = qs.filter(event__start_date__gte=start_date,
                       event__start_date__lte=end_date)
        return qs


# ExpectedGuestsStates = (GuestStates.invited, GuestStates.accepted)


class ExpectedGuests(cal.Guests):
    label = _("Expected Guests")
    help_text = _("Consult this table when checking in a partner who \
    has an appointment.")
    # filter = Q(waiting_since__isnull=True,
    #            state__in=ExpectedGuestsStates)
    column_names = 'partner event__user event__summary workflow_buttons \
    waiting_since busy_since'
    hidden_columns = 'waiting_since busy_since'
    #~ checkin = CheckinGuest()
    required = dd.Required(user_groups='reception')

    @classmethod
    def get_queryset(self, ar):
        return self.model.objects.filter(
            waiting_since__isnull=True,
            state__in=(GuestStates.invited, GuestStates.accepted))

    @classmethod
    def param_defaults(self, ar, **kw):
        kw = super(ExpectedGuests, self).param_defaults(ar, **kw)
        #~ kw.update(only_expected=True)
        today = settings.SITE.today()
        kw.update(start_date=today)
        kw.update(end_date=today)
        return kw


if False:
    class ReceivedVisitors(cal.Guests):
        label = _("Received Visitors")
        help_text = _("Shows the visitors being received.")
        filter = Q(waiting_since__isnull=False,
                   busy_since__isnull=False, gone_since__isnull=True)
        column_names = 'since partner event__user event__summary \
        workflow_buttons'
        order_by = ['waiting_since']
        #~ checkout = CheckoutGuest()
        required = dd.Required(user_groups='reception')
        auto_fit_column_widths = True

        @dd.displayfield(_('Since'))
        def since(self, obj, ar):
            # *received since* == *waiting until*
            return naturaltime(obj.busy_since)


class Visitors(cal.Guests):

    """
    No subclass should be editable because deleting would leave the
    useless cal.Event.
    """
    editable = False
    abstract = True
    column_names = 'since partner event__user event__summary workflow_buttons'
    #~ hidden_columns = 'waiting_since busy_since gone_since'
    auto_fit_column_widths = True

    visitor_state = None

    @classmethod
    def param_defaults(self, ar, **kw):
        kw = super(Visitors, self).param_defaults(ar, **kw)
        #~ k = self.visitor_state.name+'_since'
        kw.update(guest_state=self.visitor_state)
        return kw

    #~ doesn't work because cls is always Visitors
    #~ @dd.displayfield(_('Since'))
    #~ def since(cls,obj,ar):
        # ~ # either waiting_since, busy_since or gone_since
        #~ if cls.visitor_state is None: return 'x'
        #~ k = cls.visitor_state.name+'_since'
        #~ return naturaltime(getattr(obj,k))


class MyVisitors(object):

    @classmethod
    def param_defaults(self, ar, **kw):
        kw = super(MyVisitors, self).param_defaults(ar, **kw)
        kw.update(user=ar.get_user())
        return kw


class BusyVisitors(Visitors):
    label = _("Busy visitors")
    help_text = _("Shows the visitors who are busy with some agent.")
    visitor_state = GuestStates.busy
    order_by = ['busy_since']
    required = dd.Required(user_groups='reception')

    @dd.displayfield(_('Since'))
    def since(self, obj, ar):
        return naturaltime(obj.busy_since)


class WaitingVisitors(Visitors):
    label = _("Waiting visitors")
    help_text = _("Shows the visitors in the waiting room.")
    #~ known_values = dict(state=GuestStates.waiting)
    #~ filter = Q(waiting_since__isnull=False,busy_since__isnull=True)
    column_names = 'since partner event__user position event__summary workflow_buttons'
    visitor_state = GuestStates.waiting

    order_by = ['waiting_since']
    required = dd.Required(user_groups='reception')

    @dd.displayfield(_('Since'))
    def since(self, obj, ar):
        return naturaltime(obj.waiting_since)

    @dd.displayfield(_('Position'),
                     help_text=_("Position in waiting queue (per agent)"))
    def position(self, obj, ar):
        n = 1 + rt.modules.cal.Guest.objects.filter(
            #~ waiting_since__isnull=False,
            #~ busy_since__isnull=True,
            state=GuestStates.waiting,
            event__user=obj.event.user,
            waiting_since__lt=obj.waiting_since).count()
        return str(n)


class GoneVisitors(Visitors):
    label = _("Gone visitors")
    help_text = _("Shows the visitors who have gone.")
    visitor_state = GuestStates.gone
    order_by = ['-gone_since']
    required = dd.Required(user_groups='reception')

    @dd.displayfield(_('Since'))
    def since(self, obj, ar):
        return naturaltime(obj.gone_since)


class MyWaitingVisitors(MyVisitors, WaitingVisitors):
    label = _("Visitors waiting for me")
    #~ column_names = 'since partner event__summary workflow_buttons'


class MyBusyVisitors(MyVisitors, BusyVisitors):
    label = _("Visitors busy with me")

    @classmethod
    def get_welcome_messages(cls, ar):
        guests = []
        sar = ar.spawn(cls)
        for g in sar:
            guests.append(g)
        #~ print "20130909 MyBusyVisitors get_welcome_messages", guests
        if len(guests) > 0:
            #~ print 20130909, guests[0].get_default_table()
            chunks = [unicode(_("You are busy with "))]

            def f(g):
                return sar.row_action_button(
                    g, cls.detail_action, unicode(g.partner), icon_name=None)
            chunks += join_elems([f(g)
                                 for g in guests], sep=unicode(_(" and ")))
            chunks.append('.')
            yield E.span(*chunks)


class MyGoneVisitors(MyVisitors, GoneVisitors):
    label = _("My gone visitors")


dd.add_user_group('reception', Plugin.verbose_name)


def setup_main_menu(site, ui, profile, m):
    app = dd.apps.reception
    m = m.add_menu(app.app_name, app.verbose_name)

    m.add_action('cal.EventsByDay')

    m.add_action('reception.WaitingVisitors')
    m.add_action('reception.BusyVisitors')
    m.add_action('reception.GoneVisitors')

    # MyWaitingVisitors is maybe not needed as a menu entry since it
    # is also a get_admin_main_items. if i remove it then i must edit
    # pcsw_tests.py Waiting for user feedback before doing this.
    m.add_action('reception.MyWaitingVisitors')
