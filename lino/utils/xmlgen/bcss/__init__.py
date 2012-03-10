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

r"""
This document describes how to communicate with the :term:`BCSS` server 
using Python and Lino. It covers the low-level aspects which might also 
be useful from applications that do not use the other parts of Lino.

To run these examples, you need
Python, Lino and the following Python modules:

  - :term:`lxml`
  - :term:`appy.pod`
  
  


Building SSDN requests
----------------------

This module currently supports the following "classical" SSDN requests:

- :attr:`ipr` : IdentifyPerson
- :attr:`pir` : PerformInvestigation
- :attr:`hir` : HealthInsurance
 
:attr:`ipr` has two variants: *with* known NISS or *without*.
If a NISS is given, the other parameters are "verification data". 
For example:

>>> req = ipr.build_request("68060101234",
...   last_name="SAFFRE",birth_date='1968-06-01')

To show what this request contains, we can use lxml's tostring method:

>>> print etree.tostring(req,pretty_print=True) #doctest: +ELLIPSIS
<ipr:IdentifyPersonRequest xmlns:ipr="http://.../IdentifyPerson">
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
<BLANKLINE>

If no NISS is given, the other parameters are "search criteria", 
and at least the birth date is then mandatory. If you don't give birth 
date, you'll get a :class:`SimpleException` (i.e. an Exception whose 
string is meant to be understandable by the user):

>>> req = ipr.build_request(last_name="SAFFRE")
Traceback (most recent call last):
...
SimpleException: Either national_id or birth date must be given

Here is a valid ipr request:

>>> req = ipr.build_request(last_name="SAFFRE",birth_date='1968-06-01')

Again, we can look at the XML to see what it contains:

>>> print etree.tostring(req,pretty_print=True) #doctest: +ELLIPSIS
<ipr:IdentifyPersonRequest xmlns:ipr="http://.../IdentifyPerson">
  <ipr:SearchCriteria>
    <ipr:PhoneticCriteria>
      <ipr:LastName>SAFFRE</ipr:LastName>
      <ipr:FirstName></ipr:FirstName>
      <ipr:MiddleName></ipr:MiddleName>
      <ipr:BirthDate>1968-06-01</ipr:BirthDate>
    </ipr:PhoneticCriteria>
  </ipr:SearchCriteria>
</ipr:IdentifyPersonRequest>
<BLANKLINE>



Here is also a PerformInvestigation request:

>>> req = pir.build_request("68060101234",wait="0")
>>> print etree.tostring(req,pretty_print=True) #doctest: +ELLIPSIS
<pir:PerformInvestigationRequest xmlns:pir="http://.../PerformInvestigation">
  <pir:SocialSecurityUser>68060101234</pir:SocialSecurityUser>
  <pir:DataGroups>
    <pir:FamilyCompositionGroup>1</pir:FamilyCompositionGroup>
    <pir:CitizenGroup>1</pir:CitizenGroup>
    <pir:AddressHistoryGroup>1</pir:AddressHistoryGroup>
    <pir:WaitRegisterGroup>0</pir:WaitRegisterGroup>
  </pir:DataGroups>
</pir:PerformInvestigationRequest>
<BLANKLINE>


Executing SSDN requests
-----------------------

The above examples are bare BCSS service requests.
In order to actually execute our request, 
we need some more parameters:

- The "user parameters" for the BCSS, specified as a normal Python `dict` 
  object:

  >>> user_params = dict(
  ...     UserID='123456', 
  ...     Email='info@exemple.be', 
  ...     OrgUnit='0123456', 
  ...     MatrixID='17', 
  ...     MatrixSubID='1')

  The document you are reading uses fictive user parameters and 
  doesn't actually execute any real request, 
  but if you have the permission to connect to the BCSS server
  (see `www.ksz-bcss.fgov.be <http://www.ksz-bcss.fgov.be/fr/bcss/docutheque/content/websites/belgium/services/docutheque.html>`_),
  you should be able to reproduce the examples using your correct user parameters.
  
  (In a Lino application, these user parameters 
  are defined in your local :xfile:`settings.py` 
  module :attr:`lino.Lino.bcss_user_params`.)
  
  

- You also need a unique reference and a timestamp. 

  >>> import datetime
  >>> now = datetime.datetime(2011,10,31,15,41,10)
  >>> unique_id = 'PIR # 5'

  Your application is responsible for keeping a log of all 
  requests (including also the user who issued the request).
  Lino does this in :mod:`lino.modlib.bcss`.


- And then we need the URL of the server. 
  In a real configuration it looks something like this:

  >>> bcss_soap_url = "https://bcssksz-services-test.smals.be" \
  ...   + "/connectors/webservice/KSZBCSSWebServiceConnectorPort"

  Since in this document we don't want to actually perform real 
  requests, we'll set the URL to None:

  >>> bcss_soap_url = None
  
  (In a Lino application, this is defined in 
  your local :xfile:`settings.py` 
  module :attr:`lino.Lino.bcss_soap_url`.)
  

If you run the following call in a real environment
(with permission to connect and correct data in `user_params`), 
it won't raise the `SimpleException` but return a `response object`:

>>> response = pir.execute(req,user_params,bcss_soap_url,unique_id,now) #doctest: +ELLIPSIS
Traceback (most recent call last):
...
SimpleException: Not actually sending because url is empty. Request would be:
<?xml version='1.0' encoding='ASCII'?>
<soap:Envelope ...</soap:Envelope>

The `response` is currently a simple wrapper around the XML structure 
returned by the BCSS.
Your application is responsible for treating and storing and using this data.
Lino does this in :mod:`lino.modlib.bcss`.



Internals
---------

Internally we must first wrap it into a "SSDN request".
The easiest way to do this is to use the 
:meth:`Service.ssdn_request` method.

Remember that we have in our variable ``req`` the 
PerformInvestigation request from above. 
Let's wrap this into an SSDN envelope:

>>> sr = pir.ssdn_request(req,user_params,unique_id,now)

Here is the bare XML of this wrapped SSDN request:

>>> print etree.tostring(sr,pretty_print=True) #doctest: +ELLIPSIS
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
    <pir:PerformInvestigationRequest xmlns:pir="http://.../PerformInvestigation">
    ...
    </pir:PerformInvestigationRequest>
  </ServiceRequest>
</SSDNRequest>
<BLANKLINE>

Internally, the `execute` method wraps the SSDN request 
into a SOAP envelope:

>>> print etree.tostring(soap_request("Foo"),pretty_print=True) #doctest: +ELLIPSIS
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <bcss:xmlString xmlns:bcss="http://.../WebServiceConnector"><![CDATA[Foo]]></bcss:xmlString>
  </soap:Body>
</soap:Envelope>
<BLANKLINE>


"""

import os

from appy.shared.dav import Resource
from appy.shared.xml_parser import XmlUnmarshaller

from lxml import etree

#~ from lino.utils import d2iso
#~ from lino.utils import IncompleteDate
from lino.utils.xmlgen import SimpleException, Namespace

def xsdpath(*parts):
    p1 = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(p1,'XSD',*parts)




soap = Namespace('soap',"http://schemas.xmlsoap.org/soap/envelope/")
bcss = Namespace('bcss',"http://ksz-bcss.fgov.be/connectors/WebServiceConnector")
ssdn = Namespace(None,"http://www.ksz-bcss.fgov.be/XSD/SSDN/Service")
#~ ssdn = Namespace('ssdn',"http://www.ksz-bcss.fgov.be/XSD/SSDN/Service")
#~ ,nsmap={None:ssdn._url}

#~ ssdn.define("""
#~ SSDNRequest
#~ ServiceRequest
#~ ServiceId
#~ Version
#~ RequestContext
#~ Message
#~ Reference
#~ TimeRequest
#~ """)            



#~ bcss.define('xmlString')

#~ soap.define("Body Envelope")



class Common(Namespace):
  
    def authorized_user(common,
                UserID=None,
                Email=None, 
                OrgUnit=None, 
                MatrixID=None, 
                MatrixSubID=None):
        return common.AuthorizedUser(
            common.UserID(UserID),
            common.Email(Email),
            common.OrgUnit(OrgUnit),
            common.MatrixID(MatrixID),
            common.MatrixSubID(MatrixSubID))

common = Common()
#~ common.define("""
#~ AuthorizedUser
#~ UserID
#~ Email
#~ OrgUnit
#~ MatrixID
#~ MatrixSubID
#~ """)






class Service(Namespace):
    """
    Base class for the individual services.
    """
    service_id = None
    service_version = None
      
    def ssdn_request(self,srvReq,user_params,message_ref,dt):
        #~ xg.set_default_namespace(None)
        any = etree.tostring(srvReq)
        serviceRequest = ssdn.ServiceRequest(
            ssdn.ServiceId(self.service_id),
            ssdn.Version(self.service_version),
            etree.XML(any))
        
        context = ssdn.RequestContext(
            common.authorized_user(**user_params),
            ssdn.Message(
                ssdn.Reference(message_ref),
                ssdn.TimeRequest(dt)))
        #~ xg.set_default_namespace(ssdn)
        elem = ssdn.SSDNRequest(context,serviceRequest)
        #~ elem.nsmap={None:self._url}
        return elem
        #~ return ssdn.SSDNRequest(context,serviceRequest)
        
    def execute(self,req,user_params,url=None,*args):
        #~ print 20120302
        if user_params is None:
            raise SimpleException(
                "Not actually sending because user_params is empty.")
        #~ self.validate_against_xsd(req)
            
        sr = self.ssdn_request(req,user_params,*args)
        soap_body = etree.tostring(sr)
        req = soap_request(soap_body)
        #~ xmlString = """<?xml version="1.0" encoding="utf-8"?>""" + 
        
        xmlString = etree.tostring(req,xml_declaration=True)
        
        if not url:
            raise SimpleException("""\
Not actually sending because url is empty. Request would be:
""" + xmlString)
        
        server = Resource(url,measure=True)
        res = server.soap(xmlString)
        return res

        #~ print res.code
        #~ print res.data

        #~ reply = XmlUnmarshaller().parse(str(res.data.xmlString))
        
        #~ return reply
        

        
class IdentifyPersonRequest(Service):
    "A request for identifying a person or validating a person's identity"
    service_id = 'OCMWCPASIdentifyPerson'
    service_version = '20050930'
    xsd_filename = xsdpath('SSDN','OCMW_CPAS',
        'IDENTIFYPERSON','IDENTIFYPERSONREQUEST.XSD')

    def build_request(ipr,
        national_id='',
        first_name='',
        middle_name='',
        last_name='',
        birth_date=None,
        gender=None,
        tolerance=None
        ):
        """
        If `national_id` is given, 
        request a *verification* of the personal data,
        Otherwise request a search on the person's last_name, 
        first_name and (if filled) birth_date and gender fields.
        """
        if national_id:
            pd = []
            if last_name: pd.append(ipr.LastName(last_name))
            if first_name: pd.append(ipr.FirstName(first_name))
            if middle_name: pd.append(ipr.MiddleName(middle_name))
            if birth_date: pd.append(ipr.BirthDate(birth_date))
            if gender is not None: pd.append(ipr.Gender(gender))
            if tolerance is not None: pd.append(ipr.Tolerance(tolerance))
            
            #~ for k in ('LastName','FirstName','MiddleName','BirthDate'):
                #~ v = kw.get(k,None)
                #~ if v: # ignore empty values
                    #~ cl = getattr(ipr,k)
                    #~ pd.append(cl(v))
            return ipr.IdentifyPersonRequest(
              ipr.SearchCriteria(ipr.SSIN(national_id)),
              ipr.VerificationData(ipr.PersonData(*pd)))
          
        if birth_date is None:
            raise SimpleException(
                "Either national_id or birth date must be given")
        pc = []
        pc.append(ipr.LastName(last_name))
        pc.append(ipr.FirstName(first_name))
        pc.append(ipr.MiddleName(middle_name))
        pc.append(ipr.BirthDate(birth_date))
        #~ if gender is not None: pc.append(ipr.Gender(gender))
        #~ if tolerance is not None: pc.append(ipr.Tolerance(tolerance))
        root = ipr.IdentifyPersonRequest(
            ipr.SearchCriteria(ipr.PhoneticCriteria(*pc)))
        ipr.validate_root(root)
        return root 
          


class PerformInvestigationRequest(Service):
    """
    A request to the PerformInvestigation BCSS service.
    Net yet used in practice.
    """
    service_id = 'OCMWCPASPerformInvestigation'
    service_version = '20080604'
    xsd_filename = xsdpath('SSDN','OCMW_CPAS',
        'PERFORMINVESTIGATION','PERFORMINVESTIGATIONREQUEST.XSD')
    
    def build_request(pir,ssin,family='1',citizen='1',address='1',wait='1'):
        root = pir.PerformInvestigationRequest(
            pir.SocialSecurityUser(ssin),
            pir.DataGroups(
              pir.FamilyCompositionGroup(family),
              pir.CitizenGroup(citizen),
              pir.AddressHistoryGroup(address),
              pir.WaitRegisterGroup(wait)))

        pir.validate_root(root)
        return root 
    
    

    
        
class HealthInsuranceRequest(Service):
    """
    A request to the HealthInsurance BCSS service.
    Net yet used in practice.
    """
    service_id = 'OCMWCPASHealthInsurance'
    service_version = '20070509'
    
    
    
ipr = IdentifyPersonRequest('ipr') # ,"http://www.ksz-bcss.fgov.be/XSD/SSDN/OCMW_CPAS/IdentifyPerson")
"""
The Namespace for :class:`IdentifyPersonRequest`.
"""

#~ ipr.define("""
#~ IdentifyPersonRequest
#~ SearchCriteria
#~ PhoneticCriteria
#~ SSIN
#~ LastName
#~ FirstName
#~ MiddleName
#~ BirthDate
#~ Gender
#~ Tolerance
#~ Maximum

#~ VerificationData
#~ SISCardNumber
#~ IdentityCardNumber
#~ PersonData 
#~ """)


pir = PerformInvestigationRequest('pir') # ,"http://www.ksz-bcss.fgov.be/XSD/SSDN/OCMW_CPAS/PerformInvestigation")
"""
The Namespace for :class:`PerformInvestigationRequest`.
"""

#~ pir.define("""
#~ PerformInvestigationRequest
#~ SocialSecurityUser
#~ DataGroups
#~ FamilyCompositionGroup
#~ CitizenGroup
#~ AddressHistoryGroup
#~ WaitRegisterGroup
#~ """)

hir = HealthInsuranceRequest('hir') # ,"http://www.ksz-bcss.fgov.be/XSD/SSDN/HealthInsurance")
"""
The Namespace for :class:`HealthInsuranceRequest`.
"""

#~ hir.define("""
#~ HealthInsuranceRequest
#~ SSIN
#~ Assurability
#~ Period
#~ StartDate
#~ EndDate
#~ """)

    





def soap_request(s):
    #~ xg.set_default_namespace(bcss)
    if not isinstance(s,basestring):
        raise Exception("Must give a string, not %r" % s)
    body = bcss.xmlString()
    body.text = etree.CDATA(s)
    #~ body = etree.tostring(body)
    return soap.Envelope(soap.Body(body))
    


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

