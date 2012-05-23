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

#from lino.igen import models
#from lino.modlib.contacts.models import Contact, Companies
#from lino.modlib.countries.models import Country
#~ from lino.modlib.contacts.models import Companies


from lino.utils import i2d
from lino.utils import babel
from lino.tools import resolve_model
#Companies = resolve_model('contacts.Companies')
from lino.utils.test import TestCase

#~ Person = resolve_model('contacts.Person')
#~ Property = resolve_model('properties.Property')
#~ PersonProperty = resolve_model('properties.PersonProperty')

#~ from lino.apps.pcsw.models import Person
#~ from lino.modlib.cv.models import PersonProperty
#~ from lino.modlib.properties.models import Property

from lino.utils import IncompleteDate


class QuickTest(TestCase):
    auto_build_site_cache = True
    #~ pass
    #~ def setUp(self):
        #~ settings.LINO.auto_build_site_cache = False
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
    
    from lino.ui.extjs3 import urls # create cache/wsdl files
    
    # save site settings
    saved_cbss_environment = settings.LINO.cbss_environment
    saved_cbss_user_params = settings.LINO.cbss_user_params
    saved_cbss_live_tests = settings.LINO.cbss_live_tests
    
    """
    set fictive user params and run some offline tests
    """
    
    settings.LINO.cbss_user_params = dict(
          UserID='12345678901', 
          Email='123@example.be', 
          OrgUnit='123', 
          MatrixID=12, 
          MatrixSubID=3)
    

    # create an IPR
    from lino.modlib.cbss.models import IdentifyPersonRequest, IdentifyPersonResult
    #~ IdentifyPersonRequest = resolve_model('cbss.IdentifyPersonRequest')
    req = IdentifyPersonRequest(
        last_name="MUSTERMANN",
        birth_date=IncompleteDate(1968,6,1))
    
    """
    try it without environment and with `validate=True`
    just to have the XML generated and validated
    """
    
    settings.LINO.cbss_environment = ''
    req.execute_request(None,validate=True)
    expected = """\
Not actually sending because environment is empty. Request would be:
<ipr:IdentifyPersonRequest xmlns:ipr="http://www.ksz-bcss.fgov.be/XSD/SSDN/OCMW_CPAS/IdentifyPerson">
   <ipr:SearchCriteria>
      <ipr:PhoneticCriteria>
         <ipr:LastName>MUSTERMANN</ipr:LastName>
         <ipr:FirstName></ipr:FirstName>
         <ipr:MiddleName></ipr:MiddleName>
         <ipr:BirthDate>1968-06-01</ipr:BirthDate>
      </ipr:PhoneticCriteria>
   </ipr:SearchCriteria>
</ipr:IdentifyPersonRequest>"""
    self.assertEqual(req.response_xml,expected)
    
    
    
    """
    Now in test environment but still offline (set `cbss_live_tests` to False)
    """
    
    settings.LINO.cbss_live_tests = False
    settings.LINO.cbss_environment = 'test'
    now = datetime.datetime(2012,5,9,18,34,50)
    req.execute_request(None,now=now)
    #~ print req.response_xml

    expected = """\
NOT sending because `cbss_live_tests` is False:
<ssdn:SSDNRequest xmlns:ssdn="http://www.ksz-bcss.fgov.be/XSD/SSDN/Service">
   <ssdn:RequestContext>
      <ssdn:AuthorizedUser>
         <ssdn:UserID>12345678901</ssdn:UserID>
         <ssdn:Email>123@example.be</ssdn:Email>
         <ssdn:OrgUnit>123</ssdn:OrgUnit>
         <ssdn:MatrixID>12</ssdn:MatrixID>
         <ssdn:MatrixSubID>3</ssdn:MatrixSubID>
      </ssdn:AuthorizedUser>
      <ssdn:Message>
         <ssdn:Reference>IdentifyPersonRequest # 1</ssdn:Reference>
         <ssdn:TimeRequest>20120509T183450</ssdn:TimeRequest>
      </ssdn:Message>
   </ssdn:RequestContext>
   <ssdn:ServiceRequest>
      <ssdn:ServiceId>OCMWCPASIdentifyPerson</ssdn:ServiceId>
      <ssdn:Version>20050930</ssdn:Version>
      <ipr:IdentifyPersonRequest xmlns:ipr="http://www.ksz-bcss.fgov.be/XSD/SSDN/OCMW_CPAS/IdentifyPerson">
         <ipr:SearchCriteria>
            <ipr:PhoneticCriteria>
               <ipr:LastName>MUSTERMANN</ipr:LastName>
               <ipr:FirstName></ipr:FirstName>
               <ipr:MiddleName></ipr:MiddleName>
               <ipr:BirthDate>1968-06-01</ipr:BirthDate>
            </ipr:PhoneticCriteria>
         </ipr:SearchCriteria>
      </ipr:IdentifyPersonRequest>
   </ssdn:ServiceRequest>
</ssdn:SSDNRequest>"""
    self.assertEqual(req.response_xml,expected)
    
    
    """
    Restore real user params.
    """
    
    settings.LINO.cbss_user_params = saved_cbss_user_params
    settings.LINO.cbss_environment = saved_cbss_environment 
    settings.LINO.cbss_live_tests = saved_cbss_live_tests
    
    """
    If `cbss_live_tests` is True, run some live tests.
    """
    if settings.LINO.cbss_live_tests:
      
        resp = req.execute_request()
    
        if req.response_xml == TIMEOUT_RESPONSE:
            self.fail(TIMEOUT_MESSAGE)
            
        expected = """\
CBSS error 10000:
Severity : ERROR foo
ReasonCode : 32007004 
Diagnostic : The phonetic search did not return any matches. 
AuthorCodeList : CBSS"""
        #~ print resp.__class__, dir(resp)
        #~ logger.info(req.response_xml)
        self.assertEquivalent(expected,req.response_xml,report_plain=True)
        
        req = IdentifyPersonRequest(
            last_name="SAFFRE",
            birth_date=IncompleteDate(1968,6,1))
            
        req.execute_request(None)
        ar = IdentifyPersonResult.request(master_instance=req)
        self.assertEqual(1,ar.get_total_count())
        row = ar.data_iterator[0]
        self.assertEquivalent(
          IdentifyPersonResult.first_name.value_from_object(row),
          'LUC JOHANNES')
        

    

def test02(self):
    """
    Execute a RetrieveTIGroupsRequest.
    """
    saved_cbss_environment = settings.LINO.cbss_environment

    # create an RTI
    
    RetrieveTIGroupsRequest = resolve_model('cbss.RetrieveTIGroupsRequest')
    req = RetrieveTIGroupsRequest(national_id='12345678901')
    
    # try it without environment to validate and see the XML
    
    settings.LINO.cbss_environment = ''
    req.execute_request(None,validate=True)
    #~ print req.response_xml
    expected = """\
Not actually sending because environment is empty. Request would be:
(SearchInformationType){
   ssin = "12345678901"
   language = "de"
   history = False
 }"""
    self.assertEqual(req.response_xml,expected)
    
    if settings.LINO.cbss_live_tests:
        # try it in test environment
        settings.LINO.cbss_environment = 'test'
        req.execute_request(None)
        if req.response_xml == TIMEOUT_RESPONSE:
            self.fail(TIMEOUT_MESSAGE)
            
        expected = """\
"""
        #~ logger.info(req.response_xml)
        self.assertEqual(req.response_xml,expected)
    
    settings.LINO.cbss_environment = saved_cbss_environment 
