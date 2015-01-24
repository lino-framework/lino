from lino.runtime import *
from django.utils import translation
from django.test import Client
import json
from bs4 import BeautifulSoup
from lino.utils import AttrDict

client = Client()

def get_json_soup(username, uri, fieldname, an='detail'):
    url = '/api/{0}?fmt=json&an={1}'.format(uri, an)
    res = client.get(url, REMOTE_USER=username)
    assert res.status_code == 200
    d = json.loads(res.content)
    html = d['data'][fieldname]
    return BeautifulSoup(html)
