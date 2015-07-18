# Copyright 2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""Defines the standard user roles for `lino.projects.presto`."""

from django.utils.translation import ugettext_lazy as _
from lino.core.roles import UserRole, SiteAdmin, SiteStaff
from lino.modlib.office.roles import OfficeStaff, OfficeUser
from lino.modlib.users.choicelists import UserProfiles


class SiteUser(OfficeUser):
    pass


class SiteAdmin(SiteAdmin, OfficeStaff):
    pass


class Developer(SiteStaff):
    pass


class SeniorDeveloper(Developer):
    pass

UserProfiles.clear()
add = UserProfiles.add_item
add('000', _("Anonymous"), UserRole, name='anonymous',
    readonly=True,
    authenticated=False)
add('100', _("User"), SiteUser, name='user')
add('500', _("Developer"), Developer, name='developer')
add('510', _("Senior Developer"), SeniorDeveloper, name='senior')
add('900', _("Administrator"), SiteAdmin, name='admin')
