# -*- coding: UTF-8 -*-
# Copyright 2015 Luc Saffre
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

"""Database models for :mod:`lino_noi.modlib.contacts`.

"""

from lino.api import dd, _

from lino_xl.lib.contacts.models import *


class CompanyDetail(CompanyDetail):
    main = "general tickets"

    general = dd.Panel("""
    address_box:60 contact_box:30
    bottom_box
    """, label=_("General"))

    tickets = dd.Panel("""
    tickets.ProjectsByCompany
    """, label=_("Tickets"))


# @dd.receiver(dd.post_analyze)
# def my_details(sender, **kw):
#     contacts = sender.models.contacts
#     contacts.Companies.set_detail_layout(contacts.CompanyDetail())

Companies.set_detail_layout(CompanyDetail())
