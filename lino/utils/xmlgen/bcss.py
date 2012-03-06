# -*- coding: UTF-8 -*-
## Copyright 2011-2012 Luc Saffre
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

This module is deprecated. 
Use :mod:`lino.utils.bcss` instead.
See :doc:`/blog/2012/0301` and :doc:`/blog/2012/0302`

Communicate with the :term:`BCSS` server.

Example:

>>> req = ipr.verify_request("68060101234",
...   LastName="SAFFRE",BirthDate='1968-06-01')
>>> print req.tostring(True)
<ipr:IdentifyPersonRequest xmlns:ipr="http://www.ksz-bcss.fgov.be/XSD/SSDN/OCMW_CPAS/IdentifyPerson">
<ipr:SearchCriteria>
<ipr:SSIN>68060101234</ipr:SSIN>
</ipr:SearchCriteria>
<ipr:VerificationData>
<ipr:PersonData>
<ipr:LastName>SAFFRE</ipr:LastName>
<ipr:BirthDate>1968-06-01</ipr:BirthDate>
</ipr:PersonData>
</ipr:VerificationData>
</ipr:IdentifyPersonRequest>

>>> req = pir.perform_investigation("6806010123",wait="0")
>>> print req.tostring(True)
<pir:PerformInvestigationRequest xmlns:pir="http://www.ksz-bcss.fgov.be/XSD/SSDN/OCMW_CPAS/PerformInvestigation">
<pir:SocialSecurityUser>6806010123</pir:SocialSecurityUser>
<pir:DataGroups>
<pir:FamilyCompositionGroup>1</pir:FamilyCompositionGroup>
<pir:CitizenGroup>1</pir:CitizenGroup>
<pir:AddressHistoryGroup>1</pir:AddressHistoryGroup>
<pir:WaitRegisterGroup>0</pir:WaitRegisterGroup>
</pir:DataGroups>
</pir:PerformInvestigationRequest>

The above examples are bare BCSS service requests.
Before sending a request to the BCSS server, 
we must wrap it into a "SSDN request".
The easiest way to do this is to use the 
:meth:`Service.ssdn_request` method.

:meth:`Service.ssdn_request` wants the 
"user parameters" for the BCSS as a dict:

>>> user_params = dict(
...     UserID='123456', 
...     Email='info@exemple.be', 
...     OrgUnit='0123456', 
...     MatrixID=17, 
...     MatrixSubID=1)

(In a Lino application, these user parameters 
are set once in your local :xfile:`settings.py` 
module :attr:`lino.Lino.bcss_user_params`.)

:meth:`Service.ssdn_request` also expects a unique reference 
and a timestamp for your request:

>>> now = datetime.datetime(2011,10,31,15,41,10)
>>> unique_id = 'PIR # 5'

Here we go:

>>> sr = req.ssdn_request(user_params,unique_id,now)
>>> print sr.tostring(True,namespace=ssdn) #doctest: +ELLIPSIS
<SSDNRequest xmlns="http://www.ksz-bcss.fgov.be/XSD/SSDN/Service">
<RequestContext>
<AuthorizedUser>
<UserID>123456</UserID>
<Email>info@exemple.be</Email>
<OrgUnit>0123456</OrgUnit>
<MatrixID>17</MatrixID>
<MatrixSubID>1</MatrixSubID>
</AuthorizedUser>
<Message>
<Reference>PIR # 5</Reference>
<TimeRequest>20111031T154110</TimeRequest>
</Message>
</RequestContext>
<ServiceRequest>
<ServiceId>OCMWCPASPerformInvestigation</ServiceId>
<Version>20080604</Version>
<pir:PerformInvestigationRequest xmlns:pir="http://www.ksz-bcss.fgov.be/XSD/SSDN/OCMW_CPAS/PerformInvestigation">
...
</pir:PerformInvestigationRequest>
</ServiceRequest>
</SSDNRequest>

Now we perform another wrapping of this SSDN request.

>>> print soap.request("Foo").tostring(True)
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
<soap:Body>
<bcss:xmlString xmlns:bcss="http://ksz-bcss.fgov.be/connectors/WebServiceConnector">
<![CDATA[Foo]]>
</bcss:xmlString>
</soap:Body>
</soap:Envelope>

Element-level validation:

>>> G = ipr.PhoneticCriteria.Gender

>>> G(4)
Traceback (most recent call last):
...
Exception: Bad value 4 for Gender : Must be one of (0, 1, 2).

>>> print G(2).tostring(namespace=ipr,declare_namespaces=False)
<Gender>2</Gender>

Birth dates
-----------

>>> B = ipr.PhoneticCriteria.BirthDate

A birth date with missing month and day:

>>> print B('1978-00-00').tostring(namespace=ipr,declare_namespaces=False)
<BirthDate>1978-00-00</BirthDate>

BCSS requires at least the year of a birth date:

>>> node = B('0000-04-27')
Traceback (most recent call last):
...
Exception: Bad value IncompleteDate('0000-04-27') for BirthDate : Year may not be 0

A normal birth date instantiated from a `datetime.date`:

>>> print B(datetime.date(1968,6,1)).tostring(namespace=ipr,declare_namespaces=False)
<BirthDate>1968-06-01</BirthDate>

An empty birth date:

>>> print B('').tostring(namespace=ipr,declare_namespaces=False)
<BirthDate/>


"""


import datetime

from appy.shared.dav import Resource
#~ from appy import Object
from appy.shared.xml_parser import XmlUnmarshaller

#~ from lino.utils.xmlgen import *
from lino.utils import d2iso
from lino.utils import IncompleteDate
from lino.utils import xmlgen as xg

class bcss(xg.Namespace):
  
    url = "http://ksz-bcss.fgov.be/connectors/WebServiceConnector"
    
    class xmlString(xg.Container):
        pass

class soap(xg.Namespace):
    """
    Our simplified representation of the SOAP Schema
    """
    url = "http://schemas.xmlsoap.org/soap/envelope/" 
    class Envelope(xg.Container):
        pass
    class Body(xg.Container):
        pass

    @classmethod
    def request(soap,xmlString):
        #~ xg.set_default_namespace(bcss)
        body = bcss.xmlString(xg.CDATA(xmlString)).tostring()
        return soap.Envelope(soap.Body(body))
        
  
#~ class com(xg.Namespace):
    #~ url = "http://www.ksz-bcss.fgov.be/XSD/SSDN/Common"
    #~ class SSIN(String): pass
      
class SSINType(xg.String):
    u"""
    Belgian Social Security Identification Number.
    AKA as "Numéro d'identification au régistre national".
    """
    def validate(self):
        if len(self.value) != 11:
            self.badValue("length must be 11")
        if not self.value.isdigit():
            self.badValue("must be a number")
        

class t_IncompleteDate(xg.Element):
    
    def parse_value(self):
        if isinstance(self.value,datetime.date):
            self.value = IncompleteDate.from_date(self.value)
        if isinstance(self.value,basestring):
            self.value = IncompleteDate.parse(self.value)
        
    def validate(self):
        if not isinstance(self.value,IncompleteDate):
            self.badValue("Must be an IncompleteDate instance")
        if self.value.year == 0:
            self.badValue("Year may not be 0")
        xg.Element.validate(self)
      
        #~ if isinstance(v,datetime.date):
            #~ v = IncompleteDate(v)
        #~ elif isinstance(v,basestring):
            #~ v = IncompleteDate.parse(v)
        #~ if isinstance(v,IncompleteDate):
            #~ return xg.Element.validate(self,v)
        #~ raise Exception("%r is not a valid value for Date element" % v)
        
    def value_as_string(self):
        return str(self.value)

        
      
  
class common(xg.Namespace):
    prefix = None
    class AuthorizedUser(xg.Container):
        class UserID(xg.String): pass
        class Email(xg.EmailAddress): pass
        class OrgUnit(xg.String): pass
        class MatrixID(xg.String): pass
        class MatrixSubID(xg.String): pass
        def __init__(self,
                    UserID=None,
                    Email=None, 
                    OrgUnit=None, 
                    MatrixID=None, 
                    MatrixSubID=None):
            xg.Container.__init__(self,
                self.UserID(UserID),
                self.Email(Email),
                self.OrgUnit(OrgUnit),
                self.MatrixID(MatrixID),
                self.MatrixSubID(MatrixSubID))
              
  
class ssdn(xg.Namespace):
    url = "http://www.ksz-bcss.fgov.be/XSD/SSDN/Service"

    class SSDNRequest(xg.Container): 
        """
        General SSDN service request wrapper
        """
        #~ namespace = ssdn
    
    class ServiceRequest(xg.Container):
      
        class ServiceId(xg.String): pass
        class Version(xg.String): pass
        #~ _any = ANY()
        
    class RequestContext(xg.Container):
      
            
        class Message(xg.Container):
            class Reference(xg.String): pass
            class TimeRequest(xg.DateTime): pass
            


class Service(xg.Container):
    """
    Base class for the individual services.
    """
    service_id = None
    service_version = None
    #~ def request(self,anyXML):
        #~ R = SSDNRequest.ServiceRequest
        #~ return R(
            #~ R.ServiceId(self.service_id),
            #~ R.Version(self.service_version),
            #~ anyXML)
      
    def ssdn_request(self,user_params,message_ref,dt):
        #~ xg.set_default_namespace(None)
        any = self.tostring()
        SR = ssdn.ServiceRequest
        serviceRequest = SR(
            SR.ServiceId(self.service_id),
            SR.Version(self.service_version),
            xg.ANY(any))
        
        RC = ssdn.RequestContext
        context = RC(
            common.AuthorizedUser(**user_params),
            RC.Message(
                RC.Message.Reference(message_ref),
                RC.Message.TimeRequest(dt)))
        #~ xg.set_default_namespace(ssdn)
        return ssdn.SSDNRequest(context,serviceRequest)
        
    def execute(self,user_params,url=None,*args):
        sr = self.ssdn_request(user_params,*args).tostring(namespace=ssdn)
        req = soap.request(sr)
        xmlString = """<?xml version="1.0" encoding="utf-8"?>""" + req.tostring()
        
        #~ dblogger.info("Going to send request /******\n%s\n******/",xmlString)
        if not url:
            raise Exception("Not actually sending because url is empty.")
            #~ return Object(data=Object(xmlString="Not actually sending because url is empty."))
            #~ return None
        
        server = Resource(url,measure=True)
        res = server.soap(xmlString)
        return res

        #~ print res.code
        #~ print res.data

        #~ reply = XmlUnmarshaller().parse(str(res.data.xmlString))
        
        #~ return reply
            

class ipr(xg.Namespace):
    """
    Namespace of the IdentifyPerson service.
    
    """
    url = "http://www.ksz-bcss.fgov.be/XSD/SSDN/OCMW_CPAS/IdentifyPerson"


    class IdentifyPersonRequest(Service):
        "A request for identifying a person or validating a person's identity"
        #~ namespace = ipr
        service_id = 'OCMWCPASIdentifyPerson'
        service_version = '20050930'
        
    class SearchCriteria(xg.Container):
        "criteria for identifying a person"
        #~ allowedChildren = [SSIN,PhoneticCriteria]
        class SSIN(SSINType):
            "Social Security Identification number of the person to identify"
            minOccurs = 0
            
    class PhoneticCriteria(xg.Container): 
        """
        set of criteria for a phonetic search. 
        all persons matching these criteria will be returned. 
        Ignored if SSIN is also specified
        """
        minOccurs = 0
        class LastName(xg.String): 
            "last name to search for. Matched phonetically"
        class FirstName(xg.String): pass
        class MiddleName(xg.String): pass
        class BirthDate(t_IncompleteDate):
            """
            birth date in the format yyyy-MM-dd. 
            May be an incomplete date in the format yyyy-MM-00 or yyyy-00-00.
            If incomplete, Tolerance must be specified.
            """
        class Gender(xg.Integer):
            "gender of the person. 0 = unknown, 1 = male, 2 = female"
            allowedValues = (0,1,2)
            
        class Tolerance(xg.Integer):
            """
            tolerance on the bith date. 
            specifies how much BirthDate may be off. 
            the unit depends on the format of BirthDate. 
            yyyy-MM-dd = days; 
            yyyy-MM-00 = months; 
            yyyy-00-00 = years.
            """
        class Maximum(xg.Integer):
            """
            maximum number of results returned. 
            if not specified, maximum number is returned
            """
          
    class VerificationData(xg.Container):
        """
        data used for validating a persons identity. 
        If this element is present, at least one of the 
        subelements must be specified. 
        Validation is successful if one of the subelements 
        can be successfully validated. 
        Ignored if SSIN is not present in the search criteria.
        """
        class SISCardNumber(xg.Container):
            "ID of the person's SIS card"
        class IdentityCardNumber(xg.Container):
            "ID of the person's identity card"
            
    class PersonData(xg.Container):
        "set of personal data to match against"
        class LastName(xg.String):
            "last name to verify. matched exactly"
        class FirstName(xg.String):
            "first name to verify. matched exactly if present"
        class MiddleName(xg.String):
            "middle name to verify. matched exactly if present"
        class BirthDate(t_IncompleteDate):
            """
            birth date in the format yyyy-MM-dd. 
            May be an incomplete date in the format yyyy-MM-00 or yyyy-00-00. 
            If incomplete, Tolerance must be specified
            """

    @classmethod          
    def verify_request(ipr,ssin,**kw):
        """
        possible keywords are the allowed children of
        :class:`IdentifyPersonRequest.VerificationData.PersonData`:
        LastName,
        FirstName,
        MiddleName and 
        BirthDate.
        
        """
        SC = ipr.SearchCriteria
        VD = ipr.VerificationData
        PD = ipr.PersonData
        pd = []
        for k in ('LastName','FirstName','MiddleName','BirthDate'):
        #~ for k,v in kw.items():
            v = kw.get(k,None)
            if v: # ignore empty values
                cl = getattr(PD,k)
                pd.append(cl(v))
        return ipr.IdentifyPersonRequest(
          SC(SC.SSIN(ssin)),
          VD(PD(*pd)))


class pir(xg.Namespace):
    url = "http://www.ksz-bcss.fgov.be/XSD/SSDN/OCMW_CPAS/PerformInvestigation"
    
    class PerformInvestigationRequest(Service):
        #~ namespace = pir
        service_id = 'OCMWCPASPerformInvestigation'
        service_version = '20080604'
    class SocialSecurityUser(xg.String): pass
    class DataGroups(xg.Container):
        """
        The possible types of information that can be obtained. 
        If not specified, all available information is returned.
        """
        class FamilyCompositionGroup(xg.String): pass
        class CitizenGroup(xg.String): pass
        class AddressHistoryGroup(xg.String): pass
        class WaitRegisterGroup(xg.String): pass
          
    #~ def __init__(self,ssin,family='1',citizen='1',address='1',wait='1'):
    @classmethod
    def perform_investigation(pir,ssin,family='1',citizen='1',address='1',wait='1'):
        DG = pir.DataGroups
        return pir.PerformInvestigationRequest(
            pir.SocialSecurityUser(ssin),
            DG(
              DG.FamilyCompositionGroup(family),
              DG.CitizenGroup(citizen),
              DG.AddressHistoryGroup(address),
              DG.WaitRegisterGroup(wait)))
            

class hir(xg.Namespace):
    url = "http://www.ksz-bcss.fgov.be/XSD/SSDN/HealthInsurance"
    
    class HealthInsuranceRequest(Service):
        service_id = 'OCMWCPASHealthInsurance'
        service_version = '20070509'
        class SSIN(SSINType): pass
        class Assurability(xg.Container):
            class Period(xg.Container):
                class StartDate(xg.Date): pass
                class EndDate(xg.Date): pass
        












def xml2reply(xmlString):
    u"""
    Parse the XML string and return a "reply handler".
    
    "Lorsque le détail sous-jacent ne contient pas d’erreur 
    ou d’avertissement, le code possède la valeur 0. 
    Si au moins un avertissement est présent, le code 
    a la valeur 1. Si au moins une erreur est présente, 
    le code sera égal à 10000. 
    Veuillez noter que si des erreurs et des avertissements sont 
    présents, le niveau le plus critique est pris en compte 
    (en l’occurrence, l’erreur, donc le code sera égal à 10000)."
    
    """
    return XmlUnmarshaller().parse(str(xmlString))

    
def reply2lines(reply):
    """
    Convert a reply into a 
    """
    yield "ReplyContext:"
    yield "- ResultSummary:"
    yield "  - Detail:"
    yield "    - AuthorCodeList: %s" % reply.ReplyContext.ResultSummary.Detail.AuthorCodeList
    yield "    - Diagnostic: %s" % reply.ReplyContext.ResultSummary.Detail.Diagnostic
    yield "    - ReasonCode: %s" % reply.ReplyContext.ResultSummary.Detail.ReasonCode
    yield "    - Severity: %s" % reply.ReplyContext.ResultSummary.Detail.Severity
    
    if False:
        yield "- AuthorizedUser:"
        yield "  - UserID: %s" % reply.ReplyContext.AuthorizedUser.UserID
        yield "  - Email: %s" % reply.ReplyContext.AuthorizedUser.Email
        yield "  - OrgUnit: %s" % reply.ReplyContext.AuthorizedUser.OrgUnit
        yield "  - MatrixID: %s" % reply.ReplyContext.AuthorizedUser.MatrixID
        yield "  - MatrixSubID: %s" % reply.ReplyContext.AuthorizedUser.MatrixSubID

    yield "- Message:"
    yield "  - TimeRequest: %s" % reply.ReplyContext.Message.TimeRequest
    yield "  - TimeResponse: %s" % reply.ReplyContext.Message.TimeResponse
    yield "  - TimeReceive: %s" % reply.ReplyContext.Message.TimeReceive
    yield "  - Ticket: %s" % reply.ReplyContext.Message.Ticket
    yield "  - Reference: %s" % reply.ReplyContext.Message.Reference

    yield "ServiceReply:"
    yield "- ServiceId: %s" % reply.ServiceReply.ServiceId
    yield "- Version: %s" % reply.ServiceReply.Version
    yield "- ResultSummary:"
    yield "  - ReturnCode: %s" % reply.ServiceReply.ResultSummary.ReturnCode
    for dtl in reply.ServiceReply.ResultSummary.Detail:
        yield "  - Detail[]:"
        yield "    - ReasonCode: %s" % dtl.ReasonCode
        yield "    - Information: %s" % dtl.Information
        #~ info = dtl.Information:
        #~ yield "    - Information.FieldName[]: %s" % info.FieldName
        #~ yield "    - Information.FieldValue[]: %s" % info.FieldValue
        #~ yield "    - %s = %s" % (info.FieldName,info.FieldValue)
        #~ yield "    - %s" % info
    
    
def unused_test_connection(nr):
  
    xmlString = PerformInvestigationRequest(nr)
    
    reply = unused_send_request(xmlString)

    #~ reply.ReplyContext.AuthorizedUser
    #~ reply.ReplyContext.Message
    dtl = reply.ReplyContext.ResultSummary.Detail
    #~ dtl.AuthorCodeList
    #~ dtl.Diagnostic
    #~ dtl.ReasonCode
    #~ dtl.Severity
    print reply.ReplyContext.ResultSummary.ReturnCode
    print dtl

    import pdb
    pdb.set_trace()

def unused_send_request(settings,xmlString):
    
    #~ logger.info("Going to send request:\n%s",xmlString)
    
    #~ xmlString = SOAP_ENVELOPE % xmlString
    
    xg.set_default_namespace(bcss)
    xmlString = soap.request(xmlString).tostring()
    
    xmlString = """<?xml version="1.0" encoding="utf-8"?>""" + xmlString
    
    #~ xmlString = xmlString.encode('utf-8')
    
    if not settings.LINO.bcss_soap_url:
        #~ logger.info("Not actually sending because Lino.bcss_soap_url is empty.")
        return None
    
    server = Resource(settings.LINO.bcss_soap_url,measure=True)
    
    res = server.soap(xmlString)

    #~ print res.code
    #~ print res.data

    reply = XmlUnmarshaller().parse(str(res.data.xmlString))
    
    return reply
    
  
    

def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()

