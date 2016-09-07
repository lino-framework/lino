.. _noi.specs.tickets:

=============================
Ticket management in Lino Noi
=============================


.. How to test only this document:

    $ python setup.py test -s tests.SpecsTests.test_tickets
    
    doctest init:

    >>> import lino
    >>> lino.startup('lino_noi.projects.team.settings.demo')
    >>> from lino.api.doctest import *


This document specifies the ticket management functions of Lino Noi,
implemented in :mod:`lino_noi.lib.tickets`.


.. contents::
  :local:


Tickets
=======

A :class:`Ticket <lino_noi.lib.tickets.models.Ticket>` represents a
concrete problem introduced by a :attr:`reporter
<lino_noi.lib.tickets.models.Ticket.reporter>` (a system user).

A ticket is usually *assigned* to one and only one user
(:attr:`assigned_to <lino_noi.lib.tickets.models.Ticket.assigned_to>`)
who is expected to work on it. That user might be the customer,
e.g. when the developer has a question.

Lifecycle of a ticket
=====================

The :attr:`state <lino_noi.lib.tickets.models.Ticket.state>` of a
ticket has one of the following values:

>>> rt.show(tickets.TicketStates)
======= =========== =========== ======== ========
 value   name        text        Symbol   Active
------- ----------- ----------- -------- --------
 10      new         New         📥        No
 15      talk        Talk        🗪        Yes
 20      todo        ToDo        🐜        Yes
 21      sticky      Sticky      📌        No
 30      sleeping    Sleeping    🕸        No
 40      ready       Ready       ☐        Yes
 50      done        Done        ☑        No
 60      cancelled   Cancelled   🗑        No
======= =========== =========== ======== ========
<BLANKLINE>

You can see this table in your web interface using
:menuselection:`Explorer --> Tickets --> States`.

.. >>> show_menu_path(tickets.TicketStates)
   Explorer --> Tickets --> States

See :class:`lino_noi.lib.tickets.choicelists.TicketStates` for more
information about every state.

Above table in German:

>>> rt.show(tickets.TicketStates, language="de")
====== =========== ============ ======== ========
 Wert   name        Text         Symbol   Aktive
------ ----------- ------------ -------- --------
 10     new         Neu          📥        Nein
 15     talk        Besprechen   🗪        Ja
 20     todo        ZuTun        🐜        Ja
 21     sticky      Sticky       📌        Nein
 30     sleeping    Schläft      🕸        Nein
 40     ready       Bereit       ☐        Ja
 50     done        Erledigt     ☑        Nein
 60     cancelled   Storniert    🗑        Nein
====== =========== ============ ======== ========
<BLANKLINE>

And in French (not yet fully translated):

>>> rt.show(tickets.TicketStates, language="fr")
======= =========== =========== ======== ========
 value   name        text        Symbol   Active
------- ----------- ----------- -------- --------
 10      new         Nouveau     📥        Non
 15      talk        Talk        🗪        Oui
 20      todo        ToDo        🐜        Oui
 21      sticky      Sticky      📌        Non
 30      sleeping    Sleeping    🕸        Non
 40      ready       Ready       ☐        Oui
 50      done        accomplie   ☑        Non
 60      cancelled   Annulé      🗑        Non
======= =========== =========== ======== ========
<BLANKLINE>


Note that a ticket also has a checkbox for marking it as :attr:`closed
<lino_noi.lib.tickets.models.Ticket.closed>`.  This means that a ticket
can be marked as "closed" in any of above states.  We don't use this for the moment and are not sure
whether this is a cool feature (:ticket:`372`).

- :attr:`standby <lino_noi.lib.tickets.models.Ticket.standby>` 


Projects
========

The :attr:`project <lino_noi.lib.tickets.models.Ticket.project>` of a
ticket is used to specify "who is going to pay" for it. Lino Noi does
not issue invoices, so it uses this information only for reporting
about it and helping with the decision about whether and how worktime
is being invoiced to the customer.  But the invoicing itself is not
currently a goal of Lino Noi.

So a **project** is something for which somebody is possibly willing
to pay money.

>>> rt.show(tickets.Projects)
=========== =============== ======== ============== =========
 Reference   Name            Parent   Project Type   Private
----------- --------------- -------- -------------- ---------
 linö        Framewörk                               No
 téam        Téam            linö                    Yes
 docs        Documentatión   linö                    No
 research    Research        docs                    No
 shop        Shop                                    No
=========== =============== ======== ============== =========
<BLANKLINE>


>>> rt.show(tickets.TopLevelProjects)
=========== =========== ======== ================
 Reference   Name        Parent   Children
----------- ----------- -------- ----------------
 linö        Framewörk            *téam*, *docs*
 shop        Shop
=========== =========== ======== ================
<BLANKLINE>


Developers can start working on tickets without specifying a project
(i.e. without knowing who is going to pay for their work).  

But after some time every ticket should get assigned to some
project. You can see a list of tickets which have not yet been
assigned to a project:

>>> pv = dict(has_project=dd.YesNo.no)
>>> rt.show(tickets.Tickets, param_values=pv)
... #doctest: +REPORT_UDIFF
==== =================== ================= =========== ========= ============== =========
 ID   Summary             Reporter          Topic       Faculty   Workflow       Project
---- ------------------- ----------------- ----------- --------- -------------- ---------
 5    Cannot create Foo   Romain Raffault   Lino Cosi             **Sleeping**
 3    Baz sucks           marc              Lino Core             **ToDo**
==== =================== ================= =========== ========= ============== =========
<BLANKLINE>


Distribution of tickets per project
===================================

In our demo database, tickets are distributed over the different
projects as follows (not a realistic distribution):

>>> for p in tickets.Project.objects.all():
...     print p.ref, p.tickets_by_project.count()
linö 3
téam 3
docs 3
research 3
shop 2



Private tickets
===============

Tickets are private by default. But when they are assigned to a public
project, then their privacy is removed.

So the private tickets are (1) those in project "téam" and (2) those
without project:

>>> pv = dict(show_private=dd.YesNo.yes)
>>> rt.show(tickets.Tickets, param_values=pv,
...     column_names="id summary assigned_to project")
... #doctest: +REPORT_UDIFF
==== ======================= ============= =========
 ID   Summary                 Assigned to   Project
---- ----------------------- ------------- ---------
 14   Bar cannot baz          luc           téam
 9    Foo never matches Bar                 téam
 5    Cannot create Foo
 3    Baz sucks               luc
 2    Bar is not always baz   jean          téam
==== ======================= ============= =========
<BLANKLINE>

And these are the public tickets:

>>> pv = dict(show_private=dd.YesNo.no)
>>> rt.show(tickets.Tickets, param_values=pv,
...     column_names="id summary assigned_to project")
... #doctest: +REPORT_UDIFF
==== =========================================== ============= ==========
 ID   Summary                                     Assigned to   Project
---- ------------------------------------------- ------------- ----------
 16   How to get bar from foo                     mathieu       research
 15   Bars have no foo                            marc          docs
 13   Bar cannot foo                                            linö
 12   Foo cannot bar                              jean          shop
 11   Class-based Foos and Bars?                  mathieu       research
 10   Where can I find a Foo when bazing Bazes?   marc          docs
 8    Is there any Bar in Foo?                    luc           linö
 7    No Foo after deleting Bar                   jean          shop
 6    Sell bar in baz                             mathieu       research
 4    Foo and bar don't baz                       marc          docs
 1    Föö fails to bar when baz                                 linö
==== =========================================== ============= ==========
<BLANKLINE>


There are 5 private and 11 public tickets in the demo database.

>>> tickets.Ticket.objects.filter(private=True).count()
5
>>> tickets.Ticket.objects.filter(private=False).count()
11

My tickets
==========

>>> rt.login('jean').show(tickets.MyTickets)
... #doctest: +REPORT_UDIFF
============================================= ========= ============== ===============================================
 Overview                                      Faculty   Topic          Workflow
--------------------------------------------- --------- -------------- -----------------------------------------------
 `#15 (Bars have no foo) <Detail>`__                     Lino Core      **Done** → [▶] [☆]
 `#8 (Is there any Bar in Foo?) <Detail>`__              Lino Welfare   **Cancelled** → [▶] [☆]
 `#1 (Föö fails to bar when baz) <Detail>`__             Lino Cosi      **New** → [📌] [🗪] [🐜] [🕸] [☐] [☑] [🗑] [▶] [☆]
============================================= ========= ============== ===============================================
<BLANKLINE>


Topics
========

The :attr:`topic <lino_noi.lib.tickets.models.Ticket.topic>` of a
ticket is what Trac calls "component". Topics are a "customer-side"
classification of the different components which are being developed
by the team that uses a given Lino Noi site.

There are 4 topics in the demo database.

>>> rt.show(topics.Topics)
=========== ============== ================== ================== =============
 Reference   Designation    Designation (de)   Designation (fr)   Topic group
----------- -------------- ------------------ ------------------ -------------
 linõ        Lino Core
 welfäre     Lino Welfare
 così        Lino Cosi
 faggio      Lino Voga
=========== ============== ================== ================== =============
<BLANKLINE>


Choosing a topic
================

When choosing a topic, the search text looks in both the reference and
the designation:

>>> base = '/choices/tickets/Tickets/topic'
>>> show_choices("robin", base + '?query=')
<br/>
Lino Core
Lino Welfare
Lino Cosi
Lino Voga

Note that we have a topic whose `ref` is different from `name`, and
that the search works in both fields:

>>> obj = topics.Topic.get_by_ref('faggio')
>>> print(obj.ref)
faggio
>>> print(obj.name)
Lino Voga

>>> show_choices("robin", base + '?query=fag')
Lino Voga

>>> show_choices("robin", base + '?query=voga')
Lino Voga


Interests
=========

Every partner can have its list of "interests". They will get notified
about changes in these topics even when they did not report the
ticket.


>>> obj = contacts.Partner.objects.get(name="welket")
>>> rt.show(topics.InterestsByPartner, obj)
... #doctest: +REPORT_UDIFF
==============
 Topic
--------------
 Lino Core
 Lino Welfare
 Lino Cosi
==============
<BLANKLINE>

>>> obj = topics.Topic.objects.get(ref="welfäre")
>>> rt.show(topics.InterestsByTopic, obj)
... #doctest: +REPORT_UDIFF
=========
 Partner
---------
 welket
 welsch
=========
<BLANKLINE>



Filtering tickets by topic
==========================

>>> pv = dict(topic=rt.models.topics.Topic.get_by_ref("così"))
>>> rt.show(tickets.Tickets, param_values=pv)
... #doctest: +REPORT_UDIFF
==== =========================== ================= =========== =============== ============== =========
 ID   Summary                     Reporter          Topic       Faculty         Workflow       Project
---- --------------------------- ----------------- ----------- --------------- -------------- ---------
 13   Bar cannot foo              Rolf Rompen       Lino Cosi   Documentation   **Sleeping**   linö
 9    Foo never matches Bar       luc               Lino Cosi   Testing         **New**        téam
 5    Cannot create Foo           Romain Raffault   Lino Cosi                   **Sleeping**
 1    Föö fails to bar when baz   jean              Lino Cosi                   **New**        linö
==== =========================== ================= =========== =============== ============== =========
<BLANKLINE>
 



Sites
=====

Lino Noi has a list of all sites for which we do support:

>>> rt.show(tickets.Sites)
============= ========= ======== ====
 Designation   Partner   Remark   ID
------------- --------- -------- ----
 pypi          pypi               3
 welket        welket             1
 welsch        welsch             2
============= ========= ======== ====
<BLANKLINE>

A ticket may or may not be "local", i.e. specific to a given site.
When a ticket is site-specific, we simply assign the `site` field.  We
can see all local tickets for a given site object:

>>> welket = tickets.Site.objects.get(name="welket")
>>> rt.show(tickets.TicketsBySite, welket)
... #doctest: +REPORT_UDIFF
==== =========================================== ============= ============== =============== =============== ==========
 ID   Summary                                     Reporter      Topic          Faculty         Workflow        Project
---- ------------------------------------------- ------------- -------------- --------------- --------------- ----------
 16   How to get bar from foo                     luc           Lino Welfare                   **Cancelled**   research
 13   Bar cannot foo                              Rolf Rompen   Lino Cosi      Documentation   **Sleeping**    linö
 10   Where can I find a Foo when bazing Bazes?   marc          Lino Voga                      **Talk**        docs
 7    No Foo after deleting Bar                   Robin Rood    Lino Core                      **Done**        shop
 4    Foo and bar don't baz                       mathieu       Lino Welfare                   **Sticky**      docs
 1    Föö fails to bar when baz                   jean          Lino Cosi                      **New**         linö
==== =========================================== ============= ============== =============== =============== ==========
<BLANKLINE>

Note that the above table shows no state change actions in the
Workflow column because it is being requested by anonymous. For an
authenticated developer it looks like this:

>>> rt.login('jean').show(tickets.TicketsBySite, welket)
... #doctest: +REPORT_UDIFF
==== =========================================== ============= ============== =============== =============================================== ==========
 ID   Summary                                     Reporter      Topic          Faculty         Workflow                                        Project
---- ------------------------------------------- ------------- -------------- --------------- ----------------------------------------------- ----------
 16   How to get bar from foo                     luc           Lino Welfare                   **Cancelled** → [☆]                             research
 13   Bar cannot foo                              Rolf Rompen   Lino Cosi      Documentation   **Sleeping** → [☆]                              linö
 10   Where can I find a Foo when bazing Bazes?   marc          Lino Voga                      **Talk** → [☆]                                  docs
 7    No Foo after deleting Bar                   Robin Rood    Lino Core                      **Done** → [☆]                                  shop
 4    Foo and bar don't baz                       mathieu       Lino Welfare                   **Sticky** → [☆]                                docs
 1    Föö fails to bar when baz                   jean          Lino Cosi                      **New** → [📌] [🗪] [🐜] [🕸] [☐] [☑] [🗑] [▶] [☆]   linö
==== =========================================== ============= ============== =============== =============================================== ==========
<BLANKLINE>


Milestones
==========

Every site can have its list of "milestones" or "releases". A
milestone is when a site gets an upgrade of the software which is
running there. 

A milestone is not necessary an *official* release of a new
version. It just means that you release some changed software to the
users of that site.

>>> welket = tickets.Site.objects.get(name="welket")
>>> rt.show(rt.actors.deploy.MilestonesBySite, welket)
... #doctest: -REPORT_UDIFF
======= ============== ============ ======== ====
 Label   Expected for   Reached      Closed   ID
------- -------------- ------------ -------- ----
         15/05/2015     15/05/2015   No       7
         11/05/2015     11/05/2015   No       5
         07/05/2015     07/05/2015   No       3
         03/05/2015     03/05/2015   No       1
======= ============== ============ ======== ====
<BLANKLINE>


Deployments
===========

Every milestone has its list of "deployments", i.e. the tickets that
are being fixed when this milestone is reached.

The demo database currently does not have any deployments:

>>> rt.show(rt.actors.deploy.Deployments)
No data to display


Release notes
=============

Lino Noi has an excerpt type for printing a milestone.  This is used
to produce *release notes*.

>>> obj = deploy.Milestone.objects.get(pk=7)
>>> rt.show(rt.actors.deploy.DeploymentsByMilestone, obj)
No data to display

>>> rt.show(clocking.OtherTicketsByMilestone, obj)
No data to display



Dependencies between tickets
============================

>>> rt.show(tickets.LinkTypes)
... #doctest: +REPORT_UDIFF
======= =========== ===========
 value   name        text
------- ----------- -----------
 10      requires    Requires
 20      triggers    Triggers
 30      suggests    Suggests
 40      obsoletes   Obsoletes
======= =========== ===========
<BLANKLINE>




>>> rt.show(tickets.Links)
... #doctest: +REPORT_UDIFF
==== ================= ================================ ============================
 ID   Dependency type   Parent                           Child
---- ----------------- -------------------------------- ----------------------------
 1    Requires          #1 (Föö fails to bar when baz)   #2 (Bar is not always baz)
==== ================= ================================ ============================
<BLANKLINE>


Comments
========

Currently the demo database contains no comments...

>>> rt.show(comments.Comments)
No data to display


>>> obj = tickets.Ticket.objects.get(pk=7)
>>> rt.show(comments.CommentsByRFC, obj)
<BLANKLINE>


Filtering tickets
=================


>>> show_fields(tickets.Tickets)
+-----------------+-----------------+------------------------------------------------------------------+
| Internal name   | Verbose name    | Help text                                                        |
+=================+=================+==================================================================+
| reporter        | Reporter        | Only rows reporter by this user.                                 |
+-----------------+-----------------+------------------------------------------------------------------+
| assigned_to     | Assigned to     | Only tickets assigned to this user.                              |
+-----------------+-----------------+------------------------------------------------------------------+
| interesting_for | Interesting for | Only tickets interesting for this partner.                       |
+-----------------+-----------------+------------------------------------------------------------------+
| site            | Site            | Select a site if you want to see only tickets for this site.     |
+-----------------+-----------------+------------------------------------------------------------------+
| project         | Project         |                                                                  |
+-----------------+-----------------+------------------------------------------------------------------+
| state           | State           | Only rows having this state.                                     |
+-----------------+-----------------+------------------------------------------------------------------+
| has_project     | Has project     | Show only (or hide) tickets which have a project assigned.       |
+-----------------+-----------------+------------------------------------------------------------------+
| show_assigned   | Assigned        | Show only (or hide) tickets which are assigned to somebody.      |
+-----------------+-----------------+------------------------------------------------------------------+
| show_active     | Active          | Show only (or hide) tickets which are active (i.e. state is Talk |
|                 |                 | or ToDo).                                                        |
+-----------------+-----------------+------------------------------------------------------------------+
| show_private    | Private         | Show only (or hide) tickets that are marked private.             |
+-----------------+-----------------+------------------------------------------------------------------+
| start_date      | Period from     | Start date of observed period                                    |
+-----------------+-----------------+------------------------------------------------------------------+
| end_date        | until           | End date of observed period                                      |
+-----------------+-----------------+------------------------------------------------------------------+
| observed_event  | Observed event  |                                                                  |
+-----------------+-----------------+------------------------------------------------------------------+
| topic           | Topic           |                                                                  |
+-----------------+-----------------+------------------------------------------------------------------+
| feasable_by     | Feasable by     | Show only tickets for which I am competent.                      |
+-----------------+-----------------+------------------------------------------------------------------+

>>> rt.login('robin').show(rt.actors.tickets.Tickets)
... #doctest: +REPORT_UDIFF
==== =========================================== ================= ============== =============== =============================================== ==========
 ID   Summary                                     Reporter          Topic          Faculty         Workflow                                        Project
---- ------------------------------------------- ----------------- -------------- --------------- ----------------------------------------------- ----------
 16   How to get bar from foo                     luc               Lino Welfare                   **Cancelled** → [▶] [☆]                         research
 15   Bars have no foo                            jean              Lino Core                      **Done** → [▶] [☆]                              docs
 14   Bar cannot baz                              Robin Rood        Lino Voga                      **Ready** → [🗪] [🐜] [☑] [▶] [☆]                 téam
 13   Bar cannot foo                              Rolf Rompen       Lino Cosi      Documentation   **Sleeping** → [☑] [🗑] [▶] [☆]                  linö
 12   Foo cannot bar                              Romain Raffault   Lino Welfare   Code changes    **Sticky** → [▶] [☆]                            shop
 11   Class-based Foos and Bars?                  mathieu           Lino Core                      **ToDo** → [🗪] [🕸] [☐] [☑] [🗑] [▶] [☆]          research
 10   Where can I find a Foo when bazing Bazes?   marc              Lino Voga                      **Talk** → [🐜] [🕸] [☐] [☑] [🗑] [▶] [☆]          docs
 9    Foo never matches Bar                       luc               Lino Cosi      Testing         **New** → [📌] [🗪] [🐜] [🕸] [☐] [☑] [🗑] [▶] [☆]   téam
 8    Is there any Bar in Foo?                    jean              Lino Welfare                   **Cancelled** → [▶] [☆]                         linö
 7    No Foo after deleting Bar                   Robin Rood        Lino Core                      **Done** → [▶] [☆]                              shop
 6    Sell bar in baz                             Rolf Rompen       Lino Voga      Analysis        **Ready** → [🗪] [🐜] [☑] [▶] [☆]                 research
 5    Cannot create Foo                           Romain Raffault   Lino Cosi                      **Sleeping** → [☑] [🗑] [▶] [☆]
 4    Foo and bar don't baz                       mathieu           Lino Welfare                   **Sticky** → [▶] [☆]                            docs
 3    Baz sucks                                   marc              Lino Core                      **ToDo** → [🗪] [🕸] [☐] [☑] [🗑] [▶] [☆]
 2    Bar is not always baz                       luc               Lino Voga                      **Talk** → [🐜] [🕸] [☐] [☑] [🗑] [▶] [☆]          téam
 1    Föö fails to bar when baz                   jean              Lino Cosi                      **New** → [📌] [🗪] [🐜] [🕸] [☐] [☑] [🗑] [▶] [☆]   linö
==== =========================================== ================= ============== =============== =============================================== ==========
<BLANKLINE>
