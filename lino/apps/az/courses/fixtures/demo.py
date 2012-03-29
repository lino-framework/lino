# -*- coding: UTF-8 -*-
## Copyright 2012 Luc Saffre
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


#~ from django.contrib.contenttypes.models import ContentType
#~ from lino.utils.instantiator import Instantiator, i2d
from lino.tools import resolve_model
from lino.utils import mti
from django.utils.translation import ugettext_lazy as _


from django.db import models
from django.conf import settings
from lino.utils.babel import babel_values

Person = resolve_model('contacts.Person')
#~ Room = resolve_model('courses.Room')
#~ Content = resolve_model('courses.Content')
#~ PresenceStatus = resolve_model('courses.PresenceStatus')

from lino.apps.az.courses import models as courses

def objects():
  
    yield courses.PresenceStatus(**babel_values('name',
          de=u"Anwesend",
          fr=u"présent",
          en=u"present",
          ))
    yield courses.PresenceStatus(**babel_values('name',
          de=u"Abwesend",
          fr=u"absent",
          en=u"absent",
          ))
    yield courses.PresenceStatus(**babel_values('name',
          de=u"Entschuldigt",
          fr=u"excusé",
          en=u"excused",
          ))
    yield courses.Content(**babel_values('name',
          de=u"Deutsch Anfänger",
          fr=u"Allemand débutants",
          en=u"German beginners",
          ))
    yield courses.Content(**babel_values('name',
          de=u"Französisch Anfänger",
          fr=u"Français débutants",
          en=u"French beginners",
          ))
    yield courses.Room(name="A")
    yield courses.Room(name="B")
    yield courses.Room(name="C")
    yield courses.Room(name="D")
    yield courses.Room(name="E")
    yield courses.Room(name="F")

    n = 0
    for p in Person.objects.all():
        if n % 3 == 0:
            yield mti.insert_child(p,courses.Pupil)
        if n % 10 == 0:
            yield mti.insert_child(p,courses.Teacher)
        n += 1
        