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

from django.conf import settings
from django.db import models

from lino import mixins
from lino.api import dd, rt, _

from lino.utils.xmlgen.html import E
from lino.modlib.cal.mixins import Started, Ended
from lino.modlib.users.mixins import ByUser, UserAuthored


class SessionType(mixins.BabelNamed):

    "Deserves more documentation."

    class Meta:
        verbose_name = _("Session Type")
        verbose_name_plural = _('Session Types')


class SessionTypes(dd.Table):
    model = 'clocking.SessionType'
    column_names = 'name *'


class Session(UserAuthored, Started, Ended):

    """
    A Session is when a user works on a given ticket.
    """
    class Meta:
        verbose_name = _("Session")
        verbose_name_plural = _('Sessions')

    ticket = dd.ForeignKey('tickets.Ticket')
    session_type = dd.ForeignKey('clocking.SessionType')
    summary = models.CharField(
        _("Summary"), max_length=200, blank=True,
        help_text=_("Summary of the session."))
    # date = models.DateField(verbose_name=_("Date"), blank=True)
    break_time = models.TimeField(
        blank=True, null=True,
        verbose_name=_("Break Time"))

    def __unicode__(self):
        if self.start_time and self.end_time:
            return u"%s %s-%s" % (
                self.start_date.strftime(settings.SITE.date_format_strftime),
                self.start_time.strftime(settings.SITE.time_format_strftime),
                self.end_time.strftime(settings.SITE.time_format_strftime))
        return "%s # %s" % (self._meta.verbose_name, self.pk)

    def save(self, *args, **kwargs):
        if self.start_date is None and not settings.SITE.loading_from_dump:
            self.start_date = settings.SITE.today()
        super(Session, self).save(*args, **kwargs)


class Sessions(dd.Table):
    model = Session
    column_names = 'ticket start_date start_time end_date end_time break_time summary user *'
    order_by = ['start_date', 'start_time']
    stay_in_grid = True


class SessionsByTicket(Sessions):
    master_key = 'ticket'
    column_names = 'start_date start_time summary user end_time break_time end_date *'


# class SessionsByProject(Sessions):
#     master_key = 'project'

class MySessions(Sessions, ByUser):
    order_by = ['start_date', 'start_time']
    column_names = 'start_date start_time end_time break_time ticket summary *'


class MySessionsByDate(MySessions):
    #~ master_key = 'date'
    order_by = ['start_time']
    label = _("My sessions by date")
    column_names = 'start_time end_time break_time ticket summary *'

    parameters = dict(
        today=models.DateField(_("Date"),
                               blank=True, default=settings.SITE.today),
    )

    @classmethod
    def get_request_queryset(self, ar):
        qs = super(MySessions, self).get_request_queryset(ar)
        #~ if ar.param_values.date:
        return qs.filter(start_date=ar.param_values.today)
        #~ return qs

    @classmethod
    def create_instance(self, ar, **kw):
        kw.update(date=ar.param_values.today)
        return super(MySessions, self).create_instance(ar, **kw)


def you_are_busy_messages(ar):
    """Yield :message:`You are busy in XXX` messages for the welcome
page."""

    events = rt.modules.cal.Event.objects.filter(
        user=ar.get_user(), guest__state=GuestStates.busy).distinct()
    if events.count() > 0:
        chunks = [unicode(_("You are busy in "))]
        sep = None
        for evt in events:
            if sep:
                chunks.append(sep)
            ctx = dict(id=evt.id)
            if evt.event_type is None:
                ctx.update(label=unicode(evt))
            else:
                ctx.update(label=evt.event_type.event_label)

            if evt.project is None:
                txt = _("{label} #{id}").format(**ctx)
            else:
                ctx.update(project=unicode(evt.project))
                txt = _("{label} with {project}").format(**ctx)
            chunks.append(ar.obj2html(evt, txt))
            chunks += [
                ' (',
                ar.instance_action_button(evt.close_meeting),
                ')']
            sep = ', '
        chunks.append('. ')
        yield E.span(*chunks)
            
#dd.add_welcome_handler(you_are_busy_messages)


