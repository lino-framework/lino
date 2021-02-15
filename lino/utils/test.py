# -*- coding: UTF-8 -*-
# Copyright 2013-2021 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""Defines some TestCase classes that are meant for writing general Python test
cases (not Django test cases, which are defined in
:mod:`lino.utils.djangotest`).

"""

import logging ; logger = logging.getLogger(__name__)

import os
import json
import unittest
import doctest

from lino.utils.pythontest import TestCase as PythonTestCase
from lino.utils.instantiator import create_row
from lino.utils import AttrDict
from lino.core import constants

import collections
HttpQuery = collections.namedtuple(
    'HttpQuery',
    ['username', 'url_base', 'json_fields', 'expected_rows', 'kwargs'])


class CommonTestCase(unittest.TestCase):
    """

    A :class:`unittest.TestCase` (not a :class:`django.test.TestCase`) that
    starts a Django test client on a demo database populated using
    :manage:`prep`.

    """

    def create_obj(self, model, **values):
        """Create the given database object, run :meth:`full_clean` and
        :meth:`save`, return the object.

        This is here for backwards compatibility.
        New code should use :func:`lino.utils.instantiator.create_row` instead.

        """
        return create_row(model, **values)

    def check_json_result(self, response, expected_keys=None, msg=''):
        """Checks the result of response which is expected to return a
        JSON-encoded dictionary with the expected_keys.

        """
        # print("20150129 response is %r" % response.content)
        self.assertEqual(
            response.status_code, 200,
            "Response status ({0}) was {1} instead of 200".format(
                msg, response.status_code))
        content = response.content.decode()
        try:
            result = json.loads(content)
        except ValueError as e:
            logger.warning("%s in %r", e, content)
            raise
        if expected_keys is not None:
            self.assertEqual(set(result.keys()), set(expected_keys.split()))
        return result

    def assertEquivalent(self, a, b, report_plain=False):
        """Compares two strings `a` (expected) and `b` (got), ignoring
        whitespace repetitions and writing a logger message in case
        they are different.  For long strings it's then more easy to
        find the difference.

        """
        if a == b:
            return
        ta = a.strip().split()
        tb = b.strip().split()
        if ta == tb:
            return
        if report_plain:
            msg = "----- EXPECTED : -----\n%s\n----- GOT : -----\n%s" % (a, b)
        else:
            msg =  "\nEXPECTED : %s" % (' '.join(ta))
            msg += "\n     GOT : %s" % (' '.join(tb))
        if False:
            logger.warning(msg)
            self.fail("EXPECTED and GOT are not equivalent")
        else:
            self.fail(msg)

    def request_PUT(self, url, data, **kw):
        """Sends a PUT request using Django's test client, overriding the
        `content_type` keyword.  This is how ExtJS grids behave by
        default.

        """
        kw.update(content_type='application/x-www-form-urlencoded')
        response = self.client.put(url, data, **kw)
        self.assertEqual(response.status_code, 200)
        return response

    def assertDoesNotExist(self, model, **kw):
        try:
            model.objects.get(**kw)
            self.fail("Oops, %s(%s) already exists?" % (model.__name__, kw))
        except model.DoesNotExist:
            pass


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
        from django.conf import settings
        g = dict()
        g.update(settings=settings)
        # g.update(unicode_literals=unicode_literals)
        # g.update(print_function=print_function)
        kwargs = dict(globs=g)
        kwargs.update(module_relative=False)
        kwargs.update(encoding="utf-8")
        # kwargs.update(optionflags=doctest.REPORT_ONLY_FIRST_FAILURE)
        # kwargs.update(verbose=False)
        for n in self.doctest_files:
            fn = os.path.join(settings.SITE.project_dir, n)
            if os.path.exists(fn):
                res = doctest.testfile(fn, **kwargs)
                if res.failed:
                    self.fail("Failed doctest %s" % fn)
                    return
            else:
                self.fail("No such file: %s" % fn)


class DemoTestCase(PythonTestCase, CommonTestCase):
    """

    Base class for unit tests that are meant to run directly in a demo
    project that has been initialized with :manage:`prep`.

    It expects the demo database to be initialized, and it should be read-only,
    i.e. not modify any data.

    This is used by the :manage:`demotest` command.

    """
    def __call__(self, *args, **kw):
        from django.test import Client
        self.client = Client()
        return super(DemoTestCase, self).__call__(*args, **kw)

    def login(self, username, pwd):
        """

        Invoke the :class:`lino.modlib.users.SignIn` action for the given
        username and password. Unlike :meth:`django.test.Client.force_login`,
        this simulates a real login, which later causes Lino to build the JS
        cache for this user.

        """

        data = {
            constants.URL_PARAM_FIELD_VALUES: [username, pwd],
            constants.URL_PARAM_ACTION_NAME: 'sign_in'}
        url = "/api/users/UsersOverview/-99998"
        res = self.client.post(url, data)
        self.assertEqual(res.status_code, 200)
        content = res.content.decode()
        d = json.loads(content)
        # return str(d.keys())
        return AttrDict(d)

    def demo_get(self, username, url_base, json_fields, expected_rows,
                 **kwargs):
        from django.conf import settings
        case = HttpQuery(username, url_base, json_fields,
                         expected_rows, kwargs)
        url = settings.SITE.buildurl(case.url_base, **case.kwargs)

        msg = 'Using remote authentication, but no user credentials found.'
        try:
            response = self.client.get(url)
            self.fail("Expected '%s'" % msg)
            #~ raise Exception("Expected '%s'" % msg)
        except Exception:
            pass

        response = self.client.get(url, REMOTE_USER='foo')
        self.assertEqual(
            response.status_code, 403,
            "Status code %s other than 403 for anonymous on GET %s" % (
                response.status_code, url))

        response = self.client.get(url, REMOTE_USER=case.username)
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
