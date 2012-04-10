Running Lino under Apache
=========================
 
Set up Apache and `mod_wsgi`
----------------------------

Create a file `wsgi.py` in your project directory::

  import os

  os.environ['DJANGO_SETTINGS_MODULE'] = 'myproject.settings'

  import django.core.handlers.wsgi
  application = django.core.handlers.wsgi.WSGIHandler()

And in your Apache config file::
  
  <VirtualHost *:80>
    ServerName myproject.example.com
    ServerAdmin webmaster@example.com
    
    WSGIDaemonProcess myproject processes=2 threads=15
    #WSGIDaemonProcess myproject threads=15
    WSGIProcessGroup myproject
    WSGIScriptAlias / /usr/local/django/myproject/wsgi.py
    WSGIApplicationGroup %{GLOBAL}

    Alias /media/ /usr/local/django/myproject/media/
    <Location /media/>
       SetHandler none
    </Location>
  </VirtualHost>  
  

The `WSGIApplicationGroup %{GLOBAL}` instruction 
is necessary when your Lino application uses :term:`lxml`. 
It tells mod_wsgi to not use multiple Python interpreters 
(a feature that is not supported by lxml).

If you run multiple Django sites on your Apache server 
and need `WSGIApplicationGroup %{GLOBAL}`, 
then you *must* use daemon mode and delegate 
each Django site to a separate `WSGIProcessGroup`. 
(`* <http://stackoverflow.com/questions/3405533/problem-using-wsgiapplicationgroup-global-in-apache-configuration>`_
`* <http://stackoverflow.com/questions/5021424/mod-wsgi-daemon-mode-wsgiapplicationgroup-and-python-interpreter-separation>`_)
It is not possible in that case to have multiple sites on a 
single virtual host using :attr:`lino.Lino.root_url`.


Django docs on Apache and mod_wsgi:

  - http://docs.djangoproject.com/en/dev/howto/deployment/modwsgi/
  - http://code.djangoproject.com/wiki/django_apache_and_mod_wsgi
  - http://code.google.com/p/modwsgi/wiki/IntegrationWithDjango
  - :doc:`/tickets/9`
  - :doc:`/tickets/10`
  
  


Miscellaneous
-------------

You'll probably need to add `umask 002` to your `/etc/apache2/envvars`. 
For example if Lino's `.log` file doesn't exist or gets wrapped, 
`www-data` (the user under which Apache is running) will create a new file, 
and the file should to be writable by other users of the `www-data` group.

When :mod:`initdb <lino.management.commands.initdb>` is done, 
you must check that user `www-data` has write access 
to this file. 
Something like this::

  chgrp www-data /usr/local/django/myproject/myproject.db
  chmod -R g+w /usr/local/django/myproject/myproject.db
  
You'll maybe have to do something like this::

  # addgroup YOURSELF www-data
  

In certain cases it may be useful to tidy up::

  $ find /var/snapshots/ -name '*.pyc' -delete
  
To see which directories are on your Python path::

  python -c "import sys; print sys.path"


Did you know? To watch all log files at once, you can do::

  sudo tail -f /var/log/lino/system.log /var/log/lino/db.log /var/log/apache2/error.log /var/log/apache2/access.log
  
See also the `multitail` package  
  

Set up Mercurial
----------------

Add in your `/etc/mercurial/hgrc`::

  [trusted]
  groups = www-data


