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

from __future__ import unicode_literals
from __future__ import print_function

"""
"""

from lino.utils.instantiator import InstanceGenerator
from lino import dd

from lino.modlib.countries.models import PlaceTypes


class InstanceGenerator(InstanceGenerator):
    def __init__(self):
        super(InstanceGenerator, self).__init__()
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

        self.prev_obj = obj
        return super(InstanceGenerator, self).on_new(obj)
    
    def assimilate(self, pt):
        """In Estonia, municipalities and towns can be siblings within a same
county."""
        if pt == PlaceTypes.municipality:
            return PlaceTypes.town
        return pt
    
    def can_be_parent(self, p, o):
        "return True if p can be parent for o"
        if p.type < self.assimilate(o.type):
            return True
        return False


def objects():

    ig = InstanceGenerator()
    ig.county("Harju")
    ig.town("Tallinn")
    ig.county("Rapla")
    ig.town("Rapla")
    ig.municipality("Kaiu")
    ig.village("Karitsa", "79320")
    ig.village("Kasvandu", "79321")
    ig.village("Kuimetsa")

    ig.municipality("Juuru")
    ig.municipality("Märjamaa")
    ig.municipality("Vigala")
    ig.village("Kivi-Vigala")
    ig.village("Vana-Vigala", "78003")

    yield ig.flush()


def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()
