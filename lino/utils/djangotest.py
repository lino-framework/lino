# Copyright: Copyright 2011-2015 by Luc Saffre.
# License: BSD, see LICENSE for more details.

"""Two TestCase classes for writing tests be run using Django's test
runner (i.e. `manage.py test`).

"""

from __future__ import print_function

import logging
logger = logging.getLogger(__name__)

from django.conf import settings
from django.test import TestCase as DjangoTestCase
from django.test import Client
from django.db import connection, reset_queries

from lino.core.signals import testcase_setup, database_ready

from .test import CommonTestCase


class DjangoManageTestCase(DjangoTestCase, CommonTestCase):
    """Adds some extensions to the Django TestCase.

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


class WebIndexTestCase(DjangoManageTestCase):
    """Designed to be just imported. No subclassing needed."""

    # removed 20150819 because it took unbearably much time for
    # welfare test suite:
    # override_djangosite_settings = dict(
    #     build_js_cache_on_startup=True)

    def test_get_root(self):
        client = Client()
        url = '/'
        res = client.get(url)
        self.assertEqual(
            res.status_code, 200,
            "Status code %s other than 200 for anonymous on GET %s" % (
                res.status_code, url))


class RemoteAuthTestCase(DjangoManageTestCase):

    def __call__(self, *args, **kw):
        # these tests use remote http authentication, so we override the run()
        # method to simulate
        #~ settings.SITE.remote_user_header = 'REMOTE_USER'
        settings.SITE.override_defaults(remote_user_header='REMOTE_USER')
        mysettings = dict()
        for k in ('MIDDLEWARE_CLASSES',):
            mysettings[k] = settings.SITE.django_settings.get(k)

        with self.settings(**mysettings):
            return super(RemoteAuthTestCase, self).__call__(*args, **kw)

TestCase = RemoteAuthTestCase


class NoAuthTestCase(DjangoManageTestCase):

    def __call__(self, *args, **kw):
        # these tests use remote http authentication, so we override the run()
        # method to simulate
        settings.SITE.override_defaults(remote_user_header=None)
        mysettings = dict()
        for k in ('MIDDLEWARE_CLASSES',):
            mysettings[k] = settings.SITE.django_settings.get(k)

        with self.settings(**mysettings):
            return super(NoAuthTestCase, self).__call__(*args, **kw)

