# -*- coding: UTF-8 -*-
# Copyright 2014-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""User roles for `lino.modlib.checkdata`."""

from lino.core.roles import UserRole


class CheckdataUser(UserRole):
    """A user who can see data problems."""
