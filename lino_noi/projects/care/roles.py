# -*- coding: UTF-8 -*-
# Copyright 2015-2016 Luc Saffre
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


"""Defines user roles for the Care variant of Lino Noi."""


from lino.core.roles import UserRole, SiteAdmin
from lino.modlib.users.roles import Helper
# from lino.modlib.office.roles import OfficeStaff
from lino_xl.lib.contacts.roles import ContactsUser
from lino.modlib.office.roles import OfficeStaff, OfficeUser
from lino_noi.lib.tickets.roles import Triager
from lino_noi.lib.clocking.roles import Worker
from lino.modlib.users.choicelists import UserProfiles
from django.utils.translation import ugettext_lazy as _


#class SimpleUser(Helper):
class SimpleUser(Helper, ContactsUser, OfficeUser):
    """A **simple user** is a person who can log into the application in
    order to manage their own pleas and competences and potentially
    can respond to other user's pleas.

    """
    pass


class Connector(Helper, ContactsUser, OfficeUser, Worker, Triager):
    """A **connector** is a person who knows other persons and who
    introduces pleas on their behalf.

    """
    pass


class SiteAdmin(SiteAdmin, OfficeStaff, Helper, ContactsUser,
                Worker, Triager):
    """A **site administrator** can create new users."""
    pass


#EndUser = SimpleUser
#Developer = SimpleUser


UserProfiles.clear()
add = UserProfiles.add_item
add('000', _("Anonymous"),        UserRole, 'anonymous',
    readonly=True, authenticated=False)
add('100', _("User"), SimpleUser, 'user')
add('500', _("Connector"), Connector, 'connector')
add('900', _("Administrator"),    SiteAdmin, 'admin')
