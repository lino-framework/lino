===============
Installing Lino
===============

This page is work in progress.
Don't hesitate to contact me if you get stucked.

WARNING: Don't apply the instructions on this page 
without understanding what you are doing!

Software prerequisites
----------------------

You'll maybe need the following Debian packages installed:

 * Packages needed to download Lino and Django::
 
      mercurial subversion unzip patch

 * Packages needed by Django applications to run in Apache2::

    apache2 apache2-doc apache2-mpm-prefork \
      apache2-utils libexpat1 ssl-cert libapache2-mod-wsgi
      
 * Packages needed by Lino to work::
 
      python-dateutil python-yaml python-cheetah python-docutils
      
      python-reportlab 
      python-imaging 
      python-html5lib
      python-uno

 * If you need to run `watch_tim` as a daemon::
 
      python-daemon
      
 * Some database frontend (choose one):
 
      python-pysqlite2
      mysql-server python-mysqldb
      

Download
--------

Create a directory :file:`/var/snapshots` and go to that directory::

  hg clone https://lino.googlecode.com/hg/ lino

Note: don't run Lino's file `setup.py`, it is not necessary and doesn't work.  

The Django version provided by Debian Lenny `python-django` module is too old for Lino, so you need Django's development version. Get that snapshot as well::

  svn co http://code.djangoproject.com/svn/django/trunk/ django

I also installed 
:term:`ExtJS`, 
:term:`pyratemp`, :term:`Pisa` and :term:`appy_pod` 
into `/var/snapshots/`::

  wget http://extjs.cachefly.net/ext-3.3.1.zip
  unzip ext-3.3.1.zip
  rm ext-3.3.1.zip

  wget http://launchpad.net/appy/0.6/0.6.3/+download/appy0.6.3.zip
  unzip appy0.6.3.zip -d appy-0.6.3
  

.. 

 The following instructions are currently obsolete::
  
  wget http://pypi.python.org/packages/source/p/pisa/pisa-3.0.32.zip
  unzip pisa-3.0.32.zip
  rm pisa-3.0.32.zip
  
  wget http://www.simple-is-better.org/template/pyratemp-0.2.0.tgz
  tar -xvzf pyratemp-0.2.0.tgz
  
  hg clone http://bitbucket.org/andrewgodwin/south/

  wget http://pypi.python.org/packages/source/p/python-daemon/python-daemon-1.5.5.tar.gz
  tar -xvzf python-daemon-1.5.5.tar.gz
  
  wget http://smontanaro.dyndns.org/python/lockfile-0.7.tar.gz
  tar -xvzf lockfile-0.7.tar.gz


Set up your Python path
-----------------------

For example on a Linux system, you can add a 
path configuration file :file:`local.pth` 
to a directory that's already on your 
`Python's path <http://www.python.org/doc/current/install/index.html>`_. 

Here is how 
:file:`/usr/local/lib/python2.5/site-packages/local.pth` (Debian Lenny)
:file:`/usr/local/lib/python2.6/dist-packages/local.pth` (Debian Squeeze)
might look in our example::

  /var/snapshots/lino
  /var/snapshots/django
  /var/snapshots/appy-0.6.3
  /usr/local/django  
  
.. 

  The following lines are probably no longer used::

    /var/snapshots/pisa-3.0.32
    /var/snapshots/pyratemp-0.2.0
    /var/snapshots/south
    /var/snapshots/python-daemon-1.5.5
    /var/snapshots/lockfile-0.7

To see which directories are on your Python path::

  python -c "import sys; print sys.path"


Create mysql user
-----------------

::
    $ sudo aptitude install mysql-server python-mysqldb
    
    $ mysql -u root -p 
    mysql> create database myproject collate latin1_german1_ci;
    mysql> create user 'django'@'localhost' identified by 'pwd';
    mysql> grant all on myproject.* to django with grant option;
    mysql> grant all on test_myproject.* to django with grant option;
    mysql> quit;


Create local Django project
---------------------------

Create your Django project directory 
`/usr/local/django/myproject`, containing files
:xfile:`settings.py`, :file:`__init__.py` and :xfile:`manage.py`.

You may either create your Django project from scratch, or
copy these files from one of the subdirs of 
:file:`/var/snapshots/lino/lino/demos`.

Adapt :xfile:`settings.py` to your needs.
Consider using a simplified version of :xfile:`settings.py` that 
imports settings from one of the Lino demos. 
For example::

  from os.path import join
  from lino.sites.dsbe.settings import *
  DATA_DIR = '/usr/local/django/myproject'
  DATABASES = {
      # 'default': {
      #     'ENGINE': 'django.db.backends.sqlite3',
      #     'NAME': join(DATA_DIR,'myproject.db')
      # }
      'default': {
          'ENGINE': 'django.db.backends.mysql',
          'NAME': 'myproject',
          'USER' : 'django',
          'HOST' : 'localhost',
          'PASSWORD' : 'password'
      }
  }
  
Copy the following bash scripts to 
your Django project directory:

  ============================= =========================================
  :srcref:`start </bash/start>` Manually start all local Lino services
  :srcref:`stop </bash/stop>`   Manually stop all local Lino services
  :srcref:`dump </bash/dump>`   Write a dpy dump of your database
  :srcref:`pull </bash/pull>`   Update local copy of Lino sources 
  ============================= =========================================

  
Apply a patch for Django
------------------------

Lino needs Django ticket `#10808 <http://code.djangoproject.com/ticket/10808>`_
to be fixed, here is how I do it::

  $ cd /var/snapshots/django
  $ patch -p0 < /var/snapshots/lino/patches/10808b-r14404.diff

The expected output is something like this::

  (Stripping trailing CRs from patch.)
  patching file django/db/models/base.py
  (Stripping trailing CRs from patch.)
  patching file django/forms/models.py
  (Stripping trailing CRs from patch.)
  patching file tests/modeltests/model_inheritance/models.py

Read :doc:`/django/DjangoPatches` for more details.

  
  
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

Static files
------------

Lino uses the following types of static files:

=========================== =========================================== ============================================
Prefix                      Description                                 location                
=========================== =========================================== ============================================
/media/extjs/               ExtJS library                               /var/snapshots/ext-3.2.1/ 
/media/lino/                lino.js and lino.css                        /var/snapshots/lino/lino/ui/extjs/media/
/media/cache/               files generated and served by 
                            lino.modlib.documents                       /var/snapshots/lino/lino/demos/dsbe/media/ 
/media/beid/                image files for dsbe.models.PersonDetail    ... 
/media/upload/              Uploaded files                              
/media/webdav/              User-editable files 
/media/webdav/doctemplates  local doctemplates directory
=========================== =========================================== ============================================

The prefixes are currently not configurable.

The development server does these mappings automatically in `urls.py`. 

On a production server you'll probably add an ``Alias /media/ /usr/local/django/myproject/media/`` 
directive in your Apache config, and then use symbolic links in :file:`/usr/local/django/myproject/media/`::

  mkdir /usr/local/django/myproject/media
  cd /usr/local/django/myproject/media
  mkdir cache
  mkdir upload
  mkdir webdav
  mkdir webdav/doctemplates
  ln -s /var/snapshots/lino/media lino
  ln -s /var/snapshots/ext-3.3.1 extjs


User permissions
----------------

You'll probably need to do something like this afterwards::

  # chgrp -R www-data /var/snapshots /var/log/lino /usr/local/django
  # chmod -R g+s /var/snapshots /var/log/lino  /usr/local/django

``chmod g+s`` sets the SGID to ensure that when a new file is created in the directory it will inherit the group of the directory.

Maybe also::

  $ chmod a+x /usr/local/django/myproject/manage.py

Maybe you'll also add `umask 002` to your `/etc/apache2/envvars`. 
For example if `lino.log` doesn't exist and Lino creates it, you may want it to be writable by group.

And then add in your `/etc/mercurial/hgrc`::

  [trusted]
  groups = www-data

You'll maybe have to do something like this::

  # addgroup YOURSELF www-data
  
It may be useful to tidy up::

  $ find /var/snapshots/ -name '*.pyc' -delete




Installing startup scripts 
--------------------------

:srcref:`oood </bash/oood>`  Start/Stop OpenOffice (LibreOffice) in server mode
:srcref:`watch_tim </bash/watch_tim>`  Start/Stop `watch_tim` daemon

OpenOffice.org server 
=====================

See also :doc:`/blog/2010/1116`. But basically:

- Install a headless version > 2.3 of openoffice or libreoffice

- Install the startup script::

    # cp /var/snapshots/lino/bash/oood /etc/init.d
    # nano /etc/init.d/oood
  
  Check whether everything is correct, then::

    # chmod 755 /etc/init.d/oood
    # update-rc.d oood defaults

`watch_tim` daemon
==================

This is only for :term:`TIM` users who use Lino in parallel with TIM. 
`watch_tim` keeps an individually configured set of data in sync with 
the TIM data.

Create a directory 
:file:`/usr/local/django/myproject/watch_tim` 
and a :file:`/usr/local/django/myproject/watch_tim/run` 
with something like::
  
  #!/bin/bash
  MYPROJECT="myproject"
  PROJECT_DIR="/usr/local/django/$MYPROJECT"
  PID="$PROJECT_DIR/watch_tim/pid"
  DJANGO_SETTINGS_MODULE=$MYPROJECT.settings
  python $PROJECT_DIR/manage.py watch_tim --pidfile $PID /path/to/TIM/changelog
  
Don't forget to do ``chmod 755 watch_tim/run``.

Then, as root, copy Lino's startup template :srcref:`/bash/watch_tim` 
to your :file:`/etc/init.d` directory and edit the copy::

  # cp /var/snapshots/lino/bash/watch_tim /etc/init.d
  # chmod 755 /etc/init.d/watch_tim
  # nano /etc/init.d/watch_tim

In this file you must edit at least the content of variable `MYPROJECT`.
Check manually whether the script works correctly::

  # /etc/init.d/watch_tim start
  # /etc/init.d/watch_tim stop
  # /etc/init.d/watch_tim restart

And finally::

  # update-rc.d watch_tim defaults
  
In case of problems, see also 
:mod:`lino.modlib.dsbe.management.commands.watch_tim`  


Create a demo database
----------------------

Go to your `/usr/local/django/myproject` directory and run::

  python manage.py initdb demo

Currently there is also an unelegant thing to do by hand::

  chgrp www-data /usr/local/django/myproject/data/myproject.db
  chmod -R g+w /usr/local/django/myproject
  
  

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