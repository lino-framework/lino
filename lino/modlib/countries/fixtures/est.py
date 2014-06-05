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
from lino.modlib.countries.utils import PlaceGenerator


def objects():

    ig = PlaceGenerator()
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


