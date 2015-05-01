# -*- coding: UTF-8 -*-
# Copyright 2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""Database models for :mod:`lino_noi.modlib.contacts`.

"""

from lino.api import dd, _

from lino.modlib.contacts.models import *


class CompanyDetail(CompanyDetail):
    main = "general tickets"

    general = dd.Panel("""
    address_box:60 contact_box:30
    bottom_box
    """, label=_("General"))

    tickets = dd.Panel("""
    tickets.ProjectsByCompany
    """, label=_("Tickets"))


def site_setup(site):
    site.modules.contacts.Companies.set_detail_layout(CompanyDetail())
