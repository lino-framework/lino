# -*- coding: UTF-8 -*-
# Copyright 2014-2018 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

"""User roles for `lino.modlib.checkdata`."""

from lino.core.roles import UserRole


class CheckdataUser(UserRole):
    """Can see data problems."""
