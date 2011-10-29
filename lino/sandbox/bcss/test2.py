# -*- coding: UTF-8 -*-
u"""
Send a SOAP request to the :term: `BCSS` server
using Dave Kuhlmann's :term:`generateDS` (version 2.6a).

Continued from :mod:`lino.sandbox.bcss.test`.
File :file:`SSDNRequest.py` has been modified manually 
for <any> support according to Dave's instructions.

When running this script you need to set your 
DJANGO_SETTINGS_MODULE environment variable
which points to a :xfile:`settings.py` 
that defines your :attr:`lino.Lino.bcss_user_params`.
Since this script doesn't actually perform any connection, 
the `bcss_user_params` may contain fictive values. 
But they must exist.

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
    def __init__(self,name,requestClass,targetNamespace,doc): # ,*args,**kw):
        self.name = name
        self.requestClass = requestClass
        self.targetNamespace = targetNamespace
        self.doc = doc
        #~ self.args = args
        #~ self.kw = kw
    def instantiate(self,*args,**kw):
        return self.requestClass(*args,**kw)

from PerformInvestigation import PerformInvestigationRequest

SERVICES = []

SERVICES.append(
  Service(
    'OCMWCPASPerformInvestigation', 
    PerformInvestigationRequest,
    'http://www.ksz-bcss.fgov.be/XSD/SSDN/OCMW_CPAS/PerformInvestigation',
    u"""
    Obtention d’informations des registres national et BCSS 
    en vue de l’enquête sociale (données légales, composition 
    de ménage, historique des adresses, recherche dans le 
    fichier d’attente).
    
    Instance parameters: 
    
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