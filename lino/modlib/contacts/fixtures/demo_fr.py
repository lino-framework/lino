# -*- coding: UTF-8 -*-
# Copyright 2012-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""
"""
from builtins import range

from lino.utils import Cycler
from lino.api import dd, rt
from lino.utils import demonames


def objects():

    last_names = demonames.LAST_NAMES_BELGIUM
    male_first_names = demonames.MALE_FIRST_NAMES_FRANCE
    female_first_names = demonames.FEMALE_FIRST_NAMES_FRANCE

    Person = rt.modules.contacts.Person
    Place = rt.modules.countries.Place

    CITIES = Cycler(
        Place.objects.filter(country_id='BE', zip_code__startswith='40'))
    STREETS = Cycler(demonames.streets_of_liege())

    common = dict(language='fr', country_id='BE')
    for i in range(100):
        yield Person(
            first_name=male_first_names.pop(),
            last_name=last_names.pop(),
            gender=dd.Genders.male,
            city=CITIES.pop(),
            street=STREETS.pop(),
            **common
        )
        yield Person(
            first_name=female_first_names.pop(),
            last_name=last_names.pop(),
            gender=dd.Genders.female,
            city=CITIES.pop(),
            street=STREETS.pop(),
            **common
        )
