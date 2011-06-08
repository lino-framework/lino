Coming
======

New features
------------

- New fixture :mod:`pp2lino <lino.apps.dsbe.fixtures.pp2lino>` 
  is a customized data import for a new user in Brussels. 
  How to try it: 
  
  Copy a recent version of your database to 
  :file:`/usr/local/django/myproject/PPv5MasterCopie.mdb`
  (the file name is currently hard-coded, let me know if you prefer another name).
  
  Then run::
    
    cd /usr/local/django/myproject
    python manage.py initdb std all_countries all_cities be all_languages props pp2lino
      
  (that is, the same as `initdb_demo.sh` except that the last fixture "demo" is 
  replaced by "pp2lino".)
  


Bugs fixed
----------



Upgrade instructions
--------------------

The following are technical instructions related to this 
upgrade, designed to be executed by a Lino expert.
For more general instructions on how to upgrade an existing 
Lino site, see :doc:`/admin/upgrade`.

- Database migration: 

  - New field `street_prefix` in :class:`lino.modlib.contacts.models.Addressable`. 
    See :doc:`/blog/2011/0609`.

  

  