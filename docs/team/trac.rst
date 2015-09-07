====================
Our ticketing system
====================

Obsolete. We now use `Lino Noi <http://noi.lino-framework.org/>`__ as
ticketing system.

.. glossary::

  trac

    Trac is our ticketing system.  When we say :term:`trac`, then we
    usually mean our public trac environment at
    http://trac.lino-framework.org

  milestone

    In :term:`trac` we can define "milestones". 

    "When you file the ticket, you (the ticket submitter) use the
    version field to indicate the version of the software that
    exhibits the defect. Once the software maintainer triages the
    ticket, they assign it to a milestone that indicates the time
    frame in which the defect will be fixed. The ticket can be
    re-assigned from one milestone to another depending on project
    schedule, but the version number will remain the same. Version
    numbers refer to things that have already been released, and
    milestones refer to things that are in development or planned for
    the future and not yet started."  (user "bta" on stackoverflow in
    `Proper way to use versions and milestones
    <http://stackoverflow.com/questions/7489580/proper-way-to-use-versions-and-milestones>`_)

    Every milestone represents either an :term:`upgrade` or a
    :term:`release`.

  release

    A release is when a given project gets a new version number and is
    published on PyPI. We do this using the :cmd:`fab release`
    command.


  upgrade

    An upgrade is when the Lino installation at a given :term:`site` gets
    upgraded.

  site

    A *site* is a "Django project" running on a given server.


Rules
=====

Every :term:`upgrade` and every :term:`release` should get a
:term:`milestone` in :term:`trac`.

Neither upgrades nor releases are not strictly scheduled. We do them
when they are ready.

Upgrades are not the same as releases. For example, a release implies
a new product version.


Naming milestones
-----------------

*Release milestones* are named ``XXXX-version``, where XXXX is our
internal codename (atelier, lino, welfare...) and version is a string
like "1.6.18".

*Upgrade milestones* are named ``XXXX-YYYY-MM``, where

- `XXXX` represents the :term:`site` (these are named using short
  names like "dsbe", "chat", "lf", "eiche", "fijal" and so on).

- `YYYY-MM` the month of the (initial) schedule date. 

- If there is more than one upgrade for a given site in a given month,
  then we add a sequence number: "XXXX-YYYY-MM-2"


