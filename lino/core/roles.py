# Copyright 2011-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""Defines built-in user roles. See :mod:`lino.core.permissions`.

"""


class UserRole(object):
    pass


# class Anonymous(UserRole):
#     pass


class SiteUser(UserRole):
    """Every authenticated user has this role."""


class SiteStaff(SiteUser):
    """A user who can configure site-wide functionality.

    Certain privileged actions require this role:

    - Merging duplicate database records (:class:`MergeAction
      <lino.core.merge.MergeAction>`)

    - Editing printable templates (:class:`EditTemplate
      <lino.mixins.printable.EditTemplate>`)

    """


class SiteAdmin(SiteStaff):
    """The root user of this system. """
    pass
