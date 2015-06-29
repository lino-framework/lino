# Copyright 2015 Luc Saffre
# License: BSD (see file COPYING for details)

from lino.core.roles import SiteUser

from lino.modlib.contacts.roles import ContactsUser, ContactsStaff


class OfficeUser(ContactsUser):
    """A user who has access to office functionality like calendar, notes
    and uploads.

    """


class OfficeOperator(ContactsUser):
    """A user who manages office functionality for other users (but not
    for himself).

    """


class OfficeStaff(OfficeUser, OfficeOperator, ContactsStaff):
    pass


