# Copyright 2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""Defines the standard user roles for `lino_noi`."""


from lino.core.roles import UserRole, SiteAdmin
from lino.modlib.office.roles import OfficeStaff, OfficeUser
from lino.modlib.tickets.roles import Worker
from lino.modlib.users.choicelists import UserProfiles
from django.utils.translation import ugettext_lazy as _


class EndUser(OfficeUser):
    """An **end user** is somebody who uses our software and may report
    tickets, but won't work on them.

    """
    pass


class Consultant(EndUser, Worker):
    """A **consultant** is somebody who may both report tickets and work
    on them.

    """
    pass


class SiteAdmin(Consultant, SiteAdmin, OfficeStaff):
    pass

UserProfiles.clear()
add = UserProfiles.add_item
add('000', _("Anonymous"),       UserRole, 'anonymous',
    readonly=True, authenticated=False)
add('100', _("User"),            EndUser, 'user')
add('200', _("Consultant"),      Consultant, 'consultant')
add('300', _("Hoster"),          Consultant, 'hoster')
add('400', _("Developer"),       Consultant, 'developer')
add('490', _("Senior"),          Consultant, 'senior')
add('900', _("Administrator"),   SiteAdmin, 'admin')
