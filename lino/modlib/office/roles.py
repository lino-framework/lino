# Copyright 2015-2017 Luc Saffre
# License: BSD (see file COPYING for details)
"""User roles for `lino.modlib.office`.

"""

from lino.core.roles import UserRole, SiteUser, SiteAdmin

# from lino_xl.lib.contacts.roles import ContactsUser, ContactsStaff
# from lino.modlib.users.roles import AuthorshipTaker


# class OfficeUser(ContactsUser):
class OfficeUser(SiteUser):
    """A user who has access to office functionality like calendar, notes
    and uploads.

    """

# class OfficeOperator(AuthorshipTaker):
class OfficeOperator(SiteUser):
    """A user who manages office functionality for other users (but not
    for himself).

    Currently an office operator can create their own notes and
    uploads, but no calendar entries.

    For example the `lino_xl.lib.cal.ui.OverdueAppointments` table
    requires :class:`OfficeStaff` and is *not* available for
    :class:`OfficeOperator`.

    """


# class OfficeStaff(OfficeUser, OfficeOperator, ContactsStaff):
class OfficeStaff(OfficeUser, OfficeOperator):
    """A user who manages configuration of office functionality.

    """


class SiteAdmin(SiteAdmin, OfficeStaff):
    """A user with all permissions."""
    pass

from django.utils.translation import ugettext_lazy as _
from lino.modlib.users.choicelists import UserTypes

UserTypes.clear()
add = UserTypes.add_item
add('000', _("Anonymous"), UserRole, name='anonymous', readonly=True)
add('100', _("User"), OfficeUser, name='user')
add('900', _("Administrator"), SiteAdmin, name='admin')
