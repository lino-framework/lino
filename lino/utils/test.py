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

Used in :mod:`lino.modlib.pcsw.tests.pcsw_tests`

"""

import logging
logger = logging.getLogger(__name__)

from django.conf import settings
from django.utils import simplejson
from django.utils.importlib import import_module
from django.test import TestCase as DjangoTestCase
from django.db import connection, reset_queries


class TestCase(DjangoTestCase):
    """
    Adds some extensions to the Django TestCase.
    
    This is to increase lisibility of your module 
    when you want to group several separate tests into a 
    single fixture load. 
    You gain 4 leading spaces for every line.
    
    The Django testrunner creates and initializes a new database 
    for every TestCase instance.
    
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
          
    
    If you instantiate a `lino.utils.test.TestCase` in your test module, 
    it will automatically inspect the globel namespace of your module and 
    add all callables whose name begins with "test" to it's test suite.
    
    Since all 'testXX' functions are run in a same database, their execution 
    order may be important: keep in mind that they are executed in 
    *alphabetical* order, and that database changes remain for the whole 
    sequence.
    
    """
    
    defining_module = None
    """
    When you decorate your subclass of TestCase, you must also specify::
    
        defining_module = __name__

    Because a decorator will change 
    your class's  `__module__` attribute 
    and :meth:`test_them_all` would search 
    for test methods in the wrong module.
    
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
                  
    def setUp(self):
        settings.LINO.auto_makeui = False
        super(TestCase,self).setUp()
        
    def test_them_all(self):
        """
        This method will be executed automatically since it's 
        name starts with 'test_'.
        """
        m = import_module(self.defining_module or self.__module__)
        #~ for k,v in m.__dict__.items():
        for k in sorted(m.__dict__.keys()):
            v = m.__dict__.get(k)
            if k.startswith('test') and callable(v):
                if not getattr(v,'skip',False):
                    v(self)
                  
    def check_json_result(self,response,expected_keys):
        """
        Checks the result of response which is expected to return 
        a JSON-encoded dictionary with the expected_keys.
        """
        #~ print "20110301 response is %r" % response.content
        try:
            result = simplejson.loads(response.content)
        except ValueError,e:
            logger.warning("%s in %r",e,response.content)
            raise 
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
        ta = a.strip().split() 
        tb = b.strip().split()
        if ta == tb:
            return 
        logger.warning("EXPECTED : %s",' '.join(ta))
        logger.warning("     GOT : %s",' '.join(tb))
        #~ logger.warning("EXPECTED : %s",a)
        #~ logger.warning("     GOT : %s",b)
        self.fail("EXPECTED and GOT are not equivalent")
        
    def request_PUT(self,url,data,**kw):
        """
        Sends a PUT request using Djangos test client, 
        overriding the `content_type` keyword.
        This is how ExtJS grids behave by default.
        """
        kw.update(content_type='application/x-www-form-urlencoded')
        response = self.client.put(url,data,**kw)
        self.assertEqual(response.status_code,200)
        return response
        
    def check_sql_queries(self,*expected):
        """
        Checks whether the specified expected SQL queries match to those 
        who actually have been emitted.
        """
        for i,x1 in enumerate(expected):
            sql = connection.queries[i]['sql'].strip()
            x2 = x1.split('[...]')
            if len(x2) == 2:
                s = x2.pop().strip()
                if not sql.endswith(s):
                    self.fail("SQL %d doesn't end with %s:---\n%s\n---" % (i,s,sql))
                    
            self.assertEqual(len(x2),1)
            s = x2[0].strip()
            if not sql.startswith(s):
                self.fail("SQL %d doesn't start with %s:---\n%s\n---" % (i,s,sql))
        if len(expected) < len(connection.queries):
            for q in connection.queries[len(expected):]:
                logger.warning("Unexpected SQL:---\n%s\n---",q['sql'])
            self.fail("Found unexpected SQL")
        reset_queries()
