===============
Installing Lino
===============

To get Lino running on your computer system, you need at least one 
Linux computer that acts as Server. 
The easiest choice is a Debian distribution 
since the following instructions are 
currently rather Debian centrated.

.. note:: 

  This document contains instructions for Linux system administrators.
  Don't apply them without understanding what you are doing.  
  This document is work in progress.
  Please help us to make it better by sending your 
  feedback to the author.  

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

    python-dateutil python-yaml python-cheetah python-docutils python-vobject
    
* Some database frontend (choose one)::

    python-pysqlite2
    mysql-server python-mysqldb
    
* If :attr:`lino.Lino.use_tinymce` is `True` (probably yes)::

    tinymce 
    
* If you run :term:`watch_tim` as a daemon (probably not)::

    python-daemon 
    
* If you want to import data from a legacy `.mdb` file::

    mdbtools



Create directories
------------------

Create the following directories and make them writeable by www-data::

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

python-django

The Django version 1.2.3 provided 
by the Debian Squeeze `python-django` package 
is too old for Lino, so you need either the latest 
released Django version 1.3, or (if you don't 
need production server quality) Django's 
development version. 

To install Django 1.3::

  cd /var/snapshots
  wget http://media.djangoproject.com/releases/1.3/Django-1.3.tar.gz
  tar xzvf Django-1.3.tar.gz
  mv Django-1.3 django


To install Django's latest development snapshot::

  cd /var/snapshots
  svn co http://code.djangoproject.com/svn/django/trunk/ django
  
We recommend to not run Django's :file:`setup.py` since that's 
not needed for Lino and removes flexibility to switch from one 
version to the other. 
Just `Set up your Python path`_ manually (see below).
Comments on this are welcome.

Install other software
----------------------

You'll also need to install
:term:`ExtJS` 
and :term:`appy_pod` 
into `/var/snapshots/`::

  wget http://extjs.cachefly.net/ext-3.3.1.zip
  unzip ext-3.3.1.zip
  rm ext-3.3.1.zip

  wget http://launchpad.net/appy/0.6/0.6.6/+download/appy0.6.6.zip
  unzip appy0.6.6.zip -d appy
  wget http://launchpad.net/appy/0.7/0.7.0/+download/appy0.7.0.zip
  unzip appy0.7.0.zip -d appy
  
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
  

Create a MySQL database
-----------------------

If you decided to use MySQL as database frontend, 
you must now create a database for your project and a 
user ``django@localhost``::

    $ sudo aptitude install mysql-server python-mysqldb
    
    $ mysql -u root -p 
    mysql> create database mysite charset 'utf8';
    mysql> create user 'django'@'localhost' identified by 'my cool password';
    mysql> grant all on mysite.* to django with grant option;
    mysql> grant all on test_mysite.* to django with grant option;
    mysql> quit;
    
See also http://dev.mysql.com/doc/refman/5.0/en/charset-database.html

You want Lino? Which Lino?
--------------------------

Lino is a framework. 
In fact you don't want "just Lino",  
you'll have to decide which Lino application you want.

Soon you will probably want to 
:doc:`write your own Lino application </tutorials/t1>` 
or get somebody else write it for you, 
but in a first step we suggest that you choose one 
of the "batteries included" applications:

- :mod:`lino.apps.dsbe` 
  (a database for social assistants who assist 
  people in finding jobs or education).

- :mod:`lino.apps.igen` 
  (an accounting application focussed on sales) 
  
In fact you don't even need to decide. 
Just pick a random one.
As long as you are just playing around, 
it is easy to switch between these applications 
since the only difference is one line in 
your :xfile:`settings.py` 
(one of the files we are going to create in the following section).


Create a local Django project
-----------------------------

Lino applications are Django projects.
In case you don't know Django, we
suggest that you also read 
`Part 1 of the Django tutorial
<https://docs.djangoproject.com/en/dev/intro/tutorial01/>`_
which applies entirely for a Lino application.
It introduces some important notions about
Creating a project,
The development server,
Database setup,
Creating models,
Activating models,
and Playing with the API.

When that you've done and learned all this, 
modify the file
:xfile:`settings.py`
of your Django project directory 
`/usr/local/django/mysite`.

Replace your :xfile:`settings.py` with the following 
(but maintaining the DATABASES setting you chose during the Django Tutorial)::

.. literalinclude:: settings.py
    
You'll soon learn more about the :xfile:`settings.py` 
file.
For the moment we suppose that you want to get a quick result.

The ``polls`` subdirectory which you maybe created during the Django 
Tutorial is not necessary for now, but you'll need it again 
later.


Create a project from scratch
-----------------------------

You don't need Django's startproject command.
To install a Lino project from scratch, 
we suggest the following :xfile:`__init__.py` and :xfile:`manage.py`.

The :file:`__init__.py` must exist but can be empty::

    touch __init__.py
    
We suggest the following :doc:`optimized </blog/2011/0531>`
:xfile:`manage.py`::

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



Run the test suite
------------------

Try the following command to run Lino's unit test suite on your project::

  python manage.py test
  
Create your database
--------------------

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

  ln -s /var/snapshots/lino/media media/lino
  ln -s /var/snapshots/ext-3.3.1 media/extjs
  ln -s /usr/share/tinymce/www media/tinymce
  
Besides these manual entries, 
the Lino server will 
automatically create other subdirectories 
`cache`, `uploads` and `webdav` in :xfile:`media`.


Start a development server
--------------------------

Now finally we are ready to go::

  python manage.py runserver
  
This should run something like::  
  
  Validating models...

  0 errors found
  Django version 1.4 pre-alpha SVN-16376, using settings 'dsbe.settings'
  Development server is running at http://127.0.0.1:8000/
  Quit the server with CTRL-BREAK.
  
  
Then point a browser to http://127.0.0.1:8000/ 
and enjoy your Lino application.
Congratulations.


As the `Django docs 
<https://docs.djangoproject.com/en/dev/intro/tutorial01/#the-development-server>`_  
say: 

  You've started the Django development server, a lightweight Web server written purely in Python. We've included this with Django so you can develop things rapidly, without having to deal with configuring a production server -- such as Apache -- until you're ready for production.

  Now's a good time to note: DON'T use this server in anything resembling a production environment. 
  It's intended only for use while developing


Where to go from here
---------------------

- We suggest that you read the :doc:`dpytutorial` and play 
  around with some of the fixtures that come with Lino.

- Now you are ready for our :doc:`/tutorials/index` section.

- If you want to seriously install Lino on your server right now,
  read :doc:`install_apache` and get Lino running under `mod_wsgi`.


