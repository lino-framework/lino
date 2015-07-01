# -*- coding: UTF-8 -*-
# Copyright 2014-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""User roles for `lino.modlib.plausibility`."""

from lino.core.roles import SiteUser


class PlausibilityUser(SiteUser):
    """A user who can see plausibility problems."""
