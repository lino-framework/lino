Installing Lino
===============

Lino is in a very early development stage. 
Don't hesitate to contact me if you get stucked.

Note: The string `LINO_APP` on this page is to be replaced by either `dsbe` or `igen`, depending on which of the :doc:`Lino demo applications </demos>` you chose to use as template.

Software prerequisites
----------------------

You'll maybe need the following Debian packages installed:

 * Packages needed to download Lino and Django::
 
      aptitude install mercurial subversion unzip

 * Packages needed by Lino to work::
 
    aptitude install python-dateutil python-reportlab \
      python-yaml python-imaging python-html5lib

 * Packages needed by Django to run in Apache2::

    aptitude install apache2 apache2-doc apache2-mpm-prefork \
      apache2-utils libexpat1 ssl-cert libapache2-mod-wsgi
      

Download
--------

Create a directory :file:`/var/snapshots` and go to that directory::

  hg clone https://lino.googlecode.com/hg/ lino
  hg clone https://timtools.googlecode.com/hg/ timtools
  hg clone https://lino-LINO_APP.googlecode.com/hg/ LINO_APP

Note: don't run Lino's file `setup.py`, it is not necessary and doesn't work.  

The Django version provided by Debian Lenny `python-django` module is too old for Lino, so you need Django's development version. Get that snapshot as well::

  svn co http://code.djangoproject.com/svn/django/trunk/ django

I also installed :term:`ExtJS`, `Pisa <http://www.xhtml2pdf.com/>` and :term:`Appy` into `/var/snapshots/`::

  wget http://www.extjs.com/deploy/ext-3.2.1.zip
  unzip ext-3.2.1.zip
  rm ext-3.2.1.zip

  wget http://launchpad.net/appy/0.5/0.5.5/+download/appy0.5.5.zip  
  unzip appy0.5.5.zip -d appy-0.5.5
  
  wget http://pypi.python.org/packages/source/p/pisa/pisa-3.0.32.zip
  unzip pisa-3.0.32.zip
  rm pisa-3.0.32.zip
  
South::  
  
  hg clone http://bitbucket.org/andrewgodwin/south/
  


Set up your Python path
-----------------------

For example on a Linux system, you can add a 
path configuration file `local.pth` 
to a directory that's already on your `Python's path <http://www.python.org/doc/current/install/index.html>`_. 

Here is how :file:`/usr/local/lib/python2.5/site-packages/local.pth` might look in our example::

  /var/snapshots/lino
  /var/snapshots/timtools/src
  /var/snapshots/LINO_APP
  /var/snapshots/django
  /var/snapshots/pisa-3.0.32
  /var/snapshots/appy-0.5.5
  /var/snapshots/south
  /usr/local/django

To see which directories are on your Python path::

  python -c "import sys; print sys.path"


Create local Django project
---------------------------

Create your Django project directory `/usr/local/django/myproject`, containing files
:xfile:`settings.py`, :file:`__init__.py` and :xfile:`manage.py`.

You may either create your Django project from scratch, or
simply link to these files from :file:`/var/snapshots/LINO_APP/LINO_APP/demo`.

::

  ln /var/snapshots/LINO_APP/LINO_APP/demo/__init__.py .
  ln /var/snapshots/LINO_APP/LINO_APP/demo/manage.py .
  
Adapt :xfile:`settings.py` to your needs.
Consider using a simplified version of :xfile:`settings.py` that 
imports settings from LINO_APP::

  from os.path import join
  from LINO_APP.demo.settings import *
  DATA_DIR = '/usr/local/django/myproject'
  DATABASES = {
      'default': {
          'ENGINE': 'django.db.backends.sqlite3',
          'NAME': join(DATA_DIR,'myproject.db')
      }
  }
  


There's also the pseudo command scipts :xfile:`initdb.py`, :xfile:`load_tim.py`, :xfile:`make_staff.py`

::  
  ln /var/snapshots/LINO_APP/LINO_APP/demo/initdb.py .
  ln /var/snapshots/dsbe/dsbe/demo/make_staff.py .
  ln /var/snapshots/dsbe/dsbe/demo/load_tim.py .
  ln /var/snapshots/dsbe/igen/demo/make_invoices.py .

  
  
Set up Apache and `mod_wsgi`
----------------------------

Create a file `apache.wsgi` in `/usr/local/django/myproject`::

  import os

  os.environ['DJANGO_SETTINGS_MODULE'] = 'myproject.settings'

  import django.core.handlers.wsgi
  application = django.core.handlers.wsgi.WSGIHandler()

And in your Apache config file::
  
  <VirtualHost *:80>
    ServerName myproject.example.com
    ServerAdmin webmaster@example.com
    WSGIScriptAlias / /usr/local/django/myproject/apache.wsgi

    ErrorLog /var/log/apache2/myproject.error.log

    # Possible values include: debug, info, notice, warn, error, crit,
    # alert, emerg.
    LogLevel info

    CustomLog /var/log/apache2/myproject.access.log combined
    #ServerSignature On

    Alias /media/ /usr/local/lino/media/
    <Location /media/>
       SetHandler none
    </Location>
  </VirtualHost>  
  


Static files
------------

Lino uses 4 sets of static files:

================= =========================================== ============================================
Prefix            Description                                 location                
================= =========================================== ============================================
/media/extjs/     ExtJS library                               /var/snapshots/ext-3.2.1/ 
/media/lino/      lino.js and lino.css                        /var/snapshots/lino/lino/ui/extjs/media/
/media/pdf_cache/ files generated and served by 
                  lino.modlib.documents                       /var/snapshots/LINO_APP/LINO_APP/demo/media/ 
/media/beid/      image files for dsbe.models.PersonDetail    ... 
================= =========================================== ============================================

The prefixes are currently not configurable.

For the development server, these mappings are done automatically in `urls.py`. 

On a production server you'll probably add an ``Alias /media/ /usr/local/lino/media/`` directive in your Apache config, and then use symbolic links in :file:`/usr/local/lino/media/`::

  mkdir /usr/local/lino/media
  cd /usr/local/lino/media
  mkdir pdf_cache
  ln -s /var/snapshots/lino/lino/ui/extjs/media lino
  ln -s /var/snapshots/ext-3.2.1 extjs


Configure Apache `mod_python`
-----------------------------

Note that `mod_python` is obsolete. On new installations use `mod_wsgi`.
Here is a simple example for file :file:`/etc/aspache2/sites-available/default`::

  <VirtualHost *:80>
      SetHandler python-program
      PythonHandler django.core.handlers.modpython
      SetEnv DJANGO_SETTINGS_MODULE LINO_APP.demo.settings
      PythonOption django.root
      PythonDebug On

      ErrorLog /var/log/apache2/lino-error.log
      # Possible values include: debug, info, notice, warn, error, crit,
      # alert, emerg.
      LogLevel info
      CustomLog /var/log/apache2/lino-access.log combined
      #ServerSignature On

      Alias /media/ /usr/local/lino/media/
      <Location /media/>
         SetHandler none
      </Location>
  </VirtualHost>

You'll also need to configure Apache to do HTTP authentication: [ApacheHttpAuth simple example].

After modifying the apache config, you must restart the daemon:

  /etc/init.d/apache2 restart
 

User permissions
----------------

You'll probably need to do something like this afterwards::

  chgrp -R www-data /var/snapshots /var/log/lino /usr/local/lino
  chmod -R g+s /var/snapshots /var/log/lino  /usr/local/lino

``chmod g+s`` sets the SGID to ensure that when a new file is created in the directory it will inherit the group of the directory.

Maybe you'll also add `umask 002` to your `/etc/apache2/envvars`. For example if `lino.log` doesn't exist and Lino creates it, you may want it to be writable by group.



And then add in your `/etc/mercurial/hgrc`::

  [trusted]
  groups = www-data

I may be useful to tidy up::

  find /var/snapshots/ -name '*.pyc' -delete


Apply a patch for Django
------------------------

Lino needs Django ticket `#10808 <http://code.djangoproject.com/ticket/10808>`_
to be fixed, here is how I do it::

  $ cd /var/snapshots/django
  $ patch -p0 < /var/snapshots/lino/patch/10808b.diff

The expected output is something like this::

  (Stripping trailing CRs from patch.)
  patching file django/db/models/base.py
  (Stripping trailing CRs from patch.)
  patching file django/forms/models.py
  (Stripping trailing CRs from patch.)
  patching file tests/modeltests/model_inheritance/models.py

Read :ref:`django/DjangoPatches` for more details.


Test whether it worked
----------------------

To test whether the Lino framework is okay::

  $ cd /var/snapshots/lino/src/test_apps
  $ python manage.py test -v0
  ..........
  ----------------------------------------------------------------------
  Ran 10 tests in 0.156s

  OK

You may want to run the same command `python manage.py test` in your applications demo directory (:file:`/var/snapshots/LINO_APP/LINO_APP/demo`).


Create the demo database
------------------------

Go to your `/var/snapshots/LINO_APP/LINO_APP/demo` directory and run::

  python fill.py demo
  python manage.py runserver

Currently there is also an unelegant thing to do by hand::

  chgrp www-data /usr/local/lino/LINO_APP_demo.db
  chmod g+w /usr/local/lino/LINO_APP_demo.db

Updating your Lino to the newest version
----------------------------------------

::

  cd /var/snapshots/lino
  hg pull -u

And the same for each Lino application::

  cd /var/snapshots/LINO_APP
  hg pull -u 

You'll maybe have to do something like this::

  addgroup YOURSELF www-data
