# Copyright: Copyright 2011-2014 by Luc Saffre.
# License: BSD, see LICENSE for more details.

"""An extended `django.test.TestCase` to be run using Django's test
runner (i.e. `manage.py test`).

"""

from __future__ import print_function

import os

import logging
logger = logging.getLogger(__name__)

import unittest

from django.conf import settings
import json
from django.utils.importlib import import_module
from django.test import TestCase as DjangoTestCase
from django.db import connection, reset_queries

from lino.core.signals import testcase_setup, database_ready


def check_json_result(response, expected_keys=None, msg=None):
    """
    Checks the result of response which is expected to return 
    a JSON-encoded dictionary with the expected_keys.
    """
    #~ print("20110301 response is %r" % response.content)
    if response.status_code != 200:
        raise Exception(msg)
    try:
        result = json.loads(response.content)
    except ValueError, e:
        logger.warning("%s in %r", e, response.content)
        raise
    if expected_keys is not None:
        if set(result.keys()) != set(expected_keys.split()):
            raise Exception(msg)
    return result


class CommonTestCase(unittest.TestCase):

    def unused_check_json_result(self, *args, **kw):
        return check_json_result(*args, **kw)

    def check_json_result(self, response, expected_keys=None, msg=None):
        """
        Checks the result of response which is expected to return
        a JSON-encoded dictionary with the expected_keys.
        """
        #~ print("20110301 response is %r" % response.content)
        self.assertEqual(
            response.status_code, 200,
            "%s returned %s instead of 200" % (
                msg, response.status_code))
        try:
            result = json.loads(response.content)
        except ValueError as e:
            logger.warning("%s in %r", e, response.content)
            raise
        if expected_keys is not None:
            self.assertEqual(set(result.keys()), set(expected_keys.split()))
        return result

    def assertEquivalent(self, a, b, report_plain=False):
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
        if report_plain:
            logger.warning(
                "----- EXPECTED : -----\n%s\n----- GOT : -----\n%s", a, b)
        else:
            logger.warning("EXPECTED : %s", ' '.join(ta))
            logger.warning("     GOT : %s", ' '.join(tb))
        self.fail("EXPECTED and GOT are not equivalent")

    def request_PUT(self, url, data, **kw):
        """
        Sends a PUT request using Djangos test client, 
        overriding the `content_type` keyword.
        This is how ExtJS grids behave by default.
        """
        kw.update(content_type='application/x-www-form-urlencoded')
        response = self.client.put(url, data, **kw)
        self.assertEqual(response.status_code, 200)
        return response

    def check_sql_queries(self, *expected):
        """
        Checks whether the specified expected SQL queries match to those 
        who actually have been emitted.
        """
        for i, x1 in enumerate(expected):
            if len(connection.queries) <= i:
                self.fail("SQL %d expected %s, found nothing" % (i, x1))
            sql = connection.queries[i]['sql'].strip()
            x2 = x1.split('[...]')
            if len(x2) == 2:
                s = x2.pop().strip()
                if not sql.endswith(s):
                    self.fail("SQL %d doesn't end with %s:---\n%s\n---" %
                              (i, s, sql))

            self.assertEqual(len(x2), 1)
            s = x2[0].strip()
            if not sql.startswith(s):
                self.fail("SQL %d doesn't start with %s:---\n%s\n---" %
                          (i, s, sql))
        if len(expected) < len(connection.queries):
            for q in connection.queries[len(expected):]:
                logger.warning("Unexpected SQL:---\n%s\n---", q['sql'])
            self.fail("Found unexpected SQL")
        reset_queries()

    def assertDoesNotExist(self, model, **kw):
        try:
            model.objects.get(**kw)
            self.fail("Oops, %s(%s) already exists?" % (model.__name__, kw))
        except model.DoesNotExist:
            pass


class DjangoManageTestCase(DjangoTestCase, CommonTestCase):

    """
    Adds some extensions to the Django TestCase.
    
    """

    longMessage = True  # see unittest. used for check_json_result

    override_djangosite_settings = dict()
    """
    If specified, this is a dict of :class:`Site <ad.Site>`
    attributes to override before running the test.
    """

    #~ never_build_site_cache = True
    #~ """
    #~ Test cases usually don't need the site cache, so this is switched off.
    #~ But e.g. :mod:`lino_welfare.modlib.cbss.tests.cbss_tests` switches
    #~ it on because there it is needed.
    #~ """

    defining_module = None
    """
    When you decorate your subclass of TestCase, you must also specify::
    
        defining_module = __name__

    Because a decorator will change 
    your class's  `__module__` attribute 
    and :meth:`test_them_all` would search 
    for test methods in the wrong module.
    
    """

    def __call__(self, *args, **kw):
        """
        Does some initialization and sends the 
        :attr:`testcase_setup <lino.utils.testcase_setup>` 
        signal, then calls super.
        """
        if self.override_djangosite_settings:
            settings.SITE.override_defaults(
                **self.override_djangosite_settings)
        #~ settings.SITE.never_build_site_cache = self.never_build_site_cache
        testcase_setup.send(self)
        #~ database_ready.send(self)
        return super(DjangoManageTestCase, self).__call__(*args, **kw)

    def tearDown(self):
        #~ settings.SITE.shutdown()
        super(DjangoManageTestCase, self).tearDown()

    def setUp(self):
        #~ settings.SITE.never_build_site_cache = self.never_build_site_cache
        # ~ # settings.SITE.remote_user_header = 'REMOTE_USER'
        # ~ # raise Exception("20130704 logger.level is %s" % logger.level)
        # ~ # logger.info("20130704 fire testcase_setup in %s", settings.SITE.title)
        # ~ # print("20130704 send testcase_setup signal %s" % settings.SITE.title)
        #~ testcase_setup.send(self)
        super(DjangoManageTestCase, self).setUp()
        database_ready.send(self)


#~ class DocTest(unittest.TestCase):
    #~ """
    #~ """
    #~ doctest_files = ["index.rst"]
    #~ def test_files(self):
        #~ g = dict(print_=six.print_)
        #~ g.update(settings=settings)
        #~ for n in self.doctest_files:
            #~ f = os.path.join(settings.SITE.project_dir,n)
            #~ if os.path.exists(f):
                #~ print(f)
                #~ res = doctest.testfile(f,module_relative=False,globs=g)
                #~ if res.failed:
                    #~ self.fail("Failed doctest %s" % f)
class RemoteAuthTestCase(DjangoManageTestCase):
    #~ fixtures = [ 'std', 'few_countries', 'ee', 'be', 'demo', 'demo_ee']
    #~ fixtures = 'few_countries few_languages demo_cities std demo demo_ee'.split()
    #~ fixtures = 'std few_countries few_cities few_languages props demo'.split()

    def __call__(self, *args, **kw):
        # these tests use remote http authentication, so we override the run()
        # method to simulate
        #~ settings.SITE.remote_user_header = 'REMOTE_USER'
        settings.SITE.override_defaults(remote_user_header='REMOTE_USER')
        mysettings = dict()
        for k in ('MIDDLEWARE_CLASSES',):
            mysettings[k] = settings.SITE.django_settings.get(k)
        #~ MIDDLEWARE_CLASSES = settings.SITE.django_settings.get('MIDDLEWARE_CLASSES')
        with self.settings(**mysettings):
            return super(RemoteAuthTestCase, self).__call__(*args, **kw)

TestCase = RemoteAuthTestCase


class NoAuthTestCase(DjangoManageTestCase):

    def __call__(self, *args, **kw):
        # these tests use remote http authentication, so we override the run()
        # method to simulate
        #~ settings.SITE.remote_user_header = 'REMOTE_USER'
        settings.SITE.override_defaults(remote_user_header=None)
        mysettings = dict()
        for k in ('MIDDLEWARE_CLASSES',):
            mysettings[k] = settings.SITE.django_settings.get(k)
        #~ MIDDLEWARE_CLASSES = settings.SITE.django_settings.get('MIDDLEWARE_CLASSES')
        with self.settings(**mysettings):
            return super(NoAuthTestCase, self).__call__(*args, **kw)


class AutoTestCase(DjangoManageTestCase):

    """
    Deprecated. No longer recommended. 
    This brings a very small advantage and some important disadvantages:
    
    - more complexity leading to possible problems which are hard to debug
    - cannot run a function separately.
    
    
    This was to increase lisibility of your module 
    when you want to group several separate tests into a 
    single fixture load. 
    You gain 4 leading spaces for every line.
    
    The Django testrunner creates and initializes a new database 
    for every TestCase instance.
    
    Using `django.test`::

      from django.test import TestCase
      class DemoTest(TestCase):
          fixtures = 'std props demo'.split()
                  
          def test01(self):
             ...
              
          def test02(self):
             ...
         
    Using `lino.utils.djangotest`::
    
      from lino.utils.djangotest import AutoTestCase
      class DemoTest(AutoTestCase):
          fixtures = 'std props demo'.split()
                  
      def test01(self):
         ...
          
      def test02(self):
         ...
          
    
    If you instantiate a `lino.utils.djangotest.TestCase` in your test module, 
    it will automatically inspect the globel namespace of your module and 
    add all callables whose name begins with "test" to it's test suite.
    
    Since all 'testXX' functions are run in a same database, their execution 
    order may be important: keep in mind that they are executed in 
    *alphabetical* order, and that database changes remain for the whole 
    sequence.
    
    """

    #~ def runTest(self,*args,**kw):
        # ~ # super(TestCase,self).runTest(*args,**kw)
        #~ m = import_module(self.__module__)
        #~ for k,v in m.__dict__.items():
            #~ if k.startswith('test') and callable(v):
                # ~ # print(20110301, k,v)
                # ~ # self.__class__.__dict__[k] = v
                # ~ # setattr(self.__class__,k,v)
                #~ if not getattr(v,'skip',False):
                    #~ v(self)

    def test_them_all(self):
        """
        This method will be executed automatically since its 
        name starts with ``test_``.
        """
        m = import_module(self.defining_module or self.__module__)
        #~ for k,v in m.__dict__.items():
        for k in sorted(m.__dict__.keys()):
            v = m.__dict__.get(k)
            if k.startswith('test') and callable(v):
                if not getattr(v, 'skip', False):
                    v(self)
