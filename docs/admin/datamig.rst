Data migration
==============

Here is how we suggest to migrate data.

Stop application services::

  ./stop
  
Before upgrading, create a dpy dump. Go to your local directory 
and type::

  python manage.py dumpdata --format dpy > fixtures/dYYYMMDD.dpy
  nano fixtures/dYYYMMDD.dpy
  
Now you can upgrade your Lino sources::

  ./pull
  
Depending on on the changes due to the upgrade,
it may (or may not) be necessary to 
edit the dpy file. 
According to the release information.

Then reset the database and reload the dump::
  
  python manage.py initdb dYYYMMDD
  
Restart application server (Apache) and `watch_tim`::
  
  ./start



python manage.py dumpdata --format dpy > fixtures/d20110206.dpy