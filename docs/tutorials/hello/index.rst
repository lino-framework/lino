.. _lino.tutorial.hello:

===========================
Create a local Lino project
===========================

In this tutorial we are going to create a local Lino project which
inherits from one of the simple :ref:`out-of-the-box projects
<lino.projects>` included with Lino.

We suppose that you have installed Lino the framework as described in
:ref:`lino.dev.install`.


The project directory
---------------------

Create an empty directory which will become your project directory::

    $ mkdir ~/mysite
    $ cd ~/mysite

Create two files :file:`settings.py` and  :xfile:`manage.py` 
in this directory as described hereafter.

The ``settings.py`` file
-------------------------

Your first :file:`settings.py` file should look as follows:

.. literalinclude:: settings.py

Explanations:

#.  :mod:`lino.projects.min1` is one of the simple 
    :ref:`out-of-the-box projects
    <lino.projects>` included with Lino.

    We import these settings directly into our global namespace using
    the wildcard ``*``. This is necessary because that's how Django
    wants settings.
   
#.  Then we define a :setting:`SITE` setting::

       SITE = Site(globals(), ...)

    This is the important trick which turns your Django project into a
    Lino application.  It will set default values for all required
    Django settings (e.g. :setting:`DATABASES` and
    :setting:`LOGGING`).  More about this in :ref:`settings`.
    
You might add ``DEBUG = True`` or other settings of your choice.


The ``manage.py`` file
----------------------

We suggest the following content for your project's :xfile:`manage.py`
file:

.. literalinclude:: manage.py

This is plain traditional Django know-how.  There are many opinions,
tricks, flavors and conventions about how Django's :xfile:`manage.py`
file should look. Partly for historical reasons.

Lino does not add any tricks to the `manage.py` file.  You can use
your own variant if you prefer.


Initial data
------------

Next we create your database and populate it with some demo content.
This is just one command to type::

    $ python manage.py initdb_demo

That is, you run the :manage:`initdb_demo` management command that
comes with every Lino application.  It will ask you::

  INFO Started manage.py initdb_demo (using mysite.settings) --> PID 3848
  INFO This is Lino Così 0.1 using Python 2.7.3, Django 1.4.5, django-site 0.0.2, North 0.0.2, Lino 1.6.0, Jinja 2.6, Sphinx 1.1.3, python-dat
  eutil 2.1, OdfPy ODFPY/0.9.6, docutils 0.10, suds 0.4, PyYaml 3.10, Appy 0.8.3 (2013/02/22 15:29).
  INFO Languages: en, de, fr. 16 apps, 37 models, 93 actors.
  We are going to flush your database (/home/luc/mysite/mysite/default.db).
  Are you sure (y/n) ?

If you answer "y" here, then Lino will delete everything in the given
database file and replace it with its "factory default" demo data.
That's what you want, don't you? So go on and type ``y``::

  Creating tables ...
  Creating table ui_siteconfig
  ...
  Installing custom SQL ...
  Installing indexes ...
  INFO Loading /home/luc/hgwork/lino/lino/ui/fixtures/std.py...
  ...
  INFO Loading /home/luc/hgwork/lino/lino/projects/cosi/fixtures/userman.py...
  Installed 361 object(s) from 14 fixture(s)
  INFO Stopped manage.py initdb_demo (PID 3780)  


There's a lot to say about what we just did.  Lino applications use to
make abundant use of :ref:`dpy` in order to have a rich set of "demo
data".  If you are curious, then read more about Python fixtures in
:ref:`lino.tutorial.dpy`.



Start the web server
--------------------

Now you can start the development server::

  $ python manage.py runserver
  
which should output something like::  
  
  Validating models...
  0 errors found
  Django version 1.4.5, using settings 'mysite.settings'
  Development server is running at http://127.0.0.1:8000/
  Quit the server with CTRL-BREAK.

And then point our web browser to http://127.0.0.1:8000 and you should
see some welcome text and instructions for logging in.

Congratulations! Enjoy your first Lino application.

