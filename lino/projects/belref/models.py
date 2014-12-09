# -*- coding: UTF-8 -*-
# Copyright 2013-2014 Luc Saffre
# License: BSD (see file COPYING for details)

"""
The :xfile:`models` module for the :mod:`lino.projects.belref` app.

"""

from lino import dd

concepts = dd.resolve_app('concepts')


class Main(concepts.TopLevelConcepts):
    pass


def site_setup(site):
    site.modules.countries.Places.required = dd.required(auth=False)
    site.modules.countries.Countries.required = dd.required(auth=False)
    site.modules.concepts.Concepts.required = dd.required(auth=False)

    site.modules.countries.Places.set_detail_layout("""
    name country inscode
    parent type id
    PlacesByPlace
    """)

    site.modules.countries.Countries.set_detail_layout("""
    isocode name short_code inscode
    countries.PlacesByCountry
    """)
