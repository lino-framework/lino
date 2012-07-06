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
from lino.utils import Cycler
from lino.core.modeltools import resolve_model
# from django.utils.translation import ugettext_lazy as _

#~ from django.db import models
from lino.utils.babel import babel_values, babelitem
from lino.core.perms import UserProfiles

def objects():
  
    #~ from lino.modlib.users.models import 
    from lino.modlib.newcomers.models import Broker, Faculty, Competence
    from lino.apps.pcsw.models import Person
    
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
    
    
    #~ root = User.objects.get(username="root")
    #~ root.newcomers_level = UserLevel.expert
    #~ root.save()

    #~ I = Instantiator(User).build
    #~ yield I(username="caroline",is_newcomers=True,first_name="Caroline",last_name="Carnol")
    #~ yield I(username="caroline",newcomers_level=UserLevel.user,first_name="Caroline",last_name="Carnol")
    
    User = resolve_model('users.User')
    yield User(username="caroline",
        first_name="Caroline",last_name="Carnol",
        profile='200') # UserProfiles.caroline)
        #~ newcomers_level=UserLevel.user)
    #~ yield I(username="doris",first_name="Doris",last_name="Decker",profile='caroline')
    
    FACULTIES = Cycler(Faculty.objects.all())
    #~ USERS = Cycler(User.objects.filter(is_spis=True))
    #~ USERS = Cycler(User.objects.filter(integ_level__isnull=False))
    profiles = [p for p in UserProfiles.items() if p.integ_level]
    #~ USERS = Cycler(User.objects.filter(profile__in=(UserProfiles.melanie,UserProfiles.hubert)))
    USERS = Cycler(User.objects.filter(profile__in=profiles))
    for i in range(7):
        yield Competence(user=USERS.pop(),faculty=FACULTIES.pop())
    for p in Person.objects.filter(newcomer=True):
        p.faculty = FACULTIES.pop()
        p.save()