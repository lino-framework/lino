# -*- coding: UTF-8 -*-
## Copyright 2011 Luc Saffre
## This file is part of the Lino project.
## Lino is free software; you can redistribute it and/or modify 
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 3 of the License, or
## (at your option) any later version.
## Lino is distributed in the hope that it will be useful, 
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
## GNU General Public License for more details.
## You should have received a copy of the GNU General Public License
## along with Lino; if not, see <http://www.gnu.org/licenses/>.

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
          
    etype = Instantiator('cal.EventType').build
    yield etype(**babel_values('name',
          de=u"Besprechung",
          fr=u"Coordination",
          en=u"Coordination",
          ))
    yield etype(**babel_values('name',
          de=u"Erstgespräch",
          fr=u"Première rencontre",
          en=u"First meeting",
          ))
    yield etype(**babel_values('name',
          de=u"Auswertungsgespräch",
          fr=u"Évaluation",
          en=u"Evaluation",
          ))
    
    place = Instantiator('cal.Place').build
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

    #~ event = Instantiator('cal.Event','user:username').build
    #~ yield event("user",start_date=settings.LINO.demo_date(),type=1)
    #~ yield event("user",start_date=settings.LINO.demo_date(days=1),type=2)
    #~ yield event("user",start_date=settings.LINO.demo_date(days=2),type=2)
    User = resolve_model('users.User')
    #~ Event = resolve_model('cal.Event')
    user = User.objects.get(username='user')
    event = Instantiator('cal.Event').build
    yield event(user=user,start_date=settings.LINO.demo_date(),type=1)
    yield event(user=user,start_date=settings.LINO.demo_date(days=1),type=2)
    yield event(user=user,start_date=settings.LINO.demo_date(days=2),type=2)
    