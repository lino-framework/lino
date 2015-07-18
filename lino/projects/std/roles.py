# Copyright 2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""Defines a default set of user profiles "Anonymous", "User" and
"Administrator". To be used as :attr:`user_profiles_module
<lino.core.site.Site.user_profiles_module>`.

"""

from lino.core.roles import UserRole, SiteAdmin, SiteStaff
from lino.modlib.office.roles import OfficeStaff, OfficeUser
from lino.modlib.accounts.roles import AccountingReader


class SiteUser(OfficeUser, AccountingReader):
    """A normal user of this site."""
    pass


class SiteAdmin(SiteAdmin, OfficeStaff, AccountingReader):
    """A user with all adminstrator permissions on this site."""
    pass


from django.utils.translation import ugettext_lazy as _
from lino.modlib.users.choicelists import UserProfiles
UserProfiles.clear()
add = UserProfiles.add_item
add('000', _("Anonymous"), UserRole, name='anonymous',
    readonly=True,
    authenticated=False)
add('100', _("User"), SiteUser, name='user')
add('900', _("Administrator"), SiteAdmin, name='admin')
