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


from lino.utils.instantiator import Instantiator, i2d
from lino.utils import Cycler
#~ from lino.tools import resolve_model
# from django.utils.translation import ugettext_lazy as _

#~ from django.db import models
from lino.utils.babel import babel_values, babelitem

def objects():
  
    from lino.modlib.users.models import User
    from lino.modlib.newcomers.models import Broker, Faculty, Competence
    from lino.apps.dsbe.models import Person
    
    I = Instantiator(Broker).build
    #~ yield I(**babel_values('name',
        #~ de=u"Polizei", fr=u"Police",en=u"Police"))
    #~ yield I(**babel_values('name',
        #~ de=u"Jugendgericht", fr=u"Jugendgericht",en=u"Jugendgericht"))
    yield I(name="Police")
    yield I(name="Other PCSW")

    I = Instantiator(Faculty).build
    yield I(**babel_values('name', de=u"Eingliederungseinkommen", fr=u"EiEi",en=u"EiEi"))
    yield I(**babel_values('name', de=u"DSBE", fr=u"DSBE",en=u"DSBE"))
    yield I(**babel_values('name', de=u"Ausländerbeihilfe", fr=u"Ausländerbeihilfe",en=u"Ausländerbeihilfe"))
    yield I(**babel_values('name', de=u"Finanzielle Begleitung", fr=u"Finanzielle Begleitung",en=u"Finanzielle Begleitung"))
    yield I(**babel_values('name', de=u"Laufende Beihilfe", fr=u"Laufende Beihilfe",en=u"Laufende Beihilfe"))
    
    root = User.objects.get(username="root")
    root.is_newcomers = True
    root.save()

    I = Instantiator(User).build
    yield I(username="caroline",is_newcomers=True)
    
    FACULTIES = Cycler(Faculty.objects.all())
    USERS = Cycler(User.objects.filter(is_spis=True))
    for i in range(7):
        yield Competence(user=USERS.pop(),faculty=FACULTIES.pop())
    for p in Person.objects.filter(newcomer=True):
        p.faculty = FACULTIES.pop()
        p.save()