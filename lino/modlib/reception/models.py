# -*- coding: UTF-8 -*-
# Copyright 2013-2016 Luc Saffre
# License: BSD (see file COPYING for details)

"""The :xfile:`models.py` file for `lino.modlib.reception`.

This injects three fields to :class:`cal.Guest
<lino.modlib.cal.models.Guest>` and defines three new states in
:class:`cal.GuestStates <lino.modlib.cal.models.GuestStates>`.


    state   ---action--> new state

    present ---checkin--> waiting
    waiting ---receive-->  busy
    busy    ---checkout--> gone


========================== ============== ============ ============
What                       waiting_since  busy_since   gone_since
========================== ============== ============ ============
Visitor checks in          X
Agent receives the visitor X              X
Visitor leaves             X              X            X
========================== ============== ============ ============

"""
from builtins import str

import logging
logger = logging.getLogger(__name__)

import datetime


from django.db import models
from django.db.models import Q
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.contrib.humanize.templatetags.humanize import naturaltime


from lino.modlib.users.mixins import My

from lino.utils.xmlgen.html import E
from lino.utils import join_elems

from lino.api import dd, rt

cal = dd.resolve_app('cal')
system = dd.resolve_app('system')

from lino.modlib.cal.workflows import GuestStates, EventStates
from lino.modlib.office.roles import OfficeUser, OfficeOperator

# lino.modlib.reception requires the `feedback` workflow. Before
# adding new GuestStates, make sure that
# `lino.modlib.cal.workflows.feedback` has been imported because this
# will clear GuestStates

import lino.modlib.cal.workflows.feedback

add = GuestStates.add_item
add('44', _("Waiting"), 'waiting')
add('45', _("Busy"), 'busy')
add('46', _("Gone"), 'gone')


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
            raise Warning(
                _("The event type for prompt events may not invite client!"))

#~ dd.inject_field('cal.Event','is_prompt',
    #~ models.BooleanField(_("Prompt event"),default=False))


def create_prompt_event(
        project, partner, user, summary, guest_role, now=None):
    """
    Create a "prompt event".
    """
    ekw = dict(project=project)
    today = settings.SITE.today()
    ekw.update(start_date=today)
    ekw.update(end_date=today)
    ekw.update(event_type=settings.SITE.site_config.prompt_calendar)
    ekw.update(state=EventStates.published)
    ekw.update(user=user)
    if summary:
        ekw.update(summary=summary)
    event = rt.modules.cal.Event(**ekw)
    event.save()
    if now is None:
        now = timezone.now()
    rt.modules.cal.Guest(
        event=event,
        partner=partner,
        state=rt.modules.cal.GuestStates.waiting,
        role=guest_role,
        #~ role=settings.SITE.site_config.client_guestrole,
        waiting_since=now
    ).save()
    #~ event.full_clean()
    #~ print 20130722, ekw, ar.action_param_values.user, ar.get_user()
    return event


class CheckinVisitor(dd.NotifyingAction):
    """The "Checkin" action on a :class:`Guest
    <lino.modlib.cal.models_guest.Guest>`.

    """
    label = _("Checkin")
    help_text = _("Mark this visitor as arrived")
    show_in_workflow = True
    show_in_bbar = False

    required_roles = dd.required((OfficeUser, OfficeOperator))
    required_states = 'invited accepted present'

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
        obj = ar.selected_rows[0]  # a cal.Guest instance

        def doit(ar2):
            obj.waiting_since = timezone.now()
            obj.state = GuestStates.waiting
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


class MyVisitorAction(dd.Action):
    readonly = False

    def get_action_permission(self, ar, obj, state):
        me = ar.get_user()
        if obj.event.user != me \
           and not me.profile.has_required_roles([OfficeOperator]):
            return False
        return super(MyVisitorAction, self).get_action_permission(
            ar, obj, state)


class ReceiveVisitor(MyVisitorAction):
    """The "Receive" action on a :class:`Guest
    <lino.modlib.cal.models_guest.Guest>`.

    """
    label = _("Receive")
    help_text = _("Visitor was received by agent")
    show_in_workflow = True
    show_in_bbar = False
    required_states = 'waiting'

    def run_from_ui(self, ar, **kw):
        obj = ar.selected_rows[0]

        def ok(ar):
            obj.state = GuestStates.busy
            obj.busy_since = timezone.now()

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


def checkout_guest(obj, ar):
    """Check a guest out. This sets the :attr:`gone_since` timestamp to
    now and the `state` to `gone`.

    If :attr:`busy_since` is empty, set it to :attr:`gone_since`.

    If the related event has no `end_time`, also set this.

    """
    if obj.gone_since:
        if ar is not None:
            ar.info("Cannot checkout_guest because gone_since is not empty.")
    obj.gone_since = timezone.now()
    if obj.busy_since is None:
        obj.busy_since = obj.gone_since
    if not obj.event.end_time:
        if ar is not None:
            ar.info("event.end_time has been set")
        obj.event.end_time = obj.gone_since
        obj.event.full_clean()
        obj.event.save()

    obj.state = GuestStates.gone
    obj.full_clean()
    obj.save()


class CheckoutVisitor(MyVisitorAction):
    """The "Checkout" action on a :class:`Guest
    <lino.modlib.cal.models_guest.Guest>`.

    """
    label = _("Checkout")
    help_text = _("Visitor left the centre")
    show_in_workflow = True
    show_in_bbar = False
    required_states = 'busy waiting'

    def run_from_ui(self, ar, **kw):
        obj = ar.selected_rows[0]

        def ok(ar2):
            checkout_guest(obj, ar)
            kw.update(refresh=True)
            ar2.success(**kw)

        msg = _("%(guest)s leaves after meeting with %(user)s.") % dict(
            guest=obj.partner, user=obj.user)
        ar.confirm(ok, msg, _("Are you sure?"))


@dd.receiver(dd.pre_analyze)
def my_guest_workflows(sender=None, **kw):
    Guest = rt.modules.cal.Guest

    Guest.checkin = CheckinVisitor(sort_index=100)
    Guest.receive = ReceiveVisitor(sort_index=101)
    Guest.checkout = CheckoutVisitor(sort_index=102)

    GuestStates.excused.add_transition(
        required_states='invited accepted absent')
    GuestStates.absent.add_transition(
        required_states='accepted excused')
    GuestStates.present.add_transition(
        required_states='invited accepted')


class AppointmentsByPartner(dd.Table):
    """Show the participations in upcoming calendar events for a given
    partner.

    TODO: rename this to `GuestsByPartner` or
    `ParticipationsByPartner` and add filter parameters.

    """
    label = _("Appointments")
    model = 'cal.Guest'
    master_key = 'partner'
    column_names = 'event__when_text event__user workflow_buttons'
    editable = False
    auto_fit_column_widths = True
    variable_row_height = True
    order_by = ['event__start_date', 'event__start_time']

    @classmethod
    def get_request_queryset(self, ar):
        # logger.info("20121010 Clients.get_request_queryset %s",ar.param_values)
        qs = super(AppointmentsByPartner, self).get_request_queryset(ar)
        if isinstance(qs, list):
            return qs
        start_date = settings.SITE.today() - datetime.timedelta(days=17)
        # end_date = settings.SITE.today() + datetime.timedelta(days=17)
        # qs = qs.filter(event__start_date__gte=start_date,
        #                event__start_date__lte=end_date)
        qs = qs.filter(event__start_date__gte=start_date)
        return qs


# ExpectedGuestsStates = (GuestStates.invited, GuestStates.accepted)


class ExpectedGuests(cal.Guests):
    """General table of all expected guests."""
    label = _("Expected Guests")
    help_text = _("Consult this table when checking in a partner who \
    has an appointment.")
    # filter = Q(waiting_since__isnull=True,
    #            state__in=ExpectedGuestsStates)
    column_names = 'partner event__user event__summary workflow_buttons \
    waiting_since busy_since'
    hidden_columns = 'waiting_since busy_since'
    #~ checkin = CheckinGuest()
    required_roles = dd.required(OfficeOperator)

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
        required_roles = dd.required(OfficeUser)
        auto_fit_column_widths = True

        @dd.displayfield(_('Since'))
        def since(self, obj, ar):
            # *received since* == *waiting until*
            return naturaltime(obj.busy_since)


# class ReceptionUser(SiteUser):
#     ored_roles = (OfficeUser(), OfficeOperator())
#     def satisfies(self, required_role):
#         is isinstance(OfficeUser, OfficeOperator

class Visitors(cal.Guests):
    """Common base class for the following tables:

    ========================== ============================
    :class:`WaitingVisitors`   :class:`MyWaitingVisitors`
    :class:`BusyVisitors`      :class:`MyBusyVisitors`
    :class:`GoneVisitors`      :class:`MyGoneVisitors`
    ========================== ============================

    No subclass should be editable because deleting would leave the
    useless cal.Event.

    """
    # debug_permissions = 20150227

    required_roles = dd.required((OfficeUser, OfficeOperator))
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



class BusyVisitors(Visitors):
    """Show busy visitors (with any user)."""
    label = _("Busy visitors")
    help_text = _("Shows the visitors who are busy with some agent.")
    visitor_state = GuestStates.busy
    order_by = ['busy_since']

    @dd.displayfield(_('Since'))
    def since(self, obj, ar):
        return naturaltime(obj.busy_since)


class WaitingVisitors(Visitors):
    """Show waiting visitors (for any user)."""
    label = _("Waiting visitors")
    help_text = _("Shows the visitors in the waiting room.")
    column_names = ('since partner event__user position '
                    'event__summary workflow_buttons')
    visitor_state = GuestStates.waiting

    order_by = ['waiting_since']

    @dd.displayfield(_('Since'))
    def since(self, obj, ar):
        return naturaltime(obj.waiting_since)

    @dd.displayfield(
        _('Position'), help_text=_("Position in waiting queue (per agent)"))
    def position(self, obj, ar):
        n = 1 + rt.modules.cal.Guest.objects.filter(
            #~ waiting_since__isnull=False,
            #~ busy_since__isnull=True,
            state=GuestStates.waiting,
            event__user=obj.event.user,
            waiting_since__lt=obj.waiting_since).count()
        return str(n)


class GoneVisitors(Visitors):
    """Show gone visitors (for any user)."""
    label = _("Gone visitors")
    help_text = _("Shows the visitors who have gone.")
    visitor_state = GuestStates.gone
    order_by = ['-gone_since']

    @dd.displayfield(_('Since'))
    def since(self, obj, ar):
        return naturaltime(obj.gone_since)


class MyWaitingVisitors(My, WaitingVisitors):
    """Show visitors waiting for me."""
    required_roles = dd.required(OfficeUser)
    label = _("Visitors waiting for me")
    column_names = ('since partner position '
                    'event__summary workflow_buttons')


class MyBusyVisitors(My, BusyVisitors):
    """Show the visitors with whom I am busy."""
    required_roles = dd.required(OfficeUser)
    label = _("Visitors busy with me")


class MyGoneVisitors(My, GoneVisitors):
    """Show my visitors who have gone."""
    required_roles = dd.required(OfficeUser)
    label = _("My gone visitors")


