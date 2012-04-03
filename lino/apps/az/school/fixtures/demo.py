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

import datetime

#~ from django.contrib.contenttypes.models import ContentType
#~ from lino.utils.instantiator import Instantiator, i2d
from lino.tools import resolve_model
from lino.utils import mti, Cycler
from django.utils.translation import ugettext_lazy as _


from django.db import models
from django.conf import settings
from lino.utils.babel import babel_values

Person = resolve_model('contacts.Person')
#~ Room = resolve_model('courses.Room')
#~ Content = resolve_model('courses.Content')
#~ PresenceStatus = resolve_model('courses.PresenceStatus')

from lino.apps.az.school import models as school
from lino.modlib.cal import models as cal

def objects():
  
    #~ yield school.PresenceStatus(**babel_values('name',
          #~ de=u"Anwesend",
          #~ fr=u"présent",
          #~ en=u"present",
          #~ ))
    #~ yield school.PresenceStatus(**babel_values('name',
          #~ de=u"Abwesend",
          #~ fr=u"absent",
          #~ en=u"absent",
          #~ ))
    #~ yield school.PresenceStatus(**babel_values('name',
          #~ de=u"Entschuldigt",
          #~ fr=u"excusé",
          #~ en=u"excused",
          #~ ))
    yield school.Content(**babel_values('name',
          de=u"Deutsch Anfänger",
          fr=u"Allemand débutants",
          en=u"German beginners",
          ))
    yield school.Content(**babel_values('name',
          de=u"Französisch Anfänger",
          fr=u"Français débutants",
          en=u"French beginners",
          ))
          
    #~ def slotkw(weekday,hour,**kw):
        #~ if hour == 1:
            #~ kw.update(start_time="13:00",end_time="14:00")
        #~ elif hour == 2:
            #~ kw.update(start_time="14:00",end_time="15:00")
        #~ elif hour == 3:
            #~ kw.update(start_time="15:00",end_time="16:00")
        #~ elif hour == 4:
            #~ kw.update(start_time="16:00",end_time="17:00")
        #~ elif hour == 5:
            #~ kw.update(start_time="17:00",end_time="18:00")
        #~ elif hour == 6:
            #~ kw.update(start_time="18:00",end_time="19:00")
        #~ return kw
        
    #~ for weekday in ("1","2","3","4","5"):
        #~ for n in [i+1 for i in range(5)]:
            #~ yield school.Slot(weekday=weekday,n,**slotkw(weekday,n))
            
    #~ yield school.Room(name="A")
    yield cal.Place(name="A")
    yield cal.Place(name="B")
    yield cal.Place(name="C")
    yield cal.Place(name="D")
    yield cal.Place(name="E")
    yield cal.Place(name="F")

    n = 0
    for p in Person.objects.all():
        if n % 3 == 0:
            yield mti.insert_child(p,school.Pupil)
        if n % 10 == 0:
            yield mti.insert_child(p,school.Teacher)
        n += 1
        
    #~ PS = Cycler(school.PresenceStatus.objects.all())
    CONTENTS = Cycler(school.Content.objects.all())
    TEACHERS = Cycler(school.Teacher.objects.all())
    #~ SLOTS = Cycler(school.Slot.objects.all())
    SLOTS = Cycler(1,2,3,4)
    PUPILS = Cycler(school.Pupil.objects.all())
    PLACES = Cycler(cal.Place.objects.all())
    #~ Event = settings.LINO.modules.cal.Event
    
    from lino.modlib.cal.models import DurationUnit
    
    year = settings.LINO.demo_date().year
    if settings.LINO.demo_date().month < 7:
        year -= 1
    for i in range(10):
        c = school.Course(user=TEACHERS.pop(),
          content=CONTENTS.pop(),place=PLACES.pop(),
          start_date=datetime.date(year,9,1+i),
          end_date=datetime.date(year+1,6,30),
          every=1,
          every_unit=DurationUnit.weeks,
          slot=SLOTS.pop(),
          )
        yield c
        for j in range(5):
            yield school.Enrolment(pupil=PUPILS.pop(),course=c)
            
        c.save() # fill presences
        
        #~ for j in range(5):
            #~ yield school.Event(start_date=settings.LINO.demo_date(j*7),course=c)
            #~ yield school.Presence()
        