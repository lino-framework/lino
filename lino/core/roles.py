# Copyright 2011-2018 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""Defines built-in user roles. See :ref:`permissions`.

"""
from builtins import object


class UserRole(object):
    """
    Base class for all user roles. Even anonymous users have this
    role.

    """

    def satisfies_requirement(self, required_roles):
        """
        Return `True` if this user role satisfies the specified role
        requirement.  

        `required_roles` is the set of required roles (class objects).
        Every item is either a class object (subclass of
        :class:`<UserRole>`) or a tuple thereof.  This role (an
        instance) must satisfy *every* specified requirement.
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


class Anonymous(UserRole):
    """The role used by anonymous guest sessions."""
    
class SiteUser(UserRole):
    """Every authenticated user has this role."""

class Expert(SiteUser):
    """A user with some expertise."""


class SiteStaff(Expert):
    """
    A user who can configure site-wide functionality.

    Certain privileged actions require this role:

    - Merging duplicate database records (:class:`MergeAction
      <lino.core.merge.MergeAction>`)

    - Editing printable templates (:class:`EditTemplate
      <lino.mixins.printable.EditTemplate>`)

    """


class Supervisor(UserRole):
    """A user who has permission to act as another user."""


class Explorer(UserRole):
    """
    A user who has permission to explore the database content, e.g.
    for writing statistical reports.

    """


class SiteAdmin(SiteStaff, Supervisor, Explorer):
    """The root user of this system. """
    pass


def login_required(*args):
    """Return a set of roles to be used for a required_roles.

    An API shortcut available in :mod:`lino.api.dd`. 

    """
    if len(args):
        return set(args)
    return {SiteUser}


def check_role(rr, actor):
    if not issubclass(rr, UserRole):
        raise Exception(
            "{0} (required on {1}) is not a UserRole".format(rr, actor))


def check_required_roles(required_roles, actor):
    """
    Check whether the given value is a valid required_roles
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


def checkmro(*args):
    """
    Utility function to find out the reason of a TypeError "Cannot
    create a consistent method resolution order (MRO)".

    Usage: imagine you have some code like this:

        from one import A
        from two import B
        from three import C

        # A, B and C are subclasses of UserRole

        class MyUserRole(A, B, C):
            pass

    and Python tells you that it cannot create a consistent MRO.

    So somewhere in those classes A, B and C is a "duplicate"
    ancestor. And you have no idea where it is.

    In that case you comment out the definition of MyUserRole and
    say::

        checkmro(A, B, C):
    """
    bases = dict()
    for cl in args:
        for b in cl.__mro__:
            if b is UserRole:
                break
            if b in bases:
                print("{} inherits {} is already in {}".format(cl, b, bases[b]))
            else:
                bases[b] = cl

            
