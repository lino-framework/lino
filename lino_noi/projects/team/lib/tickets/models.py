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
"""Database models specific for the Team variant of Lino Noi.

Defines a customized :class:`TicketDetail`.

"""

from lino_noi.lib.tickets.models import *
from lino.api import _


class TicketDetail(TicketDetail):
    """Customized detail_lyout for Tickets.  Replaces `waiting_for` by
    `faculties`

    """
    
    general = dd.Panel("""
    general1:60 deploy.DeploymentsByTicket:20
    comments.CommentsByRFC:60 clocking.SessionsByTicket:20
    """, label=_("General"))

    general1 = """
    summary:40 id:6 reporter:12
    site topic project private
    workflow_buttons:30 assigned_to:20 faculty:20
    """

Tickets.detail_layout = TicketDetail()

Sites.detail_layout = """
id name partner #responsible_user
remark
#InterestsBySite TicketsBySite deploy.MilestonesBySite
"""



@dd.receiver(dd.post_analyze)
def my_details(sender, **kw):
    sender.modules.system.SiteConfigs.set_detail_layout("""
    site_company next_partner_id:10
    default_build_method
    """)

