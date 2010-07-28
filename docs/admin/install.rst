Installing Lino
===============

Lino is in a very early development stage. 
Don't hesitate to contact me if you get stucked.

Note: The string `APP` on this page is to be replaced by either `dsbe` or `igen`, depending on which of the Lino demo applications you chose.

Software prerequisites
----------------------

You'll maybe need the following Debian packages installed:

 * Packages needed to download Lino and Django::
 
      aptitude install mercurial subversion unzip

 * Packages needed by Django to run in Apache2::

    aptitude install apache2 apache2-doc apache2-mpm-prefork \
      apache2-utils libexpat1 ssl-cert libapache2-mod-python


 * Packages needed by Lino to work::
 
    aptitude install python-dateutil python-reportlab \
      python-yaml python-imaging python-html5lib

Download
--------

Create a directory :file:`/var/snapshots` and go to that directory::

  hg clone https://lino.googlecode.com/hg/ lino
  hg clone https://timtools.googlecode.com/hg/ timtools
  hg clone https://lino-APP.googlecode.com/hg/ APP

Note: don't run Lino's file `setup.py`, it is not necessary and doesn't work.  

The Django version provided by Debian Lenny `python-django` module is too old for Lino, so you need Django's development version. Get that snapshot as well::

  svn co http://code.djangoproject.com/svn/django/trunk/ django

I also installed `ExtJS <http://www.extjs.com>`_ and `Pisa <http://www.xhtml2pdf.com/>` into `/var/snapshots/`::

  wget http://www.extjs.com/deploy/ext-3.2.1.zip
  unzip ext-3.2.1.zip
  rm ext-3.2.1.zip

  http://pypi.python.org/packages/source/p/pisa/pisa-3.0.32.zip
  unzip pisa-3.0.32.zip
  rm pisa-3.0.32.zip

Add Lino and other software to your Python path
-----------------------------------------------

For example on a Linux system, you can add a 
path configuration file `snapshots.pth` 
to a directory that's already on your `Python's path <http://www.python.org/doc/current/install/index.html>`_. 

Here is how `/usr/local/lib/python2.5/site-packages/snapshots.pth` might look in our example::

  /var/snapshots/lino
  /var/snapshots/timtools/src
  /var/snapshots/APP
  /var/snapshots/django
  /var/snapshots/pisa-3.0.32

To see which directories are on your Python path::

  python -c "import sys; print sys.path"



Static files
------------

Lino uses 4 sets of static files:

================= =========================================== ============================================
Prefix            Description                                 location                
================= =========================================== ============================================
/media/extjs/     ExtJS library                               /var/snapshots/ext-3.2.1/ 
/media/lino/      lino.js and lino.css                        /var/snapshots/lino/lino/ui/extjs/media/
/media/pdf_cache/ files generated and served by 
                  lino.modlib.documents                       /var/snapshots/lino/media/ 
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


Configure Apache
----------------

Here is a simple example for file :file:`/etc/aspache2/sites-available/default`::

  <VirtualHost *:80>
      SetHandler python-program
      PythonHandler django.core.handlers.modpython
      SetEnv DJANGO_SETTINGS_MODULE APP.demo.settings
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

You may want to run the same command `python manage.py test` in your applications demo directory (:file:`/var/snapshots/APP/APP/demo` or :file:`/var/snapshots/APP/APP/demo`).


Create the demo database
------------------------

Go to your `/var/snapshots/APP/APP/demo` directory and run::

  python fill.py demo
  python manage.py runserver

Currently there is also an unelegant thing to do by hand::

  chgrp www-data /usr/local/lino/APP_demo.db
  chmod g+w /usr/local/lino/APP_demo.db

Updating your Lino to the newest version
----------------------------------------

::

  cd /var/snapshots/lino
  hg pull -u

And the same for each Lino application::

  cd /var/snapshots/APP
  hg pull -u 

You'll maybe have to do something like this::

  addgroup YOURSELF www-data
