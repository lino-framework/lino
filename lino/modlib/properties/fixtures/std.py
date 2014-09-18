# -*- coding: UTF-8 -*-
# Copyright 2011-2012 Luc Saffre
# License: BSD (see file COPYING for details)


from django.utils.translation import ugettext as _

from lino.utils.instantiator import Instantiator
from lino import dd
from north.dbutils import babel_values

#~ def objects():
    #~ ptype = Instantiator('properties.PropType').build

    #~ division = ptype(**babel_values('name',**dict(en="Division",fr="Division",de=u"Abteilung")))
    #~ yield division
    #~ divchoice = Instantiator('properties.PropChoice','value',type=division).build
    #~ yield divchoice('1',**babel_values('text',**dict(en="Furniture",de=u"Möbel",fr=u"Meubles")))
    #~ yield divchoice('1',**babel_values('text',**dict(en="Web hosting",de=u"Hosting",fr=u"Hosting")))


def objects():
    ptype = Instantiator('properties.PropType').build
    yield ptype(id=1, **babel_values('name', **dict(
        en="Present or not",
        de=u"Vorhanden oder nicht",
        fr=u"Présent ou pas",
        et=u"Olemas või mitte",
        nl=u"Ja of niet",
    )))
    yield ptype(id=2,
                choicelist=dd.HowWell.actor_id,
                default_value=dd.HowWell.default.value,
                **babel_values('name', **dict(
                    en="Rating",
                    de=u"Bewertung",
                    et=u"Hinnang",
                    fr=u"Appréciation(?)",
                    nl=u"Hoe goed",
                )))
