.. _noi.specs.topics:

=============================
Topics in Lino Noi
=============================


.. How to test only this document:

    $ python setup.py test -s tests.SpecsTests.test_topics
    
    doctest init:

    >>> import lino
    >>> lino.startup('lino_noi.projects.team.settings.demo')
    >>> from lino.api.doctest import *


This document specifies the ticket management functions of Lino Noi,
implemented in :mod:`lino_noi.lib.tickets`.


.. contents::
  :local:



Topics
========

The :attr:`topic <lino_noi.lib.tickets.models.Ticket.topic>` of a
ticket is what Trac calls "component". Topics are a "customer-side"
classification of the different components which are being developed
by the team that uses a given Lino Noi site.

There are 4 topics in the demo database.

>>> show_menu_path(topics.AllTopics)
Configure --> Contacts --> Topics



>>> rt.show(topics.AllTopics)
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
===== =========================== ================= =========== =============== ============== ==========
 ID    Summary                     Reporter          Topic       Faculty         Workflow       Project
----- --------------------------- ----------------- ----------- --------------- -------------- ----------
 113   Ticket 96                   jean              Lino Cosi                   **New**        linö
 109   Ticket 92                   mathieu           Lino Cosi                   **Sleeping**   téam
 105   Ticket 88                   Robin Rood        Lino Cosi                   **New**        docs
 101   Ticket 84                   marc              Lino Cosi                   **Sleeping**   research
 97    Ticket 80                   Rolf Rompen       Lino Cosi                   **New**        shop
 93    Ticket 76                   luc               Lino Cosi                   **Sleeping**   linö
 89    Ticket 72                   Romain Raffault   Lino Cosi                   **New**        téam
 85    Ticket 68                   jean              Lino Cosi                   **Sleeping**   docs
 81    Ticket 64                   mathieu           Lino Cosi                   **New**        research
 77    Ticket 60                   Robin Rood        Lino Cosi                   **Sleeping**   shop
 73    Ticket 56                   marc              Lino Cosi                   **New**        linö
 69    Ticket 52                   Rolf Rompen       Lino Cosi                   **Sleeping**   téam
 65    Ticket 48                   luc               Lino Cosi                   **New**        docs
 61    Ticket 44                   Romain Raffault   Lino Cosi                   **Sleeping**   research
 57    Ticket 40                   jean              Lino Cosi                   **New**        shop
 53    Ticket 36                   mathieu           Lino Cosi                   **Sleeping**   linö
 49    Ticket 32                   Robin Rood        Lino Cosi                   **New**        téam
 45    Ticket 28                   marc              Lino Cosi                   **Sleeping**   docs
 41    Ticket 24                   Rolf Rompen       Lino Cosi                   **New**        research
 37    Ticket 20                   luc               Lino Cosi                   **Sleeping**   shop
 33    Ticket 16                   Romain Raffault   Lino Cosi                   **New**        linö
 29    Ticket 12                   jean              Lino Cosi                   **Sleeping**   téam
 25    Ticket 8                    mathieu           Lino Cosi                   **New**        docs
 21    Ticket 4                    Robin Rood        Lino Cosi                   **Sleeping**   research
 17    Ticket 0                    marc              Lino Cosi                   **New**        shop
 13    Bar cannot foo              Rolf Rompen       Lino Cosi   Documentation   **Sleeping**   linö
 9     Foo never matches Bar       luc               Lino Cosi   Testing         **New**        téam
 5     Cannot create Foo           Romain Raffault   Lino Cosi                   **Sleeping**
 1     Föö fails to bar when baz   jean              Lino Cosi                   **New**        linö
===== =========================== ================= =========== =============== ============== ==========
<BLANKLINE>

 


Topic groups
============

>>> rt.show(topics.TopicGroups)
No data to display

>>> show_menu_path(topics.TopicGroups)
Configure --> Contacts --> Topic groups
