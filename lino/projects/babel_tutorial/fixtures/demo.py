# -*- coding: UTF-8 -*-

from __future__ import unicode_literals

from lino.api import dd, rt

Product = dd.resolve_model('babel_tutorial.Product')


def P(en, de, fr, cat):
    return Product(
        category=cat, **dd.babel_values('name', en=en, de=de, fr=fr))


def objects():
    yield P("Chair", "Stuhl", "Chaise", '03')
    yield P("Table", "Tisch", "Table", '03')
    yield P("Monitor", "Bildschirm", "Écran", '01')
    yield P("Mouse", "Maus", "Souris", '03')
    yield P("Keyboard", "Tastatur", "Clavier", '03')
    yield P("Consultation", "Beratung", "Consultation", '02')
