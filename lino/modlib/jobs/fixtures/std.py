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


from lino.utils.instantiator import Instantiator, i2d
#~ from lino.tools import resolve_model
#~ from django.utils.translation import ugettext_lazy as _

#~ from django.db import models
from lino.utils.babel import babel_values, babelitem

def objects():
  
    regime = Instantiator('jobs.Regime').build
    yield regime(**babel_values('name',
        de=u"20 Stunden/Woche", fr=u"20 heures/semaine",en=u"20 hours/week"))
    yield regime(**babel_values('name',
        de=u"35 Stunden/Woche", fr=u"35 heures/semaine",en=u"35 hours/week"))
    yield regime(**babel_values('name',
        de=u"38 Stunden/Woche", fr=u"38 heures/semaine",en=u"38 hours/week"))
  
    schedule = Instantiator('jobs.Schedule').build
    yield schedule(**babel_values('name',
        de=u"5-Tage-Woche",              fr=u"5 jours/semaine",         en=u"5 days/week"))
    yield schedule(**babel_values('name',
        de=u"Individuell",               fr=u"individuel",              en=u"Individual"))
    yield schedule(**babel_values('name',
        de=u"Montag, Mittwoch, Freitag", fr=u"lundi,mercredi,vendredi", en=u"Monday, Wednesday, Friday"))


