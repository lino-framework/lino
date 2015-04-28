# -*- coding: UTF-8 -*-
# Copyright 2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""A selection of names to be used in tested documents."""



from lino.api.shell import *
from django.utils import translation
from django.test import Client
import json
from bs4 import BeautifulSoup
from lino.utils import AttrDict
from lino.utils import i2d
from lino.utils.xmlgen.html import E
from atelier.rstgen import attrtable

test_client = Client()
# naming it simply "client" caused conflict with a
# `lino_welfare.pcsw.models.Client`

import collections
HttpQuery = collections.namedtuple(
    'HttpQuery',
    ['username', 'url_base', 'json_fields', 'expected_rows', 'kwargs'])


def get_json_soup(username, uri, fieldname, an='detail'):
    """Being authentified as `username`, perform a web request to `uri` of
    the test client.

    """
    url = '/api/{0}?fmt=json&an={1}'.format(uri, an)
    res = test_client.get(url, REMOTE_USER=username)
    assert res.status_code == 200
    d = json.loads(res.content)
    html = d['data'][fieldname]
    return BeautifulSoup(html)


def post_json_dict(username, url, data, **extra):
    """Send a POST with given username, url and data. The client is
    expected to respond with a JSON encoded response. Parse the
    response's content (which is expected to contain a dict), convert
    this dict to an AttrDict before returning it.

    """
    res = test_client.post(url, data, REMOTE_USER=username, **extra)
    assert res.status_code == 200
    return AttrDict(json.loads(res.content))


def check_json_result(response, expected_keys=None, msg=''):
    """Checks the result of response which is expected to return a
    JSON-encoded dictionary with the expected_keys.

    """
    # print("20150129 response is %r" % response.content)
    if response.status_code != 200:
        raise Exception(
            "Response status ({0}) was {1} instead of 200".format(
                msg, response.status_code))
    try:
        result = json.loads(response.content)
    except ValueError as e:
        raise Exception("{0} in {1}".format(e, response.content))
    if expected_keys is not None:
        if set(result.keys()) != set(expected_keys.split()):
            raise Exception("{0} != {1}".format(
                result.keys() != expected_keys.split()))
    return result


def demo_get(username, url_base, json_fields, expected_rows, **kwargs):
    from django.conf import settings
    case = HttpQuery(username, url_base, json_fields,
                     expected_rows, kwargs)
    url = settings.SITE.buildurl(case.url_base, **case.kwargs)

    if True:
        msg = 'Using remote authentication, but no user credentials found.'
        try:
            response = self.client.get(url)
            raise Exception("Expected '%s'" % msg)
        except Exception:
            pass
            #~ self.tc.assertEqual(str(e),msg)
            #~ if str(e) != msg:
                    #~ raise Exception("Expected %r but got %r" % (msg,str(e)))

    response = test_client.get(url, REMOTE_USER='foo')
    if response.status_code != 403:
        raise Exception(
            "Status code %s other than 403 for anonymous on GET %s" % (
                response.status_code, url))

    response = test_client.get(url, REMOTE_USER=case.username)
    # try:
    if True:
        user = settings.SITE.user_model.objects.get(
            username=case.username)
        result = check_json_result(
            response, case.json_fields,
            "GET %s for user %s" % (url, user))

        num = case.expected_rows
        if num is not None:
            if not isinstance(num, tuple):
                num = [num]
            if result['count'] not in num:
                msg = "%s got %s rows instead of %s" % (
                    url, result['count'], num)
                raise Exception(msg)

    # except Exception as e:
    #     print("%s:\n%s" % (url, e))
    #     raise


