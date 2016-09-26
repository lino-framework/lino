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


"""Database models for this plugin.

"""

# import datetime

from django.conf import settings
from django.db import models
from django.utils import timezone

from lino import mixins
from lino.api import dd, rt, _

from lino.utils.xmlgen.html import E
from lino.utils.quantities import Duration

from lino_xl.lib.cal.mixins import Started, Ended
from lino.modlib.users.mixins import UserAuthored

from .actions import EndThisSession, PrintActivityReport, EndTicketSession


class SessionType(mixins.BabelNamed):
    """The type of a :class:`Session`.
    """

    class Meta:
        app_label = 'clocking'
        verbose_name = _("Session Type")
        verbose_name_plural = _('Session Types')


class Session(UserAuthored, Started, Ended):
    """A **Session** is when a user works during a given lapse of time on
    a given Ticket.

    Extreme case of a session:

    - I start to work on an existing ticket #1 at 9:23.  A customer phones
      at 10:17 with a question. Created #2.  That call is interrupted
      several times (by the customer himself).  During the first
      interruption another customer calls, with another problem (ticket
      #3) which we solve together within 5 minutes.  During the second
      interruption of #2 (which lasts 7 minutes) I make a coffee break.

      During the third interruption I continue to analyze the
      customer's problem.  When ticket #2 is solved, I decided that
      it's not worth to keep track of each interruption and that the
      overall session time for this ticket can be estimated to 0:40.

      ::

        Ticket start end    Pause  Duration
        #1      9:23 13:12  0:45
        #2     10:17 11:12  0:12       0:43
        #3     10:23 10:28             0:05


    .. attribute:: start_time
    .. attribute:: end_time

    .. attribute:: break_time
    
       The time (in `hh:mm`) to remove from the duration resulting
       from the difference between :attr:`start_time` and
       :attr:`end_time`.

    .. attribute:: faculty

       The faculty that has been used during this session. On a new
       session this defaults to the needed faculty currently specified
       on the ticket.

    """
    class Meta:
        app_label = 'clocking'
        verbose_name = _("Session")
        verbose_name_plural = _('Sessions')
        abstract = dd.is_abstract_model(__name__, 'Session')

    ticket = dd.ForeignKey(
        dd.plugins.clocking.ticket_model,
        related_name="sessions_by_ticket")

    session_type = dd.ForeignKey(
        'clocking.SessionType', null=True, blank=True)
    summary = models.CharField(
        _("Summary"), max_length=200, blank=True,
        help_text=_("Summary of the session."))
    description = dd.RichTextField(_("Description"), blank=True)
    # break_time = models.TimeField(
    #     blank=True, null=True,
    #     verbose_name=_("Break Time"))
    break_time = dd.DurationField(_("Break Time"), blank=True, null=True)
    faculty = dd.ForeignKey(
        'faculties.Faculty', related_name="sessions_by_faculty",
        blank=True, null=True)

    end_session = EndThisSession()
    # print_activity_report = PrintActivityReport()

    def __unicode__(self):
        if self.start_time and self.end_time:
            return u"%s %s-%s" % (
                self.start_date.strftime(settings.SITE.date_format_strftime),
                self.start_time.strftime(settings.SITE.time_format_strftime),
                self.end_time.strftime(settings.SITE.time_format_strftime))
        return "%s # %s" % (self._meta.verbose_name, self.pk)

    def full_clean(self, *args, **kwargs):
        if not settings.SITE.loading_from_dump:
            if self.start_time is None:
                self.set_datetime('start', timezone.now())
                # value = timezone.now()
                # if pytz:
                #     tz = pytz.timezone(self.get_timezone())
                #     value = value.astimezone(tz)
                # self.start_time = value.time()
            if self.start_date is None:
                self.start_date = dd.today()
            if self.ticket_id is not None and self.faculty_id is None:
                self.faculty = self.ticket.faculty
        super(Session, self).full_clean(*args, **kwargs)

    def unused_save(self, *args, **kwargs):
        if not settings.SITE.loading_from_dump:
            if self.start_date is None:
                self.start_date = dd.today()
            if self.start_time is None:
                self.start_time = timezone.now().time()
        super(Session, self).save(*args, **kwargs)

    def get_root_project(self):
        """Return the root project for this session (or None if session has no
        ticket).

        """
        if self.ticket and self.ticket.project:
            return self.ticket.project.get_parental_line()[0]

    def get_duration(self):
        """Return the duration in hours as a
        :class:`lino.utils.quantities.Quantity`.  This inherits from
        :meth:`StartedEnded
        <lino_xl.lib.cal.mixins.StartedEnded.get_duration>` but
        removes :attr:`break_time` if specified.

        """
        diff = super(Session, self).get_duration()
        if diff and self.break_time:
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


from .ui import *
