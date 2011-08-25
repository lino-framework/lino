===============
Installing Lino
===============

This page is work in progress.
Don't hesitate to contact us (lino-users@googlegroups.com) 
if you get stucked or find documentation bugs.

WARNING: Don't apply the instructions on this page 
without understanding what you are doing!

.. contents:: Table of Contents
   :local:
   :depth: 2


Software prerequisites
----------------------

You'll need the following Debian packages installed:

* Packages needed to download Lino and Django::

    mercurial subversion unzip patch

* Packages needed by Django applications to run in Apache2::

    apache2 apache2-doc apache2-mpm-prefork \
      libexpat1 libapache2-mod-wsgi
      
    ssl-cert       
    
* Packages needed by Lino to work::

    python-dateutil python-yaml python-cheetah python-docutils
    
* Some database frontend (choose one)::

    python-pysqlite2
    mysql-server python-mysqldb
    
* If :attr:`lino.Lino.use_tinymce` is `True` (probably yes)::

    tinymce 
    
* If you run :term:`watch_tim` as a daemon (probably not)::

    python-daemon 
    
* If you want to import data from an `.mdb` file::

    mdbtools
    
*  Maybe openoffice.org::

    openoffice.org-headless
    python-openoffice
  


Create directories
------------------

Create some directories and make them writeable by www-data::

  # mkdir /var/snapshots /var/log/lino /usr/local/django
  # chgrp -R www-data /var/snapshots /var/log/lino /usr/local/django
  # chmod -R g+ws /var/snapshots /var/log/lino  /usr/local/django

``chmod g+s`` sets the SGID to ensure that when a new file is created in the directory 
it will inherit the group of the directory.


Download Lino
-------------

Go to the :file:`/var/snapshots` and do::

  hg clone https://lino.googlecode.com/hg/ lino

Note: don't run Lino's file `setup.py`, it is not necessary and doesn't work.  
Just `Set up your Python path`_ manually (see below).

Install Django
--------------

The Django version 1.2.3 provided 
by the Debian Squeeze `python-django` package 
is too old for Lino, so you need either the latest 
released Django version 1.3, or (if you don't 
need "production server" quality) Django's 
development version. 

To install Django 1.3::

  cd /var/snapshots
  wget http://media.djangoproject.com/releases/1.3/Django-1.3.tar.gz
  tar xzvf Django-1.3.tar.gz
  mv Django-1.3 django


To install Django's latest development snapshot::

  cd /var/snapshots
  svn co http://code.djangoproject.com/svn/django/trunk/ django
  
We recommend to not run Django's setup.py as well since that's 
not needed for Lino and removes flexipility to switch from one 
version to the other. 
Just `Set up your Python path`_ manually (see below).
Comments on this are welcome.

Install other software
----------------------

We also suggest to install
:term:`ExtJS` 
and :term:`appy_pod` 
into `/var/snapshots/`::

  wget http://extjs.cachefly.net/ext-3.3.1.zip
  unzip ext-3.3.1.zip
  rm ext-3.3.1.zip

  wget http://launchpad.net/appy/0.6/0.6.6/+download/appy0.6.6.zip
  unzip appy0.6.6.zip -d appy
  
Note: Lino didn't yet migrate to ExtJS 4.0. See :doc:`/tickets/40`

Install TinyMCE language packs
------------------------------

If you plan to use Lino in another language than English, you must 
manually install language packs for TinyMCE from
http://tinymce.moxiecode.com/i18n/index.php?ctrl=lang&act=download&pr_id=1

Simplified instructions::

  # cd /usr/share/tinymce/www
  # wget http://tim.saffre-rumma.net/dl/tmp/tinymce_language_pack.zip
  # unzip tinymce_language_pack.zip
  
  
Set up your Python path
-----------------------

We suggest to add a 
path configuration file :xfile:`local.pth` 
to a directory that's already on your 
`Python's path <http://www.python.org/doc/current/install/index.html>`_. 
 
=============== ==============================================
OS              Recommended directory
=============== ==============================================
Debian Lenny    :file:`/usr/local/lib/python2.5/site-packages`
Debian Squeeze  :file:`/usr/local/lib/python2.6/dist-packages`
=============== ==============================================

The file :xfile:`local.pth` itself should have the following content::


  /var/snapshots/lino
  /var/snapshots/django
  /var/snapshots/appy
  /usr/local/django  
  

Create mysql database
---------------------

If you decided to use MySQL as database frontend, 
you must now create a database for your project and a 
user ``django@localhost``::

    $ sudo aptitude install mysql-server python-mysqldb
    
    $ mysql -u root -p 
    mysql> create database myproject charset 'utf8';
    mysql> create user 'django'@'localhost' identified by 'my cool password';
    mysql> grant all on myproject.* to django with grant option;
    mysql> grant all on test_myproject.* to django with grant option;
    mysql> quit;
    
create database myproject;
create user 'django'@'localhost' identified by 'my cool password';
grant all on myproject.* to django with grant option;
grant all on test_myproject.* to django with grant option;
quit;


See also http://dev.mysql.com/doc/refman/5.0/en/charset-database.html    


Create local Django project
---------------------------

Create your Django project directory 
`/usr/local/django/myproject`, containing files
:xfile:`settings.py`, :file:`__init__.py` and :xfile:`manage.py`.

You may either create your Django project from scratch 
(as explained in 
`Django's docs <https://docs.djangoproject.com/en/dev/intro/tutorial01/>`_), 
or start with our suggestions.

The :file:`__init__.py` must exist but can be empty::

    touch __init__.py
    
We suggest the following :xfile:`manage.py` (see also :doc:`/blog/2011/0531`)::

    #!/usr/bin/env python
    import os
    prj = os.path.split(os.path.dirname(os.path.abspath(__file__)))[-1]
    os.environ['DJANGO_SETTINGS_MODULE'] = prj + '.settings'

    from django.core.management import execute_manager
    import settings # Required to be in the same directory.
    from django.core.management import setup_environ
    setup_environ(settings)

    if __name__ == "__main__":
        execute_manager(settings)


And here is our suggestion for :xfile:`settings.py`::

    # -*- coding: UTF-8 -*-
    # Django settings for myproject project.
    from os.path import join, dirname
    from lino.apps.dsbe.settings import *

    class Lino(Lino):

        title = u"My first Lino site"
        csv_params = dict(delimiter=',',encoding='utf-16')

    LINO = Lino(__file__,globals())

    LANGUAGE_CODE = 'fr' # "main" language
    LANGUAGES = language_choices('fr','nl','en')

    LINO.appy_params.update(pythonWithUnoPath='/etc/openoffice.org3/program/python')

    LOGGING = dict(filename='/var/log/lino/system.log'),level='DEBUG')
    # some alternative examples:
    # LOGGING = dict(filename=join(LINO.project_dir,'log','system.log'),level='DEBUG')
    # LOGGING = dict(filename=None,level='DEBUG')


    # MySQL
    # DATABASES = {
    #     'default': {
    #         'ENGINE': 'django.db.backends.mysql', 
    #         'NAME': 'myproject',                  
    #         'USER': 'django',                     
    #         'PASSWORD': 'my cool password',               
    #         'HOST': 'localhost',                  
    #         'PORT': 3306,
    #     }
    # }
    
    # sqlite
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite', 
            'NAME': join(LINO.project_dir,'myproject.db')
        }
    }

    # Make this unique, and don't share it with anybody.
    SECRET_KEY = 'cqt^18t(Fb#14a@s%mbtdif+ih8fscpf8l9aw+0ivo2!3c(c%&'
    
    EMAIL_HOST = "mail.example.com"
    #EMAIL_PORT = ""
    

More documentation about the :setting:`LOGGING` setting
in :doc:`lino.utils.log.configure`

Prepare your Django project for Lino
------------------------------------

Lino expects a few subdirectories of your local project directory.
It doesn't create them automatically, so you must do it yourself::

  cd /usr/local/django/myproject
  mkdir config
  mkdir fixtures
  
  mkdir media
  mkdir media/cache
  mkdir media/cache/js
  mkdir media/upload
  mkdir media/webdav
  mkdir media/webdav/doctemplates

The `media` directory 
is the central place where Lino expects static files to be served.
Besides the `cache`, `uploads` and `webdav` directory it must 
contain the following symbolic links::

  ln -s /var/snapshots/lino/media media/lino
  ln -s /var/snapshots/ext-3.3.1 media/extjs
  ln -s /usr/share/tinymce/www media/tinymce


Create a demo database
----------------------

Go to your :file:`/usr/local/django/myproject` directory and run::

  python manage.py initdb std all_countries few_cities all_languages props demo 
  
When using sqlite, 
the :mod:`initdb <lino.management.commands.initdb>` command will create 
the database file whose name is specified in your :setting:`DATABASES` setting.

See also the :doc:`dpytutorial`.


Start a development server
--------------------------

:file:`/usr/local/django/myproject`

  python manage.py test
  
  python manage.py runserver


  
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




OpenOffice.org server 
---------------------

See also :doc:`/blog/2010/1116`. But basically:

- Install a headless version > 2.3 of openoffice or libreoffice::
    
    # aptitude install openoffice.org-headless python-openoffice
    # aptitude install openoffice.org-java-common java-virtual-machine
    
  Check whether everything is correct:
  
    $ python /usr/share/doc/python-openoffice/examples/check-installation
    
  This should output something like::
  
    Starting OOo for listening on pipe,name=uno387349758964
    Will use command ('/usr/lib/openoffice/program/soffice', '-headless', '-norestore', '-accept=pipe,name=uno387349758964;urp;')
    Started OOo with process id 5216

    Now trying to connect to OOo.
    Connecting with context pyuno object (com.sun.star.uno.XInterface)0xa36b354{, supportedInterfaces={com.sun.star.uno.XComponentContext,com.sun.star.container.XNameContainer,com.sun.star.lang.XTypeProvider,com.sun.star.uno.XWeak,com.sun.star.lang.XComponent}}

    Looks good.  

    
- Install the startup script::

    # cp /var/snapshots/lino/bash/oood /etc/init.d
    # chmod 755 /etc/init.d/oood
    # nano /etc/init.d/oood
    
    
  Check the value of the `SOFFICE` environment variable::
  
    SOFFICE=/usr/lib/openoffice/program/soffice  
  
  Finally, run ``update-rc.d`` to have the daemon 
  automatically start when the server boots::

    # update-rc.d oood defaults
    
    
- In your local :xfile:`settings.py`::



`watch_tim` daemon
------------------

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





