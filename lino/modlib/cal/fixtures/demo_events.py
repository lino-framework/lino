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

"""
Generates a suite of ficive demo events.
"""

import decimal
from dateutil.relativedelta import relativedelta
ONE_DAY = relativedelta(days=1)

from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext as _


from lino.utils import i2d, Cycler
from lino.utils.instantiator import Instantiator
from lino.core.modeltools import resolve_model
from lino.utils.babel import babel_values

from lino.modlib.cal import models as cal

from lino import dd

def objects():
    
    if settings.LINO.project_model:
        PROJECTS = Cycler(settings.LINO.project_model.objects.all())
    USERS = Cycler(settings.LINO.user_model.objects.all())
    ETYPES = Cycler(cal.Calendar.objects.all())
    TIMES = Cycler(['08:30','09:40','10:20','11:10','13:30'])
    ACL = Cycler(cal.AccessClasses.items())
    SUMMARIES = Cycler((
      dict(en='Lunch',de=u"Mittagessen",fr=u"Diner")
      ,dict(en='Dinner',de=u"Abendessen",fr=u"Souper")
      ,dict(en='Breakfast',de=u"Frühstück",fr=u"Petit-déjeuner")
      ,dict(en='Meeting',de=u"Treffen",fr=u"Rencontre")
      ,dict(en='Consultation',de=u"Beratung",fr=u"Consultation")
      ,dict(en='Seminar',de=u"Seminar",fr=u"Séminaire")
      ,dict(en='Evaluation',de=u"Auswertung",fr=u"Evaluation")
      ,dict(en='First meeting',de=u"Erstgespräch",fr=u"Première rencontre")
      ,dict(en='Interview',de=u"Interview",fr=u"Interview")
      ))
    #~ for i in range(20):
    for u in settings.LINO.user_model.objects.exclude(email=''):
        u = USERS.pop()
        date = settings.LINO.demo_date()
        for i in range(12):
            if i % 3:
                date += relativedelta(days=1)
            s = SUMMARIES.pop().get(u.language,None) or SUMMARIES.pop().get('en')
            kw = dict(user=u,
              start_date=date,
              calendar=ETYPES.pop(),start_time=TIMES.pop(),
              summary=s)
            kw.update(access_class=ACL.pop())
            if settings.LINO.project_model:
                kw.update(project=PROJECTS.pop())
            yield cal.Event(**kw)
    #~ yield event(user=user,start_date=settings.LINO.demo_date(days=1),type=2)
    #~ yield event(user=user,start_date=settings.LINO.demo_date(days=2),type=2)
    
    #~ for u in settings.LINO.user_model.objects.all():
        for obj in settings.LINO.user_model.objects.exclude(
              profile=dd.UserProfiles.blank_item).exclude(id=u.id):
            yield cal.Membership(user=u,watched_user=obj)
        for obj in cal.Calendar.objects.all():
            yield cal.Subscription(user=u,calendar=obj)
    
    