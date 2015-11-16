.. _tested.polly:

Polls
=====

This document tests some functionality of the :mod:`lino.modlib.polls`
plugin using :ref:`polly`.

.. How to test only this document:

    $ python setup.py test -s tests.DocsTests.test_polly
    
    doctest init:

    >>> from __future__ import print_function
    >>> import os
    >>> os.environ['DJANGO_SETTINGS_MODULE'] = \
    ...    'lino.projects.polly.settings.doctests'
    >>> from lino.api.doctest import *
    
This document uses the :mod:`lino.projects.polly` test database:

>>> print(settings.SETTINGS_MODULE)
lino.projects.polly.settings.doctests

>>> pk = 2
>>> obj = polls.Response.objects.get(pk=pk)
>>> print(obj)
Rolf Rompen's response to Participant feedback

>>> rt.login(obj.user.username).show(polls.AnswersByResponse, obj)
Question 10/23/14 
<BLANKLINE>
1) There was enough to eat. **1** **2** **3** **4** **5** (**Remark**)
<BLANKLINE>
2) The stewards were nice and attentive. **1** **2** **3** **4** **5** (**Remark**)
<BLANKLINE>
3) The participation fee was worth the money. **1** **2** **3** **4** **5** (**Remark**)
<BLANKLINE>
4) Next time I will participate again. **1** **2** **3** **4** **5** (**Remark**)

>>> client = Client()
>>> mt = contenttypes.ContentType.objects.get_for_model(obj.__class__).id
>>> url = '/api/polls/AnswersByResponse?rp=ext-comp-1351&fmt=json&mt=%d&mk=%d' % (mt, pk)
>>> res = client.get(url, REMOTE_USER=obj.user.username)


>>> print(res.status_code)
200
>>> d = json.loads(res.content)

>>> len(d['rows'])
5

>>> print(d['rows'][0][0])
<span class="htmlText">1) There was enough to eat.</span>


The "My answer" column for the first row has 5 links:

>>> soup = BeautifulSoup(d['rows'][0][1], 'lxml')
>>> links = soup.find_all('a')
>>> len(links)
5

The first of them displays a "1":

>>> print(links[0].string)
... #doctest: +NORMALIZE_WHITESPACE
1

And clicking on it would run the following Javascript code:

>>> print(links[0].get('href'))
javascript:Lino.polls.Responses.toggle_choice("ext-comp-1351",2,{ "fv": [ 9, 17 ] })

The 2 is the id of the Response we are acting on:

>>> polls.Response.objects.get(pk=2)
Response #2 (u"Rolf Rompen's response to Participant feedback")


"fv" stands for "field values". 
It refers to the two `parameters` of the 
:class:`lino.modlib.polls.models.ToggleChoice` action.
The 9 is the id of a `polls.Question`, 
the 17 is the id of a `polls.Choice`.

>>> polls.Question.objects.get(pk=9)
Question #9 (u'1) There was enough to eat.')

>>> polls.Choice.objects.get(pk=17)
Choice #17 (u'1')


