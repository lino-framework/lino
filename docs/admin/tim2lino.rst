============================
Data import from TIM to Lino 
============================

Initial import::

  $ cd /usr/local/django/myproject
  $ python manage.py initdb_tim /mnt/path/to/tim/data


When this is done, start the process that keeps data synchronized::

  $ cd /usr/local/django/myproject
  $ ./watch_tim > /var/log/lino/watch_tim.log 2>&1 &
  
  
Where :xfile:`watch_tim` contains something like::
 
  python manage.py watch_tim /mnt/path/to/tim/data/changelog