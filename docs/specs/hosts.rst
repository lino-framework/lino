.. _noi.specs.hosts:

=====
Hosts
=====

This is currently just an idea.

A new :mod:`lino.modlib.hosting` plugin would add the following models.

- A **host** is a VPS or dedicated server running somewhere.
  A given *host* 
  can offer one or several *environments*
  and can host one or several *sites*. 

- A **site** is a website where some web application is
  running.  On an Apache server this corresponds to a VirtualHost.
  A *site* is always hosted on one and only one **host**.  

- An **environment** is a set of libraries. In a Python context this
  corresponds to a virtualenv.  A *site* always uses one and only one
  *environment* from those offered by its *host*.
  Every environment possibly uses a set of *repositories*.

- A **repository** is a Python package which is being used in an
  *environment*.

- An **upgrade** is the fact that a *site* has been upgraded from one
  set of revisions to another set of revisions.

Dependencies:

- :mod:`lino.modlib.hosting` would need :mod:`lino_noi.lib.tickets`,
  and it would extend the :mod:`Ticket
  <lino_noi.lib.tickets.models.Ticket>` model by injecting a field
  ``site`` which points to the *site* where the problem was observed.

The **only goal** of all this (in a first stage) is to know the
timestamps of "the previous" and "the new" revisions in order to
generate release notes.

I may sound surprising to perform such a complex theatre just for such
a little thing.

It is partly due to the fact that we don't work with released
versions.

A "lighter" version of this would be to have only one model
**Upgrade** which holds the timestamps *before* and *after*, to have
the `diag` command output our current timestamp, and to enter these
timestamps manually.

And it seems that the **Milestone** model (currently in
:mod:`lino_noi.lib.tickets`) can go away.
