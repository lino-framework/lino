Coming
======

New features
------------



Bugs fixed
----------


Upgrade instructions
--------------------

- doctemplates: "Konvention Sozialoekonomie.odt" umbenennen nach "art60-7.odt"

- Add `BABEL_LANGS = ['fr']` to :xfile:`settings.py`
  

- Upgrade your copy of the Lino sources::

    cd /var/snapshots/lino
    hg pull -u
    
  
- The usual things in your local directory::

    cd /usr/local/django/myproject
    python manage.py initdb_tim
    python manage.py make_staff
  
- Restart Apache::

    sudo /etc/init.d/apache2 restart

