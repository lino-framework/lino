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
Communicate with the :term:`BCSS` server.

Example:

>>> req = IdentifyPersonRequest("68060101234",
...   LastName="SAFFRE",BirthDate="1968-06-01")
>>> print req.toxml(True)
<ips:IdentifyPersonRequest xmlns:ips="http://www.ksz-bcss.fgov.be/XSD/SSDN/OCMW_CPAS/IdentifyPerson">
<ips:SearchCriteria>
<ips:SSIN>68060101234</ips:SSIN>
</ips:SearchCriteria>
<ips:VerificationData>
<ips:PersonData>
<ips:LastName>SAFFRE</ips:LastName>
<ips:BirthDate>1968-06-01</ips:BirthDate>
</ips:PersonData>
</ips:VerificationData>
</ips:IdentifyPersonRequest>

>>> req = PerformInvestigationRequest("6806010123",wait="0")
>>> print req.toxml(True)
<ns1:PerformInvestigationRequest xmlns:ns1="http://www.ksz-bcss.fgov.be/XSD/SSDN/OCMW_CPAS/PerformInvestigation">
<ns1:SocialSecurityUser>6806010123</ns1:SocialSecurityUser>
<ns1:DataGroups>
<ns1:FamilyCompositionGroup>1</ns1:FamilyCompositionGroup>
<ns1:CitizenGroup>1</ns1:CitizenGroup>
<ns1:AddressHistoryGroup>1</ns1:AddressHistoryGroup>
<ns1:WaitRegisterGroup>0</ns1:WaitRegisterGroup>
</ns1:DataGroups>
</ns1:PerformInvestigationRequest>

The above examples are bare service request bodies.
Before sending them to the BCSS server, they must be wrapped.
Simulate a Django `settings` module:

>>> from appy import Object
>>> settings = Object(LINO=Object(
...   bcss_user_params = dict(
...     UserID='123456', 
...     Email='info@exemple.be', 
...     OrgUnit='0123456', 
...     MatrixID=17, 
...     MatrixSubID=1)))


>>> import datetime
>>> now = datetime.datetime(2011,10,31,15,41,10)
>>> wrapped_req = req.send(settings,'PIR # 5',now)
>>> print wrapped_req.toxml(True)
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
<ns1:PerformInvestigationRequest xmlns:ns1="http://www.ksz-bcss.fgov.be/XSD/SSDN/OCMW_CPAS/PerformInvestigation">
<ns1:SocialSecurityUser>6806010123</ns1:SocialSecurityUser>
<ns1:DataGroups>
<ns1:FamilyCompositionGroup>1</ns1:FamilyCompositionGroup>
<ns1:CitizenGroup>1</ns1:CitizenGroup>
<ns1:AddressHistoryGroup>1</ns1:AddressHistoryGroup>
<ns1:WaitRegisterGroup>0</ns1:WaitRegisterGroup>
</ns1:DataGroups>
</ns1:PerformInvestigationRequest>
</ServiceRequest>
</SSDNRequest>

"""




from appy.shared.dav import Resource
from appy.shared.xml_parser import XmlUnmarshaller, XmlMarshaller

#~ from lino.utils.xmlgen import *
from lino.utils import xmlgen as xg

class bcss(xg.Namespace):
  url = "http://ksz-bcss.fgov.be/connectors/WebServiceConnector"
  class xmlString(xg.Container):
    pass

class soap(xg.Namespace):
  url = "http://schemas.xmlsoap.org/soap/envelope/" 
  class Envelope(xg.Container):
    class Body(xg.Container):
        pass

  
#~ class com(xg.Namespace):
    #~ url = "http://www.ksz-bcss.fgov.be/XSD/SSDN/Common"
    #~ class SSIN(String): pass
      
class SSIN(xg.String):
    def validate(self,v):
        if len(v) != 11:
            raise Exception("length must be 11")
        if not v.isdigit():
            raise Exception("must be a number")
        return v
      
  
class ssdn(xg.Namespace):
    url = "http://www.ksz-bcss.fgov.be/XSD/SSDN/Service"

class SSDNRequest(xg.Container): 
    """
    General SSDN service request wrapper
    """
    namespace = ssdn
    class RequestContext(xg.Container):
      
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
              
            
        class Message(xg.Container):
            class Reference(xg.String): pass
            class TimeRequest(xg.String): pass
            
    class ServiceRequest(xg.Container):
      
        class ServiceId(xg.String): pass
        class Version(xg.String): pass
        #~ _any = ANY()


class Service(xg.Container):
    """
    Base class for the individual services.
    """
    service_id = None
    service_version = None
    def request(self,anyXML):
        R = SSDNRequest.ServiceRequest
        return R(
            R.ServiceId(self.service_id),
            R.Version(self.service_version),
            anyXML)
      
    def send(self,settings,message_ref,dt):
        anyXML = self.toxml()
        C = SSDNRequest.RequestContext
        context = C(
            C.AuthorizedUser(**settings.LINO.bcss_user_params),
            C.Message(
                C.Message.Reference(message_ref),
                C.Message.TimeRequest(dt.strftime("%Y%m%dT%H%M%S"))))
        xg.set_default_namespace(ssdn)
        return SSDNRequest(context,self.request(anyXML))
            

class ips(xg.Namespace):
    """
    Namespace of the IdentifyPerson service.
    
    """
    url = "http://www.ksz-bcss.fgov.be/XSD/SSDN/OCMW_CPAS/IdentifyPerson"
    
    
class IdentifyPersonRequest(Service):
    "A request for identifying a person or validating a persons identity"
    namespace = ips
    service_id = 'OCMWCPASIdentifyPerson'
    service_version = '20050930'
    class SearchCriteria(xg.Container):
        "criteria for identifying a person"
        #~ allowedChildren = [SSIN,PhoneticCriteria]
        class SSIN(SSIN):
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
            class BirthDate(xg.Date):
                """
                birth date in the format yyyy-MM-dd. 
                May be an incomplete date in the format yyyy-MM-00 or yyyy-00-00.
                If incomplete, Tolerance must be specified.
                """
            class Gender(xg.String):
                "gender of the person. 0 = unknown, 1 = male, 2 = female"
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
            "ID of the persons SIS card"
        class IdentityCardNumber(xg.Container):
            "ID of the persons identity card"
        class PersonData(xg.Container):
            "set of personal data to match against"
            class LastName(xg.String):
                "last name to verify. matched exactly"
            class FirstName(xg.String):
                "first name to verify. matched exactly if present"
            class MiddleName(xg.String):
                "middle name to verify. matched exactly if present"
            class BirthDate(xg.Date):
                """
                birth date in the format yyyy-MM-dd. 
                May be an incomplete date in the format yyyy-MM-00 or yyyy-00-00. 
                If incomplete, Tolerance must be specified
                """

              
    def __init__(self,ssin,LastName=None,BirthDate=None):
        SC = IdentifyPersonRequest.SearchCriteria
        VD = IdentifyPersonRequest.VerificationData
        xg.Container.__init__(self,
          SC(SC.SSIN(ssin)),
          VD(VD.PersonData(
              VD.PersonData.LastName(LastName),
              VD.PersonData.BirthDate(BirthDate),
            )))


class ns2(xg.Namespace):
    url = "http://www.ksz-bcss.fgov.be/XSD/SSDN/HealthInsurance"
    
    class HealthInsuranceRequest(Service):
        service_id = 'OCMWCPASHealthInsurance'
        service_version = '20070509'
        class SSIN(SSIN): pass
        class Assurability(xg.Container):
            class Period(xg.Container):
                class StartDate(xg.Date): pass
                class EndDate(xg.Date): pass
        

class ns1(xg.Namespace):
    url = "http://www.ksz-bcss.fgov.be/XSD/SSDN/OCMW_CPAS/PerformInvestigation"
    
class PerformInvestigationRequest(Service):
    namespace = ns1
    service_id = 'OCMWCPASPerformInvestigation'
    service_version = '20080604'
    class SocialSecurityUser(xg.String): pass
    class DataGroups(xg.Container):
        class FamilyCompositionGroup(xg.String): pass
        class CitizenGroup(xg.String): pass
        class AddressHistoryGroup(xg.String): pass
        class WaitRegisterGroup(xg.String): pass
    def __init__(self,ssin,family='1',citizen='1',address='1',wait='1'):
        DG = PerformInvestigationRequest.DataGroups
        xg.Container.__init__(self,
          PerformInvestigationRequest.SocialSecurityUser(ssin),
          DG(
            DG.FamilyCompositionGroup(family),
            DG.CitizenGroup(citizen),
            DG.AddressHistoryGroup(address),
            DG.WaitRegisterGroup(wait)))
            


    
def send_request(settings,xmlString):
    
    #~ logger.info("Going to send request:\n%s",xmlString)
    
    if not settings.LINO.bcss_soap_url:
        #~ logger.info("Not actually sending because Lino.bcss_soap_url is empty.")
        return None
    
    #~ xmlString = SOAP_ENVELOPE % xmlString
    
    xg.set_default_namespace(bcss)
    xmlString = soap.Envelope(soap.Body(bcss.xmlString(CDATA(xmlString)))).toxml()
    
    xmlString = """<?xml version="1.0" encoding="utf-8"?>""" + xmlString
    
    #~ xmlString = xmlString.encode('utf-8')
    
    server = Resource(settings.LINO.bcss_soap_url,measure=True)
    
    res = server.soap(xmlString)

    #~ print res.code
    #~ print res.data

    reply = XmlUnmarshaller().parse(str(res.data.xmlString))
    
    return reply
    
def test_connection(nr):
  
    xmlString = PerformInvestigationRequest(nr)
    
    reply = send_request(xmlString)

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
    
        

  
    
#~ if __name__ == '__main__':
  
    #~ test_connection(sys.argv[1])
  

def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()

