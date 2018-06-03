# Copyright 2015-2018 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""
Defines a set of user types "Anonymous", "User" and
"Administrator".

This can be used directly as :attr:`user_types_module
<lino.core.site.Site.user_types_module>` for simple applications.
"""

from django.utils.translation import ugettext_lazy as _
from lino.core.roles import UserRole, SiteAdmin
from lino.modlib.office.roles import OfficeUser, OfficeStaff
from lino.modlib.users.choicelists import UserTypes


class SiteAdmin(SiteAdmin, OfficeStaff):
    """A user with all permissions."""
    pass


UserTypes.clear()
add = UserTypes.add_item
add('000', _("Anonymous"), UserRole, name='anonymous', readonly=True)
add('100', _("User"), OfficeUser, name='user')
add('900', _("Administrator"), SiteAdmin, name='admin')
