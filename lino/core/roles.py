# Copyright 2011-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""Defines built-in user roles. See :mod:`lino.core.permissions`.

"""


class UserRole(object):
    """Base class for all user roles. Even anonymous users have this
    role.

    """

    def has_required_roles(self, required_roles):
        """Return `True` if this role satisfies the specified roles.

        The specified arguments are the set of role requirements
        (class objects).  This role (an instance) must satisfy *every*
        specified requirement.  Every requirement is either a class
        object (subclass of :class:`<UserRole>`) or a tuple thereof.

        """
        for rr in required_roles:
            if not isinstance(self, rr):
                return False
        return True


class SiteUser(UserRole):
    """Every authenticated user has this role."""


class Supervisor(UserRole):
    """A user who has permission to act as another user."""


class SiteStaff(SiteUser):
    """A user who can configure site-wide functionality.

    Certain privileged actions require this role:

    - Merging duplicate database records (:class:`MergeAction
      <lino.core.merge.MergeAction>`)

    - Editing printable templates (:class:`EditTemplate
      <lino.mixins.printable.EditTemplate>`)

    """


class SiteAdmin(SiteStaff, Supervisor):
    """The root user of this system. """
    pass


def login_required(*args):
    """An API shortcut available in :mod:`lino.api.dd`. See
    :meth:`lino.modlib.users.choicelists.UserProfile.has_required_role`

    """
    if len(args):
        return set(args)
    return set([SiteUser])

