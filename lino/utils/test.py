## Copyright 2011 Luc Saffre
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
Extensions to the `django.test` package.

Used in :mod:`lino.modlib.dsbe.tests.dsbe_tests`

"""

import logging
logger = logging.getLogger(__name__)

from django.utils import simplejson
from django.utils.importlib import import_module
from django.test import TestCase as DjangoTestCase

class TestCase(DjangoTestCase):
    """
    Adds some extensions to the Django TestCase.
    
    This is to increase lisibility of your module 
    when you want to group several separate tests into a 
    single fixture load. 
    You gain 4 leading spaces for every line.
    
    The Django testrunner creates and initializes a new database 
    for every TestCase instance.
    
    If you instantiate a `lino.utils.test.TestCase` in your test module, 
    it will automatically inspect the globel namespace of your module.
    
    Using `django.test`::

      from django.test import TestCase
      class DemoTest(TestCase):
          fixtures = 'std few_countries few_languages props demo'.split()
                  
          def test01(self):
             ...
              
          def test02(self):
             ...
         
    Using `lino.utils.test`::
    
      from lino.utils.test import TestCase
      class DemoTest(TestCase):
          fixtures = 'std few_countries few_languages props demo'.split()
                  
      def test01(self):
         ...
          
      def test02(self):
         ...
          
    
    you simply write global functions that take a single argument, 
    and the test case 
    """
    #~ def runTest(self,*args,**kw):
        #~ # super(TestCase,self).runTest(*args,**kw)
        #~ m = import_module(self.__module__)
        #~ for k,v in m.__dict__.items():
            #~ if k.startswith('test') and callable(v):
                #~ # print 20110301, k,v
                #~ # self.__class__.__dict__[k] = v
                #~ # setattr(self.__class__,k,v)
                #~ if not getattr(v,'skip',False):
                    #~ v(self)
                  
    def test_them_all(self):
        m = import_module(self.__module__)
        for k,v in m.__dict__.items():
          if k.startswith('test') and callable(v):
              if not getattr(v,'skip',False):
                  v(self)
                  
    def check_json_result(self,response,expected_keys):
        """
        Checks the result of response which is expected to return 
        a JSON-encoded dictionary with the expected_keys.
        """
        #~ print "20110301 response is %r" % response.content
        result = simplejson.loads(response.content)
        self.assertEqual(set(result.keys()),set(expected_keys.split()))
        return result
        
    def assertEquivalent(self,a,b):
        """
        Compares to strings, ignoring whitespace repetitions and 
        writing a logger message in case they are different. 
        For long strings it's then more easy to find the difference.
        """
        if a == b:
            return
        a = a.strip().split() 
        b = b.strip().split()
        if a == b:
            return 
        logger.warning("EXPECTED : %s",' '.join(a))
        logger.warning("     GOT : %s",' '.join(b))
        self.fail("EXPECTED and GOT are not equivalent")
        
    def request_PUT(self,url,data):
        """
        Sends a PUT request using Djangos test client, 
        overriding the `content_type` keyword.
        This is how ExtJS grids behave by default.
        """
        response = self.client.put(url,data,content_type='application/x-www-form-urlencoded')
        self.assertEqual(response.status_code,200)
        return response
        
