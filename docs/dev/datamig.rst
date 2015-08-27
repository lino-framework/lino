.. _lino.datamig:

=========================
Data migrations à la Lino
=========================

Overview
========

Data migration is a complex topic. Django needed until version 1.7
before they dared to suggest a default method to automating these
tasks (see `Migrations
<https://docs.djangoproject.com/en/1.7/topics/migrations/>`_ if you
are curious).  

Lino includes a system for managing database migrations which takes a
rather different approach than Django.

The basic idea is that you write a *Python dump* (see
:doc:`/dev/dump2py`) *before* upgrading with the old version, and that
you load that dump with the new version *after* upgrading.

Disadvantage:

- You cannot migrate a running system. Users must stop to work in your
  application for a few minutes.

Advantage: 

- The whole process of developing, maintaining and testing migration
  code becomes more natural and easier to manage.


General strategy for handling data migrations
=============================================

- When you upgrade on a production site, always make a
  :manage:`dump2py` of your database before the upgrade.

- After the upgrade, reinitialize your database from that dump by
  running the :xfile:`restore.py` script.

- Certain schema changes don't need a migrator and will work
  automatically: new models, new fields (when they have a default
  value), `unique` constraints, ...

- If there were unhandled schema changes, you will get error messages.
  No reason to panic. Just correct your code and try again.  You can
  run the :xfile:`restore.py` script as often as needed until there
  are no more errors.

There are two ways for correcting your code: either by locally
modifying your :xfile:`restore.py` script or by writing a migrator.


Modifying :xfile:`restore.py` script
====================================

Locally modifying a :xfile:`restore.py` script is the natural way when
there is only one production site who needs to be migrated. It is a
common situation when a new customer project has gone into production
but is being used only on that customer's site.

Look at the code of your :xfile:`restore.py` script.

For example if a model or field has been removed, you can just comment
out one line in that script.

See also :doc:`dump2py`.


Writing a migrator
==================

- Increase your version number
- 

