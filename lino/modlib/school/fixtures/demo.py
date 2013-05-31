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

from __future__ import unicode_literals

import datetime

#~ from django.contrib.contenttypes.models import ContentType

from lino import dd
#~ from lino.utils.instantiator import Instantiator, i2d
#~ from lino.core.dbutils import resolve_model
from lino.utils import mti, Cycler
from django.utils.translation import ugettext_lazy as _


from django.db import models
from django.conf import settings
from north.dbutils import babelkw

Person = dd.resolve_model('contacts.Person')

school = dd.resolve_app('school')
cal = dd.resolve_app('cal')
users = dd.resolve_app('users')
#~ Room = resolve_model('courses.Room')
#~ Content = resolve_model('courses.Content')
#~ PresenceStatus = resolve_model('courses.PresenceStatus')


def objects():
  
            
    #~ yield school.Room(name="A")
    #~ yield cal.Place(name="A")
    #~ yield cal.Place(name="B")
    #~ yield cal.Place(name="C")
    #~ yield cal.Place(name="D")
    #~ yield cal.Place(name="E")
    #~ yield cal.Place(name="F")

    PTYPES = Cycler(school.PupilType.objects.all())
    TTYPES = Cycler(school.TeacherType.objects.all())
    
    n = 0
    for p in Person.objects.all():
        if n % 2 == 0:
            yield mti.insert_child(p,school.Pupil,pupil_type=PTYPES.pop())
        if n % 9 == 0:
            yield mti.insert_child(p,school.Teacher,teacher_type=TTYPES.pop())
        n += 1
        
    if False:
        
        #~ PS = Cycler(school.PresenceStatus.objects.all())
        CONTENTS = Cycler(school.Line.objects.all())
        USERS = Cycler(users.User.objects.all())
        PLACES = Cycler(cal.Room.objects.all())
        TEACHERS = Cycler(school.Teacher.objects.all())
        SLOTS = Cycler(school.Slot.objects.all())
        #~ SLOTS = Cycler(1,2,3,4)
        PUPILS = Cycler(school.Pupil.objects.all())
        #~ Event = settings.SITE.modules.cal.Event
        
        #~ from lino.modlib.cal.utils import DurationUnit
        
        year = settings.SITE.demo_date().year
        if settings.SITE.demo_date().month < 7:
            year -= 1
        for i in range(10):
            c = school.Course(
              user=USERS.pop(),
              teacher=TEACHERS.pop(),
              line=CONTENTS.pop(),room=PLACES.pop(),
              start_date=datetime.date(year,9,1+i),
              end_date=datetime.date(year+1,6,30),
              every=1,
              every_unit=cal.DurationUnits.weeks,
              slot=SLOTS.pop(),
              )
            yield c
            for j in range(5):
                yield school.Enrolment(pupil=PUPILS.pop(),course=c)
                
            c.save() # fill presences
            
            #~ for j in range(5):
                #~ yield school.Event(start_date=settings.SITE.demo_date(j*7),course=c)
                #~ yield school.Presence()
            
