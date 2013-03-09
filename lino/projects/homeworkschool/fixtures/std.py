# -*- coding: UTF-8 -*-
## Copyright 2012 Luc Saffre
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


from lino.utils.instantiator import Instantiator, i2d
from lino.core.dbutils import resolve_model
from django.utils.translation import ugettext_lazy as _


from django.conf import settings
from north.babel import babel_values, babelitem


def objects():
  
    mailType = Instantiator('notes.NoteType').build
    
    yield mailType(**babel_values('name',
        en="Enrolment",
        fr=u'Inscription',de=u"Einschreibeformular"))
    yield mailType(**babel_values('name',
        en="Timetable",
        fr=u'Horaire',de=u"Stundenplan"))
    yield mailType(**babel_values('name',
        en="Letter",
        fr=u'Lettre',de=u"Brief"))
