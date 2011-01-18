Coming
======

New features
------------

- Erster Reiter im Detail von Firmen heißt jetzt "Allgemein" statt "General"
- Person.card_type_text()
- Feld `Alter` sieht jetzt nicht mehr editierbar aus.


Bugs fixed
----------


Upgrade instructions
--------------------

- Upgrade your copy of the Lino sources::

    cd /var/snapshots/lino
    hg pull -u
    
  
- The usual things in your local directory::

    cd /usr/local/django/myproject
    python manage.py initdb_tim
    python manage.py make_staff
  
- Restart Apache::

    sudo /etc/init.d/apache2 restart

