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

    $ mkdir ~/projects/mysite
    $ cd ~/projects/mysite

Create two files :xfile:`settings.py` and :xfile:`manage.py` in this
directory as described hereafter.


The ``settings.py`` file
-------------------------

Your first :xfile:`settings.py` file should look as follows:

.. literalinclude:: settings.py

Explanations:

#.  :mod:`lino.projects.min1` is one of the simple 
    :ref:`out-of-the-box projects
    <lino.projects>` included with Lino.

    We import these settings directly into our global namespace using
    the wildcard ``*``. This is necessary because that's how Django
    wants settings.
   
#.  Then comes the important trick which turns your Django project
    into a Lino application::

       SITE = Site(globals(), ...)

    That is, you **instantiate** a :class:`Site
    <lino.core.site.Site>` class and store this object as
    :setting:`SITE` in your Django settings. It will set default
    values for all required Django settings (e.g. :setting:`DATABASES`
    and :setting:`LOGGING`).  More about this in :ref:`settings`.
    
You might add ``DEBUG = True`` or other settings of your choice.


The ``manage.py`` file
----------------------

It's not absolutele necessary, but we suggest that you also add a
:xfile:`manage.py` file with the following content:

.. literalinclude:: manage.py

This is plain traditional Django know-how.  There are many opinions,
tricks, flavors and conventions about Django's :xfile:`manage.py`
files, partly for historical reasons.  Lino does not add any tricks to
the :xfile:`manage.py` file, so you can use your own flavour if you
prefer.


Initial data
------------

Next we create your database and populate it with some demo content.

With a normal Lino application this is just one command to type::

    $ python manage.py initdb_demo

That is, you run the :manage:`initdb_demo` management command that
comes with every Lino application.

It will ask you::

    INFO Started manage.py initdb_demo (using settings) --> PID 28463
    INFO This is yet another Lino site using Lino 1.6.17, Django 1.6.9, Python 2.7.4, Babel 1.3, Jinja 2.7.3, Sphinx 1.3b3, python-dateutil 2.1, OdfPy ODFPY/0.9.6, docutils 0.11, suds 0.4, PyYaml 3.10, Appy 0.9.0 (2014/06/23 22:15).
    INFO Languages: en, de. 12 apps, 26 models, 81 actors.
    We are going to flush your database (/home/luc/hgwork/lino/docs/tutorials/hello/default.db).
    Are you sure (y/n) ?

If you answer "y" here, then Lino will delete everything in the given
database and replace it with its "factory default" demo data.  Yes,
that's what you want. So go on and type ``y``::

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

Congratulations! Enjoy the first Lino application running on your
machine!
