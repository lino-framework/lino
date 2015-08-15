.. _noi.tested.general:

=================
Lino Noi Overview
=================

The goal of Lino Noi is managing **tickets** (problems reported by
customers or other users) and registering the **time** needed by
developers (or other users) to work on these tickets. It is then
possible to publish **service reports**.

.. How to test only this document:

    $ python setup.py test -s tests.SpecsTests.test_tickets
    
    doctest init:

    >>> import os
    >>> os.environ['DJANGO_SETTINGS_MODULE'] = 'lino_noi.projects.team.settings.demo'
    >>> from __future__ import print_function 
    >>> from __future__ import unicode_literals
    >>> from lino.api.doctest import *


Lino Noi uses both :mod:`lino.modlib.tickets` (Ticket management) and
:mod:`lino.modlib.clocking` (Development time tracking).


.. contents::
  :local:


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
['lino.modlib.excerpts']

See also :attr:`needs_plugins <lino.core.plugin.Plugin.needs_plugins>`.


User profiles
=============

A default Lino Noi site has the following user profiles:

>>> rt.show(users.UserProfiles)
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

