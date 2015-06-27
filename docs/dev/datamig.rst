=========================
Designing data migrations
=========================

Data migration is a complex topic. Django needed until version 1.7
before they dared to suggest a default method to automating these
tasks (see `Migrations
<https://docs.djangoproject.com/en/1.7/topics/migrations/>`_ if you
are curious).  

Lino includes an optional system for managing database migrations
which takes a rather different approach than Django.

This system is based on :doc:`Python serializer </topics/dpy>`.

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
