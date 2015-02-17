.. _lino.tested.export_excel:

Exporting to Excel
==================

This document obsoletes :doc:`test_presto`.

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

When exporting to `.xls`, the URL is rather long because it includes
detailed information about the grid columns: their widths (``cw``),
whether they are hidden (``ch``) and their ordering (``ci``).

>>> url = "/api/cal/MyEvents?_dc=1414106085710"
>>> url += "&cw=411&cw=287&cw=411&cw=73&cw=274&cw=140&cw=274&cw=220&cw=220&cw=220&cw=287&cw=181&cw=114&cw=181&cw=114&cw=170&cw=73&cw=73&cw=274&cw=140&cw=274&cw=274&cw=181&cw=274&cw=140"
>>> url += "&ch=&ch=true&ch=true&ch=true&ch=true&ch=true&ch=true&ch=true&ch=false&ch=true&ch=true&ch=false&ch=false&ch=true&ch=true&ch=true&ch=true&ch=true&ch=true&ch=true&ch=true&ch=true&ch=true&ch=true&ch=true"
>>> url += "&ci=when_text&ci=summary&ci=workflow_buttons&ci=id&ci=owner_type&ci=owner_id&ci=user&ci=modified&ci=created&ci=build_time&ci=build_method&ci=start_date&ci=start_time&ci=end_date&ci=end_time&ci=access_class&ci=sequence&ci=auto_type&ci=event_type&ci=transparent&ci=room&ci=priority&ci=state&ci=assigned_to&ci=owner&name=0"
>>> url += "&pv=23.10.2014&pv=&pv=&pv=&pv=2&pv=&pv=&pv=&pv=y"
>>> url += "&an=export_excel&sr=61"

>>> res = client.get(url, REMOTE_USER='robin')
>>> print(res.status_code)
200
>>> result = json.loads(res.content)
>>> print(result.keys())
[u'open_url', u'success']
>>> print(result['open_url'])
/media/cache/appyxls/127.0.0.1/cal.MyEvents.xls

The action performed without error.
But does the file exist?

>>> from unipath import Path
>>> p = Path(settings.MEDIA_ROOT, 
...    'cache', 'appyxls', '127.0.0.1', 'cal.MyEvents.xls')
>>> p.exists()
True

Now test whether the file is really okay.

>>> import xlrd
>>> wb = xlrd.open_workbook(p)
>>> s = wb.sheet_by_index(0)

Note that long titles are truncated:

>>> print(s.name.strip())
My appointments (Dates 23.10.20

It has 4 columns and 13 rows:

>>> print(s.ncols, s.nrows)
(4, 13)

>>> print(s.row(0))
[text:u'When', text:u'Created', text:u'Start date', text:u'Start time']

>>> print(s.row(1))
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
[text:u'Thu 10/23/14 (10:20)', xldate:..., xldate:..., xldate:...]


