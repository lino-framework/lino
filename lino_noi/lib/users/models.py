# -*- coding: UTF-8 -*-
# Copyright 2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""Database models for :mod:`lino_noi.modlib.users`.

"""

from __future__ import unicode_literals

import logging
logger = logging.getLogger(__name__)


from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from lino.api import dd

from lino.modlib.users.models import *

from lino.modlib.office.roles import OfficeUser


class UserDetail(UserDetail):
    """Layout of User Detail in Lino Welfare."""

    main = "general tickets cal"

    cal_left = """
    event_type access_class
    cal.SubscriptionsByUser
    """

    cal = dd.Panel("""
    cal_left:30 cal.TasksByUser:60
    """, label=dd.plugins.cal.verbose_name,
                   required_roles=dd.login_required(OfficeUser))

    general = dd.Panel("""
    box1
    remarks:40 AuthoritiesGiven:20
    """, label=_("General"))

    tickets = dd.Panel("""
    open_session_on_new_ticket current_project
    tickets.TicketsByReporter
    """, label=_("Tickets"))


def site_setup(site):
    site.modules.users.Users.set_detail_layout(UserDetail())
