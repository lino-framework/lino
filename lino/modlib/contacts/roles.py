# Copyright 2015 Luc Saffre
# License: BSD (see file COPYING for details)
"""User roles for `lino.modlib.contacts`. """

from lino.core.roles import SiteUser


class ContactsUser(SiteUser):
    """A user who has access to contacts functionality.

    """


class ContactsStaff(ContactsUser):
    """A user who can configure contacts functionality.

    """

