# -*- coding: UTF-8 -*-

from __future__ import unicode_literals

from lino.api import dd

Product = dd.resolve_model('mldbc.Product')


def P(en, de, fr, cat, price):
    return Product(
        price=price,
        category=cat,
        **dd.babel_values('name', en=en, de=de, fr=fr))


def objects():
    yield P("Chair", "Stuhl", "Chaise", '03', '29.95')
    yield P("Table", "Tisch", "Table", '03', '89.95')
    # doctests fail with non-ascii text, so we need to cheat:
    # yield P("Monitor", "Bildschirm", "Écran", '01', '19.95')
    yield P("Monitor", "Bildschirm", "Ecran", '01', '19.95')
    yield P("Mouse", "Maus", "Souris", '03', '2.95')
    yield P("Keyboard", "Tastatur", "Clavier", '03', '4.95')
    yield P("Consultation", "Beratung", "Consultation", '02', '59.95')
