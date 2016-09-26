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
============================================= ========== ============= ========== =========== ==========
 Overview                                      State      Ticket type   Project    Topic       Priority
--------------------------------------------- ---------- ------------- ---------- ----------- ----------
 `#113 (Ticket 96) <Detail>`__                 New        Enhancement   linö       Lino Cosi   100
 `#105 (Ticket 88) <Detail>`__                 New        Upgrade       docs       Lino Cosi   100
 `#101 (Ticket 84) <Detail>`__                 Sleeping   Enhancement   research   Lino Cosi   100
 `#97 (Ticket 80) <Detail>`__                  New        Bugfix        shop       Lino Cosi   100
 `#93 (Ticket 76) <Detail>`__                  Sleeping   Upgrade       linö       Lino Cosi   100
 `#85 (Ticket 68) <Detail>`__                  Sleeping   Bugfix        docs       Lino Cosi   100
 `#81 (Ticket 64) <Detail>`__                  New        Upgrade       research   Lino Cosi   100
 `#77 (Ticket 60) <Detail>`__                  Sleeping   Enhancement   shop       Lino Cosi   100
 `#73 (Ticket 56) <Detail>`__                  New        Bugfix        linö       Lino Cosi   100
 `#65 (Ticket 48) <Detail>`__                  New        Enhancement   docs       Lino Cosi   100
 `#61 (Ticket 44) <Detail>`__                  Sleeping   Bugfix        research   Lino Cosi   100
 `#57 (Ticket 40) <Detail>`__                  New        Upgrade       shop       Lino Cosi   100
 `#53 (Ticket 36) <Detail>`__                  Sleeping   Enhancement   linö       Lino Cosi   100
 `#45 (Ticket 28) <Detail>`__                  Sleeping   Upgrade       docs       Lino Cosi   100
 `#41 (Ticket 24) <Detail>`__                  New        Enhancement   research   Lino Cosi   100
 `#37 (Ticket 20) <Detail>`__                  Sleeping   Bugfix        shop       Lino Cosi   100
 `#33 (Ticket 16) <Detail>`__                  New        Upgrade       linö       Lino Cosi   100
 `#25 (Ticket 8) <Detail>`__                   New        Bugfix        docs       Lino Cosi   100
 `#21 (Ticket 4) <Detail>`__                   Sleeping   Upgrade       research   Lino Cosi   100
 `#17 (Ticket 0) <Detail>`__                   New        Enhancement   shop       Lino Cosi   100
 `#13 (Bar cannot foo) <Detail>`__             Sleeping   Bugfix        linö       Lino Cosi   100
 `#1 (Föö fails to bar when baz) <Detail>`__   New        Bugfix        linö       Lino Cosi   100
 **Total (22 rows)**                                                                           **2200**
============================================= ========== ============= ========== =========== ==========
<BLANKLINE>

The home page:

>>> res = test_client.get('/')
>>> res.status_code
200
>>> soup = BeautifulSoup(res.content, 'lxml')
>>> links = soup.find_all('a')
>>> len(links)
40
>>> print(links[0].get('href'))
/?ul=de
>>> print(links[1].get('href'))
/?ul=fr
>>> print(links[2].get('href'))
/ticket/113


>>> res = test_client.get('/ticket/13/')
>>> res.status_code
200
>>> soup = BeautifulSoup(res.content, 'lxml')
>>> print(soup.get_text(' ', strip=True))
... #doctest: +NORMALIZE_WHITESPACE +REPORT_UDIFF +ELLIPSIS
Home en de fr #13 Bar cannot foo State: Sleeping
<BLANKLINE>
<BLANKLINE>
(last update ...) Reported by: Rolf Rompen ... Topic: Lino Cosi Linking to [ticket 1] and to
 [url http://luc.lino-framework.org/blog/2015/0923.html blog]. This is Lino Noi ... using ...
