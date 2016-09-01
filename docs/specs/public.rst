.. _noi.specs.public:

=================================================================
Experimental interface to Team using Bootstrap and self-made URLs
=================================================================

.. How to test only this document:

    $ python setup.py test -s tests.SpecsTests.test_public
    
    doctest init:

    >>> from lino import startup
    >>> startup('lino_noi.projects.public.settings.demo')
    >>> from lino.api.doctest import *

This document describes the :mod:`lino_noi.projects.public` variant of
:ref:`noi` which provides readonly anonymous access to the data of
:mod:`lino_noi.projects.team` using the :mod:`lino_noi.lib.public`
user interface.

The :mod:`lino_noi.lib.public` user interface is yet another way of
providing read-only anonymous access.  But it is experimental,
currently we recommend :ref:`noi.specs.bs3`


.. contents::
  :local:

Public tickets
==============

This is currently the only table publicly available.

The demo database contains the following data:

>>> rt.show(tickets.PublicTickets)
... #doctest: +REPORT_UDIFF
============================================= ========== ============= ========= =========== ==========
 Overview                                      State      Ticket type   Project   Topic       Priority
--------------------------------------------- ---------- ------------- --------- ----------- ----------
 `#13 (Bar cannot foo) <Detail>`__             Sleeping   Bugfix        linö      Lino Cosi   0
 `#1 (Föö fails to bar when baz) <Detail>`__   New        Bugfix        linö      Lino Cosi   0
============================================= ========== ============= ========= =========== ==========
<BLANKLINE>

The home page:

>>> res = test_client.get('/')
>>> res.status_code
200
>>> soup = BeautifulSoup(res.content)
>>> links = soup.find_all('a')
>>> len(links)
20
>>> print(links[0].get('href'))
/?ul=de
>>> print(links[1].get('href'))
/?ul=fr
>>> print(links[2].get('href'))
/ticket/13


>>> res = test_client.get('/ticket/13/')
>>> res.status_code
200
>>> soup = BeautifulSoup(res.content)
>>> print(soup.get_text(' ', strip=True))
... #doctest: +NORMALIZE_WHITESPACE +REPORT_UDIFF +ELLIPSIS
Home en de fr #13 Bar cannot foo State: Sleeping
<BLANKLINE>
<BLANKLINE>
(last update ...) Reported by: Rolf Rompen ... Topic: Lino Cosi Linking to [ticket 1] and to
 [url http://luc.lino-framework.org/blog/2015/0923.html blog]. This is Lino Noi ... using ...
