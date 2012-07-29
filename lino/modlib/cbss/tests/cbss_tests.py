# -*- coding: utf-8 -*-
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
This module contains "quick" tests that are run on a demo database 
without any fixture. You can run only these tests by issuing::

  python manage.py test cbss.QuickTest

  
"""
import datetime
import logging
logger = logging.getLogger(__name__)

#~ from django.utils import unittest
#~ from django.test.client import Client
from django.conf import settings
from django.core.exceptions import ValidationError

#from lino.igen import models
#from lino.modlib.contacts.models import Contact, Companies
#from lino.modlib.countries.models import Country
#~ from lino.modlib.contacts.models import Companies


from lino.utils import i2d
from lino.utils import babel
from lino.core.modeltools import resolve_model
#Companies = resolve_model('contacts.Companies')
from lino.utils.test import TestCase
from lino.utils import Warning


#~ Person = resolve_model('contacts.Person')
#~ Property = resolve_model('properties.Property')
#~ PersonProperty = resolve_model('properties.PersonProperty')

#~ from lino.apps.pcsw.models import Person
#~ from lino.modlib.cv.models import PersonProperty
#~ from lino.modlib.properties.models import Property

from lino.modlib.cbss import models as cbss

from lino.utils import IncompleteDate
from lino.utils.instantiator import create_and_get


class QuickTest(TestCase):
    never_build_site_cache = False
    fixtures = 'sectors purposes cbss_demo'.split()
    #~ pass
    #~ def setUp(self):
        #~ settings.LINO.never_build_site_cache = False
        #~ super(DemoTest,self).setUp()
            
TIMEOUT_RESPONSE = '<urlopen error [Errno 10060] A connection attempt '\
  'failed because the connected party did not properly respond '\
  'after a period of time, or established connection failed '\
  'because connected host has failed to respond>'  
          
TIMEOUT_MESSAGE = """\
We got a timeout. 
That's normal when this test is run behind an IP address that is not registered.
Set your :attr:`lino.Lino.cbss_live_tests` setting to False to skip this test.
"""



def test01(self):
    """
    Execute an IdentifyPersonRequest.
    """
    #~ create_and_get('cbss.Sector')
    #~ from lino.ui.extjs3 import urls # create cache/wsdl files
    settings.LINO.startup() # create cache/wsdl files
    
    global root
    #~ User = resolve_model(settings.LINO.user_model)
    #~ root = User(username='root')
    #~ root.save()
    root = create_and_get(settings.LINO.user_model,username='root')
    
    #~ Person = resolve_model(settings.LINO.person_model)
    global luc
    #~ luc = Person(first_name='Luc',last_name='Saffre')
    #~ luc.save()
    luc = create_and_get(settings.LINO.person_model,first_name='Luc',last_name='Saffre')
    
    # save site settings
    #~ saved_cbss_environment = settings.LINO.cbss_environment
    #~ saved_cbss_user_params = settings.LINO.cbss_user_params
    saved_cbss_live_tests = settings.LINO.cbss_live_tests
    
    
    """
    set fictive user params and run some offline tests
    """
    
    #~ settings.LINO.cbss_user_params = dict(
          #~ UserID='12345678901', 
          #~ Email='123@example.be', 
          #~ OrgUnit='123', 
          #~ MatrixID=12, 
          #~ MatrixSubID=3)
    

    # create an IPR
    #~ from lino.modlib.cbss.models import IdentifyPersonRequest, IdentifyPersonResult
    
    """
    Create an IPR with NISS just to have the XML validated.
    """
    
    #~ req = cbss.IdentifyPersonRequest(national_id="70100853190",last_name='MUSTERMANN')
    req = cbss.IdentifyPersonRequest(national_id="70100853190")
    
    try:
        req.full_clean()
        self.fail('Expected ValidationError "birth_date cannot be blank."')
    except ValidationError:
        pass
        
    req.birth_date = IncompleteDate(1938,6,1)
    try:
        req.validate_request()
        #~ self.fail('Expected Warning "Fields last_name and first_name are mandatory."')
    except Warning:
        pass
        
    req.birth_date = IncompleteDate(1938,0,0)
    req.validate_request()
    
    #~ try:
        #~ req.validate_request()
        #~ self.fail('Expected ')
    #~ except Warning:
        #~ pass
    #~ req.first_name = "MAX"
    #~ req.validate_request()
    
    req = cbss.IdentifyPersonRequest(
        last_name="MUSTERMANN",
        birth_date=IncompleteDate(1938,0,0))
    req.validate_request()
    
    
    """
    Create another one, this time a name search.
    This time we also inspect the generated XML.
    """
    
    #~ root = User.objects.get(username='root')
    
    #~ IdentifyPersonRequest = resolve_model('cbss.IdentifyPersonRequest')
    req = cbss.IdentifyPersonRequest(
        user=root,person=luc,
        last_name="MUSTERMANN",
        first_name="Max",
        birth_date=IncompleteDate(1938,6,1))
    
    req.validate_request()
    
    req.execute_request(environment='')
    expected = """\
Not actually sending because environment is empty. Request would be:
<ipr:IdentifyPersonRequest xmlns:ipr="http://www.ksz-bcss.fgov.be/XSD/SSDN/OCMW_CPAS/IdentifyPerson">
   <ipr:SearchCriteria>
      <ipr:PhoneticCriteria>
         <ipr:LastName>MUSTERMANN</ipr:LastName>
         <ipr:FirstName>Max</ipr:FirstName>
         <ipr:MiddleName></ipr:MiddleName>
         <ipr:BirthDate>1938-06-01</ipr:BirthDate>
      </ipr:PhoneticCriteria>
   </ipr:SearchCriteria>
</ipr:IdentifyPersonRequest>"""
    self.assertEquivalent(expected,req.response_xml)
    
    
    
    #~ """
    #~ Now in test environment but still offline (set `cbss_live_tests` to False)
    #~ """
    
    #~ settings.LINO.cbss_live_tests = False
    #~ now = datetime.datetime(2012,5,9,18,34,50)
    #~ req.execute_request(now=now,environment='test')

    #~ expected = """\
#~ NOT sending because `cbss_live_tests` is False:
#~ <ssdn:SSDNRequest xmlns:ssdn="http://www.ksz-bcss.fgov.be/XSD/SSDN/Service">
   #~ <ssdn:RequestContext>
      #~ <ssdn:AuthorizedUser>
         #~ <ssdn:UserID>12345678901</ssdn:UserID>
         #~ <ssdn:Email>123@example.be</ssdn:Email>
         #~ <ssdn:OrgUnit>123</ssdn:OrgUnit>
         #~ <ssdn:MatrixID>12</ssdn:MatrixID>
         #~ <ssdn:MatrixSubID>3</ssdn:MatrixSubID>
      #~ </ssdn:AuthorizedUser>
      #~ <ssdn:Message>
         #~ <ssdn:Reference>IdentifyPersonRequest # 1</ssdn:Reference>
         #~ <ssdn:TimeRequest>20120509T183450</ssdn:TimeRequest>
      #~ </ssdn:Message>
   #~ </ssdn:RequestContext>
   #~ <ssdn:ServiceRequest>
      #~ <ssdn:ServiceId>OCMWCPASIdentifyPerson</ssdn:ServiceId>
      #~ <ssdn:Version>20050930</ssdn:Version>
      #~ <ipr:IdentifyPersonRequest xmlns:ipr="http://www.ksz-bcss.fgov.be/XSD/SSDN/OCMW_CPAS/IdentifyPerson">
         #~ <ipr:SearchCriteria>
            #~ <ipr:PhoneticCriteria>
               #~ <ipr:LastName>MUSTERMANN</ipr:LastName>
               #~ <ipr:FirstName></ipr:FirstName>
               #~ <ipr:MiddleName></ipr:MiddleName>
               #~ <ipr:BirthDate>1938-06-01</ipr:BirthDate>
            #~ </ipr:PhoneticCriteria>
         #~ </ipr:SearchCriteria>
      #~ </ipr:IdentifyPersonRequest>
   #~ </ssdn:ServiceRequest>
#~ </ssdn:SSDNRequest>"""
    #~ self.assertEquivalent(expected,req.response_xml)
    
    
    """
    Restore real user params.
    """
    
    #~ settings.LINO.cbss_user_params = saved_cbss_user_params
    #~ settings.LINO.cbss_environment = saved_cbss_environment 
    settings.LINO.cbss_live_tests = saved_cbss_live_tests
    
    """
    Skip live tests unless we are in test environment.
    Otherwise we would have to build /media/chache/wsdl files
    """
    if settings.LINO.cbss_environment != 'test':
        return
        
    """
    Skip live tests if `cbss_live_tests` is False
    """
    if not settings.LINO.cbss_live_tests:
        return
    
    resp = req.execute_request()

    if req.response_xml == TIMEOUT_RESPONSE:
        self.fail(TIMEOUT_MESSAGE)
        
    expected = """\
CBSS error 10000:
Severity : ERROR
ReasonCode : 32007004 
Diagnostic : The phonetic search did not return any matches. 
AuthorCodeList : CBSS"""
    #~ print resp.__class__, dir(resp)
    #~ logger.info(req.response_xml)
    self.assertEquivalent(expected,req.response_xml,report_plain=True)
    
    """
    Second live test. There's exactly one Belgian with 
    LastName "SAFFRE" and BirthDate 1968-06-01:
    """
    req = cbss.IdentifyPersonRequest(
        user=root,person=luc,
        last_name="SAFFRE",
        birth_date=IncompleteDate(1968,6,1))
    req.execute_request()
    ar = cbss.IdentifyPersonResult.request(master_instance=req)
    self.assertEqual(1,ar.get_total_count())
    row = ar.data_iterator[0]
    self.assertEqual(
      cbss.IdentifyPersonResult.first_name.value_from_object(row),
      'LUC JOHANNES')
    self.assertEqual(
      cbss.IdentifyPersonResult.national_id.value_from_object(row),
      '68060105329')
    
    """
    Third IPR live test. NISS and birth_date are not enough.
    """
    req = cbss.IdentifyPersonRequest(
        user=root,person=luc,
        national_id="70100853190",birth_date=IncompleteDate(1970,10,8))
    req.execute_request()
    
    expected = """\
CBSS error 10000:
Severity : ERROR
ReasonCode : 31000007
Diagnostic : The expected mandatory argument is not provided or empty.
AuthorCodeList : CBSS"""
    self.assertEquivalent(expected,req.response_xml,report_plain=True)
    
    ar = cbss.IdentifyPersonResult.request(master_instance=req)
    self.assertEqual(0,ar.get_total_count())
    


def test02(self):
    """
    Execute a RetrieveTIGroupsRequest.
    """
    #~ saved_cbss_environment = settings.LINO.cbss_environment
    

    """
    create an RTI
    """
    
    #~ RetrieveTIGroupsRequest = resolve_model('cbss.RetrieveTIGroupsRequest')
    req = cbss.RetrieveTIGroupsRequest(
        user=root,person=luc,
        national_id='12345678901',language='fr')
    
    """
    Try it without environment see the XML.
    Note that NewStyleRequests have no validate_request method.
    """
    
    #~ settings.LINO.cbss_environment = ''
    req.execute_request(environment='')
    #~ print req.response_xml
    expected = """\
Not actually sending because environment is empty. Request would be:
(SearchInformationType){
   ssin = "12345678901"
   language = "fr"
   history = False
 }"""
    self.assertEquivalent(expected,req.response_xml,report_plain=True)
    
    """
    Skip live tests unless we are in test environment.
    Otherwise we would have to build /media/chache/wsdl files
    """
    if settings.LINO.cbss_environment != 'test':
        return
        
    #~ """
    #~ Skip live tests if `cbss_live_tests` is False
    #~ """
    #~ if not settings.LINO.cbss_live_tests:
        #~ return
        
    """
    run the first request for real
    """
    reply = req.execute_request()
    if settings.LINO.cbss_live_tests:
        if req.response_xml == TIMEOUT_RESPONSE:
            self.fail(TIMEOUT_MESSAGE)
        #~ print 20120523, reply
        expected = """\
CBSS error MSG00008:
value : NO_RESULT
code : MSG00008
description : A validation error occurred.
- ssin = 12345678901"""
        #~ logger.info(req.response_xml)
        self.assertEquivalent(expected,req.response_xml,report_plain=True)
    
    """
    second request with a valid SSIN but which is not not integrated.
    """
    req = cbss.RetrieveTIGroupsRequest(
        user=root,person=luc,
        national_id='70100853190',
        language='fr',history=False)
    reply = req.execute_request()
    if settings.LINO.cbss_live_tests:
        expected = """\
CBSS error MSG00012:
value : NO_RESULT
code : MSG00012
description : The given SSIN is not integrated correctly.
- Register = Secondary matrix"""
        #~ print reply
        self.assertEquivalent(expected,req.response_xml,report_plain=True)
    
    """
    """
    #~ today = datetime.date.today()
    today = datetime.date(2012,5,24)
    kw = dict()
    kw.update(purpose=1) # dossier in onderzoek voor een maximale periode van twee maanden
    kw.update(national_id='68060105329') 
    kw.update(user=root) 
    kw.update(person=luc) 
    kw.update(start_date=today)
    kw.update(end_date=today) 
    kw.update(action=cbss.ManageAction.REGISTER) 
    kw.update(query_register=cbss.QueryRegister.SECONDARY) 
    #~ kw.update(id_card_no=) 
    if False:
        # this fails to fail if the suite is being run a second time
        req = cbss.ManageAccessRequest(**kw)
        reply = req.execute_request()
        if settings.LINO.cbss_live_tests:
            expected = """\
    CBSS error 10000:
    Severity : ERROR
    ReasonCode : 31000007
    Diagnostic : The expected mandatory argument is not provided or empty.
    AuthorCodeList : CBSS"""
            #~ print reply
            self.assertEquivalent(expected,req.response_xml,report_plain=True)

    kw.update(last_name='SAFFRE') 
    kw.update(first_name='LUC JOHANNES') 
    kw.update(birth_date=IncompleteDate(1968,6,1)) 
    req = cbss.ManageAccessRequest(**kw)
    reply = req.execute_request()
    if False and settings.LINO.cbss_live_tests:
        expected = """\
<ns3:ManageAccessReply xmlns:ns3="http://www.ksz-bcss.fgov.be/XSD/SSDN/OCMW_CPAS/ManageAccess">
   <ns3:OriginalRequest>
      <ns3:SSIN>68060105329</ns3:SSIN>
      <ns3:Purpose>1</ns3:Purpose>
      <ns3:Period>
         <ns4:StartDate xmlns:ns4="http://www.ksz-bcss.fgov.be/XSD/SSDN/Common">[...]</ns4:StartDate>
         <ns5:EndDate xmlns:ns5="http://www.ksz-bcss.fgov.be/XSD/SSDN/Common">[...]</ns5:EndDate>
      </ns3:Period>
      <ns3:Action>REGISTER</ns3:Action>
   </ns3:OriginalRequest>
   <ns3:Registrations>
      <ns3:Purpose>1</ns3:Purpose>
      <ns3:Period>
         <ns6:StartDate xmlns:ns6="http://www.ksz-bcss.fgov.be/XSD/SSDN/Common">[...]</ns6:StartDate>
         <ns7:EndDate xmlns:ns7="http://www.ksz-bcss.fgov.be/XSD/SSDN/Common">[...]</ns7:EndDate>
      </ns3:Period>
      <ns3:OrgUnit>[...]</ns3:OrgUnit>
      <ns3:Register>SECONDARY</ns3:Register>
   </ns3:Registrations>
</ns3:ManageAccessReply>"""
        #~ print reply
        self.assertEquivalent(expected,req.response_xml,report_plain=True)

    req = cbss.RetrieveTIGroupsRequest(
        user=root,person=luc,
        national_id='68060105329',
        language='fr',history=False)
    reply = req.execute_request()
    if settings.LINO.cbss_live_tests:
        expected = """\
todo"""
        #~ print reply
        self.assertEquivalent(expected,req.response_xml,report_plain=True)
