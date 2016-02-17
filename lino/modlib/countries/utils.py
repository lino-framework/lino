# -*- coding: UTF-8 -*-
# Copyright 2014-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""
Utilities for `lino.modlib.countries`.

Defines models
:class:`AddressFormatter` and
:class:`CountryDrivers`.

"""
from __future__ import print_function
from __future__ import unicode_literals
from builtins import str
from builtins import object

import logging
logger = logging.getLogger(__name__)

from django.core.exceptions import ValidationError

from lino.api import rt
from lino.utils import join_words
from lino.utils.instantiator import InstanceGenerator

from .choicelists import PlaceTypes
from .choicelists import CountryDrivers


class AddressFormatter(object):
    """Format used in BE, DE, FR, NL...

    """
    def get_city_lines(me, self):
        if self.city is not None:
            s = join_words(self.zip_code or self.city.zip_code, self.city)
            if s:
                yield s

    def get_street_lines(me, self):
        if self.street:
            s = join_words(
                self.street_prefix, self.street,
                self.street_no)
            if self.street_box:
                if self.street_box[0] in '/-':
                    s += self.street_box
                else:
                    s += ' ' + self.street_box
            yield s


class EstonianAddressFormatter(AddressFormatter):

    """Format used in Estonia.

    """
    
    def format_place(self, p):
        if p.type == PlaceTypes.municipality:
            return "%s vald" % p
        elif p.type == PlaceTypes.village:
            return "%s küla" % p
        elif p.type == PlaceTypes.county:
            return "%s maakond" % p
        return str(p)

    def get_city_lines(me, self):
        lines = []
        if self.city:
            city = self.city
            zip_code = self.zip_code or self.city.zip_code
            # Tallinna linnaosade asemel kirjutakse "Tallinn"
            if city.type == PlaceTypes.township and city.parent:
                city = city.parent
            # linna puhul pole vaja maakonda
            if city.type in (PlaceTypes.town, PlaceTypes.city):
                s = join_words(zip_code, city)
            else:
                lines.append(me.format_place(city))
                p = city.parent
                while p and not CountryDrivers.EE.is_region(p):
                    lines.append(me.format_place(p))
                    p = p.parent
                if self.region:
                    s = join_words(zip_code, self.region)
                elif p:
                    s = join_words(zip_code, me.format_place(p))
                elif len(lines) and zip_code:
                    lines[-1] = zip_code + ' ' + lines[-1]
                    s = ''
                else:
                    s = zip_code
        else:
            s = join_words(self.zip_code, self.region)
        if s:
            lines.append(s)
        return lines


ADDRESS_FORMATTERS = dict()
ADDRESS_FORMATTERS[None] = AddressFormatter()
ADDRESS_FORMATTERS['EE'] = EstonianAddressFormatter()


def get_address_formatter(country):
    """Return the address formatter (an :class:`AddressFormatter`
instance) for the given country."""
    if country and country.isocode:
        af = ADDRESS_FORMATTERS.get(country.isocode, None)
        if af is not None:
            return af
    return ADDRESS_FORMATTERS.get(None)


class PlaceGenerator(InstanceGenerator):
    def __init__(self):
        super(PlaceGenerator, self).__init__()
        self.prev_obj = None
        EE = rt.modules.countries.Country.objects.get(isocode="EE")

        for pt in PlaceTypes.objects():
            self.add_instantiator(
                pt.name, 'countries.Place', 'name zip_code',
                country=EE,
                type=pt)

    def on_new(self, obj):
        prev = self.prev_obj
        if prev and prev.type and obj.type:
            otype = self.assimilate(obj.type)
            ptype = self.assimilate(prev.type)
            if ptype < otype:
                obj.parent = prev
            else:
                p = prev.parent
                while p and not self.can_be_parent(
                        self.assimilate(p.type), otype):
                    p = p.parent
                if p is not None:
                    obj.parent = p
                elif False:
                    logger.warning(
                        "%s (%s) is no parent for %s (%s)",
                        prev, prev.type, obj, obj.type)

        try:
            obj.full_clean()
            obj.save()
            self.prev_obj = obj
            return obj
        except ValidationError as e:
            logger.warning(
                "Failed to load %s (%s) : %s",
                obj, obj.type, e)
        # return super(PlaceGenerator, self).on_new(obj)
    
    def can_be_parent(self, ptype, otype):
        """return True if a place of type pt can be parent for a place of type
        ot.

        """
        if ptype < otype:
            return True
        return False

    def assimilate(self, pt):
        """In Estonia, municipalities and towns can be siblings within a same
county."""
        if pt == PlaceTypes.municipality:
            return PlaceTypes.town
        return pt
