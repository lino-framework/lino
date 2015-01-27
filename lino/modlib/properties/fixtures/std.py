# -*- coding: UTF-8 -*-
# Copyright 2011-2014 Luc Saffre
# License: BSD (see file COPYING for details)


from django.utils.translation import ugettext as _

from lino.utils.instantiator import Instantiator
from lino.api import dd


def objects():
    ptype = Instantiator('properties.PropType').build
    properties = dd.resolve_app('properties')
    yield ptype(id=1, **dd.babel_values('name', **dict(
        en="Present or not",
        de=u"Vorhanden oder nicht",
        fr=u"Présent ou pas",
        et=u"Olemas või mitte",
        nl=u"Ja of niet",
    )))
    yield ptype(id=2,
                choicelist=properties.HowWell.actor_id,
                default_value=properties.HowWell.default.value,
                **dd.babel_values('name', **dict(
                    en="Rating",
                    de=u"Bewertung",
                    et=u"Hinnang",
                    fr=u"Appréciation(?)",
                    nl=u"Hoe goed",
                )))
