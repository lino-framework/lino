# Copyright 2015 Luc Saffre
# License: BSD (see file COPYING for details)

from lino.core.roles import SiteUser


class ContactsUser(SiteUser):
    """A user who has access to contacts data (persons, companies etc...).

    """


class ContactsStaff(ContactsUser):
    pass


