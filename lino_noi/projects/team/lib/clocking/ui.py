# -*- coding: UTF-8 -*-
# Copyright 2016 Luc Saffre
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
"""User interface for this plugin.


"""

from lino_noi.lib.clocking.ui import *
from lino.api import _


from lino_noi.lib.tickets.models import Project
from lino_noi.lib.tickets.models import Ticket
from lino_noi.lib.clocking.roles import Worker


MySessionsByDate.column_names = (
    'start_time end_time break_time duration summary ticket '
    'ticket__project workflow_buttons *')


class WorkedHours(dd.VentilatingTable):
    """A table showing one row per day with a summary view of the sesions
    on that day."""
    required_roles = dd.required(Worker)
    label = _("Worked hours")
    hide_zero_rows = True
    parameters = ObservedPeriod(
        user=dd.ForeignKey('users.User', null=True, blank=True))
    params_layout = "start_date end_date user"
    # editable = False
    auto_fit_column_widths = True

    class Row(object):
        def __init__(self, ar, day):
            self.day = day
            self._root2tot = {}
            self._tickets = set()
            grand_tot = Duration()
            pv = dict(start_date=day, end_date=day)
            pv.update(observed_event=dd.PeriodEvents.started)
            pv.update(user=ar.param_values.user)
            self.sar = ar.spawn(MySessionsByDate, param_values=pv)
            for ses in self.sar:
                self._tickets.add(ses.ticket)
                d = ses.get_duration() or MIN_DURATION
                grand_tot += d
                root = ses.get_root_project()
                if root is not None:
                    tot = self._root2tot.get(root, Duration()) + d
                    self._root2tot[root] = tot
    
            self._root2tot[None] = grand_tot

        def __unicode__(self):
            return when_text(self.day)

    @dd.displayfield(_("Description"))
    def description(self, obj, ar):
        # pv = dict(start_date=obj.day, end_date=obj.day)
        # pv.update(observed_event=dd.PeriodEvents.active)
        # pv.update(user=ar.param_values.user)
        # sar = ar.spawn(MySessionsByDate, param_values=pv)
        elems = [obj.sar.ar2button(label=unicode(obj))]
        tickets = [
            ar.obj2html(t, "#{0}".format(t.id), title=t.summary)
            for t in obj._tickets]
        if len(tickets) > 0:
            elems.append(" (")
            elems += join_elems(tickets, ', ')
            elems.append(")")
        return E.p(*elems)

    @classmethod
    def get_data_rows(cls, ar):
        pv = ar.param_values
        start_date = pv.start_date or dd.today(-7)
        end_date = pv.end_date or dd.today(7)
        d = end_date
        while d > start_date:
            yield cls.Row(ar, d)
            d -= ONE_DAY

    @dd.displayfield("Date")
    def date(cls, row, ar):
        return dd.fdl(row.day)

    @classmethod
    def param_defaults(cls, ar, **kw):
        kw = super(WorkedHours, cls).param_defaults(ar, **kw)
        kw.update(start_date=dd.today(-7))
        kw.update(end_date=dd.today())
        kw.update(user=ar.get_user())
        return kw

    @classmethod
    def get_ventilated_columns(cls):
        Project = rt.modules.tickets.Project

        def w(prj, verbose_name):
            # return a getter function for a RequestField on the given
            # EntryType.

            def func(fld, obj, ar):
                return obj._root2tot.get(prj, None)

            return dd.VirtualField(dd.DurationField(verbose_name), func)

        for p in Project.objects.filter(parent__isnull=True).order_by('ref'):
            yield w(p, unicode(p))
        yield w(None, _("Total"))


class OtherTicketsByMilestone(Tickets, InvestedTime):
    """Print a table with tickets that are not explicitly deployed but
    which have been worked on and which are interesting for this site.

    """
    column_names = "id my_description state invested_time"
    master = 'deploy.Milestone'
    label = _("Other tickets")
    
    @classmethod
    def get_request_queryset(self, ar):
        mi = ar.master_instance
        if mi is None:
            return

        if not mi.changes_since:
            return

        spv = dict()
        end_date = mi.reached or mi.expected or dd.today()
        spv.update(start_date=mi.changes_since, end_date=end_date)
        spv.update(interesting_for=mi.site.partner)
        spv.update(observed_event=TicketEvents.clocking)
        ar.param_values.update(spv)

        qs = super(OtherTicketsByMilestone, self).get_request_queryset(ar)

        explicit = rt.models.deploy.Deployment.objects.filter(
            milestone=mi).values_list('ticket_id', flat=True)
        qs = qs.exclude(id__in=explicit)
        for obj in qs:
            obj._invested_time = compute_invested_time(
                obj, start_date=mi.changes_since, end_date=end_date)
            yield obj

    @classmethod
    def get_title_base(self, ar):
        """
        """
        title = self.title or self.label
        mi = ar.master_instance
        if mi is None:
            return title
        if mi.changes_since:
            return _("Changes since {0}").format(dd.fds(mi.changes_since))
        # end_date = mi.reached or mi.expected or dd.today()
        # return _("Changes before {0}").format(dd.fds(end_date))
        return title


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
        spv = mi.get_tickets_parameters()
        # spv = dict(start_date=mi.start_date, end_date=mi.end_date)
        spv.update(observed_event=TicketEvents.clocking)
        # spv.update(interesting_for=mi.interesting_for)
        # if mi.ticket_state:
        #     spv.update(state=mi.ticket_state)
        ar.param_values.update(spv)

        qs = super(TicketsByReport, self).get_request_queryset(ar)
        for obj in qs:
            obj._invested_time = compute_invested_time(
                obj, start_date=mi.start_date, end_date=mi.end_date,
                user=mi.user)
            yield obj


class ProjectsByReport(Projects, InvestedTime):
    """The list of projects mentioned in a service report.
    
    """
    master = 'clocking.ServiceReport'
    column_names = "ref name parent active_tickets invested_time total_time"
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
            spv = mi.get_tickets_parameters(**spv)
            spv.update(observed_event=TicketEvents.clocking)
            sar = Tickets.request(param_values=spv)
            for ticket in sar:
                ttot = compute_invested_time(
                    ticket, start_date=mi.start_date, end_date=mi.end_date,
                    user=mi.user)
                if ttot:
                    tot += ttot
                    tickets.append(ticket)
            return tot, tickets

        projects_list = []
        children_time = {}

        qs = super(ProjectsByReport, self).get_request_queryset(ar)
        for prj in qs:
            tot, tickets = worked_time(project=prj)
            prj._tickets = tickets
            prj._invested_time = tot
            projects_list.append(prj)
            if tot:
                p = prj.parent
                while p is not None:
                    cht = children_time.get(p.id, Duration())
                    children_time[p.id] = cht + tot
                    p = p.parent

        # compute children_time for each project
        for prj in projects_list:
            prj._children_time = children_time.get(prj.id, Duration())
            # p = prj.parent
            # ct = Duration()
            # while p is not None:
            #     ct += children_time.get(p.id, Duration())

        # remove projects that have no time at all
        def f(prj):
            return prj._invested_time or prj._children_time
        projects_list = filter(f, projects_list)

        # add an unsaved Project for the tickets without project:
        tot, tickets = worked_time(has_project=dd.YesNo.no)
        if tot:
            prj = rt.modules.tickets.Project(name="(no project)")
            prj._tickets = tickets
            prj._invested_time = tot
            prj._children_time = Duration()
            projects_list.append(prj)
        return projects_list

    @dd.displayfield(_("Tickets"))
    def active_tickets(cls, obj, ar):
        lst = []
        for ticket in obj._tickets:
            lst.append(ar.obj2html(
                ticket, text="#%d" % ticket.id, title=unicode(ticket)))
        return E.p(*join_elems(lst, ', '))

    @dd.displayfield(_("Total time"))
    def total_time(cls, obj, ar):
        tt = obj._invested_time + obj._children_time
        return E.p(str(tt))


class ServiceReports(dd.Table):
    """List of service reports."""
    required_roles = dd.required(Worker)

    model = "clocking.ServiceReport"
    # detail_layout = """
    # start_date end_date user interesting_for ticket_state printed
    # TicketsByReport
    # ProjectsByReport
    # """
    column_names = "start_date end_date user interesting_for "\
                   "ticket_state printed *"

    params_panel_hidden = True
    


class ReportsByPartner(ServiceReports):
    """List of service reports issued for a given site."""
    master_key = 'interesting_for'


@dd.receiver(dd.post_save, sender=Project)
def my_setup_columns(sender, **kw):
    WorkedHours.setup_columns()
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

