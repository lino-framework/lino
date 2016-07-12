# -*- coding: UTF-8 -*-
# Copyright 2011-2016 Luc Saffre
#
# This file is part of Lino Noi.
#
# Lino Noi is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# Lino Noi is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with Lino Noi.  If not, see
# <http://www.gnu.org/licenses/>.


"""Tables for `lino_noi.lib.clocking`.

"""


from django.conf import settings
from django.db.models import Count

from lino.api import dd, rt, _

from lino.utils import ONE_DAY
from lino.utils.xmlgen.html import E, join_elems
from lino.utils.quantities import Duration
from lino.modlib.system.choicelists import ObservedEvent
from lino.mixins.periods import ObservedPeriod


from lino_xl.lib.cal.utils import when_text


from lino_noi.lib.tickets.choicelists import (TicketEvents,
                                              ProjectEvents, ObservedEvent)
from lino_noi.lib.tickets.ui import Tickets, Projects
from lino_noi.lib.tickets.roles import Worker

MIN_DURATION = Duration('0:01')


class TicketHasSessions(ObservedEvent):
    """Select only tickets for which there has been at least one session
    during the given period.

    """
    text = _("Has been worked on")

    def add_filter(self, qs, pv):
        if pv.start_date:
            qs = qs.filter(sessions_by_ticket__start_date__gte=pv.start_date)
        if pv.end_date:
            qs = qs.filter(sessions_by_ticket__end_date__lte=pv.end_date)
        qs = qs.annotate(num_sessions=Count('sessions_by_ticket'))
        qs = qs.filter(num_sessions__gt=0)
        return qs

TicketEvents.add_item_instance(TicketHasSessions("clocking"))


class ProjectHasSessions(ObservedEvent):
    """Select only projects for which there has been at least one session
    during the given period.

    """
    text = _("Has been worked on")

    def add_filter(self, qs, pv):
        if pv.start_date:
            qs = qs.filter(
                tickets_by_project__sessions_by_ticket__start_date__gte=
                pv.start_date)
        if pv.end_date:
            qs = qs.filter(
                tickets_by_project__sessions_by_ticket__end_date__lte=
                pv.end_date)
        qs = qs.annotate(num_sessions=Count(
            'tickets_by_project__sessions_by_ticket'))
        qs = qs.filter(num_sessions__gt=0)
        return qs

ProjectEvents.add_item_instance(ProjectHasSessions("clocking"))


class SessionTypes(dd.Table):
    model = 'clocking.SessionType'
    column_names = 'name *'


class Sessions(dd.Table):
    required_roles = dd.required(Worker)
    model = 'clocking.Session'
    column_names = 'ticket user start_date start_time end_date end_time '\
                   'break_time summary duration  *'

    detail_layout = """
    ticket:40 user:20 faculty:20
    start_date start_time end_date end_time break_time duration
    summary:60 workflow_buttons:20
    description
    """
    insert_layout = """
    ticket
    summary
    session_type
    """

    order_by = ['-start_date', '-start_time']
    # order_by = ['start_date', 'start_time']
    # stay_in_grid = True
    parameters = ObservedPeriod(
        project=dd.ForeignKey('tickets.Project', null=True, blank=True),
        ticket=dd.ForeignKey('tickets.Ticket', null=True, blank=True),
        # user=dd.ForeignKey('users.User', null=True, blank=True),
        session_type=dd.ForeignKey(
            'clocking.SessionType', null=True, blank=True),
        observed_event=dd.PeriodEvents.field(
            blank=True, default=dd.PeriodEvents.active.as_callable),
    )

    @classmethod
    def get_simple_parameters(cls):
        s = super(Sessions, cls).get_simple_parameters()
        s |= set(['session_type', 'ticket'])
        return s

    params_layout = "start_date end_date observed_event project "\
                    "user session_type ticket"
    auto_fit_column_widths = True

    @classmethod
    def get_request_queryset(self, ar):
        qs = super(Sessions, self).get_request_queryset(ar)
        pv = ar.param_values
        ce = pv.observed_event
        if ce is not None:
            qs = ce.add_filter(qs, pv)

        if pv.project:
            qs = qs.filter(ticket__project__in=pv.project.whole_clan())

        return qs


class SessionsByTicket(Sessions):
    """
    The "Sessions" panel in the detail of a ticket.

    .. attribute:: slave_summary

        This panel shows:

         
    """
    master_key = 'ticket'
    column_names = 'start_date summary start_time end_time  '\
                   'break_time duration user *'
    slave_grid_format = 'summary'

    @classmethod
    def get_slave_summary(self, obj, ar):
        if ar is None:
            return ''
        elems = []

        # Active sessions:
        active_sessions = []
        qs = rt.modules.clocking.Session.objects.filter(ticket=obj)
        tot = Duration()
        for ses in qs:
            d = ses.get_duration()
            if d is not None:
                tot += d
            if ses.end_time is None:
                txt = "{0} since {1}".format(ses.user, ses.start_time)
                lnk = ar.obj2html(ses, txt)
                sar = ses.end_session.request_from(ar)
                if sar.get_permission():
                    lnk = E.span(lnk, " ", sar.ar2button(ses))
                active_sessions.append(lnk)

        # elems.append(E.p(_("Total {0} hours.").format(tot)))
        elems.append(E.p(_("Total %s hours.") % tot))

        if len(active_sessions) > 0:
            elems.append(E.p(
                unicode(_("Active sessions")), ": ",
                *join_elems(active_sessions, ', ')))

        # Button for starting a session from ticket

        sar = obj.start_session.request_from(ar)
        # if ar.renderer.is_interactive and sar.get_permission():
        if sar.get_permission():
            btn = sar.ar2button(obj)
            elems += [E.p(btn)]
        
        return E.div(*elems)


class MySessions(Sessions):
    column_names = 'start_date start_time end_time '\
                   'break_time duration ticket summary *'

    @classmethod
    def param_defaults(self, ar, **kw):
        kw = super(MySessions, self).param_defaults(ar, **kw)
        kw.update(user=ar.get_user())
        return kw


class MySessionsByDate(MySessions):
    order_by = ['start_date', 'start_time']
    label = _("My sessions by date")
    column_names = (
        'start_time end_time break_time duration summary ticket '
        'workflow_buttons *')

    @classmethod
    def param_defaults(self, ar, **kw):
        kw = super(MySessionsByDate, self).param_defaults(ar, **kw)
        kw.update(start_date=dd.today())
        kw.update(end_date=dd.today())
        return kw

    @classmethod
    def create_instance(self, ar, **kw):
        kw.update(start_date=ar.param_values.start_date)
        return super(MySessions, self).create_instance(ar, **kw)


def compute_invested_time(obj, **spv):
    # spv = dict(start_date=pv.start_date, end_date=pv.end_date)
    spv.update(observed_event=dd.PeriodEvents.started)
    sar = SessionsByTicket.request(master_instance=obj, param_values=spv)
    tot = Duration()
    for obj in sar:
        d = obj.get_duration()
        if d is not None:
            tot += d
    return tot


class InvestedTime(dd.Table):
    @dd.virtualfield(dd.DurationField(_("Time")))
    def invested_time(cls, obj, ar):
        return obj._invested_time

    @dd.displayfield(_("Description"))
    def my_description(cls, obj, ar):
        mi = ar.master_instance
        if mi is None:
            return
        lst = [obj.summary]
        tpl = u"{0}: {1}"
        # if obj.site is not None and obj.site == mi.interesting_for:
        #     lst.append(_("site-specific"))
        if obj.site is not None:  # and obj.site != mi.interesting_for:
            lst.append(tpl.format(
                unicode(_("Site")), unicode(obj.site)))
        if obj.reporter is not None:
            lst.append(tpl.format(
                unicode(_("Reporter")), unicode(obj.reporter)))
        if obj.project is not None:
            lst.append(tpl.format(
                unicode(_("Project")), unicode(obj.project)))
        if obj.topic is not None:
            lst.append(tpl.format(
                unicode(_("Topic")), unicode(obj.topic)))
        return E.p(*join_elems(lst, '. '))


