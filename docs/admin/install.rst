.. _lino.admin.install:

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
    
python-dev python-pip python-virtualenv

    If you host more than one Lino application, then you should 
    use Ian Bicking's virtualenv tool.


tinymce

    If :attr:`lino.Lino.use_tinymce` is `True` (probably yes),
    then Lino's ExtJS UI uses the TinyMCE WYSIWYG text editor.
    
mysqldb-server
mariadb-server

    Needed if you plan to use Django's MySQL backend.
    See :doc:`install_mysql`.


ssl-cert
    
    If you want to run a https server.
    

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

fabric

    Needed if you do certain development tasks using :mod:`atelier.fablib`
    
python-daemon 

    Needed if you run `watch_tim` or some other daemon process
    (probably not).


mysql-python

    Needed if you plan to use Django's MySQL backend.
    See :doc:`install_mysql`.



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

Lino applications need certain third-party Javascript libraries, and
the Lino server comes with a default configuration which instructs the
clients to fetch them from some public location::

  extjs_base_url = "http://extjs-public.googlecode.com/svn/tags/extjs-3.3.1/release/"
  extensible_base_url = "http://ext.ensible.com/deploy/1.0.2/"
  bootstrap_base_url = "http://twitter.github.com/bootstrap/assets/"
  tinymce_base_url = "http://www.tinymce.com/js/tinymce/jscripts/tiny_mce/"

On a production server you will probably want to serve them yourself.
Here is how to do this.

First you must download them::

  cd /var/snapshots/

  wget http://extjs.cachefly.net/ext-3.3.1.zip
  unzip ext-3.3.1.zip
  rm ext-3.3.1.zip
  
  wget https://github.com/downloads/bmoeskau/Extensible/extensible-1.0.1.zip
  unzip extensible-1.0.1.zip
  rm extensible-1.0.1.zip

  # wget http://twitter.github.com/bootstrap/assets/bootstrap.zip
  wget http://getbootstrap.com/2.3.2/assets/bootstrap.zip
  unzip bootstrap.zip
  
Then in your :file:`settings.py` (or your :file:`djangosite_local.py`)
you must tell Lino to use these files instead of the default
locations::

  SITE = Site(globals())
  SITE.extjs_base_url = None
  SITE.extjs_root = '/var/snapshots/ext-3.3.1'

  SITE.extensible_base_url = None
  SITE.extensible_root = '/var/snapshots/extensible-1.0.1'

  SITE.bootstrap_base_url = None
  SITE.bootstrap_root = '/var/snapshots/bootstrap'

  SITE.tinymce_base_url = None
  SITE.tinymce_root = '/usr/share/tinymce/www'


Notes:

- If the `xxx_base_url` is not empty, Lino will use it

- Otherwise, Lino will check (once, at server startup) whether a
  subdirectory xxx exists in your media directory. If not, it will
  create symbolic links to `xxx_root` in your media directory.

Attention: In versions after 201401 the configuration has changed,
these settings are now in their respective plugin (except for tinymce
which is not yet converted to a plugin). Your :xfile:`settings.py`
should look like this::

    SITE = Site(globals())

    JSLIBS = '/var/snapshots/'

    SITE.configure_plugin(
        'extensible',
        media_root=JSLIBS+'extensible-1.0.1',
        media_base_url=None)

    SITE.configure_plugin(
        'plain',
        media_root=JSLIBS+'bootstrap',
        media_base_url=None)

    SITE.configure_plugin(
        'extjs',
        media_root=JSLIBS+'ext-3.3.1',
        media_base_url=None)


  
 
  
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
  
  
