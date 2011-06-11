Coming
======

New features
------------


Bugs fixed
----------

- Auto-create of Cities in learning comboboxes is now more strict.

- Optimizations in :mod:`lino.management.commands.diag`.
  See :doc:`/blog/2011/0611`.


Upgrade instructions
--------------------

The following are technical instructions related to this 
upgrade, designed to be executed by a Lino expert.
For more general instructions on how to upgrade an existing 
Lino site, see :doc:`/admin/upgrade`.

- Database migration: 

  - New field `street_prefix` in :class:`lino.modlib.contacts.models.Addressable`. 
    See :doc:`/blog/2011/0609`.

  

  