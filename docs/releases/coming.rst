Coming
======

New features
------------

- New fixture :mod:`pp2lino <lino.apps.dsbe.fixtures.pp2lino>` 
  is a customized data import for a new user in Brussels. 
  How to try it: copy a recent version of your database to 
  :file:`/usr/local/django/myproject/PPv5MasterCopie.mdb`, 
  then run::
    
    cd /usr/local/django/myproject
    python manage.py initdb std all_countries all_cities be all_languages props pp2lino
      
  That is: same as `initdb_demo.sh` except that the last fixture "demo" is 
  replaced by "pp2lino".
  
  The file name expected by the pp2lino fixture is currently hard-coded. 
  Let me know if you prefer another name.
    
  


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

  

  