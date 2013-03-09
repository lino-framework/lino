Getting started
===============

This document is targeted to **Lino application developers**.



If your computer has Python and pip installed, then just type::

  C:\temp> pip install lino
  
  C:\temp> pip install -U lino
  
  C:\temp> pip install -U --find-links http://lino.saffre-rumma.net/dl lino
 
For other situations and methods of installing Lino, 
see :doc:`/admin/index`.

We begin by creating a Django project::

  C:\temp> django-admin startproject mysite
  
In case the above command is new to you, 
we recommend to read
`Part 1 of the Django tutorial
<https://docs.djangoproject.com/en/1.4/intro/tutorial01/>`_,
which applies entirely for a Lino project.

The Django documentation is good,
and it introduces some important notions about
Creating a project,
The development server,
Database setup,
Creating models,
Activating models,
and Playing with the API.

Now take the :xfile:`settings.py` file of your project 
and replace it's content with the following two lines::

  from lino.projects.cosi.settings import *
  SITE = Site(__file__,globals())

That is, we import settings from Lino Così, 
one of the out-of-the-box projects included with Lino.
Then we create a :setting:`SITE` setting which for the moment 
is just an instance of an unmodified :class:`lino.Site` setting object.
This second line occurs in this same form in every 
Lino :xfile:`settings.py` file.

Next we create a database with some content.
This is just one command to type::

  C:\temp> python manage.py initdb_demo

Lino will ask you::

  INFO Started manage.py initdb_demo on u'Unnamed Lino site' (PID 3872). Languages: en, de, fr.
  INFO Using Lino Così 0.1, Lino 1.5.12, Django 1.4.5, Jinja 2.6, Sphinx 1.1.3, python-dateutil 2.1, 
  OdfPy ODFPY/0.9.6, docutils 0.10, suds 0.4, PyYaml 3.10, Appy 0.8.3 (2013/02/22 15:29), 
  Python 2.7.3, Silk Icons 1.3.
  INFO 36 models, 92 actors.
  We are going to flush your database (C:\temp\mysite\mysite\default.db).
  Are you sure (y/n) ?

If you answer "y" here, 
Lino will **delete everything in the given database** 
and replace it with its "factory default" demo data.
That's what we want, so go on and type ``y``::

  Creating tables ...
  Creating table ui_siteconfig
  ...
  Installing custom SQL ...
  Installing indexes ...
  INFO Loading t:\hgwork\lino\lino\ui\fixtures\std.py...
  ...
  INFO Loading t:\hgwork\lino\lino\projects\cosi\fixtures\userman.py...
  Installed 361 object(s) from 14 fixture(s)
  INFO Stopped manage.py initdb_demo (PID 3780)  


Now we can start the development server::

  C:\temp> python manage.py runserver
  
which should output something like::  
  
  Validating models...
  0 errors found
  Django version 1.4.5, using settings 'mysite.settings'
  Development server is running at http://127.0.0.1:8000/
  Quit the server with CTRL-BREAK.

And then point our web browser to http://127.0.0.1:8000/  

Note what the development server does when the first web request arrives::

  INFO Checking /media URLs
  INFO Building C:\temp\mysite\mysite\media\cache\js\lino_000_de.js ...
  [27/Feb/2013 10:42:36] "GET / HTTP/1.1" 200 4465
  [27/Feb/2013 10:42:40] "GET /media/cache/js/lino_000_de.js HTTP/1.1" 200 198655





