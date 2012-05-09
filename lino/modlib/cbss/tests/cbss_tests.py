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
            
TIMEOUT_MESSAGE = '<urlopen error [Errno 10060] A connection attempt '\
  'failed because the connected party did not properly respond '\
  'after a period of time, or established connection failed '\
  'because connected host has failed to respond>'  
          
  

def test01(self):
    """
    Execute an IdentifyPersonRequest.
    """
    
    from lino.ui.extjs3 import urls # create cache/wsdl files
    
    # save site settings
    saved_cbss_environment = settings.LINO.cbss_environment
    saved_cbss_user_params = settings.LINO.cbss_user_params
    saved_cbss_live_tests = settings.LINO.cbss_live_tests
    
    # set fictive user params
    
    settings.LINO.cbss_user_params = dict(
          UserID='12345678901', 
          Email='123@example.be', 
          OrgUnit='123', 
          MatrixID=12, 
          MatrixSubID=3)
    

    # create an IPR
    
    IdentifyPersonRequest = resolve_model('cbss.IdentifyPersonRequest')
    req = IdentifyPersonRequest(last_name="MUSTERMANN",birth_date=IncompleteDate(1968,6,1))
    
    # try it without environment to see the XML
    
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
    
    settings.LINO.cbss_live_tests = False
    # try it in test environment
    settings.LINO.cbss_environment = 'test'
    now = datetime.datetime(2012,5,9,18,34,50)
    req.execute_request(None,now=now)
    print req.response_xml
    expected = """\
NOT sending because `cbss_live_tests` is False:
<wsc:xmlString xmlns:wsc="http://ksz-bcss.fgov.be/connectors/WebServiceConnector">&lt;ssdn:SSDNRequest xmlns:ssdn=&quot;http://www.ksz-bcss.fgov.be/XSD/SSDN/Service&quot;&gt;
   &lt;ssdn:RequestContext&gt;
      &lt;ssdn:AuthorizedUser&gt;
         &lt;ssdn:UserID&gt;12345678901&lt;/ssdn:UserID&gt;
         &lt;ssdn:Email&gt;123@example.be&lt;/ssdn:Email&gt;
         &lt;ssdn:OrgUnit&gt;123&lt;/ssdn:OrgUnit&gt;
         &lt;ssdn:MatrixID&gt;12&lt;/ssdn:MatrixID&gt;
         &lt;ssdn:MatrixSubID&gt;3&lt;/ssdn:MatrixSubID&gt;
      &lt;/ssdn:AuthorizedUser&gt;
      &lt;ssdn:Message&gt;
         &lt;ssdn:Reference&gt;IdentifyPersonRequest # 1&lt;/ssdn:Reference&gt;
         &lt;ssdn:TimeRequest&gt;20120509T183450&lt;/ssdn:TimeRequest&gt;
      &lt;/ssdn:Message&gt;
   &lt;/ssdn:RequestContext&gt;
   &lt;ssdn:ServiceRequest&gt;
      &lt;ssdn:ServiceId&gt;OCMWCPASIdentifyPerson&lt;/ssdn:ServiceId&gt;
      &lt;ssdn:Version&gt;20050930&lt;/ssdn:Version&gt;
      &lt;ipr:IdentifyPersonRequest xmlns:ipr=&quot;http://www.ksz-bcss.fgov.be/XSD/SSDN/OCMW_CPAS/IdentifyPerson&quot;&gt;
         &lt;ipr:SearchCriteria&gt;
            &lt;ipr:PhoneticCriteria&gt;
               &lt;ipr:LastName&gt;MUSTERMANN&lt;/ipr:LastName&gt;
               &lt;ipr:FirstName&gt;&lt;/ipr:FirstName&gt;
               &lt;ipr:MiddleName&gt;&lt;/ipr:MiddleName&gt;
               &lt;ipr:BirthDate&gt;1968-06-01&lt;/ipr:BirthDate&gt;
            &lt;/ipr:PhoneticCriteria&gt;
         &lt;/ipr:SearchCriteria&gt;
      &lt;/ipr:IdentifyPersonRequest&gt;
   &lt;/ssdn:ServiceRequest&gt;
&lt;/ssdn:SSDNRequest&gt;</wsc:xmlString>"""
    self.assertEqual(req.response_xml,expected)
    
    settings.LINO.cbss_user_params = saved_cbss_user_params
    settings.LINO.cbss_environment = saved_cbss_environment 
    settings.LINO.cbss_live_tests = saved_cbss_live_tests
    
    if settings.LINO.cbss_live_tests:
        req.execute_request(None)
    
        if req.response_xml == TIMEOUT_MESSAGE:
            self.fail("""\
We got a timeout. 
That's normal when this test is run behind an IP address that is not registered.
Set your :attr:`lino.Lino.cbss_live_tests` setting to False to skip this test.
""")
        print req.response_xml
        expected = ''
        self.assertEqual(req.response_xml,expected)


    

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
    
    if settings.LINO.cbss_user_params:
        # try it in test environment
        settings.LINO.cbss_environment = 'test'
        req.execute_request(None)
        
        if req.response_xml == TIMEOUT_MESSAGE:
            self.fail("""\
We got a timeout. 
That's normal when this test is run behind an IP address that is not registered.
Set your `cbss_user_params` settings to None to skip this test.
""")
        expected = """\
        """
        self.assertEqual(req.response_xml,expected)
    
    settings.LINO.cbss_environment = saved_cbss_environment 
