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
        [ cbss.IdentifyPersonRequest, 
          dict(last_name="MUSTERMANN",birth_date=IncompleteDate(1938,6,1)), 
          'demo_ipr_1.xml' ],
        [ cbss.IdentifyPersonRequest, 
          dict(last_name="MUSTERMANN",birth_date=IncompleteDate(1938,6,0)), 
          'demo_ipr_2.xml' ],
        [ cbss.IdentifyPersonRequest, 
          dict(last_name="MUSTERMANN",birth_date=IncompleteDate(1938,6,1)), 
          'demo_ipr_3.xml' ],
        [ cbss.IdentifyPersonRequest, 
          dict(last_name="MUSTERMANN",birth_date=IncompleteDate(1968,3,7)), 
          'demo_ipr_4.xml' ],
        [ cbss.IdentifyPersonRequest, 
          dict(last_name="MUSTERMANN",birth_date=IncompleteDate(1968,3,7)), 
          'demo_ipr_5.xml' ],
        [ cbss.ManageAccessRequest, dict(
            national_id='680601 053-29',
            birth_date=IncompleteDate(1968,6,1),
            start_date=settings.LINO.demo_date(),
            end_date=settings.LINO.demo_date(15),
            sector=cbss.Sector.objects.get(code=17,subcode=1),
            purpose=cbss.Purpose.objects.get(code=902),
            action=cbss.ManageAction.REGISTER,
            query_register=cbss.QueryRegister.ALL,
            ), '' ],
        [ cbss.RetrieveTIGroupsRequest, 
          dict(national_id='680601 053-29',history=False,language='de'), 
          'demo_tx25_1.xml' ],
        [ cbss.RetrieveTIGroupsRequest, 
          dict(national_id='680307 001-74',history=True), 
          'demo_tx25_2.xml' ],
    ]

    def objects():
      
        User = dd.resolve_model(settings.LINO.user_model)
        root = User.objects.get(username='root')
        Person = dd.resolve_model(settings.LINO.person_model)
        #~ PERSONS = Cycler(Person.objects.filter(coached_from__isnull=False).order_by('id'))
        PERSONS = Cycler(Person.objects.all().order_by('id'))
        mustermann = PERSONS.pop()
        for model,kw,fn in DEMO_REQUESTS:
            kw.update(person=mustermann)
            kw.update(user=root)
            obj = model(**kw)
            if fn:
                fn = os.path.join(os.path.dirname(__file__),fn)
                xml = open(fn).read()
                obj.execute_request(simulate_response=xml)
                #~ print obj.debug_messages
            yield obj
            
            
        #~ Company = resolve_model('contacts.Company')
        #~ settings.LINO.site_config.site_company = Company.objects.get(pk=1)
        #~ settings.LINO.site_config.save()
            