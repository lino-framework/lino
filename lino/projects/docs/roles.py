# Copyright 2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""Defines the standard user roles for `lino.projects.docs`.

See also :attr:`lino.core.Site.Site.user_profiles_module`.

"""

from lino.core.roles import Anonymous, SiteAdmin, SiteStaff
from lino.modlib.office.roles import OfficeStaff, OfficeUser
from lino.modlib.accounts.roles import AccountingReader


class SiteUser(OfficeUser, AccountingReader):
    pass


class SiteAdmin(SiteAdmin, OfficeStaff, AccountingReader):
    pass


from django.utils.translation import ugettext_lazy as _
from lino.modlib.users.choicelists import UserProfiles
UserProfiles.clear()
add = UserProfiles.add_item
add('000', _("Anonymous"), Anonymous, name='anonymous',
    readonly=True,
    authenticated=False)
add('100', _("User"), SiteUser, name='user')
add('900', _("Administrator"), SiteAdmin, name='admin')
