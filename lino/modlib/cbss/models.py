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

u"""
Adds models and tables used to make the following :term:`CBSS` requests
(descriptions taken from `SYNTHESE_SERVICESXML_CPAS_FR.DOC`):

- :class:`IdentifyPersonRequest` :
  Identifier la personne par son NISS ou ses données phonétiques et vérifier son identité par le numéro de carte SIS, de carte d'identité ou par ses données phonétiques ()

- :class:`ManageAccessRequest`: 
  Enregistrer, désenregistrer ou consulter (:class:`ManageAction`) un dossier 
  dans le registre du réseau de la sécurité sociale (registre BCSS) 
  et dans le répertoire sectoriel des CPAS géré par la SmalS-MvM (:class:`QueryRegister`).
  
  - `ManageAction.REGISTER` : 
    Ce service est sollicité au moment du démarrage de l’enquête sociale.  
    Le CPAS déclare au réseau de la sécurité sociale qu’il possède un dossier pour lequel il a 
    l’autorisation (dispositions légales et réglementaires) d’obtenir des informations des autres 
    institutions en vue de compléter son enquête dans le cadre de l’octroi du revenu d’intégration.  
    Cette déclaration concerne le répertoire sectoriel des CPAS à la SmalS-MvM et peut 
    concerner plusieurs catégories de personnes : 
    le demandeur, les cohabitants et les tiers concernés 
    et ce, pour des finalités différentes. 
  - `ManageAction.UNREGISTER` : 
    L’opération contraire est aussi mise à disposition. 
  - `ManageAction.LIST` : 
    Il est en plus possible d’obtenir une liste des enregistrements 
    dans le répertoire sectoriel des CPAS à la SmalS-MvM 
    ainsi qu’au sein du réseau BCSS.
  
- :class:`RetrieveTIGroupsRequest`: 
  Obtenir des informations à propos d’une personne dans le cadre de l’enquête sociale.



"""

import os
import shutil
import traceback
import datetime
import logging
logger = logging.getLogger(__name__)


from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from appy.shared.xml_parser import XmlUnmarshaller


from lino import mixins
from lino import dd
from lino.utils import Warning
from lino.utils import join_words
from lino.utils import AttrDict, IncompleteDate
from lino.tools import obj2str

from lino.utils import babel
from lino.utils.choosers import chooser

#~ from lino.utils import dblogger
#~ from lino.tools import resolve_model
#~ from lino.utils.xmlgen import etree
#~ from lino.utils.xmlgen import cbss


from lino.utils.choicelists import ChoiceList
from lino.utils.choicelists import Gender
from lino.utils.choicelists import UserLevel
#~ from lino.modlib.contacts import models as contacts
from lino.tools import makedirs_if_missing
#~ from lino.mixins.printable import DirectPrintAction

from lino.apps.pcsw import models as pcsw

try:
  
    import suds
    from suds.client import Client
    from suds.transport.http import HttpAuthenticated
    from suds.transport.http import HttpTransport
    from suds.sax.element import Element as E
    from suds.sax.parser import Parser
    PARSER = Parser()

except ImportError, e:
    pass

countries = dd.resolve_app('countries')

CBSS_ENVS = ('test', 'acpt', 'prod')

def xsdpath(*parts):
    p1 = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(p1,'XSD',*parts)

CBSS_ERROR_MESSAGE = "CBSS error %s:\n"

def gender2cbss(gender):
    if gender == Gender.male:
        return '1'
    elif gender == Gender.female:
        return '2'
    else:
        return '0'
            

def cbss2gender(v):
    if v == '1':
        return Gender.male
    elif v == '2':
        return Gender.female
    return None
      
def cbss2date(s):
    a = s.split('-')
    assert len(a) == 3
    a = [int(i) for i in a]
    return IncompleteDate(*a)


def cbss2civilstate(node):
    value = nodetext(node)
    if not value:
        return value
    v = pcsw.CivilState.get_by_value(value)
    if v is None:
        print "20120601 cbss2civilstate None for ", repr(value)
    return unicode(v)
    
def nodetext(node):
    if node is None:
        return ''
    return node.text
    
def cbss2country(code):
    try:
        return countries.Country.objects.get(inscode=code)
    except Country.DoesNotExist:
        logger.warning("Unknown country code %s",code)
    
    
def cbss2address(obj,**data):
    n = obj.childAtPath('/Basic/DiplomaticPost')
    if n is not None:
        data.update(country=cbss2country(nodetext(n.childAtPath('/CountryCode'))))
        #~ n.childAtPath('/Post')
        data.update(address=nodetext(n.childAtPath('/AddressPlainText')))
        return data
    n = obj.childAtPath('/Basic/Address')
    if n is not None:
        data.update(country=cbss2country(nodetext(n.childAtPath('/CountryCode'))))
        #~ country = countries.Country.objects.get(
            #~ inscode=n.childAtPath('/CountryCode').text)
        addr = ''
        #~ addr += n.childAtPath('/MunicipalityCode').text
        addr += join_words(
            nodetext(n.childAtPath('/Street')),
            nodetext(n.childAtPath('/HouseNumber')),
            nodetext(n.childAtPath('/Box'))
            )
        addr += ', ' + join_words(
            nodetext(n.childAtPath('/PostalCode')),
            nodetext(n.childAtPath('/Municipality'))
            )
        data.update(address=addr)
    return data
    
    
    
class RequestStatus(ChoiceList):
    """
    The status of a :class:`CBSSRequest`.
    """
    label = _("Status")

add = RequestStatus.add_item
add('0',_("New"),'new')
add('1',_("Pending"),'pending')
add('2',_("Failed"),'failed')
add('3',_("OK"),'ok')
add('4',_("Warnings"),'warnings')
add('5',_("Errors"),'errors')
add('6',_("Validated"),'validated')
#~ add('6',_("Invalid reply"),'invalid')
#~ add('9',_("Fictive"),'fictive')
  
#~ class Environment(ChoiceList):
    #~ """
    #~ The environment where a :class:`CBSSRequest` is being executed.
    #~ """
    #~ label = _("Environment")
#~ add = Environment.add_item
#~ add('t',_("Test"),alias='test')
#~ add('a',_("Acceptance"),alias='acpt')
#~ add('p',_("Production"),alias='prod')
  

    
    


class SendAction(dd.RowAction):
    """
    This defines the "Execute" button on a 
    :class:`CBSSRequest` or
    :class:`SSDNRequest` 
    record.
    """
    readonly = False
    url_action_name = 'send'
    label = _('Execute')
    #~ callable_from = None
    callable_from = (dd.GridEdit,dd.ShowDetailAction)
    
    #~ def get_row_permission(self,user,obj):
        #~ if obj.ticket:
            #~ return False
        #~ return super(SendAction,self).get_row_permission(user,obj)
      
    def run(self,obj,ar,**kw):
        obj.execute_request(ar)
        if obj.status == RequestStatus.failed:
            kw.update(message=obj.logged_messages)
            kw.update(alert=True)
        elif obj.status == RequestStatus.warnings:
            kw.update(message=_("Got valid response, but it contains warnings."))
            kw.update(alert=True)
        kw.update(refresh=True)
        return ar.ui.success_response(**kw)



class Sector(babel.BabelNamed):
    """
    Default values filled from :mod:`lino.modlib.cbss.fixtures.sectors`.
    """
    class Meta:
        verbose_name = _("Sector")
        verbose_name_plural = _('Sectors')
        unique_together = ['code','subcode']
        
    #~ code = models.CharField(max_length=2,verbose_name=_("Code"),primary_key=True)
    code = models.IntegerField(max_length=2,verbose_name=_("Code"))
    subcode = models.IntegerField(max_length=2,verbose_name=_("Subcode"),default=0)
    abbr = babel.BabelCharField(_("Abbreviation"),max_length=50,blank=True)
    
    
    def __unicode__(self):
        #~ return '(' + str(self.code) + ') ' + babel.BabelNamed.__unicode__(self)
        if self.subcode != 0:
            return str(self.code) + '.' + str(self.subcode) + ' - ' + babel.BabelNamed.__unicode__(self)
        return str(self.code) + ' - ' + babel.BabelNamed.__unicode__(self)
        

class Sectors(dd.Table):
    model = Sector
    required_user_groups = ['cbss']
    column_names = 'code subcode abbr name *'
    order_by = ['code','subcode']


class Purpose(babel.BabelNamed):
    u"""
    Codes qualité (Hoedanigheidscodes),
    http://www.bcss.fgov.be/binaries/documentation/fr/documentation/general/lijst_hoedanigheidscodes.pdf
    """
    class Meta:
        verbose_name = _("Purpose")
        verbose_name_plural = _('Purposes')
        unique_together = ['sector_code','code']
    sector_code = models.IntegerField(max_length=2,verbose_name=_("Sector"),blank=True,null=True)
    #~ sector_subcode = models.IntegerField(max_length=2,verbose_name=_("Subsector"),blank=True,null=True)
    #~ sector = models.ForeignKey(Sector,blank=True,null=True)
    #~ code = models.CharField(max_length=3,verbose_name=_("Code"))
    code = models.IntegerField(max_length=3,verbose_name=_("Code"))
    
    def __unicode__(self):
        #~ return '(' + str(self.code) + ') ' + babel.BabelNamed.__unicode__(self)
        return str(self.code) + ' - ' + babel.BabelNamed.__unicode__(self)
        

class Purposes(dd.Table):
    model = Purpose
    required_user_groups = ['cbss']
    column_names = 'sector_code code name *'
    order_by = ['sector_code','code']




NSCOMMON = ('common','http://www.ksz-bcss.fgov.be/XSD/SSDN/Common')
NSSSDN = ('ssdn','http://www.ksz-bcss.fgov.be/XSD/SSDN/Service')
NSIPR = ('ipr',"http://www.ksz-bcss.fgov.be/XSD/SSDN/OCMW_CPAS/IdentifyPerson")
NSMAR = ('mar',"http://www.ksz-bcss.fgov.be/XSD/SSDN/OCMW_CPAS/ManageAccess")
NSWSC = ('wsc',"http://ksz-bcss.fgov.be/connectors/WebServiceConnector")


#~ class CBSSRequest(mixins.ProjectRelated,mixins.AutoUser):
class CBSSRequest(mixins.AutoUser,mixins.Printable):
    """
    Common Abstract Base Class for :class:`SSDNRequest`
    and :class:`NewStyleRequest`
    """
    
    wsdl_parts = NotImplementedError
    
    class Meta:
        abstract = True
        
    person = models.ForeignKey(
        settings.LINO.person_model,
        verbose_name=_("Client"))
    
    sent = models.DateTimeField(
        verbose_name=_("Sent"),
        blank=True,null=True,
        editable=False,
        help_text="""\
The date and time when this request has been executed. 
This is empty for requests than haven't been sent.
Read-only.""")
    
    status = RequestStatus.field(default=RequestStatus.new,editable=False)
    environment = models.CharField(max_length=4,editable=False,verbose_name=_("T/A/B"))
    ticket  = models.CharField(max_length=36,editable=False,verbose_name=_("Ticket"))
    #~ environment = Environment.field(blank=True,null=True)
    
    # will probably go away soon
    request_xml = models.TextField(verbose_name=_("Request"),
        editable=False,blank=True,
        help_text="""The raw XML string that has (or would have) been sent.""")
    
    response_xml = models.TextField(
        verbose_name=_("Response"),
        editable=False,blank=True,
        help_text="""\
The response received, raw XML string. 
If the request failed with a local exception, then it contains a traceback.""")

    logged_messages = models.TextField(
        verbose_name=_("Logged messages"),
        editable=False,blank=True,
        help_text="""Logged messages about this request.""")

    send_action = SendAction()
    print_action = mixins.DirectPrintAction()
    
    
    #~ def save(self,*args,**kw):
        #~ if not self.environment:
            #~ self.environment = settings.LINO.cbss_environment or ''
        #~ super(CBSSRequest,self).save(*args,**kw)

    #~ def disable_editing(self,ar):
        #~ if self.ticket: return True

    def on_cbss_ok(self,reply):
        """
        Called when a successful reply has been received.
        """
        pass
        
    #~ @classmethod
    #~ def setup_report(cls,rpt):
        #~ # call_optional_super(CBSSRequest,cls,'setup_report',rpt)
        #~ rpt.add_action(SendAction())
        
    def logmsg(self,s,*args):
        if args:
            s = s % args
        self.logged_messages += ("[%s] " % datetime.datetime.now()) + s + '\n'
        
    def __unicode__(self):
        return u"%s #%s" % (self._meta.verbose_name,self.pk)

    def execute_request(self,ar=None,now=None,simulate_response=None,environment=None):
        """
        This is the general method for all SSDN services,
        executed when a user runs :class:`SendAction`.
        """
        if ar is not None:
            logger.info("%s executes CBSS request %s",ar.get_user(),self)
        if self.ticket:
            raise Exception("Tried to re-execute %s with non-empty ticket." % self)
        if now is None:
            now = datetime.datetime.now()
        if environment is None:
            environment = settings.LINO.cbss_environment or ''
            
        self.environment = environment
        self.sent = now
        
        if not settings.LINO.cbss_live_tests:
            if simulate_response is None and environment:
                self.validate_request()
                self.status = RequestStatus.validated
                self.save()
                return
                
        self.status = RequestStatus.pending
        self.save()
        
        retval = None
        try:
            #~ if not settings.LINO.cbss_live_tests:
                #~ self.validate_request()
            retval = self.execute_request_(now,simulate_response)
        except (IOError,Warning),e:
            self.status = RequestStatus.failed
            self.logmsg(unicode(e))
        except Exception,e:
            self.status = RequestStatus.failed
            #~ self.response_xml = traceback.format_exc(e)
            self.logmsg(traceback.format_exc(e))

        self.save()
        return retval


    
    #~ @dd.action(_("Validate"))
    #~ def validate(self,ar):
        #~ try:
            #~ self.validate_request()
            #~ self.save()
            #~ return ar.ui.success_response(
                #~ message="%s validation passed." % self)
        #~ except Exception,e:
            #~ self.logmsg(traceback.format_exc(e))
            #~ self.save()
            #~ return ar.ui.error_response(e)
          
        
          
        
        
            
    def validate_request(self):
        pass

    def get_wsdl_uri(self):
        url = os.path.join(settings.MEDIA_ROOT,*self.wsdl_parts) 
        if not url.startswith('/'):
            # on a windows machine we need to prepend an additional "/"
            url = '/' + url
        if os.path.sep != '/':
            url = url.replace(os.path.sep,'/')
        url = 'file://' + url 
        return url

    def check_environment(self,req):
        if not self.environment:
            raise Warning("""\
Not actually sending because environment is empty. Request would be:
""" + unicode(req))

        assert self.environment in CBSS_ENVS

    @dd.virtualfield(dd.HtmlBox(_("Result")))
    def result(self,ar):
        return self.response_xml
        
#~ dd.update_field(CBSSRequest,'project',blank=False,null=False)
dd.update_field(CBSSRequest,'user',blank=False,null=False)

class CBSSRequestDetail(dd.DetailLayout):
    #~ main = 'request response'
    main = 'request technical'
    
    request = """
    info
    parameters
    result
    """
    
    technical = """
    response_xml 
    logged_messages
    """
    
    info = """
    id person user environment sent status ticket
    """
    
    #~ response = "response_xml\nlogged_messages"
    
    def setup_handle(self,lh):
        lh.request.label = _("Request")
        lh.info.label = _("Request information")
        lh.result.label = _("Result")
        lh.technical.label = _("Technical")
        lh.technical.required_user_level = UserLevel.manager
        #~ lh.response.label = _("Response")
        #~ lh.log.label = _("Log")
        lh.parameters.label = _("Parameters")
    

class SSDNRequest(CBSSRequest):
    """
    Abstract Base Class for Models that represent 
    SSDN ("classic") requests to the :term:`CBSS`.
    """
    
    wsdl_parts = ('cache','wsdl','WebServiceConnector.wsdl')
    
    xsd_filename = None
    
    class Meta:
        abstract = True
        
    def validate_against_xsd(self,srvreq,xsd_filename):
        #~ logger.info("20120524 Validate against %s", xsd_filename)
        from lxml import etree
        xml = unicode(srvreq)
        #~ print xml
        doc = etree.fromstring(xml)
        schema_doc = etree.parse(xsd_filename)
        schema = etree.XMLSchema(schema_doc)
        #~ if not schema.validate(doc):
            #~ print xml
        schema.assertValid(doc)
        #~ self.logmsg("Validated %s against %s", xml,xsd_filename)
        self.logmsg("Validated %s against %s", self,xsd_filename)
      
    def validate_wrapped(self,srvreq):
        self.validate_against_xsd(srvreq,xsdpath('SSDN','Service','SSDNRequest.xsd'))
        
        
    def validate_inner(self,srvreq):
        if not self.xsd_filename: return
        self.validate_against_xsd(srvreq,self.xsd_filename)
        
    
    def validate_request(self):
        """
        Validates the generated XML against the XSD files.
        Used by test suite.
        It is not necessary to validate each real request before actually sending it.
        """
        srvreq = self.build_request()
        self.validate_inner(srvreq)
        wrapped_srvreq = self.wrap_ssdn_request(srvreq,datetime.datetime.now())
        self.validate_wrapped(wrapped_srvreq)
      
    def execute_request_(self,now,simulate_response):
        "SSDN specific part of a request."
        srvreq = self.build_request()
        
        #~ if validate:
            #~ self.validate_inner(srvreq)
            
        wrapped_srvreq = self.wrap_ssdn_request(srvreq,now)
        
        #~ if validate:
            #~ self.validate_wrapped(wrapped_srvreq)
            #~ logger.info("XSD validation passed.")
            
        if simulate_response is None:
            self.check_environment(srvreq)
            url = self.get_wsdl_uri()
            
            #~ logger.info("Instantiate Client at %s", url)
            t = HttpTransport()
            client = Client(url, transport=t)
            #~ print 20120507, client
        
            xmlString = unicode(wrapped_srvreq)
            self.request_xml = xmlString
            #~ logger.info("20120521 Gonna sendXML(<xmlString>):\n%s",xmlString)
            if not settings.LINO.cbss_live_tests:
                #~ raise Warning("NOT sending because `cbss_live_tests` is False:\n" + unicode(xmlString))
                raise Warning(
                    "NOT sending because `cbss_live_tests` is False:\n" + xmlString)
            #~ xmlString.append(wrapped_srvreq)
            self.logmsg("client.service.sendXML(\n%s\n)",xmlString)
            res = client.service.sendXML(xmlString)
            #~ print 20120522, res
            self.response_xml = unicode(res)
            #~ self.save()
            #~ return self.fill_from_string(res.encode('utf-8'),xmlString)
            return self.fill_from_string(res.encode('utf-8'))
        else:
            self.environment = 'demo'
            return self.fill_from_string(simulate_response)
                
        
    def fill_from_string(self,s,sent_xmlString=None):
        #~ self.response_xml = unicode(res)
        reply = PARSER.parse(string=s).root()
        self.ticket = nodetext(reply.childAtPath('/ReplyContext/Message/Ticket'))
        rs = reply.childAtPath('/ServiceReply/ResultSummary')
        if rs is None:
            raise Warning("Unexpected CBSS reply:\n%s" % reply)
        rc = nodetext(rs.childAtPath('/ReturnCode'))
        #~ print reply.__class__, dir(reply)
        #~ print reply
        #~ rc = reply.root().SSDNReply.ServiceReply.ResultSummary.ReturnCode
        if rc == '0':
            self.status = RequestStatus.ok
        elif rc == '1':
            self.status = RequestStatus.warnings
            self.logmsg("Warnings:==============\n%s\n===============" % s)
        #~ elif rc == '10000':
            #~ self.status = RequestStatus.errors
        else:
            #~ self.status = RequestStatus.errors
            #~ self.response_xml = unicode(reply)
            if False and sent_xmlString is not None:
                msg = """\
%s : CBSS returned error %s 
======= xmlString sent:
%s
======= response:
%s
=======
""" % (self,rc,sent_xmlString,unicode(reply))
                logger.warning(msg)
            dtl = rs.childAtPath('/Detail')
            msg = CBSS_ERROR_MESSAGE % rc
            keys = ('Severity', 'ReasonCode', 'Diagnostic', 'AuthorCodeList')
            msg += '\n'.join([
                k+' : '+nodetext(dtl.childAtPath('/'+k))
                    for k in keys])
            raise Warning(msg)
            #~ return None
            #~ raise Exception("Got invalid response status")
            
        #~ self.on_cbss_ok(reply)
        service_reply = self.get_service_reply(reply)
        if service_reply is None:
            raise Exception(
              "Return code is %r, but there's no service reply." % rc)
              #~ "Return code is %r but there's no service reply in:\n%s\n" % (rc,reply))
        #~ reply.childAtPath('/ServiceReply/IdentifyPersonReply')
        self.response_xml = unicode(service_reply)
        return service_reply
        
        
    def get_service_reply(self,full_reply=None):
        raise NotImplementedError()
        
        
        
    def wrap_ssdn_request(self,srvreq,dt):
        """
        Wrap the given service request into the SSDN envelope 
        by adding AuthorizedUser and other information common 
        the all SSDN requests).
        """
        #~ up  = settings.LINO.ssdn_user_params
        #~ user_params = settings.LINO.cbss_user_params
        sc = settings.LINO.site_config
        #~ au = E('common:AuthorizedUser',ns=NSCOMMON)
        #~ au.append(E('common:UserID').setText(up['UserID']))
        #~ au.append(E('common:Email').setText(up['Email']))
        #~ au.append(E('common:OrgUnit').setText(up['OrgUnit']))
        #~ au.append(E('common:MatrixID').setText(up['MatrixID']))
        #~ au.append(E('common:MatrixSubID').setText(up['MatrixSubID']))
        au = E('ssdn:AuthorizedUser')
        #~ au.append(E('ssdn:UserID').setText(user_params['UserID']))
        au.append(E('ssdn:UserID').setText(sc.ssdn_user_id))
        #~ au.append(E('ssdn:Email').setText(user_params['Email']))
        #~ if not sc.site_company:
            #~ raise Exception("")
        #~ au.append(E('ssdn:Email').setText(sc.site_company.email))
        au.append(E('ssdn:Email').setText(sc.ssdn_email))
        #~ au.append(E('ssdn:OrgUnit').setText(user_params['OrgUnit']))
        #~ au.append(E('ssdn:OrgUnit').setText(sc.site_company.vat_id))
        au.append(E('ssdn:OrgUnit').setText(sc.cbss_org_unit))
        #~ au.append(E('ssdn:MatrixID').setText(user_params['MatrixID']))
        au.append(E('ssdn:MatrixID').setText(sc.sector.code))
        #~ au.append(E('ssdn:MatrixSubID').setText(user_params['MatrixSubID']))
        au.append(E('ssdn:MatrixSubID').setText(sc.sector.subcode))
        
        ref = "%s # %s" % (self.__class__.__name__,self.id)
        msg = E('ssdn:Message')
        msg.append(E('ssdn:Reference').setText(ref))
        msg.append(E('ssdn:TimeRequest').setText(dt.strftime("%Y%m%dT%H%M%S")))
        
        context = E('ssdn:RequestContext')
        context.append(au)
        context.append(msg)
        
        sr = E('ssdn:ServiceRequest')
        sr.append(E('ssdn:ServiceId').setText(self.ssdn_service_id))
        sr.append(E('ssdn:Version').setText(self.ssdn_service_version))
        sr.append(srvreq)
        
        
        #~ xg.set_default_namespace(SSDN)
        e = E('ssdn:SSDNRequest',ns=NSSSDN)
        e.append(context)
        e.append(sr)
        #~ if srvreq.prefix != e.prefix:
            #~ e.addPrefix(srvreq.prefix,srvreq.nsprefixes[srvreq.prefix])
        
        return e
      

class NewStyleRequest(CBSSRequest):
    """
    Abstract Base Class for Models that represent 
    "new style" requests to the :term:`CBSS` (and responses).
    """
    
    class Meta:
        abstract = True
        
    def execute_request_(self,now,simulate_response):
      
        url = self.get_wsdl_uri()
        
        #~ logger.info("Instantiate Client at %s", url)
        sc = settings.LINO.site_config
        #~ t = HttpAuthenticated(
            #~ username=settings.LINO.cbss_username, 
            #~ password=settings.LINO.cbss_password)
        t = HttpAuthenticated(
            username=sc.cbss_http_username, 
            password=sc.cbss_http_password)
        client = Client(url, transport=t)
        #print client

        ci = client.factory.create('ns0:CustomerIdentificationType')
        #~ cbeNumber = client.factory.create('ns0:CbeNumberType')
        #~ ci.cbeNumber = settings.LINO.cbss_cbe_number
        #~ ci.cbeNumber = settings.LINO.site_config.site_company.vat_id
        ci.cbeNumber = sc.cbss_org_unit
        info = client.factory.create('ns0:InformationCustomerType')
        info.ticket = str(self.id)
        info.timestampSent = now
        info.customerIdentification = ci
        
        res = self.execute_newstyle(client,info)
        
        return res
        
        
    def on_cbss_ok(self,reply):
        """
        Called when a successful reply has been received.
        """
        pass
        
    #~ @classmethod
    #~ def setup_report(cls,rpt):
        #~ # call_optional_super(CBSSRequest,cls,'setup_report',rpt)
        #~ rpt.add_action(SendAction())
        
    #~ def __unicode__(self):
        #~ return u"%s#%s" % (self.__class__.__name__,self.pk)
        
    def execute_newstyle(self,client,infoCustomer):
        raise NotImplementedError()











class SSIN(models.Model):
    """
    Abstract base for models that have a field `national_id` and a method 
    :meth:`get_ssin`.
    """
    class Meta:
        abstract = True
  
    national_id = models.CharField(max_length=200,
        blank=True,verbose_name=_("National ID")
        ,validators=[pcsw.niss_validator]
        )
        
    birth_date = dd.IncompleteDateField(
        blank=True,
        verbose_name=_("Birth date"))
    sis_card_no = models.CharField(verbose_name=_('SIS card number'),
        max_length=10,
        blank=True, help_text="""\
The number of the SIS card used to authenticate the person.""")

    id_card_no = models.CharField(verbose_name=_('ID card number'),
        max_length=20,
        blank=True, help_text="""\
The number of the ID card used to authenticate the person.""")

    first_name = models.CharField(max_length=200,
      blank=True,
      verbose_name=_('First name'))
    "Space-separated list of all first names."
    
    last_name = models.CharField(max_length=200,
      blank=True,
      verbose_name=_('Last name'))
    """Last name (family name)."""
    
    def get_ssin(self):
        national_id = self.national_id.replace('=','')
        national_id = national_id.replace(' ','')
        national_id = national_id.replace('-','')
        return national_id
        
    def save(self,*args,**kw):
        if self.person_id and not self.last_name: 
            self.fill_from_person(self.person)
        super(SSIN,self).save(*args,**kw)
        
    def on_create(self,ar):
        #~ print '20120527 SSIN.on_create', obj2str(self), ar
        #~ super(ContractBase,self).on_create(request)
        self.person_changed(ar)
        
    def person_changed(self,ar):
        #~ print '20120603 person_changed', obj2str(self)
        if self.person_id: 
            self.fill_from_person(self.person)
        
    def fill_from_person(self,person):
        self.national_id = person.national_id
        self.id_card_no = person.card_number
        self.last_name = person.last_name
        self.first_name = person.first_name
        self.birth_date = person.birth_date
        #~ print '20120603 fill_from_person', self.national_id
                
        
class IdentifyPersonRequest(SSDNRequest,SSIN):
    """
    A request to the IdentifyPerson service.
    
    """
    
    ssdn_service_id = 'OCMWCPASIdentifyPerson'
    ssdn_service_version = '20050930'
    xsd_filename = xsdpath('SSDN','OCMW_CPAS',
        'IDENTIFYPERSON','IDENTIFYPERSONREQUEST.XSD')
    
    #~ cbss_namespace = cbss.IPR # IdentifyPersonRequest
    
    class Meta:
        verbose_name = _("IdentifyPerson Request")
        verbose_name_plural = _("IdentifyPerson Requests")
        
    #~ first_name = models.CharField(max_length=200,
      #~ blank=True,
      #~ verbose_name=_('First name'))
    #~ "Space-separated list of all first names."
    
    #~ last_name = models.CharField(max_length=200,
      #~ blank=True,
      #~ verbose_name=_('Last name'))
    #~ """Last name (family name)."""

    middle_name = models.CharField(max_length=200,
      blank=True,
      verbose_name=_('Middle name'),
      help_text="Whatever this means...")
      
    gender = Gender.field()
        
    tolerance = models.IntegerField(verbose_name=_('Tolerance'),
      default=0,
      help_text=u"""
      Falls Monat oder Tag des Geburtsdatums unbekannt sind, 
      um wieviel Monate bzw. Tage die Suche nach unten/oben ausgeweitet wird.
      Gültige Werte: 0 bis 10.
      """)
      # 20120606 gridcolumn doesn't like tooltips containing HTML
      #~ <p>Zum Beispiel 
      #~ <table border=1 class="htmlText">
      #~ <tr>
        #~ <td>Geburtsdatum</td>
        #~ <td colspan="3">Toleranz</td>
      #~ </tr><tr>
        #~ <td></td>
        #~ <td>0</td>
        #~ <td>1</td>
        #~ <td>10</td>
      #~ </tr><tr>
        #~ <td> 1968-00-00  </td>
        #~ <td> im Jahr 1968 </td>
        #~ <td> von 1967 bis 1969 </td>
        #~ <td> 1958 bis 1978 </td>
      #~ </tr><tr>
        #~ <td> 1968-06-00  </td>
        #~ <td> im Juni 1968 </td>
        #~ <td> von Mai  bis Juli 1968 </td>
        #~ <td>von Oktober 1967 bis April 1969</td>
      #~ </tr>
      #~ </table>
      #~ </p>
      
      
        
    def on_create(self,ar):
        mixins.AutoUser.on_create(self,ar)
        SSIN.on_create(self,ar)

    def get_result_table(self,ar):
        return ar.spawn(IdentifyPersonResult,master_instance=self)
        
    def fill_from_person(self,person):
        super(IdentifyPersonRequest,self).fill_from_person(person)
        self.gender = person.gender
        
    def build_request(self):
        """Construct and return the root element of the (inner) service request."""
        if not self.birth_date:
            raise Exception("Empty birth date (a full_clean() would have told that, too!)")
        
        national_id = self.get_ssin()
        gender = gender2cbss(self.gender)
        #~ https://fedorahosted.org/suds/wiki/TipsAndTricks#IncludingLiteralXML
        main = E('ipr:IdentifyPersonRequest',ns=NSIPR)
        sc = E('ipr:SearchCriteria') 
        main.append(sc)
        if national_id:
            # VerificatioinData is ignored if there's no SSIN in the SearchCriteria
            sc.append(E('ipr:SSIN').setText(national_id))
            
            vd = E('ipr:VerificationData')
            main.append(vd)
            if self.sis_card_no:
                vd.append(E('ipr:SISCardNumber').setText(self.sis_card_no))
            if self.id_card_no:
                vd.append(E('ipr:IdentityCardNumber').setText(self.id_card_no))
            
            pd = E('ipr:PersonData')
            vd.append(pd)
            #~ if not self.last_name or not self.first_name:
                #~ raise Warning("Fields last_name and first_name are mandatory.")
            pd.append(E('ipr:LastName').setText(self.last_name))
            pd.append(E('ipr:FirstName').setText(self.first_name))
            pd.append(E('ipr:MiddleName').setText(self.middle_name))
            pd.append(E('ipr:BirthDate').setText(str(self.birth_date)))
            #~ if not self.birth_date.is_complete():
                #~ pd.append(E('ipr:Tolerance').setText(self.tolerance))
            #~ if gender is not None: pd.append(E('ipr:Gender').setText(gender))
        pc = E('ipr:PhoneticCriteria') 
        sc.append(pc)
        pc.append(E('ipr:LastName').setText(self.last_name))
        pc.append(E('ipr:FirstName').setText(self.first_name))
        pc.append(E('ipr:MiddleName').setText(self.middle_name))
        pc.append(E('ipr:BirthDate').setText(str(self.birth_date)))
        return main
        
    def get_service_reply(self,full_reply=None):
        if full_reply is not None:
            return full_reply.childAtPath('/ServiceReply/IdentifyPersonReply')
        return PARSER.parse(string=self.response_xml.encode('utf-8')).root()
        #~ return reply
           
        #~ if False:
          
            #~ try:
                #~ res = self.cbss_namespace.execute(srvreq,str(self.id),now)
            #~ except cbss.Warning,e:
                #~ self.status = RequestStatus.exception
                #~ self.response_xml = unicode(e)
                #~ self.save()
                #~ return
            #~ except Exception,e:
                #~ self.status = RequestStatus.exception
                #~ self.response_xml = traceback.format_exc(e)
                #~ self.save()
                #~ return
            #~ self.sent = now
            #~ self.response_xml = res.data.xmlString
            #~ reply = cbss.xml2reply(res.data.xmlString)
            #~ rc = reply.ServiceReply.ResultSummary.ReturnCode
            #~ if rc == '0':
                #~ self.status = RequestStatus.ok
            #~ elif rc == '1':
                #~ self.status = RequestStatus.warnings
            #~ elif rc == '10000':
                #~ self.status = RequestStatus.errors
            #~ self.save()
            
            #~ if self.status != RequestStatus.ok:
                #~ msg = '\n'.join(list(cbss.reply2lines(reply)))
                #~ raise Exception(msg)
                
            #~ self.on_cbss_ok(reply)
        

#~ dd.update_field(IdentifyPersonRequest,'birth_date',blank=False,null=False)
#~ dd.update_field(IdentifyPersonRequest,'first_name',blank=True)
#~ dd.update_field(IdentifyPersonRequest,'last_name',blank=True)

    
    
class IdentifyPersonRequestDetail(CBSSRequestDetail):
    p1 = """
    national_id
    spacer
    """
    p2 = """
    first_name middle_name last_name
    birth_date tolerance  gender 
    """
    parameters = "p1 p2"
    
    result = "IdentifyPersonResult"
    
    def setup_handle(self,lh):
        lh.p1.label = _("Using the national ID")
        lh.p2.label = _("Using phonetic search")
        CBSSRequestDetail.setup_handle(self,lh)
    

class CBSSRequests(dd.Table):
  
    @classmethod
    def get_row_permission(cls,action,user,row):
        if row.ticket and not action.readonly: 
            return False
        if not super(CBSSRequests,cls).get_row_permission(action,user,row):
            return False
        return True
        
    
class IdentifyPersonRequests(CBSSRequests):
    #~ window_size = (500,400)
    required_user_groups = ['cbss']
    model = IdentifyPersonRequest
    active_fields = ['person']
    detail_layout = IdentifyPersonRequestDetail()
    #~ detail_template = """
    #~ id project 
    #~ national_id
    #~ first_name middle_name last_name
    #~ birth_date tolerance  gender 
    #~ sent status 
    #~ request_xml
    #~ response_xml
    #~ """
    
    @dd.constant()
    def spacer(self,ui):  return '<br/>'
    
class MyIdentifyPersonRequests(IdentifyPersonRequests,mixins.ByUser):
    pass
    
class IdentifyRequestsByPerson(IdentifyPersonRequests):
    master_key = 'person'
    column_names = 'user sent status'
    



class IdentifyPersonResult(dd.VirtualTable):
    """
    Displays the response of an :class:`IdentifyPersonRequest`
    as a table.
    """
    master = IdentifyPersonRequest
    master_key = None
    label = _("Results")
    column_names = 'national_id:10 last_name:20 first_name:10 address birth_date:10 birth_location civil_state *'
    
    @classmethod
    def get_data_rows(self,ar):
        ipr = ar.master_instance
        if ipr is None: 
            print "20120606 ipr is None"
            return
        #~ if not ipr.status in (RequestStatus.ok,RequestStatus.fictive):
        if not ipr.status in (RequestStatus.ok,RequestStatus.warnings):
            print "20120606 wrong status", ipr.status 
            return
        service_reply = ipr.get_service_reply()
        results = service_reply.childAtPath('/SearchResults').children
        print "20120606 got", service_reply
        if results is None:
            print "20120606 no /SearchResults"
            #~ return []
            return
        for obj in results:
            data = dict()
            data.update(national_id = nodetext(obj.childAtPath('/Basic/SocialSecurityUser')))
            data.update(last_name = nodetext(obj.childAtPath('/Basic/LastName')))
            data.update(first_name = nodetext(obj.childAtPath('/Basic/FirstName')))
            data.update(gender = cbss2gender(nodetext(obj.childAtPath('/Basic/Gender'))))
            data.update(birth_date = cbss2date(nodetext(obj.childAtPath('/Basic/BirthDate'))))
            data.update(civil_state = cbss2civilstate(
                obj.childAtPath('/Extended/CivilState')))
            data.update(birth_location=nodetext(obj.childAtPath('/Extended/BirthLocation')))
            data.update(cbss2address(obj))
            yield AttrDict(**data)
        #~ return results
        #~ if service_reply is not None:
            #~ results = service_reply.childAtPath('/SearchResults')
            #~ if results is not None:
            
    @dd.displayfield(_("National ID"))
    def national_id(self,obj,ar):
        #~ return obj.childAtPath('/Basic/SocialSecurityUser').text
        return obj.national_id
            
    @dd.displayfield(_("Last name"))
    def last_name(self,obj,ar):
        return obj.last_name
        #~ return obj.childAtPath('/Basic/LastName').text
        
    @dd.displayfield(_("First name"))
    def first_name(self,obj,ar):
        return obj.first_name
        #~ return obj.childAtPath('/Basic/FirstName').text
            
    @dd.virtualfield(Gender.field())
    def gender(self,obj,ar):
        return obj.gender
        #~ return cbss2gender(obj.childAtPath('/Basic/Gender').text)
            
    #~ @dd.displayfield(dd.IncompleteDateField(_("Birth date")))
    @dd.displayfield(_("Birth date"))
    def birth_date(self,obj,ar):
        return obj.birth_date
        #~ return obj.childAtPath('/Basic/BirthDate').text
        
    @dd.displayfield(_("Birth location"))
    def birth_location(self,obj,ar):
        return obj.birth_location
        
    @dd.displayfield(_("Civil state"))
    def civil_state(self,obj,ar):
        return obj.civil_state
        #~ return obj.childAtPath('/Extended/CivilState').text
        
    @dd.displayfield(_("Address"))
    def address(self,obj,ar):
        return obj.address
        
        
            
    #~ @dd.virtualfield(models.ForeignKey(settings.LINO.person_model))
    #~ @dd.displayfield(_("Person"))
    #~ def person(self,obj,ar):
        #~ from lino.apps.pcsw.models import Person
        #~ niss = obj.childAtPath('/Basic/SocialSecurityUser').text
        #~ if niss:
            #~ try:
                #~ return unicode(Person.objects.get(national_id=niss))
            #~ except Person.DoesNotExist:
                #~ pass
        #~ return ''
            






class ManageAction(ChoiceList):
    """
    Possible values for the 
    `action` field of a :class:`ManageAccessRequest`.
    """
    label = _("Action")

add = ManageAction.add_item
add('1',_("Register"),'REGISTER')
add('2',_("Unregister"),'UNREGISTER')
add('3',_("List"),'LIST')


class QueryRegister(ChoiceList):
    """
    Possible values for the 
    `query_register` field of a :class:`ManageAccessRequest`.
    
    """
    label = _("Query Register")

add = QueryRegister.add_item
add('1',_("Primary"),'PRIMARY')
add('2',_("Secondary"),'SECONDARY')
add('3',_("All"),'ALL')

class ManageAccessRequest(SSDNRequest,SSIN):
    """
    A request to the ManageAccess service.
    
    Registering a person means that this PCSW is 
    going to maintain a dossier about this person.
    Users commonly say "to integrate" a person.
    
    """
  
    ssdn_service_id = 'OCMWCPASManageAccess'
    ssdn_service_version = '20050930'
    
    xsd_filename = xsdpath('SSDN','OCMW_CPAS',
        'ManageAccess','ManageAccessRequest.xsd')
    
    class Meta:
        verbose_name = _("ManageAccess Request")
        verbose_name_plural = _("ManageAccess Requests")
        
    #~ purpose = models.IntegerField(verbose_name=_('Purpose'),
      #~ default=0,help_text="""\
#~ The purpose for which the inscription needs to be 
#~ registered/unregistered or listed. 
#~ For listing this field is optional, 
#~ for register/unregister it is obligated.""")

    #~ sector = models.IntegerField(verbose_name=_('Sector'),
      #~ blank=False,default=0,help_text="""\
#~ For register and unregister this element is ignored. 
#~ It can be used for list, 
#~ when information about sectors is required.""")

    sector = models.ForeignKey(Sector,
      blank=True, editable=False,
      help_text="""\
For register and unregister this element is ignored. 
It can be used for list, 
when information about sectors is required.""")

    purpose = models.ForeignKey(Purpose,
      blank=True,null=True,
      help_text="""\
The purpose for which the inscription needs to be 
registered/unregistered or listed. 
For listing this field is optional, 
for register/unregister it is mandatory.""")

    start_date = models.DateField(
        blank=True,null=True,
        verbose_name=_("Period from"))
    end_date = models.DateField(
        blank=True,null=True,
        verbose_name=_("Period until"))

    # 20120527 : Django converts default value to unicode. didnt yet understand why.
    action = ManageAction.field(blank=False,default=ManageAction.LIST)
    query_register = QueryRegister.field(blank=False,default=QueryRegister.ALL)
    #~ action = ManageAction.field(blank=False)
    #~ query_register = QueryRegister.field(blank=False) # ,default=QueryRegister.ALL)

    def save(self,*args,**kw):
        if not self.sector_id:
            self.sector = settings.LINO.site_config.sector
        super(ManageAccessRequest,self).save(*args,**kw)

    @chooser()
    def purpose_choices(cls,sector):
        if not sector:
            sector = settings.LINO.site_config.sector
        if not sector:
            raise Exception("SiteConfig.sector is not set!")
        Q = models.Q
        return Purpose.objects.filter(
            Q(sector_code=sector.code)|Q(sector_code__isnull=True)).order_by('code')


    def on_create(self,ar):
        #~ self.query_register = QueryRegister.ALL
        #~ self.action = ManageAction.LIST
        mixins.AutoUser.on_create(self,ar)
        SSIN.on_create(self,ar)

    def build_request(self):
        """Construct and return the root element of the (inner) service request."""
        national_id = self.get_ssin()
        main = E('mar:ManageAccessRequest',ns=NSMAR)
        main.append(E('mar:SSIN').setText(national_id))
        #~ main.append(E('mar:Purpose').setText(str(self.purpose)))
        if self.purpose_id:
            main.append(E('mar:Purpose').setText(str(self.purpose.code)))
        period = E('mar:Period')
        main.append(period)
        period.append(E('common:StartDate',ns=NSCOMMON).setText(str(self.start_date)))
        if self.end_date:
            period.append(E('common:EndDate',ns=NSCOMMON).setText(str(self.end_date)))
        main.append(E('mar:Action').setText(self.action.name))
        main.append(E('mar:Sector').setText(str(self.sector.code)))
        if self.query_register:
            main.append(E('mar:QueryRegister').setText(self.query_register.name))
        proof = E('mar:ProofOfAuthentication')
        main.append(proof)
        if self.sis_card_no:
            proof.append(E('mar:SISCardNumber').setText(self.sis_card_no))
        if self.id_card_no:
            proof.append(E('mar:IdentityCardNumber').setText(self.id_card_no))
        if self.last_name or self.first_name or self.birth_date:
            pd = E('mar:PersonData')
            proof.append(pd)
            pd.append(E('mar:LastName').setText(self.last_name))
            pd.append(E('mar:FirstName').setText(self.first_name))
            pd.append(E('mar:BirthDate').setText(self.birth_date))
        return main
    
    def get_service_reply(self,full_reply=None):
        """
        Extract the "service reply" part from a full reply.
        Example of a full reply::
        
         <ServiceReply>
            <ns2:ResultSummary xmlns:ns2="http://www.ksz-bcss.fgov.be/XSD/SSDN/Common" ok="YES">
               <ns2:ReturnCode>0</ns2:ReturnCode>
            </ns2:ResultSummary>
            <ServiceId>OCMWCPASManageAccess</ServiceId>
            <Version>20050930</Version>
            <ns3:ManageAccessReply xmlns:ns3="http://www.ksz-bcss.fgov.be/XSD/SSDN/OCMW_CPAS/ManageAccess">
               <ns3:OriginalRequest>
                  <ns3:SSIN>68060105329</ns3:SSIN>
                  <ns3:Purpose>1</ns3:Purpose>
                  <ns3:Period>
                     <ns4:StartDate xmlns:ns4="http://www.ksz-bcss.fgov.be/XSD/SSDN/Common">2012-05-24+02:00</ns4:StartDate>
                     <ns5:EndDate xmlns:ns5="http://www.ksz-bcss.fgov.be/XSD/SSDN/Common">2012-05-24+02:00</ns5:EndDate>
                  </ns3:Period>
                  <ns3:Action>REGISTER</ns3:Action>
               </ns3:OriginalRequest>
               <ns3:Registrations>
                  <ns3:Purpose>1</ns3:Purpose>
                  <ns3:Period>
                     <ns6:StartDate xmlns:ns6="http://www.ksz-bcss.fgov.be/XSD/SSDN/Common">2012-05-24+02:00</ns6:StartDate>
                     <ns7:EndDate xmlns:ns7="http://www.ksz-bcss.fgov.be/XSD/SSDN/Common">2012-05-24+02:00</ns7:EndDate>
                  </ns3:Period>
                  <ns3:OrgUnit>63023</ns3:OrgUnit>
                  <ns3:Register>SECONDARY</ns3:Register>
               </ns3:Registrations>
            </ns3:ManageAccessReply>
         </ServiceReply>        
        """
        if full_reply is not None:
            return full_reply.childAtPath('/ServiceReply/ManageAccessReply')
        return PARSER.parse(string=self.response_xml.encode('utf-8')).root()
        
        
    
dd.update_field(ManageAccessRequest,'national_id',help_text="""\
The SSIN of the person to register/unregister/list.
""")





class ManageAccessRequestDetail(CBSSRequestDetail):
    p1 = """
    action start_date end_date 
    purpose query_register
    """
    proof = """
    national_id sis_card_no id_card_no
    first_name last_name birth_date 
    """
    parameters = "p1 proof"
    
    #~ result = "result"
    
    def setup_handle(self,lh):
        lh.p1.label = _("Requested action")
        lh.proof.label = _("Proof of authentication")
        CBSSRequestDetail.setup_handle(self,lh)
    

class ManageAccessRequests(CBSSRequests):
    #~ window_size = (500,400)
    model = ManageAccessRequest
    detail_layout = ManageAccessRequestDetail()
    required_user_groups = ['cbss']
    active_fields = ['person']
    
    
class ManageAccessRequestsByPerson(ManageAccessRequests):
    master_key = 'person'


class MyManageAccessRequests(ManageAccessRequests,mixins.ByUser):
    pass


        
class RetrieveTIGroupsRequest(NewStyleRequest,SSIN):
    """
    A request to the RetrieveTIGroups service
    """
    
    class Meta:
        verbose_name = _("Tx25 Request")
        verbose_name_plural = _('Tx25 Requests')
        
    wsdl_parts = ('cache','wsdl','RetrieveTIGroupsV3.wsdl')
    
    language = babel.LanguageField()
    history = models.BooleanField(
        verbose_name=_("History"),default=False,
        help_text = "Whatever this means.")
    
        
    def execute_newstyle(self,client,infoCustomer):
        si = client.factory.create('ns0:SearchInformationType')
        si.ssin = self.get_ssin()
        if self.language:
            si.language = self.language
        #~ if self.history:
            #~ si.history = 'true'
        si.history = self.history
        #~ if validate:
            #~ self.validate_newstyle(srvreq)
        self.check_environment(si)
        try:
            reply = client.service.retrieveTI(infoCustomer,None,si)        
        except suds.WebFault,e:
            """
            Example of a SOAP fault:
      <soapenv:Fault>
         <faultcode>soapenv:Server</faultcode>
         <faultstring>An error occurred while servicing your request.</faultstring>
         <detail>
            <v1:retrieveTIGroupsFault>
               <informationCustomer xmlns:ns0="http://kszbcss.fgov.be/intf/RetrieveTIGroupsService/v1" xmlns:ns1="http://schemas.xmlsoap.org/soap/envelope/">
                  <ticket>2</ticket>
                  <timestampSent>2012-05-23T10:19:27.636628+01:00</timestampSent>
                  <customerIdentification>
                     <cbeNumber>0212344876</cbeNumber>
                  </customerIdentification>
               </informationCustomer>
               <informationCBSS>
                  <ticketCBSS>f4b9cabe-e457-4f6b-bfcc-00fe258a9b7f</ticketCBSS>
                  <timestampReceive>2012-05-23T08:19:09.029Z</timestampReceive>
                  <timestampReply>2012-05-23T08:19:09.325Z</timestampReply>
               </informationCBSS>
               <error>
                  <severity>FATAL</severity>
                  <reasonCode>MSG00003</reasonCode>
                  <diagnostic>Unexpected internal error occurred</diagnostic>
                  <authorCode>http://www.bcss.fgov.be/en/international/home/index.html</authorCode>
               </error>
            </v1:retrieveTIGroupsFault>
         </detail>
      </soapenv:Fault>
            """
            
            msg = CBSS_ERROR_MESSAGE % e.fault.faultstring
            msg += unicode(e.document)
            self.status = RequestStatus.failed
            raise Warning(msg)
            
        self.response_xml = unicode(reply)
        
        """
        Example of reply:
        (reply){
           informationCustomer =
              (InformationCustomerType){
                 ticket = "1"
                 timestampSent = 2012-05-23 09:24:55.316312
                 customerIdentification =
                    (CustomerIdentificationType){
                       cbeNumber = "0123456789"
                    }
              }
           informationCBSS =
              (InformationCBSSType){
                 ticketCBSS = "f11736b3-97bc-452a-a75c-16fcc2a2f6ae"
                 timestampReceive = 2012-05-23 08:24:37.000385
                 timestampReply = 2012-05-23 08:24:37.000516
              }
           status =
              (StatusType){
                 value = "NO_RESULT"
                 code = "MSG00008"
                 description = "A validation error occurred."
                 information[] =
                    (InformationType){
                       fieldName = "ssin"
                       fieldValue = "12345678901"
                    },
              }
           searchInformation =
              (SearchInformationType){
                 ssin = "12345678901"
                 language = "de"
                 history = False
              }
         }        
        """
        self.ticket = reply.informationCBSS.ticketCBSS
        if reply.status.value == "NO_RESULT":
            msg = CBSS_ERROR_MESSAGE % reply.status.code
            keys = ('value','code','description')
            msg += '\n'.join([
                k+' : '+getattr(reply.status,k)
                    for k in keys])
            for i in reply.status.information:
                msg += "\n- %s = %s" % (i.fieldName,i.fieldValue)
            self.status = RequestStatus.warnings
            raise Warning(msg)
            
        self.status = RequestStatus.ok
        #~ self.response_xml = str(res)
        #~ self.response_xml = "20120522 %s %s" % (res.__class__,res)
        #~ print 20120523, res.informationCustomer
        #~ print self.response_xml
        return reply
        

  
class RetrieveTIGroupsRequestDetail(CBSSRequestDetail):
  
    parameters = "national_id language history"
    
    #~ result = "cbss.RetrieveTIGroupsResult"
    
    #~ def setup_handle(self,lh):
        #~ CBSSRequestDetail.setup_handle(self,lh)

class RetrieveTIGroupsRequests(CBSSRequests):
    model = RetrieveTIGroupsRequest
    detail_layout = RetrieveTIGroupsRequestDetail()
    required_user_groups = ['cbss']
        
    #~ @dd.virtualfield(dd.HtmlBox())
    #~ def result(self,row,ar):
        #~ return row.response_xml
        
class RetrieveTIGroupsRequestsByPerson(RetrieveTIGroupsRequests):
    master_key = 'person'
    
class MyRetrieveTIGroupsRequests(RetrieveTIGroupsRequests,mixins.ByUser):
    pass

    
#~ class RetrieveTIGroupsResult(dd.EmptyTable):
    #~ master = RetrieveTIGroupsRequest
    #~ master_key = None
    
    #~ detail_template = """
    #~ body
    #~ """

from lino.models import SiteConfig
dd.inject_field(SiteConfig,
    'sector',
    models.ForeignKey(Sector,
        blank=True,null=True,
        help_text="""\
The CBSS sector/subsector of the requesting organization.        
For PCSWs this is always 17.1.
Used in SSDN requests as text of the `MatrixID` and `MatrixSubID` 
elements of `AuthorizedUser`. 
Used in ManageAccess requests as default value 
for the non-editable field `sector` 
(which defines the choices of the `purpose` field).
"""))
    
dd.inject_field(SiteConfig,
    'cbss_org_unit',
    models.CharField(_("Requesting organisation"),
      max_length=50,
      blank=True,
      help_text="""\
In CBSS requests, identifies the requesting organization.
For PCSWs this is the enterprise number 
(CBE, KBO) and should have 10 digits and no formatting characters.

Used in SSDN requests as text of the `AuthorizedUser\OrgUnit` element . 
Used in new style requests as text of the `CustomerIdentification\cbeNumber` element . 
"""))
dd.inject_field(SiteConfig,
    'ssdn_user_id',
    models.CharField(_("SSDN User Id"),
      max_length=50,
      blank=True,
      help_text="""\
Used in SSDN requests as text of the `AuthorizedUser\UserID` element.
"""))
dd.inject_field(SiteConfig,
    'ssdn_email',
    models.EmailField(_("SSDN email address"),
      blank=True,
      help_text="""\
Used in SSDN requests as text of the `AuthorizedUser\Email` element.
"""))
dd.inject_field(SiteConfig,
    'cbss_http_username',
    models.CharField(_("HTTP username"),
      max_length=50,
      blank=True,
      help_text="""\
Used in the http header of new-style requests.
"""))
dd.inject_field(SiteConfig,
    'cbss_http_password',
    models.CharField(_("HTTP password"),
      max_length=50,
      blank=True,
      help_text="""\
Used in the http header of new-style requests.
"""))


    
    
dd.inject_quick_add_buttons(
    pcsw.Person,'cbss_identify_person',IdentifyRequestsByPerson)
dd.inject_quick_add_buttons(
    pcsw.Person,'cbss_manage_access',ManageAccessRequestsByPerson)
dd.inject_quick_add_buttons(
    pcsw.Person,'cbss_retrieve_ti_groups',RetrieveTIGroupsRequestsByPerson)

def cbss_summary(self,ar):
    """
    returns a summary overview of the CBSS requests for this person.
    """
    #~ qs = IdentifyPersonRequest.objects.filter(person=self,status=RequestStatus.ok)
    html = '<p><ul>'
    for m in (IdentifyPersonRequest,ManageAccessRequest,RetrieveTIGroupsRequest):
        n = m.objects.filter(person=self).count()
        if n > 0:
            html += "<li>%d %s</li>" % (n,unicode(m._meta.verbose_name_plural))
    html += '</ul></p>'
    return html
    
dd.inject_field(pcsw.Person,
    'cbss_summary',
    dd.VirtualField(dd.HtmlBox(_("CBSS summary")),cbss_summary))
    

MODULE_NAME = _("CBSS")

settings.LINO.add_user_field('cbss_level',UserLevel.field(MODULE_NAME))

dd.inject_field('countries.City',
    'inscode',
    models.CharField(
        max_length=5,
        verbose_name=_("INS code"),
        blank=True,
    ))
        
dd.inject_field('countries.Country',
    'inscode',
    models.CharField(
        max_length=3,
        verbose_name=_("INS code"),
        blank=True,
    ))
        


def setup_site_cache(self,force):
    """
    Called from :meth:`build_site_cache`. 
    First argument is the LINO instance."""
    
    import logging
    logger = logging.getLogger(__name__)
    
    environment = settings.LINO.cbss_environment
    if not environment:
        return # silently return
        
    if not environment in CBSS_ENVS:
        raise Exception("Invalid `cbss_environment` %r: must be empty or one of %s." % (
          environment,CBSS_ENVS))
    
    context = dict(cbss_environment=environment)
    def make_wsdl(template,parts):
        fn = os.path.join(settings.MEDIA_ROOT,*parts) 
        if not force and os.path.exists(fn):
            if os.stat(fn).st_mtime > self.mtime:
                logger.info("NOT generating %s because it is newer than the code.",fn)
                return
        s = file(os.path.join(os.path.dirname(__file__),'WSDL',template)).read()
        s = s % context
        makedirs_if_missing(os.path.dirname(fn))
        open(fn,'wt').write(s)
        logger.info("Generated %s for environment %r.",fn,environment)
        
    make_wsdl('RetrieveTIGroupsV3.wsdl',RetrieveTIGroupsRequest.wsdl_parts)
    make_wsdl('WebServiceConnector.wsdl',SSDNRequest.wsdl_parts)
    #~ make_wsdl('TestConnectionService.wsdl',TestConnectionRequest.wsdl_parts)
    
    # The following xsd files are needed, unmodified but in the same directory
    #~ for fn in 'RetrieveTIGroupsV3.xsd', 'rn25_Release201104.xsd', 'TestConnectionServiceV1.xsd':
    for fn in 'RetrieveTIGroupsV3.xsd', 'rn25_Release201104.xsd':
        src = os.path.join(os.path.dirname(__file__),'XSD',fn)
        target = os.path.join(settings.MEDIA_ROOT,'cache','wsdl',fn) 
        if not os.path.exists(target):
            shutil.copy(src,target)
            
    
def site_setup(self):
    """
    (Called during site setup.)
    
    Adds a new tab "CBSS" to the Detail of `contacts.Persons`.
    """
    self.modules.contacts.AllPersons.add_detail_tab('cbss',"""
    cbss_identify_person cbss_manage_access  cbss_retrieve_ti_groups
    cbss_summary
    """,MODULE_NAME,required_user_groups=['cbss'])
    #~ cbss.IdentifyRequestsByPerson
    #~ self.modules.contacts.AllPersons.add_detail_panel('cbssrequests',"""
    #~ cbss_identify_person 
    #~ cbss_manage_access 
    #~ cbss_retrieve_ti_groups
    #~ """,_("CBSS Requests"))
    #~ self.modules.contacts.AllPersons.add_detail_tab('cbss',"cbssrequests",MODULE_NAME,required_user_groups=['cbss'])
    #~ 
    
    self.modules.lino.SiteConfigs.add_detail_tab('cbss',"""
    cbss_org_unit sector ssdn_user_id ssdn_email
    cbss_http_username cbss_http_password
    """,MODULE_NAME,required_user_groups=['cbss'])
    
    
    
def setup_main_menu(site,ui,user,m): pass
def setup_master_menu(site,ui,user,m): pass
  
def setup_my_menu(site,ui,user,m): 
    if user.cbss_level < UserLevel.user: 
        return
    m  = m.add_menu("cbss",MODULE_NAME)
    m.add_action(MyIdentifyPersonRequests)
    m.add_action(MyManageAccessRequests)
    m.add_action(MyRetrieveTIGroupsRequests)
    
def setup_config_menu(site,ui,user,m):
    m  = m.add_menu("cbss",MODULE_NAME)
    m.add_action(Sectors)
    m.add_action(Purposes)
  
def setup_explorer_menu(site,ui,user,m):
    if user.cbss_level < UserLevel.manager: 
        return
    m  = m.add_menu("cbss",MODULE_NAME)
    m.add_action(IdentifyPersonRequests)
    m.add_action(ManageAccessRequests)
    m.add_action(RetrieveTIGroupsRequests)
    