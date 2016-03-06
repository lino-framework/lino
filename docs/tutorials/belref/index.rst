.. _belref:
.. _lino.tutorial.belref:

======================
The ``belref`` project
======================

.. this document is part of the Lino test suite. To test only this
   document, run::

       $ python setup.py test -s tests.DocsTests.test_belref

   doctest init:

   >>> from __future__ import print_function
   >>> #import sys
   >>> #import codecs
   >>> #sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
   >>> from lino.api.doctest import *
   >>> from django.core.management import call_command
   >>> call_command('initdb', 'demo', interactive=False, verbosity=0)


.. contents::
   :local:


A way for publishing structured data
====================================

Lino Belref is a website with various structured information about
Belgium in three national languages.  An early prototype is running at
http://belref.lino-framework.org and is mentioned on our :ref:`demos`
page.

The primary goal of this project is to describe a way for storing,
maintaining and publishing certain kind of **structured data** about a
given topic.  The system would publish that data in many different
ways.

The `belref` project shows a dictionary with specific "Belgian"
vocabulary and a database of Belgian cities and other geographic
names. That choice is just illustrative and not a definitive
decision. There is also :mod:`lino.projects.estref`.

The data on such a site would be *stored* as :ref:`Python fixtures
<dpy>` which makes it possible to maintain the content using
established development tools for version control, issue tracking and
testing.  This mixture of data and source code is currently published
and maintained as part of Lino's repository in the
:mod:`lino.projects.belref` package.


Project status
==============

A side benefit of this project is to be our test field for the
:mod:`lino.modlib.bootstrap3` user interface.

The project itself grows very slowly because I know no single person
who believes that this might make sense (and even I wouldn't give my
hand for it).  See also :doc:`/topics/gpdn`.

The API
==============

The current implementation has only one HTTP API which is the JSON API
of :mod:`lino.modlib.extjs` 

>>> res = test_client.get("/api/concepts/Concepts?fmt=json&start=0&limit=100")
>>> res.status_code
200
>>> data = json.loads(res.content)
>>> data.keys()
[u'count', u'rows', u'success', u'no_data_text', u'title']
>>> data['count']
12
>>> data['rows'][0]
[u'Institut National de Statistique', u'Nationaal Instituut voor Statistiek', u'Nationales Institut f\xfcr Statistik', 1, u'INS', u'NIS', u'NIS', {u'id': True}, {u'delete_selected': True, u'insert': True}, True]


Get the list of places in Belgium:

>>> res = test_client.get("/api/countries/Places?fmt=json&start=0&limit=100")
>>> res.status_code
200
>>> data = json.loads(res.content)
>>> data['count']
78
>>> data['rows'][0]
[u'Belgique', u'BE', u'Aalst-bij-Sint-Truiden', u'', u'', u'70 (Village)', u'70', u'3800', u'Limbourg', 22, 23, u'', u'<span />', u'<a href="javascript:Lino.countries.Places.detail.run(null,{ &quot;record_id&quot;: 23 })">Aalst-bij-Sint-Truiden</a>', {u'id': True}, {u'delete_selected': True, u'insert': True, u'duplicate': True}, True]

The JSON API of :mod:`lino.modlib.extjs` is actually not written for
being public, that's why we have strange items like
``delete_selected`` which are used by the ExtJS user interface.

So a next step might be to write an XML-based API for publishing data
from a database, maybe SOAP or XML-RPC.

In a project like belref where data does not change very often, a
dynamic API would be overhead. So another step might be to write an
admin command which generates a set of static files to be published.
These static files can be XML, JSON or OpenDocument.  Maybe even some
proprietary format like `.xls`.

One application might be to write some Wikipedia pages with that data
and a `Wikipedia bot <https://en.wikipedia.org/wiki/Wikipedia:Bots>`_
which maintains them by accessing our API.


Yet another UnicodeDecodeError
==============================

A subtle and unrelated problem is the following:

>>> rt.show(countries.Places)
... #doctest: +NORMALIZE_WHITESPACE +SKIP

Above snippet fails because the test runner gets a UnicodeDecodeError
when trying to report the expected result::

    Traceback (most recent call last):
      File "/media/dell1tb/luc/work/lino/lino/utils/test.py", line 135, in test_files
        res = doctest.testfile(fn, **kwargs)
      File "/usr/lib/python2.7/doctest.py", line 2037, in testfile
        runner.run(test)
      File "/usr/lib/python2.7/doctest.py", line 1455, in run
        return self.__run(test, compileflags, out)
      File "/usr/lib/python2.7/doctest.py", line 1364, in __run
        self.report_failure(out, test, example, got)
      File "/usr/lib/python2.7/doctest.py", line 1229, in report_failure
        self._checker.output_difference(example, got, self.optionflags))
      File "/media/dell1tb/virtualenvs/py27/lib/python2.7/codecs.py", line 351, in write
        data, consumed = self.encode(object, self.errors)
    UnicodeDecodeError: 'ascii' codec can't decode byte 0xc3 in position 1413: ordinal not in range(128)


