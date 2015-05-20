# -*- coding: UTF-8 -*-
# Copyright 2011-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""Database models for `lino.modlib.clocking`.

A **Session** is when an employee (a User) works during a given lapse
of time on a given Ticket.

All the Sessions related to a given Project represent the time
invested into that Project.

Extreme case of a session:

- I start to work on an existing ticket #1 at 9:23.  A customer phones
  at 10:17 with a question. Created #2.  That call is interrupted
  several times (by the customer himself).  During the first
  interruption another customer calls, with another problem (ticket
  #3) which we solve together within 5 minutes.  During the second
  interruption of #2 (which lasts 7 minutes) I make a coffee break.

  During the third interruption I continue to analyze the customer's
  problem.  When ticket #2 is solved, I decided that it's not worth to
  keep track of each interruption and that the overall session time
  for this ticket can be estimated to 0:40.

  ::

    Ticket start end    Pause  Duration
    #1     9:23  13:12  0:45
    #2     10:17 11:12  0:12       0:43   
    #3     10:23 10:28             0:05

"""

import datetime
from collections import OrderedDict

from django.conf import settings
from django.db import models
from django.db.models import Q, Count

from lino import mixins
from lino.api import dd, rt, _

from lino.utils import ONE_DAY
from lino.utils.xmlgen.html import E
from lino.utils.quantities import Duration

from lino.modlib.cal.mixins import StartedEnded
from lino.modlib.cal.utils import when_text
from lino.modlib.users.mixins import ByUser, UserAuthored

from lino.modlib.tickets.choicelists import TicketEvents, ObservedEvent


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


class SessionType(mixins.BabelNamed):
    """The type of a :class:`Session`.
    """

    class Meta:
        verbose_name = _("Session Type")
        verbose_name_plural = _('Session Types')


class SessionTypes(dd.Table):
    model = 'clocking.SessionType'
    column_names = 'name *'


class EndSession(dd.Action):
    """To close a session means to stop working on that ticket for this time.

    """
    label = _("End session")
    help_text = _("Stop time-tracking this session.")
    # icon_name = 'emoticon_smile'
    show_in_workflow = True
    # show_in_bbar = False

    def get_action_permission(self, ar, obj, state):
        if obj.end_time:
            return False
        return super(EndSession,
                     self).get_action_permission(ar, obj, state)

    def run_from_ui(self, ar, **kw):

        def ok(ar2):
            now = datetime.datetime.now()
            for obj in ar.selected_rows:
                obj.set_datetime('end', now)
                # obj.end_date = dd.today()
                # obj.end_time = now.time()
                obj.save()
                obj.ticket.touch()
                obj.ticket.save()
                ar2.set_response(refresh=True)

        if True:
            ok(ar)
        else:
            msg = _("Close {0} sessions.").format(len(ar.selected_rows))
            ar.confirm(ok, msg, _("Are you sure?"))


class EndTicketSession(dd.Action):
    # label = _("End session")
    # label = u"\u231a\u2198"
    label = u"\u2198"
    help_text = _("End the active session on this ticket.")
    show_in_workflow = True
    show_in_bbar = False
    
    def get_action_permission(self, ar, obj, state):
        Session = rt.modules.clocking.Session
        qs = Session.objects.filter(
            user=ar.get_user(), ticket=obj, end_time__isnull=True)
        if qs.count() == 0:
            return False
        return super(EndTicketSession, self).get_action_permission(
            ar, obj, state)

    def run_from_ui(self, ar, **kw):
        Session = rt.modules.clocking.Session
        ses = Session.objects.get(
            user=ar.get_user(), ticket=ar.selected_rows[0],
            end_time__isnull=True)
        ses.set_datetime('end', datetime.datetime.now())
        ses.full_clean()
        ses.save()
        ar.set_response(refresh=True)


class StartTicketSession(dd.Action):
    # label = _("Start session")
    # label = u"\u262d"
    #label = u"\u2692"
    # label = u"\u2690"
    # label = u"\u2328"
    # label = u"\u231a\u2197"
    label = u"\u2197"

    help_text = _("Start a session on this ticket.")
    # icon_name = 'emoticon_smile'
    show_in_workflow = True
    show_in_bbar = False

    # parameters = dict(
    #     summary=models.CharField(_("Summary"), blank=True, max_length=200),
    #     session_type=dd.ForeignKey(
    #         'clocking.SessionType', null=True, blank=True)
    # )

    # params_layout = """
    # summary
    # session_type
    # """

    def get_action_permission(self, ar, obj, state):
        if obj.standby or obj.closed:
            return False
        Session = rt.modules.clocking.Session
        qs = Session.objects.filter(
            user=ar.get_user(), ticket=obj, end_time__isnull=True)
        if qs.count():
            return False
        return super(StartTicketSession, self).get_action_permission(
            ar, obj, state)

    def run_from_ui(self, ar, **kw):
        me = ar.get_user()
        obj = ar.selected_rows[0]

        ses = rt.modules.clocking.Session(ticket=obj, user=me)
        ses.full_clean()
        ses.save()
        ar.set_response(refresh=True)


dd.inject_action("tickets.Ticket", start_session=StartTicketSession())
dd.inject_action("tickets.Ticket", end_session=EndTicketSession())


class Session(UserAuthored, StartedEnded):
    """
    A Session is when a user works on a given ticket.
    """
    class Meta:
        verbose_name = _("Session")
        verbose_name_plural = _('Sessions')

    ticket = dd.ForeignKey(
        'tickets.Ticket', related_name="sessions_by_ticket")
    session_type = dd.ForeignKey('clocking.SessionType', null=True, blank=True)
    summary = models.CharField(
        _("Summary"), max_length=200, blank=True,
        help_text=_("Summary of the session."))
    description = dd.RichTextField(_("Description"), blank=True)
    # break_time = models.TimeField(
    #     blank=True, null=True,
    #     verbose_name=_("Break Time"))
    break_time = dd.DurationField(_("Break Time"), blank=True)

    end_session = EndSession()

    def __unicode__(self):
        if self.start_time and self.end_time:
            return u"%s %s-%s" % (
                self.start_date.strftime(settings.SITE.date_format_strftime),
                self.start_time.strftime(settings.SITE.time_format_strftime),
                self.end_time.strftime(settings.SITE.time_format_strftime))
        return "%s # %s" % (self._meta.verbose_name, self.pk)

    def save(self, *args, **kwargs):
        if not settings.SITE.loading_from_dump:
            if self.start_date is None:
                self.start_date = dd.today()
            if self.start_time is None:
                self.start_time = datetime.datetime.now().time()
        super(Session, self).save(*args, **kwargs)

    def get_duration(self):
        diff = super(Session, self).get_duration()
        if diff is not None and self.break_time is not None:
            diff -= self.break_time
        return diff
        
        # if self.end_time is None:
        #     diff = datetime.timedelta()
        # else:
        #     diff = self.get_datetime('end') - self.get_datetime('start')
        #     if self.break_time is not None:
        #         diff -= self.break_time
        # return Duration(diff)

dd.update_field(Session, 'user', blank=False, nul=False)


class Sessions(dd.Table):
    model = 'clocking.Session'
    column_names = 'ticket start_date start_time end_date end_time '\
                   'break_time summary user *'
    order_by = ['-start_date', '-start_time']
    # order_by = ['start_date', 'start_time']
    # stay_in_grid = True
    parameters = mixins.ObservedPeriod(
        project=dd.ForeignKey('tickets.Project', blank=True),
        observed_event=dd.PeriodEvents.field(
            blank=True, default=dd.PeriodEvents.active),
    )
    params_layout = "start_date end_date observed_event project"
    auto_fit_column_widths = True

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

        # if pv.start_date:
        #     if pv.end_date:
        #         qs = qs.filter(start_date__gte=pv.start_date)
        #     else:
        #         qs = qs.filter(start_date=pv.start_date)
        # if pv.end_date:
        #     qs = qs.filter(end_date__lte=pv.end_date)
        # print 20150421, qs.query
        return qs


class SessionsByTicket(Sessions):
    master_key = 'ticket'
    column_names = 'start_date summary start_time end_time  '\
                   'break_time duration user *'


class MySessions(Sessions, ByUser):
    column_names = 'start_date start_time end_time break_time ticket summary *'


class MySessionsByDate(MySessions):
    order_by = ['start_date', 'start_time']
    label = _("My sessions by date")
    column_names = 'start_time end_time break_time duration ticket summary '\
                   'workflow_buttons *'

    # parameters = dict(
    #     today=models.DateField(_("Date"), blank=True),
    # )

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


def welcome_messages(ar):
    """Yield messages for the welcome page."""

    Session = rt.modules.clocking.Session
    Ticket = rt.modules.tickets.Ticket
    TicketStates = rt.modules.tickets.TicketStates
    me = ar.get_user()

    busy_tickets = set()
    # your open sessions (i.e. those you are busy with)
    qs = Session.objects.filter(user=me, end_time__isnull=True)
    if qs.count() > 0:
        chunks = [unicode(_("You are busy with "))]
        sep = None
        for ses in qs:
            if sep:
                chunks.append(sep)
            busy_tickets.add(ses.ticket.id)
            txt = unicode(ses.ticket)
            chunks.append(
                ar.obj2html(ses.ticket, txt, title=ses.ticket.summary))
            chunks += [
                ' (',
                ar.instance_action_button(ses.end_session, u'\u2713'),
                ')']
            sep = ', '
        chunks.append('. ')
        yield E.span(*chunks)
        # return

    if False:
        # Tickets in "favourite" states get their own welcome message.
        qs = Ticket.objects.filter(
            Q(assigned_to__isnull=True) | Q(assigned_to=me))
        qs = qs.filter(state__in=TicketStates.favorite_states)
        qs = qs.filter(closed=False, standby=False)
        qs = qs.exclude(id__in=busy_tickets)
        qs = qs.order_by('-modified')
        if qs.count() > 0:
            od = OrderedDict()  # state -> list of tickets
            for ticket in qs:
                lst = od.setdefault(ticket.state, [])
                if len(lst) < 10:
                    txt = unicode(ticket)
                    # txt = "#{0}".format(ticket.id)
                    # if ticket.nickname:
                    #     txt += u" ({0})".format(ticket.nickname)
                    lst.append(ar.obj2html(ticket, txt, title=ticket.summary))
                elif len(lst) == 10:
                    lst.append('...')
            items = []
            for state, tickets in od.items():
                chunks = ["{0} : ".format(state)]
                sep = None
                for ticket in tickets:
                    if sep:
                        chunks.append(sep)
                    chunks.append(ticket)
                    sep = ', '
                # chunks.append('. ')
                items.append(E.li(*chunks))
            yield _("Your favourite tickets are:")
            yield E.ul(*items)
            # yield E.div(E.p(_("You might want to work on")), E.ul(*items))

dd.add_welcome_handler(welcome_messages)


# class DurationsByUser(dd.VirtualTable):
#     master = 'users.User'

class InvestedTimes(dd.VentilatingTable):
    required = dd.Required()
    label = _("Hours worked")
    hide_zero_rows = True
    parameters = mixins.ObservedPeriod()
    params_layout = "start_date end_date"
    # editable = False
    auto_fit_column_widths = True

    class Row(object):
        def __init__(self, day):
            self.day = day

        def __unicode__(self):
            return when_text(self.day)

    # @dd.virtualfield(models.CharField(_("Description"), max_length=30))
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
                sar = Sessions.request(param_values=pv)
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

from lino.modlib.tickets.models import Project


@dd.receiver(dd.post_save, sender=Project)
def my_setup_columns(sender, **kw):
    InvestedTimes.setup_columns()
    settings.SITE.kernel.must_build_site_cache()


if False:  # works, but is not useful

    def weekly_reporter(days, ar, start_date, end_date):
        Session = rt.modules.clocking.Session
        me = ar.get_user()
        qs = Session.objects.filter(
            user=me, start_date__gte=start_date, end_date__lte=end_date)
        # print 20150420, start_date, end_date, qs
        d2p = dict()
        for ses in qs:
            prj = ses.ticket.project
            if prj is not None:
                while prj.parent is not None:
                    prj = prj.parent
            projects = d2p.setdefault(ses.start_date, dict())
            duration = projects.setdefault(prj, Duration())
            #datetime.timedelta())
            duration += ses.get_duration()
            projects[prj] = duration

        # print 20150420, d2p
        def fmt(delta):
            return str(Duration(delta))

        for date, projects in d2p.items():
            parts = []
            tot = Duration()
            for prj, duration in projects.items():
                if prj is None:
                    prj = "N/A"
                txt = "{0} ({1})".format(prj, fmt(duration))
                parts.append(txt)
                tot += duration
            if len(parts):
                if len(parts) == 1:
                    txt = parts[0]
                else:
                    txt = ', '.join(parts) + " = " + fmt(tot)
                txt = E.p(txt, style="text-align:right")
                days[date].append(txt)

    from lino.utils.weekly import add_reporter
    add_reporter(weekly_reporter)
