# Copyright 2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""Defines a default set of user profiles "Anonymous", "User" and
"Administrator".

This can be used directly as :attr:`user_profiles_module
<lino.core.site.Site.user_profiles_module>` for simple applications,
e.g.  :mod:`lino.projects.min1` and :mod:`lino.projects.min2`.

"""

from django.utils.translation import ugettext_lazy as _
from lino.core.roles import UserRole, SiteUser, SiteAdmin


from .choicelists import UserProfiles


UserProfiles.clear()
add = UserProfiles.add_item
add('000', _("Anonymous"), UserRole, name='anonymous', readonly=True)
add('100', _("User"), SiteUser, name='user')
add('900', _("Administrator"), SiteAdmin, name='admin')
