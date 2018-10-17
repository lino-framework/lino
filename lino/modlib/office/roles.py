# Copyright 2015-2018 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)
"""User roles for `lino.modlib.office`.

"""

# from lino.core.roles import UserRole, SiteUser, SiteAdmin
from lino.core.roles import UserRole

class OfficeUser(UserRole):
    """
    Has access to office functionality like calendar, notes and
    uploads.
    """

class OfficeOperator(UserRole):
    """
    Can manage office functionality for other users (but not for
    himself).

    An office operator can create their own notes and uploads, but no
    calendar entries.

    For example the `lino_xl.lib.cal.ui.OverdueAppointments` table
    requires :class:`OfficeStaff` and is *not* available for
    :class:`OfficeOperator`.
    """

class OfficeStaff(OfficeUser, OfficeOperator):
    """
    Can manage configuration of office functionality.
    """


