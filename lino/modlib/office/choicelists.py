# Copyright 2015 Luc Saffre
# License: BSD (see file COPYING for details)

from lino.api import _
from lino.modlib.users.choicelists import SiteUser


class OfficeUser(SiteUser):
    text = _("Office user")


class OfficeStaff(OfficeUser):
    text = _("Office staff")

