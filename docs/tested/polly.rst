.. _tested.polly:

Polls
=====

.. include:: /include/tested.rst

.. How to test only this document:
  $ python setup.py test -s tests.DocsTests.test_polly

..  
    >>> from __future__ import print_function
    >>> import os
    >>> os.environ['DJANGO_SETTINGS_MODULE'] = \
    ...    'lino.projects.polly.settings.test'
    >>> from lino.runtime import *
    >>> from django.utils import translation
    >>> from django.test import Client
    >>> import json
    >>> from bs4 import BeautifulSoup

>>> print(settings.SETTINGS_MODULE)
lino.projects.polly.settings.test

>>> obj = polls.Response.objects.get(pk=1)
>>> print(obj)
Rando Roosi's response to Participant feedback

>>> rt.show(polls.AnswersByResponse, obj)
============================================ =============================== ===========
 Question                                     My answer                       My remark
-------------------------------------------- ------------------------------- -----------
 There was enough to eat.                     **1** **2** **3** **4** **5**
 The stewards were nice and attentive.        **1** **2** **3** **4** **5**
 The participation fee was worth the money.   **1** **2** **3** **4** **5**
 Next time I will participate again.          **1** **2** **3** **4** **5**
============================================ =============================== ===========
<BLANKLINE>


>>> client = Client()
>>> mt = contenttypes.ContentType.objects.get_for_model(obj.__class__).id
>>> url = '/api/polls/AnswersByResponse?rp=ext-comp-1351&fmt=json&mt=%d&mk=1' % mt
>>> res = client.get(url, REMOTE_USER='robin')

This returns a huge JSON structure:

>>> print(res.status_code)
200
>>> d = json.loads(res.content)

>>> len(d['rows'])
5

>>> print(d['rows'][0][0])
<p>There was enough to eat.</p>

>>> soup = BeautifulSoup(d['rows'][0][1])
>>> links = soup.find_all('a')
>>> len(links)
5

>>> print(links[0].string)
... #doctest: +NORMALIZE_WHITESPACE
1

>>> print(links[0].get('href'))
javascript:Lino.polls.Responses.toggle_choice("ext-comp-1351",1,{ "fv": [ 7, 17 ] })

