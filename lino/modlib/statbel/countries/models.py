# -*- coding: UTF-8 -*-
# Copyright 2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""Database models for `lino.modlib.statbel.countries`.

.. autosummary::

    Country
    Place
    my_details

"""

from __future__ import unicode_literals

from lino.api import rt, _
from lino.modlib.countries.models import *


class Country(Country):
    """Adds two fields :attr:`inscode` and :attr:`actual_country`.

    .. attribute:: inscode

        The code for this country used by statbel.fgov.be

        See also :mod:`lino.modlib.statbel.countries.fixtures.inscodes`.

    .. attribute:: actual_country

        If this row represents a fake country, e.g.  a refugee status
        or a former country, then this field should contain a pointer
        to the actual country.

    """
    inscode = models.CharField(
        _("INS code"),
        max_length=3, blank=True,
        help_text=_("The official code for this country "
                    "used by statbel.fgov.be"))

    actual_country = models.ForeignKey(
        'self', verbose_name=_("Actual country"),
        blank=True, null=True,
        help_text=_("Select the actual country if this row represents "
                    "a refugee status or a former country."))

    @dd.chooser()
    def actual_country_choices(cls):
        """Avoid selecting a country which actually isn't one. """
        return cls.get_actual_countries()

    @classmethod
    def get_actual_countries(cls):
        return rt.modules.countries.Country.objects.filter(
            actual_country__isnull=True)

Country.set_widget_options('actual_country', width=20)
Country.set_widget_options('inscode', width=10)


class Place(Place):
    """Adds a field :attr:`inscode`.

    """
    inscode = models.CharField(
        _("INS code"),
        max_length=5, blank=True,
        help_text=_("The official code for this place "
                    "used by statbel.fgov.be"))


@dd.receiver(dd.post_analyze)
def my_details(sender, **kw):
    """Define an insert layout for Countries."""
    site = sender
    # site.modules.countries.Places.set_detail_layout("""
    # name country inscode zip_code
    # parent type id
    # PlacesByPlace
    # contacts.PartnersByCity cv.StudiesByPlace
    # """)

    # site.modules.countries.Countries.set_detail_layout("""
    # isocode name short_code:10 inscode:10 actual_country
    # # nationalities
    # countries.PlacesByCountry cv.StudiesByCountry
    # """)

    site.modules.countries.Countries.set_insert_layout("""
    isocode inscode
    name
    """)
