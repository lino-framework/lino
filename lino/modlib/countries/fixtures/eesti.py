# -*- coding: UTF-8 -*-
# Copyright 2014 Luc Saffre
# This file is part of the Lino project.
# Lino is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
# Lino is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
# You should have received a copy of the GNU Lesser General Public License
# along with Lino; if not, see <http://www.gnu.org/licenses/>.

"""This fixture imports all Estonian places from :mod:`commondata.ee`
(which needs to be installed before loading this fixture).

"""

from commondata.ee.places import root

from commondata.ee.places import (Village, SmallBorough, Borough,
                                  Township, Town, Municipality, County)

from lino import dd

countries = dd.resolve_app('countries')


def cd2type(p):
    if isinstance(p, County):
        return countries.PlaceTypes.county
    if isinstance(p, Township):
        return countries.PlaceTypes.township
    if isinstance(p, Town):
        return countries.PlaceTypes.town
    if isinstance(p, Municipality):
        return countries.PlaceTypes.municipality
    if isinstance(p, Borough):
        return countries.PlaceTypes.borough
    if isinstance(p, SmallBorough):
        return countries.PlaceTypes.smallborough
    if isinstance(p, Village):
        return countries.PlaceTypes.village


def objects():

    EE = countries.Country.objects.get(isocode="EE")

    # def get_from_db(p):
    #     t = cd2type(p)
    #     if t is None:
    #         raise Exception("Oops")
    #     fkw = dict(name=p.name, type=t, country=EE,
    #                zip_code=p.zip_code)
    #     return countries.Places.objects.get(**fkw)
    
    def place2objects(place, parent=None):
        t = cd2type(place)
        if t is None:
            return
        obj = countries.Place(
            country=EE, type=t, name=place.name,
            parent=parent,
            zip_code=place.zip_code)
        obj.full_clean()
        obj.save()
        yield obj
        
        for cp in place.children:
            yield place2objects(cp, obj)

    eesti = root()
    for p in eesti.children:
        yield place2objects(p)
