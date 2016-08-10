.. _noi.specs.bs3:

=====================================================
A read-only interface to Team using generic Bootstrap
=====================================================

.. How to test only this document:

    $ python setup.py test -s tests.SpecsTests.test_bs3
    
    doctest init:

    >>> from lino import startup
    >>> startup('lino_noi.projects.bs3.settings.demo')
    >>> from lino.api.doctest import *


This document specifies the read-only public interface of Lino Noi.
implemented in :mod:`lino_noi.projects.bs3`.

Provides readonly anonymous access to the data of
:mod:`lino_noi.projects.team`, using the :mod:`lino.modlib.bootstrap3`
user interface. See also :mod:`lino_noi.projects.public`

This does not use :mod:`lino.modlib.extjs` at all.


.. contents::
  :local:

.. The following was used to reproduce :ticket:`960`:

    >>> res = test_client.get('/tickets/Ticket/13')
    >>> res.status_code
    200



Unassigned tickets
==================


The demo database contains the following data:

>>> rt.show(tickets.PublicTickets)
... #doctest: -REPORT_UDIFF
================================== ========== ============= ========= =========== ==========
 Overview                           State      Ticket type   Project   Topic       Priority
---------------------------------- ---------- ------------- --------- ----------- ----------
 *#13 (Bar cannot foo)*             Sleeping   Bugfix        linö      Lino Cosi   0
 *#1 (Föö fails to bar when baz)*   New        Bugfix        linö      Lino Cosi   0
================================== ========== ============= ========= =========== ==========
<BLANKLINE>


This data is being rendered using plain bootstrap HTML:

>>> res = test_client.get('/')
>>> res.status_code
200
>>> soup = BeautifulSoup(res.content)
>>> links = soup.find_all('a')
>>> len(links)
29
>>> print(links[0].get('href'))
/?ul=de
>>> print(links[1].get('href'))
/?ul=fr
>>> print(links[2].get('href'))
#

>>> res = test_client.get('/tickets/Ticket/13')
>>> res.status_code
200
>>> soup = BeautifulSoup(res.content)


>>> links = soup.find_all('a')
>>> len(links)
31
>>> print(links[0].get('href'))
/?ul=en

>>> print(soup.get_text(' ', strip=True))
... #doctest: +NORMALIZE_WHITESPACE +REPORT_UDIFF +ELLIPSIS
Tickets Home en de fr Tickets Active tickets Tickets Unassigned Tickets Site About #13 (Bar cannot foo) << < > >> State: Sleeping
<BLANKLINE>
<BLANKLINE>
(last update ...) Reported by: Rolf Rompen ... Topic: Lino Cosi Site: welket Linking to #1 and to blog . This is Lino Noi ... using ...
