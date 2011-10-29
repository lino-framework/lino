# -*- coding: UTF-8 -*-
u"""
Send a SOAP request to the :term: `BCSS` server
using Gaëtan Delannay's :term:`appy` toolkit.

"""


import sys
from cStringIO import StringIO

import logging
logger = logging.getLogger(__name__)

import SSDNRequest


from appy import Object
from appy.shared.dav import Resource
from appy.shared.xml_parser import XmlUnmarshaller, XmlMarshaller
from xml.dom.minidom import parseString

#~ from django.conf import settings
#  simulate a Django `settings` module:
settings = Object(LINO=Object(
    bcss_user_params = dict(
          UserID='123456', 
          Email='info@exemple.be', 
          OrgUnit='0123456', 
          MatrixID=17, 
          MatrixSubID=1)))



class AnyMarshaller(XmlMarshaller):
    """
    An XmlMarshaller who expects an attribute `_any` on its 
    root instance which is expected to contain a string to be
    written after the other child elements.
    """
    fieldsToExclude = ['_any']
    def marshallSpecificElements(self, instance, res):
        res.write(instance._any)

def assert_equivalent(xs1,xs2):
    print "xs1: -------------------"
    print xs1
    print "xs2: -------------------"
    print xs2
    print "-------------------"
    dom1 = parseString(xs1)
    dom2 = parseString(xs2)
    if dom1 != dom2:
        sys.exit()
      
def main():
    allocationReq1 = """<ns1:AllocationRequest xmlns:ns1="http://www.smals.be/XSD/OCMW_CPAS/HeatingAllocationRequest" xmlns:com="http://www.smals.be/XSD/OCMW_CPAS/HeatingAllocationDataTypes"><ns1:ComputeAllocation><ns1:PrimaryBeneficiary><ns1:SSIN>67031703807</ns1:SSIN><ns1:Category>1</ns1:Category></ns1:PrimaryBeneficiary><ns1:Invoice><com:Amount>8390100</com:Amount><com:Quantity>1000</com:Quantity><com:HousingNumber>1</com:HousingNumber><com:DeliveryDate>2011-09-19</com:DeliveryDate><com:UnitFuel>3</com:UnitFuel></ns1:Invoice></ns1:ComputeAllocation><ns1:OCMW_CPAS><ns1:KboBceNumber>0212344876</ns1:KboBceNumber></ns1:OCMW_CPAS></ns1:AllocationRequest>"""

    ssin = '67031703807'

    allocationReq = Object(
      ComputeAllocation=Object(
        Invoice=Object(
          Amount="8390100",
          Quantity=1000,
          HousingNumber=1,
          DeliveryDate="2011-09-19",
          UnitFuel=3),
        PrimaryBeneficiary=Object(SSIN=ssin,Category="1"),
      ),
      OCMW_CPAS=Object(KboBceNumber='0212344876')
      )
      
    ns = dict(
      ns1="http://www.smals.be/XSD/OCMW_CPAS/HeatingAllocationRequest",
      com="http://www.smals.be/XSD/OCMW_CPAS/HeatingAllocationDataTypes")
    nst = dict()
    nst.update(AllocationRequest='ns1')  
    nst.update(ComputeAllocation='ns1')  
    nst.update(OCMW_CPAS='ns1')  
    nst.update(KboBceNumber='ns1')  
    nst.update(Invoice='ns1')  
    nst.update(Quantity='com')  
    nst.update(HousingNumber='com')  
    nst.update(DeliveryDate='com')  
    nst.update(UnitFuel='com')

    m = XmlMarshaller(namespaces=ns,namespacedTags=nst,dumpXmlPrologue=False,rootTag="AllocationRequest")
    allocationReq2 = m.marshall(allocationReq)
      
    #~ assert_equivalent(allocationReq1,allocationReq2)

    contenu1 = """<SSDNRequest xmlns="http://www.ksz-bcss.fgov.be/XSD/SSDN/Service">
    <RequestContext><AuthorizedUser><UserID>00901732883</UserID><Email>info@oshz.eupen.net</Email><OrgUnit>0212344876</OrgUnit><MatrixID>17</MatrixID><MatrixSubID>1</MatrixSubID></AuthorizedUser><Message><Reference>630230001126766</Reference><TimeRequest>20110921T105230</TimeRequest></Message></RequestContext><ServiceRequest><ServiceId>OCMWCPASHeatingAllocation</ServiceId><Version>20090409</Version>
    %s
    </ServiceRequest></SSDNRequest>""" % allocationReq1

    ssdnReq = Object(
        RequestContext=Object(
          AuthorizedUser=Object(**settings.LINO.bcss_user_params),
          Message=Object(Reference='630230001126766',TimeRequest='20110921T105230')
          ),
        ServiceRequest=Object(
          ServiceId="OCMWCPASHeatingAllocation",
          Version="20090409"
        ),
        _any=allocationReq2
        )
          
    ns = dict(xmlns="http://www.ksz-bcss.fgov.be/XSD/SSDN/Service")
    m = AnyMarshaller(namespaces=ns,dumpXmlPrologue=False,rootTag='SSDNRequest')
    contenu2 = m.marshall(ssdnReq)
      
    assert_equivalent(contenu1,contenu2)

    body = Object(
        #~ xmlString="<![CDATA[%s]]>" % contenu)
        xmlString=contenu2)
          
    raise Exception("ok jusqu'ici")

    server = Resource('https://bcssksz-services-test.smals.be/connectors/webservice/KSZBCSSWebServiceConnectorPort',measure=True)

    res = server.soap(body,namespace="http://ksz-bcss.fgov.be/connectors/WebServiceConnector")

    print res.code
    print res.data

    s = str(res.data.xmlString)
    #~ s = res.data.xmlString.replace('"UTF-8"','"utf-8"')
    #~ s = s.replace('?>','?>\n')
    print s

    reply = XmlUnmarshaller().parse(s)

    import pdb
    pdb.set_trace()

if __name__ == '__main__':
    main()