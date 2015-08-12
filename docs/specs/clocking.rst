.. _noi.specs.clocking:

==================
Work time tracking
==================

.. How to test only this document:

    $ python setup.py test -s tests.SpecsTests.test_clocking
    
    doctest init:

    >>> from __future__ import print_function, unicode_literals
    >>> import os
    >>> os.environ['DJANGO_SETTINGS_MODULE'] = 'lino_noi.settings.demo'
    >>> from lino.api.doctest import *


Lino Noi uses both :mod:`lino.modlib.tickets` (Ticket management) and
:mod:`lino.modlib.clocking` (Development time tracking).

Sessions
========

A :class:`Session <lino.modlib.clocking.models.Session>` is when a
user works on a ticket for a given lapse of time.

>>> rt.show(clocking.Sessions, limit=15)
... #doctest: +REPORT_UDIFF
=============================== ================= ============ ============ ========== ========== ============ ========= ===========
 Ticket                          Worker            Start date   Start time   End Date   End Time   Break Time   Summary   Duration
------------------------------- ----------------- ------------ ------------ ---------- ---------- ------------ --------- -----------
 #6 (Sell bar in baz)            jean              5/23/15      19:57:00     5/23/15    20:07:00                          0:10
 #8 (Is there any Bar in Foo?)   Romain Raffault   5/23/15      19:29:00     5/23/15    20:59:00                          1:30
 #2 (Bar is not always baz)      mathieu           5/23/15      18:41:00     5/23/15    19:18:00                          0:37
 #6 (Sell bar in baz)            jean              5/23/15      18:27:00     5/23/15    19:57:00                          1:30
 #9 (Foo never matches Bar)      Rolf Rompen       5/23/15      17:48:00     5/23/15    20:06:00                          2:18
 #9 (Foo never matches Bar)      Rolf Rompen       5/23/15      17:36:00     5/23/15    17:48:00                          0:12
 #9 (Foo never matches Bar)      Rolf Rompen       5/23/15      17:31:00     5/23/15    17:36:00                          0:05
 #8 (Is there any Bar in Foo?)   Romain Raffault   5/23/15      17:11:00     5/23/15    19:29:00                          2:18
 #5 (Cannot create Foo)          luc               5/23/15      17:08:00     5/23/15    19:10:00                          2:02
 #8 (Is there any Bar in Foo?)   Romain Raffault   5/23/15      16:59:00     5/23/15    17:11:00                          0:12
 #5 (Cannot create Foo)          luc               5/23/15      16:58:00     5/23/15    17:08:00                          0:10
 #8 (Is there any Bar in Foo?)   Romain Raffault   5/23/15      16:54:00     5/23/15    16:59:00                          0:05
 #6 (Sell bar in baz)            jean              5/23/15      16:09:00     5/23/15    18:27:00                          2:18
 #6 (Sell bar in baz)            jean              5/23/15      15:57:00     5/23/15    16:09:00                          0:12
 #6 (Sell bar in baz)            jean              5/23/15      15:52:00     5/23/15    15:57:00                          0:05
 **Total (126 rows)**                                                                                                     **13:44**
=============================== ================= ============ ============ ========== ========== ============ ========= ===========
<BLANKLINE>




Site interests
==============

Not every site is interested in everything. For example the site
`welket` is interested only in three products. We define this by
creating :class:`Interest
<lino.modlib.tickets.models.Interest>` objects:

>>> welket = tickets.Site.objects.get(name="welket")
>>> rt.show(tickets.InterestsBySite, welket)
... #doctest: +REPORT_UDIFF
==============
 Product
--------------
 Lino Core
 Lino Welfare
 Lino Cosi
==============
<BLANKLINE>

>>> rt.show(tickets.InterestsByProduct, products.Product.objects.get(ref="welfäre"))
... #doctest: +REPORT_UDIFF
========
 Site
--------
 welket
 welsch
========
<BLANKLINE>

Worked hours
============

>>> rt.login('rolf').show(clocking.WorkedHours)
... #doctest: +REPORT_UDIFF
==================== ====== =========== ====== ===========
 Description          dócs   linö        téam   Total
-------------------- ------ ----------- ------ -----------
 **Sat 5/23/15**             11:06              11:06
 **Fri 5/22/15**             11:49              11:49
 **Thu 5/21/15**
 **Wed 5/20/15**             10:10              10:10
 **Tue 5/19/15**
 **Mon 5/18/15**
 **Sun 5/17/15**
 **Total (7 rows)**          **33:05**          **33:05**
==================== ====== =========== ====== ===========
<BLANKLINE>




Service Report
==============

A service report (:class:`clocking.ServiceReport
<lino.modlib.clocking.ui.ServiceReport>`) is a document which reports
about the hours invested during a given date range.  It can be
addressed to a recipient (a user) and in that case will consider only
the tickets for which this user has specified interest.

It currently contains two tables:

- a list of tickets, with invested time (i.e. the sum of durations
  of all sessions that lie in the given data range)
- a list of projects, with invested time and list of the tickets that
  are assigned to this project.

This report will be a valuable help for developers like me because it
serves as a base for writing invoices.


>>> obj = clocking.ServiceReport.objects.get(pk=1)
>>> obj.printed_by.build_method
<BuildMethods.appyodt:appyodt>

>>> obj.interesting_for
Site #1 (u'welket')

>>> rt.show(clocking.TicketsByReport, obj)
... #doctest: +REPORT_UDIFF
==== ================================================================================================= ======= ============
 ID   Description                                                                                       State   Time
---- ------------------------------------------------------------------------------------------------- ------- ------------
 3    Baz sucks. Site: pypi. Reporter: luc. Product: Lino Core                                          New     32:41
 5    Cannot create Foo. Site: welsch. Reporter: Romain Raffault. Product: Lino Cosi                    New     33:35
 8    Is there any Bar in Foo?. Site: welsch. Reporter: mathieu. Project: dócs. Product: Lino Welfare   New     35:57
 9    Foo never matches Bar. Site: pypi. Reporter: marc. Project: linö. Product: Lino Cosi              New     33:05
                                                                                                                **135:18**
==== ================================================================================================= ======= ============
<BLANKLINE>

>>> rt.show(clocking.ProjectsByReport, obj)
==================== =============== ============ ============
 Reference            Name            Tickets      Time
-------------------- --------------- ------------ ------------
 dócs                 Documentatión   *#8*         35:57
 linö                 Framewörk       *#9*         33:05
                      (no project)    *#5*, *#3*   66:16
 **Total (3 rows)**                                **135:18**
==================== =============== ============ ============
<BLANKLINE>
