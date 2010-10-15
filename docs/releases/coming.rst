Coming
======

Changes
-------

- :mod:`lino.modlib.links` has been reactivated.


Upgrade instructions
--------------------

- The local config dir is now in PROJECT_DIR, not in DATA_DIR::

    cd /usr/local/myproject
    mv data/config .


- Upgrade you copy of the Lino sources::

    cd /var/snapshots/lino
    hg pull -u
  
- The usual things for DSBE::

    cd /usr/local/django/myproject
    python manage.py initdb_tim
    python manage.py make_staff luc
  
- Restart Apache::

    sudo /etc/init.d/apache2 restart
