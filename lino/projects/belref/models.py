# -*- coding: UTF-8 -*-
# Copyright 2013-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""
The :xfile:`models` module for the :mod:`lino.projects.belref` app.

"""

from lino.api import dd

from lino.modlib.users.choicelists import SiteUser, StaffMember

concepts = dd.resolve_app('concepts')


class Main(concepts.TopLevelConcepts):
    pass


@dd.receiver(dd.post_analyze)
def my_details(sender, **kw):
    site = sender

    lst = (site.modules.countries.Places,
           site.modules.countries.Countries,
           site.modules.concepts.Concepts)
    for t in lst:
        t.required_roles.discard(SiteUser)
        t.required_roles.discard(StaffMember)

    site.modules.countries.Places.set_detail_layout("""
    name country inscode
    parent type id
    PlacesByPlace
    """)

    site.modules.countries.Countries.set_detail_layout("""
    isocode name short_code inscode
    countries.PlacesByCountry
    """)
