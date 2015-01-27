# -*- coding: UTF-8 -*-
# Copyright 2014 Luc Saffre
# License: BSD (see file COPYING for details)

"""This is not yet used nor tested.  The idea is to collect some
product repertoire using real products. To be complete this would
require a model Producer or Provider (which does not yet exist).

"""

from __future__ import unicode_literals

from lino.utils.instantiator import Instantiator

from lino.api import dd

def objects():

    productcat = Instantiator('products.ProductCat').build
    product = Instantiator('products.Product', "cat name").build

    food = productcat(**dd.babel_values(
        'name',
        en="Food", et="Toit", de="Lebensmittel", fr="Alimentaire"))
    yield food
    yield product(food, "Le petit Fagnard", **dd.babel_values(
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

