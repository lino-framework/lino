====================================================
Installing a Lino application on a production server
====================================================

Before setting up a production server you should be familiar 
with setting up and running a development server
as documented in :ref:`lino.dev.install`.

For a Lino production server you'll need shell access to a Linux 
computer that acts as server.

Basically you do the same as for Django. 
We recommend the method using `mod_wsgi` and `virtualenv` 
as described in the following documents:

- https://docs.djangoproject.com/en/dev/howto/deployment/wsgi/modwsgi/
- https://code.google.com/p/modwsgi/wiki/VirtualEnvironments


Debian packages
---------------

Some Debian packages and why you might need them:

libapache2-mod-wsgi
  
    This will automatically install Apache 
    (packages apache2 apache2-doc apache2-mpm-prefork libexpat1...)
    
ssl-cert       
    
    If you want to run a https server.
    
python-virtualenv

    If you host more than one Lino application, then you should 
    use Ian Bicking's virtualenv tool.


tinymce

    If :attr:`lino.Lino.use_tinymce` is `True` (probably yes),
    then Lino's ExtJS UI uses the TinyMCE WYSIWYG text editor.
    

Install Lino
------------

- Create a virtualenv for your Lino application

- Activate this environment, then type::

    $ pip install lino
    
    
To test whether Lino is installed, you can write::

    $ python -c "print __import__('lino').__version__"
    
Note: third-party Lino applications 
usually depend on Lino, 
so installing such an application will automatically
install Lino.
For example to install :ref:`welfare`, you can just type::
  
    $ pip install lino-welfare


Optional Python packages  
------------------------
  
The following Python packages (to be installed using `pip install`) 
are optional and therefore not automatically installed:

python-daemon 

    Needed if you run :term:`watch_tim` or some other daemon process 
    (probably not).


mysql-python

    Needed if you plan to use Django's MySQL backend.

    
mdbtools

  If you want to import data from a legacy `.mdb` file


  

Create a local Lino project
---------------------------

Every Lino project should have at least its own :file:`settings.py` and 
project directory (the directory containing this file).
Local Lino :file:`settings.py` files on production servers 
are usually rather short. Something like::

  from foo.bar.settings import *
  SITE = Site(globals())
   
Possible values for ``foo.bar`` are:
:mod:`lino.projects.






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
  

Then in your :file:`settings.py` (or your :file:`djangosite_local.py`) 
you'll set the `FOO_root <lino.ui.Site.extjs_root>` attributes 
accordingly::


  extjs_root = '/var/snapshots/ext-3.3.1'
  extensible_root = '/var/snapshots/extensible-1.0.1'
  bootstrap_root = '/var/snapshots/bootstrap'
  
Lino will use these values to create symbolic links in 
your media directory.

 
  
Install TinyMCE language packs
------------------------------

If you plan to use Lino in other languages than English, you must 
manually install language packs for TinyMCE from
http://tinymce.moxiecode.com/i18n/index.php?ctrl=lang&act=download&pr_id=1

Simplified instructions for a language pack containing 
my personal selection (de, fr, nl and et)::

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


