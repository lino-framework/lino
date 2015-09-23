.. _noi.specs.clocking:

==================
Work time tracking
==================

.. How to test only this document:

    $ python setup.py test -s tests.SpecsTests.test_clocking
    
    doctest init:

    >>> import os
    >>> os.environ['DJANGO_SETTINGS_MODULE'] = 'lino_noi.projects.team.settings.doctests'
    >>> from lino.api.doctest import *


Lino Noi uses both :mod:`lino_noi.lib.tickets` (Ticket management) and
:mod:`lino_noi.lib.clocking` (Development time tracking).

Sessions
========

A :class:`Session <lino_noi.lib.clocking.models.Session>` is when a
user works on a ticket for a given lapse of time.

>>> rt.show(clocking.Sessions, limit=15)
... #doctest: +REPORT_UDIFF
================================================= ========= ============ ============ ========== ========== ============ ========= ===========
 Ticket                                            Worker    Start date   Start time   End Date   End Time   Break Time   Summary   Duration
------------------------------------------------- --------- ------------ ------------ ---------- ---------- ------------ --------- -----------
 #2 (Bar is not always baz)                        jean      5/23/15      09:00:00     5/23/15    09:12:00                          0:12
 #3 (Baz sucks)                                    luc       5/23/15      09:00:00     5/23/15    09:10:00                          0:10
 #4 (Foo and bar don't baz)                        marc      5/23/15      09:00:00     5/23/15    09:37:00                          0:37
 #6 (Sell bar in baz)                              mathieu   5/23/15      09:00:00     5/23/15    12:53:00                          3:53
 #16 (How to get bar from foo)                     mathieu   5/22/15      09:05:00     5/22/15    09:17:00                          0:12
 #7 (No Foo after deleting Bar)                    jean      5/22/15      09:00:00     5/22/15    11:18:00                          2:18
 #8 (Is there any Bar in Foo?)                     luc       5/22/15      09:00:00     5/22/15    11:02:00                          2:02
 #10 (Where can I find a Foo when bazing Bazes?)   marc      5/22/15      09:00:00     5/22/15    10:02:00                          1:02
 #11 (Class-based Foos and Bars?)                  mathieu   5/22/15      09:00:00     5/22/15    09:05:00                          0:05
 #12 (Foo cannot bar)                              jean      5/20/15      09:00:00     5/20/15    10:30:00                          1:30
 #14 (Bar cannot baz)                              luc       5/20/15      09:00:00     5/20/15    12:29:00                          3:29
 #15 (Bars have no foo)                            marc      5/20/15      09:00:00     5/20/15    11:59:00                          2:59
 #6 (Sell bar in baz)                              mathieu   5/20/15      09:00:00     5/20/15    11:18:00                          2:18
 **Total (13 rows)**                                                                                                                **20:47**
================================================= ========= ============ ============ ========== ========== ============ ========= ===========
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
 #14 (Bar cannot baz)         luc      3:29       téam
 **Total (3 rows)**                    **3:51**
============================ ======== ========== =========
<BLANKLINE>


Site interests
==============

Not every site is interested in everything. For example the site
`welket` is interested only in three products. We define this by
creating :class:`Interest
<lino_noi.lib.tickets.models.Interest>` objects:

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
working hours based on your sessions.

>>> rt.login('jean').show(clocking.WorkedHours)
... #doctest: +REPORT_UDIFF
========================= ====== ====== ========== ========== ========== ==========
 Description               docs   linö   research   shop       téam       Total
------------------------- ------ ------ ---------- ---------- ---------- ----------
 **Sat 5/23/15** (*#2*)                                        0:12       0:12
 **Fri 5/22/15** (*#7*)                             2:18                  2:18
 **Thu 5/21/15**                                                          0:00
 **Wed 5/20/15** (*#12*)                            1:30                  1:30
 **Tue 5/19/15**                                                          0:00
 **Mon 5/18/15**                                                          0:00
 **Sun 5/17/15**                                                          0:00
 **Total (7 rows)**                                 **3:48**   **0:12**   **4:00**
========================= ====== ====== ========== ========== ========== ==========
<BLANKLINE>


In the "description" column you see a list of the tickets on which you
worked that day. This is a convenient way to continue some work you
started some days ago.

.. 
    Find the users who worked on more than one project:
    >>> for u in users.User.objects.all():
    ...     qs = tickets.Project.objects.filter(tickets_by_project__sessions_by_ticket__user=u).distinct()
    ...     if qs.count() > 1:
    ...         print u.username, "worked on", qs
    jean worked on [Project #2 (u't\xe9am'), Project #5 (u'shop')]
    luc worked on [Project #1 (u'lin\xf6'), Project #2 (u't\xe9am')]

Render this table to HTML in order to reproduce :ticket:`523`:

>>> url = "/api/clocking/WorkedHours?"
>>> url += "_dc=1442341081053&cw=430&cw=83&cw=83&cw=83&cw=83&cw=83&cw=83&ch=&ch=&ch=&ch=&ch=&ch=&ch=&ci=description&ci=vc0&ci=vc1&ci=vc2&ci=vc3&ci=vc4&ci=vc5&name=0&pv=16.05.2015&pv=23.05.2015&pv=7&an=show_as_html&sr="
>>> res = test_client.get(url, REMOTE_USER="jean")
>>> json.loads(res.content)
{u'open_url': u'/bs3/clocking/WorkedHours?limit=15', u'success': True}

.. Also interesting:

    >>> ar = rt.login('jean')
    >>> u = ar.get_user()
    >>> ar = clocking.WorkedHours.request(user=u)
    >>> ar = ar.spawn(clocking.WorkedHours)
    >>> lst = list(ar)
    >>> len(lst)
    7
    >>> e = ar.table2xhtml()

The html table has only 4 rows (3 data rows and the total row) because
valueless rows are not included by default:

>>> len(e.findall('./tbody/tr'))
4




Service Report
==============

A service report (:class:`clocking.ServiceReport
<lino_noi.lib.clocking.ui.ServiceReport>`) is a document which reports
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
... #doctest: -REPORT_UDIFF
==== ============================================================================================================== ======= ===========
 ID   Description                                                                                                    State   Time
---- -------------------------------------------------------------------------------------------------------------- ------- -----------
 4    Foo and bar don't baz. Site: welket. Reporter: mathieu. Project: docs. Product: Lino Welfare                   New     0:37
 7    No Foo after deleting Bar. Site: welket. Reporter: Robin Rood. Project: shop. Product: Lino Core               New     2:18
 8    Is there any Bar in Foo?. Site: welsch. Reporter: jean. Project: linö. Product: Lino Welfare                   New     2:02
 10   Where can I find a Foo when bazing Bazes?. Site: welket. Reporter: marc. Project: docs. Product: Lino Faggio   New     1:02
 11   Class-based Foos and Bars?. Site: welsch. Reporter: mathieu. Project: research. Product: Lino Core             New     0:05
 12   Foo cannot bar. Site: pypi. Reporter: Romain Raffault. Project: shop. Product: Lino Welfare                    New     1:30
 15   Bars have no foo. Site: pypi. Reporter: jean. Project: docs. Product: Lino Core                                New     2:59
 16   How to get bar from foo. Site: welket. Reporter: luc. Project: research. Product: Lino Welfare                 New     0:12
                                                                                                                             **10:45**
==== ============================================================================================================== ======= ===========
<BLANKLINE>


>>> rt.show(clocking.ProjectsByReport, obj)
==================== =============== ==================== ===========
 Reference            Name            Tickets              Time
-------------------- --------------- -------------------- -----------
 docs                 Documentatión   *#15*, *#10*, *#4*   4:38
 linö                 Framewörk       *#8*                 2:02
 research             Research        *#16*, *#11*         0:17
 shop                 Shop            *#12*, *#7*          3:48
 **Total (4 rows)**                                        **10:45**
==================== =============== ==================== ===========
<BLANKLINE>
