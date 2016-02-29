# Copyright 2011-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""Defines built-in user roles. See :mod:`lino.core.permissions`.

"""
from builtins import object


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
        check_required_roles(required_roles, "code")
        for rr in required_roles:
            if not isinstance(self, rr):
                return False
        return True

    @classmethod
    def get_user_profiles(cls):
        """Yield a series of all user profiles on this site which satisfy this
        role.

        """
        from lino.modlib.users.choicelists import UserProfiles
        for p in UserProfiles.items():
            if p.has_required_roles([cls]):
                yield p


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


def check_role(rr, actor):
    if not issubclass(rr, UserRole):
        raise Exception(
            "{0} (required on {1}) is not a UserRole".format(rr, actor))


def check_required_roles(required_roles, actor):
    for rr in required_roles:
        if isinstance(rr, (tuple, list)):
            if len(rr) == 0:
                raise Exception(
                    "{0} (required on {1}) is an empty tuple".format(
                        rr, actor))
            for rri in rr:
                check_role(rri, actor)
        else:
            check_role(rr, actor)

