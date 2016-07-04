# -*- coding: UTF-8 -*-
# Copyright 2015-2016 Luc Saffre
# License: BSD (see file COPYING for details)

"""A selection of names to be used in tested documents.
"""

from __future__ import print_function

import six
from builtins import str

from lino import AFTER17
if AFTER17:
    import django
    django.setup()
from lino.api.shell import *
from django.utils import translation
from django.test import Client
import json
from bs4 import BeautifulSoup
from lino.utils import AttrDict
from lino.utils import i2d
from lino.utils.xmlgen.html import E
from lino.utils.diag import analyzer

from atelier.rstgen import table
from atelier.rstgen import attrtable
from atelier.utils import unindent

test_client = Client()
# naming it simply "client" caused conflict with a
# `lino_welfare.pcsw.models.Client`

import collections
HttpQuery = collections.namedtuple(
    'HttpQuery',
    ['username', 'url_base', 'json_fields', 'expected_rows', 'kwargs'])


def get_json_dict(username, uri, an='detail'):
    url = '/api/{0}?fmt=json&an={1}'.format(uri, an)
    res = test_client.get(url, REMOTE_USER=username)
    assert res.status_code == 200
    return json.loads(res.content)


def get_json_soup(username, uri, fieldname, **kwargs):
    """Being authentified as `username`, perform a web request to `uri` of
    the test client.

    """
    d = get_json_dict(username, uri, **kwargs)
    html = d['data'][fieldname]
    return BeautifulSoup(html, 'lxml')


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
            raise Exception("'{0}' != '{1}'".format(
                ' '.join(list(result.keys())), expected_keys))
    return result


def demo_get(
        username, url_base, json_fields,
        expected_rows=None, **kwargs):
    from django.conf import settings
    case = HttpQuery(username, url_base, json_fields,
                     expected_rows, kwargs)
    # Django test client does not like future pseudo-unicode strings
    # See #870
    url = six.text_type(settings.SITE.buildurl(case.url_base, **case.kwargs))
    # print(20160329, url)
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

    response = test_client.get(url, REMOTE_USER=six.text_type('foo'))
    if response.status_code != 403:
        raise Exception(
            "Status code %s other than 403 for anonymous on GET %s" % (
                response.status_code, url))

    response = test_client.get(url, REMOTE_USER=str(case.username))
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


def screenshot(obj, filename, rstname, username='robin'):
    """Insert a screenshot of the detail window for the given database
    object.

    Usage example in the source code of
    http://xl.lino-framework.org/specs/holidays.html.

    Problems: doesn't seem to wait long enough and
    therefore produces a white .png file.

    How to specify the filename? the current directory when doctest is
    running is normally the project root, but that's not sure. Best
    place would be the same directory as the rst file, but how to know
    that name from within a tested snippet?

    """
    from lino.api.selenium import Album, runserver

    assert filename.endswith('.png')
    assert rstname.endswith('.rst')

    self = dd.plugins.extjs.renderer
    uri = self.get_detail_url(obj)
    # ar = rt.login(username, renderer=self)
    # h = self.instance_handler(ar, obj)
    # uri = self.js2url(h)
    print(uri)

    def f(driver):
        app = Album(driver)
        driver.get("http://127.0.0.1:8000" + uri)
        # driver.get(uri)
        app.stabilize()
        if not driver.get_screenshot_as_file(filename):
            app.error("Failed to create {0}".format(filename))

    runserver(settings.SETTINGS_MODULE, f)
        

def show_menu_path(spec, language=None):
    from lino.core.menus import find_menu_item
    from lino.sphinxcontrib.actordoc import menuselection_text

    # profile = ar.get_user().profile
    # menu = settings.SITE.get_site_menu(settings.SITE.kernel, profile)
    # mi = menu.find_item(spec)
    mi = find_menu_item(spec)

    if mi is None:
        raise Exception("Invalid spec {0}".format(spec))

    def doit():
        print(menuselection_text(mi))

    if language:
        with translation.override(language):
            return doit()
    return doit()

    # items = [mi]
    # p = mi.parent
    # while p:
    #     items.insert(0, p)
    #     p = p.parent
    # return " --> ".join([i.label for i in items])


def noblanklines(s):
    """Remove blank lines from output. This is used to increase
    readability when some expected output would otherweise contain
    disturbing `<BLANKLINE>` which are not relevant to the test
    itself.

    """
    return '\n'.join([ln for ln in s.splitlines() if ln.strip()])


def show_choices(username, url):
    """Print the choices returned via web client."""
    response = test_client.get(url, REMOTE_USER=username)
    result = json.loads(response.content)
    for r in result['rows']:
        print(r['text'])
        # print(r['value'], r['text'])


def show_fields(model, fieldnames):
    """Print an overview description of the specified fields of the
    specified model.

    """
    cells = []
    cols = ["Internal name", "Verbose name", "Help text"]
    for n in fieldnames.split():
        fld = model._meta.get_field(n)
        cells.append([n, fld.verbose_name, unindent(fld.help_text)])

    print(table(cols, cells).strip())


