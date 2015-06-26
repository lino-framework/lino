# Copyright 2011-2015 Luc Saffre
# License: BSD (see file COPYING for details)

raise Exception("moved to users.choicelists")

from lino.api import _

USER_ROLES = set()


class UserRoleMeta(type):

    def __new__(meta, classname, bases, classDict):
        """Every subclass of :class:`UserRole` is being registered into a
        global set of available user roles.

        """
        cls = type.__new__(meta, classname, bases, classDict)

        if classname != 'UserRole':
            USER_ROLES.add(cls)
        return cls


class UserRole(object):
    __metaclass__ = UserRoleMeta

    @classmethod
    def permitted_for(cls, profile):
        """Return `True` if actions requiring this role are permitted for
        users with the given profile.

        """
        for r in profile.roles:
            if issubclass(r, cls):
                return True
        return False


class SiteUser(UserRole):
    verbose_name = _("Site user")


class StaffMember(SiteUser):
    verbose_name = _("Staff member")


class SiteAdmin(StaffMember):
    verbose_name = _("Site administrator")

