# -*- coding: UTF-8 -*-
u"""
Send a SOAP request to the Belgian 
`BCSS server <http://www.ksz-bcss.fgov.be>`_
(Banque Carrefour de la Sécurité Sociale, 
"Crossroads Bank for Social Security").

I got a set of XSD files that describe the services provided by the 
BCSS. I could sucessfully convert them to Python modules using  
commands like::

  python -m generateDS -o SSDNRequest.py XSD\SSDN\SERVICE\SSDNREQUEST.XSD
  
(See :srcref:`xsd2py.bat </lino/utils/bcss/xsd2py.bat>`
for the actual commands used on a windows machine.)

Currently only the `SSDNRequest.py` module is being used,
you can browse the input XSD 
:srcref:`here </lino/utils/bcss/XSD/SSDN/SERVICE/SSDNREQUEST.XSD>`
and the generated source code 
:srcref:`here </lino/utils/bcss/SSDNRequest.py>`.

When running this script you need to set your 
DJANGO_SETTINGS_MODULE environment variable.
  
This requires `bcss_user_params` in your :xfile:`settings.py` 
defined like::

  class Lino(Lino):
      ...
      bcss_user_params = dict(
            UserID='123', 
            Email='123@example.com', 
            OrgUnit='123', 
            MatrixID=12, 
            MatrixSubID=3)

"""

import sys
from cStringIO import StringIO

import logging
logger = logging.getLogger(__name__)

from SOAPpy import WSDL
import SSDNRequest
#~ import PerformInvestigation

from django.conf import settings

#~ The SOAP Envelope element is the root element of a SOAP message.
#~ http://www.w3schools.com/soap/soap_envelope.asp

SOAP_ENVELOPE = """
<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope 
  xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" 
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xmlns:xsd="http://www.w3.org/2001/XMLSchema">
  <soap:Body>
    <xmlString xmlns="http://ksz-bcss.fgov.be/connectors/WebServiceConnector">
      <![CDATA[%s]]>
    </xmlString>
  </soap:Body>
</soap:Envelope>
"""

class Service:
    def __init__(self,name,requestClass,doc): # ,*args,**kw):
        self.name = name
        self.requestClass = requestClass
        self.doc = doc
        #~ self.args = args
        #~ self.kw = kw
    def instantiate(self,*args,**kw):
        # currently there is no verification of the parameters
        return self.requestClass(*args,**kw)

from PerformInvestigation import PerformInvestigationRequest

SERVICES = []

SERVICES.append(
  Service(
    'OCMWCPASPerformInvestigation', 
    PerformInvestigationRequest,
    u"""
    Obtention d’informations des registres national et BCSS 
    en vue de l’enquête sociale (données légales, composition 
    de ménage, historique des adresses, recherche dans le 
    fichier d’attente).
    
    Parameters: 
    
    - SocialSecurityUser (string)
    - DataGroups : The possible types of information that can be obtained. 
      If not specified, all available information is returned
    """
    ))

def req2str(req):
    f = StringIO()
    req.export(f,0)
    s = f.getvalue()
    f.close()
    return s


def run_request(serviceId,*args,**kw):
    srv = SERVICES[serviceId]
    srvReq = srv.instantiate(*args,**kw)
    user = SSDNRequest.AuthorizedUserType(**settings.LINO.bcss_user_params)
    service = SSDNRequest.ServiceRequestType(
      ServiceId=srv.name, 
      Version='20090409',
      any_=srvReq)
    msg = SSDNRequest.RequestMessageType(
      Reference='123456789', 
      TimeRequest='20110921T105230')
    context = SSDNRequest.RequestContextType(
      AuthorizedUser=user,
      Message=msg)
    req = SSDNRequest.SSDNRequest(
      RequestContext=context, 
      ServiceRequest=[service])

    requestXML = SOAP_ENVELOPE % req2str(req)
    
    print requestXML
    if False:
        logger.info("Going to send request:\n%s",requestXML)
        proxy = WSDL.Proxy(wsdl_url)
        #~ proxy.soapproxy.config.dumpSOAPOut = 1
        #~ proxy.soapproxy.config.dumpSOAPIn = 1
        m = proxy.methods['sendXML']
        response = m(requestXML)
        logger.info("Got response:\n%s",response)
    

def simple_test():
    run_request(0,SocialSecurityUser='36806010010')
    
    
if __name__ == '__main__':
    simple_test()