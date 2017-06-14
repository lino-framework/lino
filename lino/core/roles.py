# Copyright 2011-2017 Luc Saffre
# License: BSD (see file COPYING for details)

"""Defines built-in user roles. See :ref:`permissions`.

"""
from builtins import object


class UserRole(object):
    """Base class for all user roles. Even anonymous users have this
    role.

    """

    def satisfies_requirement(self, required_roles):
        """Return `True` if this user role satisfies the specified role
        requirement.

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

    has_required_roles = satisfies_requirement  # backwards compat

    @classmethod
    def get_user_profiles(cls):
        """Yield a series of all user profiles on this site which satisfy this
        role.

        """
        from lino.modlib.users.choicelists import UserTypes
        for p in UserTypes.items():
            if p.has_required_roles([cls]):
                yield p


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


class Supervisor(UserRole):
    """A user who has permission to act as another user."""


class Explorer(UserRole):
    """A user who has permission to explore the database content, e.g.
    for writing statistical reports.

    """


class SiteAdmin(SiteStaff, Supervisor, Explorer):
    """The root user of this system. """
    pass


def login_required(*args):
    """An API shortcut available in :mod:`lino.api.dd`. See
    :meth:`lino.modlib.users.choicelists.UserType.has_required_role`

    """
    if len(args):
        return set(args)
    return set([SiteUser])


def check_role(rr, actor):
    if not issubclass(rr, UserRole):
        raise Exception(
            "{0} (required on {1}) is not a UserRole".format(rr, actor))


def check_required_roles(required_roles, actor):
    """Check whether the given value is a valid required_roles
    specification.

    - it must be iterable

    - every element must be either a subclass of :class:`UserRole` or
      an iterable thereof.

    - if an element is an iterable, then it may not be empty. Only the
      top-level iterable may be empty.

    """
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

