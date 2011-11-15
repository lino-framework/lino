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
Lino-specific extensions to make the :term:`BCSS` 
connection visible.

"""

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
from lino.utils import bcss

from lino.reports import GridEdit, ShowDetailAction
from appy.shared.xml_parser import XmlUnmarshaller

from lino.utils.choicelists import ChoiceList

class RequestStatus(ChoiceList):
    """
    The status of a :class:`BCSSRequest`.
    """
    label = _("Status")

add = RequestStatus.add_item
add('0',_("New"),alias='new')
add('1',_("Pending"),alias='pending')
add('2',_("Exception"),alias='exception')
add('3',_("OK"),alias='ok')
add('4',_("Warnings"),alias='warnings')
add('5',_("Errors"),alias='errors')
  

    
    


class SendAction(reports.RowAction):
    """
    This defines the "Execute" button on a :class:`BCSSRequest` record.
    """
    name = 'sendbcss'
    label = _('Execute')
    #~ callable_from = None
    callable_from = (GridEdit,ShowDetailAction)
    
    def disabled_for(self,obj,request):
        if obj.sent:
            return True
    
    def run(self,rr,elem,**kw):
        elem.execute_request()
        if elem.status == RequestStatus.warnings:
            kw.update(message=_("There were warnings but no errors."))
            kw.update(alert=True)
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
    request_xml = models.TextField(verbose_name=_("Request"),editable=False,blank=True)
    response_xml = models.TextField(verbose_name=_("Response"),editable=False,blank=True)
    status = RequestStatus.field(default=RequestStatus.new,editable=False)
    
    def execute_request(self):
        """
        This is the general method executed when a user runs :class:`SendAction`.
        """
        if not self.id:
            self.save()
        srv = self.build_service()
        now = datetime.datetime.now()
        self.request_xml = srv.toxml(True)
        self.status = RequestStatus.pending
        self.save()
        
        try:
            res = srv.execute(settings,str(self.id),now)
        except Exception,e:
            self.status = RequestStatus.exception
            self.response_xml = traceback.format_exc(e)
            self.save()
            return
            
        self.sent = now
        self.response_xml = res.data.xmlString
        reply = bcss.xml2reply(res.data.xmlString)
        rc = reply.ServiceReply.ResultSummary.ReturnCode
        if rc == '0':
            self.status = RequestStatus.ok
        elif rc == '1':
            self.status = RequestStatus.warnings
        elif rc == '10000':
            self.status = RequestStatus.errors
        self.save()
        
        if self.status != RequestStatus.ok:
            msg = '\n'.join(list(reply2lines(reply)))
            raise Exception(msg)
            
        self.on_bcss_ok(reply)
        
    def on_bcss_ok(self):
        """
        Called when a successful reply has been received.
        """
        pass
        
    @classmethod
    def setup_report(cls,rpt):
        #~ call_optional_super(BCSSRequest,cls,'setup_report',rpt)
        rpt.add_action(SendAction())
        
    def __unicode__(self):
        return u"%s#%s" % (self.__class__.__name__,self.pk)
        
        
class IdentifyPersonRequest(BCSSRequest):
    """
    Represents a request to the :term:`BCSS` IdentifyPerson service.
    
    """
    def build_service(self):
        """
        If the person has her `national_id` field filled, 
        it does a *verification* of the personal data,
        Otherwise it does a search request on the person's last_name, 
        first_name and (if filled) birth_date and gender fields.
        """
        person = self.project
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
              FirstName=person.first_name,
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
          pc.append(PC.MiddleName(''))
          if person.birth_date:
              pc.append(PC.BirthDate(person.birth_date))
          if person.gender:
              from lino.modlib.choicelists import Gender
              if person.gender == Gender.male:
                  pc.append(PC.Gender(1))
              elif person.gender == Gender.female:
                  pc.append(PC.Gender(2))
          return bcss.IdentifyPersonRequest(SC(PC(*pc)))
      
class IdentifyRequestsByPerson(reports.Report):
    model = IdentifyPersonRequest
    fk_name = 'project'