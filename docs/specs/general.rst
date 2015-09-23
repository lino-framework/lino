.. _noi.tested.general:

=================
Lino Noi Overview
=================

The goal of Lino Noi is managing **tickets** (problems reported by
customers or other users) and registering the **time** needed by
developers (or other users) to work on these tickets. It is then
possible to publish **service reports**.

.. How to test only this document:

    $ python setup.py test -s tests.SpecsTests.test_general
    
    doctest init:

    >>> import os
    >>> os.environ['DJANGO_SETTINGS_MODULE'] = 'lino_noi.projects.team.settings.demo'
    >>> from __future__ import print_function 
    >>> from __future__ import unicode_literals
    >>> from lino.api.doctest import *


Lino Noi uses both :mod:`lino_noi.lib.tickets` (Ticket management) and
:mod:`lino_noi.lib.clocking` (Development time tracking).


.. contents::
  :local:


Tickets versus Clocking
=======================

Note that :mod:`lino_noi.lib.clocking` depends on
:mod:`lino_noi.lib.tickets` and not vice-versa.  A time tracking system
makes no sense if you don't have a ticketing system.  Lino Noi uses
them both, but some other applicaton might use only :mod:`tickets
<lino_noi.lib.tickets>` without wanting to manage :mod:`clocking
<lino_noi.lib.clocking>`.

>>> dd.plugins.clocking.needs_plugins
['lino_noi.lib.tickets']

>>> dd.plugins.tickets.needs_plugins
['lino.modlib.excerpts']

See also :attr:`needs_plugins <lino.core.plugin.Plugin.needs_plugins>`.


User profiles
=============

A default Lino Noi site has the following user profiles:

>>> rt.show(users.UserProfiles)
======= ============ ==================
 value   name         text
------- ------------ ------------------
 000     anonymous    Anonymous
 100     user         User
 200     consultant   Consultant
 300     hoster       Hoster
 400     developer    Developer
 490     senior       Senior developer
 900     admin        Administrator
======= ============ ==================
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

Here is a list of user profiles of those who can work on tickets:

>>> from lino_noi.lib.tickets.roles import Worker
>>> UserProfiles = rt.modules.users.UserProfiles
>>> [p.name for p in UserProfiles.items()
...     if p.has_required_roles([Worker])]
['consultant', 'hoster', 'developer', 'senior', 'admin']

And here are those who don't work:

>>> [p.name for p in UserProfiles.items()
...    if not p.has_required_roles([Worker])]
['anonymous', 'user']


Users
=====

>>> rt.show(users.UsersOverview)
========== ================== ==========
 Username   User Profile       Language
---------- ------------------ ----------
 jean       Senior developer   en
 luc        Developer          en
 marc       Consultant         en
 mathieu    Consultant         en
 robin      Administrator      en
 rolf       Administrator      de
 romain     Administrator      fr
========== ================== ==========
<BLANKLINE>

