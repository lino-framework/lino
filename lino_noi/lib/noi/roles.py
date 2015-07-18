# Copyright 2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""Defines the standard user roles for `lino_noi`."""


from lino.core.roles import (UserRole, SiteAdmin)
from lino.modlib.office.roles import OfficeStaff, OfficeUser
from lino.modlib.users.choicelists import UserProfiles
from django.utils.translation import ugettext_lazy as _


class SiteUser(OfficeUser):
    pass


class SiteAdmin(SiteAdmin, OfficeStaff):
    pass

UserProfiles.clear()
add = UserProfiles.add_item
add('000', _("Anonymous"),       UserRole, 'anonymous',
    readonly=True, authenticated=False)
add('100', _("User"),            SiteUser, 'user')
add('200', _("Consultant"),      SiteUser, 'consultant')
add('300', _("Hoster"),          SiteUser, 'hoster')
add('400', _("Developer"),       SiteUser, 'developer')
add('490', _("Senior"),          SiteUser, 'senior')
add('900', _("Administrator"),   SiteAdmin, 'admin')
