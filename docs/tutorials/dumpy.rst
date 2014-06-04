.. _lino.tutorial.dpy:

============================
Playing with Python fixtures
============================

This tutorial explains what :ref:`dpy` are and shows how to use them.


.. _dpy:

Python fixtures
---------------

Python fixtures are one of the important concepts which Lino adds to a
Django project.  They are useful for unit tests, application
prototypes and demonstrative examples.

You know that a *fixture* is a portion of data (a collection of data
records in one or several tables) which can be loaded into a database.
Read more about fixtures in the `Providing initial data for models
<https://docs.djangoproject.com/en/dev/howto/initial-data/>`_ article
of the Django documentation.  This article says that "fixtures can be
written as XML, YAML, or JSON documents".  Well, Lino adds another
format to this list: Python.  Here is a fictive minimal example::

  from myapp.models import Foo
  def objects():
      yield Foo(name="First")
      yield Foo(name="Second")

A Python fixture is syntactically a normal Python module, stored in a
file ending with `.py` and designed to being imported and exectued
during Django's `loaddata
<https://docs.djangoproject.com/en/dev/ref/django-admin/#django-admin-loaddata>`_
command.


How it works
------------
  
Django will associate the `.py` ending to 
the North deserializer because your
`SERIALIZATION_MODULES 
<https://docs.djangoproject.com/en/dev/ref/settings/#serialization-modules>`_
setting contains `{"py" : "north.dpy"}`.

The North deserializer expects every Python fixture to define 
a global function `objects` which it expects to return 
(or `yield <http://stackoverflow.com/questions/231767/the-python-yield-keyword-explained>`_)
the list of model instances to be added to the database. 

Vocabulary:

- a *serializer* is run by the 
  `dumpdata <https://docs.djangoproject.com/en/dev/ref/django-admin/#dumpdata-appname-appname-appname-model>`_ 
  command and 
  dumps data into a file which can be  used as a fixture.
  
- a *deserializer* is run by 
  `loaddata <https://docs.djangoproject.com/en/dev/ref/django-admin/#django-admin-loaddata>`_ 
  and loads fixtures into the database.
  
  
Note that you cannot use relative imports in a Python fixture.
See `here 
<http://stackoverflow.com/questions/4907054/loading-each-py-file-in-a-path-imp-load-module-complains-about-relative-impor>`__
  
Discussion
----------
  
Concept and implementation of Python fixtures is fully the author's
work, and we didn't yet find a similar approach in any other
framework.  But the basic idea of using Python language to describe
data collections is of course not new.

- For example Limodou published a Djangosnippet in 2007 which does
  something similar: `db_dump.py - for dumpping and loading data from
  database <http://djangosnippets.org/snippets/14/>`_.

- http://code.djangoproject.com/ticket/10664



The :manage:`initdb` and :manage:`initdb_demo` commands
-------------------------------------------------------

Remember that we told you (in :ref:`lino.tutorial.hello`) 
to "prepare your database" by running the command::

  $ python manage.py initdb_demo
  
The :xfile:`manage.py` Python script is the standard Django interface 
for running a so-called management command.
If you don't know what *management commands* are, 
please read this:
`django-admin.py and manage.py 
<https://docs.djangoproject.com/en/dev/ref/django-admin/>`_.

The :manage:`initdb_demo` 
command which we used here is a `custom management command 
<https://docs.djangoproject.com/en/dev/howto/custom-management-commands/>`_ 
provided by Lino.
It does nothing else than to call 
:manage:`initdb` with the **demo fixtures**.

The **demo fixtures** is a predefined set of fixture names,
defined by the application developer in 
the :setting:`demo_fixtures` setting.
The `min1` app has the following demo fixtures:

    >>> import os
    >>> os.environ['DJANGO_SETTINGS_MODULE'] = 'lino.projects.min1.settings'
    >>> from django.conf import settings
    >>> settings.SITE.demo_fixtures
    'std demo'

So the ``initdb_demo`` command above is equivalent to::
  
  $ python manage.py initdb std demo

The :manage:`initdb` command
----------------------------

The :manage:`initdb` command performs three actions in one:

- a flush of your database, removing *all existing tables* 
  (not only Django tables)
  from the database specified in your :xfile:`settings.py`,
 
- then runs Django's `syncdb` command to re-create all tables,

- and finally runs Django's `loaddata` command to load 
  the specified fixtures.

Removing all existing tables
may sound dangerous, but that's what we want when we have a 
:doc:`Python dump </topics/dumpy>` to restore our database.
Keep in mind that you should rather not let 
Lino and some other application share the same database.

So the above line is roughly equivalent to::

  $ python manage.py flush
  $ python manage.py syncdb
  $ python manage.py loaddata std all_countries few_cities all_languages props demo 
  
Have a look at the following fixture files

- :srcref:`few_countries </lino/modlib/countries/fixtures/few_countries.py>`
  and :srcref:`all_countries </lino/modlib/countries/fixtures/all_countries.py>`

- :srcref:`few_languages </lino/modlib/countries/fixtures/few_languages.py>`
  and :srcref:`all_languages </lino/modlib/countries/fixtures/all_languages.py>`

- :srcref:`few_cities </lino/modlib/countries/fixtures/few_cities.py>`
  and :srcref:`be </lino/modlib/countries/fixtures/be.py>`.

Play with them::

  python manage.py initdb std all_countries be few_languages props demo 
  python manage.py initdb std few_languages few_countries few_cities demo 
  ...



Writing your own fixture
------------------------

Create a directory `fixtures` in your local project directory::

   mkdir ~/mysite/fixtures
   
Create a file `dumpy1.py` in that directory as the following.
But put your real name and data, this is your local file.

.. literalinclude:: dumpy1.py
    :linenos:
    
   
Try to apply this fixture::    

  $ python manage.py initdb dumpy1
  Gonna flush your database (myproject).
  Are you sure (y/n) ?y
  INFO Lino initdb ('dumpy1',) started on database myproject.
  INFO Lino version 1.1.11 using Python 2.7.1, Django 1.4 pre-alpha SVN-16280, 
  python-dateutil 1.4.1, Cheetah 2.4.4, docutils 0.7, PyYaml 3.08, 
  pyratemp (not installed), xhtml2pdf 3.0.32, ReportLab Toolkit 2.4, 
  appy.pod 0.6.6 (2011/04/26 20:50)
  No fixtures found.
  INFO Saved 2 instances from t:\hgwork\lino\docs\tutorials\dumpy1.py.
  Installed 1 object(s) from 1 fixture(s)
  INFO Lino initdb done ('dumpy1',) on database t:\data\luc\lino\dsbe\dsbe_test.db.


Second step
-----------

Since `.py` fixtures are normal Python modules, there are 
no limits to our phantasy when creating new objects.

A first thing that drops into mind is: there should be a more compact 
way to create many records of a same table. That's why 
:class:`lino.utils.instantiator.Instantiator` was written.
Here is the same fixture in a more compact way:

.. literalinclude:: dumpy2.py
    :linenos:


Third step
----------

Play around and try to add some more objects to your local demo database!


The default demo fixtures
-------------------------

The :ref:`cosi` application developer had decided that a 
demo site should by default load just *this* set of fixtures.
How did he do that?
Look at the source code of  
:srcref:`/lino/projects/min1/settings/__init__.py`
where he overrides the 
:setting:`demo_fixtures` 
attribute of his :class:`Site` 
class, setting it to::

    demo_fixtures = 'std few_countries few_cities few_languages furniture demo demo2'.split()


Conclusion
----------

Python fixtures are an important tool for application developers
because 

- they are more flexible than json or xml fixtures and easy to adapt 
  when your database structure changes.
  
- they provide a simple interface to deploy demo data for an application


