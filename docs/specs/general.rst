.. _noi.specs.general:

=================
Lino Noi Overview
=================

The goal of Lino Noi is managing **tickets** (problems reported by
customers or other users) and registering the **time** needed by
developers (or other users) to work on these tickets. It is then
possible to publish **service reports**.

.. How to test just this document:

    $ python setup.py test -s tests.SpecsTests.test_general
    
    doctest init:

    >>> from lino import startup
    >>> startup('lino_noi.projects.team.settings.demo')
    >>> from lino.api.doctest import *


Lino Noi uses both :mod:`lino_noi.lib.tickets` (Ticket management) and
:mod:`lino_noi.lib.clocking` (Worktime tracking).


.. contents::
  :local:


Tickets versus Clocking
=======================

Note that :mod:`lino_noi.lib.clocking` and :mod:`lino_noi.lib.tickets`
are independent modules which might be reused by other applicaton.
Lino Noi uses them both and extends the "library" versions:

- :mod:`lino_noi.projects.team.lib.clocking` 
- :mod:`lino_noi.projects.team.lib.tickets` 

>>> dd.plugins.clocking
lino_noi.projects.team.lib.clocking

>>> dd.plugins.tickets
lino_noi.projects.team.lib.tickets

For example, a service report is part of the clocking plugin, but the
current implementation is defined in
:class:`lino_noi.projects.team.lib.clocking.models.ServiceReport` (not
in :mod:`lino_noi.lib.clocking`) because it makes sense only if you
have both clocking and tickets.


>>> dd.plugins.clocking.needs_plugins
['lino_noi.projects.team.lib.tickets']

>>> dd.plugins.tickets.needs_plugins
['lino_xl.lib.stars', 'lino_xl.lib.excerpts', 'lino.modlib.comments', 'lino.modlib.changes', 'lino_noi.lib.noi']

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

