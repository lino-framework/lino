.. _lino.tested.export_excel:

Exporting to Excel
==================

.. to run only this test:
  $ python setup.py test -s tests.DocsTests.test_presto

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


>>> url = "http://127.0.0.1:8000/api/cal/MyEvents?_dc=1414086313105&cw=197&cw=139&cw=197&cw=36&cw=133&cw=68&cw=133&cw=106&cw=106&cw=106&cw=139&cw=87&cw=55&cw=87&cw=55&cw=80&cw=36&cw=36&cw=133&cw=68&cw=133&cw=133&cw=87&cw=133&cw=68&ch=&ch=&ch=&ch=true&ch=true&ch=true&ch=true&ch=false&ch=true&ch=true&ch=true&ch=false&ch=false&ch=false&ch=false&ch=true&ch=true&ch=true&ch=true&ch=true&ch=true&ch=true&ch=true&ch=true&ch=true&ci=when_text&ci=summary&ci=workflow_buttons&ci=id&ci=owner_type&ci=owner_id&ci=user&ci=modified&ci=created&ci=build_time&ci=build_method&ci=start_date&ci=start_time&ci=end_date&ci=end_time&ci=access_class&ci=sequence&ci=auto_type&ci=event_type&ci=transparent&ci=room&ci=priority&ci=state&ci=assigned_to&ci=owner&name=0&pv=23.10.2014&pv=&pv=&pv=&pv=1&pv=&pv=&pv=&pv=y&an=export_excel&sr=72"

