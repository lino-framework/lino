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

import traceback
import datetime

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from lino import mixins
from lino import fields
from lino import reports

from lino.utils import babel
from lino.utils import dblogger
from lino.tools import resolve_model

from lino.reports import GridEdit, ShowDetailAction

class SendAction(reports.RowAction):
    name = 'sendbcss'
    label = _('Execute')
    #~ callable_from = None
    callable_from = (GridEdit,ShowDetailAction)
    
    def run(self,rr,elem,**kw):
        elem.execute_request()
        kw.update(refresh=True)
        return rr.ui.success_response(**kw)


class BCSSRequest(mixins.ProjectRelated,mixins.AutoUser):
    """
    
    Abstract Base class for models that represent 
    requests to the :term:`BCSS` (and responses).
    """
    class Meta:
        abstract = True
        
    sent = models.DateTimeField(verbose_name=_("Sent"),
        blank=True,null=True,
        editable=False)
    request_xml = models.TextField(verbose_name=_("Request"),blank=True)
    response_xml = models.TextField(verbose_name=_("Response"),blank=True)
    
    def execute_request(self):
        if not self.id:
            self.save()
        srv = self.build_service()
        now = datetime.datetime.now()
        self.sent = now
        self.request_xml = srv.toxml(True)
        self.response_xml = "Pending..."
        self.save()
        
        try:
            res = srv.execute(settings,str(self.id),now)
            self.response_xml = res.data.xmlString
        except Exception,e:
            self.response_xml = traceback.format_exc(e)
        self.save()
        
    @classmethod
    def setup_report(cls,rpt):
        #~ call_optional_super(BCSSRequest,cls,'setup_report',rpt)
        rpt.add_action(SendAction())
        
    def __unicode__(self):
        return u"%s#%s" % (self.__class__.__name__,self.pk)
        
        
class IdentifyPersonRequest(BCSSRequest):
    """
    Represents a request to the :term:`BCSS` IdentifyPerson service.
    If the person has her `national_id` field filled, 
    it does a *verification* of the personal data,
    Otherwise it does a search request on the person's last_name, 
    first_name and (if filled) birth_date and gender fields.
    """
    def build_service(self):
        person = self.project
        from lino.utils import bcss 
        VD = bcss.IdentifyPersonRequest.VerificationData
        SC = bcss.IdentifyPersonRequest.SearchCriteria
        PC = SC.PhoneticCriteria
        if person.national_id:
            national_id = person.national_id.replace(' ','')
            national_id = national_id.replace('-','')
            national_id = national_id.replace('=','')
            return bcss.IdentifyPersonRequest.verify_request(
              national_id,
              LastName=person.last_name,
              FirstName=person.last_name,
              BirthDate=person.birth_date,
              )
            #~ ip = [SC(SC.SSIN(person.national_id))]
            #~ vd = []
            #~ if person.card_number:
                #~ vd.append(VD.IdentityCardNumber(person.card_number))
            #~ vd.append(VD.PersonData(
              #~ VD.PersonData.LastName(person.last_name),
              #~ VD.PersonData.FirstName(person.last_name),
              #~ VD.PersonData.BirthDate(person.birth_date)))
            #~ ip.append(VD(*vd))
            #~ return bcss.IdentifyPersonRequest(*ip)
        else:
          pc = []
          pc.append(PC.LastName(person.last_name))
          pc.append(PC.FirstName(person.first_name))
          if person.birth_date:
              pc.append(PC.BirthDate(person.birth_date))
          if person.gender:
              from lino.modlib.contacts.utils import GENDER_MALE, GENDER_FEMALE
              if person.gender == GENDER_MALE:
                  pc.append(PC.Gender(1))
              elif person.gender == GENDER_FEMALE:
                  pc.append(PC.Gender(2))
          return bcss.IdentifyPersonRequest(SC(PC(*pc)))
      
class IdentifyRequestsByPerson(reports.Report):
    model = IdentifyPersonRequest
    fk_name = 'project'