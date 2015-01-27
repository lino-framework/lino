# -*- coding: UTF-8 -*-
# Copyright 2009-2014 Luc Saffre
# License: BSD (see file COPYING for details)

from __future__ import unicode_literals

from lino.utils.instantiator import Instantiator

from lino.api import dd


def objects():

    productcat = Instantiator('products.ProductCat').build
    product = Instantiator('products.Product', "sales_price cat").build

    furniture = productcat(
        id=1, **dd.babel_values(
            'name',
            en="Furniture", et="Mööbel", de="Möbel", fr="Meubles"))
    yield furniture
    # print "foo", furniture.id, furniture
    hosting = productcat(
        id=2, **dd.babel_values(
            'name',
            en="Website Hosting",
            et="Veebimajutus",
            de="Website-Hosting",
            fr="Hébergement de sites Internet"))
    yield hosting

    kw = dd.babel_values('name',
                      en="Wooden table",
                      et=u"Laud puidust",
                      de="Tisch aus Holz",
                      fr=u"Table en bois")
    kw.update(dd.babel_values(
        'description',
        en="""\
This table is made of pure wood.
It has **four legs**.
Designed to fit perfectly with **up to 6 wooden chairs**.
Product of the year 2008.""",
        et="""\
See laud on tehtud ehtsast puust.
Sellel on **neli jalga**.
Disainitud sobida kokku **kuni 6 puidust tooliga**.
Product of the year 2008.""",
        de="""\
Dieser Tisch ist aus echtem Holz.
Er hat **vier Beine**.
Passt perfekt zusammen mit **bis zu 6 Stühlen aus Holz**.
Produkt des Jahres 2008.""",
        fr="""\
Cette table est en bois authentique.
Elle a **quatre jambes**.
Conçue pour mettre jusqu'à **6 chaises en bois**.
Produit de l'année 2008.""",
    ))
    yield product("199.99", 1, **kw)
    yield product("99.99", 1, **dd.babel_values('name',
                                             en="Wooden chair",
                                             et="Tool puidust",
                                             de="Stuhl aus Holz",
                                             fr="Chaise en bois"))
    yield product("129.99", 1, **dd.babel_values('name',
                                              en="Metal table",
                                              et="Laud metallist",
                                              de="Tisch aus Metall",
                                              fr="Table en métal"))
    yield product("79.99", 1, **dd.babel_values('name',
                                             en="Metal chair",
                                             et="Tool metallist",
                                             de="Stuhl aus Metall",
                                             fr="Chaise en métal"))
    hosting = product("3.99", 2,
                      **dd.babel_values('name',
                                     en="Website hosting 1MB/month",
                                     et="Majutus 1MB/s",
                                     de="Website-Hosting 1MB/Monat",
                                     fr="Hébergement 1MB/mois"))
    yield hosting
    yield product("30.00", 2,
                  **dd.babel_values('name',
                                 en="IT consultation & maintenance",
                                 et=u"IKT konsultatsioonid & hooldustööd",
                                 de=u"EDV Konsultierung & Unterhaltsarbeiten",
                                 fr=u"ICT Consultation & maintenance"))
    yield product("35.00", 2, **dd.babel_values(
        'name',
        en="Server software installation, configuration and administration",
        et="Serveritarkvara installeerimine, seadistamine ja administreerimine",
        de="Server software installation, configuration and administration",
        fr="Server software installation, configuration and administration"))

    yield product("40.00", 2, **dd.babel_values(
        'name',
        en="Programming",
        et="Programmeerimistööd",
        de="Programmierung",
        fr="Programmation"))

    yield product("25.00", 2, **dd.babel_values(
        'name',
        en="Image processing and website content maintenance",
        et="Pilditöötlus ja kodulehtede sisuhaldustööd",
        de="Bildbearbeitung und Unterhalt Website",
        fr="Traitement d'images et maintenance site existant"))
