# -*- coding: UTF-8 -*-
# Copyright 2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""The :xfile:`models.py` module for `lino_welfare.modlib.countries`.

"""

from __future__ import unicode_literals

from lino.api import _
from lino.modlib.countries.models import *


class Country(Country):
    inscode = models.CharField(
        _("INS code"),
        max_length=3, blank=True,
        help_text=_("The official code for this country "
                    "used by statbel.fgov.be"))
    

class Place(Place):
    inscode = models.CharField(
        _("INS code"),
        max_length=5, blank=True,
        help_text=_("The official code for this place "
                    "used by statbel.fgov.be"))

Places.detail_layout = """
name country inscode zip_code
parent type id
PlacesByPlace
contacts.PartnersByCity cv.StudiesByPlace
"""

Countries.detail_layout = """
isocode name short_code inscode
# nationalities
countries.PlacesByCountry cv.StudiesByCountry
"""

Countries.insert_layout = """
isocode inscode
name
"""
