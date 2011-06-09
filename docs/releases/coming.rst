Coming
======

New features
------------



Bugs fixed
----------

- The "Save" button of the Layout Editor of Detail windows didn't work. Fixed.


Upgrade instructions
--------------------

The following are technical instructions related to this 
upgrade, designed to be executed by a Lino expert.
For more general instructions on how to upgrade an existing 
Lino site, see :doc:`/admin/upgrade`.

- Database migration: 

  - New field `street_prefix` in :class:`lino.modlib.contacts.models.Addressable`. 
    See :doc:`/blog/2011/0609`.

  

  