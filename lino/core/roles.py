# Copyright 2011-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""Defines built-in user roles. See :mod:`lino.core.permissions`.

"""


class UserRole(object):
    pass


class Anonymous(UserRole):
    pass


class SiteUser(UserRole):
    pass


class SiteStaff(SiteUser):
    """Certain privileged technical actions require this role by default:

    :class:`MergeAction <lino.core.merge.MergeAction>`
    :class:`EditTemplate <lino.mixins.printable.EditTemplate>`
    """
    pass


class SiteAdmin(SiteStaff):
    """The root user of this system. """
    pass
