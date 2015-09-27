.. _lino.tested.export_excel:

Exporting to Excel
==================

When :mod:`lino.modlib.export_excel` is installed, every grid view has
a button `Export to Excel`.

This document tests this functionality.


.. to run only this test:

    $ python setup.py test -s tests.DocsTests.test_min1
    
    doctest init:

    >>> import os
    >>> os.environ['DJANGO_SETTINGS_MODULE'] = 'lino.projects.min1.settings.doctests'
    >>> from lino.api.doctest import *


Robin has twelve appointments in the period 20141023..20141122:

>>> from lino.utils import i2d
>>> pv = dict(start_date=i2d(20141023), end_date=i2d(20141122))
>>> rt.login('robin').show(cal.MyEvents, param_values=pv, header_level=1)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
=======================================================================
My appointments (Managed by Robin Rood, Dates 23.10.2014 to 22.11.2014)
=======================================================================
====================== ===================== =============== ================
 When                   Calendar Event Type   Summary         Workflow
---------------------- --------------------- --------------- ----------------
 Thu 10/23/14 (10:20)   Meeting               Meeting         **Took place**
 Fri 10/24/14 (11:10)   Meeting               Consultation    **Cancelled**
 Sat 10/25/14 (08:30)   Meeting               Evaluation      **Suggested**
 Sat 10/25/14 (13:30)   Meeting               Seminar         **Omitted**
 Sun 10/26/14 (09:40)   Meeting               First meeting   **Draft**
 Mon 10/27/14 (10:20)   Meeting               Interview       **Took place**
 Mon 10/27/14 (11:10)   Meeting               Lunch           **Cancelled**
 Tue 10/28/14 (13:30)   Meeting               Dinner          **Omitted**
 Wed 10/29/14 (08:30)   Meeting               Breakfast       **Suggested**
 Wed 10/29/14 (09:40)   Meeting               Meeting         **Draft**
 Thu 10/30/14 (10:20)   Meeting               Consultation    **Took place**
 Fri 10/31/14 (11:10)   Meeting               Seminar         **Cancelled**
====================== ===================== =============== ================
<BLANKLINE>

Let's import them to `.xls`.

When exporting to `.xls`, the URL is rather long because it includes
detailed information about the grid columns: their widths (``cw``),
whether they are hidden (``ch``) and their ordering (``ci``). This is
necessary because we want the resulting `.xls` sheet to reflect
if the client has changed these.

.. intermezzo 20150828

    >>> cal.MyEvents.model.manager_roles_required
    set([<class 'lino.modlib.office.roles.OfficeStaff'>])
    >>> ba = cal.MyEvents.get_action_by_name("export_excel")
    >>> u = rt.login('robin').user
    >>> ba.actor.get_view_permission(u.profile)
    True
    >>> ba.action.get_view_permission(u.profile)
    True
    >>> ba.allow_view(u.profile)
    True
    >>> ba.get_view_permission(u.profile)
    True

A subtlety: the third column (`workflow_buttons`) contains images.

>>> url = "/api/cal/MyEvents?_dc=1414106085710"
>>> url += "&cw=411&cw=287&cw=411&cw=73&cw=274&cw=140&cw=274&cw=220&cw=220&cw=220&cw=287&cw=181&cw=114&cw=181&cw=114&cw=170&cw=73&cw=73&cw=274&cw=140&cw=274&cw=274&cw=181&cw=274&cw=140"
>>> url += "&ch=&ch=true&ch="
>>> url += "&ch=true&ch=true&ch=true&ch=true&ch=true&ch=false&ch=true&ch=true&ch=false&ch=false&ch=true&ch=true&ch=true&ch=true&ch=true&ch=true&ch=true&ch=true&ch=true&ch=true&ch=true&ch=true"
>>> url += "&ci=when_text&ci=summary&ci=workflow_buttons&ci=id&ci=owner_type&ci=owner_id&ci=user&ci=modified&ci=created&ci=build_time&ci=build_method&ci=start_date&ci=start_time&ci=end_date&ci=end_time&ci=access_class&ci=sequence&ci=auto_type&ci=event_type&ci=transparent&ci=room&ci=priority&ci=state&ci=assigned_to&ci=owner&name=0"
>>> url += "&pv=23.10.2014&pv=22.11.2014&pv=&pv=&pv=2&pv=&pv=&pv=&pv=y"
>>> url += "&an=export_excel&sr=61"

>>> res = test_client.get(url, REMOTE_USER='robin')
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
My appointments (Managed by Rol

It has 5 columns and 13 rows:

>>> print(s.ncols, s.nrows)
(5, 13)

The first row contains our column headings. Which differ from those of
the table above because our user had changed them manually:

>>> print(s.row(0))
[text:u'When', text:u'Workflow', text:u'Created', text:u'Start date', text:u'Start time']

>>> print(s.row(1))
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
[text:u'Thu 10/23/14 (08:30)', text:u'**Suggested** \u2192 `[img flag_green] <...>`__', xldate:..., xldate:..., xldate:...]


.. _invalid_requests:

Answering to invalid requests
=============================

We are going to send some invalid AJAX requests to
:class:`lino.modlib.contacts.models.RolesByPerson`, a slave table on
person.

>>> contacts.RolesByPerson.master
<class 'lino.modlib.contacts.models.Person'>

Simulate an AJAX request:

>>> headers = dict(HTTP_X_REQUESTED_WITH='XMLHttpRequest')
>>> headers.update(REMOTE_USER='robin')

Here is a valid request:

>>> url = "/api/contacts/RolesByPerson?fmt=json&start=0&limit=15&mt=8&mk=114"
>>> res = test_client.get(url, **headers)
>>> print(res.status_code)
200
>>> d = AttrDict(json.loads(res.content))
>>> d.count
1
>>> print(d.title)
Contact for of Mr Hans Altenberg


Specifying an *invalid primary key* for the master (5114 in the
example below) will internally raise an `ObjectDoesNotExist`
exception, which in turn will cause an `HttpResponseBadRequest`
response (i.e. status code 400):

>>> url = "/api/contacts/RolesByPerson?fmt=json&start=0&limit=15&mt=8&mk=114114"
>>> res = test_client.get(url, **headers)
>>> print(res.status_code)
400

Since RolesByPerson has a known master class (i.e. Person), the
``mt``url parameter is *ignored*: invalid value for ``mt`` does *not*
raise an exception:

>>> url = "/api/contacts/RolesByPerson?fmt=json&start=0&limit=15&mt=8888&mk=114"
>>> res = test_client.get(url, **headers)
>>> print(res.status_code)
200

