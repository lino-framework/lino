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
:ref:`noi`.

This variant provides readonly anonymous access to the data of
:mod:`lino_noi.projects.team` using the :mod:`lino_noi.lib.public`
user interface.

The :mod:`lino_noi.lib.public` user interface. is yet another way of
providing read-only anonymous access.  But it is experimental.  But
currently we recommend :ref:`noi.specs.bs3`


.. contents::
  :local:

Public tickets
==============

This is currently the only table publicly available.

The demo database contains the following data:

>>> rt.show(tickets.PublicTickets)
... #doctest: +REPORT_UDIFF
================================== ======= ============= ========= =========== ==========
 Overview                           State   Ticket type   Project   Topic       Priority
---------------------------------- ------- ------------- --------- ----------- ----------
 *#13 (Bar cannot foo)*             Done    Bugfix        linö      Lino Cosi   0
 *#1 (Föö fails to bar when baz)*   New     Bugfix        linö      Lino Cosi   0
================================== ======= ============= ========= =========== ==========
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
Home en de fr #13 (Bar cannot foo) State: Done  
<BLANKLINE>
<BLANKLINE>
(last update ...) Reported by: Rolf Rompen ... Topic: Lino Cosi Linking to [ticket 1] and to
 [url http://luc.lino-framework.org/blog/2015/0923.html blog]. This is Lino Noi 1.0.1 using Lino 1.7.0, Django 1.9.6, Python 2.7.6, Babel 2.2.0, Jinja 2.8, Sphinx 1.4a1, python-dateutil 2.5.2, OdfPy ODFPY/1.3.2, docutils 0.12, suds 0.4, PyYaml 3.11, Appy 0.9.2 (2015/04/30 15:00), Bootstrap 3.3.4, TinyMCE 3.5.11, Ext.ux.TinyMCE 0.8.4
