.. _noi.tested.clocking:

==================
Work time tracking
==================

.. How to test only this document:

    $ python setup.py test -s tests.SpecsTests.test_clocking
    
    doctest init:

    >>> import os
    >>> os.environ['DJANGO_SETTINGS_MODULE'] = 'lino_noi.settings.demo'
    >>> from __future__ import print_function 
    >>> from __future__ import unicode_literals
    >>> from lino.api.doctest import *


Lino Noi uses both :mod:`lino.modlib.tickets` (Ticket management) and
:mod:`lino.modlib.clocking` (Development time tracking).

Sessions
========

The 

>>> rt.show(clocking.Sessions)
... #doctest: +REPORT_UDIFF
================================ ======== ============ ============ ========== ========== ============ ========= ==========
 Ticket                           Worker   Start date   Start time   End Date   End Time   Break Time   Summary   Duration
-------------------------------- -------- ------------ ------------ ---------- ---------- ------------ --------- ----------
 #4 (Foo and bar don't baz)       jean     5/23/15      13:29:00     5/23/15    13:49:00                          0:20
 #3 (Baz sucks)                   luc      5/23/15      13:12:00     5/23/15    13:18:00                          0:06
 #1 (Foo fails to bar when baz)   luc      5/23/15      13:09:00     5/23/15    13:12:00                          0:03
 #2 (Bar is not always baz)       jean     5/23/15      13:09:00     5/23/15    13:29:00                          0:20
 #4 (Foo and bar don't baz)       jean     5/23/15      12:59:00     5/23/15    13:09:00                          0:10
 #5 (Cannot create Foo)           luc      5/23/15      12:49:00     5/23/15    13:09:00                          0:20
 #2 (Bar is not always baz)       jean     5/23/15      12:39:00     5/23/15    12:59:00                          0:20
 #3 (Baz sucks)                   luc      5/23/15      12:29:00     5/23/15    12:49:00                          0:20
 #4 (Foo and bar don't baz)       jean     5/23/15      12:26:00     5/23/15    12:39:00                          0:13
 #1 (Foo fails to bar when baz)   luc      5/23/15      12:19:00     5/23/15    12:29:00                          0:10
 #2 (Bar is not always baz)       jean     5/23/15      12:14:00     5/23/15    12:26:00                          0:12
 #4 (Foo and bar don't baz)       jean     5/23/15      12:09:00     5/23/15    12:14:00                          0:05
 #5 (Cannot create Foo)           luc      5/23/15      11:59:00     5/23/15    12:19:00                          0:20
 #3 (Baz sucks)                   luc      5/23/15      11:46:00     5/23/15    11:59:00                          0:13
 #2 (Bar is not always baz)       jean     5/23/15      11:46:00     5/23/15    12:09:00                          0:23
 #1 (Foo fails to bar when baz)   luc      5/23/15      11:34:00     5/23/15    11:46:00                          0:12
 #5 (Cannot create Foo)           luc      5/23/15      11:29:00     5/23/15    11:34:00                          0:05
 #4 (Foo and bar don't baz)       jean     5/23/15      11:29:00     5/23/15    11:46:00                          0:17
 #2 (Bar is not always baz)       jean     5/23/15      11:23:00     5/23/15    11:29:00                          0:06
 #4 (Foo and bar don't baz)       jean     5/23/15      11:20:00     5/23/15    11:23:00                          0:03
 #3 (Baz sucks)                   luc      5/23/15      11:06:00     5/23/15    11:29:00                          0:23
 #2 (Bar is not always baz)       jean     5/23/15      11:00:00     5/23/15    11:20:00                          0:20
 #1 (Foo fails to bar when baz)   luc      5/23/15      10:49:00     5/23/15    11:06:00                          0:17
 #5 (Cannot create Foo)           luc      5/23/15      10:43:00     5/23/15    10:49:00                          0:06
 #3 (Baz sucks)                   luc      5/23/15      10:40:00     5/23/15    10:43:00                          0:03
 #4 (Foo and bar don't baz)       jean     5/23/15      10:40:00     5/23/15    11:00:00                          0:20
 #2 (Bar is not always baz)       jean     5/23/15      10:30:00     5/23/15    10:40:00                          0:10
 #1 (Foo fails to bar when baz)   luc      5/23/15      10:20:00     5/23/15    10:40:00                          0:20
 #4 (Foo and bar don't baz)       jean     5/23/15      10:10:00     5/23/15    10:30:00                          0:20
 #5 (Cannot create Foo)           luc      5/23/15      10:00:00     5/23/15    10:20:00                          0:20
 #2 (Bar is not always baz)       jean     5/23/15      09:57:00     5/23/15    10:10:00                          0:13
 #3 (Baz sucks)                   luc      5/23/15      09:50:00     5/23/15    10:00:00                          0:10
 #4 (Foo and bar don't baz)       jean     5/23/15      09:45:00     5/23/15    09:57:00                          0:12
 #2 (Bar is not always baz)       jean     5/23/15      09:40:00     5/23/15    09:45:00                          0:05
 #1 (Foo fails to bar when baz)   luc      5/23/15      09:30:00     5/23/15    09:50:00                          0:20
 #5 (Cannot create Foo)           luc      5/23/15      09:17:00     5/23/15    09:30:00                          0:13
 #4 (Foo and bar don't baz)       jean     5/23/15      09:17:00     5/23/15    09:40:00                          0:23
 #3 (Baz sucks)                   luc      5/23/15      09:05:00     5/23/15    09:17:00                          0:12
 #1 (Foo fails to bar when baz)   luc      5/23/15      09:00:00     5/23/15    09:05:00                          0:05
 #2 (Bar is not always baz)       jean     5/23/15      09:00:00     5/23/15    09:17:00                          0:17
 **Total (40 rows)**                                                                                              **9:07**
================================ ======== ============ ============ ========== ========== ============ ========= ==========
<BLANKLINE>


- :class:`Session <lino.modlib.clocking.models.Session>`

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

>>> rt.show(tickets.InterestsByProduct, products.Product.objects.get(ref="welfare"))
... #doctest: +REPORT_UDIFF
========
 Site
--------
 welket
 welsch
========
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

>>> rt.show(clocking.ReportedTickets, obj)
=========================== ==== ============ ========= ============== ======== ======= ==========
 Summary                     ID   Reporter     Project   Product        Site     State   Time
--------------------------- ---- ------------ --------- -------------- -------- ------- ----------
 Foo fails to bar when baz   1    mathieu      lino      Lino Cosi      welket   New     1:27
 Baz sucks                   3    luc                    Lino Core               New     1:27
 Foo and bar don't baz       4    jean         docs      Lino Welfare            New     2:23
 Cannot create Foo           5    Robin Rood             Lino Cosi               New     1:24
 **Total (4 rows)**                                                                      **6:41**
=========================== ==== ============ ========= ============== ======== ======= ==========
<BLANKLINE>

>>> rt.show(clocking.ReportedProjects, obj)
==================== =============== ============ ==========
 Reference            Name            Tickets      Time
-------------------- --------------- ------------ ----------
 lino                 Framework       *#1*         1:27
 docs                 Documentation   *#4*         2:23
                      (no project)    *#3*, *#5*   2:51
 **Total (3 rows)**                                **6:41**
==================== =============== ============ ==========
<BLANKLINE>
