Running Lino under Apache
=========================


Install startup scripts 
-----------------------

Copy the Lino utility scripts to your project directory and make them 
executable::

  cd /usr/local/django/myproject
  cp /var/snapshots/lino/bash/* .
  chmod u+x pull oood manage.py dump start stop watch_tim
  
Explanations:

  ===================================== =========================================
  :srcref:`start </bash/start>`         Manually start all local Lino services
  :srcref:`stop </bash/stop>`           Manually stop all local Lino services
  :srcref:`dump </bash/dump>`           Write a dpy dump of your database
  :srcref:`pull </bash/pull>`           Update your copy of Lino sources 
  :srcref:`oood </bash/oood>`           Start or stop OpenOffice (LibreOffice) in server mode
  :srcref:`watch_tim </bash/watch_tim>` Start or stop the :term:`watch_tim` daemon
  ===================================== =========================================

Afterwards you'll have to manually adapt them:

- `start` and `stop` : remove the line for :term:`watch_tim` if you don't need this.
- `oood` : check the path of OpenOffice / LibreOffice

  
Set up Apache and `mod_wsgi`
----------------------------

Create a file `django.wsgi` in `/usr/local/django/myproject/apache`::

  import os

  os.environ['DJANGO_SETTINGS_MODULE'] = 'myproject.settings'

  import django.core.handlers.wsgi
  application = django.core.handlers.wsgi.WSGIHandler()

And in your Apache config file::
  
  <VirtualHost *:80>
    ServerName myproject.example.com
    ServerAdmin webmaster@example.com
    
    WSGIDaemonProcess example.com processes=2 threads=15
    #WSGIDaemonProcess example.com threads=15
    WSGIProcessGroup example.com
    WSGIScriptAlias / /usr/local/django/myproject/apache/django.wsgi

    ErrorLog /var/log/apache2/myproject.error.log

    # Possible values include: debug, info, notice, warn, error, crit,
    # alert, emerg.
    LogLevel info

    CustomLog /var/log/apache2/myproject.access.log combined
    #ServerSignature On

    Alias /media/ /usr/local/django/myproject/media/
    <Location /media/>
       SetHandler none
    </Location>
  </VirtualHost>  
  

Django docs on Apache and mod_wsgi:

  - http://docs.djangoproject.com/en/dev/howto/deployment/modwsgi/
  - http://code.djangoproject.com/wiki/django_apache_and_mod_wsgi
  - http://code.google.com/p/modwsgi/wiki/IntegrationWithDjango
  - :doc:`/tickets/9`
  - :doc:`/tickets/10`

You'll also need to configure Apache to do HTTP authentication: :doc:`ApacheHttpAuth`.

You'll probably need to add `umask 002` to your `/etc/apache2/envvars`. 
For example if `system.log` doesn't exist or gets wrapped, 
`www-data` (the user under which Apache is running) will create a new file, 
and the file should to be writable by other users of the `www-data` group.

Lino uses the following types of static files:

=========================== =========================================== 
Prefix                      Description                                 
=========================== =========================================== 
/media/extjs/               ExtJS library                               
/media/tinymce/             TinyMCE library                             
/media/lino/                lino.css                                    
/media/cache/               temporary files created by Lino
/media/beid/                image files for dsbe.models.PersonDetail    
/media/uploads/             Uploaded files
/media/webdav/              User-editable files 
=========================== =========================================== 

While the development server does these mappings 
automatically.

On a production server you then add a line like the following 
to your Apache config::

  Alias /media/ /usr/local/django/myproject/media/
  


Miscellaneous
-------------


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


Set up WebDAV
-------------

See :doc:`apache_webdav`