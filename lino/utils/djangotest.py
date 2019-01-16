# Copyright: Copyright 2011-2018 Rumma & Ko Ltd
# License: BSD, see LICENSE for more details.

"""
Two TestCase classes for writing tests be run using Django's test
runner (i.e. `manage.py test`).
"""

from __future__ import print_function

import logging

logger = logging.getLogger(__name__)

import sys

from django.conf import settings
from django.test import TestCase as DjangoTestCase,TransactionTestCase
from django.core.management import call_command
from django.test import Client
from django.db import connection, reset_queries, connections, DEFAULT_DB_ALIAS
from django.utils import translation

import json
from atelier.utils import AttrDict
from lino.core.signals import testcase_setup # , database_ready

from .test import CommonTestCase


class DjangoManageTestCase(DjangoTestCase, CommonTestCase):
    """
    Adds some extensions to the Django TestCase.
    """

    longMessage = True  # see unittest. used for check_json_result

    override_djangosite_settings = dict()
    """If specified, this is a dict of :class:`Site<lino.core.site.Site>`
    attributes to override before running the test.

    """

    defining_module = None
    """When you decorate your subclass of TestCase, you must also specify::
    
        defining_module = __name__

    Because a decorator will change your class's `__module__`
    attribute and :meth:`test_them_all` would search for test methods
    in the wrong module.

    """

    def __call__(self, *args, **kw):
        """Does some initialization and sends the :attr:`testcase_setup
        <lino.utils.testcase_setup>` signal, then calls super.

        """
        if self.override_djangosite_settings:
            settings.SITE.override_defaults(
                **self.override_djangosite_settings)
        # Make sure that every test runs with the same language.
        # Without this it is possible that some other language may
        # have been activated by previous tests:
        if settings.LANGUAGE_CODE:
            translation.activate(settings.LANGUAGE_CODE)
        testcase_setup.send(self)
        return super(DjangoManageTestCase, self).__call__(*args, **kw)

    def tearDown(self):
        super(DjangoManageTestCase, self).tearDown()

    def setUp(self):
        super(DjangoManageTestCase, self).setUp()
        # 20151203 database_ready.send(self)

    def check_sql_queries(self, *expected):
        """Checks whether the specified expected SQL queries match to those
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

    def get_json_dict(self, *args, **kwargs):
        return self.client_json_dict(self.client.get, *args, **kwargs)
    
    def post_json_dict(self, *args, **kwargs):
        return self.client_json_dict(self.client.post, *args, **kwargs)
    
    def put_json_dict(self, *args, **kwargs):
        return self.client_json_dict(self.client.put, *args, **kwargs)
    
    def client_json_dict(self, meth, username, url, *data, **extra):
        """Send a POST or PUT to client with given username, url and data. The
        client is expected to respond with a JSON encoded
        response. Parse the response's content (which is expected to
        contain a dict), convert this dict to an AttrDict before
        returning it.

        """
        ar = settings.SITE.login(username)
        self.client.force_login(ar.user)
        extra[settings.SITE.remote_user_header] = username
        # extra.update(REMOTE_USER=username)
        # print(20170609, settings.MIDDLEWARE_CLASSES)
        # print(20170609, settings.AUTHENTICATION_BACKENDS)
        res = meth(url, *data, **extra)
        if res.status_code != 200:
            raise Exception("{} gave status code {} instead of 200".format(
                url, res.status_code))
        content = res.content.decode()
        try:
            d = json.loads(content)
        except ValueError as e:
            raise ValueError("Invalid JSON {} : {}".format(content, e))
        return AttrDict(d)

    def check_callback_dialog(self, meth, username, url, dialog, *data, **extra):
        """Check wether the given dialog runs as expected and return the final
        response as an `AttrDict`.

        - `meth` : should be `self.client.get` or `self.client.post`
        - `username` : the username
        - `url` : the url

        - `dialog` : a list of `(expected, reply)` tuples where
          `expected` it the expected response message and `reply` must
          be one of `'yes'` or `'no'` for all items expect for the
          last item where it must be None.

        - `data` : optional positional arguments to the `meth`
        - `extra` : optional keywords arguments to the `meth`

        """
        result = self.client_json_dict(meth, username, url, *data, **extra)
        for expected, answer in dialog:
            self.assertEquivalent(expected, result.message)
            if answer is None:
                return result
            cb = result.xcallback
            self.assertEqual(cb['title'], "Confirmation")
            self.assertEqual(cb['buttons'], {'yes': 'Yes', 'no': 'No'})
            url = '/callbacks/{}/yes'.format(cb['id'])
            result = self.client_json_dict(
                self.client.get, username, url, **extra)
            self.assertEqual(result.success, True)
            
        raise Exception("last item of dialog must have answer None")


class RemoteAuthTestCase(DjangoManageTestCase):
    """
    Base class for tests that use remote http authentication.  We
    override the :meth:`__call__` method in order to simulate
    `remote_user_header <lino.core.site.Site.remote_user_header>`
    being set to ``'REMOTE_USER'``.
    """
    def __call__(self, *args, **kw):
        settings.SITE.override_defaults(remote_user_header='REMOTE_USER')
        mysettings = dict()
        for k in ('MIDDLEWARE', 'AUTHENTICATION_BACKENDS'):
            mysettings[k] = settings.SITE.django_settings.get(k)

        with self.settings(**mysettings):
            return super(RemoteAuthTestCase, self).__call__(*args, **kw)

TestCase = RemoteAuthTestCase


#class WebIndexTestCase(DjangoManageTestCase):
class WebIndexTestCase(RemoteAuthTestCase):
    """Designed to be just imported. No subclassing needed."""

    # removed 20150819 because it took unbearably much time for
    # welfare test suite:
    # override_djangosite_settings = dict(
    #     build_js_cache_on_startup=True)

    def test_get_index(self):
        client = Client()
        url = '/'
        res = client.get(url)
        self.assertEqual(
            res.status_code, 200,
            "Status code %s other than 200 for anonymous on GET %s" % (
                res.status_code, url))
        # res = client.get(url, REMOTE_USER='robin')
        # self.assertEqual(
        #     res.status_code, 200,
        #     "Status code %s other than 200 for robin on GET %s" % (
        #         res.status_code, url))


class NoAuthTestCase(DjangoManageTestCase):

    def __call__(self, *args, **kw):
        # these tests use remote http authentication, so we override the run()
        # method to simulate
        settings.SITE.override_defaults(remote_user_header=None)
        mysettings = dict()
        for k in ('MIDDLEWARE',):
            mysettings[k] = settings.SITE.django_settings.get(k)

        with self.settings(**mysettings):
            return super(NoAuthTestCase, self).__call__(*args, **kw)

class RestoreTestCase(TransactionTestCase):
    """
    Used for testing migrations from previous versions.

    See :doc:`/dev/migtests`.
    """

    tested_versions = []
    """
    A list of strings, each string is a version for which there must
    be a migration dump created by :manage:`makemigdump`.
    """

    def test_restore(self):
        conn = connections[DEFAULT_DB_ALIAS]
        cursor = conn.cursor()
        cursor.execute('PRAGMA foreign_keys = OFF')
        enabled = cursor.execute('PRAGMA foreign_keys').fetchone()[0]
        for v in self.tested_versions:
            run_args = ["tests/dumps/{}/restore.py".format(v),
                        "--noinput"]
            sys.argv = ["manage.py", "run"] + run_args
            call_command("run", *run_args)
    
