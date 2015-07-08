# Copyright 2015 Luc Saffre
# License: BSD (see file COPYING for details)
"""User roles for `lino.modlib.office`.

"""

from lino.core.roles import SiteUser

from lino.modlib.contacts.roles import ContactsUser, ContactsStaff


class OfficeUser(ContactsUser):
    """A user who has access to office functionality like calendar, notes
    and uploads.

    """


class OfficeOperator(SiteUser):
    """A user who manages office functionality for other users (but not
    for himself).

    Currently an office operator can create their own notes and
    uploads but no calendar entries.

    """


class OfficeStaff(OfficeUser, OfficeOperator, ContactsStaff):
    """A user who manages configuration of office functionality.

    """

