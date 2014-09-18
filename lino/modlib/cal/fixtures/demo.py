# -*- coding: UTF-8 -*-
# Copyright 2011-2013 Luc Saffre
# License: BSD (see file COPYING for details)

import decimal
from dateutil.relativedelta import relativedelta
ONE_DAY = relativedelta(days=1)

from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext as _


from lino.utils import i2d, Cycler
from lino.utils.instantiator import Instantiator
from lino.core.dbutils import resolve_model
from north.dbutils import babel_values


def objects():

    if False:

        guest_role = Instantiator('cal.GuestRole').build
        yield guest_role(**babel_values('name',
                                        de=u"Teilnehmer",
                                        fr=u"Participant",
                                        en=u"Participant",
                                        et=u"Osavõtja",
                                        ))
        yield guest_role(**babel_values('name',
                                        de=u"Reiseführer",
                                        fr=u"Guide",
                                        en=u"Guide",
                                        et=u"Reisijuht",
                                        ))
        yield guest_role(**babel_values('name',
                                        de=u"Vorsitzender",
                                        fr=u"Président",
                                        en=u"Presider",
                                        et=u"Eesistuja",
                                        ))
        yield guest_role(**babel_values('name',
                                        de=u"Protokollführer",
                                        fr=u"Greffier",
                                        en=u"Reporter",
                                        et=u"Sekretär",
                                        ))

    if False:

        place = Instantiator('cal.Room').build
        yield place(**babel_values('name',
                                   de=u"Büro",
                                   fr=u"Bureau",
                                   en=u"Office",
                                   ))
        yield place(**babel_values('name',
                                   de=u"Beim Klienten",
                                   fr=u"Chez le client",
                                   en=u"A the client's",
                                   ))
        yield place(**babel_values('name',
                                   de=u"beim Arbeitgeber",
                                   fr=u"chez l'employeur",
                                   en=u"at employer's",
                                   ))
