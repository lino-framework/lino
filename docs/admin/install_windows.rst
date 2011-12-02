=====================================
Installing Lino on a Windows computer
=====================================


.. contents:: Table of Contents
   :local:
   :depth: 2


Software prerequisites
----------------------

You'll need the following software installed on your computer:

- `Django <https://www.djangoproject.com/download/>`_. 
  Follow also the instructions 
  in Django's 
  `Quick install guide <https://docs.djangoproject.com/en/dev/intro/install/>`_
  to install Python.
  
- `Mercurial <http://mercurial.selenic.com/>`_, 
  needed because Lino is in a Mercurial repository 
  and doesn't yet provide downloadable official releases.

- You'll sooner or later also probably need the following Python packages :

  - `python-dateutil <http://labix.org/python-dateutil>`_
  - python-yaml
  - python-cheetah 
  - python-vobject

  You may skip this step for now and worry about these packages later.

- If you want WYSYWIG editor for Rich Text fields, 
  you'll need also 
  `TinyMCE <http://www.tinymce.com/>`_.
  If you skip this, set
  :attr:`lino.Lino.use_tinymce` to `False` in your 
  local settings (see later).
    

- Install `ExtJS 3 <http://www.sencha.com/products/extjs3/>`_::

    c:\Documents and Settings> md \snapshots
    c:\Documents and Settings> cd \snapshots
    c:\snapshots> wget http://extjs.cachefly.net/ext-3.3.1.zip
    c:\snapshots> unzip ext-3.3.1.zip 
  
If you don't have `wget`, you can simply paste the link to your browser and then select 
:file:`c:\\snapshots` as download location.  
ExtJS 3.3.1 should be enough, but you can download also 3.4 and later switch between 
them if things don't work as expected::

  c:\snapshots> wget http://www.sencha.com/products/extjs3/download/ext-js-3.4.0/203
  c:\snapshots> unzip ext-3.4.0.zip
  
Note that Lino didn't yet migrate to ExtJS 4.0. See :doc:`/tickets/40`


You'll probably also want :term:`appy_pod` 
so that Lino can generate .pdf, .rtf or .odt documents::


  c:\snapshots> wget http://launchpad.net/appy/0.7/0.7.0/+download/appy0.7.0.zip
  c:\snapshots> unzip appy0.7.0.zip -d appy

Last but not least we install Lino itself::

  c:\snapshots> hg clone https://lino.googlecode.com/hg/ lino

  
Set up your Python path
-----------------------

There are several possibilities to do this, but
ee suggest to create a 
path configuration file :xfile:`local.pth` 
in the :file:`c:\\Python27\\Lib\\site-packages` directory
(or any other directory that's already on your 
`Python's path <http://www.python.org/doc/current/install/index.html>`_). 
 
The file :xfile:`local.pth` is a simple text file and 
should have the following content::

  c:\snapshots\lino
  c:\snapshots\appy
  c:\mypy
  
The directory :file:`c:\\mypy` is the place where you'll hold your local Python projects.

Test whether Lino is installed
------------------------------

::

  c:\mypy> python
  Python 2.7.1 (r271:86832, Nov 27 2010, 18:30:46) [MSC v.1500 32 bit (Intel)] on win32
  Type "help", "copyright", "credits" or "license" for more information.
  >>> import lino
  >>> print lino.welcome_text()
  Lino version 1.3.0 using Python 2.7.1, Django 1.4 pre-alpha SVN-16714, python-dateutil 1.5, Cheetah 2.4.4, docutils 0.7,
   PyYaml 3.08, xhtml2pdf 3.0.32, ReportLab Toolkit 2.4, appy.pod 0.6.7 (2011/06/28 09:13)
   
If things fail: contact me.

You want Lino? Which Lino?
--------------------------

Lino is a framework. 
In fact you don't want "just Lino",  
you'll have to decide which Lino application you want.

Soon you will probably 
:doc:`write your own Lino application </tutorials/t1>` 
or get somebody else write it for you, 
but in a first step we suggest that you choose one 
of the applications that are part of Lino:

- :mod:`lino.apps.dsbe` 
  (a database for social assistants who assist 
  people in finding jobs or education).

- :mod:`lino.apps.igen` 
  (an accounting application focussed on sales) 
  
In fact you don't even need to choose. 
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
suggest that you now follow
`Part 1 of the Django tutorial
<https://docs.djangoproject.com/en/dev/intro/tutorial01/>`_
which applies entirely for a Lino application.
Choose `c:\\mypy\\mysite` for your Django project directory and `mysite.settings`
for your `DJANGO_SETTINGS_MODULE`

The Django documentation is very good, 
and it introduces some important notions about
Creating a project,
The development server,
Database setup,
Creating models,
Activating models,
and Playing with the API.

When you've done and learned all this, we go further.
Replace the :xfile:`settings.py` 
of your project directory 
`c:\\mypy\\mysite`
with the following:

.. literalinclude:: settings.py
    
You'll soon learn more about the :xfile:`settings.py` 
file.
For the moment we suppose that you want to get a quick result.

The ``polls`` subdirectory which you maybe created during the Django 
Tutorial is not necessary for now, but you'll need it again 
later.


Create a project from scratch
-----------------------------

As an alternative to the previous section, in fact you don't need 
Django's `startproject` command.
To install a Lino project from scratch, 
just create the following 
files in your :file:`c:\\mypy\\mysite`:

#.  An empty file :file:`__init__.py` must exist::

      touch __init__.py
    
#.  Our suggestion for an :doc:`optimized </blog/2011/0531>`
    :xfile:`manage.py`:
    
    .. literalinclude:: manage.py


#.  And of course also your :xfile:`settings.py` file from the previous section.

Run the test suite
------------------

Try the following command to run Lino's unit test suite on your project::

  cd \mypy\mysite
  python manage.py test
  
Again: if things fail: contact me.   
 
  
Create your database
--------------------

Go to your 
:file:`c:\\mypy\\mysite`
directory and run::

  python manage.py initdb std all_countries few_cities all_languages props demo 
  
When using sqlite, 
the :mod:`initdb <lino.management.commands.initdb>` command will create 
the database file whose name is specified in your :setting:`DATABASES` setting.


Start a development web server
------------------------------

Open your :xfile:`settings.py` file and add two entries 
:attr:`extjs_root <lino.Lino.extjs_root>`
and
:attr:`extjs_root <lino.Lino.tinymce_root>`::

  class Lino(Lino):

      title = u"My first Lino site"
      csv_params = dict(delimiter=',',encoding='utf-16')
      
      extjs_root = r'c:\snapshots\ext-3.3.1'
      tinymce_root = r'c:\snapshots\tinymce\jscripts\tiny_mce'
      
Lino expects a few subdirectories of your local project directory.
It doesn't create them automatically, so you must do it yourself::

  c:\mypy\mysite> mkdir config
  c:\mypy\mysite> mkdir fixtures
  c:\mypy\mysite> mkdir media
  

Now finally we are ready to go::

  c:\mypy\mysite> python manage.py runserver
  
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
