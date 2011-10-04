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



def main():
    user = SSDNRequest.AuthorizedUserType(**settings.LINO.bcss_user_params)
    service = SSDNRequest.ServiceRequestType(
      ServiceId='Test', 
      Version='20090409')
    msg = SSDNRequest.RequestMessageType(
      Reference='123456789', 
      TimeRequest='20110921T105230')
    context = SSDNRequest.RequestContextType(
      AuthorizedUser=user,
      Message=msg)
    req = SSDNRequest.SSDNRequest(
      RequestContext=context, 
      ServiceRequest=[service])

    f = StringIO()
    req.export(f,0)
    xmlrequest = f.getvalue()
    f.close()

    requestXML = SOAP_ENVELOPE % xmlrequest
    
    logger.info("Going to send request:\n%s",requestXML)
    proxy = WSDL.Proxy(wsdl_url)
    #~ proxy.soapproxy.config.dumpSOAPOut = 1
    #~ proxy.soapproxy.config.dumpSOAPIn = 1
    m = proxy.methods['sendXML']
    response = = m(requestXML)
    logger.info("Got response:\n%s",response)
    
    
if __name__ == '__main__':
    main()