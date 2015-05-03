# Copyright 2011-2015 Luc Saffre
# License: BSD (see file COPYING for details)

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

