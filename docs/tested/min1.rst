.. _lino.tested.min1:

Exporting to Excel
==================

.. to run only this test:
  $ python setup.py test -s tests.DocsTests.test_min1

General stuff:

>>> import os
>>> import json
>>> os.environ['DJANGO_SETTINGS_MODULE'] = 'lino.projects.min1.settings.doctests'
>>> from lino.runtime import *
>>> from lino import dd
>>> from django.test import Client
>>> client = Client()



>>> url = "/api/cal/MyEvents?_dc=1414086313105&cw=197&cw=139&cw=197&cw=36&cw=133&cw=68&cw=133&cw=106&cw=106&cw=106&cw=139&cw=87&cw=55&cw=87&cw=55&cw=80&cw=36&cw=36&cw=133&cw=68&cw=133&cw=133&cw=87&cw=133&cw=68&ch=&ch=&ch=&ch=true&ch=true&ch=true&ch=true&ch=false&ch=true&ch=true&ch=true&ch=false&ch=false&ch=false&ch=false&ch=true&ch=true&ch=true&ch=true&ch=true&ch=true&ch=true&ch=true&ch=true&ch=true&ci=when_text&ci=summary&ci=workflow_buttons&ci=id&ci=owner_type&ci=owner_id&ci=user&ci=modified&ci=created&ci=build_time&ci=build_method&ci=start_date&ci=start_time&ci=end_date&ci=end_time&ci=access_class&ci=sequence&ci=auto_type&ci=event_type&ci=transparent&ci=room&ci=priority&ci=state&ci=assigned_to&ci=owner&name=0&pv=23.10.2014&pv=&pv=&pv=&pv=1&pv=&pv=&pv=&pv=y&an=export_excel&sr=72"
>>> res = client.get(url, REMOTE_USER='robin')
>>> print(res.status_code)
200
>>> result = json.loads(res.content)
>>> print(result.keys())
[u'open_url', u'success']
>>> print(result['open_url'])
/media/cache/appyxls/127.0.0.1/cal.MyEvents.xls

>>> from unipath import Path
>>> p = Path(settings.MEDIA_ROOT, 
...    'cache', 'appyxls', '127.0.0.1', 'cal.MyEvents.xls')
>>> p.exists()
True

Now we test whether the file is really okay.

>>> import xlrd
>>> wb = xlrd.open_workbook(p)
>>> s = wb.sheet_by_index(0)

Note that long titles are truncated:

>>> print(s.name.strip())
My events (Dates 23.10.2014 to

It has 8 columns and 13 rows:

>>> print(s.ncols, s.nrows)
(8, 13)


