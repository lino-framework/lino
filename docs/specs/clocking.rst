.. _noi.specs.clocking:

==================
Work time tracking
==================

.. How to test only this document:

    $ python setup.py test -s tests.SpecsTests.test_clocking
    
    doctest init:

    >>> import os
    >>> os.environ['DJANGO_SETTINGS_MODULE'] = 'lino_noi.projects.team.settings.demo'
    >>> from lino.api.doctest import *


Lino Noi uses both :mod:`lino.modlib.tickets` (Ticket management) and
:mod:`lino.modlib.clocking` (Development time tracking).

Sessions
========

A :class:`Session <lino.modlib.clocking.models.Session>` is when a
user works on a ticket for a given lapse of time.

>>> rt.show(clocking.Sessions, limit=15)
... #doctest: +REPORT_UDIFF
================================== ================= ============ ============ ========== ========== ============ ========= ===========
 Ticket                             Worker            Start date   Start time   End Date   End Time   Break Time   Summary   Duration
---------------------------------- ----------------- ------------ ------------ ---------- ---------- ------------ --------- -----------
 #2 (Bar is not always baz)         jean              5/23/15      09:00:00     5/23/15    09:12:00                          0:12
 #3 (Baz sucks)                     luc               5/23/15      09:00:00     5/23/15    09:10:00                          0:10
 #5 (Cannot create Foo)             marc              5/23/15      09:00:00     5/23/15    09:37:00                          0:37
 #6 (Sell bar in baz)               mathieu           5/23/15      09:00:00     5/23/15    12:53:00                          3:53
 #8 (Is there any Bar in Foo?)      Romain Raffault   5/23/15      09:00:00     5/23/15    10:30:00                          1:30
 #9 (Foo never matches Bar)         Rolf Rompen       5/23/15      09:00:00     5/23/15    12:29:00                          3:29
 #11 (Class-based Foos and Bars?)   Robin Rood        5/23/15      09:00:00     5/23/15    11:59:00                          2:59
 #6 (Sell bar in baz)               mathieu           5/22/15      09:05:00     5/22/15    09:17:00                          0:12
 #12 (Foo cannot bar)               jean              5/22/15      09:00:00     5/22/15    11:18:00                          2:18
 #14 (Bar cannot baz)               luc               5/22/15      09:00:00     5/22/15    11:02:00                          2:02
 #15 (Bars have no foo)             marc              5/22/15      09:00:00     5/22/15    10:02:00                          1:02
 #6 (Sell bar in baz)               mathieu           5/22/15      09:00:00     5/22/15    09:05:00                          0:05
 #8 (Is there any Bar in Foo?)      Romain Raffault   5/22/15      09:00:00     5/22/15    09:10:00                          0:10
 #9 (Foo never matches Bar)         Rolf Rompen       5/22/15      09:00:00     5/22/15    09:37:00                          0:37
 #11 (Class-based Foos and Bars?)   Robin Rood        5/22/15      09:00:00     5/22/15    12:53:00                          3:53
 **Total (23 rows)**                                                                                                         **23:09**
================================== ================= ============ ============ ========== ========== ============ ========= ===========
<BLANKLINE>

Some sessions are on private tickets:

>>> from django.db.models import Q
>>> rt.show(clocking.Sessions, column_names="ticket user duration ticket__project", filter=Q(ticket__private=True))
... #doctest: +REPORT_UDIFF
============================ ======== ========== =========
 Ticket                       Worker   Duration   Project
---------------------------- -------- ---------- ---------
 #2 (Bar is not always baz)   jean     0:12       téam
 #3 (Baz sucks)               luc      0:10
 #5 (Cannot create Foo)       marc     0:37
 #2 (Bar is not always baz)   jean     1:30       téam
 #3 (Baz sucks)               luc      3:29
 #5 (Cannot create Foo)       marc     2:59
 **Total (6 rows)**                    **8:57**
============================ ======== ========== =========
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

This table shows the last seven days, one row per day, with your
woring hours based on your sessions.

In the "description" column you see a list of the tickets on which you
worked that day. This is a convenient way to continue some work you
started some days ago.

>>> rt.login('rolf').show(clocking.WorkedHours)
... #doctest: +REPORT_UDIFF
======================== ====== ========== ====== ==========
 Description              docs   linö       téam   Total
------------------------ ------ ---------- ------ ----------
 **Sat 5/23/15** (*#9*)          3:29              3:29
 **Fri 5/22/15** (*#9*)          0:37              0:37
 **Thu 5/21/15**                                   0:00
 **Wed 5/20/15** (*#9*)          1:02              1:02
 **Tue 5/19/15**                                   0:00
 **Mon 5/18/15**                                   0:00
 **Sun 5/17/15**                                   0:00
 **Total (7 rows)**              **5:08**          **5:08**
======================== ====== ========== ====== ==========
<BLANKLINE>

Users who worked on more than one project:

>>> for u in users.User.objects.all():
...     qs = tickets.Project.objects.filter(tickets_by_project__sessions_by_ticket__user=u).distinct()
...     if qs.count() > 1:
...         print u.username, "worked on", qs
jean worked on [Project #2 (u't\xe9am'), Project #1 (u'lin\xf6')]

Jean worked on more than one project:

>>> rt.login('jean').show(clocking.WorkedHours)
... #doctest: +REPORT_UDIFF
========================= ====== ========== ========== ==========
 Description               docs   linö       téam       Total
------------------------- ------ ---------- ---------- ----------
 **Sat 5/23/15** (*#2*)                      0:12       0:12
 **Fri 5/22/15** (*#12*)          2:18                  2:18
 **Thu 5/21/15**                                        0:00
 **Wed 5/20/15** (*#2*)                      1:30       1:30
 **Tue 5/19/15**                                        0:00
 **Mon 5/18/15**                                        0:00
 **Sun 5/17/15**                                        0:00
 **Total (7 rows)**               **2:18**   **1:42**   **4:00**
========================= ====== ========== ========== ==========
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

This report is useful for developers like me because it serves as a
base for writing invoices.


>>> obj = clocking.ServiceReport.objects.get(pk=1)
>>> obj.printed_by.build_method
<BuildMethods.appyodt:appyodt>

>>> obj.interesting_for
Site #1 (u'welket')

>>> rt.show(clocking.TicketsByReport, obj)
... #doctest: +REPORT_UDIFF
==== ================================================================================================ ======= ===========
 ID   Description                                                                                      State   Time
---- ------------------------------------------------------------------------------------------------ ------- -----------
 8    Is there any Bar in Foo?. Site: welsch. Reporter: jean. Project: docs. Product: Lino Welfare     New     3:42
 9    Foo never matches Bar. Site: pypi. Reporter: luc. Project: linö. Product: Lino Cosi              New     5:08
 11   Class-based Foos and Bars?. Site: welsch. Reporter: mathieu. Project: docs. Product: Lino Core   New     7:09
 12   Foo cannot bar. Site: pypi. Reporter: Romain Raffault. Project: linö. Product: Lino Welfare      New     2:18
 15   Bars have no foo. Site: pypi. Reporter: jean. Project: linö. Product: Lino Core                  New     1:02
                                                                                                               **19:19**
==== ================================================================================================ ======= ===========
<BLANKLINE>

>>> rt.show(clocking.ProjectsByReport, obj)
==================== =============== ==================== ===========
 Reference            Name            Tickets              Time
-------------------- --------------- -------------------- -----------
 docs                 Documentatión   *#11*, *#8*          10:51
 linö                 Framewörk       *#15*, *#12*, *#9*   8:28
 **Total (2 rows)**                                        **19:19**
==================== =============== ==================== ===========
<BLANKLINE>
