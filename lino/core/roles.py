# Copyright 2011-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""Defines built-in user roles.

"""


class UserRole(object):
    pass


class Anonymous(UserRole):
    pass


class SiteUser(UserRole):
    pass


class SiteStaff(SiteUser):
    pass


class SiteAdmin(SiteStaff):
    pass
