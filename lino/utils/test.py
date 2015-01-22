# -*- coding: UTF-8 -*-
# Copyright 2013-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""Defines the :class:`DocTest` and :class:`DemoTestCase` classes.

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
    """Looks for a file "index.rst" in your project_dir and (if it exists)
    runs doctest on it.

    This is for tests to be run by the Django test runner on a
    temporary test database.

    """
    doctest_files = ["index.rst"]
    """The files to be tested.

    """

    def test_files(self):
        #~ g = dict(print_=six.print_)
        g = dict()
        g.update(settings=settings)
        for n in self.doctest_files:
            f = os.path.join(settings.SITE.project_dir, n)
            if os.path.exists(f):
                res = doctest.testfile(f, module_relative=False, globs=g)
                if res.failed:
                    self.fail("Failed doctest %s" % f)
            else:
                self.fail("No such file: %s" % f)


class DemoTestCase(PythonTestCase, CommonTestCase):
    """Used to define tests that are to be run directly in the demo
    database, *without* using the Django test runner (i.e. without
    creating a temporary test database).

    It expects the demo database to be initialized, and it works only in
    an environment with :attr:`lino.core.site.Site.remote_user_header`
    set to ``'REMOTE_USER'``.

    """
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
