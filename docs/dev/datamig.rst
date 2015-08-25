=========================
Designing data migrations
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

Advantages: 

- Less work needed for developing, maintaining and testing migration code.
- No need to panic if something goes wrong during the migrate, just
  correct your code and try again.


General strategy for handling data migrations
=============================================

- Before upgrading it is useful to have a description of the changes
  that are being applied. Writing such descriptions is job of the
  application maintainer.  In smaller customized database application
  projects this step can be optional. 

- When you upgrade on a production site, always make a dump2py of your
  database before the upgrade.

- After the upgrade, reinitialize your database from that dump by
  running the `restore.py` script.

- Certain schema changes don't need a migrator and will be automatic:
  new models, new fields (when they have a default value), `unique`
  constraints, ...

- If there were unhandled schema changes, you will get error messages.
  You can then start to handle these database changes by either
  locally modifying your `restore.py` script or by writing a migrator.
  You can run the `restore.py` script as often as needed until there
  are no more errors.

Writing a migrator
==================

- Increase your version number
- 

