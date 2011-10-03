# -*- coding: UTF-8 -*-
u"""
I am trying to use generateDS to write a SOAP request to the 
Belgian `BCSS server <http://www.ksz-bcss.fgov.be>`_
(Banque Carrefour de la Sécurité Sociale, 
"Crossroads Bank for Social Security").

I got a set of XSD files that describe the services provided by the 
BCSS. I could sucessfully convert them to Python modules using following 
commands like:

  python -m generateDS -o SSDNRequest.py XSD\SSDN\SERVICE\SSDNREQUEST.XSD
  
See :file:`xsd2py.bat` for the actual commands used on a windows machine.

Currently only the `SSDNRequest.py` module is being used. 
The following code should simply output an XML string to stdout.
My problem is that executing it causes a traceback ::

  Traceback (most recent call last):
    File "test.py", line 45, in <module>
      req.export(f,0)
    File "SSDNRequest.py", line 613, in export
      self.exportChildren(outfile, level + 1, namespace_, name_)
    File "SSDNRequest.py", line 622, in exportChildren
      self.RequestContext.export(outfile, level, namespace_, name_='RequestContext', )
    File "SSDNRequest.py", line 525, in export
      self.exportChildren(outfile, level + 1, namespace_, name_)
    File "SSDNRequest.py", line 534, in exportChildren
      self.AuthorizedUser.export(outfile, level, namespace_, name_='AuthorizedUser', )
    File "SSDNRequest.py", line 800, in export
      self.exportChildren(outfile, level + 1, namespace_, name_)
    File "SSDNRequest.py", line 810, in exportChildren
      outfile.write('<%sUserID>%s</%sUserID>\n' % (namespace_, self.gds_format_string(quote_xml(self.UserID).encode(ExternalEncoding), input_name='UserID'), namespace_))
  AttributeError: 'AuthorizedUserType' object has no attribute 'gds_format_string'
  
What is going wrong?

  
"""
import sys
import SSDNRequest
#~ import PerformInvestigation

from cStringIO import StringIO

user = SSDNRequest.AuthorizedUserType(
  UserID='123', 
  Email='123@example.com', 
  OrgUnit='123', 
  MatrixID=12, 
  MatrixSubID=3)
service = SSDNRequest.ServiceRequestType(
  ServiceId='Test', 
  Version='20090409')
msg = SSDNRequest.RequestMessageType(
  Reference='123456789', 
  TimeRequest='20110921T105230')
context = SSDNRequest.RequestContextType(AuthorizedUser=user,Message=msg)
req = SSDNRequest.SSDNRequest(RequestContext=context, ServiceRequest=service)

f = StringIO()
req.export(f,0)
xmlrequest = f.getvalue()
f.close()

#~ The SOAP Envelope element is the root element of a SOAP message.
#~ http://www.w3schools.com/soap/soap_envelope.asp

soap_envelope = """
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

print soap_envelope % xmlrequest