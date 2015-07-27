# -*- coding: UTF-8 -*-
# Copyright 2011-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""Tables for `lino.modlib.clocking`.

"""


from django.conf import settings
from django.db.models import Count

from lino.api import dd, rt, _

from lino.utils import ONE_DAY
from lino.utils.xmlgen.html import E, join_elems
from lino.utils.quantities import Duration
from lino.mixins import ObservedPeriod

from lino.modlib.cal.utils import when_text


from lino.modlib.tickets.choicelists import (TicketEvents,
                                             ProjectEvents, ObservedEvent)
from lino.modlib.tickets.ui import Tickets, Projects


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
    model = 'clocking.Session'
    column_names = 'ticket user start_date start_time end_date end_time '\
                   'break_time summary duration  *'
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
            blank=True, default=dd.PeriodEvents.active),
    )
    params_layout = "start_date end_date observed_event project "\
                    "user session_type ticket"
    auto_fit_column_widths = True
    simple_parameters = ('user', 'session_type', 'ticket')

    detail_layout = """
    ticket start_date start_time end_date end_time break_time user
    summary
    description
    """
    insert_layout = """
    ticket
    summary
    session_type
    """

    @classmethod
    def get_request_queryset(self, ar):
        qs = super(Sessions, self).get_request_queryset(ar)
        pv = ar.param_values
        ce = pv.observed_event
        if ce is not None:
            qs = ce.add_filter(qs, pv)

        if pv.project:
            l1 = Project.objects.filter(parent=pv.project)
            l2 = Project.objects.filter(parent__in=l1)
            l3 = Project.objects.filter(parent__in=l2)
            projects = set([pv.project])
            projects |= set(l1)
            projects |= set(l2)
            projects |= set(l3)
            # print 20150421, projects
            qs = qs.filter(ticket__project__in=projects)

        return qs


class SessionsByTicket(Sessions):
    master_key = 'ticket'
    column_names = 'start_date summary start_time end_time  '\
                   'break_time duration user *'


class MySessions(Sessions):
    column_names = 'start_date start_time end_time '\
                   'break_time ticket summary *'

    @classmethod
    def param_defaults(self, ar, **kw):
        kw = super(MySessions, self).param_defaults(ar, **kw)
        kw.update(user=ar.get_user())
        return kw


class MySessionsByDate(MySessions):
    order_by = ['start_date', 'start_time']
    label = _("My sessions by date")
    column_names = 'start_time end_time break_time duration ticket summary '\
                   'workflow_buttons *'

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


class InvestedTimes(dd.VentilatingTable):
    required_roles = dd.required()
    label = _("Hours worked")
    hide_zero_rows = True
    parameters = ObservedPeriod()
    params_layout = "start_date end_date"
    # editable = False
    auto_fit_column_widths = True

    class Row(object):
        def __init__(self, day):
            self.day = day

        def __unicode__(self):
            return when_text(self.day)

    @dd.displayfield(_("Description"))
    def description(self, obj, ar):
        pv = dict(start_date=obj.day, end_date=obj.day)
        pv.update(observed_event=dd.PeriodEvents.active)
        sar = ar.spawn(MySessionsByDate, param_values=pv)
        return sar.ar2button(label=unicode(obj))

    @classmethod
    def get_data_rows(cls, ar):
        pv = ar.param_values
        start_date = pv.start_date or dd.today(-7)
        end_date = pv.end_date or dd.today(7)
        # settings.SITE.ignore_dates_after
        d = end_date
        while d > start_date:
            yield cls.Row(d)
            d -= ONE_DAY

    @dd.displayfield("Date")
    def date(cls, row, ar):
        return dd.fdl(row.day)

    @classmethod
    def param_defaults(cls, ar, **kw):
        kw = super(InvestedTimes, cls).param_defaults(ar, **kw)
        kw.update(start_date=dd.today(-7))
        kw.update(end_date=dd.today())
        return kw

    @classmethod
    def get_ventilated_columns(self):
        Project = rt.modules.tickets.Project

        def w(prj, verbose_name):
            # return a getter function for a RequestField on the given
            # EntryType.

            def func(fld, obj, ar):
                pv = dict(start_date=obj.day, end_date=obj.day)
                pv.update(observed_event=dd.PeriodEvents.active)
                pv.update(project=prj)
                pv.update(user=ar.get_user())
                sar = MySessionsByDate.request(param_values=pv)
                tot = Duration()
                for obj in sar:
                    d = obj.get_duration()
                    if d is not None:
                        tot += d
                if tot:
                    return tot

            return dd.VirtualField(dd.DurationField(verbose_name), func)
        for p in Project.objects.filter(parent__isnull=True).order_by('ref'):
            yield w(p, unicode(p))
        yield w(None, _("Total"))




def compute_invested_time(obj, pv):
    spv = dict(start_date=pv.start_date, end_date=pv.end_date)
    spv.update(observed_event=dd.PeriodEvents.active)
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

    
class TicketsByReport(Tickets, InvestedTime):
    """The list of tickets mentioned in a service report."""
    master = 'clocking.ServiceReport'
    # column_names = "summary id reporter project product site state
    # invested_time"
    column_names = "id my_description state invested_time"
    order_by = ['id']

    @classmethod
    def get_request_queryset(self, ar):
        mi = ar.master_instance
        if mi is None:
            return
        spv = dict(start_date=mi.start_date, end_date=mi.end_date)
        spv.update(observed_event=TicketEvents.clocking)
        spv.update(interesting_for=mi.interesting_for)
        ar.param_values.update(spv)

        qs = super(TicketsByReport, self).get_request_queryset(ar)
        for obj in qs:
            obj._invested_time = compute_invested_time(obj, mi)
            yield obj

    @dd.displayfield(_("Description"))
    def my_description(cls, obj, ar):
        mi = ar.master_instance
        if mi is None:
            return
        lst = [obj.summary]
        tpl = u"{0}: {1}"
        if obj.site is not None and obj.site == mi.interesting_for:
            lst.append(_("site-specific"))
        if obj.reporter is not None:
            lst.append(tpl.format(
                unicode(_("Reporter")), unicode(obj.reporter)))
        if obj.project is not None:
            lst.append(tpl.format(
                unicode(_("Project")), unicode(obj.project)))
        if obj.product is not None:
            lst.append(tpl.format(
                unicode(_("Product")), unicode(obj.product)))
        return E.p(*join_elems(lst, '. '))


class ProjectsByReport(Projects, InvestedTime):
    """The list of projects mentioned in a service report."""
    master = 'clocking.ServiceReport'
    column_names = "ref name active_tickets invested_time"
    order_by = ['ref']

    @classmethod
    def get_request_queryset(self, ar):
        Tickets = rt.modules.tickets.Tickets
        mi = ar.master_instance
        if mi is None:
            return

        def worked_time(**spv):
            tot = Duration()
            tickets = []
            spv.update(start_date=mi.start_date, end_date=mi.end_date)
            spv.update(observed_event=TicketEvents.clocking)
            spv.update(interesting_for=mi.interesting_for)
            # spv.update(project=prj)
            sar = Tickets.request(param_values=spv)
            # for ticket in Ticket.objects.filter(project=prj):
            for ticket in sar:
                ttot = compute_invested_time(ticket, mi)
                if ttot:
                    tot += ttot
                    tickets.append(ticket)
            return tot, tickets

        qs = super(ProjectsByReport, self).get_request_queryset(ar)
        for prj in qs:
            tot, tickets = worked_time(project=prj)
            if tot:
                prj._tickets = tickets
                prj._invested_time = tot
                yield prj

        # add an unsaved project for the tickets without project:
        tot, tickets = worked_time(has_project=dd.YesNo.no)
        if tot:
            prj = rt.modules.tickets.Project(name="(no project)")
            prj._tickets = tickets
            prj._invested_time = tot
            yield prj

    @dd.displayfield(_("Tickets"))
    def active_tickets(cls, obj, ar):
        lst = []
        for ticket in obj._tickets:
            lst.append(ar.obj2html(
                ticket, text="#%d" % ticket.id, title=unicode(ticket)))
        return E.p(*join_elems(lst, ', '))


class ServiceReports(dd.Table):
    """List of service reports."""
    model = "clocking.ServiceReport"
    detail_layout = """
    start_date end_date interesting_for printed
    TicketsByReport
    ProjectsByReport
    """


class ReportsBySite(ServiceReports):
    """List of service reports issued for a given site."""
    master_key = 'interesting_for'


from lino.modlib.tickets.models import Project
from lino.modlib.tickets.models import Ticket


@dd.receiver(dd.post_save, sender=Project)
def my_setup_columns(sender, **kw):
    InvestedTimes.setup_columns()
    settings.SITE.kernel.must_build_site_cache()


@dd.receiver(dd.post_save, sender=Ticket)
def on_ticket_create(sender, instance=None, created=False, **kwargs):
    if settings.SITE.loading_from_dump:
        return
    me = instance.reporter
    if created and me is not None and me.open_session_on_new_ticket:
        ses = rt.modules.clocking.Session(ticket=instance, user=me)
        ses.full_clean()
        ses.save()

