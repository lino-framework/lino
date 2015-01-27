# -*- coding: UTF-8 -*-
# Copyright 2011-2014 Luc Saffre
# License: BSD (see file COPYING for details)


from django.utils.translation import ugettext as _

from lino.utils.instantiator import Instantiator
from lino.api import dd


def objects():
    ptype = Instantiator('properties.PropType').build

    division = ptype(
        **dd.babel_values('name', **dict(
            en="Division", fr="Division", de=u"Abteilung")))
    yield division
    divchoice = Instantiator(
        'properties.PropChoice', 'value', type=division).build
    yield divchoice('1', **dd.babel_values(
        'text', **dict(en="Furniture", de=u"Möbel", fr=u"Meubles")))
    yield divchoice('2', **dd.babel_values(
        'text', **dict(en="Web hosting", de=u"Hosting", fr=u"Hosting")))
