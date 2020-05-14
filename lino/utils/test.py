# -*- coding: UTF-8 -*-
# Copyright 2013-2020 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""Defines the :class:`DocTest` and :class:`DemoTestCase` classes.

"""

# import sys
# import codecs
# sys.stdout = codecs.getwriter('utf8')(sys.stdout)

import logging ; logger = logging.getLogger(__name__)

import os
import json
import unittest
import doctest

from lino.utils.pythontest import TestCase as PythonTestCase

import collections
HttpQuery = collections.namedtuple(
    'HttpQuery',
    ['username', 'url_base', 'json_fields', 'expected_rows', 'kwargs'])


class CommonTestCase(unittest.TestCase):
    """An extended `django.test.TestCase`.

    """

    def create_obj(self, model, **values):
        """Create the given database object, run :meth:`full_clean` and
        :meth:`save`, return the object.

        Deprecated. Use :func:`lino.utils.instantiator.create_row`
        instead.

        """
        obj = model(**values)
        obj.full_clean()
        obj.save()
        return obj

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
    """Used to define tests that are to be run directly in the demo
    database, *without* using the Django test runner (i.e. without
    creating a temporary test database).

    It expects the demo database to be initialized, and it works only in
    an environment with :attr:`lino.core.site.Site.remote_user_header`
    set to ``'REMOTE_USER'``.

    """
    def __call__(self, *args, **kw):
        from django.test import Client
        self.client = Client()
        return super(DemoTestCase, self).__call__(*args, **kw)

    def demo_get(self, username, url_base, json_fields, expected_rows,
                 **kwargs):
        from django.conf import settings
        case = HttpQuery(username, url_base, json_fields,
                         expected_rows, kwargs)
        url = settings.SITE.buildurl(case.url_base, **case.kwargs)

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



#class WebIndexTestCase(DjangoManageTestCase):
#class WebIndexTestCase(RemoteAuthTestCase):
class WebIndexTestCase(DemoTestCase):
    """

    Test whether a :manage:`runserver` on this database would respond with 200
    to an anonymous request.

    You add this to your test suite by just importing it. No subclassing needed.

    By convention this is done in a file :xfile:`test_webindex.py`, i.e. when
    such a file is present in the :xfile:`tests` directory of a demo project,
    this test is being run as part of :manage:`test`.

    """
    # 20200513 : WebIndexTestCase now runs on the populatd demo data, not as an empty django test case

    # removed 20150819 because it took unbearably much time for
    # welfare test suite:
    # override_djangosite_settings = dict(
    #     build_js_cache_on_startup=True)

    tested_urls = ('/', '/?su=3', '/?su=1234')

    def test_get_index(self):
        from django.conf import settings
        # client = Client()
        for url in self.tested_urls:
            # print("20200513", url)
            res = self.client.get(url)
            self.assertEqual(
                res.status_code, 200,
                "Status code %s other than 200 for anonymous on GET %s" % (
                    res.status_code, url))

        if settings.SITE.user_model:
            for user in settings.SITE.user_model.objects.all():
                if user.user_type:
                    self.client.force_login(user)
                    res = self.client.get(url)
                    self.assertEqual(
                        res.status_code, 200,
                        "Status code {} for {} on GET {}".format(
                            res.status_code, user, url))

        # res = client.get(url, REMOTE_USER='robin')
        # self.assertEqual(
        #     res.status_code, 200,
        #     "Status code %s other than 200 for robin on GET %s" % (
        #         res.status_code, url))
