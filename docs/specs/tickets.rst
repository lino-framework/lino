.. _noi.tested.tickets:

========================================
Ticket management and work time tracking
========================================

.. How to test only this document:

  $ python setup.py test -s tests.SpecsTests.test_tickets

Lino Noi uses both :mod:`lino.modlib.tickets` (Ticket management) and
:mod:`lino.modlib.clocking` (Development time tracking).

The goal of these modules is managing tickets (problems reported by
customers or other users) and registering the time needed by
developers (or other users) to work on these tickets. It is then
possible to publish diverse work reports.


.. contents::
  :local:

A tested document
=================

.. include:: /include/tested.rst

>>> import os
>>> os.environ['DJANGO_SETTINGS_MODULE'] = 'lino_noi.settings.demo'
>>> from __future__ import print_function 
>>> from __future__ import unicode_literals
>>> from lino.api.doctest import *

>>> ses = rt.login("robin")


Tickets versus Clocking
=======================

Note that :mod:`lino.modlib.clocking` depends on
:mod:`lino.modlib.tickets` and not vice-versa.  A time tracking system
makes no sense if you don't have a ticketing system.  Lino Noi uses
them both, but some other applicaton might use only :mod:`tickets
<lino.modlib.tickets>` without wanting to manage :mod:`clocking
<lino.modlib.clocking>`.

>>> dd.plugins.clocking.needs_plugins
['lino.modlib.tickets']
>>> dd.plugins.tickets.needs_plugins
[]

See also :attr:`needs_plugin <lino.core.plugin.Plugin.needs_plugin>`.


User profiles
=============

A default Lino Noi site has the following user profiles:

>>> ses.show(users.UserProfiles)
======= ============ ===============
 value   name         text
------- ------------ ---------------
 000     anonymous    Anonymous
 100     user         User
 200     consultant   Consultant
 300     hoster       Hoster
 400     developer    Developer
 490     senior       Senior
 900     admin        Administrator
======= ============ ===============
<BLANKLINE>


A **user** is somebody who uses some part of the software being
developed by the team. This is usually the contact person of a
customer.

A **consultant** is an intermediate agent between end-users and the
team.

A **hoster** is a special kind of customer who installs and maintains
servers where Lino applications run.

A **developer** is somebody who works on tickets by doing code
changes.

A **senior** is a developer who additionaly can triage tickets.

Tickets
=======

A :class:`Ticket <lino.modlib.tickets.models.Ticket>` represents a
concrete problem introduced by a 
:attr:`reporter <lino.modlib.tickets.models.Ticket.reporter>` 
(usually a customer).

A ticket is usually assigned to one and only one user
(:attr:`assigned_to <lino.modlib.tickets.models.Ticket.assigned_to>`)
who is expected to work on it. That user might be the customer,
e.g. when the developer has a question.

The :attr:`project <lino.modlib.tickets.models.Ticket.project>` of a
ticket is used to specify "who is going to pay" for it. Lino Noi does
not issue invoices, so it uses this information only for reporting
about it and helping with the decision about whether and how worktime
is being invoiced to the customer.  But the invoicing itself is not
curently goal of Lino Noi.

The :attr:`product <lino.modlib.tickets.models.Ticket.product>` is
what Trac calls "component". Products are "customer-side
classification" of the different components which are being developed
by the team that uses a given Lino Noi site.

Lifecycle of a ticket
=====================

The :attr:`state <lino.modlib.tickets.models.Ticket.state>` of a ticket

>>> ses.show(tickets.TicketStates)
======= ========= =========
 value   name      text
------- --------- ---------
 10      new       New
 20      todo      To do
 21      sticky    Sticky
 50      done      Done
 60      refused   Refused
======= ========= =========
<BLANKLINE>


When a ticket has been marked as :attr:`closed <lino.modlib.tickets.models.Ticket.closed>`.

- :attr:`standby <lino.modlib.tickets.models.Ticket.standby>` 


Projects
========

>>> ses.show(tickets.Projects)
=========== ============ ======== ==============
 Reference   Name         Parent   Project Type
----------- ------------ -------- --------------
             Eupen
             Raeren
             Bütgenbach
=========== ============ ======== ==============
<BLANKLINE>


Products
========

>>> ses.show(products.Products)
=========== ============== ==========
 Reference   Designation    Category
----------- -------------- ----------
             Lino Core
             Lino Welfare
             Lino Cosi
             Lino Faggio
=========== ============== ==========
<BLANKLINE>
  
- :class:`Session <lino.modlib.clocking.models.Session>`

Sessions
========

The 

>>> ses.show(clocking.Sessions)
... #doctest: +REPORT_UDIFF
================================ ============ ============ ============ ========== ========== ============ ========= ==========
 Ticket                           Author       Start date   Start time   End Date   End Time   Break Time   Summary   Duration
-------------------------------- ------------ ------------ ------------ ---------- ---------- ------------ --------- ----------
 #5 (Cannot create Foo)           Robin Rood   5/23/15      13:12:00     5/23/15    13:18:00                          0:06
 #4 (Foo and bar don't baz)       jean         5/23/15      13:09:00     5/23/15    13:12:00                          0:03
 #3 (Baz sucks)                   luc          5/23/15      12:49:00     5/23/15    13:09:00                          0:20
 #2 (Bar is not always baz)       marc         5/23/15      12:29:00     5/23/15    12:49:00                          0:20
 #1 (Foo fails to bar when baz)   mathieu      5/23/15      12:19:00     5/23/15    12:29:00                          0:10
 #5 (Cannot create Foo)           Robin Rood   5/23/15      11:59:00     5/23/15    12:19:00                          0:20
 #4 (Foo and bar don't baz)       jean         5/23/15      11:46:00     5/23/15    11:59:00                          0:13
 #3 (Baz sucks)                   luc          5/23/15      11:34:00     5/23/15    11:46:00                          0:12
 #2 (Bar is not always baz)       marc         5/23/15      11:29:00     5/23/15    11:34:00                          0:05
 #1 (Foo fails to bar when baz)   mathieu      5/23/15      11:06:00     5/23/15    11:29:00                          0:23
 #5 (Cannot create Foo)           Robin Rood   5/23/15      10:49:00     5/23/15    11:06:00                          0:17
 #4 (Foo and bar don't baz)       jean         5/23/15      10:43:00     5/23/15    10:49:00                          0:06
 #3 (Baz sucks)                   luc          5/23/15      10:40:00     5/23/15    10:43:00                          0:03
 #2 (Bar is not always baz)       marc         5/23/15      10:20:00     5/23/15    10:40:00                          0:20
 #1 (Foo fails to bar when baz)   mathieu      5/23/15      10:00:00     5/23/15    10:20:00                          0:20
 #5 (Cannot create Foo)           Robin Rood   5/23/15      09:50:00     5/23/15    10:00:00                          0:10
 #4 (Foo and bar don't baz)       jean         5/23/15      09:30:00     5/23/15    09:50:00                          0:20
 #3 (Baz sucks)                   luc          5/23/15      09:17:00     5/23/15    09:30:00                          0:13
 #2 (Bar is not always baz)       marc         5/23/15      09:05:00     5/23/15    09:17:00                          0:12
 #1 (Foo fails to bar when baz)   mathieu      5/23/15      09:00:00     5/23/15    09:05:00                          0:05
 **Total (20 rows)**                                                                                                  **4:18**
================================ ============ ============ ============ ========== ========== ============ ========= ==========
<BLANKLINE>
