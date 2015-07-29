.. _noi.tested.tickets:

=================
Ticket management
=================


.. How to test only this document:

    $ python setup.py test -s tests.SpecsTests.test_tickets
    
    doctest init:

    >>> import os
    >>> os.environ['DJANGO_SETTINGS_MODULE'] = 'lino_noi.settings.demo'
    >>> from __future__ import print_function 
    >>> from __future__ import unicode_literals
    >>> from lino.api.doctest import *


This document specifies the ticket management functions of Lino Noi,
implemented in :mod:`lino.modlib.tickets`.


.. contents::
  :local:


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

The :attr:`state <lino.modlib.tickets.models.Ticket.state>` of a
ticket has one of the following values:

>>> rt.show(tickets.TicketStates)
======= ========= =========
 value   name      text
------- --------- ---------
 10      new       New
 15      talk      Talk
 20      todo      To do
 21      sticky    Sticky
 50      done      Done
 60      refused   Refused
======= ========= =========
<BLANKLINE>

See :class:`lino.modlib.tickets.choicelists.TicketStates` for an
overview of these.

Note that a ticket also has a checkbox for marking it as :attr:`closed
<lino.modlib.tickets.models.Ticket.closed>`.  This means that a ticket
can be marked as "closed" in any of above states.  We are not sure
whether this is a cool feature (#372).

- :attr:`standby <lino.modlib.tickets.models.Ticket.standby>` 


Projects
========

A **project** is something for which somebody is possibly willing to
pay money.

>>> rt.show(tickets.Projects)
=========== =============== ======== ==============
 Reference   Name            Parent   Project Type
----------- --------------- -------- --------------
 lino        Framework
 team        Team
 docs        Documentation
=========== =============== ======== ==============
<BLANKLINE>

Developers can start working on tickets without needing to know who is
going to pay for their work.  Every ticket should get assigned to some
project after some time, but You can see a list of tickets which have
not yet been assigned to a project:

>>> pv = dict(has_project=dd.YesNo.no)
>>> rt.show(tickets.Tickets, param_values=pv)
... #doctest: +REPORT_UDIFF
==== =================== ======== ========== ============ =========
 ID   Summary             Closed   Workflow   Reporter     Project
---- ------------------- -------- ---------- ------------ ---------
 5    Cannot create Foo   No       **New**    Robin Rood
 3    Baz sucks           No       **New**    luc
==== =================== ======== ========== ============ =========
<BLANKLINE>



Products
========

>>> rt.show(products.Products)
=========== ============== ==========
 Reference   Designation    Category
----------- -------------- ----------
 lino        Lino Core
 welfare     Lino Welfare
 cosi        Lino Cosi
 faggio      Lino Faggio
=========== ============== ==========
<BLANKLINE>
  

Sites
=====

We have a list of all sites for which we do support:

>>> rt.show(tickets.Sites)
============= ========= ======== ====
 Designation   Partner   Remark   ID
------------- --------- -------- ----
 welket                           1
 welsch                           2
============= ========= ======== ====
<BLANKLINE>


A ticket may or may not be **local**, i.e. specific to a given
**Site**. Local tickets are never interesting to other sites even when
they are assigned a product for which the other site has interest.

When a ticket is site-specific, we simply assign the `site` field. We
can see all local tickets for a given site object:

>>> welket = tickets.Site.objects.get(name="welket")
>>> rt.show(tickets.TicketsBySite, welket)
... #doctest: +REPORT_UDIFF
==== =========================== ======== ========== ========== =========
 ID   Summary                     Closed   Workflow   Reporter   Project
---- --------------------------- -------- ---------- ---------- ---------
 1    Foo fails to bar when baz   No       **New**    mathieu    lino
==== =========================== ======== ========== ========== =========
<BLANKLINE>

Note that the above table shows no state change actions in the
Workflow column because it is being requested by anonymous. For an
authenticated developer it looks like this:

>>> rt.login('jean').show(tickets.TicketsBySite, welket)
... #doctest: +REPORT_UDIFF
==== =========================== ======== ======================================================= ========== =========
 ID   Summary                     Closed   Workflow                                                Reporter   Project
---- --------------------------- -------- ------------------------------------------------------- ---------- ---------
 1    Foo fails to bar when baz   No       **New** → [Talk] [To do] [Done] [Refused] [↗] [⚇] [☆]   mathieu    lino
==== =========================== ======== ======================================================= ========== =========
<BLANKLINE>




