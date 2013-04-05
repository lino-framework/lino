====================================================
Installing a Lino application on a production server
====================================================

.. include:: /include/needs_update.rst


Before setting up a production server you should be familiar 
with setting up and running a development server
as documented in :ref:`lino.dev.install`.

For a Lino production server you'll need a Linux computer that acts as server.

Basically you do the same as for Django. 
We recommend the method using `mod_wsgi` and `virtualenv` 
as described in the following documents:

- https://docs.djangoproject.com/en/dev/howto/deployment/wsgi/modwsgi/
- https://code.google.com/p/modwsgi/wiki/VirtualEnvironments


Debian packages
---------------

You'll need the following Debian packages installed:

* Packages needed by Django applications to run in Apache2::

    apache2 apache2-doc apache2-mpm-prefork libexpat1 libapache2-mod-wsgi
      
    ssl-cert       
    
* Packages needed by Lino to work::

    python-virtualenv

* If :attr:`lino.Lino.use_tinymce` is `True` (probably yes)::

    tinymce
    
* If you run :term:`watch_tim` as a daemon (probably not)::

    python-daemon 
    
* If you want to import data from a legacy `.mdb` file::

    mdbtools

* Packages needed to download Lino and Django::

    mercurial subversion unzip patch


Install Lino
------------

Create and activate a virtualenv for your Lino application, 
then install Lino using pip::

  $ pip install lino



Test whether Lino is installed
------------------------------

::

  $ python
  Python 2.7.1 (r271:86832, Nov 27 2010, 18:30:46) [MSC v.1500 32 bit (Intel)] on win32
  Type "help", "copyright", "credits" or "license" for more information.
  >>> import lino
  >>> print lino.welcome_text()
  Using Lino 1.4.4, Django 1.5.dev17937, python-dateutil 1.5, Cheetah 2.4.4, OdfPy ODFPY/0.9.4, docutils 0.7, suds 0.4.1, PyYaml 3.08, Appy 0.8.0 (2011/12/15 22:41), Python 2.7.1.  
  
  
Create a local Lino project
---------------------------

Every Lino project should have at least its own :file:`settings.py` and 
project directory (the directory containing this file).
Local Lino :file:`settings.py` files on production servers 
are usually rather short. Something like::

  from foo.bar.settings import *
  SITE = Site(globals())
   

Serving Javascript frameworks
-----------------------------

On a production server you will probably want to serve yourself 
the third-party Javascript libraries used by Lino.

::

  cd /var/snapshots/

  wget http://extjs.cachefly.net/ext-3.3.1.zip
  unzip ext-3.3.1.zip
  rm ext-3.3.1.zip
  
  wget https://github.com/downloads/bmoeskau/Extensible/extensible-1.0.1.zip
  unzip extensible-1.0.1.zip
  rm extensible-1.0.1.zip

  wget http://twitter.github.com/bootstrap/assets/bootstrap.zip
  unzip bootstrap.zip
  

Then in you settings.py (or your djangosite_local.py) you'll set 
the `lino.ui.Site.extjs_root` attributes accordingly::


  extjs_root = '/var/snapshots/ext-3.3.1'
  extensible_root = '/var/snapshots/extensible-1.0.1'
  bootstrap_root = '/var/snapshots/bootstrap'
  
Lino will use these values to create symbolic links in 
your media directory.
  
  
Install TinyMCE language packs
------------------------------

If you plan to use Lino in another language than English, you must 
manually install language packs for TinyMCE from
http://tinymce.moxiecode.com/i18n/index.php?ctrl=lang&act=download&pr_id=1

Simplified instructions::

  # cd /usr/share/tinymce/www
  # wget http://tim.saffre-rumma.net/dl/tmp/tinymce_language_pack.zip
  # unzip tinymce_language_pack.zip
  
  
Use a MySQL database
--------------------

If you decided to use MySQL as database frontend, 
you must create a database and a 
user ``django@localhost`` for your project.

To install mysql on your site::

    $ sudo aptitude install mysql-server python-mysqldb
    $ pip install MySQL-python
    
For your first project, you create a user::
    
    $ mysql -u root -p 
    mysql> create user 'django'@'localhost' identified by 'my cool password';
    
For each new project::
    
    $ mysql -u root -p 
    mysql> create database mysite charset 'utf8';
    mysql> grant all on mysite.* to django with grant option;
    mysql> grant all on test_mysite.* to django with grant option;
    mysql> quit;
    
See also http://dev.mysql.com/doc/refman/5.0/en/charset-database.html



Run the test suite
------------------

Try the following command to run Lino's unit test suite on your project::

  python manage.py test
  
Initialize your database
------------------------

Go to your :file:`/usr/local/django/mysite` directory and run::

  python manage.py initdb std all_countries few_cities all_languages props demo 
  
When using sqlite, 
the :mod:`initdb <lino.management.commands.initdb>` command will create 
the database file whose name is specified in your :setting:`DATABASES` setting.


Prepare your Django project for Lino
------------------------------------

Lino expects a few subdirectories of your local project directory.
It doesn't create them automatically, so you must do it yourself::

  cd /usr/local/django/mysite
  mkdir config
  mkdir fixtures
  mkdir media
  
Especially the :xfile:`media` directory is important and needs 
your attention. 
It is the central place where Lino expects static files to be served.

You must manually add the following symbolic links in order to 
tell Lino where certain other software is installed on your server::

  cd media
  ln -s ~/snapshots/lino/media lino
  ln -s ~/snapshots/ext-3.3.1 extjs
  ln -s ~/snapshots/extensible-1.0.1 extensible
  ln -s ~/snapshots/bootstrap bootstrap
  ln -s /usr/share/tinymce/www tinymce
  ln -s /usr/share/tinymce/www beid_jslib
  
  cd ..
  
Besides these manual entries, 
the Lino server will 
automatically create other subdirectories 
`cache`, `uploads` and `webdav` in :xfile:`media`.


