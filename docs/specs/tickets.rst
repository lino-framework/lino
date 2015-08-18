.. _noi.specs.tickets:

=================
Ticket management
=================


.. How to test only this document:

    $ python setup.py test -s tests.SpecsTests.test_tickets
    
    doctest init:

    >>> import os
    >>> os.environ['DJANGO_SETTINGS_MODULE'] = 'lino_noi.projects.team.settings.demo'
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
======= ========== ===========
 value   name       text
------- ---------- -----------
 10      new        New
 15      talk       Talk
 20      todo       Confirmed
 21      sticky     Sticky
 30      sleeping   Sleeping
 50      done       Done
 60      refused    Refused
======= ========== ===========
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
 linö        Framewörk
 téam        Téam
 docs        Documentatión
=========== =============== ======== ==============
<BLANKLINE>

Developers can start working on tickets without needing to know who is
going to pay for their work.  Every ticket should get assigned to some
project after some time, but You can see a list of tickets which have
not yet been assigned to a project:

>>> pv = dict(has_project=dd.YesNo.no)
>>> rt.show(tickets.Tickets, param_values=pv)
... #doctest: +REPORT_UDIFF
==== =================== ======== ========== ================= =========
 ID   Summary             Closed   Workflow   Reporter          Project
---- ------------------- -------- ---------- ----------------- ---------
 5    Cannot create Foo   No       **New**    Romain Raffault
 3    Baz sucks           No       **New**    luc
==== =================== ======== ========== ================= =========
<BLANKLINE>



Products
========

>>> rt.show(products.Products)
=========== ============== ================== ================== ==========
 Reference   Designation    Designation (de)   Designation (fr)   Category
----------- -------------- ------------------ ------------------ ----------
 linõ        Lino Core
 welfäre     Lino Welfare
 così        Lino Cosi
 faggiö      Lino Faggio
=========== ============== ================== ================== ==========
<BLANKLINE>
  

Sites
=====

We have a list of all sites for which we do support:

>>> rt.show(tickets.Sites)
============= ========= ======== ====
 Designation   Partner   Remark   ID
------------- --------- -------- ----
 pypi                             3
 welket                           1
 welsch                           2
============= ========= ======== ====
<BLANKLINE>


A ticket may or may not be **local**, i.e. assigned to a given
**Site**.

When a ticket is site-specific, we simply assign the `site` field. We
can see all local tickets for a given site object:

>>> welket = tickets.Site.objects.get(name="welket")
>>> rt.show(tickets.TicketsBySite, welket)
... #doctest: +REPORT_UDIFF
==== =========================================== ======== ========== ============= =========
 ID   Summary                                     Closed   Workflow   Reporter      Project
---- ------------------------------------------- -------- ---------- ------------- ---------
 16   How to get bar from foo                     No       **New**    marc          téam
 13   Bar cannot foo                              No       **New**    Rolf Rompen   téam
 10   Where can I find a Foo when bazing Bazes?   No       **New**    luc           téam
 7    No Foo after deleting Bar                   No       **New**    Robin Rood    téam
 4    Foo and bar don't baz                       No       **New**    jean          docs
 1    Föö fails to bar when baz                   No       **New**    mathieu       linö
==== =========================================== ======== ========== ============= =========
<BLANKLINE>

Note that the above table shows no state change actions in the
Workflow column because it is being requested by anonymous. For an
authenticated developer it looks like this:

>>> rt.login('jean').show(tickets.TicketsBySite, welket)
... #doctest: +REPORT_UDIFF
==== =========================================== ======== =========================================================================== ============= =========
 ID   Summary                                     Closed   Workflow                                                                    Reporter      Project
---- ------------------------------------------- -------- --------------------------------------------------------------------------- ------------- ---------
 16   How to get bar from foo                     No       **New** → [Sticky] [Talk] [Confirmed] [Sleeping] [Done] [Refused] [↗] [☆]   marc          téam
 13   Bar cannot foo                              No       **New** → [Sticky] [Talk] [Confirmed] [Sleeping] [Done] [Refused] [↗] [☆]   Rolf Rompen   téam
 10   Where can I find a Foo when bazing Bazes?   No       **New** → [Sticky] [Talk] [Confirmed] [Sleeping] [Done] [Refused] [↗] [☆]   luc           téam
 7    No Foo after deleting Bar                   No       **New** → [Sticky] [Talk] [Confirmed] [Sleeping] [Done] [Refused] [↗] [☆]   Robin Rood    téam
 4    Foo and bar don't baz                       No       **New** → [Sticky] [Talk] [Confirmed] [Sleeping] [Done] [Refused] [↗] [☆]   jean          docs
 1    Föö fails to bar when baz                   No       **New** → [Sticky] [Talk] [Confirmed] [Sleeping] [Done] [Refused] [↗] [☆]   mathieu       linö
==== =========================================== ======== =========================================================================== ============= =========
<BLANKLINE>


>>> welket = tickets.Site.objects.get(name="welket")
>>> rt.show(tickets.MilestonesBySite, welket)
... #doctest: +REPORT_UDIFF
==== ============== ========= =======
 ID   Expected for   Reached   Label
---- -------------- --------- -------
 7    5/15/15        5/15/15
 5    5/11/15        5/11/15
 3    5/7/15         5/7/15
 1    5/3/15         5/3/15
==== ============== ========= =======
<BLANKLINE>
