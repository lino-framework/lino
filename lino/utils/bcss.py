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

    #  simulate a Django `settings` module:


>>> from appy import Object
>>> settings = Object(LINO=Object(
...   bcss_user_params = dict(
...     UserID='123456', 
...     Email='info@exemple.be', 
...     OrgUnit='0123456', 
...     MatrixID=17, 
...     MatrixSubID=1)))


>>> print PerformInvestigationRequest(settings,"6806010123").toxml(True)
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
<Reference>630230001156994</Reference>
<TimeRequest>20111020T153528</TimeRequest>
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

#~ if True:
    #~ from django.conf import settings
#~ else:
    #~ from appy import Object
    #~ settings = Object(LINO=Object(
        #~ bcss_soap_url=None,
        #~ bcss_user_params = dict(
              #~ UserID='123456', 
              #~ Email='info@exemple.be', 
              #~ OrgUnit='0123456', 
              #~ MatrixID=17, 
              #~ MatrixSubID=1)))

from lino.utils.xmlgen import *

#~ class com(Namespace):
    #~ url = "http://www.ksz-bcss.fgov.be/XSD/SSDN/Service"

#~ class xsi(Namespace):
#~ class xsd(Namespace):
#~ class soap(Namespace):
    #~ class Envelope
#~ xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" 
#~ xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
#~ xmlns:xsd="http://www.w3.org/2001/XMLSchema"  


#~ SOAP_ENVELOPE = u"""\
#~ <?xml version="1.0" encoding="utf-8"?>
#~ <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
#~ xmlns:xsd="http://www.w3.org/2001/XMLSchema">
#~ <soap:Body>
#~ <xmlString xmlns="http://ksz-bcss.fgov.be/connectors/WebServiceConnector">
#~ <![CDATA[%s
#~ ]]>
#~ </xmlString>
#~ </soap:Body>
#~ </soap:Envelope>
#~ """

class bcss(Namespace):
  url = "http://ksz-bcss.fgov.be/connectors/WebServiceConnector"
  class xmlString(Container):
    pass

class soap(Namespace):
  url = "http://schemas.xmlsoap.org/soap/envelope/" 
  class Envelope(Container):
    class Body(Container):
        pass

  
class ssdn(Namespace):
    #~ isdefault = True
    url = "http://www.ksz-bcss.fgov.be/XSD/SSDN/Service"

    class SSDNRequest(Container): 
        class RequestContext(Container):
          
            class AuthorizedUser(Container):
                class UserID(String): pass
                class Email(EmailAddress): pass
                class OrgUnit(String): pass
                class MatrixID(String): pass
                class MatrixSubID(String): pass
                def __init__(self,
                            UserID=None,
                            Email=None, 
                            OrgUnit=None, 
                            MatrixID=None, 
                            MatrixSubID=None):
                    Container.__init__(self,
                        ssdn.UserID(UserID),
                        ssdn.Email(Email),
                        ssdn.OrgUnit(OrgUnit),
                        ssdn.MatrixID(MatrixID),
                        ssdn.MatrixSubID(MatrixSubID))
                  
                
            class Message(Container):
                class Reference(String): pass
                class TimeRequest(String): pass
                
        class ServiceRequest(Container):
          
            class ServiceId(String): pass
            class Version(String): pass
            #~ _any = ANY()


class ns2(Namespace):
    url = "http://www.ksz-bcss.fgov.be/XSD/SSDN/HealthInsurance"
    
    class HealthInsuranceRequest(Container):
        service_id = 'OCMWCPASHealthInsurance'
        service_version = '20070509'
        class SSIN(String): pass
        class Assurability(Container):
            class Period(Container):
                class StartDate(Date): pass
                class EndDate(Date): pass
        
class ns1(Namespace):
    url = "http://www.ksz-bcss.fgov.be/XSD/SSDN/OCMW_CPAS/PerformInvestigation"
    class PerformInvestigationRequest(Container):
        service_id = 'OCMWCPASPerformInvestigation'
        service_version = '20080604'
        class SocialSecurityUser(String): pass
        class DataGroups(Container):
            class FamilyCompositionGroup(String): pass
            class CitizenGroup(String): pass
            class AddressHistoryGroup(String): pass
            class WaitRegisterGroup(String): pass
        def __init__(self,ss_user,family='1',citizen='1',address='1',wait='1'):
            Container.__init__(self,
              ns1.SocialSecurityUser(ss_user),
              ns1.DataGroups(
                ns1.FamilyCompositionGroup(family),
                ns1.CitizenGroup(citizen),
                ns1.AddressHistoryGroup(address),
                ns1.WaitRegisterGroup(wait)))


def PerformInvestigationRequest(settings,person_niss):

    context = ssdn.RequestContext(
        ssdn.AuthorizedUser(**settings.LINO.bcss_user_params),
        ssdn.Message(
            ssdn.Reference('630230001156994'),
            ssdn.TimeRequest('20111020T153528')))
            
            
    request = ns1.PerformInvestigationRequest(person_niss,wait='0')

    sr = ssdn.ServiceRequest(
        ssdn.ServiceId(request.service_id),
        ssdn.Version(request.service_version),
        request)

    set_default_namespace(ssdn)
    return ssdn.SSDNRequest(context,sr)
    #~ xmlString = ssdn.SSDNRequest(context,sr).toxml()
    #~ return xmlString
    
def send_request(settings,xmlString):
    
    #~ logger.info("Going to send request:\n%s",xmlString)
    
    if not settings.LINO.bcss_soap_url:
        #~ logger.info("Not actually sending because Lino.bcss_soap_url is empty.")
        return None
    
    #~ xmlString = SOAP_ENVELOPE % xmlString
    
    set_default_namespace(bcss)
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

