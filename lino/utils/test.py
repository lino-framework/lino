# -*- coding: UTF-8 -*-
# Copyright 2013-2014 Luc Saffre
# This file is part of the Lino project.
# Lino is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
# Lino is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
# You should have received a copy of the GNU Lesser General Public License
# along with Lino; if not, see <http://www.gnu.org/licenses/>.

"""Defines the :class:`DemoTestCase` class, used to define tests that are
to be run tests directly in the `persistent test database`_, *without*
using the Django test runner (i.e. without creating a temporary test
database).

Persistent test database
------------------------

This is the database defined by...

  import os
  os.environ['DJANGO_SETTINGS_MODULE'] = "lino_welfare.settings.test"

This expects the persistent test database to be initialized.

, and
it works only in an environment with :setting:`remote_user_header`
set to ``'REMOTE_USER'``. Concretely

"""

from __future__ import print_function

from djangosite.utils.pythontest import TestCase as PythonTestCase
from djangosite.utils.djangotest import CommonTestCase
from django.test import Client
from django.conf import settings

import collections
HttpQuery = collections.namedtuple(
    'HttpQuery',
    ['username', 'url_base', 'json_fields', 'expected_rows', 'kwargs'])


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
            except Exception as e:
                pass
                #~ self.tc.assertEqual(str(e),msg)
                #~ if str(e) != msg:
                        #~ raise Exception("Expected %r but got %r" % (msg,str(e)))

        response = self.client.get(url, REMOTE_USER='foo')
        self.assertEqual(
            response.status_code, 403,
            "Status code other than 403 for anonymous on GET %s" % url)

        response = self.client.get(url, REMOTE_USER=case.username)
        try:
        #~ if True:
            result = self.check_json_result(response, case.json_fields, url)

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

        except Exception as e:
            print("%s:\n%s" % (url, e))
            raise
