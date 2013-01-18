Database Migration
==================

When an end-user upgrades to a newer version of 
a Lino application or Lino itself, or when they change 
certain parameters in their local :xfile:`settings.py`,
then this might require a **change in the database structure**.

Lino comes with a data migration system using :doc:`/topics/dumpy`.
It's not mandatory but we recommend it.

For the end-user it is easy to use:

- Before upgrading or applying configuration changes, 
  create a backup using 
  :mod:`dumpdata <lino.management.commands.dumpdata>`,
  redirecting the output to a uniquely named file in 
  your local fixtures directory. For example::
  
    $ python manage.py dumpdata --format py > fixtures/b20130117.py
    
  (Where `b20130117.py` means "backup made 2013-01-17")
  
- After upgrading or applying configuration changes, 
  run :mod:`initdb <lino.management.commands.initdb>` 
  on that backup.
  For example:::
  
    $ python manage.py initdb b20130117



See :doc:`/admin/datamig`.

