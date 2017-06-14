# Copyright 2015-2017 Luc Saffre
# License: BSD (see file COPYING for details)

"""Defines a default set of user user_types "Anonymous", "User" and
"Administrator".

This can be used directly as :attr:`user_types_module
<lino.core.site.Site.user_types_module>` for simple applications,
e.g.  :mod:`lino.projects.min1` and :mod:`lino.projects.min2`.

"""

from lino.core.roles import SiteUser

class Helper(SiteUser):
    """Somebody who can help others by running :class:`AssignToMe`
    action.

    """

class AuthorshipTaker(SiteUser):
    """Somebody who can help others by running :class:`TakeAuthorship`
    action.

    """

