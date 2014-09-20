# -*- coding: UTF-8 -*-
# Copyright 2014 Luc Saffre
# License: BSD (see file COPYING for details)

from __future__ import print_function

import logging
logger = logging.getLogger(__name__)

from django.core.exceptions import ValidationError

from lino import dd, rt

from lino.utils.instantiator import InstanceGenerator

from .models import PlaceTypes


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
    

