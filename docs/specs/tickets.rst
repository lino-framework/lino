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
linö 23
téam 23
docs 23
research 23
shop 22



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
===== ======================= ============= =========
 ID    Summary                 Assigned to   Project
----- ----------------------- ------------- ---------
 114   Ticket 97               jean          téam
 109   Ticket 92                             téam
 104   Ticket 87               luc           téam
 99    Ticket 82               luc           téam
 94    Ticket 77               luc           téam
 89    Ticket 72                             téam
 84    Ticket 67               marc          téam
 79    Ticket 62               marc          téam
 74    Ticket 57               marc          téam
 69    Ticket 52                             téam
 64    Ticket 47               mathieu       téam
 59    Ticket 42               mathieu       téam
 54    Ticket 37               mathieu       téam
 49    Ticket 32                             téam
 44    Ticket 27               jean          téam
 39    Ticket 22               jean          téam
 34    Ticket 17               jean          téam
 29    Ticket 12                             téam
 24    Ticket 7                luc           téam
 19    Ticket 2                luc           téam
 14    Bar cannot baz          luc           téam
 9     Foo never matches Bar                 téam
 5     Cannot create Foo
 3     Baz sucks               luc
 2     Bar is not always baz   jean          téam
===== ======================= ============= =========
<BLANKLINE>


And these are the public tickets:

>>> pv = dict(show_private=dd.YesNo.no)
>>> rt.show(tickets.Tickets, param_values=pv,
...     column_names="id summary assigned_to project")
... #doctest: +REPORT_UDIFF
===== =========================================== ============= ==========
 ID    Summary                                     Assigned to   Project
----- ------------------------------------------- ------------- ----------
 116   Ticket 99                                   marc          research
 115   Ticket 98                                   luc           docs
 113   Ticket 96                                                 linö
 112   Ticket 95                                   mathieu       shop
 111   Ticket 94                                   marc          research
 110   Ticket 93                                   luc           docs
 108   Ticket 91                                   jean          linö
 107   Ticket 90                                   mathieu       shop
 106   Ticket 89                                   marc          research
 105   Ticket 88                                                 docs
 103   Ticket 86                                   jean          linö
 102   Ticket 85                                   mathieu       shop
 101   Ticket 84                                                 research
 100   Ticket 83                                   marc          docs
 98    Ticket 81                                   jean          linö
 97    Ticket 80                                                 shop
 96    Ticket 79                                   mathieu       research
 95    Ticket 78                                   marc          docs
 93    Ticket 76                                                 linö
 92    Ticket 75                                   jean          shop
 91    Ticket 74                                   mathieu       research
 90    Ticket 73                                   marc          docs
 88    Ticket 71                                   luc           linö
 87    Ticket 70                                   jean          shop
 86    Ticket 69                                   mathieu       research
 85    Ticket 68                                                 docs
 83    Ticket 66                                   luc           linö
 82    Ticket 65                                   jean          shop
 81    Ticket 64                                                 research
 80    Ticket 63                                   mathieu       docs
 78    Ticket 61                                   luc           linö
 77    Ticket 60                                                 shop
 76    Ticket 59                                   jean          research
 75    Ticket 58                                   mathieu       docs
 73    Ticket 56                                                 linö
 72    Ticket 55                                   luc           shop
 71    Ticket 54                                   jean          research
 70    Ticket 53                                   mathieu       docs
 68    Ticket 51                                   marc          linö
 67    Ticket 50                                   luc           shop
 66    Ticket 49                                   jean          research
 65    Ticket 48                                                 docs
 63    Ticket 46                                   marc          linö
 62    Ticket 45                                   luc           shop
 61    Ticket 44                                                 research
 60    Ticket 43                                   jean          docs
 58    Ticket 41                                   marc          linö
 57    Ticket 40                                                 shop
 56    Ticket 39                                   luc           research
 55    Ticket 38                                   jean          docs
 53    Ticket 36                                                 linö
 52    Ticket 35                                   marc          shop
 51    Ticket 34                                   luc           research
 50    Ticket 33                                   jean          docs
 48    Ticket 31                                   mathieu       linö
 47    Ticket 30                                   marc          shop
 46    Ticket 29                                   luc           research
 45    Ticket 28                                                 docs
 43    Ticket 26                                   mathieu       linö
 42    Ticket 25                                   marc          shop
 41    Ticket 24                                                 research
 40    Ticket 23                                   luc           docs
 38    Ticket 21                                   mathieu       linö
 37    Ticket 20                                                 shop
 36    Ticket 19                                   marc          research
 35    Ticket 18                                   luc           docs
 33    Ticket 16                                                 linö
 32    Ticket 15                                   mathieu       shop
 31    Ticket 14                                   marc          research
 30    Ticket 13                                   luc           docs
 28    Ticket 11                                   jean          linö
 27    Ticket 10                                   mathieu       shop
 26    Ticket 9                                    marc          research
 25    Ticket 8                                                  docs
 23    Ticket 6                                    jean          linö
 22    Ticket 5                                    mathieu       shop
 21    Ticket 4                                                  research
 20    Ticket 3                                    marc          docs
 18    Ticket 1                                    jean          linö
 17    Ticket 0                                                  shop
 16    How to get bar from foo                     mathieu       research
 15    Bars have no foo                            marc          docs
 13    Bar cannot foo                                            linö
 12    Foo cannot bar                              jean          shop
 11    Class-based Foos and Bars?                  mathieu       research
 10    Where can I find a Foo when bazing Bazes?   marc          docs
 8     Is there any Bar in Foo?                    luc           linö
 7     No Foo after deleting Bar                   jean          shop
 6     Sell bar in baz                             mathieu       research
 4     Foo and bar don't baz                       marc          docs
 1     Föö fails to bar when baz                                 linö
===== =========================================== ============= ==========
<BLANKLINE>



There are 5 private and 11 public tickets in the demo database.

>>> tickets.Ticket.objects.filter(private=True).count()
25
>>> tickets.Ticket.objects.filter(private=False).count()
91

My tickets
==========

>>> rt.login('jean').show(tickets.MyTickets)
... #doctest: +REPORT_UDIFF
============================================= ========= ============== ===============================================
 Overview                                      Faculty   Topic          Workflow
--------------------------------------------- --------- -------------- -----------------------------------------------
 `#113 (Ticket 96) <Detail>`__                           Lino Cosi      **New** → [📌] [🗪] [🐜] [🕸] [☐] [☑] [🗑] [▶] [☆]
 `#106 (Ticket 89) <Detail>`__                           Lino Voga      **Talk** → [🐜] [🕸] [☐] [☑] [🗑] [▶] [☆]
 `#99 (Ticket 82) <Detail>`__                            Lino Core      **ToDo** → [🗪] [🕸] [☐] [☑] [🗑] [▶] [☆]
 `#92 (Ticket 75) <Detail>`__                            Lino Welfare   **Sticky** → [▶] [☆]
 `#85 (Ticket 68) <Detail>`__                            Lino Cosi      **Sleeping** → [☑] [🗑] [▶] [☆]
 `#78 (Ticket 61) <Detail>`__                            Lino Voga      **Ready** → [🗪] [🐜] [☑] [▶] [☆]
 `#71 (Ticket 54) <Detail>`__                            Lino Core      **Done** → [▶] [☆]
 `#64 (Ticket 47) <Detail>`__                            Lino Welfare   **Cancelled** → [▶] [☆]
 `#57 (Ticket 40) <Detail>`__                            Lino Cosi      **New** → [📌] [🗪] [🐜] [🕸] [☐] [☑] [🗑] [▶] [☆]
 `#50 (Ticket 33) <Detail>`__                            Lino Voga      **Talk** → [🐜] [🕸] [☐] [☑] [🗑] [▶] [☆]
 `#43 (Ticket 26) <Detail>`__                            Lino Core      **ToDo** → [🗪] [🕸] [☐] [☑] [🗑] [▶] [☆]
 `#36 (Ticket 19) <Detail>`__                            Lino Welfare   **Sticky** → [▶] [☆]
 `#29 (Ticket 12) <Detail>`__                            Lino Cosi      **Sleeping** → [☑] [🗑] [▶] [☆]
 `#22 (Ticket 5) <Detail>`__                             Lino Voga      **Ready** → [🗪] [🐜] [☑] [▶] [☆]
 `#15 (Bars have no foo) <Detail>`__                     Lino Core      **Done** → [▶] [☆]
 `#8 (Is there any Bar in Foo?) <Detail>`__              Lino Welfare   **Cancelled** → [▶] [☆]
 `#1 (Föö fails to bar when baz) <Detail>`__             Lino Cosi      **New** → [📌] [🗪] [🐜] [🕸] [☐] [☑] [🗑] [▶] [☆]
============================================= ========= ============== ===============================================
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
===== =========================================== ================= ============== =============== =============== ==========
 ID    Summary                                     Reporter          Topic          Faculty         Workflow        Project
----- ------------------------------------------- ----------------- -------------- --------------- --------------- ----------
 115   Ticket 98                                   marc              Lino Core                      **ToDo**        docs
 112   Ticket 95                                   Robin Rood        Lino Welfare                   **Cancelled**   shop
 109   Ticket 92                                   mathieu           Lino Cosi                      **Sleeping**    téam
 106   Ticket 89                                   jean              Lino Voga                      **Talk**        research
 103   Ticket 86                                   Romain Raffault   Lino Core                      **Done**        linö
 100   Ticket 83                                   luc               Lino Welfare                   **Sticky**      docs
 97    Ticket 80                                   Rolf Rompen       Lino Cosi                      **New**         shop
 94    Ticket 77                                   marc              Lino Voga                      **Ready**       téam
 91    Ticket 74                                   Robin Rood        Lino Core                      **ToDo**        research
 88    Ticket 71                                   mathieu           Lino Welfare                   **Cancelled**   linö
 85    Ticket 68                                   jean              Lino Cosi                      **Sleeping**    docs
 82    Ticket 65                                   Romain Raffault   Lino Voga                      **Talk**        shop
 79    Ticket 62                                   luc               Lino Core                      **Done**        téam
 76    Ticket 59                                   Rolf Rompen       Lino Welfare                   **Sticky**      research
 73    Ticket 56                                   marc              Lino Cosi                      **New**         linö
 70    Ticket 53                                   Robin Rood        Lino Voga                      **Ready**       docs
 67    Ticket 50                                   mathieu           Lino Core                      **ToDo**        shop
 64    Ticket 47                                   jean              Lino Welfare                   **Cancelled**   téam
 61    Ticket 44                                   Romain Raffault   Lino Cosi                      **Sleeping**    research
 58    Ticket 41                                   luc               Lino Voga                      **Talk**        linö
 55    Ticket 38                                   Rolf Rompen       Lino Core                      **Done**        docs
 52    Ticket 35                                   marc              Lino Welfare                   **Sticky**      shop
 49    Ticket 32                                   Robin Rood        Lino Cosi                      **New**         téam
 46    Ticket 29                                   mathieu           Lino Voga                      **Ready**       research
 43    Ticket 26                                   jean              Lino Core                      **ToDo**        linö
 40    Ticket 23                                   Romain Raffault   Lino Welfare                   **Cancelled**   docs
 37    Ticket 20                                   luc               Lino Cosi                      **Sleeping**    shop
 34    Ticket 17                                   Rolf Rompen       Lino Voga                      **Talk**        téam
 31    Ticket 14                                   marc              Lino Core                      **Done**        research
 28    Ticket 11                                   Robin Rood        Lino Welfare                   **Sticky**      linö
 25    Ticket 8                                    mathieu           Lino Cosi                      **New**         docs
 22    Ticket 5                                    jean              Lino Voga                      **Ready**       shop
 19    Ticket 2                                    Romain Raffault   Lino Core                      **ToDo**        téam
 16    How to get bar from foo                     luc               Lino Welfare                   **Cancelled**   research
 13    Bar cannot foo                              Rolf Rompen       Lino Cosi      Documentation   **Sleeping**    linö
 10    Where can I find a Foo when bazing Bazes?   marc              Lino Voga                      **Talk**        docs
 7     No Foo after deleting Bar                   Robin Rood        Lino Core                      **Done**        shop
 4     Foo and bar don't baz                       mathieu           Lino Welfare                   **Sticky**      docs
 1     Föö fails to bar when baz                   jean              Lino Cosi                      **New**         linö
===== =========================================== ================= ============== =============== =============== ==========
<BLANKLINE>


Note that the above table shows no state change actions in the
Workflow column because it is being requested by anonymous. For an
authenticated developer it looks like this:

>>> rt.login('jean').show(tickets.TicketsBySite, welket)
... #doctest: +REPORT_UDIFF
===== =========================================== ================= ============== =============== =============================================== ==========
 ID    Summary                                     Reporter          Topic          Faculty         Workflow                                        Project
----- ------------------------------------------- ----------------- -------------- --------------- ----------------------------------------------- ----------
 115   Ticket 98                                   marc              Lino Core                      **ToDo** → [☆]                                  docs
 112   Ticket 95                                   Robin Rood        Lino Welfare                   **Cancelled** → [☆]                             shop
 109   Ticket 92                                   mathieu           Lino Cosi                      **Sleeping** → [☆]                              téam
 106   Ticket 89                                   jean              Lino Voga                      **Talk** → [🐜] [🕸] [☐] [☑] [🗑] [▶] [☆]          research
 103   Ticket 86                                   Romain Raffault   Lino Core                      **Done** → [☆]                                  linö
 100   Ticket 83                                   luc               Lino Welfare                   **Sticky** → [☆]                                docs
 97    Ticket 80                                   Rolf Rompen       Lino Cosi                      **New** → [☆]                                   shop
 94    Ticket 77                                   marc              Lino Voga                      **Ready** → [☆]                                 téam
 91    Ticket 74                                   Robin Rood        Lino Core                      **ToDo** → [☆]                                  research
 88    Ticket 71                                   mathieu           Lino Welfare                   **Cancelled** → [☆]                             linö
 85    Ticket 68                                   jean              Lino Cosi                      **Sleeping** → [☑] [🗑] [▶] [☆]                  docs
 82    Ticket 65                                   Romain Raffault   Lino Voga                      **Talk** → [☆]                                  shop
 79    Ticket 62                                   luc               Lino Core                      **Done** → [☆]                                  téam
 76    Ticket 59                                   Rolf Rompen       Lino Welfare                   **Sticky** → [☆]                                research
 73    Ticket 56                                   marc              Lino Cosi                      **New** → [☆]                                   linö
 70    Ticket 53                                   Robin Rood        Lino Voga                      **Ready** → [☆]                                 docs
 67    Ticket 50                                   mathieu           Lino Core                      **ToDo** → [☆]                                  shop
 64    Ticket 47                                   jean              Lino Welfare                   **Cancelled** → [▶] [☆]                         téam
 61    Ticket 44                                   Romain Raffault   Lino Cosi                      **Sleeping** → [☆]                              research
 58    Ticket 41                                   luc               Lino Voga                      **Talk** → [☆]                                  linö
 55    Ticket 38                                   Rolf Rompen       Lino Core                      **Done** → [☆]                                  docs
 52    Ticket 35                                   marc              Lino Welfare                   **Sticky** → [☆]                                shop
 49    Ticket 32                                   Robin Rood        Lino Cosi                      **New** → [☆]                                   téam
 46    Ticket 29                                   mathieu           Lino Voga                      **Ready** → [☆]                                 research
 43    Ticket 26                                   jean              Lino Core                      **ToDo** → [🗪] [🕸] [☐] [☑] [🗑] [▶] [☆]          linö
 40    Ticket 23                                   Romain Raffault   Lino Welfare                   **Cancelled** → [☆]                             docs
 37    Ticket 20                                   luc               Lino Cosi                      **Sleeping** → [☆]                              shop
 34    Ticket 17                                   Rolf Rompen       Lino Voga                      **Talk** → [☆]                                  téam
 31    Ticket 14                                   marc              Lino Core                      **Done** → [☆]                                  research
 28    Ticket 11                                   Robin Rood        Lino Welfare                   **Sticky** → [☆]                                linö
 25    Ticket 8                                    mathieu           Lino Cosi                      **New** → [☆]                                   docs
 22    Ticket 5                                    jean              Lino Voga                      **Ready** → [🗪] [🐜] [☑] [▶] [☆]                 shop
 19    Ticket 2                                    Romain Raffault   Lino Core                      **ToDo** → [☆]                                  téam
 16    How to get bar from foo                     luc               Lino Welfare                   **Cancelled** → [☆]                             research
 13    Bar cannot foo                              Rolf Rompen       Lino Cosi      Documentation   **Sleeping** → [☆]                              linö
 10    Where can I find a Foo when bazing Bazes?   marc              Lino Voga                      **Talk** → [☆]                                  docs
 7     No Foo after deleting Bar                   Robin Rood        Lino Core                      **Done** → [☆]                                  shop
 4     Foo and bar don't baz                       mathieu           Lino Welfare                   **Sticky** → [☆]                                docs
 1     Föö fails to bar when baz                   jean              Lino Cosi                      **New** → [📌] [🗪] [🐜] [🕸] [☐] [☑] [🗑] [▶] [☆]   linö
===== =========================================== ================= ============== =============== =============================================== ==========
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
===== =========================================== ================= ============== =============== =============================================== ==========
 ID    Summary                                     Reporter          Topic          Faculty         Workflow                                        Project
----- ------------------------------------------- ----------------- -------------- --------------- ----------------------------------------------- ----------
 116   Ticket 99                                   mathieu           Lino Welfare                   **Sticky** → [▶] [☆]                            research
 115   Ticket 98                                   marc              Lino Core                      **ToDo** → [🗪] [🕸] [☐] [☑] [🗑] [▶] [☆]          docs
 114   Ticket 97                                   luc               Lino Voga                      **Talk** → [🐜] [🕸] [☐] [☑] [🗑] [▶] [☆]          téam
 113   Ticket 96                                   jean              Lino Cosi                      **New** → [📌] [🗪] [🐜] [🕸] [☐] [☑] [🗑] [▶] [☆]   linö
 112   Ticket 95                                   Robin Rood        Lino Welfare                   **Cancelled** → [▶] [☆]                         shop
 111   Ticket 94                                   Rolf Rompen       Lino Core                      **Done** → [▶] [☆]                              research
 110   Ticket 93                                   Romain Raffault   Lino Voga                      **Ready** → [🗪] [🐜] [☑] [▶] [☆]                 docs
 109   Ticket 92                                   mathieu           Lino Cosi                      **Sleeping** → [☑] [🗑] [▶] [☆]                  téam
 108   Ticket 91                                   marc              Lino Welfare                   **Sticky** → [▶] [☆]                            linö
 107   Ticket 90                                   luc               Lino Core                      **ToDo** → [🗪] [🕸] [☐] [☑] [🗑] [▶] [☆]          shop
 106   Ticket 89                                   jean              Lino Voga                      **Talk** → [🐜] [🕸] [☐] [☑] [🗑] [▶] [☆]          research
 105   Ticket 88                                   Robin Rood        Lino Cosi                      **New** → [📌] [🗪] [🐜] [🕸] [☐] [☑] [🗑] [▶] [☆]   docs
 104   Ticket 87                                   Rolf Rompen       Lino Welfare                   **Cancelled** → [▶] [☆]                         téam
 103   Ticket 86                                   Romain Raffault   Lino Core                      **Done** → [▶] [☆]                              linö
 102   Ticket 85                                   mathieu           Lino Voga                      **Ready** → [🗪] [🐜] [☑] [▶] [☆]                 shop
 101   Ticket 84                                   marc              Lino Cosi                      **Sleeping** → [☑] [🗑] [▶] [☆]                  research
 100   Ticket 83                                   luc               Lino Welfare                   **Sticky** → [▶] [☆]                            docs
 99    Ticket 82                                   jean              Lino Core                      **ToDo** → [🗪] [🕸] [☐] [☑] [🗑] [▶] [☆]          téam
 98    Ticket 81                                   Robin Rood        Lino Voga                      **Talk** → [🐜] [🕸] [☐] [☑] [🗑] [▶] [☆]          linö
 97    Ticket 80                                   Rolf Rompen       Lino Cosi                      **New** → [📌] [🗪] [🐜] [🕸] [☐] [☑] [🗑] [▶] [☆]   shop
 96    Ticket 79                                   Romain Raffault   Lino Welfare                   **Cancelled** → [▶] [☆]                         research
 95    Ticket 78                                   mathieu           Lino Core                      **Done** → [▶] [☆]                              docs
 94    Ticket 77                                   marc              Lino Voga                      **Ready** → [🗪] [🐜] [☑] [▶] [☆]                 téam
 93    Ticket 76                                   luc               Lino Cosi                      **Sleeping** → [☑] [🗑] [▶] [☆]                  linö
 92    Ticket 75                                   jean              Lino Welfare                   **Sticky** → [▶] [☆]                            shop
 91    Ticket 74                                   Robin Rood        Lino Core                      **ToDo** → [🗪] [🕸] [☐] [☑] [🗑] [▶] [☆]          research
 90    Ticket 73                                   Rolf Rompen       Lino Voga                      **Talk** → [🐜] [🕸] [☐] [☑] [🗑] [▶] [☆]          docs
 89    Ticket 72                                   Romain Raffault   Lino Cosi                      **New** → [📌] [🗪] [🐜] [🕸] [☐] [☑] [🗑] [▶] [☆]   téam
 88    Ticket 71                                   mathieu           Lino Welfare                   **Cancelled** → [▶] [☆]                         linö
 87    Ticket 70                                   marc              Lino Core                      **Done** → [▶] [☆]                              shop
 86    Ticket 69                                   luc               Lino Voga                      **Ready** → [🗪] [🐜] [☑] [▶] [☆]                 research
 85    Ticket 68                                   jean              Lino Cosi                      **Sleeping** → [☑] [🗑] [▶] [☆]                  docs
 84    Ticket 67                                   Robin Rood        Lino Welfare                   **Sticky** → [▶] [☆]                            téam
 83    Ticket 66                                   Rolf Rompen       Lino Core                      **ToDo** → [🗪] [🕸] [☐] [☑] [🗑] [▶] [☆]          linö
 82    Ticket 65                                   Romain Raffault   Lino Voga                      **Talk** → [🐜] [🕸] [☐] [☑] [🗑] [▶] [☆]          shop
 81    Ticket 64                                   mathieu           Lino Cosi                      **New** → [📌] [🗪] [🐜] [🕸] [☐] [☑] [🗑] [▶] [☆]   research
 80    Ticket 63                                   marc              Lino Welfare                   **Cancelled** → [▶] [☆]                         docs
 79    Ticket 62                                   luc               Lino Core                      **Done** → [▶] [☆]                              téam
 78    Ticket 61                                   jean              Lino Voga                      **Ready** → [🗪] [🐜] [☑] [▶] [☆]                 linö
 77    Ticket 60                                   Robin Rood        Lino Cosi                      **Sleeping** → [☑] [🗑] [▶] [☆]                  shop
 76    Ticket 59                                   Rolf Rompen       Lino Welfare                   **Sticky** → [▶] [☆]                            research
 75    Ticket 58                                   Romain Raffault   Lino Core                      **ToDo** → [🗪] [🕸] [☐] [☑] [🗑] [▶] [☆]          docs
 74    Ticket 57                                   mathieu           Lino Voga                      **Talk** → [🐜] [🕸] [☐] [☑] [🗑] [▶] [☆]          téam
 73    Ticket 56                                   marc              Lino Cosi                      **New** → [📌] [🗪] [🐜] [🕸] [☐] [☑] [🗑] [▶] [☆]   linö
 72    Ticket 55                                   luc               Lino Welfare                   **Cancelled** → [▶] [☆]                         shop
 71    Ticket 54                                   jean              Lino Core                      **Done** → [▶] [☆]                              research
 70    Ticket 53                                   Robin Rood        Lino Voga                      **Ready** → [🗪] [🐜] [☑] [▶] [☆]                 docs
 69    Ticket 52                                   Rolf Rompen       Lino Cosi                      **Sleeping** → [☑] [🗑] [▶] [☆]                  téam
 68    Ticket 51                                   Romain Raffault   Lino Welfare                   **Sticky** → [▶] [☆]                            linö
 67    Ticket 50                                   mathieu           Lino Core                      **ToDo** → [🗪] [🕸] [☐] [☑] [🗑] [▶] [☆]          shop
 66    Ticket 49                                   marc              Lino Voga                      **Talk** → [🐜] [🕸] [☐] [☑] [🗑] [▶] [☆]          research
 65    Ticket 48                                   luc               Lino Cosi                      **New** → [📌] [🗪] [🐜] [🕸] [☐] [☑] [🗑] [▶] [☆]   docs
 64    Ticket 47                                   jean              Lino Welfare                   **Cancelled** → [▶] [☆]                         téam
 63    Ticket 46                                   Robin Rood        Lino Core                      **Done** → [▶] [☆]                              linö
 62    Ticket 45                                   Rolf Rompen       Lino Voga                      **Ready** → [🗪] [🐜] [☑] [▶] [☆]                 shop
 61    Ticket 44                                   Romain Raffault   Lino Cosi                      **Sleeping** → [☑] [🗑] [▶] [☆]                  research
 60    Ticket 43                                   mathieu           Lino Welfare                   **Sticky** → [▶] [☆]                            docs
 59    Ticket 42                                   marc              Lino Core                      **ToDo** → [🗪] [🕸] [☐] [☑] [🗑] [▶] [☆]          téam
 58    Ticket 41                                   luc               Lino Voga                      **Talk** → [🐜] [🕸] [☐] [☑] [🗑] [▶] [☆]          linö
 57    Ticket 40                                   jean              Lino Cosi                      **New** → [📌] [🗪] [🐜] [🕸] [☐] [☑] [🗑] [▶] [☆]   shop
 56    Ticket 39                                   Robin Rood        Lino Welfare                   **Cancelled** → [▶] [☆]                         research
 55    Ticket 38                                   Rolf Rompen       Lino Core                      **Done** → [▶] [☆]                              docs
 54    Ticket 37                                   Romain Raffault   Lino Voga                      **Ready** → [🗪] [🐜] [☑] [▶] [☆]                 téam
 53    Ticket 36                                   mathieu           Lino Cosi                      **Sleeping** → [☑] [🗑] [▶] [☆]                  linö
 52    Ticket 35                                   marc              Lino Welfare                   **Sticky** → [▶] [☆]                            shop
 51    Ticket 34                                   luc               Lino Core                      **ToDo** → [🗪] [🕸] [☐] [☑] [🗑] [▶] [☆]          research
 50    Ticket 33                                   jean              Lino Voga                      **Talk** → [🐜] [🕸] [☐] [☑] [🗑] [▶] [☆]          docs
 49    Ticket 32                                   Robin Rood        Lino Cosi                      **New** → [📌] [🗪] [🐜] [🕸] [☐] [☑] [🗑] [▶] [☆]   téam
 48    Ticket 31                                   Rolf Rompen       Lino Welfare                   **Cancelled** → [▶] [☆]                         linö
 47    Ticket 30                                   Romain Raffault   Lino Core                      **Done** → [▶] [☆]                              shop
 46    Ticket 29                                   mathieu           Lino Voga                      **Ready** → [🗪] [🐜] [☑] [▶] [☆]                 research
 45    Ticket 28                                   marc              Lino Cosi                      **Sleeping** → [☑] [🗑] [▶] [☆]                  docs
 44    Ticket 27                                   luc               Lino Welfare                   **Sticky** → [▶] [☆]                            téam
 43    Ticket 26                                   jean              Lino Core                      **ToDo** → [🗪] [🕸] [☐] [☑] [🗑] [▶] [☆]          linö
 42    Ticket 25                                   Robin Rood        Lino Voga                      **Talk** → [🐜] [🕸] [☐] [☑] [🗑] [▶] [☆]          shop
 41    Ticket 24                                   Rolf Rompen       Lino Cosi                      **New** → [📌] [🗪] [🐜] [🕸] [☐] [☑] [🗑] [▶] [☆]   research
 40    Ticket 23                                   Romain Raffault   Lino Welfare                   **Cancelled** → [▶] [☆]                         docs
 39    Ticket 22                                   mathieu           Lino Core                      **Done** → [▶] [☆]                              téam
 38    Ticket 21                                   marc              Lino Voga                      **Ready** → [🗪] [🐜] [☑] [▶] [☆]                 linö
 37    Ticket 20                                   luc               Lino Cosi                      **Sleeping** → [☑] [🗑] [▶] [☆]                  shop
 36    Ticket 19                                   jean              Lino Welfare                   **Sticky** → [▶] [☆]                            research
 35    Ticket 18                                   Robin Rood        Lino Core                      **ToDo** → [🗪] [🕸] [☐] [☑] [🗑] [▶] [☆]          docs
 34    Ticket 17                                   Rolf Rompen       Lino Voga                      **Talk** → [🐜] [🕸] [☐] [☑] [🗑] [▶] [☆]          téam
 33    Ticket 16                                   Romain Raffault   Lino Cosi                      **New** → [📌] [🗪] [🐜] [🕸] [☐] [☑] [🗑] [▶] [☆]   linö
 32    Ticket 15                                   mathieu           Lino Welfare                   **Cancelled** → [▶] [☆]                         shop
 31    Ticket 14                                   marc              Lino Core                      **Done** → [▶] [☆]                              research
 30    Ticket 13                                   luc               Lino Voga                      **Ready** → [🗪] [🐜] [☑] [▶] [☆]                 docs
 29    Ticket 12                                   jean              Lino Cosi                      **Sleeping** → [☑] [🗑] [▶] [☆]                  téam
 28    Ticket 11                                   Robin Rood        Lino Welfare                   **Sticky** → [▶] [☆]                            linö
 27    Ticket 10                                   Rolf Rompen       Lino Core                      **ToDo** → [🗪] [🕸] [☐] [☑] [🗑] [▶] [☆]          shop
 26    Ticket 9                                    Romain Raffault   Lino Voga                      **Talk** → [🐜] [🕸] [☐] [☑] [🗑] [▶] [☆]          research
 25    Ticket 8                                    mathieu           Lino Cosi                      **New** → [📌] [🗪] [🐜] [🕸] [☐] [☑] [🗑] [▶] [☆]   docs
 24    Ticket 7                                    marc              Lino Welfare                   **Cancelled** → [▶] [☆]                         téam
 23    Ticket 6                                    luc               Lino Core                      **Done** → [▶] [☆]                              linö
 22    Ticket 5                                    jean              Lino Voga                      **Ready** → [🗪] [🐜] [☑] [▶] [☆]                 shop
 21    Ticket 4                                    Robin Rood        Lino Cosi                      **Sleeping** → [☑] [🗑] [▶] [☆]                  research
 20    Ticket 3                                    Rolf Rompen       Lino Welfare                   **Sticky** → [▶] [☆]                            docs
 19    Ticket 2                                    Romain Raffault   Lino Core                      **ToDo** → [🗪] [🕸] [☐] [☑] [🗑] [▶] [☆]          téam
 18    Ticket 1                                    mathieu           Lino Voga                      **Talk** → [🐜] [🕸] [☐] [☑] [🗑] [▶] [☆]          linö
 17    Ticket 0                                    marc              Lino Cosi                      **New** → [📌] [🗪] [🐜] [🕸] [☐] [☑] [🗑] [▶] [☆]   shop
 16    How to get bar from foo                     luc               Lino Welfare                   **Cancelled** → [▶] [☆]                         research
 15    Bars have no foo                            jean              Lino Core                      **Done** → [▶] [☆]                              docs
 14    Bar cannot baz                              Robin Rood        Lino Voga                      **Ready** → [🗪] [🐜] [☑] [▶] [☆]                 téam
 13    Bar cannot foo                              Rolf Rompen       Lino Cosi      Documentation   **Sleeping** → [☑] [🗑] [▶] [☆]                  linö
 12    Foo cannot bar                              Romain Raffault   Lino Welfare   Code changes    **Sticky** → [▶] [☆]                            shop
 11    Class-based Foos and Bars?                  mathieu           Lino Core                      **ToDo** → [🗪] [🕸] [☐] [☑] [🗑] [▶] [☆]          research
 10    Where can I find a Foo when bazing Bazes?   marc              Lino Voga                      **Talk** → [🐜] [🕸] [☐] [☑] [🗑] [▶] [☆]          docs
 9     Foo never matches Bar                       luc               Lino Cosi      Testing         **New** → [📌] [🗪] [🐜] [🕸] [☐] [☑] [🗑] [▶] [☆]   téam
 8     Is there any Bar in Foo?                    jean              Lino Welfare                   **Cancelled** → [▶] [☆]                         linö
 7     No Foo after deleting Bar                   Robin Rood        Lino Core                      **Done** → [▶] [☆]                              shop
 6     Sell bar in baz                             Rolf Rompen       Lino Voga      Analysis        **Ready** → [🗪] [🐜] [☑] [▶] [☆]                 research
 5     Cannot create Foo                           Romain Raffault   Lino Cosi                      **Sleeping** → [☑] [🗑] [▶] [☆]
 4     Foo and bar don't baz                       mathieu           Lino Welfare                   **Sticky** → [▶] [☆]                            docs
 3     Baz sucks                                   marc              Lino Core                      **ToDo** → [🗪] [🕸] [☐] [☑] [🗑] [▶] [☆]
 2     Bar is not always baz                       luc               Lino Voga                      **Talk** → [🐜] [🕸] [☐] [☑] [🗑] [▶] [☆]          téam
 1     Föö fails to bar when baz                   jean              Lino Cosi                      **New** → [📌] [🗪] [🐜] [🕸] [☐] [☑] [🗑] [▶] [☆]   linö
===== =========================================== ================= ============== =============== =============================================== ==========
<BLANKLINE>




The detail layout of a ticket
=============================

Here is a textual description of the fields and their layout used in
the detail window of a ticket.

>>> from lino.utils.diag import py2rst
>>> print(py2rst(tickets.Tickets.detail_layout, True))
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF -SKIP
(main) [visible for all]:
- **General** (general):
  - (general_1):
    - (general1):
      - (general1_1): **Summary** (summary), **ID** (id), **Reporter** (reporter)
      - (general1_2): **Site** (site), **Topic** (topic), **Project** (project), **Private** (private)
      - (general1_3): **Workflow** (workflow_buttons), **Assigned to** (assigned_to), **Faculty** (faculty)
    - **Deployments** (deploy.DeploymentsByTicket) [visible for user consultant hoster developer senior admin]
  - (general_2): **Description** (description), **Comments** (CommentsByRFC) [visible for user consultant hoster developer senior admin], **Sessions** (SessionsByTicket) [visible for consultant hoster developer senior admin]
- **More** (more):
  - (more_1):
    - (more1):
      - (more1_1): **Created** (created), **Modified** (modified), **Reported for** (reported_for), **Ticket type** (ticket_type)
      - (more1_2): **State** (state), **Duplicate of** (duplicate_of), **Planned time** (planned_time), **Priority** (priority)
    - **Duplicates** (DuplicatesByTicket)
  - (more_2): **Upgrade notes** (upgrade_notes), **Dependencies** (LinksByTicket) [visible for senior admin]
- **History** (history_tab_1) [visible for senior admin]:
  - **Changes** (changes.ChangesByMaster) [visible for user consultant hoster developer senior admin]
  - **Starred by** (stars.StarsByController) [visible for user consultant hoster developer senior admin]
<BLANKLINE>



