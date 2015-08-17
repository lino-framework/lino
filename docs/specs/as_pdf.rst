.. _noi.specs.as_pdf:

=================
Printing tables
=================


.. How to test only this document:

    $ python setup.py test -s tests.SpecsTests.test_as_pdf
    
    doctest init:

    >>> from __future__ import print_function, unicode_literals
    >>> import os
    >>> os.environ['DJANGO_SETTINGS_MODULE'] = 'lino_noi.projects.team.settings.doctests'
    >>> from lino.api.doctest import *


This document describes and tests the print to pdf function.


.. contents::
  :local:

>>> settings.SITE.appy_params.update(raiseOnError=True)
>>> def mytest(k):
...     url = 'http://127.0.0.1:8000/api/{0}?an=as_pdf'.format(k)
...     res = test_client.get(url, REMOTE_USER='robin')
...     assert res.status_code == 200
...     result = json.loads(res.content)
...     assert result['success']
...     print(result['open_url'])

>>> mytest("tickets/TicketsToDo")  #doctest: -SKIP
/media/cache/appypdf/127.0.0.1/tickets.TicketsToDo.pdf

>>> mytest("tickets/Tickets")  #doctest: -SKIP
/media/cache/appypdf/127.0.0.1/tickets.Tickets.pdf
