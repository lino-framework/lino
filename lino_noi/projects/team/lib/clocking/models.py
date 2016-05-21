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
"""Database models for lino_noi.projects.team.lib.clocking.


"""

from lino_noi.lib.clocking.models import *
from lino.api import _


class EndTicketSession(dd.Action):
    # label = _("End session")
    # label = u"\u231a\u2198"
    # label = u"↘"  # u"\u2198"
    label = u"◉"  # FISHEYE (U+25C9)
    help_text = _("End the active session on this ticket.")
    show_in_workflow = False
    show_in_bbar = False
    required_roles = dd.login_required()
    readonly = False
    
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
        ses.set_datetime('end', timezone.now())
        ses.full_clean()
        ses.save()
        ar.set_response(refresh=True)


class StartTicketSession(dd.Action):
    # label = _("Start session")
    # label = u"\u262d"
    # label = u"\u2692"
    # label = u"\u2690"
    # label = u"\u2328"
    # label = u"\u231a\u2197"
    # label = u"↗"  # \u2197
    label = u"▶"  # BLACK RIGHT-POINTING TRIANGLE (U+25B6)
    help_text = _("Start a session on this ticket.")
    # icon_name = 'emoticon_smile'
    show_in_workflow = False
    show_in_bbar = False
    readonly = False

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


class ServiceReport(UserAuthored, Certifiable, DatePeriod):
    """A **service report** is a document used in various discussions with
    a stakeholder.

    .. attribute:: user

        This can be empty and will then show the working time of all
        users.


    .. attribute:: start_date
    .. attribute:: end_date
    .. attribute:: interesting_for
    .. attribute:: ticket_state

    .. attribute:: printed
        See :attr:`lino.modlib.exerpts.mixins.Certifiable.printed`

    """
    class Meta:
        verbose_name = _("Service Report")
        verbose_name_plural = _("Service Reports")

    interesting_for = dd.ForeignKey(
        'tickets.Site',
        verbose_name=_("Interesting for"),
        blank=True, null=True,
        help_text=_("Only tickets interesting for this site."))

    ticket_state = TicketStates.field(
        null=True, blank=True,
        help_text=_("Only tickets in this state."))

    def get_tickets_parameters(self, **pv):
        """Return a dict with parameter values for `tickets.Tickets` based on
        the options of this report.

        """
        pv.update(start_date=self.start_date, end_date=self.end_date)
        pv.update(interesting_for=self.interesting_for)
        if self.ticket_state:
            pv.update(state=self.ticket_state)
        return pv
        
from .ui import *
