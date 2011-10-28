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

u"""
test6 : 

Send a SOAP request to the Belgian 
`BCSS server <http://www.ksz-bcss.fgov.be>`_
(Banque Carrefour de la Sécurité Sociale, 
"Crossroads Bank for Social Security").

Using  a self-made toolkit :mod:`lino.utils.xmlgen`.

"""
from appy.shared.dav import Resource
from appy.shared.xml_parser import XmlUnmarshaller, XmlMarshaller

if True:
    from django.conf import settings
else:
    from appy import Object
    #  simulate a Django `settings` module:
    settings = Object(LINO=Object(
        bcss_soap_url=None,
        bcss_user_params = dict(
              UserID='123456', 
              Email='info@exemple.be', 
              OrgUnit='0123456', 
              MatrixID=17, 
              MatrixSubID=1)))

from lino.utils.xmlgen import *

class com(Namespace):
    url = "http://www.ksz-bcss.fgov.be/XSD/SSDN/Service"

#~ class xsi(Namespace):
#~ class xsd(Namespace):
#~ class soap(Namespace):
    #~ class Envelope
#~ xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" 
#~ xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
#~ xmlns:xsd="http://www.w3.org/2001/XMLSchema"  

#~ SOAP_ENVELOPE = """\
#~ <?xml version="1.0" encoding="utf-8"?>
#~ <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
#~ xmlns:xsd="http://www.w3.org/2001/XMLSchema">
#~ <soap:Body>
#~ <xmlString xmlns="http://ksz-bcss.fgov.be/connectors/WebServiceConnector">
#~ <![CDATA[%s]]>
#~ </xmlString>
#~ </soap:Body>
#~ </soap:Envelope>"""

SOAP_ENVELOPE = u"""\
<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
xmlns:xsd="http://www.w3.org/2001/XMLSchema">
<soap:Body>
<xmlString xmlns="http://ksz-bcss.fgov.be/connectors/WebServiceConnector">
<![CDATA[%s
]]>
</xmlString>
</soap:Body>
</soap:Envelope>
"""

  
class ns1(Namespace):
    url = "http://www.ksz-bcss.fgov.be/XSD/SSDN/OCMW_CPAS/PerformInvestigation"
    class PerformInvestigationRequest(RootContainer):
        class SocialSecurityUser(String): pass
        class DataGroups(Container):
            class FamilyCompositionGroup(String): pass
            class CitizenGroup(String): pass
            class AddressHistoryGroup(String): pass
            class WaitRegisterGroup(String): pass
      
class xmlns(Namespace):
    isdefault = True
    url = "http://www.ksz-bcss.fgov.be/XSD/SSDN/Service"

    class SSDNRequest(RootContainer): 
        class RequestContext(Container):
          
            class AuthorizedUser(Container):
                class UserID(String): pass
                class Email(EmailAddress): pass
                class OrgUnit(String): pass
                class MatrixID(String): pass
                class MatrixSubID(String): pass
                
            class Message(Container):
                class Reference(String): pass
                class TimeRequest(String): pass
                
        class ServiceRequest(Container):
          
            class ServiceId(String): pass
            class Version(String): pass
            #~ _any = ANY()


def PerformInvestigationRequest(person_niss):
    # the following didn't work because the elements need to be in the correct order
    #~ au = [getattr(xmlns,k)(v) 
        #~ for k,v in settings.LINO.bcss_user_params.items()]
    
    def au(UserID='01234567890', 
            Email='info@exemple.be', 
            OrgUnit='0123456789', 
            MatrixID=17, 
            MatrixSubID=1):
        return xmlns.AuthorizedUser(
            xmlns.UserID(UserID),
            xmlns.Email(Email),
            xmlns.OrgUnit(OrgUnit),
            xmlns.MatrixID(MatrixID),
            xmlns.MatrixSubID(MatrixSubID))

    context = xmlns.RequestContext(
        au(**settings.LINO.bcss_user_params),
        xmlns.Message(
            xmlns.Reference('630230001156994'),
            xmlns.TimeRequest('20111020T153528')))

    request = ns1.PerformInvestigationRequest(
        ns1.SocialSecurityUser(person_niss),
        ns1.DataGroups(
            ns1.FamilyCompositionGroup('1'),
            ns1.CitizenGroup('1'),
            ns1.AddressHistoryGroup('1'),
            ns1.WaitRegisterGroup('0')))

    sr = xmlns.ServiceRequest(
        xmlns.ServiceId('OCMWCPASPerformInvestigation'),
        xmlns.Version('20080604'),
        request)

    xmlString = xmlns.SSDNRequest(context,sr).toxml()

    #~ assert_equivalent(EXPECTED,GOT)

    xmlString = SOAP_ENVELOPE % xmlString

    
    xmlString = xmlString.encode('utf-8')
    
    #~ logger.info("Going to send request:\n%s",xmlString)
    
    if not settings.LINO.bcss_soap_url:
        #~ logger.info("Not actually sending because Lino.bcss_soap_url is empty.")
        return None
    
    
    server = Resource(settings.LINO.bcss_soap_url,measure=True)
    
    res = server.soap(xmlString)

    #~ print res.code
    #~ print res.data

    reply = XmlUnmarshaller().parse(str(res.data.xmlString))
    
    return reply
    
def test_connection(nr):
  
    reply = PerformInvestigationRequest(nr)

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
    
        

  
    
if __name__ == '__main__':
  
    test_connection(sys.argv[1])
  
