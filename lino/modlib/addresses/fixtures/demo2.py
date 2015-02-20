# -*- coding: UTF-8 -*-
# Copyright 2015 Luc Saffre
# License: BSD (see file COPYING for details)
"""Adds some additional non-primary addresses to some partners.

"""

from lino.api import rt

from lino.utils import Cycler
from lino.utils.demonames.bel import streets_of_eupen


def objects():
    AddressTypes = rt.modules.addresses.AddressTypes
    Address = rt.modules.addresses.Address
    Partner = rt.modules.contacts.Partner
    Place = rt.modules.countries.Place
    eupen = Place.objects.get(name__exact='Eupen')
    STREETS = Cycler(streets_of_eupen())
    TYPES = Cycler(AddressTypes.objects())

    nr = 1
    for p in Partner.objects.filter(city=eupen):
        if nr % 3:
            kw = dict(partner=p)
            kw.update(address_type=TYPES.pop())
            kw.update(street=STREETS.pop())
            kw.update(street_no=str(nr % 200))
            yield Address(**kw)
        nr += 1
