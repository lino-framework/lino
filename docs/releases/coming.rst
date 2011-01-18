Coming
======

New features
------------


Bugs fixed
----------


Upgrade instructions
--------------------

- Go to your local directory::

    cd /usr/local/django/myproject
    
- Stop application services::

    ./stop
    
- Update the source code::

    ./pull
    
- When a data migration is necessary::

    python manage.py dumpdata --format dpy > fixtures/dYYYMMDD.dpy
    nano fixtures/dYYYMMDD.dpy
    
  Now edit the file (to be documented...), then reset the 
  database and reload the dump::
    
    python manage.py initdb dYYYMMDD
    
  Restart application server (Apache) and `watch_tim`::
    
    ./start
  
