# Copyright 2015 Luc Saffre
# License: BSD (see file COPYING for details)
"""User roles for `lino.modlib.polls`.

This can be used directly as :attr:`user_profiles_module
<lino.core.site.Site.user_profiles_module>` for simple applications,
e.g.  :mod:`lino.projects.polly`.
"""

from django.utils.translation import ugettext_lazy as _
from lino.core.roles import UserRole, SiteUser, SiteAdmin


class PollsUser(SiteUser):
    """A user who has access to polls functionality.

    """


class PollsStaff(PollsUser):
    """A user who manages configuration of polls functionality.

    """


class PollsAdmin(PollsStaff, SiteAdmin):
    pass


from lino.modlib.users.choicelists import UserProfiles


UserProfiles.clear()
add = UserProfiles.add_item
add('000', _("Anonymous"), UserRole, name='anonymous', readonly=True)
add('100', _("User"), PollsUser, name='user')
add('900', _("Administrator"), PollsAdmin, name='admin')
