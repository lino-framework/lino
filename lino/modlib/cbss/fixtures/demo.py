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

"""
Fills in a suite of fictive CBSS requests.
"""

import os
from django.conf import settings
from lino.utils import IncompleteDate, Cycler
#~ from lino.modlib.cbss import models as cbss
from lino import dd
cbss = dd.resolve_app('cbss')

if cbss:
  
    DEMO_REQUESTS = [
        [ cbss.IdentifyPersonRequest, dict(last_name="MUSTERMANN",birth_date=IncompleteDate(1938,6,1)), 'demo_ipr_1.xml' ],
        [ cbss.IdentifyPersonRequest, dict(last_name="MUSTERMANN",birth_date=IncompleteDate(1938,6,0)), 'demo_ipr_2.xml' ],
        [ cbss.ManageAccessRequest, dict(
            national_id='01234567890',
            start_date=settings.LINO.demo_date(),
            end_date=settings.LINO.demo_date(15),
            purpose=902,
            action=cbss.ManageAction.REGISTER,
            query_register=cbss.QueryRegister.ALL,
            ), '' ],
    ]

    def objects():
        User = dd.resolve_model(settings.LINO.user_model)
        Person = dd.resolve_model(settings.LINO.person_model)
        PERSONS = Cycler(Person.objects.filter(coached_from__isnull=False).order_by('id'))
        for model,kw,fn in DEMO_REQUESTS:
            kw.update(person=PERSONS.pop())
            kw.update(user=User.objects.get(username='root'))
            obj = model(**kw)
            if fn:
                fn = os.path.join(os.path.dirname(__file__),fn)
                xml = open(fn).read()
                obj.execute_request(simulate_response=xml)
            yield obj