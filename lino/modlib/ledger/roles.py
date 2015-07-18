# -*- coding: UTF-8 -*-
# Copyright 2015 Luc Saffre
# License: BSD (see file COPYING for details)


from lino.core.roles import UserRole
from lino.api import _


class AccountingReader(UserRole):
    pass


from lino.modlib.office.roles import *


class SiteUser(OfficeUser, AccountingReader):
    """A normal authentified user."""
    pass


class SiteAdmin(SiteAdmin, OfficeStaff, AccountingReader):
    """A user with all permissions."""
    pass


UserProfiles.clear()
add = UserProfiles.add_item
add('000', _("Anonymous"), UserRole, name='anonymous', readonly=True)
add('100', _("User"), SiteUser, name='user')
add('900', _("Administrator"), SiteAdmin, name='admin')
