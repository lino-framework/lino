# -*- coding: UTF-8 -*-
## Copyright 2013 Luc Saffre
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

Defines the :class:`DemoTestCase` class.

"""

from __future__ import print_function

from djangosite.utils.pythontest import TestCase as PythonTestCase
from djangosite.utils.djangotest import CommonTestCase
from django.test import Client
from django.conf import settings

import collections
HttpQuery = collections.namedtuple('HttpQuery',
  ['username','url_base','json_fields','expected_rows','kwargs'])

#~ from djangosite.utils.djangotest import check_json_result

if False:
    
  class URLTester(object):
    """
    Usage example::
    
        ut = self.make_url_tester()
        ut.add_case(...)
        ut.add_case(...)
        ...
        ut.run_tests()
    """
    def __init__(self,testcase):
        testcase.assertEqual(settings.SITE.remote_user_header,'REMOTE_USER')
        self.tc = testcase
        self.client = Client()
        self.cases = []
        
        
    def add_case(self,username,url_base,json_fields,expected_rows,**kwargs):
        case = HttpQuery(username,url_base,json_fields,expected_rows,kwargs)
        self.cases.append(case)
        return case
        
    def run_tests(self):
        #~ failures = 0
        for i,case in enumerate(self.cases):
            url = settings.SITE.build_admin_url(case.url_base,**case.kwargs)
            
            if True:
                msg = 'Using remote authentication, but no user credentials found.'
                try:
                    response = self.client.get(url) 
                    self.tc.fail("Expected '%s'" % msg)
                    #~ raise Exception("Expected '%s'" % msg)
                except Exception as e:
                    pass
                    #~ self.tc.assertEqual(str(e),msg)
                    #~ if str(e) != msg:
                        #~ raise Exception("Expected %r but got %r" % (msg,str(e)))
                
            response = self.client.get(url,REMOTE_USER='foo') 
            #~ if response.status_code != 403:
                #~ raise Exception("Status code for anonymous on GET %s" % url)
            self.tc.assertEqual(response.status_code,403,"Status code other than 403 for anonymous on GET %s" % url)
            
            response = self.client.get(url,REMOTE_USER=case.username)
            try:
            #~ if True:
                result = self.tc.check_json_result(response,case.json_fields,url)
                
                num = case.expected_rows
                if num is not None:
                    if not isinstance(num,tuple):
                        num = [num]
                    if result['count'] not in num:
                        msg = "%s got %s rows instead of %s" % (url,result['count'],num)
                        #~ raise Exception("[%d] %s" % (i, msg))
                        self.tc.fail("[%d] %s" % (i, msg))
                        #~ failures += 1
                
            except Exception as e:
                print("[%d] %s:\n%s" % (i, url,e))
                raise
                #~ failures += 1
                
        #~ if failures:
            #~ msg = "%d URL failures" % failures
            #~ self.tc.fail(msg)
            #~ raise Exception(msg)




class DemoTestCase(PythonTestCase,CommonTestCase):
    """
    Used to run tests directly on the demo database,
    *without* using the Django test runner
    (i.e. without creating a temporary test database). 
    
    This expects the demo database to be initialized.
    
    Note also that this works only in an environment with 
    :setting:`remote_user_header` set to ``'REMOTE_USER'``.
    """
    
    def __call__(self,*args,**kw):
        self.client = Client()
        return super(DemoTestCase,self).__call__(*args,**kw)

    #~ def make_url_tester(self):
        #~ """
        #~ Instantiate and return a :class:`URLTester` object.
        #~ """
        #~ return URLTester(self)


    def demo_get(self,username,url_base,json_fields,expected_rows,**kwargs):
        case = HttpQuery(username,url_base,json_fields,expected_rows,kwargs)
        url = settings.SITE.build_admin_url(case.url_base,**case.kwargs)
        
        if True:
            msg = 'Using remote authentication, but no user credentials found.'
            try:
                response = self.client.get(url) 
                self.fail("Expected '%s'" % msg)
                #~ raise Exception("Expected '%s'" % msg)
            except Exception as e:
                pass
                #~ self.tc.assertEqual(str(e),msg)
                #~ if str(e) != msg:
                    #~ raise Exception("Expected %r but got %r" % (msg,str(e)))
            
        response = self.client.get(url,REMOTE_USER='foo') 
        #~ if response.status_code != 403:
            #~ raise Exception("Status code for anonymous on GET %s" % url)
        self.assertEqual(response.status_code,403,"Status code other than 403 for anonymous on GET %s" % url)
        
        response = self.client.get(url,REMOTE_USER=case.username)
        try:
        #~ if True:
            result = self.check_json_result(response,case.json_fields,url)
            
            num = case.expected_rows
            if num is not None:
                if not isinstance(num,tuple):
                    num = [num]
                if result['count'] not in num:
                    msg = "%s got %s rows instead of %s" % (url,result['count'],num)
                    #~ raise Exception("[%d] %s" % (i, msg))
                    self.fail(msg)
                    #~ failures += 1
            
        except Exception as e:
            print("%s:\n%s" % (url,e))
            raise
