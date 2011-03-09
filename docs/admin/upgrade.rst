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
  
  cd /var/snapshots/djangotests
  python runtests.py --settings=test_sqlite