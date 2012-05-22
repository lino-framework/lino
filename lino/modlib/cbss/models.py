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

"""
Adds models and tables used to make :term:`CBSS` requests.

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

from lino.utils import babel
from lino.utils import dblogger
#~ from lino.tools import resolve_model
#~ from lino.utils.xmlgen import etree
#~ from lino.utils.xmlgen import cbss


from lino.utils.choicelists import ChoiceList
from lino.utils.choicelists import Gender
from lino.modlib.contacts import models as contacts
from lino.tools import makedirs_if_missing

try:
  
    from suds.client import Client
    from suds.transport.http import HttpAuthenticated
    from suds.transport.http import HttpTransport
    from suds.sax.element import Element as E
    from suds.sax.parser import Parser
    PARSER = Parser()

except ImportError, e:
    pass


CBSS_ENVS = ('test', 'acpt', 'prod')

def xsdpath(*parts):
    p1 = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(p1,'XSD',*parts)




class RequestStatus(ChoiceList):
    """
    The status of a :class:`CBSSRequest`.
    """
    label = _("Status")

add = RequestStatus.add_item
add('0',_("New"),alias='new')
add('1',_("Pending"),alias='pending')
add('2',_("Exception"),alias='exception')
add('3',_("OK"),alias='ok')
add('4',_("Warnings"),alias='warnings')
add('5',_("Errors"),alias='errors')
#~ add('6',_("Invalid reply"),alias='invalid')
add('9',_("Fictive"),alias='fictive')
  
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
    name = 'sendcbss'
    label = _('Execute')
    #~ callable_from = None
    callable_from = (dd.GridEdit,dd.ShowDetailAction)
    
    def disabled_for(self,obj,request):
        if obj.sent:
            return True
    
    def run(self,rr,elem,**kw):
        elem.execute_request(rr)
        if elem.status == RequestStatus.warnings:
            kw.update(message=_("There were warnings but no errors."))
            kw.update(alert=True)
        kw.update(refresh=True)
        return rr.ui.success_response(**kw)

NSCOMMON = ('common','http://www.ksz-bcss.fgov.be/XSD/SSDN/Common')
NSSSDN = ('ssdn','http://www.ksz-bcss.fgov.be/XSD/SSDN/Service')
NSIPR = ('ipr',"http://www.ksz-bcss.fgov.be/XSD/SSDN/OCMW_CPAS/IdentifyPerson")
NSMAR = ('mar',"http://www.ksz-bcss.fgov.be/XSD/SSDN/OCMW_CPAS/ManageAccess")
NSWSC = ('wsc',"http://ksz-bcss.fgov.be/connectors/WebServiceConnector")


class CBSSRequest(mixins.ProjectRelated,mixins.AutoUser):
    """
    Common Abstract Base Class for :class:`SSDNRequest`
    and :class:`NewStyleRequest`
    """
    
    wsdl_parts = NotImplementedError
    
    class Meta:
        abstract = True
        
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
    ticket  = models.CharField(max_length=20,editable=False,verbose_name=_("Ticket"))
    #~ environment = Environment.field(blank=True,null=True)
    
    # will probably go away soon
    request_xml = models.TextField(verbose_name=_("Request"),
        editable=False,blank=True,
        help_text="""The raw XML string that has been (or will be) sent.""")
    
    response_xml = models.TextField(
        verbose_name=_("Response"),
        editable=False,blank=True,
        help_text="""\
The response received, raw XML string. 
If the request failed with a local exception, then it contains a traceback.""")
    
    #~ def save(self,*args,**kw):
        #~ if not self.environment:
            #~ self.environment = settings.LINO.cbss_environment or ''
        #~ super(CBSSRequest,self).save(*args,**kw)

    def on_cbss_ok(self,reply):
        """
        Called when a successful reply has been received.
        """
        pass
        
    @classmethod
    def setup_report(cls,rpt):
        #~ call_optional_super(CBSSRequest,cls,'setup_report',rpt)
        rpt.add_action(SendAction())
        
    def get_permission(self,action,user):
        if isinstance(action,SendAction):
            if self.ticket:
                return False
        return super(CBSSRequest,self).get_permission(action,user)
      
    def __unicode__(self):
        return u"%s#%s" % (self.__class__.__name__,self.pk)
        

    def execute_request(self,ar,validate=True):
        raise NotImplementedError()

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



class CBSSRequestDetail(dd.DetailLayout):
    main = 'request response'
    
    request = """
    info
    parameters
    result
    """
    
    info = """
    id project user environment sent status ticket
    """
    
    response = "response_xml"
    
    def setup_handle(self,lh):
        lh.request.label = _("Request")
        lh.info.label = _("Request information")
        lh.result.label = _("Result")
        lh.response.label = _("Response")
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
        from lxml import etree
        xml = unicode(srvreq)
        #~ print xml
        doc = etree.fromstring(xml)
        schema_doc = etree.parse(xsd_filename)
        schema = etree.XMLSchema(schema_doc)
        #~ if not schema.validate(doc):
            #~ print xml
        schema.assertValid(doc)
        logger.debug("Validated %s against %s", xml,xsd_filename)
      
    def validate_wrapped(self,srvreq):
        self.validate_against_xsd(srvreq,xsdpath('SSDN','Service','SSDNRequest.xsd'))
        
        
    def validate_inner(self,srvreq):
        if not self.xsd_filename: return
        self.validate_against_xsd(srvreq,self.xsd_filename)
        
    
    def execute_request(self,ar,validate=False,now=None):
        """
        This is the general method for all SSDN services,
        executed when a user runs :class:`SendAction`.
        """
        if self.ticket:
            raise Warning(unicode(_("Cannot re-execute request.")))

        self.environment = settings.LINO.cbss_environment or ''
        self.status = RequestStatus.pending
        #~ if not self.id:
        self.save()
        #~ kw = self.get_request_params()
        if now is None:
            now = datetime.datetime.now()
        try:
            #~ srvreq = self.cbss_namespace('ns1').build_request(**kw)
            #~ srvreq = self.cbss_namespace.build_request(**kw)
            srvreq = self.build_request()
            if validate:
                self.validate_inner(srvreq)
            wrapped_srvreq = self.wrap_ssdn_request(srvreq,now)
            if validate:
                self.validate_wrapped(wrapped_srvreq)
                #~ logger.info("XSD validation passed.")
            self.check_environment(srvreq)
        except Warning,e:
            self.status = RequestStatus.exception
            self.response_xml = unicode(e)
            self.save()
            return
        
        url = self.get_wsdl_uri()
        
        #~ url = os.path.join(settings.MEDIA_ROOT,*WSC_PARTS) 
        
        #~ logger.info("Instantiate Client at %s", url)
        t = HttpTransport()
        client = Client(url, transport=t)
        #~ client.add_prefix(*NSCOMMON)
        #~ client.add_prefix(*NSSSDN)
        #~ client.add_prefix(*NSIPR)
        #~ client.add_prefix(*NSMAR)
        #~ client.add_prefix(*NSWSC)
        #~ client = Client(url)
        #~ print 20120507, client
        
        self.sent = now
        
        try:
            #~ res = client.service.sendXML(request_xml)        
            #~ xmlString = client.factory.create('wsc:xmlString')
            s = unicode(wrapped_srvreq)
            self.request_xml = s
            xmlString = E('wsc:xmlString',ns=NSWSC)
            xmlString.setText(s)
            #~ logger.info("20120521 Gonna sendXML(<xmlString>):\n%s",s)
            if not settings.LINO.cbss_live_tests:
                #~ raise Warning("NOT sending because `cbss_live_tests` is False:\n" + unicode(xmlString))
                raise Warning("NOT sending because `cbss_live_tests` is False:\n" + s)
            #~ xmlString.append(wrapped_srvreq)
            res = client.service.sendXML(xmlString)
            #~ res = client.service.sendXML(wrapped_srvreq)
            service_reply = self.fill_from_string(res.encode('utf-8'))
            self.save()
            return service_reply
        except (IOError,Warning),e:
            self.status = RequestStatus.exception
            self.response_xml = unicode(e)
            self.save()
            return
        except Exception,e:
            self.status = RequestStatus.exception
            self.response_xml = traceback.format_exc(e)
            self.save()
            return
        
    def fill_from_string(self,s):
        """Also used by demo fixture to create fictive requests.
        """
        #~ self.response_xml = unicode(res)
        reply = PARSER.parse(string=s).root()
        self.ticket = reply.childAtPath('/ReplyContext/Message/Ticket').text
        rs = reply.childAtPath('/ServiceReply/ResultSummary')
        rc = rs.childAtPath('/ReturnCode').text
        #~ print reply.__class__, dir(reply)
        #~ print reply
        #~ rc = reply.root().SSDNReply.ServiceReply.ResultSummary.ReturnCode
        if rc == '0':
            self.status = RequestStatus.ok
        elif rc == '1':
            self.status = RequestStatus.warnings
        #~ elif rc == '10000':
            #~ self.status = RequestStatus.errors
        else:
            #~ self.status = RequestStatus.errors
            #~ self.response_xml = unicode(reply)
            raise Warning(_("CBSS error %s:\n%s") % (
                rc,unicode(rs.childAtPath('/Detail'))))
            #~ return None
            #~ raise Exception("Got invalid response status")
            
        #~ self.on_cbss_ok(reply)
        service_reply = self.get_service_reply(reply)
        if service_reply is None:
            raise Exception(
              "Return code is %r but there's no service reply in:\n%s\n" % (rc,reply))
        #~ reply.childAtPath('/ServiceReply/IdentifyPersonReply')
        self.response_xml = unicode(service_reply)
        return service_reply
        
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
        
    def wrap_ssdn_request(self,srvreq,dt):
        #~ up  = settings.LINO.ssdn_user_params
        user_params = settings.LINO.cbss_user_params
        #~ au = E('common:AuthorizedUser',ns=NSCOMMON)
        #~ au.append(E('common:UserID').setText(up['UserID']))
        #~ au.append(E('common:Email').setText(up['Email']))
        #~ au.append(E('common:OrgUnit').setText(up['OrgUnit']))
        #~ au.append(E('common:MatrixID').setText(up['MatrixID']))
        #~ au.append(E('common:MatrixSubID').setText(up['MatrixSubID']))
        au = E('ssdn:AuthorizedUser')
        au.append(E('ssdn:UserID').setText(user_params['UserID']))
        au.append(E('ssdn:Email').setText(user_params['Email']))
        au.append(E('ssdn:OrgUnit').setText(user_params['OrgUnit']))
        au.append(E('ssdn:MatrixID').setText(user_params['MatrixID']))
        au.append(E('ssdn:MatrixSubID').setText(user_params['MatrixSubID']))
        
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
      
class SSIN(models.Model):
    class Meta:
        abstract = True
  
    national_id = models.CharField(max_length=200,
        blank=True,verbose_name=_("National ID")
        #~ ,validators=[niss_validator]
        )
        
    def get_ssin(self):
        national_id = self.national_id.replace('=','')
        national_id = national_id.replace(' ','')
        national_id = national_id.replace('-','')
        return national_id
        
        
class IdentifyPersonRequest(SSDNRequest,SSIN,contacts.PersonMixin,contacts.Born):
    """
    Represents a request to the IdentifyPerson service.
    
    """
    
    ssdn_service_id = 'OCMWCPASIdentifyPerson'
    ssdn_service_version = '20050930'
    xsd_filename = xsdpath('SSDN','OCMW_CPAS',
        'IDENTIFYPERSON','IDENTIFYPERSONREQUEST.XSD')
    
    #~ cbss_namespace = cbss.IPR # IdentifyPersonRequest
    
    class Meta:
        verbose_name = _("IdentifyPerson Request")
        verbose_name_plural = _("IdentifyPerson Requests")
        
    middle_name = models.CharField(max_length=200,
      blank=True,
      verbose_name=_('Middle name'),
      help_text="Whatever this means...")
    tolerance = models.IntegerField(verbose_name=_('Tolerance'),
      default=0,
      help_text=u"""
      Falls Monat oder Tag des Geburtsdatums unbekannt sind, 
      um wieviel Einheiten die Suche nach unten/oben ausgeweitet wird.
      Gültige Werte: 0 bis 10.
      <p>Zum Beispiel 
      <table border=1 class="htmlText">
      <tr>
        <td>Geburtsdatum<td/>
        <td colspan="3">Toleranz<td/>
      </tr><tr>
        <td><td/>
        <td>0<td/>
        <td>1</td>
        <td>10</td>
      </tr><tr>
        <td> 1968-00-00  <td/>
        <td> im Jahr 1968 <td/>
        <td> von 1967 bis 1969 </td>
        <td> 1958 bis 1978 <td/>
      </tr><tr>
        <td> 1968-06-00  <td/>
        <td> im Juni 1968 <td/>
        <td> von Mai  bis Juli 1968 </td>
        <td>von Oktober 1967 bis April 1969</td>
      </tr>
      </table>
      </p>
      """)
      
    def save(self,*args,**kw):
        if self.project: 
            person = self.project
            if person.national_id and not self.national_id:
                self.national_id = person.national_id
            if not self.last_name:
                self.last_name = person.last_name
            if not self.first_name:
                self.first_name = person.first_name
                
        super(IdentifyPersonRequest,self).save(*args,**kw)
        
    def build_request(self):
        """

        """
        national_id = self.get_ssin()
        last_name=self.last_name
        first_name=self.first_name
        middle_name=self.middle_name
        #~ if self.birth_date is not None:
            #~ birth_date=str(self.birth_date)
        birth_date=self.birth_date
        tolerance=self.tolerance
        if self.gender == Gender.male:
            gender = 1
        elif self.gender == Gender.female:
            gender = 2
        else:
            gender = 0
            
        #~ https://fedorahosted.org/suds/wiki/TipsAndTricks#IncludingLiteralXML
            
        main = E('ipr:IdentifyPersonRequest',ns=NSIPR)
        #~ main = E('ipr:IdentifyPersonRequest')
        sc = E('ipr:SearchCriteria') 
        main.append(sc)
        if national_id:
            sc.append(E('ipr:SSIN').setText(national_id))
            pd = E('ipr:PersonData')
            if last_name: pd.append(E('ipr:LastName').setText(last_name))
            if first_name: pd.append(E('ipr:FirstName').setText(first_name))
            if middle_name: pd.append(E('ipr:MiddleName').setText(middle_name))
            if birth_date: pd.append(E('ipr:BirthDate').setText(birth_date))
            if gender is not None: pd.append(E('ipr:Gender').setText(gender))
            if tolerance is not None: pd.append(E('ipr:Tolerance').setText(tolerance))
            
            #~ for k in ('LastName','FirstName','MiddleName','BirthDate'):
                #~ v = kw.get(k,None)
                #~ if v: # ignore empty values
                    #~ cl = getattr(ipr,k)
                    #~ pd.append(cl(v))
            main.append(E('ipr:VerificationData').append(pd))
        else:
            if self.birth_date is None:
                raise Warning(
                    "Either national_id or birth date must be given")
            pc = E('ipr:PhoneticCriteria') 
            pc.append(E('ipr:LastName').setText(last_name))
            pc.append(E('ipr:FirstName').setText(first_name))
            pc.append(E('ipr:MiddleName').setText(middle_name))
            pc.append(E('ipr:BirthDate').setText(str(birth_date)))
            #~ if gender is not None: pc.append(ipr.Gender(gender))
            #~ if tolerance is not None: pc.append(ipr.Tolerance(tolerance))
            sc.append(pc)
        return main
            
        
    def unused_get_request_params(self,**kw):
        """
        """
        national_id = self.national_id.replace('=','')
        national_id = national_id.replace(' ','')
        national_id = national_id.replace('-','')
        kw.update(national_id=national_id)
        kw.update(last_name=self.last_name)
        kw.update(first_name=self.first_name)
        kw.update(middle_name=self.middle_name)
        if self.birth_date is not None:
            kw.update(birth_date=str(self.birth_date))
        kw.update(tolerance=self.tolerance)
        if self.gender == Gender.male:
            kw.update(gender=1)
        elif self.gender == Gender.female:
            kw.update(gender=2)
        else:
            kw.update(gender=0)
        return kw
        
        #~ VD = cbss.ipr.VerificationData
        #~ SC = cbss.ipr.SearchCriteria
        #~ PC = cbss.ipr.PhoneticCriteria
        #~ if self.national_id:
            #~ return cbss.ipr.verify_request(
              #~ self.national_id,
              #~ LastName=self.last_name,
              #~ FirstName=self.first_name,
              #~ BirthDate=self.birth_date,
              #~ )
        #~ else:
          #~ pc = []
          #~ pc.append(cbss.ipr.LastName(self.last_name))
          #~ pc.append(cbss.ipr.FirstName(self.first_name))
          #~ pc.append(cbss.ipr.MiddleName(self.middle_name))
          #~ # if person.birth_date:
          #~ pc.append(cbss.ipr.BirthDate(self.birth_date))
          #~ if self.gender == Gender.male:
              #~ pc.append(cbss.ipr.Gender(1))
          #~ elif self.gender == Gender.female:
              #~ pc.append(cbss.ipr.Gender(2))
          #~ else:
              #~ pc.append(cbss.ipr.Gender(0))
          #~ pc.append(cbss.ipr.Tolerance(self.tolerance))
          #~ return cbss.ipr.IdentifyPersonRequest(SC(PC(*pc)))
    
dd.update_field(IdentifyPersonRequest,'first_name',blank=True)
dd.update_field(IdentifyPersonRequest,'last_name',blank=True)
#~ IdentifyPersonRequest._meta.get_field_by_name('first_name')[0].blank = True
#~ IdentifyPersonRequest._meta.get_field_by_name('last_name')[0].blank = True

    
    
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
    

class IdentifyPersonRequests(dd.Table):
    #~ window_size = (500,400)
    model = IdentifyPersonRequest
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
    
class IdentifyRequestsByPerson(IdentifyPersonRequests):
    master_key = 'project'
    


def gender(v):
    if v == '1':
        return Gender.male
    elif v == '2':
        return Gender.female
    return None
      

class IdentifyPersonResult(dd.VirtualTable):
    """
    Displays the response of an :class:`IdentifyPersonRequest`
    as a table.
    """
    master = IdentifyPersonRequest
    master_key = None
    label = _("Results")
    column_names = 'person national_id:10 last_name:20 first_name:10 birth_date:10 *'
    
    @classmethod
    def get_data_rows(self,ar):
        ipr = ar.master_instance
        if ipr is None: 
            return
        if not ipr.status in (RequestStatus.ok,RequestStatus.fictive):
            return
        service_reply = ipr.get_service_reply()
        return service_reply.childAtPath('/SearchResults')
        #~ if service_reply is not None:
            #~ results = service_reply.childAtPath('/SearchResults')
            #~ if results is not None:
                #~ for node in results:
                    #~ yield node
            
    @dd.displayfield(_("National ID"))
    def national_id(self,obj,ar):
        return obj.childAtPath('/Basic/SocialSecurityUser').text
            
    @dd.displayfield(_("Last Name"))
    def last_name(self,obj,ar):
        return obj.childAtPath('/Basic/LastName').text
        
    @dd.displayfield(_("First Name"))
    def first_name(self,obj,ar):
        return obj.childAtPath('/Basic/FirstName').text
            
    @dd.virtualfield(Gender.field())
    def gender(self,obj,ar):
        return gender(obj.childAtPath('/Basic/Gender').text)
            
    #~ @dd.displayfield(dd.IncompleteDateField(_("Birth date")))
    @dd.displayfield(_("Birth date"))
    def birth_date(self,obj,ar):
        return obj.childAtPath('/Basic/BirthDate').text
            
    #~ @dd.virtualfield(models.ForeignKey(settings.LINO.person_model))
    @dd.displayfield(_("Person"))
    def person(self,obj,ar):
        from lino.apps.pcsw.models import Person
        niss = obj.childAtPath('/Basic/SocialSecurityUser').text
        if niss:
            try:
                return unicode(Person.objects.get(national_id=niss))
            except Person.DoesNotExist:
                pass
        return None
            
      
          
        
class NewStyleRequest(CBSSRequest):
    """
    Abstract Base Class for Models that represent 
    "new style" requests to the :term:`CBSS` (and responses).
    """
    
    class Meta:
        abstract = True
        
    def execute_request(self,ar,validate=False):
        """
        This is the general method for all services,
        executed when a user runs :class:`SendAction`.
        """
        
        now = datetime.datetime.now()
        
        self.environment = settings.LINO.cbss_environment or ''
        self.status = RequestStatus.pending
        self.save()
        
        url = self.get_wsdl_uri()
        
        #~ logger.info("Instantiate Client at %s", url)
        t = HttpAuthenticated(
            username=settings.LINO.cbss_username, 
            password=settings.LINO.cbss_password)
        client = Client(url, transport=t)
        #print client

        ci = client.factory.create('ns0:CustomerIdentificationType')
        #~ cbeNumber = client.factory.create('ns0:CbeNumberType')
        ci.cbeNumber = settings.LINO.cbss_cbe_number
        info = client.factory.create('ns0:InformationCustomerType')
        info.ticket = str(self.id)
        info.timestampSent = now
        info.customerIdentification = ci
        

        try:
            res = self.execute_newstyle(client,info,validate)
        except (IOError,Warning),e:
        #~ except Warning,e:
            self.status = RequestStatus.exception
            self.response_xml = unicode(e)
            self.save()
            return
        except Exception,e:
            self.status = RequestStatus.exception
            self.response_xml = traceback.format_exc(e)
            self.save()
            return
        self.sent = now
        self.response_xml = unicode(res)
        
        if False:
            reply = cbss.xml2reply(res.data.xmlString)
            rc = reply.ServiceReply.ResultSummary.ReturnCode
            if rc == '0':
                self.status = RequestStatus.ok
            elif rc == '1':
                self.status = RequestStatus.warnings
            elif rc == '10000':
                self.status = RequestStatus.errors
            self.save()
            
            if self.status != RequestStatus.ok:
                msg = '\n'.join(list(cbss.reply2lines(reply)))
                raise Exception(msg)
            
        self.on_cbss_ok(reply)
        
    def on_cbss_ok(self,reply):
        """
        Called when a successful reply has been received.
        """
        pass
        
    @classmethod
    def setup_report(cls,rpt):
        #~ call_optional_super(CBSSRequest,cls,'setup_report',rpt)
        rpt.add_action(SendAction())
        
    def __unicode__(self):
        return u"%s#%s" % (self.__class__.__name__,self.pk)
        
    def execute_newstyle(self,client,infoCustomer,validate):
        raise NotImplementedError()
        
class RetrieveTIGroupsRequest(NewStyleRequest,SSIN):
    """
    A request to the RetrieveTIGroups service
    """
    
    wsdl_parts = ('cache','wsdl','RetrieveTIGroupsV3.wsdl')
    
    language = babel.LanguageField()
    history = models.BooleanField(
        verbose_name=_("History"),default=False,
        help_text = "Whatever this means.")
    
        
    def execute_newstyle(self,client,infoCustomer,validate):
        si = client.factory.create('ns0:SearchInformationType')
        si.ssin = self.get_ssin()
        si.language = self.language
        si.history = self.history
        #~ if validate:
            #~ self.validate_newstyle(srvreq)
        self.check_environment(si)
        return client.service.retrieveTI(infoCustomer,None,si)        

  
class RetrieveTIGroupsRequestDetail(CBSSRequestDetail):
  
    parameters = "national_id language history"
    
    #~ result = "cbss.RetrieveTIGroupsResult"
    
    #~ def setup_handle(self,lh):
        #~ CBSSRequestDetail.setup_handle(self,lh)

class RetrieveTIGroupsRequests(dd.Table):
    model = RetrieveTIGroupsRequest
    detail_layout = RetrieveTIGroupsRequestDetail()
        
    @dd.virtualfield(dd.HtmlBox())
    def result(self,row,ar):
        return row.response_xml
        
class RetrieveTIGroupsRequestsByPerson(RetrieveTIGroupsRequests):
    master_key = 'project'
    
#~ class RetrieveTIGroupsResult(dd.EmptyTable):
    #~ master = RetrieveTIGroupsRequest
    #~ master_key = None
    
    #~ detail_template = """
    #~ body
    #~ """
    
    
    


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
    self.modules.contacts.AllPersons.add_detail_tab('cbss',"""
    cbss_identify_person cbss_retrieve_ti_groups
    cbss.IdentifyRequestsByPerson
    """,_("CBSS"))
    
    
def setup_main_menu(site,ui,user,m): pass
def setup_master_menu(site,ui,user,m): pass
def setup_my_menu(site,ui,user,m): pass
def setup_config_menu(site,ui,user,m): pass
  
def setup_explorer_menu(site,ui,user,m):
    m  = m.add_menu("cbss",_("CBSS"))
    m.add_action(IdentifyPersonRequests)
    m.add_action(RetrieveTIGroupsRequests)
    