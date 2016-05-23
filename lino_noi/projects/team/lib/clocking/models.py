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
        'contacts.Partner',
        verbose_name=_("Interesting for"),
        blank=True, null=True,
        help_text=_("Only tickets interesting for this partner."))

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
