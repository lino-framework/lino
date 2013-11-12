# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

from north.dbutils import babelkw 
from de_BE.models import Expression

def O(fr,en,de,de_BE):
    return Expression(**babelkw('name',de=de,de_BE=de_BE,en=en,fr=fr))

def objects():
    yield O("l'atelier","the workshop","die Werkstatt","das Atelier")
    yield O("le camion","the lorry","der Lastwagen","der Camion")
    yield O("le classeur","the folder","der Ordner","die Farde")


    # TODO: non-ascii chars cause doctest failure
    #~ yield O("le frigo","the fridge","der Kühlschrank","der Frigo")
    #~ yield O("C'est ça l'important.","That's what it depends on.","Darauf kommt es an.","Darauf kommt es sich an.")
    #~ yield O("C'est à propos de la santé","It's about health.","Es geht um die Gesundheit.","Es geht sich um die Gesundheit.")
