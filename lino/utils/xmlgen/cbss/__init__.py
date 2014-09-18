# -*- coding: UTF-8 -*-
# Copyright 2011-2012 Luc Saffre
# License: BSD (see file COPYING for details)


r"""

No longer used since 20120508

This document describes how to communicate with the :term:`CBSS` server 
using Python and Lino. It covers the low-level aspects which might also 
be useful from applications that do not use the other parts of Lino.

To run these examples, you need
Python, Lino and the following Python modules:

- :term:`lxml`
- :term:`appy.pod`


Building SSDN requests
----------------------

This module currently supports the following "classical" SSDN requests:

- :attr:`IPR` : IdentifyPerson
- :attr:`PIR` : PerformInvestigation
- :attr:`HIR` : HealthInsurance
 
:attr:`IPR` has two variants: *with* known NISS or *without*.
If a NISS is given, the other parameters are "verification data". 
For example:

>>> req = IPR.build_request("68060101234",
...   last_name="SAFFRE",birth_date='1968-06-01')

To show what this request contains, we can use lxml's tostring method:

>>> print pretty_print(req) #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
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
date, you'll get a :class:`Warning` (i.e. an Exception whose 
string is meant to be understandable by the user):

>>> req = IPR.build_request(last_name="SAFFRE")
Traceback (most recent call last):
...
Warning: Either national_id or birth date must be given

Here is a valid ipr request:

>>> req = IPR.build_request(last_name="SAFFRE",birth_date='1968-06-01')

Again, we can look at the XML to see what it contains:

>>> print pretty_print(req) #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
<ipr:IdentifyPersonRequest xmlns:ipr="http://.../IdentifyPerson">
  <ipr:SearchCriteria>
    <ipr:PhoneticCriteria>
      <ipr:LastName>SAFFRE</ipr:LastName>
      <ipr:FirstName />
      <ipr:MiddleName />
      <ipr:BirthDate>1968-06-01</ipr:BirthDate>
    </ipr:PhoneticCriteria>
  </ipr:SearchCriteria>
</ipr:IdentifyPersonRequest>


Here is also a PerformInvestigation request:

>>> req = PIR.build_request("68060101234",wait="0")
>>> print pretty_print(req) #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
<pir:PerformInvestigationRequest xmlns:pir="http://.../PerformInvestigation">
  <pir:SocialSecurityUser>68060101234</pir:SocialSecurityUser>
  <pir:DataGroups>
    <pir:FamilyCompositionGroup>1</pir:FamilyCompositionGroup>
    <pir:CitizenGroup>1</pir:CitizenGroup>
    <pir:AddressHistoryGroup>1</pir:AddressHistoryGroup>
    <pir:WaitRegisterGroup>0</pir:WaitRegisterGroup>
  </pir:DataGroups>
</pir:PerformInvestigationRequest>


Executing SSDN requests
-----------------------

The above examples are bare CBSS service requests.
In order to actually execute our request, we'll call the 
:meth:`execute` method. 

The document you are reading uses fictive user parameters and 
doesn't actually execute any real request, 
but if you have the permission to connect to the CBSS server
(see `www.ksz-bcss.fgov.be <http://www.ksz-bcss.fgov.be/fr/bcss/docutheque/content/websites/belgium/services/docutheque.html>`_),
you should be able to reproduce the examples using your correct user parameters.
  
The :meth:`execute` method takes four parameters:

- The request itself (the object returned by `build_request` 
  as explained in the previous section):

  >>> req = PIR.build_request("68060101234",wait="0")
  
- The "environment" to use: ``test``, ``acpt`` or ``prod``.
  In the following examples we leave this *empty* to avoid any actual connection.
  In a Lino application, this is defined in your local 
  :xfile:`settings.py` module 
  (:setting:`cbss.cbss_environment` setting).
  
- You also need to specify a unique reference and a timestamp. 

  >>> import datetime
  >>> now = datetime.datetime(2011,10,31,15,41,10)
  >>> unique_id = 'PIR # 5'

  Your application is responsible for keeping a log of all 
  requests (including also the user who issued the request).
  Lino does this in :mod:`lino.modlib.cbss`.
  
- The "user parameters" required by the CBSS, specified as a normal 
  Python `dict` object. 
  
  For SSDN request it is something like:

  >>> user_params = dict(
  ...     UserID='123456', 
  ...     Email='info@exemple.be', 
  ...     OrgUnit='0123456', 
  ...     MatrixID='17', 
  ...     MatrixSubID='1')

  In a Lino application, these user parameters 
  are defined in your local :xfile:`settings.py` 
  module (:attr:`ssdn_user_params <lino.Lino.ssdn_user_params>`).
  

If you run the following call in a real environment
(with permission to connect, and with correct data in `user_params`), 
it won't raise the `Warning` but return a `response object`:

>>> response = PIR.execute(None,req,user_params,unique_id,now) #doctest: +ELLIPSIS
Traceback (most recent call last):
...
Warning: Not actually sending because environment is empty. Request would be:
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:wsc="http://ksz-bcss.fgov.be/connectors/WebServiceConnector">
<soap:Body>
<wsc:xmlString>
<![CDATA[<ns0:SSDNRequest...</ns0:SSDNRequest>]]>
</wsc:xmlString>
</soap:Body>
</soap:Envelope>



The `response` is currently a simple wrapper around the XML structure 
returned by the CBSS.
Your application is responsible for treating and storing and using this data.
Lino does this in :mod:`lino.modlib.cbss`.


New style services
------------------

A `TestConnectionService` request
---------------------------------

(dicontinued. implemented using suds.)

>> req = TCS.build_request("hello cbss service")

New style services have a different authentication method that requires 
just a username and a password. The `user_params` is also a `dict`, 
but with different keywords:

>> user_params = dict(username='E123456789', password='p123abc')

In a Lino application, this is defined in the 
:attr:`cbss2_user_params <lino.Lino.cbss2_user_params>` setting
of your local :xfile:`settings.py` module.

A `TestConnectionService` request doesn't need a unique_id and timestamp.

>> response = tcs.execute(None,req,user_params) #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
Traceback (most recent call last):
...
Warning: Not actually sending because environment is empty. Request would be:
<?xml version='1.0' encoding='ASCII'?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tcs="http://kszbcss.fgov.be/intf/TestConnectionServiceService/v1"><soap:Header/><soap:Body><tcs:sendTestMessageRequest><tcs:echo>hello cbss service</tcs:echo></tcs:sendTestMessageRequest></soap:Body></soap:Envelope>

Note that the generated XML also specifies a namespace for 
the `echo` tag (`<tcs:echo>` instead of `<echo>`). 
Don't know yet whether this is okay.


"""

USE_XSD_FILES = False

CBSS_ENVS = ('test', 'acpt', 'prod')


import os

from appy.shared.dav import Resource
from appy.shared.xml_parser import XmlUnmarshaller

#~ from lxml import etree
#~ from xml. import etree
#~ from lino.utils.xmlgen.recipe576536 import CDATA
#~ from xml.etree import ElementTree as etree
from lino.utils.xmlgen import etree
#~ import ElementTree as etree


#~ from lino.utils import d2iso
#~ from lino.utils import IncompleteDate
from lino.utils.xmlgen import Namespace, pretty_print, prettify


def xsdpath(*parts):
    p1 = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(p1, 'XSD', *parts)

import datetime


def format(v):
    if isinstance(v, datetime.datetime):
        return v.strftime("%Y%m%dT%H%M%S")
    if isinstance(v, datetime.date):
        return v.strftime("%Y-%m-%d")
    return str(v)


#~ ssdn = Namespace('ssdn',"http://www.ksz-bcss.fgov.be/XSD/SSDN/Service")
#~ ,nsmap={None:ssdn._url}
#~ class SOAP(Namespace):
    #~ targetNamespace = "http://schemas.xmlsoap.org/soap/envelope/"
    #~ def setup_namespace(self):
        #~ self.define_names("Body Envelope Header")
#~ soap = SOAP('soap')
SOAP = Namespace(
    "http://schemas.xmlsoap.org/soap/envelope/",
    names="Body Envelope Header", prefix="soap")


class WebServiceConnector(Namespace):

    """
    The WebServiceConnector namespace used for wrapping "classical" CBSS services.
    """
    targetNamespace = "http://ksz-bcss.fgov.be/connectors/WebServiceConnector"
    prefix = 'wsc'

    def setup_namespace(self):
        self.define_names("xmlString")

    def soap_request(self, s):
        #~ xg.set_default_namespace(bcss)
        if not isinstance(s, basestring):
            raise Exception("Must give a string, not %r" % s)
        body = self.xmlString(etree.CDATA(s))
        #~ body.text =
        #~ body = etree.tostring(body)
        return SOAP.Envelope(SOAP.Body(body))

unused_WSC = WebServiceConnector()


class SSDNns(Namespace):

    """
    The SSDN namespace used for wrapping "classical" CBSS services.
    """
    targetNamespace = "http://www.ksz-bcss.fgov.be/XSD/SSDN/Service"
    names = """
    SSDNRequest
    ServiceRequest
    ServiceId
    Version
    RequestContext
    Message
    Reference
    TimeRequest
    """

SSDN = SSDNns()


class Common(Namespace):

    def setup_namespace(self):
        self.define_names("""
        AuthorizedUser
        UserID
        Email
        OrgUnit
        MatrixID
        MatrixSubID
        """)

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


ENV_TEST = 'test'
ENV_ACPT = 'acpt'
ENV_PROD = 'prod'


class Service(Namespace):

    """
    Base class for the individual services.
    """
    service_id = None

    def get_url(self, env):
        return None

    def build_request(self, *args, **kw):
        raise NotImplementedError

    #~ def execute(self,req,env,user_params=None,unique_id=None,dt=None):
    def execute(self, req, unique_id=None, dt=None):
        #~ print 20120302
        #~ if user_params is None:
            #~ raise Warning(
                #~ "Not actually sending because user_params is empty.")
        #~ self.validate_against_xsd(req)
        from django.conf import settings
        env = settings.SITE.cbss_environment
        user_params = settings.SITE.cbss_user_params

        req = self.wrap_request(req, unique_id, dt, user_params)

        #~ xml = etree.tostring(req,xml_declaration=True)
        xml = etree.tostring(req)

        if not env:
            raise Warning("""\
Not actually sending because environment is empty. Request would be:
""" + prettify(xml))

        #~ assert env in (ENV_TEST, ENV_ACPT, ENV_PROD)
        assert env in CBSS_ENVS

        url = self.get_url(env)

        if True:
            #~ x = etree.tostring(elem)
            from suds.client import Client
            url += '?WSDL'
            client = Client(url)
            #~ print 20120507, url
            #~ print client
            res = client.service.sendXML(xml)
        else:

            if isinstance(self, NewStyleService):
                server = Resource(url, measure=True, **user_params)
            else:
                server = Resource(url, measure=True)
            res = server.soap(xml)
        return res

        #~ print res.code
        #~ print res.data
        #~ reply = XmlUnmarshaller().parse(str(res.data.xmlString))
        #~ return reply

    def wrap_request(self, srvReq, message_ref, dt, user_params):
        raise NotImplementedError


#~ class NewStyleService(Service):

    #~ def wrap_request(self,srvReq,message_ref,dt,user_params):
        # ~ # soap = SOAP('soap',used_namespaces=[self])
        #~ return SOAP.Envelope(SOAP.Header(),SOAP.Body(srvReq))


#~ class TestConnectionService(NewStyleService):
    # ~ # xsd_filename = xsdpath('TestConnectionServiceV1.xsd')
    #~ targetNamespace = "http://kszbcss.fgov.be/intf/TestConnectionServiceService/v1"

    #~ def setup_namespace(self):
        #~ self.define_names("sendTestMessageRequest echo")

    #~ def build_request(self,helloString):
        #~ return self.sendTestMessageRequest(self.echo(helloString))
        # ~ # self.validate_root(root)
        # ~ # return root

    #~ def get_url(self,env):
        #~ url = "https://bcssksz-services-%s.smals.be:443/SOA4520" % env
        #~ url += "/TestConnectionServiceService/sendTestMessage"
        #~ return url

#~ tcs = TestConnectionService('tcs')

class SSDNService(Service):

    service_version = None

    def get_url(self, env):
        url = "https://bcssksz-services-%s.smals.be" % env
        url += "/connectors/webservice/KSZBCSSWebServiceConnectorPort"
        return url

    def wrap_request(self, srvReq, message_ref, dt, user_params):
        #~ xg.set_default_namespace(None)
        any = etree.tostring(srvReq)
        serviceRequest = SSDN.ServiceRequest(
            SSDN.ServiceId(self.service_id),
            SSDN.Version(self.service_version),
            etree.XML(any))

        context = SSDN.RequestContext(
            common.authorized_user(**user_params),
            SSDN.Message(
                SSDN.Reference(message_ref),
                SSDN.TimeRequest(format(dt))))
        #~ xg.set_default_namespace(SSDN)
        elem = SSDN.SSDNRequest(context, serviceRequest)
        #~ elem.nsmap={None:self._url}
        #~ elem = WSC.soap_request(etree.tostring(elem))
        if True:
            return elem
        else:
            elem = WSC.soap_request(etree.tostring(elem))
        #~ xmlString = """<?xml version="1.0" encoding="utf-8"?>""" +
        return elem
        #~ return ssdn.SSDNRequest(context,serviceRequest)


class IdentifyPersonRequest(SSDNService):

    "A request for identifying a person or validating a person's identity"
    service_id = 'OCMWCPASIdentifyPerson'
    service_version = '20050930'
    targetNamespace = "http://www.ksz-bcss.fgov.be/XSD/SSDN/OCMW_CPAS/IdentifyPerson"
    prefix = "ipr"
    if USE_XSD_FILES:
        xsd_filename = xsdpath('SSDN', 'OCMW_CPAS',
                               'IDENTIFYPERSON', 'IDENTIFYPERSONREQUEST.XSD')

    def setup_namespace(self):
        self.define_names("""
        IdentifyPersonRequest
        SearchCriteria
        PhoneticCriteria
        SSIN
        LastName
        FirstName
        MiddleName
        BirthDate
        Gender
        Tolerance
        Maximum

        VerificationData
        SISCardNumber
        IdentityCardNumber
        PersonData 
        """)

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
            if last_name:
                pd.append(ipr.LastName(last_name))
            if first_name:
                pd.append(ipr.FirstName(first_name))
            if middle_name:
                pd.append(ipr.MiddleName(middle_name))
            if birth_date:
                pd.append(ipr.BirthDate(birth_date))
            if gender is not None:
                pd.append(ipr.Gender(gender))
            if tolerance is not None:
                pd.append(ipr.Tolerance(tolerance))

            #~ for k in ('LastName','FirstName','MiddleName','BirthDate'):
                #~ v = kw.get(k,None)
                # ~ if v: # ignore empty values
                    #~ cl = getattr(ipr,k)
                    #~ pd.append(cl(v))
            return ipr.IdentifyPersonRequest(
                ipr.SearchCriteria(ipr.SSIN(national_id)),
                ipr.VerificationData(ipr.PersonData(*pd)))

        if birth_date is None:
            raise Warning(
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
        #~ ipr.validate_root(root)
        return root


class PerformInvestigationRequest(SSDNService):

    """
    A request to the PerformInvestigation BCSS service.
    Net yet used in practice.
    """
    service_id = 'OCMWCPASPerformInvestigation'
    service_version = '20080604'
    targetNamespace = "http://www.ksz-bcss.fgov.be/XSD/SSDN/OCMW_CPAS/PerformInvestigation"
    prefix = 'pir'

    if USE_XSD_FILES:
        xsd_filename = xsdpath('SSDN', 'OCMW_CPAS',
                               'PERFORMINVESTIGATION', 'PERFORMINVESTIGATIONREQUEST.XSD')

    def setup_namespace(self):
        self.define_names("""
        PerformInvestigationRequest
        SocialSecurityUser
        DataGroups
        FamilyCompositionGroup
        CitizenGroup
        AddressHistoryGroup
        WaitRegisterGroup
        """)

    def build_request(self, ssin, family='1', citizen='1', address='1', wait='1'):
        root = self.PerformInvestigationRequest(
            self.SocialSecurityUser(ssin),
            self.DataGroups(
                self.FamilyCompositionGroup(family),
                self.CitizenGroup(citizen),
                self.AddressHistoryGroup(address),
                self.WaitRegisterGroup(wait)))

        #~ pir.validate_root(root)
        return root


class ManageAccessRequest(SSDNService):
    targetNamespace = "http://www.ksz-bcss.fgov.be/XSD/SSDN/OCMW_CPAS/ManageAccess"
    prefix = 'mar'
    service_id = 'OCMWCPASManageAccess'
    service_version = '20070509'
    names = """
    ManageAccessRequest
    SSIN
    Purpose
    Period
    Action
    Sector
    QueryRegister
    ProofOfAuthentication
    """


class HealthInsuranceRequest(SSDNService):

    """
    A request to the HealthInsurance BCSS service.
    Net yet used in practice.
    """
    service_id = 'OCMWCPASHealthInsurance'
    service_version = '20070509'
    targetNamespace = "http://www.ksz-bcss.fgov.be/XSD/SSDN/HealthInsurance"

    def setup_namespace(self):
        self.define_names("""
        HealthInsuranceRequest
        SSIN
        Assurability
        Period
        StartDate
        EndDate
        """)


IPR = IdentifyPersonRequest()
"""
The Namespace instance for :class:`IdentifyPersonRequest`.
"""


# ,"http://www.ksz-bcss.fgov.be/XSD/SSDN/OCMW_CPAS/PerformInvestigation")
PIR = PerformInvestigationRequest()
"""
The Namespace instance for :class:`PerformInvestigationRequest`.
"""


HIR = HealthInsuranceRequest()
"""
The Namespace instance for :class:`HealthInsuranceRequest`.
"""

MAR = ManageAccessRequest()
"""
The Namespace instance for :class:`ManageAccessRequest`.
"""


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


def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()
