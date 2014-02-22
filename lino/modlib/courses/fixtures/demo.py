# -*- coding: UTF-8 -*-
# Copyright 2012-2014 Luc Saffre
# This file is part of the Lino project.
# Lino is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
# Lino is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
# You should have received a copy of the GNU Lesser General Public License
# along with Lino; if not, see <http://www.gnu.org/licenses/>.

from __future__ import unicode_literals

import datetime

from lino import dd
from lino.utils import mti, Cycler
from django.utils.translation import ugettext_lazy as _


from django.conf import settings

Person = dd.resolve_model('contacts.Person')

courses = dd.resolve_app('courses')
cal = dd.resolve_app('cal')
users = dd.resolve_app('users')


def objects():

    #~ yield courses.Room(name="A")
    #~ yield cal.Place(name="A")
    #~ yield cal.Place(name="B")
    #~ yield cal.Place(name="C")
    #~ yield cal.Place(name="D")
    #~ yield cal.Place(name="E")
    #~ yield cal.Place(name="F")
    PTYPES = Cycler(courses.PupilType.objects.all())
    TTYPES = Cycler(courses.TeacherType.objects.all())

    n = 0
    for p in Person.objects.all():
        if n % 2 == 0:
            yield mti.insert_child(p, courses.Pupil,
                                   pupil_type=PTYPES.pop())
        if n % 9 == 0:
            yield mti.insert_child(p, courses.Teacher,
                                   teacher_type=TTYPES.pop())
        n += 1

    if False:

        #~ PS = Cycler(courses.PresenceStatus.objects.all())
        CONTENTS = Cycler(courses.Line.objects.all())
        USERS = Cycler(users.User.objects.all())
        PLACES = Cycler(cal.Room.objects.all())
        TEACHERS = Cycler(courses.Teacher.objects.all())
        SLOTS = Cycler(courses.Slot.objects.all())
        #~ SLOTS = Cycler(1,2,3,4)
        PUPILS = Cycler(courses.Pupil.objects.all())
        #~ Event = settings.SITE.modules.cal.Event

        #~ from lino.modlib.cal.utils import DurationUnit

        year = settings.SITE.demo_date().year
        if settings.SITE.demo_date().month < 7:
            year -= 1
        for i in range(10):
            c = courses.Course(
                user=USERS.pop(),
                teacher=TEACHERS.pop(),
                line=CONTENTS.pop(), room=PLACES.pop(),
                start_date=datetime.date(year, 9, 1 + i),
                end_date=datetime.date(year + 1, 6, 30),
                every=1,
                every_unit=cal.DurationUnits.weeks,
                slot=SLOTS.pop(),
            )
            yield c
            for j in range(5):
                yield courses.Enrolment(pupil=PUPILS.pop(), course=c)

            c.save()  # fill presences

            #~ for j in range(5):
                #~ yield courses.Event(start_date=settings.SITE.demo_date(j*7),course=c)
                #~ yield courses.Presence()
