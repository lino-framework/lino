# Copyright 2011-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""
Defines application-specific default user profiles.
Local site administrators can override this in their :xfile:.
"""
from lino.modlib.users.choicelists import (
    UserProfiles, Anonymous, SiteUser, StaffMember, SiteAdmin)
from lino.modlib.office.choicelists import OfficeUser
from django.utils.translation import ugettext_lazy as _


class StaffMember(StaffMember, OfficeUser):
    pass


class SiteAdmin(SiteAdmin, OfficeUser):
    pass


class Developer(StaffMember, OfficeUser):
    text = _("Developer")


class SeniorDeveloper(Developer, OfficeUser):
    text = _("Senior developer")

UserProfiles.clear()
add = UserProfiles.add_item_instance
add(Anonymous('000', name='anonymous', readonly=True, authenticated=False))
add(OfficeUser('100',  name='user'))
add(StaffMember('200', name='developer'))
add(SeniorDeveloper('300', name='senior'))
add(SiteAdmin('900', name='admin'))
