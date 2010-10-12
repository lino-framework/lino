Coming release
==============

Changes
-------


Upgrade instructions
--------------------

Nothing special::

  cd /var/snapshots/lino
  hg pull -u
  cd /var/snapshots/dsbe
  hg pull -u
  cd /usr/local/django/myproject
  python manage.py initdb_tim
  python manage.py make_staff luc
  sudo /etc/init.d/apache2 restart
