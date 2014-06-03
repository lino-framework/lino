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

"""This is not yet used nor tested.  The idea is to collect some
product repertoire using real products. To be complete this would
require a model Producer or Provider (which does not yet exist).

"""

from __future__ import unicode_literals

from lino.utils.instantiator import Instantiator

from north.dbutils import babel_values


def objects():

    productcat = Instantiator('products.ProductCat').build
    product = Instantiator('products.Product', "cat name").build

    food = productcat(**babel_values(
        'name',
        en="Food", et="Toit", de="Lebensmittel", fr="Alimentaire"))
    yield food
    yield product(food, "Le petit Fagnard", **babel_values(
        'description',
        en="Handmade cheese from Hautes Ardennes",
        et="Käsitsi valmistatud juust Ardenne'idest",
        de="Handgemachter Käse aus den Hohen Ardennen",
        fr="Fromage artisanal au lait cru des Hautes Ardennes"))

    if False:  # we need an address parser which either returns or
               # creates the city. Here we don't want to know whether
               # `countries.fixtures.be` has been loaded.
        company = Instantiator(
            'contacts.Company',
            "name country:isocode city:zip_code").build
        yield company("Fromagerie du Troufleur", "BE", "4950 Waimes")

