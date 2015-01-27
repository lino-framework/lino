# -*- coding: UTF-8 -*-
# Copyright 2014 Luc Saffre
# License: BSD (see file COPYING for details)

"""This fixture imports all Estonian places from :mod:`commondata.ee`
(which needs to be installed before loading this fixture).

"""

import logging
logger = logging.getLogger(__name__)

from commondata.ee.places import root

from commondata.ee.places import (Village, SmallBorough, Borough,
                                  Township, Town, Municipality, County)

from lino.api import dd

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


def place2objects(country, place, parent=None):
    t = cd2type(place)
    if t is None:
        logger.info("20140612 ignoring place %s", place)
        return
    obj = countries.Place(
        country=country, type=t, name=place.name,
        parent=parent,
        zip_code=place.zip_code)

    # We must save the parent before we can generate children.
    try:
        obj.full_clean()
    except Exception as e:
        raise Exception("Could not save %s : %r" % (
            dd.obj2str(obj), e))
    obj.save()
    yield obj

    for cp in place.children:
        yield place2objects(country, cp, obj)


def objects():

    eesti = root()
    EE = countries.Country.objects.get(isocode="EE")
    for p in eesti.children:
        yield place2objects(EE, p)
        
