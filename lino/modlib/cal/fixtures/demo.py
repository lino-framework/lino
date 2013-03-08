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


from lino.utils import i2d, Cycler
from lino.utils.instantiator import Instantiator
from lino.core.dbutils import resolve_model
from north.babel import babel_values

from lino.modlib.cal import models as cal


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
          
    calendar = Instantiator('cal.Calendar').build
    #~ yield calendar(**babel_values('name',
          #~ de=u"Klientengespräche intern",
          #~ fr=u"Rencontres internes avec client",
          #~ en=u"Internal meetings with client",
          #~ ))
    yield calendar(color=1,**babel_values('name',
          de=u"Klientengespräche extern",
          fr=u"Rencontres client externes",
          en=u"External meetings with client",
          ))
    
    yield calendar(color=4,**babel_values('name',
          de=u"Versammlung intern",
          fr=u"Réunions internes",
          en=u"Internal meetings",
          ))
    
    yield calendar(color=8,**babel_values('name',
          de=u"Versammlung extern",
          fr=u"Réunions externes",
          en=u"External meetings",
          ))
          
    yield calendar(color=12,
        invite_team_members=True,email_template='Team.eml.html',
        **babel_values('name',
          de=u"Team-Besprechungen",
          fr=u"Coordinations en équipe",
          en=u"Team Meetings",
          ))
    #~ yield etype(**babel_values('name',
          #~ de=u"Erstgespräch",
          #~ fr=u"Première rencontre",
          #~ en=u"First meeting",
          #~ ))
    #~ yield etype(**babel_values('name',
          #~ de=u"Auswertungsgespräch",
          #~ fr=u"Évaluation",
          #~ en=u"Evaluation",
          #~ ))
    
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

