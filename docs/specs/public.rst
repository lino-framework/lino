.. _noi.specs.public:

==========================
Public read-only interface
==========================

.. How to test only this document:

    $ python setup.py test -s tests.SpecsTests.test_public
    
    doctest init:

    >>> from __future__ import print_function 
    >>> from __future__ import unicode_literals
    >>> import os
    >>> os.environ['DJANGO_SETTINGS_MODULE'] = 'lino_noi.projects.public.settings.demo'
    >>> from lino.api.doctest import *


This document specifies the read-only public interface of Lino Noi.
implemented in :mod:`lino_noi.projects.public`.


.. contents::
  :local:

Public tickets
==============

This is currently the only table publicly available.

The demo database contains the following data:

>>> rt.show(tickets.PublicTickets)
... #doctest: +REPORT_UDIFF
=================================================== ======= ============= ========= ============== ==========
 Overview                                            State   Ticket type   Project   Product        Priority
--------------------------------------------------- ------- ------------- --------- -------------- ----------
 *#16 (How to get bar from foo)*                     New     Bugfix        téam      Lino Welfare   0
 *#13 (Bar cannot foo)*                              New     Bugfix        téam      Lino Cosi      0
 *#10 (Where can I find a Foo when bazing Bazes?)*   New     Bugfix        téam      Lino Faggio    0
 *#7 (No Foo after deleting Bar)*                    New     Bugfix        téam      Lino Core      0
 *#4 (Foo and bar don't baz)*                        New     Bugfix        docs      Lino Welfare   0
 *#1 (Föö fails to bar when baz)*                    New     Bugfix        linö      Lino Cosi      0
=================================================== ======= ============= ========= ============== ==========
<BLANKLINE>

This data is being rendered using plain bootstrap HTML:

>>> res = test_client.get('/')
>>> res.status_code
200
>>> soup = BeautifulSoup(res.content)
>>> links = soup.find_all('a')
>>> len(links)
25
>>> print(links[0].get('href'))
/?ul=de
>>> print(links[1].get('href'))
/?ul=fr
>>> print(links[2].get('href'))
/ticket/16
>>> print(links[4].get('href'))
/ticket/10
>>> print(links[5].get('href'))
/ticket/7

>>> res = test_client.get('/ticket/7/')
>>> res.status_code
200
>>> soup = BeautifulSoup(res.content)
>>> print(soup.get_text(' ', strip=True))
... #doctest: +NORMALIZE_WHITESPACE +REPORT_CDIFF +ELLIPSIS
Home en de fr #7 (No Foo after deleting Bar) State: New  
<BLANKLINE>
<BLANKLINE>
(last update ...) Reported by: Robin Rood ... Product: Lino Core No dependencies. This is Lino Noi ...
