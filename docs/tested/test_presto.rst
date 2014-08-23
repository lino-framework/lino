.. _lino.tested.export_excel:

Exporting to Excel
==================

.. to run (almost) only this test:
  $ python setup.py test -s tests.DocsTests.test_docs

General stuff:

>>> import os
>>> import json
>>> os.environ['DJANGO_SETTINGS_MODULE'] = 'lino.projects.presto.settings.doctests'
>>> from lino.runtime import *
>>> from lino import dd
>>> from django.test import Client
>>> client = Client()



>>> url = '/api/countries/Countries?_dc=1408820029695&cw=198&cw=198&cw=198&cw=198&cw=54&cw=54&cw=45&ch=&ch=&ch=&ch=&ch=&ch=true&ch=true&ci=name&ci=name_de&ci=name_fr&ci=name_et&ci=isocode&ci=short_code&ci=iso3&name=0&an=export_excel'
>>> res = client.get(url, REMOTE_USER='robin')
>>> print(res.status_code)
200
>>> result = json.loads(res.content)
>>> print(result.keys())
[u'open_url', u'success']
>>> print(result['open_url'])
/media/cache/appyxls/127.0.0.1/countries.Countries.xls

