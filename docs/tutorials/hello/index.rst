.. _lino.tutorial.hello:

===========================
Create a local Lino project
===========================

In this tutorial we are going to create a local Lino project which
inherits from one of the simple :ref:`out-of-the-box projects
<lino.projects>` included with Lino.

We suppose that you have installed Lino the framework as described in
:doc:`/dev/install`.


.. contents::
    :depth: 1
    :local:



The project directory
=====================

Create an empty directory which will become your project directory::

    $ mkdir ~/projects/mysite
    $ cd ~/projects/mysite

Create two files :xfile:`settings.py` and :xfile:`manage.py` in this
directory as described hereafter.


The ``settings.py`` file
========================

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

    That is, you *instantiate* a :class:`Site <lino.core.site.Site>`
    class and store this object as :setting:`SITE` in your Django
    settings. This line will automatically install default values for
    all required Django settings (e.g. :setting:`DATABASES` and
    :setting:`LOGGING`) into your global namespace.

You might add ``DEBUG = True`` or other settings of your choice after
these two lines, but it is not necessary.

More about this in :doc:`/dev/settings`.
    


The ``manage.py`` file
=======================

Now add a :xfile:`manage.py` file with the following content:

.. literalinclude:: manage.py

This is plain traditional Django know-how.  There are many opinions,
tricks, flavors and conventions about Django's :xfile:`manage.py`
files, partly for historical reasons.  Lino does not add any tricks to
the :xfile:`manage.py` file, so you can use your own flavour if you
prefer.


Initial data
=======================

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
make abundant use of so-called *Python fixtures* in order to have a
rich set of "demo data".  We will come back to this in the next
chapter, :doc:`/tutorials/dumpy`.

Collecting static files
=======================

A last thing to do before you can see Lino running as a web
application is to run Django's :manage:`collectstatic` command::

    $ python manage.py collectstatic

The output should be something like this::

    You have requested to collect static files at the destination
    location as specified in your settings:

        /home/myname/tmp/lino_cache/collectstatic

    This will overwrite existing files!
    Are you sure you want to do this?

    Type 'yes' to continue, or 'no' to cancel: yes

    4688 static files copied to '/home/myname/tmp/lino_cache/collectstatic', 0 unmodified.



Actually you need to do this only for your first local Lino project
because static files are the same for every Lino application.  There
are exceptions to this rule, but we can ignore them for the moment.
More about this in :doc:`/dev/cache`.



Start the web server
=======================

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

Next suggested chapter: :doc:`/tutorials/dumpy`.
