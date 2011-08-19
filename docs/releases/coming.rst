Version 1.2.2 (Coming)
======================

New features
------------

#.  out-of-the-box doctemplates
#.  Attendances by Event
#.  New "Create Mail" button on 

Internal optimizations
----------------------


Bugs fixed
----------

Upgrade instructions
--------------------

#.  reorganize local :xfile:`doctemplates` directory as 
    explained in :doc:`/blog/2011/0809`

#.  Lino/DSBE users must run a database migration because 
    we now also use the :mod:`lino.modlib.mails` module. 

The following are technical instructions related to this 
upgrade, designed to be executed by a Lino expert.
For more general instructions on how to upgrade an existing 
Lino site, see :doc:`/admin/upgrade`.

