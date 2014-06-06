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

from __future__ import print_function

import logging
logger = logging.getLogger(__name__)

from django.core.exceptions import ValidationError

from lino import dd

from lino.utils.instantiator import InstanceGenerator

from .models import PlaceTypes


class PlaceGenerator(InstanceGenerator):
    def __init__(self):
        super(PlaceGenerator, self).__init__()
        self.prev_obj = None
        EE = dd.modules.countries.Country.objects.get(isocode="EE")

        for pt in PlaceTypes.objects():
            self.add_instantiator(
                pt.name, 'countries.Place', 'name zip_code',
                country=EE,
                type=pt)

    def on_new(self, obj):
        prev = self.prev_obj
        if prev and prev.type and obj.type:
            if prev.type < obj.type:
                obj.parent = prev
            else:
                p = prev.parent
                while p and not self.can_be_parent(p, obj):
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
    
    def can_be_parent(self, p, o):
        "return True if p can be parent for o"
        if self.assimilate(p.type) < self.assimilate(o.type):
            return True
        return False

    def assimilate(self, pt):
        """In Estonia, municipalities and towns can be siblings within a same
county."""
        if pt == PlaceTypes.municipality:
            return PlaceTypes.town
        return pt
    

