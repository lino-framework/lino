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

test_client = Client()
# naming it simply "client" caused conflict with a
# `lino_welfare.pcsw.models.Client`


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
