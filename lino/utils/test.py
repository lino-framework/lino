# -*- coding: UTF-8 -*-
# Copyright 2013-2014 Luc Saffre
# License: BSD (see file COPYING for details)

"""Defines the :class:`DemoTestCase` class, used to define tests that are
to be run tests directly in the `persistent test database`_, *without*
using the Django test runner (i.e. without creating a temporary test
database).

It expects the persistent test database to be initialized, and it
works only in an environment with :attr:`ad.Site.remote_user_header`
set to ``'REMOTE_USER'``. Concretely


Persistent test database
------------------------

This is the database defined by...

  import os
  os.environ['DJANGO_SETTINGS_MODULE'] = "myproject.settings.test"

"""

from __future__ import print_function

import os
import unittest
import doctest

from lino.utils.pythontest import TestCase as PythonTestCase
from lino.utils.djangotest import CommonTestCase
from django.test import Client
from django.conf import settings

import collections
HttpQuery = collections.namedtuple(
    'HttpQuery',
    ['username', 'url_base', 'json_fields', 'expected_rows', 'kwargs'])


class DocTest(unittest.TestCase):

    """
    Looks for a file "index.rst" in your project_dir and (if it exists) 
    run doctest on it.
    """
    doctest_files = ["index.rst"]

    def test_files(self):
        #~ g = dict(print_=six.print_)
        g = dict()
        g.update(settings=settings)
        for n in self.doctest_files:
            f = os.path.join(settings.SITE.project_dir, n)
            if os.path.exists(f):
                #~ print f
                res = doctest.testfile(f, module_relative=False, globs=g)
                if res.failed:
                    self.fail("Failed doctest %s" % f)



class DemoTestCase(PythonTestCase, CommonTestCase):

    "The class definition"
    def __call__(self, *args, **kw):
        self.client = Client()
        return super(DemoTestCase, self).__call__(*args, **kw)

    def demo_get(self, username, url_base, json_fields, expected_rows,
                 **kwargs):
        case = HttpQuery(username, url_base, json_fields,
                         expected_rows, kwargs)
        url = settings.SITE.build_admin_url(case.url_base, **case.kwargs)

        if True:
            msg = 'Using remote authentication, but no user credentials found.'
            try:
                response = self.client.get(url)
                self.fail("Expected '%s'" % msg)
                #~ raise Exception("Expected '%s'" % msg)
            except Exception:
                pass
                #~ self.tc.assertEqual(str(e),msg)
                #~ if str(e) != msg:
                        #~ raise Exception("Expected %r but got %r" % (msg,str(e)))

        response = self.client.get(url, REMOTE_USER='foo')
        self.assertEqual(
            response.status_code, 403,
            "Status code %s other than 403 for anonymous on GET %s" % (
                response.status_code, url))

        response = self.client.get(url, REMOTE_USER=case.username)
        # try:
        if True:
            user = settings.SITE.user_model.objects.get(
                username=case.username)
            result = self.check_json_result(
                response, case.json_fields,
                "GET %s for user %s" % (url, user))

            num = case.expected_rows
            if num is not None:
                if not isinstance(num, tuple):
                    num = [num]
                if result['count'] not in num:
                    msg = "%s got %s rows instead of %s" % (
                        url, result['count'], num)
                    #~ raise Exception("[%d] %s" % (i, msg))
                    self.fail(msg)
                    #~ failures += 1

        # except Exception as e:
        #     print("%s:\n%s" % (url, e))
        #     raise
