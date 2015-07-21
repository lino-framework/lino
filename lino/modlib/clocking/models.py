# -*- coding: UTF-8 -*-
# Copyright 2011-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""Database models for `lino.modlib.clocking`.

A **Session** is when a user works during a given lapse of time on a
given Ticket.

All the sessions related to a given project represent the time
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

from django.conf import settings
from django.db import models

from lino import mixins
from lino.api import dd, rt, _

from lino.core.roles import SiteUser

from lino.utils.xmlgen.html import E
from lino.utils.quantities import Duration

from lino.mixins.periods import DatePeriod
from lino.modlib.cal.mixins import StartedEnded
from lino.modlib.users.mixins import UserAuthored
from lino.modlib.excerpts.mixins import Certifiable


class SessionType(mixins.BabelNamed):
    """The type of a :class:`Session`.
    """

    class Meta:
        verbose_name = _("Session Type")
        verbose_name_plural = _('Session Types')


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
    label = u"↘"  # u"\u2198"
    help_text = _("End the active session on this ticket.")
    show_in_workflow = True
    show_in_bbar = False
    required_roles = dd.login_required()
    
    def get_action_permission(self, ar, obj, state):
        # u = ar.get_user()
        # if not u.profile.has_required_roles([SiteUser]):
        #     # avoid query with AnonymousUser
        #     return False
        if not super(EndTicketSession, self).get_action_permission(
                ar, obj, state):
            return False
        Session = rt.modules.clocking.Session
        qs = Session.objects.filter(
            user=ar.get_user(), ticket=obj, end_time__isnull=True)
        if qs.count() == 0:
            return False
        return True

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
    label = u"↗"  # \u2197

    help_text = _("Start a session on this ticket.")
    # icon_name = 'emoticon_smile'
    show_in_workflow = True
    show_in_bbar = False

    def get_action_permission(self, ar, obj, state):
        if obj.standby or obj.closed:
            return False
        u = ar.get_user()
        if not u.profile.has_required_roles([SiteUser]):
            # avoid query with AnonymousUser
            return False
        Session = rt.modules.clocking.Session
        qs = Session.objects.filter(
            user=u, ticket=obj, end_time__isnull=True)
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
dd.inject_field(
    "users.User", 'open_session_on_new_ticket',
    models.BooleanField(_("Open session on new ticket"), default=False))


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

dd.update_field(
    Session, 'user', blank=False, null=False, verbose_name=_("Worker"))


def welcome_messages(ar):
    """Yield messages for the welcome page."""

    Session = rt.modules.clocking.Session
    # Ticket = rt.modules.tickets.Ticket
    # TicketStates = rt.modules.tickets.TicketStates
    me = ar.get_user()

    busy_tickets = set()
    # your open sessions (i.e. those you are busy with)
    qs = Session.objects.filter(user=me, end_time__isnull=True)
    if qs.count() > 0:
        chunks = [E.b(unicode(_("You are busy with ")))]
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
                ar.instance_action_button(
                    ses.end_session, EndTicketSession.label),
                ')']
            sep = ', '
        chunks.append('. ')
        yield E.p(*chunks)

dd.add_welcome_handler(welcome_messages)


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


class ServiceReport(Certifiable, DatePeriod):

    class Meta:
        verbose_name = _("Service Report")
        verbose_name_plural = _("Service Reports")

    interesting_for = dd.ForeignKey(
        'tickets.Site',
        verbose_name=_("Interesting for"),
        blank=True, null=True,
        help_text=_("Only tickets interesting for this site."))


from .ui import *
