Upgrading Lino
==============

Generic instructions for upgrading an existing Lino site 
to a new version.


- Go to your local directory::

    cd /usr/local/django/myproject
    
- Stop application services::

    ./stop
    
- Update the source code::

    ./pull

- Optionally run the test suite using your 
  local :xfile:`settings.py`::
  
    python manage.py test
    
- When a data migration is necessary, see 
  :doc:`/admin/datamig`



How to install updates
----------------------

Updating Lino::

  cd /var/snapshots/lino
  hg pull -u

Updating Django::

  cd /var/snapshots/django & svn update
  
To run the Django test suite::  
  
  cd /var/snapshots/django/tests
  python runtests.py --settings=test_sqlite
  

    
  
Reverting to a previous version
-------------------------------

You can consult :file:`/var/log/lino/pull.log` to see a history of 
your pulls and find out the revision you want to revert to.

If for example your want to revert to :doc:`/releases/20110906`, 
whose revision number is 38d7d51f3f71, then type::

  cd /var/snapshots/lino
  hg revert -r 38d7d51f3f71 --all
  
  