Coming
======

New features
------------

- Lino applications can now be located somewhere else than on "/".

Bugs fixed
----------



Upgrade instructions
--------------------

The following are technical instructions related to this 
upgrade, designed to be executed by a Lino expert.
For more general instructions on how to upgrade an existing 
Lino site, see :doc:`/admin/upgrade`.

- In your local :xfile:`settings.py`, find the line::

    LINO = Lino(__file__)
    
  and change it to::
  
    LINO = Lino(__file__,globals())
    
  The result is that Lino will also adapt the 
  settings FIXTURE_DIRS, MEDIA_ROOT and TEMPLATE_DIRS for you. 
  You should no longer reassign these later in your :xfile:`settings.py`.


- Database migration: 

