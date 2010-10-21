Installing Lino
===============

This page is work in progress.
Don't hesitate to contact me if you get stucked.

WARNING: Don't apply the instructions on this page without understanding what you are doing!

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
copy these files from one of the subdirs of :file:`/var/snapshots/lino/lino/demos`.

Adapt :xfile:`settings.py` to your needs.
Consider using a simplified version of :xfile:`settings.py` that 
imports settings from one of the Lino demos. 
For example::

  from os.path import join
  from lino.demos.dsbe.settings import *
  DATA_DIR = '/usr/local/django/myproject'
  DATABASES = {
      'default': {
          'ENGINE': 'django.db.backends.sqlite3',
          'NAME': join(DATA_DIR,'myproject.db')
      }
  }
  
  
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
  
You'll also need to configure Apache to do HTTP authentication: :doc:`ApacheHttpAuth`.


Static files
------------

Lino uses 4 sets of static files:

================= =========================================== ============================================
Prefix            Description                                 location                
================= =========================================== ============================================
/media/extjs/     ExtJS library                               /var/snapshots/ext-3.2.1/ 
/media/lino/      lino.js and lino.css                        /var/snapshots/lino/lino/ui/extjs/media/
/media/cache/     files generated and served by 
                  lino.modlib.documents                       /var/snapshots/lino/lino/demos/dsbe/media/ 
/media/beid/      image files for dsbe.models.PersonDetail    ... 
================= =========================================== ============================================

The prefixes are currently not configurable.

For the development server, these mappings are done automatically in `urls.py`. 

On a production server you'll probably add an ``Alias /media/ /usr/local/django/myproject/media/`` 
directive in your Apache config, and then use symbolic links in :file:`/usr/local/django/myproject/media/`::

  mkdir /usr/local/django/myproject/media
  cd /usr/local/django/myproject/media
  mkdir pdf_cache
  ln -s /var/snapshots/lino/lino/ui/extjs/media lino
  ln -s /var/snapshots/ext-3.2.1 extjs


User permissions
----------------

You'll probably need to do something like this afterwards::

  # chgrp -R www-data /var/snapshots /var/log/lino /usr/local/django
  # chmod -R g+s /var/snapshots /var/log/lino  /usr/local/django

``chmod g+s`` sets the SGID to ensure that when a new file is created in the directory it will inherit the group of the directory.

Maybe you'll also add `umask 002` to your `/etc/apache2/envvars`. 
For example if `lino.log` doesn't exist and Lino creates it, you may want it to be writable by group.

And then add in your `/etc/mercurial/hgrc`::

  [trusted]
  groups = www-data

You'll maybe have to do something like this::

  # addgroup YOURSELF www-data
  
It may be useful to tidy up::

  $ find /var/snapshots/ -name '*.pyc' -delete


Apply a patch for Django
------------------------

(This is probably no longer necessary)

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


Create the demo database
------------------------

Go to your `/usr/local/django/myproject` directory and run::

  python manage.py initdb demo
  python manage.py runserver

Currently there is also an unelegant thing to do by hand::

  chgrp www-data /usr/local/django/myproject/data/myproject.db
  chmod -R g+w /usr/local/django/myproject

Updating your Lino to the newest version
----------------------------------------

::

  cd /var/snapshots/lino
  hg pull -u


