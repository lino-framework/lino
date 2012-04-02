## Copyright 2012 Luc Saffre
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
This script just calls the `TestConnectionService` service using :term:`SUDS`. 
It is to be called from the command line as follows::

  python -m lino.utils.xmlgen.cbss.20120305
  
Expected output::

  Instantiate Client at file:///var/snapshots/lino_dev/lino/utils/xmlgen/cbss/XSD/TestConnectionService.wsdl

  Suds ( https://fedorahosted.org/suds/ )  version: 0.3.9 GA  build: R659-20100219

  Service ( TestConnectionServiceService ) tns="http://kszbcss.fgov.be/intf/TestConnectionServiceService/v1"
     Prefixes (1)
        ns0 = "http://kszbcss.fgov.be/types/TestConnectionService/v1"
     Ports (1):
        (TestConnectionServiceService)
           Methods (1):
              sendTestMessage(xs:string echo, )
           Types (11):
              ns0:CbeNumberType
              ns0:CustomerIdentificationType
              ns0:InformationCBSSType
              ns0:InformationCustomerType
              ns0:InformationType
              ns0:MessageType
              ns0:SendTestMessageRequestType
              ns0:SendTestMessageResponseType
              ns0:SeverityType
              ns0:StatusType
              ns0:UUIDType


  Sending request ...
  Full result:
  (reply){
     informationCBSS =
        (InformationCBSSType){
           ticketCBSS = "1b1b6828-71a6-49b6-a543-7edc975d54c3"
           timestampReceive = 2012-03-30 11:16:04.000798
           timestampReply = 2012-03-30 11:16:04.000867
        }
     echo = "hello cbss service"
     sslCertificate = "CN=incursus.smals.be,C=BE,emailAddress=pki@smals.be,L=BRUSSELS,ST=BRUSSELS,OU=Smals,O=Smals"
   }
  Ticket ID:
  1b1b6828-71a6-49b6-a543-7edc975d54c3

"""

def _test():
    import os
    from os.path import abspath, dirname
    from suds.client import Client

    service = 'TestConnectionService'
    service_url = "https://bcssksz-services-test.smals.be:443/SOA4520/TestConnectionServiceService"
    #~ service = 'RetrieveTIGroupsV3'

    url = abspath(dirname(__file__)).replace(os.path.sep,"/")
    if not url.startswith('/'):
        # on a windows machine we need to prepend an additional "/"
        url = '/' + url
        
    url += '/XSD/%s.wsdl' % service
    url = 'file://' + url 
    print "Instantiate Client at", url
    suds_options = dict()
    #~ suds_options.update(location="foo")
    client = Client(url,**suds_options)
    print client
    
    #~ print client.service.__class__
    #~ m = client.service.__class__.setlocation
    #~ m(client.service,service_url)
    #~ print client.service.__services[0].__class__
    client.service.__services[0].setlocation(service_url)
    
    
    #~ if True:
        #~ print client.wsdl
    if False:
        print "Sending request ..."
        result = client.service.sendTestMessage("hello cbss service")
        print "Full result:"
        print result

        print "Ticket ID:"
        print result.informationCBSS.ticketCBSS

if __name__ == "__main__":
    _test()

