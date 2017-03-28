# Copyright 2015-2017 Luc Saffre
# License: BSD (see file COPYING for details)
"""User roles for `lino.modlib.office`.

"""

from lino.core.roles import UserRole, SiteUser, SiteAdmin

# class OfficeUser(SiteUser):
class OfficeUser(UserRole):
    """A user who has access to office functionality like calendar, notes
    and uploads.

    """

class OfficeOperator(SiteUser):
    """A user who manages office functionality for other users (but not
    for himself).

    Currently an office operator can create their own notes and
    uploads, but no calendar entries.

    For example the `lino_xl.lib.cal.ui.OverdueAppointments` table
    requires :class:`OfficeStaff` and is *not* available for
    :class:`OfficeOperator`.

    """

class OfficeStaff(OfficeUser, OfficeOperator):
    """A user who manages configuration of office functionality.

    """


