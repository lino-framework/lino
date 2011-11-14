# -*- coding: UTF-8 -*-
## Copyright 2011 Luc Saffre
## This file is part of the Lino-DSBE project.
## Lino-DSBE is free software; you can redistribute it and/or modify 
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 3 of the License, or
## (at your option) any later version.
## Lino-DSBE is distributed in the hope that it will be useful, 
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
## GNU General Public License for more details.
## You should have received a copy of the GNU General Public License
## along with Lino-DSBE; if not, see <http://www.gnu.org/licenses/>.

"""
Installas standard values for the following models:
- :class:`lino.modlib.cal.models.TaskStatus`
- :class:`lino.modlib.cal.models.EventStatus`
- :class:`lino.modlib.cal.models.AccessClass`
- :class:`lino.modlib.cal.models.Priority`

"""

import decimal
from dateutil.relativedelta import relativedelta
ONE_DAY = relativedelta(days=1)

from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext as _


from lino.utils import i2d
from lino.utils.instantiator import Instantiator
from lino.tools import resolve_model
from lino.utils.babel import babel_values



def objects():

    add = Instantiator('cal.EventStatus','ref').build
    yield add('0',**babel_values('name',en=u"tentative",de=u"Vorschlag",   fr=u"proposition"))
    yield add('1',**babel_values('name',en=u"confirmed",de=u"bestätigt",   fr=u"confirmé"))
    yield add('2',**babel_values('name',en=u"cancelled",de=u"storniert",   fr=u"annulé"))
    yield add('3',**babel_values('name',en=u"rescheduled",de=u"verschoben",   fr=u"reporté"))
    yield add('4',**babel_values('name',en=u"absent",de=u"abwesend",   fr=u"absent"))


    add = Instantiator('cal.TaskStatus','ref').build
    yield add('0',**babel_values('name',en=u"needs action",de=u"zu erledigen",   fr=u"à traîter"))
    yield add('1',**babel_values('name',en=u"in process",de=u"begonnen",   fr=u"commencée"))
    yield add('2',**babel_values('name',en=u"completed",de=u"erledigt",   fr=u"complétée"))
    yield add('3',**babel_values('name',en=u"cancelled",de=u"storniert",   fr=u"annulée"))

    add = Instantiator('cal.AccessClass','ref').build
    yield add('0',**babel_values('name',en=u"Public",de=u"Öffentlich",   fr=u"Public"))
    yield add('1',**babel_values('name',en=u"Private",de=u"Privat",   fr=u"Privé"))
    yield add('2',**babel_values('name',en=u"Confidential",de=u"Vertraulich",   fr=u"Confidentiel"))

    add = Instantiator('cal.Priority','ref').build
    yield add('1',**babel_values('name',en=u"very urgent",de=u"sehr dringend",   fr=u"très urgent"))
    yield add('2',**babel_values('name',en=u"quite urgent",de=u"recht dringend",   fr=u"relativement urgent"))
    yield add('3',**babel_values('name',en=u"relatively urgent",de=u"ziemlich dringend",   fr=u"relativement urgent"))
    yield add('4',**babel_values('name',en=u"relatively urgent",de=u"ziemlich dringend",   fr=u"relativement urgent"))
    yield add('5',**babel_values('name',en=u"normal",de=u"normal",   fr=u"normal"))
    yield add('6',**babel_values('name',en=u"not very urgent",de=u"nicht sehr niedrig",   fr=u"pas très urgent"))
    yield add('7',**babel_values('name',en=u"not urgent",de=u"nicht dringend",   fr=u"pas urgent"))
    yield add('8',**babel_values('name',en=u"not urgent",de=u"nicht dringend",   fr=u"pas urgent"))
    yield add('9',**babel_values('name',en=u"not urgent at all",de=u"überhaupt nicht dringend",   fr=u"pas urgent du tout"))
