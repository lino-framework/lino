# -*- coding: UTF-8 -*-
# Copyright 2012-2014 Luc Saffre
# License: BSD (see file COPYING for details)

"""
"""

from lino.utils import Cycler
from lino import mixins
from lino import dd, rt
from lino.utils import demonames


def objects():

    last_names = demonames.LAST_NAMES_BELGIUM
    male_first_names = demonames.MALE_FIRST_NAMES_FRANCE
    female_first_names = demonames.FEMALE_FIRST_NAMES_FRANCE

    Person = dd.resolve_model("contacts.Person")
    Place = dd.resolve_model('countries.Place')

    CITIES = Cycler(
        Place.objects.filter(country_id='BE', zip_code__startswith='40'))
    STREETS = demonames.streets_of_liege()

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
