# -*- coding: UTF-8 -*-
# Copyright 2014 Luc Saffre
# License: BSD (see file COPYING for details)

"""
The :xfile:`models` module for :ref:`estref` app.

"""

from lino.api import dd, rt
from lino.core.permissions import SiteUser, StaffMember


def site_setup(site):
    lst = (site.modules.countries.Places,
           site.modules.countries.Countries)
    for t in lst:
        t.required_roles.discard(SiteUser)
        t.required_roles.discard(StaffMember)
